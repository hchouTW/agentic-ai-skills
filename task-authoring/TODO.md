# TODO for future Claude sessions (task-authoring)

State (verified 2026-09-28 on `main`): `python3 scripts/validate_skill_bundle.py` OK (25 files, 12-section template contract); `python3 -m unittest discover -s tests` 78 tests OK. **No TODO item has been worked on yet.** Verification so far is structural (validators, link checks) plus one RED/GREEN fresh-subagent run for `loop-engineering.md`. Core task authoring, the 8 archetypes and the prompt-engineering reference have never been tested on a fresh model. Read `VALIDATION.md` first (it is still dated 2026-09-12), then this file.

Working rules:
- Work on a branch and ask before pushing or merging.
- Run the tests and the validator before committing.
- Keep `SKILL.md`, `README.md`, `scripts/validate_skill_bundle.py` `REQUIRED_PATHS` and `agents/openai.yaml` in sync.
- The template's 12-section contract (`REQUIRED_TEMPLATE_SECTIONS`) is exact. Do not add or remove a section without saying so, and update the validator, the tests and all of `examples/` together.
- Record every result, including negative ones, in `VALIDATION.md`.

Sibling tooling to reuse instead of hand-run subagents:
- Trigger tests: `../hep-analysis/tests/routing_eval.py --target task-authoring`. It runs an isolated `claude -p` with the 7 repo skills and grades routing to any owner.
- Behavior tests: `../academic-papers/tests/run_prompts.py` or `../agile-development/tests/behavior_eval.py` (with and without the skill, blind grader).
- Findings from the siblings: Haiku loads `SKILL.md` but rarely opens references, so must-do rules belong in `SKILL.md`. Compare at least 2 runs. A usage-limit notice comes back as an ordinary result, so check for it.
- Isolated routing data from 2026-09-26: task-authoring queries were routed correctly 4/4.

## Questions for the user (ask before P2)

- [ ] **The archetype-example tooling has no consumer in this repo any more.** Every skill's archetype `examples/` set was removed: academic-papers, agile-development and deep-learning in 0c5530f, hep-analysis in 86104f1. academic-diagrams keeps its own diagram examples and chose no archetype set. `references/example-authoring.md`, `generate_skill_example.py`, `validate_skill_example.py` and `check_example_diversity.py` (about 335 lines of reference plus 3 scripts and `tests/test_example_authoring.py`) now serve only external skills. Options: keep and test it on a scratch skill; slim it down; or remove it, which means updating the description, `SKILL.md`, `README.md`, `REQUIRED_PATHS` and the tests. The answer decides most of P2.
- [ ] Which task consumers matter most: Claude Code, Codex, or human engineers? The answer sets which adapters and which P1 prompts come first.
- [ ] Should the 12-section template stay fixed, or gain an optional "Risks" or "Rollout" section? That would change the validator, the tests and every example.

## P1 - description and behavior

- [ ] **The description is over the length limit:** 1274 characters, where the limit is 1024; the TODO's earlier "~1170" was wrong. `academic-diagrams` has the same problem at 1180. `scripts/validate_skill_bundle.py` does not check the length. Shorten the description first; how much depends on the archetype decision above. Add a length check with a test, then run the trigger sets below.
- [ ] Write 12-15 realistic prompts in `tests/prompts.md`, each with Must and Must-not lists (which reference is read, which rule fires). Cover:
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
- [ ] Run the prompts with and without the skill on Haiku and Sonnet, and on Opus if possible, with at least 2 runs each. Log the results in `VALIDATION.md` and fix `SKILL.md` where the skill did not help.
- [ ] Fabrication guard: over 5+ runs, count invented paths, thresholds, dataset versions, or "Confirmed" labels on things that are only inferred. Any hit is a skill bug; tighten the wording.
- [ ] Check that generated tasks pass `references/task-quality-checklist.md` and the 12-section contract. Consider a small linter for generated tasks: sections in order, non-empty Open Questions, every cited path exists.
- [ ] Trigger sets: `tests/trigger_queries.json` for tuning (20 should-trigger, 20 should-not) and a held-out set that is never tuned on. Near-misses to include:
  - ad-hoc scoping inside an active implementation chat (stays with `agile-development`);
  - "write a README";
  - "write a commit message";
  - a generic "write a prompt" with no LLM-call design;
  - drafting for `academic-papers`.

  Run each affected sibling's validator and tests after any description change. The boundary with `agile-development` was added to both descriptions in ea98f0d.

## P2 - shipped examples and tooling

- [ ] **Stale example premises.** The 6 `examples/*-task.md` files are all Task Markdown against this repo, and their Repository Context has drifted:
  - `research-task.md` investigates the duplication of `cpp-balanced-design-guidelines.md` across two skills. That duplication was resolved on 2026-09-15: only `agile-development` keeps it, and deep-learning links to it.
  - `bug-task.md` is about `academic-papers`' validator not checking `examples/`. That skill no longer has `examples/`.
  - `feature-task.md` says the validator is "duplicated five times". There are now 7 `validate_skill_bundle.py` files.
  - `ams-antiproton-analysis-task.md` proposes a `hep-analysis/examples/` entry, but that directory was removed.
  - Re-verify every path, count and "confirmed absent" claim in all six. Then fix, re-date or replace each example.
- [ ] `examples/README.md` says "Four worked Task Markdown outputs" but lists six. It still cites the unshipped `AI_Agent_Agnostic_Task_Authoring_Workflow.md` as a source; reword that as provenance, as was done for `performance-task.md`.
- [ ] `check_template_sections` passes on all 6 examples (checked by hand 2026-09-28), but no test runs it over `examples/`. Add one.
- [ ] Depending on the archetype decision:
  - Generate one example per archetype with `generate_skill_example.py` into a scratch skill.
  - Run `validate_skill_example.py` on each. Record where the output needed manual fixes and where the validator missed a real defect, and add regression tests.
  - Check for agile-specific assumptions in the cross-skill claim.
  - Run or remove `check_example_diversity.py`.
- [ ] Currency of `references/prompt-engineering-and-token-optimization.md`: token math, model names and tiers, pricing. Use the `claude-api` skill as the source, and date or remove anything time-sensitive.

## P3 - content and structure

- [ ] Progressive disclosure: `SKILL.md` is 166 lines and the references total 761 lines plus 4 adapters. Measure the references read per run in P1. The skill covers three loosely related jobs (task docs, canonical examples, prompt design): check whether a plain "write a task" request over-loads references, and tighten the "When to Load References" bullets if it does.
- [ ] Add worked examples for categories with none: a refactor or migration task, a data/ML task, and an agentic-loop task (`loop-engineering.md` has no shipped example).
- [ ] Tests for uncovered behavior: the generated-task linter (if built); error paths of `validate_skill_bundle.py` (missing file, empty file, bad frontmatter); CLI exit codes.
- [ ] Multi-platform check (Codex, Antigravity, Cursor, Copilot): confirm `agents/openai.yaml` is current, that the install paths and invocation notes in `references/adapters/*.md` are still right, and that no instruction depends on Claude-only tools. Antigravity has format constraints; see the multi-platform memory.
- [ ] Skill-reviewer pass on `SKILL.md` and `README.md` (`plugin-dev:skill-reviewer`).

## P4 - housekeeping

- [ ] Recurring: update the `VALIDATION.md` header date (still 2026-09-12) and the counts (25 files, 78 tests) after each pass. Also record the removal of `skill-router` (4e687d7) and the example rewrite (5953c63), which are not logged there.
- `scripts/__pycache__` and `tests/__pycache__` are untracked and git-ignored. Nothing to do.
