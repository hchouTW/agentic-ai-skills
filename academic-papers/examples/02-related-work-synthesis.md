---
role: Senior Postdoctoral Researcher / Literature Review Editor
skill: academic-papers
use_case: synthesizing a related-work section from a stack of papers instead of listing them
---

## Scenario

A draft paper proposes a new statistical method for combining dark-matter
direct-detection exclusion limits across experiments with different target
nuclei and energy thresholds. The author has read five prior papers on
combination methods and needs to write the Related Work section before
submission. Each prior paper takes a different approach - naive limit
addition, a fixed-target-mass profile likelihood, a Bayesian hierarchical
model, a frequentist combination assuming a shared nuclear response, and a
machine-learning surrogate for the combined likelihood - and the new paper's
contribution is a method that removes the shared-nuclear-response assumption
that four of the five rely on.

## Common Weak Approach

> **Related Work**
>
> Smith et al. [1] combined direct-detection limits by adding exclusion curves
> point-by-point across experiments. Jones et al. [2] instead built a profile
> likelihood assuming a common effective target mass. Patel et al. [3] proposed
> a Bayesian hierarchical model over the nuisance parameters shared between
> experiments. Alvarez et al. [4] extended the frequentist combination to
> multiple nuclear targets under a shared nuclear response function. Chen et
> al. [5] trained a neural surrogate to approximate the combined likelihood
> directly from per-experiment summary statistics.

This is an annotated bibliography, not a related-work section: one sentence
per paper, no comparison between them, and no statement of what none of the
five actually address. A reader finishes the paragraph knowing that five
things exist but not how they relate to each other or to the method this
paper is about to propose - the paragraph could be reordered into any
permutation with no loss of information, which is a symptom this skill's own
`references/literature-review.md` names directly: "if a paragraph could be
replaced by 'see refs. [1-8]' without losing information, it isn't yet doing
a review's actual job." The Introduction that follows has to re-explain, from
scratch, why the new method is needed, because the Related Work section never
built that case.

## Expert-Level Best Practice

> **Related Work**
>
> Prior combination methods for direct-detection limits fall into two groups
> by how they treat the target-nucleus dependence of the signal model. The
> first group sidesteps the dependence rather than modeling it: naive
> point-by-point addition of exclusion curves [1] ignores that a given
> WIMP-nucleon cross-section maps to a different expected rate in each target
> nucleus, and a common-effective-target-mass profile likelihood [2] absorbs
> that difference into a single fitted nuisance parameter shared across all
> experiments - both approaches are exact only in the limit where the
> per-target nuclear response functions coincide, which they do not for
> targets spanning xenon, germanium, and argon. The second group models the
> shared structure explicitly: a Bayesian hierarchical model over the nuisance
> parameters [3] and a frequentist multi-target combination [4] both build in
> the nuclear response function directly, but both assume that function is
> the *same* function evaluated at different target masses, which is the
> specific assumption this paper's Sec. 3.2 shows breaks down above 100 GeV
> WIMP mass once spin-dependent contributions are included. The remaining
> approach, a neural surrogate for the combined likelihood [5], reproduces
> the combination numerically but does not report which of the two failure
> modes above it inherits, since its surrogate is trained on outputs of
> exactly the frequentist combination in [4].
>
> No prior combination method reports a validated result above 100 GeV where
> the shared-nuclear-response assumption is known to break down; this is the
> coverage gap this paper addresses. Sec. 4 replaces the shared-response
> assumption in [3, 4] with a per-target response computed from the
> measured nuclear form factors of each experiment individually, and Sec. 5
> shows the resulting combined limit differs from the shared-response result
> of [4] by 18% at 500 GeV WIMP mass - the size of the systematic the
> shared-response assumption was silently absorbing into that regime.

The synthesized version groups the five papers by what they share (avoiding
vs. modeling the target-nucleus dependence), names the specific technical
assumption each group makes rather than restating each paper's method in
isolation, and ends with a coverage gap ("no prior method validated above 100
GeV") stated precisely enough to be checked against the five papers just
discussed - then ties the current paper's contribution to that gap with the
actual number (18% at 500 GeV) the rest of the paper defends, per this
skill's guidance to state the gap "directly connected to what the current
paper does about it."

## Key Takeaways

- Organize by shared technical assumption, not by citation order or paper
  identity. Grouping [1]-[2] and [3]-[4] by whether they avoid or model the
  target-nucleus dependence tells the reader something a chronological or
  per-paper listing cannot: which specific assumption the new method actually
  removes, and which prior papers share it.
- State each group's failure mode precisely enough to be falsifiable, not as
  a vague "limitations exist" gesture. "Assumes the nuclear response function
  is the same function evaluated at different target masses" is a claim a
  reader can check against the cited papers' own equations; "several
  simplifying assumptions are made" is not.
- Close with a coverage gap stated in the same technical vocabulary as the
  grouping, then connect it to a specific, checkable number from the current
  paper's own results (18% at 500 GeV). A gap statement that never reconnects
  to what the paper actually delivers reads as an unfulfilled promise, per
  `references/literature-review.md`'s "Spotting the gap" guidance.
- A synthesized paragraph is not reorderable without losing information - the
  annotated-bibliography version could be permuted into any order with no
  change in meaning, while the synthesized version's second sentence depends
  on having grouped [1]-[2] together in the first. That dependency is itself
  evidence the paragraph is doing synthesis rather than listing.
