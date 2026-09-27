# TODO for future Claude sessions (academic-papers)

State at 2026-09-27: P1 and P2 done on branch `academic-papers-todo-round1` (see the "TODO round 1" section of `VALIDATION.md`); P3 open, plus the P2 follow-ups below. Earlier state, 2026-09-21: skill is on `main`; `python3 -m unittest discover -s tests` and
`python3 scripts/validate_skill_bundle.py` pass. Verification so far is structural (bundle validator), plus
unit tests for the two helper scripts and hand-checked numbers in a few examples. Nothing has been checked by
running the skill on a fresh model, and none of the 41 references (~4,300 lines) or 24 examples has been audited
against primary sources. Read `VALIDATION.md` first, then this file.

Working rules: work on a branch, run `python3 -m unittest discover -s tests` and
`python3 scripts/validate_skill_bundle.py` before committing, keep `SKILL.md`, `README.md`,
`scripts/validate_skill_bundle.py` and `agents/openai.yaml` in sync, and ask before pushing or merging.
Record every result (including negative ones) in `VALIDATION.md`. Never invent citations, DOIs, or venue rules:
every hard fact added must have a source or be marked "not verified". The validator treats backtick-quoted
`references/...`/`scripts/...`/`assets/...` text as a claim that the path exists in this bundle; link (do not
backtick) paths that belong to other skills.

Environment facts found on 2026-09-21 (re-check, they may have changed):
- `tectonic` is in miniconda (`/Users/hchou/miniconda3/bin/tectonic`); `pdflatex`, `latexmk`, `bibtex`, `chktex`
  are NOT installed. Use Tectonic for compile checks (it fetches packages, so it needs network).
- Use a scratchpad for any generated `.tex`/`.bib`/PDF; do not write test artifacts into the skill folder.
- Network-dependent steps (INSPIRE-HEP, ADS, DBLP, arXiv, Crossref) may be unavailable or need an ADS token;
  say so in `VALIDATION.md` rather than skipping silently.

## P1 - close known verification gaps (things never actually run)
- [x] (2026-09-26: skeleton, REVTeX, JHEP and JCAP compile with Tectonic; JHEP3/jcappub.cls, showpacs, EPJC svjour3 corrected; conference styles not compiled) Compile `assets/templates/paper_skeleton.tex` with `assets/templates/references.bib` via Tectonic; confirm no
      undefined refs/citations. Then compile a minimal REVTeX 4.2, JHEP (`jheppub`), and NeurIPS/ICML skeleton
      to check the venue snippets in `references/latex-and-formatting.md` and `multi-venue-reformatting.md`
      (document class names, options, required packages, page/column limits). Fix or flag what fails.
- [x] (2026-09-26: synthetic edge cases + 16 arXiv sources incl. 3 theses vs Tectonic logs; 7 false-positive/negative classes fixed, 8 regression tests; found real duplicate .bib keys and a duplicated figure label in published theses) Run `scripts/check_manuscript.py` on realistic inputs, not only the unit-test fixtures: a compiled multi-file
      paper (`\input`/`\include`), one with `\cite` variants (`\citep`, `\citet`, `\cite[p.~3]{}`), a `.bib` with
      duplicate/odd keys, and a ~30-page thesis chapter. Record false positives/negatives; add regression tests.
- [x] (2026-09-26: 18-paper CSV renders correctly; BOM, short-row crash, extra cells, empty/non-UTF-8, semicolon and header-pipe cases fixed; 6 tests) Run `scripts/build_lit_matrix.py` on a real 15-20 paper reading-notes CSV (quoted commas, unicode, empty
      cells); check the output renders as valid markdown. Add tests for malformed CSV.
- [x] (2026-09-26: physics venues first as the user chose; every checked row dated with its source in `references/latex-and-formatting.md`; Elsevier, A&A, JMLR, AAAI, statistics journals marked "Not checked") Verify every numeric or rule claim in the venue quick-reference (`SKILL.md` "Journal / venue conventions"
      and the venue references): page/word limits, abstract lengths, reference styles, double-blind and
      supplementary rules for PRL/PRD, JHEP, JCAP, ApJ/AASTeX, EPJC, NeurIPS, ICML, ICLR, ACL, JMLR/TMLR.
      Check each against the venue's current author guide and cite the URL and date in the reference. Venue rules
      change yearly: mark year-specific values with the year.
- [x] (2026-09-26: INSPIRE, arXiv, ACL Anthology, Crossref queried live; INSPIRE collaboration keys and arXiv latest-version year corrected; DBLP and Semantic Scholar blocked, marked not verified) Verify database and tool claims in `references/citations-and-bibliography.md`,
      `literature-discovery-and-search.md`, `citation-verification.md`: INSPIRE-HEP/ADS/DBLP/Crossref API
      endpoints, cite-key conventions, query syntax. Actually run a few queries (INSPIRE REST, Crossref) and
      confirm the documented syntax works.
- [x] (obsolete 2026-09-26: `examples/` was removed 2026-09-25; the user chose to drop the example items) Re-derive the numbers in the examples that carry calculations (`01` look-elsewhere, `16` significance
      derivation, `21` word-count, others with code blocks). Extract and run each code block; confirm the
      stated values. Run `agile-development`'s `scripts/validate_skill_example.py` on all 24 examples.
- [x] (2026-09-26: guidance was correct but unsourced; 9 primary sources added, each confirmed in INSPIRE/Crossref; 3σ/5σ p-values computed; Li & Ma was not in the skill, pointer added) Audit statistics guidance against primary sources (`statistical-inference-for-physics.md`,
      `astroparticle-and-cosmic-ray-papers.md`: 5σ convention, look-elsewhere, Li & Ma, CLs, Feldman-Cousins,
      Wilks conditions). Every non-obvious formula or convention needs a source or should be softened.

## P2 - test that the skill actually changes model behavior
The workflows and modes are unproven until a fresh model is run on them.
- [x] (2026-09-26: 15 prompts, physics-weighted, Must/Must-not per prompt; runner `tests/run_prompts.py`) Write 12-15 realistic prompts in `tests/prompts.md`, each with expected behaviors (which reference is read,
      which mode fires, what must NOT happen). Cover: summarize+critique a real arXiv paper the user pastes;
      interpret a figure with a suspicious axis; lit review from 6 abstracts (must not fabricate extra papers);
      verify a citation supports a numeric claim; referee-response draft with a hostile comment; abstract
      rewrite from results; REVTeX-to-JHEP reformat; cleaning a messy `.bib` with duplicate INSPIRE keys;
      erratum vs Comment/Reply triage; reproducibility audit of a repo; reverse-engineer research code into a
      methodology write-up; ask to "add references that support my claim" (must refuse to invent; must verify);
      hand-off case where the user really needs the fit run (should route to `hep-analysis`); an unrelated
      "paper" question (paper-craft, printer paper) that must not trigger.
- [x] (2026-09-27: fresh `claude -p` sessions, blind Opus grader. Sonnet skill 27/3/0 vs baseline 25/4/1; Haiku skill 16/10/4 after moving the hard rules to the top of SKILL.md, vs baseline 7/13/10; see VALIDATION.md) Run each prompt in a fresh subagent with and without the skill; compare against expectations; log
      pass/fail and the fixes it produced in `VALIDATION.md`. Repeat a subset with Haiku and Opus.
      (Same method as `academic-diagrams/VALIDATION.md`.)
- [x] (2026-09-27: A13 recent papers with DOIs and A14 NeurIPS limit; both models pass A13 in both arms; A12 unverified BibTeX fixed by the top-level rules) Hallucination stress test: ask for "5 recent papers on X with DOIs" and "the exact NeurIPS page limit" with no
      tools. The skill must say what it cannot verify and give a lookup route, never a made-up DOI.
- [x] (2026-09-27: `tests/trigger_queries.json` + held-out set; description rewritten under 1,024 characters; Haiku recall 0/40 -> 25/40, held-out 20/28; Sonnet 27/40 -> 34/40, held-out 23/28; 0 false triggers) Trigger test for the frontmatter `description`: 20 should-trigger and 20 should-not-trigger queries,
      including near-misses (`academic-diagrams` figure requests, `hep-analysis` fit questions, `deep-learning`
      ablation design, `task-authoring`, generic "write an essay"). Consider `skill-creator` description
      optimization; keep the description under its length limit.
- [x] (2026-09-27: isolated 7-skill harness; no academic-papers false triggers on sibling-owned queries; all bundle validators and tests pass after the description change) Routing hygiene with `academic-diagrams` (structural diagrams vs data plots),
      `hep-analysis`, `ams-analysis`, `deep-learning`: run each affected skill's validator and tests after any
      description change.
- [x] (2026-09-27: fixed by the description rewrite; see the trigger item above) Under-triggering found by the isolated routing eval (2026-09-26, `hep-analysis/tests/routing_eval.py` on `hep-analysis/tests/trigger_queries_holdout.json`, all 7 repo skills loaded as project skills, 2 runs per query; "none" = the model answered without invoking any skill): "Build my BibTeX from INSPIRE for these ten arXiv IDs and fix duplicate
      keys" 0/2 Haiku, 0/2 Sonnet (none every time); "Critique the statistical treatment in this CMS paper's abstract
      and conclusions" 0/2 Haiku, 1/2 Sonnet; "Help me restructure the introduction of my thesis chapter on cosmic-ray
      antiprotons" 0/2 Haiku, 2/2 Sonnet. The description names BibTeX/INSPIRE and critique explicitly, so the
      phrasing is not the gap; check whether the long description buries them. Rerun with the harness after any
      description change (it grades routing to any `owner`, not only hep-analysis).
- [x] (obsolete 2026-09-26: `examples/` removed) Check the 24 examples follow their archetype rules (see the `task-authoring` skill's
      `references/example-authoring.md`) and that any weak-vs-expert contrast is realistic, not a strawman.

## P2 follow-ups found 2026-09-27
- [ ] A05 (hostile referee reply) is still 1 PASS / 2 FAIL on Haiku with the skill: it defends the criticized choice and adds comparisons the user never gave. Rule 6 in SKILL.md covers this; try a short worked reply in `references/submission-and-peer-review.md` and rerun A05 x3.
- [ ] A15 (CLs hand-off) is PARTIAL on both models: the limit is no longer reported as final, but the method and background-uncertainty treatment are not always stated.
- [ ] Rerun `tests/run_prompts.py` (Haiku, skill arm, 2 runs) and the trigger sets after any SKILL.md change; use run-to-run comparisons with at least 2 runs, since Haiku varies by several verdicts between identical runs.

## P3 - improve content and structure
- [ ] Progressive disclosure: `SKILL.md` is 416 lines and 41 references total ~4,300 lines. Confirm a typical task
      reads at most 2-3 references; trim `SKILL.md` toward a routing table, add "read only if" hints to vague
      rows, and check for overlapping references (e.g. `citation-verification` vs `claim-evidence-mapping`,
      `reproducibility-auditing` vs `manuscript-consistency-auditing`, `latex-and-formatting` vs
      `latex-mechanics-and-tooling` vs `multi-venue-reformatting`).
- [ ] Coverage gaps to consider (confirm each is really missing before adding): collaboration-paper workflow
      (internal review, publication committee, authorlist/ collaboration policy), arXiv submission mechanics
      (source bundle, ancillary files, licence, categories), data-availability and code-availability
      statements per venue, AI-use disclosure policies, response to a desk rejection or editor query, journal
      transfer/cascade, proceedings vs full paper, non-native-English polishing without changing claims.
- [x] (dropped 2026-09-26 by the user's choice, with `examples/` removed; if a topic needs a model answer, add a short verified walkthrough inside its reference) Add worked examples for topics with none today; check which of the 41 references have no example, and
      cover at least: reading a paper and extracting a claim ledger, a figure interpretation, `.bib` cleanup,
      venue reformatting, code-to-methodology synthesis, arXiv submission.
- [ ] Add a small end-to-end sample under `assets/` or `examples/` (paper skeleton + `.bib` + notes CSV) that runs
      `check_manuscript.py` and `build_lit_matrix.py` in sequence and serves as a smoke test.
- [ ] Extend `check_manuscript.py` only for checks that are mechanical and low-false-positive (unused bib
      entries, undefined refs, duplicate labels, unit spacing, `\ref` without `~`); ask before adding heuristics.
- [ ] Multi-platform check (Codex, Antigravity): confirm `agents/openai.yaml` is current and no instructions
      depend on Claude-only tools. See the repo's multi-platform conventions (memory: multi-platform skills target).
- [ ] Skill-doctor / skill-reviewer pass on `SKILL.md` and `README.md` (`plugin-dev:skill-reviewer`).

## P4 - housekeeping and decisions
- [x] (2026-09-26: already git-ignored; nothing to do) Remove stray `scripts/__pycache__` and `tests/__pycache__` from the working tree if untracked and not ignored.
- [ ] Update the `VALIDATION.md` header date and counts (file count, test count) after each pass. (Recurring; last done 2026-09-27, round 1.)
- [x] Asked 2026-09-26: physics (HEP/astroparticle journals) first, then ML venues. Ask the user: which venues and fields matter most (HEP/astroparticle journals vs ML conferences)? This sets
      which venue rules to verify first in P1 and which prompts to weight in P2.
- [x] Asked 2026-09-26: yes; implemented as the sources/last-verified table in `references/latex-and-formatting.md`, re-check rows older than a year. Ask the user whether a "venue rules last verified" policy is wanted (date stamp per venue row, re-check
      yearly).
