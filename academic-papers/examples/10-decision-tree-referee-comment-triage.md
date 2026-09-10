---
role: Manuscript Editor
skill: academic-papers
archetype: decision-tree
scenario: triaging a batch of referee comments on a submission into the right response category before drafting the point-by-point reply
---

## Triage Matrix

Formalizes `references/submission-and-peer-review.md`'s "Responding to
referee reports" guidance into an explicit trigger -> response-category
mapping, applied to each comment in a report before any drafting starts:

| Trigger | Resolution Strategy |
|---|---|
| Comment identifies a genuine methodological gap or missing analysis step | Perform the additional analysis or check, then report the specific numeric/textual change and its exact manuscript location |
| Comment points to unclear or incomplete text, notation, or a missing detail (a caption, a parameter definition) that does not change any result | Clarify the text or caption directly; no new analysis needed |
| Comment reflects a methodological or stylistic preference the authors do not intend to adopt, but the manuscript's existing choice is defensible | State the reason for the existing choice factually and non-defensively; do not adopt the suggestion, but do not ignore the comment either |
| Comment is a typo, formatting, or minor presentational note | Fix directly with no separate discussion needed in the response letter beyond a one-line acknowledgment |
| Comment requests something outside the scope of this paper (e.g. a substantially different analysis, a follow-up study) | State explicitly that it is out of scope for this submission, with a brief reason, rather than silently declining or attempting a scope-expanding revision |

## Selected Branch

Comment under review: "The authors should also report the result separately
for the 2018 and 2019 data-taking periods, to check for a run-dependent
effect the reader cannot currently assess." This is a genuine methodological
gap (the split was not currently shown and is a reasonable check a reader
would want), matching the first row - not a stylistic preference (row 3),
since nothing about the existing single combined result is wrong, only
incomplete for this specific cross-check.

## End-to-End Execution Script

1. Rerun the existing analysis pipeline with an added period-split
   selection: `python3 analysis.py --split-by run-period --output
   results/period_split.json`.
2. Compare the two periods' fitted values: 2018 gives `4.02 ± 0.09`, 2019
   gives `4.11 ± 0.10` - consistent within combined uncertainty
   (difference `0.09`, combined SE `0.135`), so no run-dependent effect is
   found.
3. Add a new one-paragraph subsection to the manuscript's Sec. V reporting
   both period values and the consistency check, and a corresponding row to
   Table 4.
4. Draft the response-letter entry: quote the referee's comment in full,
   state "We have added the requested period-by-period breakdown, now
   reported in Sec. V and Table 4 (new row); the two periods are consistent
   within uncertainty, indicating no run-dependent effect," per this
   reference's point-by-point structure (quote, state the change, give the
   exact location).

## Fallback Safeguards

If the period split had instead revealed a statistically significant
difference between 2018 and 2019, the branch would change: this would no
longer be a simple "add the check and report consistency" resolution, but a
finding requiring escalation to the collaboration's internal review before
any text is drafted, since it could indicate an unaccounted systematic
specific to one data-taking period rather than a statistical fluctuation -
re-triage against a methodological-gap-with-open-question status rather than
closing the comment with a one-paragraph addition.
