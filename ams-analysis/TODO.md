# ams-analysis: open work for the next session

**State (verified 2026-10-02 on `main`, everything merged up to PR #118; this renewal is a separate PR).** `python3 scripts/validate_skill_bundle.py` OK with 53 files; `python3 -m unittest discover -s tests` 462 tests OK; `python3 scripts/validate_evidence_ledger.py` pass with **60 sources and 183 claims** (the ledger test pins these counts); `python3 scripts/render_source_index.py` in sync; `python3 scripts/fetch_papers.py status`: 41 papers cached, 8 missing, 1 blocked. Read `VALIDATION.md` first: it records what was run, what was self-graded versus independently graded, and every known gap. Do not repeat finished work; do not claim a check passed without running it.

**Behavioral state.** Last full-suite run: round 18, T01-T61 x 2 samples, five Opus graders, **1181/1220 = 96.8%**, no blocking failure (`tests/grading/round18.md`). The suite now has T01-T66 (T62-T66 were added after that run). Later rounds were targeted subsets and are not full-suite scores: round 19 (T48, T49, T59, T60) 73.5/80, round 20 (T48) 8.75/10, round 21 (new T62-T66) 95.0/100, round 22 (T64) 9.25/10; no blocking failure in any round 3-22. **Not behaviorally evaluated:** the T48-related reference change in `cosmic-ray-databases` step 2 (levels 0, C127), the YAML reader, the fetch tool and the CRDB helper (code with unit tests only). Rubrics were written by the same session that added or edited the claims, so margins over the 90% bar are optimistic; grading used one grader per block.

**Ground rules.** Standard library only for scripts; every AMS-specific number needs a scoped claim in `data/claims.json` (edit the JSON, run `scripts/validate_evidence_ledger.py`, then `scripts/render_source_index.py --write`); never promote a claim's `verification_strength` or a source's `verification_level` without reading the source at that level; label statements [Documented] / [General method] / [Proposal] / [Unknown/needs input]; read numbers off rendered pages, not only pdftotext (it garbles signs and exponents); a drafted claim set gets a separate verifier before it enters the ledger. For grading, answerers and grader must be different models.

Everything in section 1 needs either a person (a physicist, a manual download, a browser) or a decision. Section 2 can be done alone.

## 1. Open: needs a person

- [ ] **Physicist review of the ledger** (`REVIEWER_PACKET.md`). Parts 1-3 are a snapshot of 49 sources and 106 claims; five addenda at the end cover S02/S03 (C107-C119), S09 (C120-C124), the databases (S50-S53, C125-C130), the nuclei and supplement work (S54-S60, C131-C182, with four questions for the reviewer) and the SSDC search page (S52, C183). C164 was amended after the packet (definition of N_i and aleph_i). A claim table with a verdict column is the return format. Still open until a physicist returns verdicts. Extend the addenda if the ledger changes again.
- [x] **S52, the ASI SSDC cosmic-ray database page.** Done 2026-10-02: the maintainer supplied a screenshot of the rendered search form; S52 is now `page` level with claim C183 (introduction text, search selectors, "All selected (25)", "Version 3.3", the time-dependent AMS data button), checked by a separate verifier (PASS). Only the form was seen: no query was run, so the 25 experiments, AMS-02 holdings and periods, output formats and terms are still unknown. To go further, run a query in a browser (for example particle = proton, experiment = AMS-02) and paste the result table header and the experiments list; an SSDC helper script still does not exist.
- [ ] **Papers with no scripted route** (download, then `python3 scripts/fetch_papers.py adopt FILE`): the Phys. Rept. 894 review (blocked; its introduction and summary were already read from another copy, C103-C104) and 8 papers: the 2002 AMS-01 Phys. Rept. (S23), the 2005 IEEE hardware paper, the 2010 Adv. Space Res. ECAL test beam, the 2013 CERN Courier piece, NIM A 970, 163657, the 2022 Moscow Univ. Bull. review, NIM A 1055, 168434 and NIM A 1086, 171364. Reading them is a separate step (own source record, scoped claims, a verifier).
- [ ] **CRDB values.** The helper `scripts/crdb_query.py` exists (PR #88) and one test query was run, but no CRDB value has been compared with an AMS paper and the CRDB release number must be recorded by hand from the website (the export header does not carry it). Do this when a real cross-check is needed.

## 2. Open: can do alone, optional

Nothing here is blocking; each item is small and single-sample. Pattern for any new round: add tests to `references/tests-and-examples.md`, fresh Sonnet answerers (one prompt each, no web, told not to read the tests or this file), one separate Opus grader, a `tests/grading/roundN.md` record.

- [ ] Re-test the `cosmic-ray-databases` step 2 wording (T48: both samples of rounds 19 and 20 omitted why combo and conversion levels are 0, C127/C128); one targeted T48 run is enough.
- [ ] Small attribution slips seen in single samples and left alone: T15_B (C23 over-generalised), T49_B and T60 propagation glosses, T59_B subtracting two printed upper bounds, T62_A "dominated by background and selection", T64_A "not double counted", T66_A unlabeled solar-rotation remark.
- [ ] Claims not yet cited by any test (about 80 by a rough count, mostly S01 detector description, S43-S47 daily-flux procedure and S59-S60 details): add tests only where a hallucination risk exists (a status, a null result, a method scope), as T62-T66 did.
- [ ] Unread parts, by design or by choice: the Supplemental Material of the seven nuclei PRLs (S54-S60; one file each, e.g. `SM-N-REV.pdf`); the complete tables and supplements of S02/S03; Tables S1-S140 and Figs. S1-S9 of S09; the plotted values of every supplement; the figure-only values of S01 (resolution and rejection curves, cross sections, limits). Transcribing table values would be unscoped numbers and is declined by design.
- [ ] Routing recheck only after a description change here or in `hep-analysis` (none since 2026-09-26; the 2026-10-01 recheck routed all AMS queries here for both Sonnet and Haiku, 10/10 runs each; the one false trigger, "boron-to-carbon with a space magnetic spectrometer", lists `ams-analysis` as acceptable). Command: `hep-analysis/tests/routing_eval.py --target ams-analysis` on `trigger_queries.json` and `trigger_queries_holdout.json`; ignore its own "recall" line (the files have no per-target flag).
- [ ] Statistical items not implemented, by design: varying weights inside a bin in the toy MC, a guaranteed-coverage construction for several nuisances, correlated gamma nuisances, Poisson-exact CV for the linear estimators, K-fold variants, learned or free-hyperparameter priors, spectrum-dependent efficiency uncertainties. The reference text for the statistical scripts has had no behavioral evaluation beyond T42-T45 (76/80 in round 9).
- [ ] Known single-sample slips left alone as minor: T08 C74, T24_B, T35_A, T36_B, T38_A, T29_A, T31_B (round 8); T32_B polarity reversed, T44_B C23 applied to S06 (round 9); T40_A "dominated by" systematics, T40_B 56-61% last-bin error stretched from C95, T33_B S05 level (round 11); T50_B no "empirical" statement (round 13).

## 3. Done (do not redo; details in `VALIDATION.md`, `tests/grading/` and `git log`)

**Behavioral rounds (answerers Sonnet, grader Opus, never the same model):**

| Round | Date | Scope | Score | Notes |
|---|---|---|---|---|
| 3-4 | 2026-09-21 | T05, T08, T24, T29, T32, T33, then second samples | 94.8%, 95.0% | one sample per prompt; answers not archived |
| 5 | 2026-09-25 | full 16 prompts x 2 | 81.6% | tests T35-T41 added for S01 claims C63-C100 |
| 6 | 2026-10-01 | full 16 x 2 | 88.75% | PR #39 |
| 7 | 2026-10-01 | 7 tests below 9, x 2 | 90.0% | PR #40, no reference changed |
| 8 | 2026-10-01 | full 16 x 2 | **92.8%** | PR #43, first clean pass |
| 9 | 2026-10-01 | T05, T32, T33, T40 + new T42-T45 | 92.5% | PR #47 |
| 10 | 2026-10-01 | T33, T40, T45 | 91.7% | PR #56 |
| 11 | 2026-10-02 | T33, T40 | 92.5% | PR #72 |
| 12 | 2026-10-02 | T33 + new T46-T48 | 91.25% | PR #83 |
| 13 | 2026-10-02 | T46, T48 + new T49-T52 | 97.5% | PR #87; round 12 fixes held |
| 14-17 | 2026-10-02 | new T53-T61 and reruns of T58/T60 | 95.0%, 89.4%, 91.3%, 93.8% | He/C/O attribution nudge in `nuclei-and-isotopes`; no blocking failure |
| 18 | 2026-10-02 | full T01-T61 x 2, five graders | **96.8%** (1181/1220) | replaces the round 8 full-suite number |
| 19 | 2026-10-02 | T48, T49, T59, T60 | 91.9% | PR #114 (round 18 rubric pass, T29 verification-level note) |
| 20 | 2026-10-02 | T48 | 8.75/10 | PR #115 (S52 page, C183) |
| 21 | 2026-10-02 | new T62-T66 | 95.0% | PR #116 |
| 22 | 2026-10-02 | T64 | 9.25/10 | PR #117 (C164 definition), PR #118 |

**Evidence (ledger 60 sources, 183 claims):**
- S01 (Phys. Rept. review): introduction, summary and chapters 1-17 read (C63-C104); numbers of C63-C100 checked on rendered pages 2026-09-21.
- S02 and S03 main articles read (C03, C107-C119); S04-S08, S10-S15 main articles; S09 main article and supplement text (C07, C120-C124, C175-C180); S41-S47 main articles with supplement text or captions (C36-C42, C51-C58, C105-C106, C181-C182).
- Nuclei PRLs S54-S60 (Li/Be/B, N, Ne/Mg/Si, Fe, F, Na/Al, S/primary composition; C131-C174), drafted per paper and verified number by number on rendered pages by a separate model (caught a wrong fit range, a misread bin edge, and numbers quoted from earlier references). S16 and S20 stay grouped `metadata-only` navigation pointers.
- Databases: S50-S53 and C125-C130, C183 (CRDB website and papers, SSDC proceedings abstract; the SSDC page S52 at `page` level, C183, from a maintainer screenshot).
- INSPIRE refresh (2026-10-02): no new AMS paper since 2026-09-20 (newest PRL 136, 241002, S15); an erratum noted for S30; five truncated DOIs fixed.
- S05 decided as full text, main article only; S07 and S11 read at main-article level (C59-C62); C36-C42 re-checked against abstracts.

**Tooling:** deterministic checkers `ams_kinematics.py`, `validate_covariance.py`, `validate_response.py`, `audit_analysis_spec.py` (JSON and a strict YAML subset via `yaml_subset.py`), `validate_evidence_ledger.py`, `render_source_index.py`, `validate_skill_bundle.py`; statistical scripts `poisson_diagnostics.py`, `statistical_toys.py`, `likelihood_limits.py`, `unfolding_diagnostics.py`, `template_fit.py` (CLs, Feldman-Cousins, profile and Berger-Boos limits, Barlow-Beeston fits, unfolding scans, response covariance, ratio toys); `fetch_papers.py` with `data/papers_manifest.json` (50 AMS articles, local cache outside the repo, blocks never bypassed); `crdb_query.py` (one native-axis CRDB query, secondary labels, provenance sidecar).

**Fixes after graded rounds** (all small and narrow; none was a global rule): claim-ID grouping split per paper; S05 and S02/S03 supersession wording; publication date versus data period (T33); column-sum statement (T30); C80, C39/C89 and C77 absolute-error wording; per-alternative verification level, date and data period in `source-policy`; C110 in the 2013-2014 lepton paragraph; earlier-reference examples in `nuclei-and-isotopes`; CRDB dataset contents unknown until queried; per-row access dates in the `source-index` header.

**Setup:** the skill is soft-linked at `~/.claude/skills/ams-analysis`; PR #1 (executable checks, b74b022) merged; routing recheck 2026-10-01 (see section 2).
