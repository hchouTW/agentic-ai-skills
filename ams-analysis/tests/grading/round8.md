# Grading round 8 (2026-10-01)

Procedure: as `round6.md`: the same 16 prompts, one prompt per answerer (32 fresh Sonnet answerers, samples A and B, no web, told not to read `tests-and-examples.md` or `tests/`), four Opus graders (a different model; both samples of a test with the same grader). Answers: `round8_answers/`; grades: `round8_grades/G1.md`-`G4.md`. Run after two reference fixes (below); `claims.json` unchanged.

**Suite: 297/320 = 92.8%, no blocking failure. Clean full-suite pass of the 90% bar (288).** Round 6: 88.75%; round 7 (targeted): 90.0%.

| Test | A | B |
|---|---|---|
| T05 | 9 | 9 |
| T08 | 8 | 9 |
| T23 | 10 | 10 |
| T24 | 10 | 9 |
| T29 | 9 | 10 |
| T30 | 10 | 10 |
| T31 | 10 | 9 |
| T32 | 9 | 8 |
| T33 | 9 | 8 |
| T35 | 9 | 10 |
| T36 | 10 | 8 |
| T37 | 10 | 10 |
| T38 | 9 | 10 |
| T39 | 10 | 9 |
| T40 | 9 | 9 |
| T41 | 9 | 9 |

Grader subtotals: G1 (T05, T08, T23, T24) 74/80; G2 (T29-T32) 75/80; G3 (T33, T35-T37) 74/80; G4 (T38-T41) 74/80.

## Fixes under test (made before this round)

- `nuclei-and-isotopes`: C80 no longer described as "consistent with" the Li result C29 (the ledger says only "complements"). T39: 9, 9 -> 10, 9; the "consistent" over-attribution is gone, but T39_B did not cite C29.
- `time-dependent-analysis`: S42 abstract (C39) carries the 830 +- 30 d transition; cite C90 with C39/C89. T41: 8, 9 -> 9, 9. T41_B still calls the logistic fit "the review's own" without S42; T41_A credits C49's per-rotation unfolding to the lepton analysis.
- Single samples cannot separate a fix from variance; treat both as improved, not proven.

## Remaining defects (none blocking)

- T05 (both): C20/C31 cited for varying the cutoff factor (belongs to C23, C27, C49, C60). Same pattern as round 6.
- T08: "about 10^4 protons per antiproton" without C74 (both); T08_A misreads the prompt.
- T24_B: "no measured data" on antinucleus interaction cross sections overstates.
- T32 (both): C36/C37 (proton, helium) cited as lepton periodicity; no joint-versus-separate fit comparison in B; amplitude a^2+b^2 instead of sqrt in B.
- T33 (both): alternatives offered without verification level; T33_B gives no data-taking period (C24).
- T35_A: negative-rigidity sample suggested as proton-enriched control (wrong).
- T36_B: antiproton claims C75/C77 cited for the electron/positron interpretation.
- T38_A: tells the user to attribute C91 to the unread nitrogen paper.
- T40: C75 attached to the wrong ratio, a wrong "mixes energy and rigidity" claim (A), review sample sizes omitted (both).
- T29_A: C62 carbon corrections quoted while helium numbers (C59) are said to be in the paper only.
- T31_B: lists only some specification fields.
