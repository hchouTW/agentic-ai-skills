# Grading round 9 (2026-10-01)

Procedure: as `round8.md`, 8 prompts x 2 samples (16 fresh Sonnet answerers, one prompt each, no web, told not to read `tests-and-examples.md` or `tests/`), four Opus graders (a different model; both samples of a test with the same grader). Answers: `round9_answers/`; grades: `round9_grades/G1.md`-`G4.md`. Prompts: T05, T32, T33, T40 (re-check of the round 8 source-discipline slip fixes) and new T42-T45 for `statistical-diagnostics` (added to `references/tests-and-examples.md` before the run; no reference text changed).

**Selected subset: 148/160 = 92.5%, no blocking failure.** This is not a full-suite score; the other 12 tests were not rerun.

| Test | A | B | Grader |
|---|---|---|---|
| T05 | 10 | 10 | G1 |
| T32 | 9 | 9 | G1 |
| T33 | 8 | 9 | G2 |
| T40 | 8 | 9 | G2 |
| T42 | 9 | 10 | G3 |
| T43 | 10 | 9 | G3 |
| T44 | 10 | 9 | G4 |
| T45 | 10 | 9 | G4 |

Subtotals: G1 38/40, G2 34/40 (85%), G3 38/40, G4 38/40. Slip re-check tests (T05, T32, T33, T40) 72/80 = 90.0%; new statistical tests (T42-T45) 76/80 = 95.0%.

## Round 8 slips re-checked

- Fixed in both samples: T05 (C20/C31 only for the 1.2 requirement, scan credited to C27); T32 (C36/C37 for proton/helium only, leptons to C40/C41; sqrt amplitude; joint versus separate fit, less direct in A); T40 (pulsar and dark-matter statements now C77; energy versus rigidity stated correctly).
- Not fixed: T33 data-taking period (C24 for S04) absent in B, and the distinction not raised in A; no verification level for the later time-structure papers. T40 review sample sizes (1.9e6 positrons, 5.6e5 antiprotons) omitted in both.

## New defects

- T32_A: C26 template description and C46 "unfold each day" attributed beyond what the claims state. T32_B: solar polarity of the epochs reversed.
- T44_B: C23 (S08 only) applied to S06. T45_B: C24/C25 described as species-specific inputs (they describe positron inputs from the electron sample).
- T42, T43: see `round9_grades/G3.md` (no blocking failure).

## Test-spec fixes made after grading

T45 now requires `ratio-measured` (or `ratio-cov`) rather than `ratio-toys` for a constant fit across bins; T44's threshold requirement now reads "any threshold quoted is labeled Proposal". Not done: a T45 requirement that a constant e+/e- is a hypothesis to test against time dependence.

## Caveats

Single samples; the new tests were written by the same author as the reference they exercise, so their pass is weaker evidence than a fully independent test.
