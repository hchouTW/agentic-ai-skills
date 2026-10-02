# TODO for future Claude sessions (task-authoring)

State (2026-10-02, branch `ta-incident-rule` (Round 3i hand read recorded) on top of `main` 20a9426; nothing pushed). Round 3j added the premise-as-fact rule (Haiku partial, Sonnet clean, 1 of 3 Haiku over-hedges on benign T14); Round 3h added the illustrative-incident rule: T13(e) now P/~/P on Haiku and 3 P on Sonnet (3 runs, skill arm, not blind): `python3 scripts/validate_skill_bundle.py` OK (30 files, 12-section template contract); `python3 -m unittest discover -s tests` 104 tests OK; description 1017 of 1024 characters. Latest behavior eval is Round 3g in `VALIDATION.md` (T1-T13, Haiku and Sonnet, baseline vs skill, 2 runs each, 108 bullet verdicts per cell): Haiku skill 67 P / 36 ~ / 5 F against baseline 18 / 25 / 65; Sonnet skill 99 / 9 / 0 against 57 / 23 / 28. The blind scorer named the arm in 102 of 104 runs (the 12-section template gives it away), so the gap is overstated. Not yet tested: Opus, and the three newest example tasks (migration, agentic-loop, data-ml) that nobody has implemented. Read `VALIDATION.md` (Round 3g, then 3e) first, then this file.

Working rules:
- Work on a branch in a worktree (`git worktree add .worktrees/<name> origin/main`); the main checkout is shared with other Claude sessions that switch branches under you. Check `git branch --show-current` before every commit. Ask before pushing or merging.
- Run the tests and the validator before committing.
- Keep `SKILL.md`, `README.md`, `scripts/validate_skill_bundle.py` `REQUIRED_PATHS` and `agents/openai.yaml` in sync.
- The template's 12-section contract (`REQUIRED_TEMPLATE_SECTIONS`) is exact. Do not add or remove a section without saying so, and update the validator, the tests and all of `examples/` together.
- Record every result, including negative ones, in `VALIDATION.md`.
- Haiku loads `SKILL.md` but rarely opens references, so a must-do rule belongs in `SKILL.md`. Pair every refusal or restriction rule with a benign prompt (a sibling's unscoped rule over-refused).

Tooling to reuse instead of hand-run subagents:
- Behavior eval: `tests/behavior_eval.py` (run / score / report; usage in its docstring) with `tests/prompts.md` (T1-T14, rubric bullets per prompt; T14 is a benign prompt whose premise is true) and `tests/fixtures/shop_repo`. Run it with `--runs 2` or more per arm. Keep `--max-turns` high; a scorer sometimes returns no JSON, so rescore with `--only`; a usage-limit notice comes back as an ordinary result, so check for it. Do not wait for a run with `pgrep -f` inside the same shell command: the pattern matches the waiting shell itself and never ends.
- Generated-task linter: `scripts/lint_task.py TASK.md --repo ROOT`. It checks the section contract, placeholders, cited paths and loop limits. It cannot see an invented fact that is not a path.
- Trigger tests: `../hep-analysis/tests/routing_eval.py --target task-authoring` (isolated `claude -p` with the 7 repo skills). Sets: `tests/trigger_queries.json` (22) and `tests/trigger_queries_holdout.json` (16). Sonnet recall 22/24 and 13/16, Haiku 0 in this harness (also 0 with the old description), 0 false triggers. These numbers date from 2026-10-01 and predate later description changes in ams-analysis and hep-analysis; rerun both sets with the next change to this description. The holdout is clean for one more change.

## Decisions

- 12-section template: stays fixed.
- Archetype-example tooling (`references/example-authoring.md`, `generate_skill_example.py`, `validate_skill_example.py`, `check_example_diversity.py`): keep and test it, although no skill in this repo ships an archetype `examples/` set any more. `check_example_diversity.py` is documented as historical; running or removing it is undecided.
- Open: which task consumers matter most (Claude Code, Codex or human engineers). The answer sets which adapters and prompts come first.

## Next, in this order

1. **Description trim with both trigger sets rerun.** Shorten the description and use the room for negative triggers; stack-trace-to-task queries load no skill on Sonnet, and prompt-design queries (token budget, ReAct loop) often go to `claude-api`. Run both sets, then each affected sibling's validator and tests. The boundary with `agile-development` was added to both descriptions in ea98f0d.
2. **Opus runs** (T1-T14, 2 runs per arm), if wanted.

## Known Haiku limits (do not over-tune)

- T6(a): the eval frame's own `## Task document` and `## Message to user` headings fail the "no other headings" rubric. A frame artifact, not a skill fault.
- T11(d): page size is not marked as an Open Question.
- Partial on T9(c)/(e) and T12(b) (iteration ceiling stated as a requirement; irreversibility and rollback), after the destructive-change rule. Round 3i: T12 backup and rollback put Out of Scope in 2 of 2 Haiku runs; after the premise rule (3j) it is a question in 2 of 3. Still unfixed on Haiku: an invented history for `legacy_id` in T12 (3 of 3) and T8's "signup exists" premise (2 of 3).

## Open items

- **Validator blind spots (example tooling).** Done 2026-10-02: the test-first Red failure marker and Green metric must sit inside a fence (3 tests, Round 3f). Still not checked: that a fence is actually a diff, log or failing test (other archetypes); the postmortem monitoring rule (metric + threshold + action), which is read from prose; a wrong causal chain; assertions where executed output is required; an invented API in a diff; fabricated numeric inputs; pre-written outcomes; leading elicitation options; the role/stance words. Decide which deserve a mechanical check, if any; most are review-step items.
- **Example currency.** The performance, CMS and AMS examples still carry their September snapshot notes; re-check them if the repository changes. The feature, bug and research examples were verified on 2026-10-02.
- **Untested examples.** The migration, agentic-loop and data-ml example tasks have not been handed to an implementer, so whether they are implementable as written is unknown.
- **Multi-platform.** Not verified: the external documentation URLs in `references/adapters/*.md`, whether the Codex install path is current (the adapter says "commonly"), and anything for Cursor or Copilot beyond the generic adapter.
- **Skill-reviewer proposals (Round 3d, model output, undecided):** a three-line job-routing block and one imperative rule per non-task job in the Decision Rules; collapse the 13-point Generic Agent Instruction into outcome checks; trim the 14 example prompts in `SKILL.md`; move the maintainer note out of the Decision Rules; stop restating the archetype list and script flags in the README.

## Recurring

- After each pass, update the `VALIDATION.md` header date and the counts (30 files, 104 tests) and this file's State line.
- Run the trigger sets after any change to the `SKILL.md` description.
- `scripts/__pycache__` and `tests/__pycache__` are untracked and git-ignored. Nothing to do.
