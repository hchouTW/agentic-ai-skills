---
role: Principal Research Scientist / Manuscript Editor
skill: academic-papers
archetype: gated-pipeline
high_stakes_task: preparing and submitting a manuscript reporting a new cross-section measurement to a target physics journal
---

## Phase 1: Input Extraction & Gap Formulation

Extracted from the draft manuscript and the collaboration's submission
request: a cross-section measurement paper, targeting a page-limited Letter
format, with a co-author list that must match the collaboration's
publications-committee-approved author list rather than whoever contributed
text most recently.

Reading the draft against `references/submission-and-peer-review.md`'s
Pre-submission checklist surfaced concrete gaps rather than a vague "looks
close":
- The abstract quotes a cross-section of 4.31 pb; Table 3 in Results states
  4.28 pb. These have not been reconciled.
- Two `\cite{}` keys in the systematics paragraph do not resolve to any entry
  in the `.bib` file.
- No cover letter draft exists yet.
- The current draft is one paragraph over the target journal's page limit.

**Gate:** proceed to Phase 2 only once every checklist item above is logged
as a named, trackable gap (not "needs review") and the target journal's exact
page limit and reference-style requirement have been confirmed from that
journal's current author guidelines rather than assumed from a prior
submission.

## Phase 2: Draft Synthesis

Closed each gap against `references/submission-and-peer-review.md`'s
Pre-submission checklist by name:
- Reconciled the abstract-vs-Results mismatch: Table 3's 4.28 pb is the
  correct, code-verified value; the abstract's 4.31 pb was a stale number
  from an earlier draft before a background-normalization fix, and was
  corrected in place.
- Resolved both broken `\cite{}` keys: one was a typo'd key for an entry that
  already existed in the `.bib` file; the other cited a preprint that had
  since been published, so the `.bib` entry was updated to the published
  version per this same checklist's citation-resolution item.
- Trimmed the draft to the page limit by moving one supplementary derivation
  out of the main text and into supplementary material, per this skill's
  own `supplementary-material-planning.md` boundary between what belongs in
  the Letter versus its supplement.
- Drafted the cover letter per `references/submission-and-peer-review.md`'s
  "Cover letters" section: the paper title and one-sentence result summary,
  why this measurement fits the target journal's scope (it is the first
  measurement at this collision energy, not an incremental update of an
  existing one), and a note that two of the four co-authors on the previous
  related submission are also authors here, disclosed for referee-selection
  purposes - written in plain, factual language per that section's explicit
  guidance against words like "unprecedented."

**Gate:** proceed to Phase 3 only once every Phase 1 gap has a corresponding,
verifiable change in the draft (not a note that it was reviewed) and the
cover letter draft exists in full.

## Phase 3: Red-Team Review & Final Artifact Packaging

Ran a mock self-review against `references/reviewer-style-assessment.md`'s
rubric before submission: a neutral summary of the contribution, strengths,
then concerns classified as Major (threatens a central inference) or Minor
(local, does not change the central inference).

The assumption most worth stress-testing going in was: "the systematic
uncertainty table is complete, and the statistical uncertainty dominates the
total." Applying `reviewer-style-assessment.md`'s instruction to assess
uncertainty and central validity directly, rather than accepting the table as
given, found this assumption **false**: the background-modeling systematic,
previously folded into an "other systematics" line at 0.3%, was recomputed
explicitly and found to be 1.8% in the highest-purity bin - comparable to the
2.1% statistical uncertainty there, not negligible next to it. This was
classified as a Major concern per the rubric (it affects the total
uncertainty quoted in the abstract, a central inference), not Minor. As a
result:
- Added a named "Background modeling" row to the systematic-uncertainty
  table instead of leaving it inside "other systematics."
- Recomputed the total uncertainty and the significance quoted in the
  abstract with the corrected breakdown, and re-checked the abstract-vs-
  Results consistency item from Phase 1 a second time now that the numbers
  had changed again.
- Logged one Minor concern from the same self-review - a figure caption using
  present tense inconsistent with the rest of the manuscript's past-tense
  reporting convention - and fixed it in the same pass, since it was a
  one-line change.

**Gate:** submit only once the Major concern from the self-review is resolved
and reflected in both the abstract and Results (not just the systematics
table), the Minor concern is either fixed or explicitly deferred with a
reason, and the full Pre-submission checklist passes a second time following
the Phase 3 changes - this is the actual submission criterion, not an
intermediate one.
