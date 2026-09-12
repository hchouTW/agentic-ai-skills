---
role: Principal Analysis Physicist
skill: hep-analysis
archetype: elicitation
user_request: "Can you unfold this spectrum?"
---

## 1. Raw Ambiguous Input

Message from a collaborator, sent with an attached reconstructed-level
histogram:

> Can you unfold this spectrum? Need the truth-level result for the
> conference note.

No named unfolding method, no binning scheme, no regularization setting,
and no statement of whether the full uncertainty propagation is expected
for the conference note or a later paper.

## 2. Missing Constraint Analysis

Per `references/10-measurements-unfolding.md`, "unfold this spectrum"
underspecifies a choice with real consequences for both the result and its
validation burden: forward-folded likelihoods, matrix methods, regularized
inversion, and iterative Bayesian unfolding are named as distinct options
"according to the target and project," and "regularization and stopping
rules trade variance against bias." Picking one without knowing the
binning or the conference note's deadline risks either an under-validated
result or an unfolding turnaround that doesn't fit the timeline.

Specifically missing:
- **Which unfolding method** - the doc lists at least four structurally
  different approaches with different bias/variance tradeoffs and
  different validation requirements; a conference-note-quality result and
  a final-paper-quality result may reasonably use different ones.
- **Binning scheme** - the response matrix's conditioning and identifiable
  truth-bin count depend directly on the chosen binning; this must be
  fixed before building the response matrix, not adjusted after the fact
  to make results look smoother.
- **Regularization strength / stopping rule** - per the doc, this must be
  set "using predefined criteria and independent truth variations, not
  visual smoothness alone" - it cannot be tuned after seeing the unfolded
  result.
- **Uncertainty scope** - whether statistical uncertainty alone is
  sufficient for the conference note, or whether the fuller systematic
  propagation (response, background, and detector/theory effects) is
  required now.

## 3. Socratic Clarification Round

1. Which unfolding method should be used?
   a) Iterative Bayesian unfolding (D'Agostini-style) - common default
      for a first-pass differential result
   b) Regularized (Tikhonov-style) matrix inversion
   c) A forward-folded likelihood fit directly comparing reco-level data
      to folded truth-level templates - no explicit unfolding step
   d) Not yet decided - depends on what's fastest to validate before the
      conference deadline
2. What binning scheme should the response matrix use?
   a) The existing analysis binning (already used for the reco-level
      selection plots)
   b) A coarser binning, chosen specifically to keep the response matrix
      well-conditioned given available MC statistics
   c) Not yet decided - needs a conditioning check first
3. How should the regularization strength (or number of iterations, for
   Bayesian unfolding) be chosen?
   a) A predefined stopping criterion (e.g. a chi-square-based rule against
      independent truth variations)
   b) A fixed, standard default number of iterations used in a prior
      analysis in this same channel
   c) Not yet decided
4. What uncertainty scope is required for the conference note?
   a) Statistical uncertainty only - the conference note is explicitly
      preliminary and systematic uncertainties will follow for the paper
   b) Full statistical + systematic (response, background, detector/theory)
      propagation is required even for the conference note
   c) Not yet decided

## 4. User Feedback Integration

The collaborator's answers, sent back the same day:

- Q1 -> **a) Iterative Bayesian unfolding.** This channel's prior
  publications used this method, and matching it keeps this result
  comparable to the earlier measurement.
- Q2 -> **b) A coarser binning, chosen for conditioning.** Available MC
  statistics for this dataset don't support the existing fine reco-level
  binning in the response matrix; a coarser scheme is needed.
- Q3 -> **a) A predefined stopping criterion.** The number of iterations
  will be fixed using a chi-square-based rule evaluated against an
  independent truth variation, per `10-measurements-unfolding.md`'s
  guidance against choosing it by "visual smoothness alone."
- Q4 -> **a) Statistical uncertainty only, for now.** The conference note
  is explicitly labeled preliminary; full systematic propagation is
  planned for the eventual paper, not required for this note.

Each answer resolves one gap from section 2: Q1 fixes the method
(consistent with the channel's prior publication), Q2 sets the binning
based on an actual conditioning constraint rather than convenience, Q3
locks in a predefined, pre-registered stopping rule rather than a
post-hoc visual choice, and Q4 scopes the uncertainty to statistical-only
for this preliminary note, deferring full systematics to the paper.

## 5. Final Mutually-Agreed Specification Document

**Outcome:** An iterative-Bayesian-unfolded, truth-level differential
spectrum for the conference note, using a coarsened binning chosen for
response-matrix conditioning, with the iteration count fixed by a
predefined chi-square stopping criterion, reporting statistical
uncertainty only.

**In scope:** Building the response matrix at the coarsened binning
(with a folding check on a small hand-calculable matrix per
`10-measurements-unfolding.md`), running the iterative Bayesian unfolding
with the pre-registered stopping rule, and a nominal closure test against
an independent truth sample split from the response-building sample.

**Out of scope:** Full systematic uncertainty propagation (response,
background, detector/theory effects) - explicitly deferred to the paper
per Q4; any binning finer than what the conditioning check supports.

**Acceptance criteria (given/when/then):**
- Given the response matrix, when folding is checked on a small
  hand-calculable case, then it reproduces the expected reco-level
  distribution exactly, per the doc's explicit validation step.
- Given the chosen binning, when the response matrix's conditioning is
  assessed, then all truth bins are identifiable at the coarsened binning
  (no rank-deficient or unidentifiable bin).
- Given the stopping-rule chi-square criterion, when it is applied, then
  the selected iteration count is documented and was fixed before looking
  at the unfolded result's shape.
- Given the closure test, when it's evaluated on an independent truth
  sample (not the one used to build the response), then it passes within
  the predefined tolerance.

**Explicit non-goals:** This does not include systematic uncertainty
propagation, alternative-truth-shape stress tests beyond the closure
check, or a cross-check against a second unfolding method - all
explicitly deferred to the paper-level analysis, consistent with the
note's preliminary, statistical-only scope.
