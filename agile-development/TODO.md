# TODO for future Claude sessions (agile-development)

State at 2026-09-21: skill is on `main`; `python3 -m unittest discover -s tests` (41 tests) and
`python3 scripts/validate_skill_bundle.py` (48 files) pass. Existing verification (see `VALIDATION.md`) is structural:
helper-script unit tests, cross-link/consistency audits, and example-format checks. The workflow guidance in
`SKILL.md` and `references/` has never been run on a fresh model to see if it changes behavior. Read `VALIDATION.md`
("Limitations" at the end) first, then this file.

Working rules: work on a branch, run the tests and bundle validator before committing, keep `SKILL.md`, `README.md`,
`scripts/validate_skill_bundle.py` and `agents/openai.yaml` in sync, and ask before pushing or merging. Record every
result (including negative ones) in `VALIDATION.md`. Run fresh-model tests via subagents (baseline without the skill
vs. with the skill). Put temporary files in the scratchpad, not the repo.

Note: `tests/` and `scripts/` contain stale `__pycache__` .pyc files for modules that moved to `task-authoring`
(`test_example_authoring`, `generate_skill_example`, `validate_skill_example`, `check_example_diversity`). They are
git-ignored; do not treat them as live code.

## P1 - test that the skill changes model behavior (never done)
- [x] (2026-09-21: 15 prompts written in `tests/prompts.md`; the trigger-test query lists there still need writing out to 20+20) Write 12-15 realistic prompts in `tests/prompts.md`, each with expected behaviors and the reference it should
      load. Cover: (a) bug fix with a vague report (should reproduce first, smallest fix); (b) ambiguous feature
      request where a wrong guess is expensive (should ask); (c) ambiguous but cheap-to-reverse request (should state
      an assumption and proceed, not ask); (d) DB migration / published API change (risk section, rollback);
      (e) dependency bump; (f) "review my diff" / PR review; (g) production incident + postmortem; (h) legacy code
      with no tests (characterization tests); (i) "is this overcomplicated?" over-engineering check; (j) architecture
      decision / ADR; (k) estimation + spike; (l) feature-flagged rollout; (m) a trivial one-line fix (should NOT
      pad with the full template - Caveats rule); (n) user says "don't run tests" (user instruction wins);
      (o) new code file (must add the top-of-file Purpose/What/Usage comment block).
- [~] (2026-09-21: Sonnet, 30 runs, results in `VALIDATION.md`; 2026-09-21: clean baselines for 1-10 re-run, 8 pass / 2 partial; still open: Haiku and Opus spot-checks on H1/H5/H6 done (Haiku H5 iterated, round 3 wording untested); still open: run every cell 3x, have a second scorer, and repeat the harder prompts H1-H6 (added 2026-09-21, run once: 2 of 6 separate the skill)); the original 15 mostly do not discriminate) Run each prompt in a fresh subagent with and without the skill; score against the expectations; log pass/fail in
      `VALIDATION.md`. Repeat with Haiku (weaker) and Opus if possible. Look especially for: claiming tests passed
      without running them, scope creep, over-asking, skipping the honest report.
- [~] (2026-09-21: 20+20 queries written and run once, 40/40 correct on the agile-development criterion; caveats in `VALIDATION.md`; still open: run with real installed descriptions and a second scorer) Trigger test for the frontmatter `description`: 20 should-trigger and 20 should-not-trigger queries. Near-misses:
      `task-authoring` (write a standalone ticket/spec), `deep-learning`/`hep-analysis` (domain code), pure Q&A
      about a language feature, a one-line typo fix. Consider `skill-creator` description optimization.
- [ ] Routing hygiene with sibling skills: `agile-development` vs `task-authoring` (live scoping vs a written
      task document). Run `skill-router`'s validator and tests after any description change.

## P2 - close verification gaps in helpers and guidance
- [x] (2026-09-21: found and fixed BOM, closing-`##`, fenced-code, `Works!` and empty-field defects; 9 regression tests added, 41 tests total. Setext headings remain unsupported by design.) Test `scripts/create_story_card.py` and `scripts/validate_agile_notes.py` on messy input: empty strings, unicode,
      very long criteria, CRLF files, headings with trailing `#`, missing/duplicate sections. Add regression tests for
      each defect found. Check that generated cards pass the validator (round trip).
- [~] (2026-09-21: syntax checked; Python/Bash pass, C++ blocks are fragments, no defect found; guidance accuracy not reviewed; see `VALIDATION.md`) Review the three language design guides (`references/cpp-`, `python-`, `bash-balanced-design-guidelines.md`,
      ~3,000 lines together) for accuracy; `VALIDATION.md` says they were only kept as a single source of truth, not
      re-validated. Run every code snippet (`g++ -std=c++20 -fsyntax-only`, `python3 -m py_compile`,
      `bash -n` + `shellcheck` if installed) and fix or label the ones that fail.
- [x] (2026-09-21: validators pass on all 24; 25/27 Python blocks compile, 2 are REPL transcripts; not executed) Run the runnable snippets in `examples/01-24` and confirm each follows its archetype rules
      (`task-authoring/references/example-authoring.md`; use `task-authoring`'s example validators).
- [x] (2026-09-21: Sonnet, 3 tasks in a scratch repo, results verified by re-running; gaps fixed or logged in `VALIDATION.md`) Dogfood: apply the skill to a real small change in a scratch repo (feature + bug fix + migration), following only
      what `SKILL.md` says, and note where the instructions were unclear or missing.

## P3 - improve content and structure
- [~] (2026-09-21: load-only-when hints added for language guides; reads-per-task not measured on a model) Progressive disclosure: `SKILL.md` is 161 lines and references ~4,600. Confirm a typical task reads at most 2-3
      references; add "read only if" hints where a routing row is vague. Check that C++/Python/Bash guides are only
      loaded when code in that language is being designed.
- [x] (2026-09-21: cross-references added, content left in place) Look for overlap: `implementation-discipline.md` vs `validation-and-done.md` vs `risk-and-quality.md`
      (duplicate checklists?), and `software-architecture.md` vs `design-and-estimation.md`.
- [ ] Gaps to consider (only add if the P1 prompt tests show a need): performance work, flaky-test triage,
      security-fix handling, monorepo/multi-package changes, working with an existing CI failure, and
      pair-with-`superpowers` guidance (TDD, verification-before-completion) so instructions do not conflict.
- [x] (2026-09-21: no Claude-only tools; CLAUDE.md mention widened) Multi-platform check (Codex, Antigravity): confirm `agents/openai.yaml` is current and no instructions depend on
      Claude-only tools. See the repo's multi-platform conventions.
- [x] (2026-09-21: 9 findings, 4 applied, rest declined with reasons in `VALIDATION.md`) Skill-doctor / `plugin-dev:skill-reviewer` pass on `SKILL.md` and `README.md`.

## P4 - housekeeping and decisions
- [x] (2026-09-21: done; re-do after each pass) Update `VALIDATION.md` header date (still 2026-09-05) and counts after each pass; add a section for the
      2026-09-21 state.
- [x] (2026-09-21: Code File Requirement scoped in `SKILL.md`, re-run passes; step-verify folded into workflow step 3, format still unused on H4) New from the 2026-09-21 run (H6: the skill arm skipped the header on a typo fix and said so, so a carve-out would match its behavior; see `VALIDATION.md`): decide whether the Code File Requirement should be relaxed for one-line/docs/review tasks (it was applied to a label rename and a PR review).
- [ ] Ask the user: which languages/stacks matter most (this sets which design guide gets validated first)?
- [ ] Ask the user whether the "Code File Requirement" (top-of-file comment block on every changed file) is still
      wanted; it is the rule most likely to conflict with repository conventions.
