# ams-analysis: open work for the next session

State: branch `ams-analysis-executable-checks`; all required work from the task brief is done and validated (`python3 scripts/validate_skill_bundle.py` OK with 38 files; `python3 -m unittest discover -s tests` 238 tests OK; `python3 scripts/render_source_index.py` in sync). Read `VALIDATION.md` first: it records what was run, what was self-graded versus independently graded, and every known gap. Do not repeat finished work; do not claim a check passed without running it.

Ground rules that still apply: standard library only for scripts; every AMS-specific number needs a scoped claim in `data/claims.json` (edit the JSON, run `scripts/validate_evidence_ledger.py`, then `scripts/render_source_index.py --write`); never promote a claim's `verification_strength` without reading the source at that level; label statements [Documented] / [General method] / [Proposal] / [Unknown/needs input].

## Done since the first TODO (do not redo)

- Supplemental Material text of S43, S45, S46 read; claims C51-C53 added (collection time and cutoff, wavelet red-noise significance, hysteresis procedure). No covariance model across days and no trial-factor correction appear in the text read.
- C36-C42 re-checked against the paper abstracts; C39 (energy, 1-50 GeV), C41, C42 corrected.
- Small defects: claim topic index in `source-index`, short-answer rule in `SKILL.md`, current-date note in `source-policy`, ECAL claim C50.
- Independent grading (Opus grader, nine prompts) done: 7 pass, 2 fail (T29 blocking, T24); narrow fixes made; T29, T24 re-run and fixed, T08 partly fixed. Details in `VALIDATION.md`.
- Branch pushed to GitHub; a PR was opened (see the PR list); do not merge without the owner's decision.

## 1. Behavioral follow-up (highest value)

- [ ] Independent grading covers only nine prompts (T05, T08, T24, T29-T34; T05, T08, T24, T29, T32 twice); the other 25 tests were self-graded, and the independent grader was stricter than the self-grades. Round 2 passed all five re-graded prompts but exactly at the 90% bar with source discipline at 1. Regenerate answers to files, grade with a different model that holds the rubric, verify every quoted claim ID against `data/claims.json`, and use more than one sample per prompt.
- [ ] Take more than one sample per prompt for the prompts that failed or were borderline (T05, T08, T24, T29, T32, T33).
- [ ] The dominant failure pattern (still present at the round-2 pass) is claim-ID precision and scope: a correct fact with the wrong or over-broad claim, or a claim widened to sibling papers. The grouped bracket citations in `antimatter-and-leptons` and `charged-cosmic-rays` were split per paper as a root-cause fix; check whether other references (`nuclei-and-isotopes`, `detector-and-observables`, `inference-and-unfolding`) group citations the same way. Also check that `antimatter-and-leptons` does not imply there is no AMS antihelium paper at all (S22 is the AMS-01 limit; C14 is the governing claim).
- [ ] T33 missed the publication-date versus data-taking-period distinction; T30 covered only the inefficiency reading of a 0.85 column sum (the out-of-range feed-in reading is also legitimate); check whether `inference-and-unfolding` states the second reading clearly.
- [ ] T23 (ACC) was over-long once; re-check after the short-answer rule.

## 2. Close the remaining evidence gaps

- [ ] Supplemental Material text of S41, S42, S44 and S47, and the supplemental data tables of all of them (not read).
- [ ] Phys. Rept. review (S01), S02, S03, S07, S11, S16, S20 (metadata-only or abstract-only rows): upgrade `verification_level` only after reading.
- [ ] Decide the S05 inconsistency noted in `VALIDATION.md` (old bullet said metadata-only, table said full-text).
- [ ] Have a human physicist review the ledger judgement calls listed in `VALIDATION.md` (claim strengths, `support_kind`, `numeric_quotation_allowed`, tier ranges, supersession S02/S03).

## 3. Optional, only if a routed decision needs it

- [ ] Network refresh of the ledger: may only propose metadata changes from INSPIRE or DOI records and must never promote a claim to full-text or rewrite scientific claims without review.
- [ ] Remaining statistical-validation items listed as not implemented in `references/statistical-diagnostics.md` (Feldman-Cousins or CLs with toys, profile-likelihood boundary behavior, finite-template effects, unfolding scans, correlated ratio toys). Keep each small, seeded and labeled as an approximation.
- [ ] A YAML-subset reader for specifications, only if users actually write YAML.
