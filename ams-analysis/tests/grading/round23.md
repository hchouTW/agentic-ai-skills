# Grading round 23: T48 rerun after the `cosmic-ray-databases` step 2 wording (2026-10-02)

2 fresh Sonnet answerers, one Opus grader. Answers: `round23_answers/`; grades: `round23_grades/G1.md`.

**T48: A 9.0, B 8.0 (mean 8.5/10), no blocking failure, no AMS flux value given.**

The step 2 wording (reason for combo and conversion level 0, C127; time series excluded by default, C128) did not fully close the slip. A states levels 0 mean no combos or conversions and keeps the native axis but not why, and cites C128 only inside "C126-C128"; B gives a reason for conversion level 0 (the AMS proton flux is in rigidity) but none for combo level 0, and misses time series excluded by default. Neither mentions that level 2 uses a stand-in A for elements as a last resort. Minor: B states a CRDB sub-experiment "matches S06" from the date range alone; A's "C36, C43-C53" is too broad (C47 and C53 are lepton hysteresis).

Closed as a known limitation (6 samples over rounds 19, 20 and 23 with the same partial omission, one narrow wording change tried); do not tune further for single-sample slips.
