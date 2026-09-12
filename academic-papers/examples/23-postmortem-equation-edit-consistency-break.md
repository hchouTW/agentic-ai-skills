---
role: Site Reliability / Principal Research Scientist
skill: academic-papers
archetype: postmortem
incident: A co-author's last-minute variable substitution in one equation was never propagated to a later equation reusing the old symbol, discovered only after submission
---

## 1. Incident Symptom & Alert Payload

Email from a reader who requested the preprint after it posted:

```
From: reader@external-institution.example
Subject: Possible notation inconsistency in Eq. (14) vs Eq. (9)

I think Eq. (9) defines the efficiency correction as a function of
reconstructed pT, calling it \hat{p}_T, but Eq. (14) later uses p_T (no
hat) in what looks like the same role. Is \hat{p}_T meant to equal p_T
here, or did I misread which quantity Eq. (14) is correcting?

--- diff between last two pre-submission commits (from co-author's own
    change log, forwarded by the corresponding author) ---
commit a91f3e2 "use calibrated pT symbol in efficiency eq per referee-
                 style pass, per PI's request night before submission"
  Eq. (9):  epsilon(p_T) -> epsilon(\hat{p}_T)     [1 site changed]
  Eq. (14): [not touched - reuses old symbol p_T unchanged]
```

The corresponding author confirmed the reader's suspicion: Eq. (9) was
edited to use the calibrated-momentum symbol `\hat{p}_T` twelve hours
before submission, but Eq. (14), several pages later, still uses the
raw-momentum symbol `p_T` for what is meant to be the same calibrated
quantity carried forward from Eq. (9).

## 2. Immediate Triage & Blast-Radius Mitigation

Per `references/manuscript-consistency-auditing.md`'s "build the result
ledger... use an identified analysis output... as authoritative," the team
first checked the underlying analysis code, not either equation's LaTeX
text, to determine which symbol reflects what was actually computed: the
analysis pipeline calibrates `p_T` before applying the efficiency
correction, confirming `\hat{p}_T` (Eq. (9)'s corrected symbol) is the
scientifically correct one and Eq. (14) is the one in error - the physics
result itself is unaffected, only the manuscript's internal notation. The
corresponding author replied to the reader within the same day acknowledging
the inconsistency and confirming the physics conclusion is unchanged, then
posted a revised preprint version with the correction, bounding the window
during which the public version contained the inconsistency to under one
week from posting.

## 3. 5-Whys Root Cause Deep-Dive

1. **Why does Eq. (14) use `p_T` where it should use `\hat{p}_T`?**
   Because Eq. (9) was edited the night before submission to switch from
   `p_T` to `\hat{p}_T`, but Eq. (14), which reuses the same quantity
   several pages later, was never updated to match.
2. **Why wasn't Eq. (14) updated when Eq. (9) was?** Because the symbol
   `p_T` was hand-typed independently in both equations rather than
   referencing a single shared macro, so editing one occurrence had no
   effect on the other - there was no mechanism by which the second use
   could have picked up the change automatically.
3. **Why was a hand-typed symbol used in two places for the same
   quantity in the first place?** Because the manuscript predates the
   introduction of `\hat{p}_T` as a distinct concept - `p_T` was
   originally the only momentum symbol in the paper, and when the
   calibration step was added late in drafting, only the equation where
   the calibration is first *introduced* (Eq. (9)) was updated to the new
   symbol, not every later equation that *uses* the calibrated value.
4. **Why did no review step catch the mismatch before submission?**
   Because the edit was made the night before the deadline, after the
   manuscript's normal internal co-author review round had already
   concluded, and `references/equation-and-notation-auditing.md`'s
   symbol-ledger check (checking every equation, prose, and appendix use of
   a symbol against a single ledger) was performed during that earlier
   review round, not re-run after this late change.
5. **Why does the notation-auditing process not re-run automatically
   after a late equation edit?** Because it is currently a manual,
   point-in-time review step invoked once per drafting round, with no
   trigger tied to "an equation changed after the last audit" - a
   single late edit close to a deadline can silently invalidate an audit
   that was correct when it was performed.

Root cause: the manuscript has no single source of truth for the symbol
`\hat{p}_T}` (each equation re-types it by hand), and the notation audit
that would have caught the resulting drift is a one-time manual step with
no re-trigger condition, so a correct, well-intentioned late edit to one
equation silently broke consistency with another.

## 4. Permanent Surgical Fix (Diff)

```diff
--- a/paper.tex
+++ b/paper.tex
@@ -1,6 +1,7 @@
 \documentclass{revtex4-2}
+\newcommand{\ptcal}{\hat{p}_T}
 \begin{document}
@@ -140,7 +141,7 @@
-\epsilon(p_T)
+\epsilon(\ptcal)
@@ -212,7 +213,7 @@
-p_T \text{ is corrected by the tag-and-probe efficiency}
+\ptcal\ \text{is corrected by the tag-and-probe efficiency}
```

```diff
--- a/tools/notation_audit.py
+++ b/tools/notation_audit.py
@@ -1,4 +1,10 @@
 #!/usr/bin/env python3
+"""Flag any raw 'p_T' (no hat) appearing after the calibration is
+introduced in Eq. (9) - per postmortem: p_T after that point should be
+\\ptcal instead. Run this any time an equation changes, not just at the
+scheduled review round."""
 import re, sys
+CALIBRATED_SYMBOL_LEAK = re.compile(r"(?<!\\hat\{)p_T(?!\})")
```

## 5. Blameless Postmortem & Preventative Monitoring Rules

No individual is at fault: the PI's requested edit the night before
submission was a reasonable, correct improvement to Eq. (9), and the
co-author who made it had no reason to know a second, unrelated-looking
equation several pages away depended on the same symbol - that dependency
was invisible without a shared macro or a ledger check triggered by the
edit itself.

**What worked:** checking the underlying analysis code (not either
equation's LaTeX) as the authoritative source resolved which symbol was
scientifically correct within minutes, confirming the physics result
itself needed no correction.

**What didn't work:** the notation audit was correct at the time it ran,
but nothing re-triggered it after a late edit close to the deadline, so a
one-time audit gave false confidence about a manuscript state that had
since changed.

**Preventative monitoring rule:** `tools/notation_audit.py` runs as a
pre-submission git hook and blocks (non-zero exit) any commit that touches
an equation environment within 120 minutes of the stated submission
deadline, until the audit has been re-run and shows zero flagged symbol
mismatches.
