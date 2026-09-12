---
role: Site Reliability / Principal Research Scientist
skill: academic-papers
archetype: postmortem
incident: Submitted manuscript's official PDF cites the wrong paper for a key claim because the venue's auto-compile pulled a stale, precompiled reference list
---

## 1. Incident Symptom & Alert Payload

Email from the handling editor, three days after submission, forwarding a
reviewer's confused comment:

```
From: editorial@venue-submission-system.example
Subject: [Manuscript #4471] Reviewer query on Ref. [17]

Reviewer 2 writes: "Ref. [17], cited in support of the claim that 'the
background model has been validated to 2% precision,' is a paper about an
unrelated detector upgrade and does not contain this result. Please
clarify or correct."

--- submission-system build log (attached) ---
[build] using cached .bbl from previous compile (2024-11-02T09:14:03Z)
[build] .bib file modified: 2024-11-04T16:47:21Z (newer than cached .bbl)
[build] WARNING: bibliography may be stale; re-run bibtex to refresh
[build] PDF generated from cached .bbl - warning not surfaced to submitter
```

The `.bib` entry for `[17]` had in fact been corrected two days *before*
submission - the compiled PDF reviewers received did not reflect that
correction.

## 2. Immediate Triage & Blast-Radius Mitigation

The corresponding author immediately verified the local, from-scratch
build: `latexmk -C && latexmk -pdf paper.tex` on the exact submitted
source reproduced the *correct* citation `[17] -> Consistency Cross-Checks
for the 2% Background Model (this collaboration, 2024)`, confirming the
`.bib` fix was real and present in the submitted source - the discrepancy
was specific to the venue's cached build, not a source-file error. Per
`references/artifact-packaging-for-release.md`'s "verify against a clean
checkout" discipline (applied here to the submission artifact rather than
a code release), the author uploaded a fresh, from-scratch-compiled PDF
through the venue's "replace submitted files" mechanism within the hour and
replied directly to Reviewer 2's comment confirming the correction, rather
than waiting for the next scheduled revision round - bounding the window
during which any reviewer could be looking at the wrong reference to under
one business day from the report.

## 3. 5-Whys Root Cause Deep-Dive

1. **Why did Reviewer 2 see a citation that didn't match the claim?**
   Because the PDF distributed to reviewers was generated from a cached
   `.bbl` (bibliography) file that predated a correction made to the
   `.bib` source two days before submission.
2. **Why was a stale `.bbl` used instead of a freshly regenerated one?**
   Because the venue's submission-system build pipeline reuses a cached
   `.bbl` whenever one already exists for a manuscript ID, and only
   regenerates it on a full `bibtex` pass when no cached `.bbl` is present
   at all - it does not compare the `.bib` file's modification time
   against the cached `.bbl`'s.
3. **Why didn't the author's own local build catch this before
   submission?** Because the author's local `latexmk` workflow always
   deletes auxiliary files (`latexmk -C`) before a full rebuild, so a
   staleness bug specific to a caching build system was never exercised
   locally - the local and remote build pipelines are not the same
   pipeline, and only one of them has this cache.
4. **Why did the submission system emit a "bibliography may be stale"
   warning without surfacing it to the author?** Because the warning is
   written only to an internal build log accessible to editorial staff,
   not to the author-facing submission-confirmation email or upload
   receipt - the system detected the exact condition that caused the
   incident and did not tell the one person positioned to fix it before
   reviewers saw the result.
5. **Why was there no independent verification step between "PDF
   generated" and "PDF sent to reviewers"?** Because the venue's process
   treats a successful build exit code as sufficient to proceed to review
   distribution, with no check that the distributed PDF's bibliography
   matches the currently-committed `.bib` source it was supposedly built
   from.

Root cause: the venue's submission-build pipeline silently trusts a cached
`.bbl` without comparing it against the current `.bib` source's
modification time, and the one diagnostic that did detect the staleness
was logged somewhere the author could never see it before reviewers
received the PDF.

## 4. Permanent Surgical Fix (Diff)

```diff
--- a/tools/pre_submission_check.sh
+++ b/tools/pre_submission_check.sh
@@ -1,6 +1,18 @@
 #!/bin/sh
 set -e
+
+# Guard against a venue submission system serving a cached .bbl that
+# predates the current .bib source (see postmortem #4471).
+BBL_TIME=$(stat -c %Y paper.bbl 2>/dev/null || echo 0)
+BIB_TIME=$(stat -c %Y references.bib)
+if [ "$BIB_TIME" -gt "$BBL_TIME" ]; then
+  echo "ERROR: references.bib is newer than paper.bbl - force a clean" \
+       "bibtex rebuild before uploading (rm paper.bbl && latexmk -pdf" \
+       "paper.tex) and re-download the compiled PDF from the venue" \
+       "system to confirm it matches before notifying reviewers." >&2
+  exit 1
+fi
 
 latexmk -C
 latexmk -pdf paper.tex
```

```diff
--- a/docs/submission-checklist.md
+++ b/docs/submission-checklist.md
@@ -4,3 +4,6 @@
 - [ ] Run `tools/pre_submission_check.sh` and resolve any reported error
 - [ ] Confirm the local from-scratch PDF's reference list matches the
       current `references.bib` for every recently-edited citation
+- [ ] After the venue system generates its own compiled PDF, download it
+      and diff its bibliography against the local from-scratch PDF before
+      the manuscript is released to reviewers
```

## 5. Blameless Postmortem & Preventative Monitoring Rules

No individual is at fault: the author corrected the citation, ran a full
local rebuild, and had no visibility into the venue's internal caching
behavior or its silently-logged staleness warning - there was no signal
available to them that the submitted PDF would differ from their own
verified build.

**What worked:** the author's from-scratch local rebuild gave an
unambiguous, fast way to confirm the source was correct and isolate the
discrepancy to the venue's build cache within the same day the reviewer
comment arrived.

**What didn't work:** the submission system detected the exact staleness
condition that caused the incident and logged it, but routed that signal
to a log file instead of to the author - a detection with no delivery path
is equivalent to no detection for the purpose of preventing this incident.

**Preventative monitoring rule:** `tools/pre_submission_check.sh` blocks
(non-zero exit) any submission where `references.bib`'s modification
timestamp is newer than `paper.bbl`'s by more than 60 seconds, and the
submission checklist adds a post-upload step requiring the author to
download and diff the venue's own compiled PDF's bibliography against the
verified local build before notifying co-authors the manuscript is ready
for review.
