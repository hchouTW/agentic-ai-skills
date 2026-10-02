# Grading round 16 (2026-10-02)

Procedure: as `round15.md`; a rerun of T58 and T60 (2 samples each, 4 fresh Sonnet answerers, no web, same exclusions; one Opus grader) to check the round 15 rubric rewording and the C140 limitation fix. Answers: `round16_answers/`; grades: `round16_grades/G1.md`.

**Selected subset: 36.5/40 = 91.3%, no blocking failure** (round 15, same tests: 35.0/40 = 87.5%). Not a full-suite score; two samples per test, so the rise is within sampling noise but no regression.

| Test | A | B |
|---|---|---|
| T58 | 9.0 | 9.0 |
| T60 | 9.0 | 9.5 |

## Round 15 slips

- T58_B "5.5 um is not in the Letter": **did not recur** (both samples say the Letter states it and its derivation is in the Supplement of Ref. [16]); the C140 wording fix held.
- T60 "no model predicted" attributed to the 2018 paper and the wrong claim ID for -0.266: did not recur.
- T60 He/C/O indices not attributed to an earlier AMS paper: recurred in 1 of 2 (T60_A); missed in 3 of 4 T60 answers across rounds 15-16.

## Open

- He/C/O provenance (3/4): candidate for a one-line nudge in `nuclei-and-isotopes` if it recurs after the next change; left alone because the two rounds did not change the reference and one sample got it right.
- C140 did not say which of N_i and aleph_i is the migration-corrected count. **Fixed after grading (untested, no rerun):** read on the Letter's text layer, Eq. (1) defines N_i as the events corrected for bin-to-bin migration (flux Phi_i = N_i/(A_i eps_i T_i dR_i)) and aleph_i as the observed events in bin i; unfolding is by reference to Ref. [20]. C140 now states this; ledger still 60 sources, 182 claims, `source-index` re-rendered. Text layer only, definitions with no signs or exponents; a separate verifier was not used because no number was added.
- Rubric: T60 should list C131, C135 and the review claims C84/C85 as acceptable labelled context (cosmetic; not applied).
