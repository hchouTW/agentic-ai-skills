# Grading round 17 (2026-10-02)

Procedure: as `round16.md`; new test T61 (nitrogen selection and backgrounds, C138, C139) and a rerun of T60 after a one-line attribution nudge in `nuclei-and-isotopes` (comparison indices and fluxes such as He, C, O come from earlier AMS papers, S11; C136, C142, C148). 4 fresh Sonnet answerers (2 samples each), one Opus grader. Answers: `round17_answers/`; grades: `round17_grades/G1.md`.

**Selected subset: 37.5/40 = 93.8%, no blocking failure.** Not a full-suite score.

| Test | A | B |
|---|---|---|
| T61 | 9.5 | 9.5 |
| T60 | 9.5 | 9.0 |

## Findings

- **He/C/O provenance met in both T60 samples** (missed in 3 of 4 answers in rounds 15-16; both now name S11 / Ref. 14). Two samples, so the nudge is the likely cause, not proven. T60 alone: 17.0 (round 15), 18.5 (round 16), 18.5.
- Earlier T60 slips ("no model predicted" credited to the 2018 paper, wrong claim ID for -0.266) did not recur.
- Milder residual slips: T60_A states the 10Be attribution as fact in a caveat (the paper says "most likely"); T60_B says the effect "therefore accounts for part of the secondary hardening" and has one garbled unsourced sentence on power laws.
- T61 clean: selection, 90-95% purity, template-fit and simulation backgrounds and the < 1.5% total all correct; no Li/Be/B or Ne/Mg/Si numbers imported.

## Changes after grading (untested, no rerun)

- T61 had been placed after the closing fence of the YAML test block; the fence is now below T61.
- Rubrics: T60 lists the acceptable context claims and states that the review's -0.266 +- 0.022 is not a per-interval value of the Li/Be/B paper; T61 lists C137, C141 and labelled review claims as acceptable.
