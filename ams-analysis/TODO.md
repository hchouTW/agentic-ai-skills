# ams-analysis: open work for the next session

State (verified 2026-10-01; rounds 5-7 merged via PR #20, #39, #40; round 8 and its two reference fixes uncommitted): `python3 scripts/validate_skill_bundle.py` OK with 38 files; `python3 -m unittest discover -s tests` 238 tests OK (ledger test counts fixed after PR #42: 49 sources, 102 claims); `python3 scripts/render_source_index.py` in sync. Latest behavioral result: **round 8 scored 92.8% (297/320), clean full-suite pass**. Earlier: round 6 scored **88.75% (284/320)** (`tests/grading/round6.md`; round 5 was 81.6%); round 7, a targeted rerun of the 7 weakest tests, scored 126/140 = 90.0% (`tests/grading/round7.md`), estimating the full suite at 90.0-91.25% (not a full-suite run). No blocking failure in either. Read `VALIDATION.md` first: it records what was run, what was self-graded versus independently graded, and every known gap. Do not repeat finished work; do not claim a check passed without running it.

Ground rules: standard library only for scripts; every AMS-specific number needs a scoped claim in `data/claims.json` (edit the JSON, run `scripts/validate_evidence_ledger.py`, then `scripts/render_source_index.py --write`); never promote a claim's `verification_strength` or a source's `verification_level` without reading the source at that level; label statements [Documented] / [General method] / [Proposal] / [Unknown/needs input]. For grading, answerers and grader must be different models.

## 1. Behavioral suite (round 8 passed; optional polish)

- [x] Round 8 (2026-10-01): full 16-prompt, 2-sample suite scored **297/320 = 92.8%**, no blocking failure; the 90% bar is cleanly met (`tests/grading/round8.md`). The T39 C80 and T41 C39/C89 fixes helped (T39 10, 9; T41 9, 9), not proven by single samples.
- [ ] Optional, all non-blocking source-discipline slips seen in round 8: T05 cutoff-scan claims (C20/C31 vs C23/C27/C49/C60) for the second round running; T32 citing proton/helium claims C36/C37 for lepton periodicity; T40 sample sizes and C75 scope; T33 verification level and data-taking period for alternatives. Fix only if a narrow reference change is clearly indicated; the next full run is not required.

## 2. Evidence gaps

- [ ] S02 and S03: APS returned 401 on 2026-09-21. They are not open access and have no arXiv version. They stay at abstract-level (S02) and metadata-only (S03) unless a human supplies the PDFs.
- [ ] S16 and S20 (grouped rows, still `metadata-only`): their individual papers are already split out as S41-S47 and read at main-article level. Decide whether to mark these rows as grouped pointers to S41-S47 or leave them as they are. Do not upgrade `verification_level` without reading.
- [ ] Supplemental Material data tables (S41-S47) are not transcribed or checked. Only the supplement text was read (C51-C58). Correlation across days/rotations and trial-factor correction remain undocumented in what was read. Keep them marked unknown.
- [ ] S01 (Phys. Rept. review): the introduction (section 0) and summary (chapter 17) are unread. They carry no additional measurements, so this is low priority. Figure-only values (resolution curves, rejection curves, cross sections, limits) stay untranscribed by design.

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
- [ ] Remaining statistical-validation items listed as not implemented in `references/statistical-diagnostics.md`: Feldman-Cousins or CLs with toys, profile-likelihood boundary behavior, finite-template effects, unfolding scans, correlated ratio toys. Keep each small, seeded and labeled as an approximation.
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
- **Round 8** (2026-10-01): full rerun after two narrow fixes (C80 wording in `nuclei-and-isotopes`, S42/C39 sentence in `time-dependent-analysis`). 297/320 = 92.8%, no blocking failure. Results in `tests/grading/round8.md`, `round8_answers/`, `round8_grades/`.
- **Evidence:**
  - Supplemental Material text of S41-S47 read (C51-C58).
  - C36-C42 re-checked against the abstracts (C39, C41, C42 corrected).
  - S05 inconsistency decided: full text, main article only.
  - S07 and S11 read at main-article level (C59-C62).
  - S01 chapters 1-16 read (C63-C100). Their numbers were checked against rendered PDF pages on 2026-09-21; C75, C79, C80 and C85 are conventions with no fit values.
- **Small defects fixed:** claim topic index in `source-index`, short-answer rule in `SKILL.md`, current-date note in `source-policy`, ECAL claim C50.
