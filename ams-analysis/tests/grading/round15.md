# Grading round 15 (2026-10-02)

Procedure: as `round14.md`, 4 new prompts x 2 samples (8 fresh Sonnet answerers, no web, told not to read `tests-and-examples.md`, `tests/`, `TODO.md`, `VALIDATION.md` or `REVIEWER_PACKET.md`), one Opus grader (a different model). Answers: `round15_answers/`; grades: `round15_grades/G1.md`. New tests on the systematics and interpretation claims: T57 (Li/Be/B systematic sources, C134, C133), T58 (nitrogen resolution and migration, C140, C141), T59 (Ne/Mg/Si versus Li/Be/B trigger, cross section, rigidity scale, 1/30 TV^-1, C132, C134, C144, C146), T60 (Li/Be/B spectral indices, C136).

**Selected subset: 71.5/80 = 89.4%, no blocking failure.** Not a full-suite score, and just under the 90% bar for a subset. Half-point scoring was used.

| Test | A | B |
|---|---|---|
| T57 | 9.5 | 9.0 |
| T58 | 9.5 | 8.5 |
| T59 | 9.5 | 8.5 |
| T60 | 9.0 | 8.0 |

## Findings

- Behavior held at the boundaries: no total systematic for Li at 3.3 TV, the -20% unfolding correction kept apart from systematics, 1/30 TV^-1 attributed to the cited reference, per-interval spectral indices declined, review numbers kept apart from the Letters'.
- B samples scored at or below A in 4/4 tests: more unlabelled inference, not missing content.
- Real answer slips (single samples): T58_B says the 5.5 um is not in the Letter (it is stated there; only its derivation is in the Supplement of another reference); T59_B calls the rigidity scale "the dominant systematic" for both papers (false for Li/Be/B, where resolution is larger at 3.3 TV); T60_B attributes "no model predicted the behaviour" to both papers (C84, the review, only) and cites C84 for a C82 number.
- Pattern (2/2 on T60): the He, C, O indices are not said to come from an earlier AMS paper. Not changed: one test, one round; revisit only if it recurs.
- Pattern: own inferences without a [General method] label in 6/8 answers; not tuned (the rule exists in SKILL.md).

## Changes after grading (untested, no rerun)

- Rubrics T57-T60 reworded (grader's list of six defects): C133 allowed for T57; "at or bounding 3.3 TV"; T58 "number not in C140-C141" replaced by "not in the ledger or mis-attributed" and the documented total flux error allowed; T59 trigger systematics and correctly attributed context claims allowed; T60 documented review numbers (C82) allowed if labelled.
- C140 limitation reworded: the Letter states the 5.5 um bending resolution; its derivation is in the Supplement of Ref. [16] (the old wording induced the T58_B slip). `source-index` re-rendered; ledger still 60 sources, 182 claims.

## Caveats

Two samples per test, one grader, rubrics written by the session that wrote the claims. After the rubric rewording the round-15 score would be somewhat higher; it is reported as graded.
