# TODO for future Claude sessions (task-authoring)

State (2026-10-02): everything below is on branch `task-authoring-behavior-eval`, open as PR #107 against `main` (not merged; `main` was last verified 2026-10-01). `python3 scripts/validate_skill_bundle.py` OK (30 files, 12-section template contract); `python3 -m unittest discover -s tests` 101 tests OK. Round 3 to 3e in `VALIDATION.md` (latest, 2026-10-02) ran the first behavior eval (12 prompts, Haiku and Sonnet, baseline vs skill, blind scorer: skill 56/98 and 93/98 bullets passed vs 20 and 50 for baseline; the scorer was not blind in practice, so the gap is overstated), added three `SKILL.md` rules from the failures, rewrote the stale examples, added three examples and a generated-task linter. Not yet tested on a fresh model: Opus, the canonical-example and archetype jobs, and the three new example tasks (nobody implemented them). Read `VALIDATION.md` first (Round 3e), then this file.

Working rules:
- Work on a branch and ask before pushing or merging.
- Run the tests and the validator before committing.
- Keep `SKILL.md`, `README.md`, `scripts/validate_skill_bundle.py` `REQUIRED_PATHS` and `agents/openai.yaml` in sync.
- The template's 12-section contract (`REQUIRED_TEMPLATE_SECTIONS`) is exact. Do not add or remove a section without saying so, and update the validator, the tests and all of `examples/` together.
- Record every result, including negative ones, in `VALIDATION.md`.

Sibling tooling to reuse instead of hand-run subagents:
- Trigger tests: `../hep-analysis/tests/routing_eval.py --target task-authoring`. It runs an isolated `claude -p` with the 7 repo skills and grades routing to any owner.
- Behavior tests: this skill now has its own `tests/behavior_eval.py` (adapted from `../agile-development/tests/behavior_eval.py`; run / score / report, fixture repo per prompt, resume mode) and `tests/prompts.md` (T1-T12). Usage is in the script docstring. `../academic-papers/tests/run_prompts.py` is the other sibling harness. Lessons: keep `--max-turns` high (the first run's 12 left 9 Haiku runs empty); the blind scorer cannot be blind because the 12-section template gives the skill arm away; a scorer sometimes returns no JSON, so rescore with `--only`.
- Findings from the siblings: Haiku loads `SKILL.md` but rarely opens references, so must-do rules belong in `SKILL.md`. Compare at least 2 runs. A usage-limit notice comes back as an ordinary result, so check for it.
- Isolated routing data from 2026-09-26: task-authoring queries were routed correctly 4/4.
- The main checkout is shared with other Claude sessions that switch branches under you (on 2026-10-02 a task-authoring commit landed on another session's branch). Work in a worktree (`git worktree add .worktrees/<name> origin/main`) and check `git branch --show-current` before every commit.

## Decisions (2026-10-02)

- Archetype-example tooling: keep and test it (P2 item "Depending on the archetype decision" is now live).
- 12-section template: stays fixed.
- Next session, in this order: (1) get PR #107 reviewed and merged; (2) a human read of a few skill-arm tasks for invented facts, then add the canonical-example prompt(s) and a Haiku rerun after the destructive-change rule; (3) tests for the validator blind spots below; (4) the description trim with both trigger sets rerun; (5) Opus runs if wanted.

## Questions for the user

- [x] **The archetype-example tooling has no consumer in this repo any more.** Every skill's archetype `examples/` set was removed: academic-papers, agile-development and deep-learning in 0c5530f, hep-analysis in 86104f1. academic-diagrams keeps its own diagram examples and chose no archetype set. `references/example-authoring.md`, `generate_skill_example.py`, `validate_skill_example.py` and `check_example_diversity.py` (about 335 lines of reference plus 3 scripts and `tests/test_example_authoring.py`) now serve only external skills. Options: keep and test it on a scratch skill; slim it down; or remove it, which means updating the description, `SKILL.md`, `README.md`, `REQUIRED_PATHS` and the tests. The answer decides most of P2.
- [ ] (still open) Which task consumers matter most: Claude Code, Codex, or human engineers? The answer sets which adapters and which P1 prompts come first.
- [x] Should the 12-section template stay fixed, or gain an optional "Risks" or "Rollout" section? That would change the validator, the tests and every example.

## P1 - description and behavior

- [x] **Description length (2026-10-01):** 1274 to 1017 characters; the validator enforces 1024 (tests added). Still to do: the trigger sets below; the archetype decision may allow cutting further.
- [x] (12 prompts written 2026-10-02, T1-T12; canonical-example prompt not added, see below) Write 12-15 realistic prompts in `tests/prompts.md`, each with Must and Must-not lists (which reference is read, which rule fires). Cover:
  - a bare one-line feature request;
  - a bug report pasted verbatim;
  - a performance request with no baseline (baseline and target must be TBD, not invented);
  - a research request;
  - a repo that has its own task template (the repo's template wins);
  - a user-supplied format (the user's format wins);
  - a file or module that does not exist (must say "not found");
  - an inferable but unconfirmed detail (must be labelled Inferred);
  - an agentic retry loop (the iteration cap is TBD if not given);
  - a prompt-budget request;
  - "now implement it" (hand off to `agile-development`);
  - canonical-example requests, only if the archetype tooling stays.
- [x] (Haiku and Sonnet, 2 runs each, 2026-10-02; results in `VALIDATION.md` Round 3; Opus not run; three `SKILL.md` rules added; Sonnet rerun after the last rule 93/98) Run the prompts with and without the skill on Haiku and Sonnet, and on Opus if possible, with at least 2 runs each. Log the results in `VALIDATION.md` and fix `SKILL.md` where the skill did not help.
- [ ] (Partly done: one real fabrication found by reading, a raw path count is not usable; needs a manual read of more runs) Fabrication guard: over 5+ runs, count invented paths, thresholds, dataset versions, or "Confirmed" labels on things that are only inferred. Any hit is a skill bug; tighten the wording.
- [~] (linter built 2026-10-02, `scripts/lint_task.py`, `VALIDATION.md` Round 3e; the checklist items it cannot see, such as invented facts and measurable criteria, still need a reader) Check that generated tasks pass `references/task-quality-checklist.md` and the 12-section contract.
- [ ] Trigger sets (partly done 2026-10-01): `tests/trigger_queries.json` (tuning) and `tests/trigger_queries_holdout.json` now exist, smaller than planned (22 and 16 queries; the plan was 20 should-trigger and 20 should-not for tuning). Sonnet recall 22/24 tuning, 13/16 holdout; Haiku 0/24 and 0/16, the same with the old description (harness limit). 0 false triggers. Open: stack-trace-to-task queries load no skill on Sonnet, and prompt-design queries (token budget, ReAct loop) often go to `claude-api`; if that matters, name them in the description (1017 of 1024 characters used) and rerun both sets, then the sibling validators. The holdout is clean for one more change. Run the sets after any change to `SKILL.md`.

  Run each affected sibling's validator and tests after any description change. The boundary with `agile-development` was added to both descriptions in ea98f0d.

## P2 - shipped examples and tooling

- [x] **Stale example premises (done 2026-10-02, `VALIDATION.md` Round 3c).** The feature, bug and research examples were rewritten with premises verified today. The performance, CMS and AMS examples still carry their September snapshot notes; re-check them if the repository changes again.
- [x] `examples/README.md` count (six) and the `AI_Agent_Agnostic_Task_Authoring_Workflow.md` citation fixed (2026-10-01).
- [x] `check_template_sections` runs over every `examples/*-task.md` in a test (2026-10-01).
- [~] Archetype decision (keep and test): first pass done 2026-10-02 (generate 8, validate 8, fill 8 in a scratch skill, `METRIC_RE` fixed, see `VALIDATION.md` Round 3b). Still open below:
  - Done: generation and validation per archetype; validator misses recorded. Open: regression tests for fence-content checks, metric-inside-fence and the Red marker matching "error" in prose.
  - Open: the validator does not catch a wrong causal chain, assertions where executed output is required, an invented API in a diff, fabricated numeric inputs, pre-written outcomes, leading elicitation options, or any check on the role/stance words (list in `VALIDATION.md` Round 3b); decide which, if any, deserve a mechanical check.
  - Checked: the example-authoring pass made no cross-skill (agile-development) claims. `check_example_diversity.py` is documented as historical and is kept; running or removing it is still undecided.
- [x] (done 2026-10-02: no model names, prices or token math in the file; two dated bullets added, see Round 3c) Currency of `references/prompt-engineering-and-token-optimization.md`: token math, model names and tiers, pricing. Use the `claude-api` skill as the source, and date or remove anything time-sensitive.

## P3 - content and structure

- [x] (measured 2026-10-02, no change needed, see `VALIDATION.md` Round 3d) Progressive disclosure: `SKILL.md` was 166 lines and the references 761 lines plus 4 adapters when measured; both have grown slightly since. Measure the references read per run in P1. The skill covers three loosely related jobs (task docs, canonical examples, prompt design): check whether a plain "write a task" request over-loads references, and tighten the "When to Load References" bullets if it does.
- [x] (done 2026-10-02: migration, agentic loop, data/ML; not yet implemented by anyone) Add worked examples for categories with none: a refactor or migration task, a data/ML task, and an agentic-loop task (`loop-engineering.md` has no shipped example).
- [x] (validator error paths and exit codes, and the generated-task linter with tests, done 2026-10-02) Tests for uncovered behavior: the generated-task linter (if built); error paths of `validate_skill_bundle.py` (missing file, empty file, bad frontmatter); CLI exit codes.
- [~] (done 2026-10-02 except external URLs and Cursor/Copilot; see Round 3d) Multi-platform check (Codex, Antigravity, Cursor, Copilot): confirm `agents/openai.yaml` is current, that the install paths and invocation notes in `references/adapters/*.md` are still right, and that no instruction depends on Claude-only tools. Antigravity has format constraints; see the multi-platform memory.
- [~] (done 2026-10-02; three small fixes applied, the rest proposed in `VALIDATION.md` Round 3d: description trim with trigger-set rerun, job-routing block, collapse the 13-point instruction) Skill-reviewer pass on `SKILL.md` and `README.md` (`plugin-dev:skill-reviewer`).

## P4 - housekeeping

- [ ] Recurring: update the `VALIDATION.md` header date and counts (30 files, 101 tests) after each pass. Last done 2026-10-02; the `skill-router` removal and the example rewrite are logged there.
- [ ] Open from the Round 3d reviewer pass (model output, not yet decided): shorten the description and use the room for negative triggers; a three-line job-routing block and one imperative rule per non-task job in the Decision Rules; collapse the 13-point Generic Agent Instruction into outcome checks; trim the 14 example prompts in `SKILL.md`; move the maintainer note out of the Decision Rules; stop restating the archetype list and script flags in the README.
- `scripts/__pycache__` and `tests/__pycache__` are untracked and git-ignored. Nothing to do.
