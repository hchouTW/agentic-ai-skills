# Grading round 14 (2026-10-02)

Procedure: as `round13.md`, 4 new prompts x 2 samples (8 fresh Sonnet answerers, one prompt each, no web, told not to read `tests-and-examples.md`, `tests/`, `TODO.md`, `VALIDATION.md` or `REVIEWER_PACKET.md`), one Opus grader (a different model, all eight answers). Answers: `round14_answers/`; grades: `round14_grades/G1.md`. New tests: T53 (Li/Be/B, C131, C133, C135), T54 (nitrogen, C137, C142), T55 (Ne/Mg/Si, C143, C145, C147, C148), T56 (S09 supplement detector, selection and template fit, C175, C177).

**Selected subset: 76/80 = 95.0%, no blocking failure.** Not a full-suite score. Rubrics were written by the session that wrote the ledger claims, so the margin over the 90% bar is optimistic.

| Test | A | B |
|---|---|---|
| T53 | 10 | 10 |
| T54 | 8 | 9 |
| T55 | 10 | 10 |
| T56 | 10 | 10 |

## Findings

- All four deductions are on T54 and are rubric defects: the prompt does not ask for the 8.5e10 total or the source N/O statement. Both items were made conditional ("if quoted", "if mentioned"). T55's "fits are empirical" was dropped (C147/C148 do not say it). T53's 8.5e10 item now accepts the ledger wording.
- Attribution drift (both T54 samples): "O purely primary, B purely secondary" is cited to C142 but that wording is in C91's limitations. Single phrase, no cluster elsewhere.
- T55_A attributes the "at least two classes" wording to the Letter; it is C92 (S01).
- T56 supplement-boundary behaviour held: both decline per-bin chi2 and purity and keep C175 apart from C121.
- Not graded: C132, C134, C138, C140, C141, C144, C146 (systematics lists) and C136 remain without a test.

## Changes after grading (untested, no rerun)

Rubric edits only; no reference or claim changed.
