---
role: Site Reliability / Principal Experimental Physicist
skill: hep-analysis
archetype: postmortem
incident: A bad calorimeter calibration-constant payload silently shifted the reconstructed energy scale for one week before an analyzer noticed a mass-peak shift
---

## 1. Incident Symptom & Alert Payload

```
[Analysis group Slack, #dilepton-analysis, 2025-06-02]
"Our Z->ee mass peak has drifted from 91.2 GeV to 89.7 GeV in the last
week's reconstructed data - is anyone else seeing this?"

--- conditions-database change log ---
payload: ECAL_ENERGY_SCALE_2025B
applied_from_run: 483112 (2025-05-26 03:14 UTC)
uploaded_by: calibration-production-pipeline (automated)
validation_status: NOT RUN (auto-upload path bypasses manual sign-off
  queue when previous payload's interval-of-validity has expired)

--- retroactive comparison, once flagged ---
Z->ee peak, runs 482900-483111 (old payload): 91.18 +/- 0.03 GeV
Z->ee peak, runs 483112-483740 (new payload): 89.71 +/- 0.03 GeV
```

The shift affected every run reconstructed with the new payload for a full
week - roughly 40% of that week's total delivered luminosity - before the
analyzer's Slack message was the first signal anyone noticed.

## 2. Immediate Triage & Blast-Radius Mitigation

Per `references/31-calibration-and-alignment.md`'s guidance that "a
calibration update is... not a local change," the on-call calibration
expert's first action was to freeze the automated calibration-production
pipeline (stopping any further payload auto-uploads) and roll the
conditions database back to the previous known-good payload
(`ECAL_ENERGY_SCALE_2025A`) for the affected run range, rather than
attempting to patch the bad payload in place - reverting to a
previously-validated payload is lower-risk than trying to fix an
un-validated one under time pressure. All downstream reconstruction jobs
that had already run against the bad payload (runs 483112-483740) were
flagged in the run registry as requiring reprocessing once the rollback
was confirmed, bounding which data any analysis group could safely use in
the meantime.

## 3. 5-Whys Root Cause Deep-Dive

1. **Why did the reconstructed Z->ee mass peak shift by 1.5 GeV?**
   Because the ECAL energy-scale payload applied starting at run 483112
   contained an absolute-scale constant that was off by approximately
   1.6%, shifting every reconstructed electron/photon energy in that run
   range downward by the same fraction.
2. **Why was the new payload's absolute scale wrong?** Because the
   calibration-production pipeline derives the absolute scale via an
   in-situ Z->ee resonance fit on a control sample, and the control
   sample's event selection for that production cycle picked up a
   contaminated data run (a run with a known, previously-flagged ECAL
   readout timing issue) that biased the fitted resonance position before
   the timing issue's veto was applied.
3. **Why wasn't the contaminated run excluded before it fed into the
   calibration fit?** Because the timing-issue veto list is maintained as
   a separate, manually-curated file that the calibration pipeline reads
   at the *start* of production, and the run in question was added to the
   veto list two days *after* that production cycle had already started -
   the pipeline had no mechanism to pick up a veto-list update mid-run.
4. **Why did the resulting payload reach production data reconstruction
   without a validation check catching the scale error?** Because the
   automated upload path is designed to bypass the manual sign-off queue
   specifically when the previous payload's interval-of-validity has
   expired, on the reasoning that "no calibration is worse than a slightly
   stale one" - but this means an urgently-needed payload skips the same
   sanity check (comparing the new fitted resonance position against the
   previous payload's) that would normally have caught a 1.6% shift before
   it was applied.
5. **Why did automated monitoring not flag the mass-peak shift itself,
   independent of the payload-validation step?** Because no dashboard
   currently tracks the Z->ee mass-peak position per run range as a
   standing data-quality metric - it is checked by individual analysis
   groups on their own data samples, on their own schedule, rather than
   centrally and continuously as each new run range is reconstructed.

Root cause: the automated calibration-upload path bypasses the manual
validation queue whenever the previous payload has expired, and no
centralized, continuous data-quality monitor independently tracks the
Z->ee resonance position per run range - so a bad payload derived from a
run that should have been vetoed reached production reconstruction with no
check positioned to catch the resulting 1.6% energy-scale error before an
analyzer noticed it downstream.

## 4. Permanent Surgical Fix (Diff)

```diff
--- a/calibration_pipeline/upload_payload.py
+++ b/calibration_pipeline/upload_payload.py
@@ -22,9 +22,16 @@ def upload_payload(new_payload, previous_payload, interval_of_validity):
-    if interval_of_validity.has_expired():
-        # skip manual sign-off to avoid a gap in coverage
-        conditions_db.commit(new_payload)
-        return
+    scale_shift = abs(new_payload.absolute_scale - previous_payload.absolute_scale)
+    if scale_shift / previous_payload.absolute_scale > MAX_UNREVIEWED_SHIFT:
+        raise CalibrationSanityError(
+            f"scale shift {scale_shift:.4f} exceeds "
+            f"{MAX_UNREVIEWED_SHIFT:.1%} even with expired IOV - "
+            f"requires manual sign-off regardless of coverage gap"
+        )
+    conditions_db.commit(new_payload)
```

```diff
--- a/calibration_pipeline/veto_list.py
+++ b/calibration_pipeline/veto_list.py
@@ -8,6 +8,10 @@ def load_veto_list(path):
-    return read_veto_file(path)
+    veto_list = read_veto_file(path)
+    if veto_list.last_modified() > production_cycle.start_time:
+        raise StaleVetoListError(
+            "veto list updated after this production cycle started - "
+            "restart the cycle with the current veto list before fitting"
+        )
+    return veto_list
```

## 5. Blameless Postmortem & Preventative Monitoring Rules

No individual is at fault: the "skip sign-off when the interval has
expired" rule was a deliberate, reasonable design choice to avoid a
coverage gap, made before anyone had evidence of how large a scale error
could slip through that path; the analyzer who added the affected run to
the veto list two days into the production cycle had no way to know the
calibration pipeline wouldn't pick up the update.

**What worked:** freezing the automated pipeline and rolling back to the
previous known-good payload, rather than attempting an in-place fix,
restored a correct energy scale within the same day the issue was
reported and gave a clear, auditable point to resume from.

**What didn't work:** the "skip sign-off on expired IOV" design assumed
the only risk was coverage, not scale correctness - it removed the one
check (comparing against the previous payload) that would have caught
this exact failure mode.

**Preventative monitoring rule:** the upload pipeline now blocks
(raises `CalibrationSanityError`, non-zero exit) any payload whose
absolute-scale shift from the previous payload exceeds 0.5% without
manual sign-off regardless of interval-of-validity status, and a new
per-run-range Z->ee mass-peak dashboard pages the calibration on-call if
the fitted peak position deviates from 91.19 GeV by more than 1% for any
completed run range.
