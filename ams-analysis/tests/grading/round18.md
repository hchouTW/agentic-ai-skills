# Grading round 18: full-suite rerun (2026-10-02)

Procedure: every test in `references/tests-and-examples.md` (T01-T61), 2 samples each = 122 fresh Sonnet answerers (one prompt each, no web, told not to read `tests-and-examples.md`, `tests/`, `TODO.md`, `VALIDATION.md` or `REVIEWER_PACKET.md`; at most 20 concurrent). Five Opus graders (a different model), one per block of tests: G1 T01-T12, G2 T13-T24, G3 T25-T36, G4 T37-T48, G5 T49-T61. Answers: `round18_answers/`; grades: `round18_grades/G1.md`-`G5.md`. Replaces the 2026-10-01 full-suite number (round 8, 297/320 = 92.8%, 16 prompts).

**Full suite: 1181/1220 = 96.8%, no blocking failure.**

| Block | Tests | Score |
|---|---|---|
| G1 | T01-T12 | 233.5/240 = 97.3% |
| G2 | T13-T24 | 235.5/240 = 98.1% |
| G3 | T25-T36 | 231.5/240 = 96.5% |
| G4 | T37-T48 | 229.5/240 = 95.6% |
| G5 | T49-T61 | 251/260 = 96.5% |

Lowest single answers: T15_B 7.5, T59_A 8, T29_B 8.5, T40_B 8.5, T49_B 8.5. No test is below 8 on average.

## Answer defects (single samples unless stated)

- T15_B over-generalises C23 (a mis-scoped Documented claim).
- T49_B and T60_B attach a propagation reading to the paper's own claim (path length or escape, C161 and C136 do not say so); both flag model dependence elsewhere.
- T59_A answers the trigger-efficiency question with the systematics only; T59 prompt is ambiguous (see below).
- T29 (both samples): the brief does not say S07 was read at main-article level only. Candidate narrow fix in `analysis-artifacts` (print each cited source's verification level in the brief's source section); not applied, one block, one round.
- T34 (both): `RooCrystalBall` quoted as needing ROOT 6.20, G3 says 6.24 (general-knowledge detail, outside this skill).
- Single slips: T29_B an S12 number without a claim ID; T59_A "looser" wording contradicts its own numbers.

## Rubric defects found by the graders

Fixed in this change: T47 stale item (the 4 sigma comparison is in Table SA of the S09 supplement, C178); T48 stale "(no query has been run)" (one test query is documented in `cosmic-ray-databases`); T52 stray empty item.

Not applied (wording, listed for the next rubric pass): T02 citation_expectation names S17/S18 (numbers are C21/C28/C70); T04 "MDR definition-dependent" beyond the sources; T07 "AMS cuts or templates presented as AMS practice" should say undocumented; T17 "media" untestable; T18 "S15 only abstract-level" stale (C30 is full text, main article); T19 "any number" contradicts C67/C112; T22 "skill not activated" is unobservable in this harness; T23 list C21/C69 as acceptable context; T25 template-variable detail finer than C22; T26 the 1.2 factor is also documented in C56, C59, C62, C132, C138, C144; T28 "other |Z| not given" is wrong (He, C, O, Fe in C61-C63); T32 "single-frequency p-value" ambiguity; T34 "does not load AMS material" unobservable; T36 split the two significance items (C97, C99); T37 "do not confuse" should be "distinguishes from"; T42 "if toys are used"; T50 "fits are empirical" not asked; T56 two positive items beyond the prompt; T59 ambiguity "trigger efficiency" versus its systematic.

## Caveats

Two samples per test, five graders (one per block, so cross-block calibration is not controlled), rubrics written by the session that wrote the ledger. Not behaviorally re-run: the rubric and ledger edits of rounds 14-17 (included in this run, since this run is after them) and the edits made in this change. Half-point scoring, as in rounds 15-17.
