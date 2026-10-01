# TODO for future Claude sessions (academic-papers)

State (verified 2026-10-01 on `main`, all work merged; round 1 via PR #25, Haiku follow-ups via PR #26, round 2 via PR #53): `python3 scripts/validate_skill_bundle.py` OK; `python3 -m unittest discover -s tests` 48 tests OK. P1-P4 are done. The skill has been run on fresh models (15 prompts, blind Opus grader):
- Sonnet skill arm: 15/15 PASS.
- Haiku skill arm: 21 PASS / 5 PARTIAL / 4 FAIL, vs a 7/13/10 baseline.

No behavioral item is open: A05 on Haiku was closed as a known limitation on 2026-10-01 (only the recurring checks below remain). `examples/` was removed on 2026-09-25, and the user chose to drop the example work. Read `VALIDATION.md` first (the "TODO round 1" and "Haiku follow-ups" sections), then this file.

Working rules:
- Work on a branch and ask before pushing or merging.
- Run `python3 -m unittest discover -s tests` and `python3 scripts/validate_skill_bundle.py` before committing.
- Keep `SKILL.md`, `README.md`, `scripts/validate_skill_bundle.py` and `agents/openai.yaml` in sync.
- Record every result, including negative ones, in `VALIDATION.md`.
- Never invent citations, DOIs or venue rules. Every hard fact added must have a source or be marked "not verified".
- The validator treats backtick-quoted `references/...`, `scripts/...` or `assets/...` text as a claim that the path exists in this bundle. Link paths that belong to other skills; do not backtick them.
- Hard rules live in "Rules for every task" at the top of `SKILL.md`, because Haiku rarely opens references. A prohibition diluted into a longer rule stops working: A02 regressed that way. Keep each ban as its own sentence.

User decisions (2026-09-26):
- Physics venues (HEP/astroparticle journals) come first, then ML venues.
- Every venue row carries a last-verified date: see the sources table in `references/latex-and-formatting.md`. Re-check rows older than a year.
- Example items are dropped. If a topic needs a model answer, add a short verified walkthrough inside its reference.

## Environment and tooling (re-check, they may have changed)

- `tectonic` (miniconda) is the only TeX engine; `pdflatex`, `latexmk`, `bibtex`, `biber` and `chktex` are not installed. Tectonic fetches packages, so it needs network access.
- DBLP (a bot-check page) and Semantic Scholar block scripted access. INSPIRE, arXiv, ACL Anthology and Crossref work. If a network step is unavailable, say so in `VALIDATION.md` rather than skipping it silently.
- Put generated `.tex`, `.bib` and PDF files in the scratchpad, never in the skill folder.
- Behavior runner: `tests/run_prompts.py` runs `tests/prompts.md` in fresh `claude -p` sessions with a blind Opus grader.
- Trigger runner: `../hep-analysis/tests/routing_eval.py --target academic-papers` with `tests/trigger_queries.json` (tuning) and `tests/trigger_queries_holdout.json`.
- The CLI returns a usage or spend-limit notice as an ordinary result. Check for USAGE_LIMIT/ERROR before trusting a run.
- Haiku varies by several verdicts between identical runs, so compare with at least 2 runs.

## Open

- [x] **A05 (hostile referee reply) on Haiku: closed as a known limitation (2026-10-01).** About 2 of 6 runs pass. Three `SKILL.md` rule-6 additions (no invented checks; no invented details; a worked reply) did no better than noise (12 runs for the worked reply: 3/3/6) and were reverted. Sonnet passes. Failures invent specifics, ask a question, or discuss strategy instead of drafting. Details in `VALIDATION.md`.
- [ ] **Recurring, after any `SKILL.md` change:** rerun `tests/run_prompts.py` (Haiku, skill arm, at least 2 runs) and both trigger sets. Last measured after the description rewrite (1,014 of 1,024 characters):
  - Haiku recall: 25/40, held-out 20/28.
  - Sonnet recall: 34/40, held-out 23/28.
  - 0 false triggers.
- [ ] **Recurring, after each pass:** update the `VALIDATION.md` header date and counts (60 files, 48 tests). Last done 2026-10-01, round 2.

Known residual gaps (only if a user need arises):
- NeurIPS, ICML, ICLR and ACL styles were not compiled. Only the skeleton, REVTeX, JHEP and JCAP were.
- Venue rules marked "Not checked": Elsevier/`elsarticle`, A&A, JMLR, AAAI, statistics journals.
- The DBLP and Semantic Scholar query syntax is not verified live.
- `SKILL.md` is about 470 lines because of the rules block. A trim was considered and not done, since skill runs read at most 3 references.

## Done (do not redo; details in `VALIDATION.md`)

**P1 - verification (2026-09-26)**
- Templates: the skeleton, REVTeX, JHEP and JCAP compile with Tectonic. JHEP3/`jcappub.cls`, `showpacs` and EPJC `svjour3` were corrected. EPJC uses `sn-jnl`; AASTeX is v7.
- `check_manuscript.py` was run on synthetic edge cases and 16 arXiv sources, including 3 theses. 7 false-positive or false-negative classes were fixed, with 8 regression tests.
- `build_lit_matrix.py` was run on an 18-paper CSV. The BOM, short-row, extra-cell, empty or non-UTF-8, semicolon and header-pipe cases were fixed, with 6 tests.
- Venue rules for physics venues are verified, each row dated and sourced in `references/latex-and-formatting.md`.
- INSPIRE, arXiv, ACL Anthology and Crossref were queried live. The INSPIRE collaboration keys and the arXiv latest-version year were corrected.
- Statistics guidance: 9 primary sources added, each confirmed in INSPIRE or Crossref. The 3σ and 5σ p-values were computed, and a Li & Ma pointer was added.

**P2 - behavior and triggering (2026-09-26/27)**
- `tests/prompts.md` holds 15 physics-weighted prompts with Must/Must-not lists, including hallucination stress tests A12-A14. `tests/run_prompts.py` uses a blind Opus grader.
- Sonnet: skill arm 27/3/0 vs baseline 25/4/1. After the follow-ups: 15/15.
- Haiku: 16/10/4 once the hard rules moved to the top of `SKILL.md` (baseline 7/13/10). After the follow-ups: 21/5/4.
  - Rule 2 now names the method and uncertainty treatment and bans estimating σ from a plot. This fixed A15 and A02.
  - Rule 6 got a reply shape.
- Description rewritten: Haiku trigger recall went from 0/40 to 25/40, and the isolated 7-skill harness under-triggering cases were fixed. There were no false triggers on sibling-owned queries, and all sibling validators and tests pass.

**P3 - content and structure (2026-09-27)**
- Progressive disclosure: skill runs read at most 3 references. The overlapping pairs state their scope and point to each other, so they were not merged.
- `references/submission-and-peer-review.md` gained: collaboration internal review, arXiv licence, ancillary files and replacements, desk rejection, editor queries, transfer offers.
- `tests/test_end_to_end.py` smoke test: skeleton + `.bib` through the checker, injected mistakes, lit-matrix output fed into the paper, and a Tectonic compile when available.
- `check_manuscript.py --style`: opt-in advisory checks for `\ref` without `~` and number-unit spacing. They never affect the exit code (user approved).
- Multi-platform check: no Claude-only tools; `agents/openai.yaml` is current.
- Skill-reviewer pass: 13 of 14 findings fixed.

**P4:** `__pycache__` is already git-ignored.
