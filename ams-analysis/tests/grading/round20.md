# Grading round 20: T48 rerun after the SSDC page claim C183 (2026-10-02)

2 fresh Sonnet answerers (no web, told not to read tests, TODO or VALIDATION), one Opus grader checking against C125-C130 and C183. Answers: `round20_answers/`; grades: `round20_grades/G1.md`. Half-point scoring.

**T48: A 8.5, B 9.0 (average 8.75/10), no blocking failure, no prohibited claim.** Targeted, 2 samples.

Slips: neither answer cites C127 or explains why the cross-check uses combo and conversion level 0 (same slip as both samples of round 19); A cites C126 for the time-series default that only C128 states, cites S41 and S43 without claim IDs, and omits the currency caveat; B says the S06 flux tables are in the Supplemental Material, which no claim supports, and calls the 2018 sub-experiment "a different dataset and analysis", slightly beyond the documented test query.

Fix after this round (not re-tested): step 2 of the cross-check procedure in `cosmic-ray-databases` now states the reason for levels 0 (C127) and that time series are excluded by default (C128). The new SSDC wording (C183) was used correctly by both answers: no holdings claimed, no confusion of "Version 3.3" with the LPSC CRDB.
