---
role: Site Reliability / Principal Experimental Physicist
skill: hep-analysis
archetype: postmortem
incident: Overnight MC-production pipeline crashes partway through, corrupting a fraction of output files
---

## 1. Incident Symptom & Alert Payload

The production system emails a digest after each overnight campaign rather
than paging in real time; the morning digest for the `ttbar_2018_full_sim`
campaign read:

```
MC PRODUCTION SUMMARY: ttbar_2018_full_sim
Submitted: 2026-07-09T22:00:00Z  Completed: 2026-07-10T06:14:00Z
Job array: 4000 sub-jobs (HTCondor)
Exit status 0:  3672 jobs
Exit status !=0: 328 jobs (8.2%)
  - 244 jobs: exit code 1 (Geant4RunManager: unhandled std::bad_alloc)
  - 84 jobs:  exit code 0, but output file size < 1 MB (expected ~180 MB)
Output directory: /store/mc/ttbar_2018_full_sim/
Merge step: NOT YET RUN
```

A physicist doing a spot-check the next morning (per
`references/02-data-pipelines.md`'s "run a small schema smoke test before
reading the full production" guidance) found that 84 of the "successful"
(exit code 0) output files were truncated ROOT files with a valid header
but zero or partial entries in the truth tree.

## 2. Immediate Triage & Blast-Radius Mitigation

The merge/skim step (`merge_ttbar_2018_full_sim.py`) had not yet run, so no
downstream analysis code had touched the corrupted files - the on-call
physicist blocked the merge step from starting (per
`references/02-data-pipelines.md`'s "do not silently skip failed remote
files and report a complete sample," the immediate priority was preventing
exactly that from happening automatically). The 328 known-bad job IDs
(244 crashed + 84 silently-truncated) were identified from the digest and a
`root -l -q 'validate.C'` schema check over the full output directory, and
all 328 corresponding files were moved to `/store/mc/_quarantine/` so a
resubmission could safely reuse their job-array indices without colliding
with quarantined files still sitting in the main output directory.

## 3. 5-Whys Root Cause Deep-Dive

1. **Why were 84 output files truncated despite exit code 0?** Because the
   job script copied the output ROOT file to `/store/mc/...` immediately
   after the simulation process exited, without checking whether the file
   had actually closed cleanly.
2. **Why didn't the file close cleanly?** Because the Geant4 job ran out of
   local scratch disk space partway through writing the final digitization
   output, causing the ROOT file's final write (and its I/O record) to fail
   silently at the OS level while the parent process itself still exited 0.
3. **Why did the job run out of local scratch disk?** Because multiple
   sub-jobs from the same array are scheduled onto the same worker node
   concurrently, and each job's temporary Geant4 stepping-output directory
   (`/scratch/g4_tmp/<job_id>/`) was never cleaned up between jobs sharing
   that node, so scratch usage accumulated across jobs rather than being
   released per job.
4. **Why was there no cleanup between jobs on a shared node?** Because the
   job template was written and tested against a one-job-per-node execution
   model; when the batch pool was later reconfigured to pack multiple
   sub-jobs per node for better utilization, the scratch-cleanup step (which
   had previously been implicit - the node was reclaimed between jobs) was
   never added explicitly to the job script.
5. **Why did nothing catch this before it reached "successful" output?**
   Because the production pipeline's automated integrity check only
   verifies exit code, not the output file's own write-completion status
   (e.g. `TFile::IsZombie()` or a checksum against an expected byte range) -
   the exact gap `references/02-data-pipelines.md`'s "audit inputs" guidance
   warns about, but it had only ever been applied by hand to *inputs* being
   read for analysis, never automated as a *production-output* gate.

Root cause: the batch-pool reconfiguration to multi-job-per-node scheduling
silently invalidated an implicit scratch-cleanup assumption the job template
depended on, and the production pipeline had no automated output-integrity
gate that would have caught the resulting truncated files before they were
copied into the "complete" output directory.

## 4. Permanent Surgical Fix (Diff)

```diff
--- a/production/submit_job.sh
+++ b/production/submit_job.sh
@@ -14,8 +14,14 @@ run_geant4_and_digitize() {
   geant4_sim --config "$CONFIG" --output "$LOCAL_TMP/raw_sim.root"
   digitize --input "$LOCAL_TMP/raw_sim.root" --output "$LOCAL_TMP/output.root"
 
-  cp "$LOCAL_TMP/output.root" "$FINAL_OUTPUT_DIR/"
+  root -l -q -b <<'ROOTEOF' || { echo "OUTPUT FILE FAILED INTEGRITY CHECK"; exit 42; }
+  TFile f("$LOCAL_TMP/output.root");
+  if (f.IsZombie() || f.TestBit(TFile::kRecovered)) { gSystem->Exit(1); }
+  gSystem->Exit(0);
+ROOTEOF
+
+  cp "$LOCAL_TMP/output.root" "$FINAL_OUTPUT_DIR/"
+  rm -rf "$LOCAL_TMP/g4_tmp"   # scratch cleanup, now explicit per job regardless of node-sharing
 }
```

The integrity check runs `TFile::IsZombie()` (catches a file that never
opened correctly) and checks the `kRecovered` bit (ROOT sets this when it
had to auto-recover a truncated file, which previously would have looked
like a normal, silently-degraded read) before the file is ever copied to
the final output directory; a job whose output fails this check now exits
42 (a new, distinct exit code from the existing crash code 1) instead of
exit 0, so it is caught by exit-status monitoring rather than requiring a
manual spot-check to discover.

## 5. Blameless Postmortem & Preventative Monitoring Rules

No individual is at fault: the job template's implicit reliance on
per-node job isolation was correct for the batch pool's original
configuration, and the person who later reconfigured the pool for
multi-job-per-node packing had no reason to know a job script two layers
away depended on that isolation - the dependency was never documented or
enforced. The system had no automated way to catch a production-output
integrity failure; only a manual spot-check did, and manual spot-checks are
not a control, they are luck.

**What worked:** the merge step not having run yet meant zero corrupted
data ever reached an analyzer's working area - blocking the merge before
investigating (rather than root-causing first) contained the blast radius
to "wasted compute," not "silently wrong physics results downstream."

**What didn't work:** the only thing that caught the 84 silently-truncated
files was a physicist's habit of running a schema smoke test before
starting analysis work; a production run without that habit would have
merged corrupted entries directly into the analysis sample.

**Preventative monitoring rule:** the production dashboard now alerts and
automatically blocks the merge step if the per-campaign
`clean-output-file-rate` (files passing the new `IsZombie()`/`kRecovered`
integrity check, divided by total jobs with exit code 0) drops below 100%
for any completed campaign, rather than relying on exit-code-0 as a proxy
for a correctly-written file.
