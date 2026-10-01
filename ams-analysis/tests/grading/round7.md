# Grading round 7 (2026-10-01): targeted rerun of the tests below 9 in round 6

Procedure: as round 6 (`round6.md`): one prompt per answerer (fresh Sonnet, no web), two new samples (C, D) per prompt, three Opus graders (a different model; both samples of a test with the same grader). Only the seven tests that scored below 9 in round 6 were rerun: T05, T08, T32, T33, T39, T40, T41. No reference was changed between rounds 6 and 7 except the C06 citation in `antimatter-and-leptons` made at the end of round 6. Answers: `round7_answers/`; grades: `round7_grades/Ga.md`, `Gb.md`, `Gc.md`.

| Test | C | D | Round 6 (A, B) |
|---|---|---|---|
| T05 | 8 | 9 | 8, 9 |
| T08 | 10 | 10 | 8, 8 |
| T32 | 9 | 10 | 9, 8 |
| T33 | 9 | 9 | 8, 8 |
| T39 | 9 | 9 | 8, 10 |
| T40 | 9 | 8 | 8, 9 |
| T41 | 8 | 9 | 8, 9 |

Rerun total **126/140 = 90.0%** (round 6 on the same tests: 118/140 = 84.3%). No blocking failure.

**Full-suite estimate (not a clean pass).** Folding the rerun into the round-6 total (284/320):
- replacing the seven tests' round-6 scores with the reruns: 292/320 = 91.25%. This is optimistic: the tests were selected for scoring low, so some of the gain is regression to the mean, and the other nine tests were not rerun.
- pooling all four samples of the seven tests (mean per answer): 288/320 = 90.0%, exactly at the bar.
Neither is a full-suite rerun, so this round does not establish a pass under the original bar. A full 16-prompt, 2-sample rerun would.

Remaining defects (none blocking), from the graders:
- T41 (both samples) misses C39 (S42 abstract, 830 +- 30 day transition) and C89; T41_C says the opposite of the ledger on whether S42 gives the fit result. Same C39/C89/S42 pattern as rounds 5 and 6.
- T33 (both) states the publication-date versus data-period principle but not the dates (C24: 19 May 2011 to 12 Nov 2017).
- T39 (both) attribute to the review (C80) a statement that the Li survival result is "consistent" with the review's results; C80 says only that it "complements" C29.
- T40_D derives "about 3.5%" relative error from C77; it is 0.035/2.00 = 1.75%.
- T05: cutoff-scan and quadrature citations still compressed onto neighbouring claims.
- T08 is fixed in both samples (10, 10, C06 cited with the right scope), consistent with the round-6 C06 fix, though two samples cannot isolate it from variance.
