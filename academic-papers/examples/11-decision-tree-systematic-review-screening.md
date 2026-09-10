---
role: Systematic Review Lead
skill: academic-papers
archetype: decision-tree
scenario: screening a batch of retrieved records against a pre-registered systematic-review protocol
---

## Triage Matrix

Formalizes `references/systematic-review-screening.md`'s "Screen with
traceable decisions" guidance into an explicit trigger -> screening-decision
mapping, applied per record at the title/abstract stage:

| Trigger | Resolution Strategy |
|---|---|
| Record clearly meets every pre-registered eligibility criterion (design, population, outcome, date range, language) from the title/abstract alone | Include, with the specific criterion(s) confirmed logged as the reason |
| Record clearly fails at least one pre-registered criterion, unambiguously, from the title/abstract | Exclude, with the single primary disqualifying criterion logged (per the reference's "one primary reason for count reconciliation") |
| Title/abstract does not give enough information to confirm or rule out a criterion (e.g. study design is ambiguous, sample population unclear) | Mark uncertain and advance to full-text screening rather than guessing |
| Full text is not accessible (paywalled with no institutional access, conference abstract with no full paper) | Log as a retrieval limitation, not as an ineligibility exclusion, per the reference's explicit distinction |
| Record is a duplicate or a second report of a study already captured under a different record ID | Link to the existing record/study ID rather than screening as a new independent record, so synthesis does not double-count the evidence |

## Selected Branch

Record under review: a conference abstract (no full text obtainable through
any available institutional access or author contact after one attempt)
reporting what appears, from the abstract alone, to be an eligible study
design and population. This matches the fourth row - not the third
(uncertain-eligibility) row, since the eligibility criteria as statable from
the abstract are actually satisfied; what's missing is the full text itself,
not information about whether the criteria are met.

## End-to-End Execution Script

1. Log the record in the screening ledger: record ID `REC-0187`, source
   database, screening stage `full-text sought`, decision `unavailable`,
   reason `conference abstract, no full text obtainable via institutional
   access; single author-contact attempt made 2026-08-14, no response as of
   2026-09-11`.
2. Do not mark it `excluded` - per the reference, "missing full text is a
   retrieval limitation, not proof of ineligibility." Keep it in the
   "reports sought but unavailable" count category, separate from the
   ineligible-exclusion count, so the reconciled flow diagram does not
   misrepresent it as a screening judgment.
3. Flag it explicitly in the results-reporting stage as a study whose
   evidence could not be obtained, rather than silently dropping it from any
   count.

## Fallback Safeguards

If the author is later reached and supplies the full text, re-screen it
against the full eligibility criteria at that point rather than assuming the
abstract-level match was sufficient - full-text screening can still exclude
a record the abstract looked eligible for. If, instead, it turns out this
same study was already reported under a different record ID found via a
different database (discovered later in deduplication), immediately
reclassify from "unavailable" to "linked duplicate" and remove it from the
unavailable-reports count so the reconciled flow counts stay accurate rather
than double-counting or over-counting missing evidence.
