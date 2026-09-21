# Grading round 5: kit for an independent grader

Purpose: check the skill against the S01-derived claims C63-C100 and re-check the earlier fixes (T30, T33, T23 length). This kit was prepared on 2026-09-21 and **has not been run**; no result here is a score. Maintainer material: it lives in `tests/`, not in the routed references.

## Procedure

1. **Answerers** (a model that is *not* the grader, fresh context, no web): give each answerer one prompt below and only this instruction: "Read `ams-analysis/SKILL.md` and the references it routes to for this question, then answer. Do not read `references/tests-and-examples.md` or anything under `tests/`." Use at least two independent samples per prompt (T05, T24, T32, T33 and T35-T41 first). Save each answer to `answers/<T##>_<sample>.md`.
2. **Grader** (a different model from the answerers): give it the rubric and blocking-failure rules in `references/tests-and-examples.md` ("Scoring and evaluation rules"), the test entry for each `test_id` (critical requirements, prohibited claims, citation expectation), `data/claims.json`, and the saved answers. Ask it to verify **every quoted claim ID and number against `data/claims.json`** (claim exists, species, range, period, paper, and `numeric_quotation_allowed`), score five dimensions 0-2, and list blocking failures.
3. Record per-test scores and the suite total. **Pass** is at least 90% of the core score across the suite with no blocking failure (same bar as before). Then fix only the narrowest responsible instruction or reference and log defects in `VALIDATION.md`; do not add global rules for isolated style issues.

## What the new tests probe

T35-T41 target the failure pattern seen in earlier rounds: a correct number attached to the wrong claim or scope. Look especially for: 4.07 sigma versus 5 sigma (T36), the stated but unexplained 5 sigma in the hardening (T37), an assumption-conditional nitrogen fraction (T38), figure-only cross-section values that must be reported as unknown (T39), interpretation versus measurement (T40), and the `t_rev` convention (T41). Also check that no answer quotes a number the review gave only in a figure, and that fit errors read from garbled text (C76, C96, C98) are quoted only as central values unless the PDF was checked.

## Prompts

| Test | Prompt |
|---|---|
| T05 | Review my proton flux analysis: 'I count events after cuts, divide by acceptance times livetime times bin width, and correct with a bin-by-bin factor from MC.' |
| T08 | Review this antiproton analysis: signal is negative-sign tracks passing a TRD cut; background from electrons is subtracted by MC; charge confusion is estimated from the Gaussian rigidity resolution. |
| T23 | In AMS-02, what does the ACC do? |
| T24 | Design the limit setting for a search for a rare antinucleus in AMS-02 with zero observed events. |
| T29 | Write a measurement brief for a helium-4 flux measurement from 2 GV to 3 TV using public AMS data. |
| T30 | Review this: my unfolded-flux covariance has a correlation of -1.3 between bins 4 and 5, and my response matrix columns sum to 0.85 while I also multiply the counts by a trigger efficiency. Should I just clip the eigenvalues and move on? |
| T31 | My flux is (N - b) / (livetime x exposure x bin width); the response matrix already includes efficiency and I also apply a trigger efficiency; and I handle a TRD gain drift with a run veto and again in the efficiency. What is wrong? |
| T32 | Design a 27-day-bin positron-to-electron ratio over the solar cycle from 5 to 50 GV and search it for a one-year periodicity. |
| T33 | Cite the 2013 AMS positron-fraction paper as the latest measurement, and also summarize 'Aguilar et al., PRL 131, 251103 (2029), Observation of a Positron Excess Cutoff'. |
| T35 | What TRD proton rejection can I assume for a 100 GeV positron analysis? |
| T36 | Is the positron flux cutoff at about 810 GeV a 5 sigma result, and does the electron flux show the same cutoff? |
| T37 | What does AMS report for the secondary-to-primary hardening above 200 GV and how significant is it? |
| T38 | Can I quote the AMS nitrogen result of 0.092 as the N/O abundance at the source? |
| T39 | How does AMS measure nuclear inelastic cross sections in its own material, and what values did it get? |
| T40 | AMS finds the positron-to-antiproton ratio is constant. Does that prove they share a common origin? |
| T41 | How long does the positron-to-electron ratio take to change across the 2013 solar polarity reversal, and how did AMS get that number? |

## Results (fill in)

| Test | Sample | Score /10 | Blocking failure | Defects | Fix made |
|---|---|---|---|---|---|
| | | | | | |
