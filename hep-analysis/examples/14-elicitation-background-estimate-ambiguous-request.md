---
role: Principal Analysis Physicist
skill: hep-analysis
archetype: elicitation
user_request: "Can you redo the background estimate?"
---

## 1. Raw Ambiguous Input

Message from the analysis group convener, posted on the internal analysis
mailing list:

> Can you redo the background estimate? Reviewers weren't happy with the
> last version.

No named background process, no stated estimation method, no control
region specified, and no indication of whether the concern was about the
central value or its uncertainty.

## 2. Missing Constraint Analysis

Per `references/05-backgrounds.md`, "redo the background estimate" spans
fundamentally different techniques with different data and modeling
requirements - a data-driven ABCD method (needs four well-defined,
sufficiently populated regions and a validated independence assumption), a
fake-factor/matrix method (needs loose/tight object definitions and a
validated extrapolation), or a simultaneous control-region fit (needs
shared normalization parameters linked across CRs and SRs in a joint
likelihood). The analysis has at least two backgrounds with open reviewer
questions, and picking the wrong one to redo - or redoing it with the wrong
method - would not address whatever the reviewers actually flagged.

Specifically missing:
- **Which background process** the reviewers flagged - the analysis note
  has open questions on both the QCD multijet estimate and the W+jets
  estimate, and they use different methods.
- **Which method is in scope for the redo** - ABCD, matrix method, and a
  simultaneous CR fit are not interchangeable; the fix depends on which one
  the reviewers' comment actually targets.
- **Which control region(s)** are available or need to be redefined - per
  `05-backgrounds.md`'s ABCD guidance, "a small or zero D invalidates
  simple ratio propagation," so knowing which region is thin matters before
  proposing a fix.
- **Scope: central value only, or also its uncertainty** - the reviewers
  may have flagged the point estimate itself, or specifically the closure
  uncertainty/correlation treatment around it (per the doc's "do not tune
  closure uncertainties to force agreement" caution).

## 3. Socratic Clarification Round

1. Which background process did the reviewers' comment target?
   a) The QCD multijet estimate (currently done via ABCD)
   b) The W+jets estimate (currently done via a matrix method)
   c) Both - the comment was general, not process-specific
2. What method should the redo use?
   a) Keep the current method (ABCD or matrix method, per Q1) but fix an
      identified flaw in its application
   b) Switch to a simultaneous control-region fit linking CRs and SRs in a
      joint likelihood
   c) Not yet decided - depends on what the specific flaw turns out to be
3. Which control/validation region is actually in question?
   a) Region D in the QCD ABCD estimate is a concern - it has very low
      statistics
   b) The matrix-method's "loose" sample composition is in question -
      possible non-negligible prompt contamination
   c) No specific region - the reviewers questioned the overall closure
      test, not a specific region's population
4. Is the reviewers' concern about the central value or its uncertainty?
   a) The central value itself is believed too high/low
   b) The central value is accepted; the closure/systematic uncertainty
      around it is judged too small or not justified
   c) Both

## 4. User Feedback Integration

The convener's answers, after re-reading the referee report line by line:

- Q1 -> **a) The QCD multijet estimate.** The reviewer comment quotes the
  ABCD closure plot specifically, not the W+jets matrix-method section.
- Q2 -> **c) Not yet decided until the specific flaw is confirmed** - but
  narrowed by Q3 below to "fix the current ABCD application," not a full
  method switch.
- Q3 -> **a) Region D has very low statistics** - roughly 8 events in the
  latest dataset, which the reviewer flagged as too thin to trust the
  simple `A ~ BC/D` ratio, consistent with `05-backgrounds.md`'s explicit
  "a small or zero D invalidates simple ratio propagation" warning.
- Q4 -> **c) Both.** The reviewer questions whether the central value
  (computed from a statistically thin D) is even meaningful, and separately
  flags that the quoted uncertainty doesn't reflect that thinness.

Each answer resolves one gap from section 2: Q1 names the specific
background (QCD, not W+jets), Q2 narrows the fix to the existing ABCD
method rather than a full method change, Q3 pinpoints the exact structural
problem (thin region D) that `05-backgrounds.md` explicitly warns about,
and Q4 confirms the redo must fix both the central-value estimator and its
uncertainty, not just one.

## 5. Final Mutually-Agreed Specification Document

**Outcome:** Redo the QCD multijet background estimate using a joint
four-region likelihood (per `05-backgrounds.md`'s explicit recommendation
for a thin D region: "use a joint four-region likelihood ... do not
replace D by one"), replacing the simple `A ~ BC/D` ratio and its
associated uncertainty.

**In scope:** Refitting regions A/B/C/D simultaneously in one likelihood
that correctly propagates region D's Poisson statistics (rather than
treating it as a fixed denominator), a closure test against an independent
validation sample, and a revised uncertainty that reflects D's actual
statistical thinness.

**Out of scope:** The W+jets matrix-method estimate - the reviewer comment
is specific to QCD/ABCD, and revisiting the matrix method without a
corresponding reviewer concern would exceed the smallest coherent slice for
this review round.

**Acceptance criteria (given/when/then):**
- Given the joint four-region likelihood, when region D's low statistics
  (~8 events) are propagated, then the resulting QCD central value's
  uncertainty visibly reflects that thinness (wider than the original
  simple-ratio uncertainty), rather than an artificially narrow interval.
- Given the closure test, when it's run against an independent validation
  sample, then it is reported per `05-backgrounds.md`'s deliverables list -
  region definitions, contamination estimate, and closure plot with
  uncertainty - not just a pass/fail statement.
- Given the revised estimate, when compared to the original ABCD number,
  then any shift in the central value is explained by the joint-likelihood
  treatment, not by ad hoc tuning of the closure uncertainty to match the
  observed SR (an explicit anti-pattern the reference doc calls out).

**Explicit non-goals:** This does not redo the W+jets matrix-method
estimate, and does not switch the QCD estimate to a different background
technique (e.g. full simulation-driven) - the reviewer's concern is
specifically the thin-D-region handling within the existing ABCD-family
approach.
