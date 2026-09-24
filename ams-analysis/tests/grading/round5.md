# Grading round 5: kit for an independent grader

Purpose: check the skill against the S01-derived claims C63-C100 and re-check the earlier fixes (T30, T33, T23 length). This kit was prepared on 2026-09-21 and **run on 2026-09-25** (results below). Maintainer material: it lives in `tests/`, not in the routed references.

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

Run 2026-09-25. Answerers: Sonnet, fresh context, no web. Deviation from step 1: to save cost, each
answerer took 4 prompts (treated as independent requests) instead of 1; samples A and B used
different batch groupings. Grader: Opus (a different model), four graders with 8 answers each,
both samples of a test with the same grader. Answers: `round5_answers/`; full grades with
defect lists: `round5_grades/`.

**Suite: 261/320 = 81.6%, no blocking failure. Below the 90% pass bar.** Every quoted AMS number
traced to a claim that allows numeric quotation. Losses were source discipline (claim IDs
missing on [Documented] tags, verification strength overstated, cross-citations missing,
claims widened past their scope) and missing required items.

| Test | Sample | Score /10 | Blocking failure |
|---|---|---|---|
| T05 | A | 8 | none |
| T05 | B | 6 | none |
| T08 | A | 8 | none |
| T08 | B | 8 | none |
| T23 | A | 9 | none |
| T23 | B | 9 | none |
| T24 | A | 9 | none |
| T24 | B | 8 | none |
| T29 | A | 6 | none |
| T29 | B | 6 | none |
| T30 | A | 9 | none |
| T30 | B | 10 | none |
| T31 | A | 8 | none |
| T31 | B | 6 | none |
| T32 | A | 9 | none |
| T32 | B | 8 | none |
| T33 | A | 8 | none |
| T33 | B | 7 | none |
| T35 | A | 8 | none |
| T35 | B | 9 | none |
| T36 | A | 7 | none |
| T36 | B | 9 | none |
| T37 | A | 9 | none |
| T37 | B | 10 | none |
| T38 | A | 8 | none |
| T38 | B | 9 | none |
| T39 | A | 9 | none |
| T39 | B | 8 | none |
| T40 | A | 8 | none |
| T40 | B | 8 | none |
| T41 | A | 9 | none |
| T41 | B | 8 | none |

Fixes made (narrow, one per root cause):
- `references/inference-and-unfolding.md`: the column-sum normalization sentence had the two
  cases reversed relative to `scripts/validate_response.py` and the standard definition. A
  reference bug, found by the T30 grader.
- `SKILL.md` source-verification rule: every [Documented] tag carries its claim ID, and evidence
  is described only at the claim's own verification level (T32_B called abstract-level claims
  "full-text-verified"; the A samples of T35-T37 had no C-IDs).
- `references/antimatter-and-leptons.md`: C99's 1.9 TeV exclusion now carries its model and
  range scope (both T36 samples stated it as universal).
- `references/analysis-artifacts.md`: the brief template now has one line each for selections,
  backgrounds, the efficiency/acceptance/livetime/response split, inference, and validation.
  It had disagreed with the T29 rubric, and both T29 samples lacked these items.

Targeted rerun after the fixes: one fresh Sonnet sample (C) each of T29, T30, T35, T36, T40
and T41, with a new Opus grader: **47/60 = 78%, no blocking failure**
(`round5_grades/grades_rerun.md`).
- T36 rose to 9: the C99 scope was kept, though one sentence overreached.
- T29 stayed at 6: it misses the test's critical items (T/A needs A and mass; S07 is read at
  main-article level only) and mis-attributes C59/C60.
- The others stayed within the per-answer spread of 1-2 points.
One sample per prompt cannot separate the effect of a fix from grader or answerer variance.
Remaining pattern: claim-boundary discipline (missing expected cross-citations such as C06,
C39/C89/S42 and C26; C72 read as an ECAL-only factor; documented results pushed one step
past their support). This round is stricter than rounds 3-4 (94.8%, 95.0%), and it adds the
new S01 tests T35-T41, so the scores are not directly comparable.
