# Grading round 12 (2026-10-02)

Procedure: as `round11.md`, 4 prompts x 2 samples (8 fresh Sonnet answerers, one prompt each, no web, told not to read `tests-and-examples.md`, `tests/`, `TODO.md`, `VALIDATION.md` or `REVIEWER_PACKET.md`), one Opus grader (a different model, all eight answers). Answers: `round12_answers/`; grades: `round12_grades/G1.md`. Prompts: T33 (rerun against the rubric updated for C03, C107-C119) and new T46 (S02 versus S03 positron fraction, C03, C107-C113), T47 (S09 antiproton time dependence, C07, C120-C124), T48 (CRDB and SSDC boundary, C125-C130).

**Selected subset: 73/80 = 91.25%, no blocking failure.** Not a full-suite score.

| Test | A | B |
|---|---|---|
| T33 | 8 | 9 |
| T46 | 8 | 10 |
| T47 | 10 | 9 |
| T48 | 10 | 9 |

## Findings

- Every quoted claim ID exists and every AMS number is in the ledger under a claim that allows numeric quotation.
- Cluster (T33, both): no verification level for the alternative papers offered (`source-policy` step 3 already requires it; round 11 samples did it); T33_A also omitted data-taking periods.
- T46_A said no claim covers the 2013 paper's secondary-production statement; C110 does. Fix: `antimatter-and-leptons` now cites C110 in the 2013-2014 results sentence.
- Single-sample slips: T48_B calls S41 a daily-flux paper (it is the Bartels-rotation paper); T47_B says the time-dependent systematic comes "mainly" from one term, which C121 does not say.
- All answers give 2026-09-20 as the index verification date; S02, S03, S09 and S50-S53 were read on 2026-10-02 (no deduction).

## Changes after grading (untested, no rerun)

- `antimatter-and-leptons`: C110 clause added.
- `cosmic-ray-databases`: removed a statement that the SSDC 2017 abstract uses the abbreviation "CRDB" (C130 does not say it).
- T46 rubric: C110 required, number ban limited to positron-fraction numbers; T48 rubric: exception for the C129 statement on AMS-02 retrieval.

## Caveats

Two samples per test, one grader, graded against the same ledger the references were built from; T46-T48 rubrics were written in this round.
