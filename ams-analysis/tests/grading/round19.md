# Grading round 19: targeted rerun of T48, T49, T59, T60 (2026-10-02)

Purpose: first behavioral check after the round 18 rubric pass (T59 rubric accepts either reading of "trigger efficiency"), the `cosmic-ray-databases` and `source-index` header fixes (T48), and the attribution glosses (T49, T60). Procedure as in round 18: 2 fresh Sonnet answerers per test (one prompt each, no web, told not to read the tests, `TODO.md`, `VALIDATION.md` or `REVIEWER_PACKET.md`), one Opus grader (a different model) checking numbers against `data/claims.json`. Answers: `round19_answers/`; grades: `round19_grades/G1.md`. Half-point scoring.

**Targeted subset: 73.5/80 = 91.9%, no blocking failure** (not a full-suite score).

| Test | A | B | Average |
|---|---|---|---|
| T48 | 9.0 | 9.0 | 9.0 |
| T49 | 9.5 | 9.0 | 9.25 |
| T59 | 9.5 | 9.0 | 9.25 |
| T60 | 9.0 | 9.5 | 9.25 |

Slips (all single-sample, none blocking): T48_A and T48_B set CRDB combo and conversion levels to 0 without explaining levels 0/1/2 (C127), and T48_B cites C126 for a statement only C128 makes; T49_B says systematics "differ by species" unlabelled and paraphrases beyond C161; T59_B subtracts two printed upper bounds as if measured; T59_A omits the two rigidity ranges; T60_A calls C148's -0.045 +- 0.008 an "index offset from He, C, O" (it is the Ne/O, Mg/O, Si/O average above 86.5 GV) and leans toward a mechanism in its General-method text; T60_B understates the evidence for C82. The T49_B and T60 attribution slips of round 18 did not recur in a form that blocks.

Limits: rubrics written by the session that edited them; one grader.
