---
role: Senior ML Systems Engineer
skill: deep-learning
archetype: decision-tree
scenario: a tracked evaluation metric changed unexpectedly after a routine, seemingly unrelated pipeline update
---

## Triage Matrix

Combines `references/evaluation-strategy.md`'s "Protect the test set" and
"The offline-online gap" with `references/data-strategy.md`'s "Splits that
survive contact with reality" and "Versioning" into a single triage matrix
for an unexplained metric change, so the response isn't "the eval set must be
wrong" or "the model must be better" by default:

| Trigger | Resolution Strategy |
|---|---|
| Metric improved suspiciously, by a large margin, right after a data-pipeline change | Check for reintroduced train/eval leakage or an unversioned change to the eval set itself, per "Versioning"'s warning that "a metric that improved because the eval set changed is not an improvement" |
| Metric changed right after an evaluation-*code* change, with no data or model change | Check for a metric-computation bug (off-by-one, wrong denominator, changed averaging) before trusting the new number at all |
| The metric is stable on the validation set used for iteration, but a held-out final test set shows a different result | The validation set has been "used up" through repeated iteration and has an optimistic bias; treat only the untouched test set's number, per "Protect the test set" |
| Metric changed with no code, data, or eval-set change identified, but live traffic's distribution has shifted since the eval set was collected | Distribution shift between the logged eval data and current live traffic, per "The offline-online gap" - measure the gap, don't assume it's zero |

## Selected Branch

Reported case: the tracked offline F1 metric jumped from 0.81 to 0.89 the day
after a routine data-pipeline update that added a near-duplicate-record
deduplication step to the training and evaluation data ingestion. No model or
evaluation code changed. This matches the first row: a suspicious, large
improvement immediately following a data-pipeline change.

## End-to-End Execution Script

1. Per "Versioning"'s explicit warning, do not accept the new metric at face
   value: confirm the eval set's version was in fact bumped by the dedup
   step, and re-check for leakage rather than assuming the new number is a
   genuine improvement.
2. Diffed the eval set before and after dedup: 340 of 12,000 eval rows were
   removed as near-duplicates of *training* rows (not other eval rows) - a
   real train/eval contamination the dedup step happened to also catch,
   distinct from its intended purpose of removing exact duplicates within
   each split separately.
3. Confirmed the previous (pre-dedup) 0.81 F1 was measured with those 340
   near-duplicate-of-training rows still in the eval set, and that the model
   scored unusually well on exactly that subset (0.97 F1 on the 340 rows vs.
   0.80 on the rest) - consistent with those rows being memorized from
   training rather than genuinely generalized to.
4. Conclusion: the 0.81 to 0.89 jump is not a new leak - it is the *removal*
   of a pre-existing one, and the new 0.89 is the more trustworthy number.
   This is the opposite of the first row's default worry, and the process
   above is what distinguished it from a newly introduced leak rather than
   assuming either answer.
5. Recorded the eval-set version bump and the reason (contamination removal,
   not a metric redefinition) explicitly in the eval-set changelog, per
   "Versioning"'s requirement to keep the evaluation set itself versioned so
   a future reader does not mistake this jump for an unexplained regression
   in the other direction when comparing across dates.

## Fallback Safeguards

If the diff in step 2 had instead shown the dedup step removing rows *between
splits in a way that merged near-duplicate eval rows into training* (rather
than removing training-contaminated eval rows), that would indicate the dedup
step introduced a new leak rather than fixing an old one - the fix would be
to add a group/near-duplicate-aware split similar to
`references/data-strategy.md`'s group-leakage guidance, and the metric
improvement would need to be treated as unverified until re-measured on a
corrected split. If no train/eval contamination were found in either
direction, re-triage against the third row (test-set overuse) and second row
(metric-computation bug) before concluding the improvement is real.
