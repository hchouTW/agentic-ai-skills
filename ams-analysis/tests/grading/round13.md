# Grading round 13 (2026-10-02)

Procedure: as `round12.md`, 6 prompts x 2 samples (12 fresh Sonnet answerers, one prompt each, no web, told not to read `tests-and-examples.md`, `tests/`, `TODO.md`, `VALIDATION.md` or `REVIEWER_PACKET.md`), one Opus grader (a different model, all twelve answers). Answers: `round13_answers/`; grades: `round13_grades/G1.md`. Prompts: new T49 (Fe and F papers, C149-C161), T50 (sulfur paper, attribution of numbers quoted from earlier references, C172-C173), T51 (S09 supplement versus per-rotation values, C178-C180), T52 (S41/S42 supplement captions, C181-C182), and reruns of T46 and T48 to check the round 12 fixes.

**Selected subset: 117/120 = 97.5%, no blocking failure.** Not a full-suite score. The rubrics for T49-T52 were written in this session, so the margin over the 90% bar partly reflects tests written by the same author as the ledger.

| Test | A | B |
|---|---|---|
| T46 | 10 | 10 |
| T48 | 10 | 9 |
| T49 | 9 | 10 |
| T50 | 10 | 9 |
| T51 | 10 | 10 |
| T52 | 10 | 10 |

## Round 12 fixes held

- T46: both samples cite C110 and attribute it to the 2013 paper (round 12: 8 and 10; now 10 and 10).
- T48: neither sample repeats the SSDC "CRDB" abbreviation, and the S41 "daily-flux" slip did not return.

## Slips (single samples, no cluster)

- T49_A calls the 0.140 +- 0.025 hardening of the light ratios "seen in B/O" (C160: an earlier-AMS result for all light ratios).
- T48_B says CRDB "holds several AMS proton datasets" with no query run.
- T50_B does not say the fits are empirical (low-value; C172 already says it).
- Carry-over: dates quoted as 2026-09-20 although S02, S03, S09 and the nuclei papers were read on 2026-10-02; neither T48 answer explains why conversions are off (C127).

## Changes after grading (untested, no rerun)

- `nuclei-and-isotopes`: examples of earlier-reference numbers (C160, C173).
- `cosmic-ray-databases`: which AMS datasets a CRDB release holds is [Unknown/needs input] until queried; C129 wording corrected.
- `source-index` header: rows read later carry their own access date.
- Rubrics: T52 no longer requires the 2-3 GeV electron structure (moved to prohibited), T48 prohibited-claim wording corrected (the "developed to retrieve AMS-02 results" wording was C130's, not C129's).

## Caveats

Two samples per test, one grader, the same ledger the references were built from; tests T49-T52 and their rubrics were written by the same session that added the claims.
