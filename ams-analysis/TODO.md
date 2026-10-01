# ams-analysis: open work for the next session

State (verified 2026-10-01 on `main`, all work merged; rounds 5-9 via PR #20, #39, #40, #43 and #47): `python3 scripts/validate_skill_bundle.py` OK with 46 files; `python3 -m unittest discover -s tests` 366 tests OK (ledger test counts match 49 sources and 104 claims); `python3 scripts/render_source_index.py` in sync. Latest behavioral result: round 9, a targeted 8-test, 2-sample run (T05, T32, T33, T40 plus new statistical-diagnostics tests T42-T45), 148/160 = 92.5%, no blocking failure (`tests/grading/round9.md`); the T33/T40 fixes made after it are untested. Latest full-suite result: round 8, a full 16-prompt, 2-sample run, scored **92.8% (297/320)** with no blocking failure, a clean pass of the 90% bar (`tests/grading/round8.md`). Earlier: round 6 scored 88.75% (284/320; round 5 was 81.6%); round 7, a targeted rerun of 7 tests, scored 90.0%. Read `VALIDATION.md` first: it records what was run, what was self-graded versus independently graded, and every known gap. Do not repeat finished work; do not claim a check passed without running it.

Ground rules: standard library only for scripts; every AMS-specific number needs a scoped claim in `data/claims.json` (edit the JSON, run `scripts/validate_evidence_ledger.py`, then `scripts/render_source_index.py --write`); never promote a claim's `verification_strength` or a source's `verification_level` without reading the source at that level; label statements [Documented] / [General method] / [Proposal] / [Unknown/needs input]. For grading, answerers and grader must be different models.

## 1. Behavioral suite (rounds 8 and 9 passed; optional polish)

- [x] Round 8 (2026-10-01): full 16-prompt, 2-sample suite scored **297/320 = 92.8%**, no blocking failure; the 90% bar is cleanly met (`tests/grading/round8.md`). The T39 C80 and T41 C39/C89 fixes helped (T39 10, 9; T41 9, 9), not proven by single samples.
- [x] Round 8 source-discipline slips (2026-10-01): added clarifying text, no behavioral rerun yet (untested). T05: `charged-cosmic-rays` and `time-dependent-analysis` now say C20/C31 state the 1.2 requirement only and the scans are C23, C27, C49, C60. T32: `time-dependent-analysis` points lepton periodicity to C40/C41/C39/C48 (not C36/C37) and adds the joint-versus-separate fit and sqrt(a^2+b^2) amplitude lines. T33: `source-policy` step 3 asks for each alternative's verification level, publication date and data period. T40: `antimatter-and-leptons` scopes C75 (antiproton/proton) versus C77 (positron/antiproton, energy), gives the review sample sizes and warns against a wrong energy-versus-rigidity claim. Not touched (single-sample, minor): T08 C74, T24_B, T35_A, T36_B, T38_A, T29_A, T31_B.

- [x] Round 9 (2026-10-01): targeted run of T05, T32, T33, T40 (round 8 slip fixes) plus new T42-T45 for `statistical-diagnostics`, 2 samples each: **148/160 = 92.5%**, no blocking failure (`tests/grading/round9.md`). Slip fixes confirmed for T05, T32 and T40 (C-tags, sqrt amplitude, energy versus rigidity); statistical tests 76/80. Follow-up fixes (untested, no rerun): `antimatter-and-leptons` has a dedicated positron-versus-antiproton paragraph (C77 energy fit, review sample sizes C95/C74, C75/C06 rigidity); `source-policy` step 2 gives the S04 data period (C24) and says the index records none for S02/S03. Still open (single-sample, minor): T32_B polarity reversed; T44_B C23 applied to S06; T33 verification level of later papers. T45 lacks a requirement that constant e+/e- is a hypothesis to test.

## 2. Evidence gaps

- [ ] S02 and S03: APS returned 401 on 2026-09-21. They are not open access and have no arXiv version. They stay at abstract-level (S02) and metadata-only (S03) unless a human supplies the PDFs.
- [x] S16 and S20 (2026-10-01): decided to keep them as grouped navigation pointers to S41-S46 and S47, still `metadata-only`; their `notes` in `data/sources.json` now say so (cite the individual record, not S16/S20). Ledger validator, renderer sync check, bundle validator and 238 tests pass.
- [ ] Supplemental Material data tables (S41-S47) are not transcribed or checked. Only the supplement text was read (C51-C58). Correlation across days/rotations and trial-factor correction remain undocumented in what was read. Keep them marked unknown.
- [x] S01 (Phys. Rept. review) introduction and summary (2026-10-01): read from the INSPIRE-hosted PDF text; two qualitative claims added, C103 (mission, orbit and the review's own characterization) and C104 (model needs and the future-program statement, not a result). No measurement or number in either. Checked against pdftotext, not a rendered page. Figure-only values (resolution curves, rejection curves, cross sections, limits) stay untranscribed by design.

## 3. Human review

- [ ] Have a human physicist review the ledger judgement calls listed in `VALIDATION.md` ("Ledger migration: differences requiring human review"): claim strengths, `support_kind`, `numeric_quotation_allowed`, tier ranges, and the S02/S03 supersession.

## 4. Routing (low priority)

- [ ] Trigger data from the isolated routing eval (2026-09-26). Setup: `hep-analysis/tests/routing_eval.py` on `hep-analysis/tests/trigger_queries_holdout.json` and on the tuning set `hep-analysis/tests/trigger_queries.json`, with all 7 repo skills loaded as project skills and 2 runs per query. "none" means the model answered without invoking any skill.
  - Sonnet: 6/6 held-out AMS queries routed here.
  - Haiku, held-out: 5/6. "Review my AMS-02 electron/positron TRD likelihood template fit" went to none once.
  - Haiku, tuning set: 2/4. "latest AMS-02 positron fraction result and its TRD selection" went to none once. "Design the AMS-02 antideuteron search selection and review it formally" went to `hep-analysis` once.

  Recheck after any description change here or in hep-analysis.

## 5. Optional, only if a routed decision needs it

- [ ] Network refresh of the ledger. It may only propose metadata changes from INSPIRE or DOI records. It must never promote a claim to full-text or rewrite scientific claims without review.
- [x] Statistical-validation items (2026-10-01): implemented small seeded, approximation-labeled versions of CLs with expected sensitivity, Feldman-Cousins and CLs with an uncertain background (Cousins-Highland marginalization), the `s >= 0` boundary p-value, finite-template effects, an unfolding-iteration scan and correlated-ratio toys (`scripts/poisson_diagnostics.py`, new `scripts/statistical_toys.py`, `references/statistical-diagnostics.md`). The remaining backlog items were done in the next entry. No behavioral (LLM) evaluation of the new reference text was run.
- [x] Remaining statistical items, second batch (2026-10-01): implemented the full per-template Barlow-Beeston fit (`scripts/template_fit.py`), profile Feldman-Cousins, profile CLs and shape/multi-nuisance limits (`scripts/likelihood_limits.py`), L-curve/cross-validated regularization choice, analytic response-covariance propagation and non-parametric forward folding (`scripts/unfolding_diagnostics.py`), and ratio toys from a measured covariance (`ratio-measured` in `scripts/statistical_toys.py`). Still not implemented, by design: weighted-MC template fits with shape nuisances, a guaranteed-coverage (hybrid or full Neyman) nuisance construction, non-Gaussian and correlated nuisance priors, bin-to-bin correlated shape nuisances, Poisson-exact cross-validation, other forward-folding priors, efficiency/lost-event response covariance, and measured response-matrix covariances. No behavioral (LLM) evaluation of the new reference text was run.
- [x] Remaining statistical items, third batch (2026-10-01): implemented weighted-MC template fits with shape and normalization nuisances (`wbb-fit`, `wbb-toys`), a guaranteed-coverage (Berger-Boos) nuisance construction with a coverage check (`neyman-limit`, `neyman-coverage`), log-normal, gamma and correlated nuisance priors (`shape-limit`), Poisson-exact cross-validation (`choose-penalty-poisson`), other forward-folding priors (`nonparam-fold --prior`, `compare-fold-priors`), multinomial lost-event and efficiency response covariance (`response-covariance --response-model`, `efficiency_uncertainty`), and measured response covariance or replicas (`response-measured`). Still not implemented, by design: varying weights inside a bin in the toy MC, a guaranteed-coverage construction for several nuisances, correlated gamma nuisances, Poisson-exact CV for the linear estimators, K-fold variants, learned or free-hyperparameter priors, spectrum-dependent efficiency uncertainties. No behavioral (LLM) evaluation of the new reference text was run.
- [ ] A YAML-subset reader for specifications, only if users actually write YAML.

## Done (do not redo; details in `VALIDATION.md`)

- **Setup:** PR #1 (`ams-analysis-executable-checks`) merged (b74b022). The skill is soft-linked at `~/.claude/skills/ams-analysis`.
- **Independent grading, first pass** (Opus grader, nine prompts): 7 pass, 2 fail (T29 blocking, T24). Narrow fixes were made, and T29 and T24 were re-run and fixed; T08 was only partly fixed.
- **Rounds 3-4** (2026-09-21), one fresh Sonnet sample per prompt, separate Opus grader:
  - Round 3 scored 94.8%: T05, T08, T24, T29, T32, T33.
  - Round 4 scored 95.0%: a second sample of T05, T24, T30, T32, T33, plus T23.
  - Neither round had a blocking failure. The fixes were in `source-policy`, `time-dependent-analysis` and `inference-and-unfolding`, plus the `validate_response.py` pointer and the rule that every [Documented] tag carries its C## ID. These answers were not archived.
- **Claim-ID root-cause fix:** the grouped bracket citations in `antimatter-and-leptons` and `charged-cosmic-rays` were split per paper. No grouped citations remain in the other references; `time-dependent-analysis` cites ranges per clause, with IDs.
- **T33 and T30 fixes:** `source-policy` step 2 now separates the publication date from the data-taking period (T33). `inference-and-unfolding` now says a column sum below one may be migration outside the tabulated range (T30). Both were re-graded in rounds 4-5.
- **Round 5** (2026-09-25): 16 prompts x 2 Sonnet samples, four Opus graders, answers archived in `tests/grading/round5_answers/`. Scored 261/320 = 81.6% with no blocking failure.
  - Added tests T35-T41 for the S01 claims C63-C100.
  - Four narrow fixes, including a reversed column-sum statement in `inference-and-unfolding`.
  - A targeted rerun scored 47/60 = 78%. T23 is no longer over-long (9/10 in both samples).
- **Round 6** (2026-10-01, PR #39): the same 16 prompts, one prompt per answerer (32 fresh Sonnet answerers, 2 samples each), four Opus graders. Scored 284/320 = 88.75% with no blocking failure (round 5: 81.6%); T29 went from 6 to 9. One narrow fix, untested at the time: `antimatter-and-leptons` now cites C06 with its abstract-level scope for the S08 antiproton counts. Results in `tests/grading/round6.md`, `round6_answers/`, `round6_grades/`.
- **Round 7** (2026-10-01, PR #40): targeted rerun of the 7 tests below 9 (T05, T08, T32, T33, T39, T40, T41), 2 fresh samples each, three Opus graders. Scored 126/140 = 90.0%, no blocking failure; T08 rose from 8, 8 to 10, 10. No reference changed. The full-suite estimate is 90.0-91.25%, with selection bias, so it is not a clean pass. Results in `tests/grading/round7.md`, `round7_answers/`, `round7_grades/`.
- **Round 8** (2026-10-01, PR #43): full rerun after two narrow fixes (C80 wording in `nuclei-and-isotopes`, S42/C39 sentence in `time-dependent-analysis`). 297/320 = 92.8%, no blocking failure. Results in `tests/grading/round8.md`, `round8_answers/`, `round8_grades/`.
- **Round 9** (2026-10-01, PR #47): targeted run, 8 tests x 2 samples, four Opus graders. 148/160 = 92.5%, no blocking failure; slip fixes for T05, T32 and T40 confirmed, new tests T42-T45 added for `statistical-diagnostics` (76/80). Afterwards: a positron-versus-antiproton paragraph in `antimatter-and-leptons` and an S04 data-period example in `source-policy` (untested). Results in `tests/grading/round9.md`, `round9_answers/`, `round9_grades/`.
- **Evidence:**
  - Supplemental Material text of S41-S47 read (C51-C58).
  - C36-C42 re-checked against the abstracts (C39, C41, C42 corrected).
  - S05 inconsistency decided: full text, main article only.
  - S07 and S11 read at main-article level (C59-C62).
  - S01 introduction and chapter 17 read (C103-C104, 2026-10-01).
  - S01 chapters 1-16 read (C63-C100). Their numbers were checked against rendered PDF pages on 2026-09-21; C75, C79, C80 and C85 are conventions with no fit values.
- **Small defects fixed:** claim topic index in `source-index`, short-answer rule in `SKILL.md`, current-date note in `source-policy`, ECAL claim C50.
