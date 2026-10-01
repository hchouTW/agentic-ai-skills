# Grading round 11 (2026-10-02)

Procedure: as `round10.md`, 2 prompts x 2 samples (4 fresh Sonnet answerers, one prompt each, no web, told not to read `tests-and-examples.md`, `tests/`, `TODO.md` or `VALIDATION.md`), one Opus grader (a different model; all four answers). Answers: `round11_answers/`; grades: `round11_grades/G1.md`. Prompts: T33 and T40, re-check of the two fixes merged in PR #71 (C77 errors are absolute; per-alternative verification level, date and data period). The ledger had C105-C106 added in the same PR; neither test cites them.

**Selected subset: 37/40 = 92.5%, no blocking failure.** Not a full-suite score; the other 14 tests were not rerun.

| Test | A | B | Grader |
|---|---|---|---|
| T33 | 10 | 9 | G1 |
| T40 | 9 | 9 | G1 |

Round 10 on the same two tests: T33 9, 9; T40 9, 10.

## Round 10 slips re-checked

- **Held (T40, both samples):** the 0.035 and 0.06 errors are stated as absolute on 2.00 (A converts them to about 1.8% and 3%); C77 (energy) kept apart from C75/C06 (rigidity); 1.9e6 and 5.6e5 called the review's samples; pulsar and dark-matter statements conditional; no claim of proof.
- **Held in A, partly in B (T33):** A gives level, publication date and data period for every alternative (S02, S03, S04, S01, S46). B does not: it lists S05 as metadata-only (the ledger has full text, main article, and the row carries a note against exactly this) with no data period, and says S46's data period is not in the row although the row records an 11-year dataset without dates.

## New defects (details in `round11_grades/G1.md`)

- T40_A: says the 3% systematic is "dominated by" systematics carried over from the two analyses; nothing in the ledger says what it is made of.
- T40_B: cites "56-61% statistical error on the last positron bin (C95)" for the ratio: 56% is the nominal last-bin error and 61% a tighter-cut stability check, not a range, and that bin belongs to the flux up to 1 TeV, above the 525 GeV top of the ratio fit.

## Not changed

No reference text changed after grading. The T33_B slip (S05 level) is single-sample and the ledger already warns against it.

## Caveats

Two samples per test and one grader; the grader reads the same ledger the reference was built from.
