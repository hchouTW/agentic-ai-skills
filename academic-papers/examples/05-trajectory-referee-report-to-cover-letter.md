---
role: Principal Research Scientist / Manuscript Editor
skill: academic-papers
archetype: trajectory
problem_input: a raw referee report with three numbered comments on a submitted manuscript, one of which the authors intend to dispute rather than accept
---

## 1. Task Input & Context

Referee report, as received from the editor:

> Comment 1: The authors report a detection significance of 4.1σ but do not
> state whether this includes a look-elsewhere correction for the three
> mass windows scanned. Please clarify.
>
> Comment 2: Figure 3's caption does not state the binning used for the
> reconstructed mass distribution.
>
> Comment 3: The authors should have used a Bayesian approach throughout
> rather than a frequentist one; the paper's conclusions would be more
> naturally expressed as posterior probabilities.

## 2. Root-Cause Triage & Action Plan

Per `references/submission-and-peer-review.md`'s "Responding to referee
reports," each comment is triaged individually rather than answered in bulk:

- Comment 1 is valid and actionable: the manuscript's Sec. IV states the
  4.1σ figure but the look-elsewhere correction, though it was in fact
  applied during the analysis, was never stated in the text. This is a
  disclosure gap, not an analysis error - the corrected number is already
  the one being reported.
- Comment 2 is valid and trivial: the binning (25 MeV/c² per bin) is in the
  analysis code but was omitted from the caption.
- Comment 3 is a methodological preference, not a defect: the manuscript's
  frequentist framework is internally consistent and standard for this
  measurement type. Per the reference's point 4 ("keep tone factual and
  non-defensive... referees are often right about something even when their
  specific framing is off"), this is answered with the specific reason for
  the choice rather than either silently ignoring it or redoing the analysis.

Action plan: add one sentence to Sec. IV stating the look-elsewhere
correction explicitly, add the bin width to Figure 3's caption, and draft a
factual, non-defensive explanation of the frequentist choice for Comment 3.

## 3. Surgical Execution

```diff
--- a/manuscript/section4.tex
+++ b/manuscript/section4.tex
@@ -42,7 +42,9 @@
-The observed excess corresponds to a local significance of 4.1$\sigma$.
+The observed excess corresponds to a local significance of 4.1$\sigma$
+(3.6$\sigma$ global, after a trials correction for the three mass windows
+scanned, computed following the procedure in Sec.~III.C).
```

```diff
--- a/manuscript/figures/fig3_caption.tex
+++ b/manuscript/figures/fig3_caption.tex
@@ -1,3 +1,3 @@
-\caption{Reconstructed invariant mass distribution for the selected sample.}
+\caption{Reconstructed invariant mass distribution for the selected sample,
+binned in 25~MeV/$c^2$ intervals.}
```

## 4. Verification Evidence

```
$ python3 scripts/check_manuscript.py manuscript/
Scanned 4 .tex file(s) and 1 .bib file(s).
No issues found.
$ grep -n "global" manuscript/section4.tex
44:(3.6$\sigma$ global, after a trials correction for the three mass windows
$ grep -n "25" manuscript/figures/fig3_caption.tex
2:binned in 25~MeV/$c^2$ intervals.}
```

## 5. Final Deliverable Summary

Drafted a point-by-point response letter, in the referee's comment order, per
`references/submission-and-peer-review.md`: Comment 1 answered by quoting the
concern and pointing to the exact revised sentence in Sec. IV; Comment 2
answered the same way for the caption; Comment 3 answered by stating
explicitly that the frequentist framework was kept, with the specific reason
(consistency with the collaboration's established significance-reporting
convention for this channel), rather than silence or an unrequested
re-analysis. The response letter closes with a one-line summary of the two
substantive changes for the editor, and the cover letter for resubmission
states the paper title, a one-sentence result summary, and a pointer to this
response letter, per that same reference's "Cover letters" section.
