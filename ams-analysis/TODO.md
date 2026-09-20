# ams-analysis: open work for the next session

State when this file was written: branch `ams-analysis-executable-checks`, all required work from the task brief is done and validated (`python3 scripts/validate_skill_bundle.py` OK with 38 files; `python3 -m unittest discover -s tests` 238 tests OK; `python3 scripts/render_source_index.py` in sync). Read `VALIDATION.md` first: it records what was run, what was self-graded, and every known gap. Do not repeat finished work; do not claim a check passed without running it.

Ground rules that still apply: standard library only for scripts; every AMS-specific number needs a scoped claim in `data/claims.json` (edit the JSON, run `scripts/validate_evidence_ledger.py`, then `scripts/render_source_index.py --write`); never promote a claim's `verification_strength` without reading the source at that level; label statements [Documented] / [General method] / [Proposal] / [Unknown/needs input].

## 1. Merge the branch (needs the owner's decision)

- [ ] Open a PR from `ams-analysis-executable-checks` into `main` (or merge locally) and check that `skill-router` still validates (`cd ../skill-router && python3 scripts/validate_skill_bundle.py && python3 -m unittest discover -s tests`).

## 2. Independent behavioral grading (highest value)

All behavioral results in `VALIDATION.md` are self-graded: one sample per prompt, answerers were fresh sub-agents, but the grader was the author who knew the rubrics. An attempted independent grader (a different model holding the rubric, reading saved transcripts) failed on an API spend limit and produced no scores; the transcripts it needed were temporary and are gone, so the answers must be regenerated.

- [ ] Re-run T29-T34 (and ideally T05, T08, T24, T31) with fresh answerers that read only `SKILL.md` and the routed references (never `references/tests-and-examples.md`), saving each final answer to a file.
- [ ] Have a separate grader on a different model, holding the rubric, grade the saved answers, verify every quoted number and claim ID against `data/claims.json`, and report PASS/FAIL, per-dimension scores and defects. Record agreement or disagreement with the earlier self-grades in `VALIDATION.md`.
- [ ] Take more than one sample per prompt for the tests that failed or were partial once (T31 first run; T23 was over-long).
- [ ] Fix narrowly, in the responsible reference only; do not add global rules for one stylistic slip.

## 3. Close the evidence gaps

- [ ] Read the Supplemental Material of the time-structure papers (S41-S47) and add scoped claims for: how systematic errors are correlated across days or rotations; how the wavelet significance was calibrated; whether any trial-factor or look-elsewhere correction was applied; how the hysteresis significance was computed; how the daily collection time T is determined. Then update `references/time-dependent-analysis.md` (Evidence boundary and gap paragraph).
- [ ] Read the Phys. Rept. review (S01) and S02, S03, S07, S11, S16, S20 (metadata-only or abstract-only rows) if full text can be obtained; upgrade `verification_level` only after reading.
- [ ] The S05 inconsistency noted in `VALIDATION.md` (the old "Items lacking verification" bullet listed it as metadata-only while its table row says full-text) is still an open human decision.
- [ ] Have a human physicist review the ledger judgement calls listed in `VALIDATION.md` (claim strengths, `support_kind`, `numeric_quotation_allowed`, tier ranges, supersession S02/S03).
- [ ] Re-verify titles and numbers of C36-C42 (read as abstracts through a summarizing fetch tool before the full texts were read) against the papers.

## 4. Small known defects to fix (each seen once in a behavioral run)

- [ ] `tests-and-examples.md` T08 answer cited the antiproton template-fit practice to claim C26 (the electron claim); C22 is correct. Consider making claim IDs easier to find (for example a one-line topic index in `source-index`).
- [ ] T23 (ACC) answers run longer than the "short answer" rubric wants; check whether `SKILL.md`'s simple-question rule needs a sharper example.
- [ ] Answers sometimes call the verification date "today's date": consider one sentence in `source-policy` that the model cannot know the current date.
- [ ] Re-run T29 and T32 after the wording fixes made in `charged-cosmic-rays.md` and `time-dependent-analysis.md` (they were not re-run).

## 5. Optional, only if a routed decision needs it

- [ ] Network refresh of the ledger: it may only propose metadata changes from INSPIRE or DOI records and must never promote a claim to full-text or rewrite scientific claims without review.
- [ ] Remaining statistical-validation items listed as not implemented in `references/statistical-diagnostics.md` (Feldman-Cousins or CLs with toys, profile-likelihood boundary behavior, finite-template effects, unfolding closure/pull/prior/regularization scans, correlated ratio toys). Keep each small, seeded and labeled as an approximation; do not build a framework.
- [ ] Consider adding a small `--format yaml-subset` reader only if users actually write YAML specifications; today the specification is JSON only.
