# Grading round 10 (2026-10-01)

Procedure: as `round9.md`, 3 prompts x 2 samples (6 fresh Sonnet answerers, one prompt each, no web, told not to read `tests-and-examples.md` or `tests/`), two Opus graders (a different model; both samples of a test with the same grader). Answers: `round10_answers/`; grades: `round10_grades/G1.md` (T33, T40) and `G2.md` (T45). Prompts: T33, T40 (re-check of the round 9 follow-up fixes) and T45 (re-check after the rubric gained "a constant e+/e- is a hypothesis to test"). No reference text changed before the run.

**Selected subset: 55/60 = 91.7%, no blocking failure.** Not a full-suite score; the other 13 tests were not rerun.

| Test | A | B | Grader |
|---|---|---|---|
| T33 | 9 | 9 | G1 |
| T40 | 9 | 10 | G1 |
| T45 | 9 | 9 | G2 |

Subtotals: G1 37/40 (92.5%), G2 18/20 (90.0%). Round 9 on the same three tests: T33 8, 9; T40 8, 9; T45 10, 9.

## Round 9 follow-up fixes re-checked

- **Held (both samples):** T33 gives the S04 data period (C24) next to the publication date and states that the index has no data period for S02; T40 gives the review sample sizes (1.9e6 positrons C95, 5.6e5 antiprotons C74) as the review's, separates C77 (energy) from C75/C06 (rigidity), and tags the pulsar and dark-matter statements as C77 interpretation.
- **T45 new requirement:** met fully in B (hypothesis to test, full-covariance chi2 with toy-calibrated p-value, time-dependent alternative); only partly in A (calls it a hypothesis but never says the chi2 or p-value can reject it, no time-dependent alternative). `ratio-measured` / `ratio-cov` / `ratio-toys` named correctly in both.
- **Not fully held:** T33 does not give a verification level for every alternative (S01 missing in both, S46 missing in A); a data period is given only for S04.

## New defects (details in the grade files)

- Claim-ID slips: T45 both samples co-cite C40 for e+ versus e- statements (C40 is e- versus p; C41 supports them); T45_B cites C49 for lepton Bartels-rotation binning (C49 is proton, helium and nuclei only) and uses C24/C25/C26 for "separate template provenance" (they say the positron template and data/MC correction come from the electron sample); T45_A co-cites C89 for the 830 days (C39 and C90 hold it); T33_B tags 1.9 million positrons as C24 (it is C04/C95).
- Science: T40_A reads absolute errors on a ratio of 2.00 as percentages ("3.5% stat, 6% syst"; they are 1.75% and 3%), the same slip class as round 9; T45_A lists bremsstrahlung as charge-sign dependent; T33_A quotes E_s = 810 (+310, -180) GeV without a claim ID (it is C97).

## Fix made after grading (untested, no rerun)

`time-dependent-analysis` lepton-periodicity line now says C40 is e- versus p, C41 is the e+/e-/p claim, the 830-day transition is C39/C90 (not C89), and C49 never covers leptons. Not addressed: the absolute-versus-percent error slip and the T33 verification-level gaps (single-sample, minor).

## Caveats

Single samples per test; answerers and graders are different models but graders read the same ledger the reference was built from.
