---
role: Research Integrity Reviewer / Co-Author
skill: academic-papers
use_case: verifying that a citation actually supports the specific numeric claim attached to it before submission
---

## Scenario

A manuscript predicting a dark-matter direct-detection event rate states, in
its Sec. 2: "We adopt a local dark-matter density of ρ_local = 0.3 GeV/cm³
[6]," where [6] is a well-known review article on the local dark-matter
distribution, and uses that single value with no quoted uncertainty to
compute the paper's headline predicted event rate. A co-author is asked to
verify the manuscript's citations before submission, per this skill's
`references/citation-verification.md`.

## Common Weak Approach

The co-author skims the abstract of [6], confirms it is indeed a review of
the local dark-matter density, and signs off:

> **Verification note:** Checked ref. [6] - it's the standard local
> dark-matter density review, matches the topic of Sec. 2. Approved.

This is an abstract-level topic match, not a claim check. The reviewer
confirmed that [6] is *about* the local dark-matter density in general, but
never opened the passage the citing sentence actually depends on: the
specific value 0.3 GeV/cm³ and the claim that it carries no meaningful
uncertainty at this precision. Per `references/citation-verification.md`,
"a plausible title or a search snippet" is not verification, and the
distinction this step skips - between a source's topic and a source's actual
supported claim - is exactly the gap that lets a rounded, undocumented
number silently propagate into a paper's headline result.

## Expert-Level Best Practice

The co-author opens [6] directly and reads the passage the citing sentence
depends on, not just the abstract:

> **Verification ledger entry**
>
> - **Manuscript location / claim:** Sec. 2, "We adopt a local dark-matter
>   density of ρ_local = 0.3 GeV/cm³ [6]."
> - **Citation key / source:** [6], review article on the local dark-matter
>   distribution (identifier and version on file).
> - **Evidence locator:** [6], Sec. 4, Table 2 and surrounding discussion.
> - **Finding:** [6] does not report a single value of 0.3 GeV/cm³. It
>   reports a *range* of ρ_local = 0.2-0.56 GeV/cm³ across the seven
>   independent determination methods it surveys (kinematic tracer fits,
>   local baryonic subtraction, and microlensing-constrained models), and
>   states explicitly that "no single method's result should be treated as
>   the field's consensus value without stating which method it comes from."
>   The commonly quoted 0.3 GeV/cm³ appears in [6] only as a rounded
>   historical reference value from an older, superseded determination that
>   the review itself flags as an underestimate relative to its own updated
>   range.
> - **Support verdict:** Unsupported as stated. [6] supports "a range of
>   0.2-0.56 GeV/cm³ depending on method," not a single value of 0.3 GeV/cm³
>   with no quoted uncertainty.
> - **Proposed fix:** Replace the Sec. 2 sentence with: "We adopt a local
>   dark-matter density of ρ_local = 0.3 GeV/cm³ as a central reference value,
>   noting that [6]'s survey of independent determinations spans 0.2-0.56
>   GeV/cm³; Sec. 5 propagates this range into the predicted event rate as a
>   dedicated systematic." Sec. 5's predicted event rate, which scales
>   linearly with ρ_local, is recomputed at the range endpoints: the
>   originally quoted single-value rate of 2.4 events/kg/year becomes
>   1.6-4.5 events/kg/year, and this range - not the single central number -
>   is what is carried into the paper's exclusion-sensitivity projection in
>   Sec. 6.

The reviewer reads the specific passage the claim depends on rather than
confirming the source's general topic, finds that the manuscript's single
undocumented number is not what the source actually supports, and proposes
the smallest correction that fixes it: state the adopted value as a central
reference, cite the source's actual range, and propagate that range into
every downstream quantity that depends on it - here, the predicted event
rate that is the paper's headline result - rather than only correcting the
one sentence where the citation appears.

## Key Takeaways

- Verifying a citation means reading the passage the citing sentence depends
  on, not confirming the source's general topic. [6] being "the standard
  local dark-matter density review" was never in question; whether it
  supports the specific number 0.3 GeV/cm³ with no uncertainty was, and only
  opening Sec. 4/Table 2 answers that.
- Separate metadata correctness from evidentiary support, per
  `references/citation-verification.md`. The weak pass conflated "this is the
  right paper on the right topic" with "this paper supports this exact
  claim" - a source can be entirely correctly cited by title and still not
  say what the citing sentence says it says.
- A support verdict is only useful if it is one of the defined categories
  (supported, partial, unsupported, unverified) with a stated reason, not a
  one-word "Approved." "Unsupported as stated" is actionable - it tells the
  next author exactly what has to change and why - where "Approved" gives no
  signal that anything was actually checked.
- Propagate a corrected claim through every quantity that depends on it, not
  just the sentence where the citation sits. The single mis-cited density
  value fed directly into the paper's headline predicted event rate; fixing
  the citation without recomputing Sec. 5's rate and Sec. 6's projection would
  leave the manuscript's main quantitative result resting on the same
  unsupported number the fix was meant to remove.
