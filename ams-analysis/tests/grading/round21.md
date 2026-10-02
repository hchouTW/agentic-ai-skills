# Grading round 21: new tests T62-T66 (2026-10-02)

Tests added for claims no earlier test cited: T62 Layer-0 planned versus actual (C101, C102), T63 antideuteron search status (C19), T64 Na/Al flux paper (C162-C166), T65 strangelet null result (C87), T66 daily-proton wavelet method and trial factor (C45, C52). 2 fresh Sonnet answerers per test (no web, told not to read tests, TODO or VALIDATION), one Opus grader (a different model) checking numbers against `data/claims.json`. Answers: `round21_answers/`; grades: `round21_grades/G1.md`. Half-point scoring.

**New tests: 95.0/100 = 95.0%, no blocking failure** (A 47.0/50, B 48.0/50).

| Test | A | B | Mean |
|---|---|---|---|
| T62 | 9.0 | 9.5 | 9.25 |
| T63 | 9.5 | 10.0 | 9.75 |
| T64 | 9.0 | 8.5 | 8.75 |
| T65 | 10.0 | 10.0 | 10.0 |
| T66 | 9.5 | 10.0 | 9.75 |

Slips (single-sample): T62_A overstates that antiproton systematics are dominated by background and selection (true at high rigidity only, C121 versus C23); T64_B inverts the unfolding definition, presenting N_i as the observed count and the aleph_i as the unfolded count (in the Ne/Mg/Si convention of C140 it is the other way round; C164 does not define them for Na/Al, which the rubric now says); T64_A asserts "not double counted" without a claim; T63_A phrasing about the beta window is misleading (labeled proposal); T66_A calls the 27-day signal plausible from solar rotation unlabeled; minor jargon in T62_B.

Rubric defects fixed in this change: T64 prohibited item on a "total systematic budget" (the C162 totals at 100 GV are allowed; a per-bin breakdown is not) plus an explicit inverted-definition item; T63 antihelium wording (a labeled contrast is fine); T66 citation expectation (C105 and C36 acceptable). C164 was not edited: adding the N_i definition would require reading S59 again.

Limits: rubrics written by the same session that read the claims, so the margin over 90% is optimistic; one grader; targeted new tests, not a full-suite score. The suite now has T01-T66.
