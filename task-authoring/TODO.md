# TODO for future Claude sessions (task-authoring)

State (2026-10-02, `main` 043f014 after PR #107, #110, #111 and #112): nothing is queued. `python3 scripts/validate_skill_bundle.py` OK (30 files, 12-section template contract); `python3 -m unittest discover -s tests` 104 tests OK; description 1017 of 1024 characters; `examples/` holds 9 task examples plus a README; `tests/prompts.md` has T1-T14. Read the newest rounds of `VALIDATION.md` (3l, then 3j and 3m) first, then this file.

Where the skill stands (all on 2026-10-02; model runs, small samples, the open scorer can tell the arm from the 12-section template, so the gap is overstated):

| Model | Baseline P / ~ / F | Skill P / ~ / F | Notes |
|---|---|---|---|
| Haiku (Round 3g, T1-T13) | 18 / 25 / 65 | 67 / 36 / 5 | slips below are a known limit |
| Sonnet (Round 3g, T1-T13) | 57 / 23 / 28 | 99 / 9 / 0 | no invented fact in 3i, 3j |
| Opus (Round 3l, T1-T14) | 58 / 26 / 34 | 106 / 11 / 1 | no invented fact in the premise cases |

Rules added this session, both in `SKILL.md` Decision Rules: a worked example's incident is labelled illustrative (Round 3h, Haiku T13(e) fixed); a premise in the request that the repository does not show is Unresolved, not Background fact, and a premise the check confirms is written as Confirmed (Round 3j, Haiku partial). The three newest example tasks (migration, agentic-loop, data-ml) were each implemented by a fresh Sonnet agent: all "implementable with guesses", defects fixed (Round 3m).

Working rules:
- Work on a branch in a worktree (`git worktree add .worktrees/<name> origin/main`); the main checkout is shared with other Claude sessions that switch branches under you. Check `git branch --show-current` before every commit. Ask before pushing.
- The user merges PRs by running `gh pr merge` themselves: the auto-mode classifier blocks an agent merge ("Merge Without Review") and the block covers the outcome, so do not retry it another way. After a merge, delete the remote branch and remove the worktree.
- Run the tests and the validator before committing.
- Keep `SKILL.md`, `README.md`, `scripts/validate_skill_bundle.py` `REQUIRED_PATHS` and `agents/openai.yaml` in sync.
- The template's 12-section contract (`REQUIRED_TEMPLATE_SECTIONS`) is exact. Do not add or remove a section without saying so, and update the validator, the tests and all of `examples/` together.
- Record every result, including negative ones, in `VALIDATION.md`.
- Haiku loads `SKILL.md` but rarely opens references, so a must-do rule belongs in `SKILL.md`. Pair every refusal or restriction rule with a benign prompt (a sibling's unscoped rule over-refused; T14 pairs the premise rule).

Tooling to reuse instead of hand-run subagents:
- Behavior eval: `tests/behavior_eval.py` (run / score / report; usage in its docstring) with `tests/prompts.md` (T1-T14, rubric bullets per prompt; T14 is the benign prompt whose premise is true) and `tests/fixtures/shop_repo`. Run it with `--runs 2` or more per arm. A scorer sometimes returns no JSON, so rescore with `--only`; a usage-limit notice comes back as an ordinary result, so check for it. The eval sandbox hides the skill's `scripts/`, so a skill-arm run cannot run `lint_task.py`; lint the extracted task yourself.
- Waiting for runs: do not use `pgrep -f` in a watcher (the pattern matches the watching shell, so it never ends or ends early), and a background launcher's "completed" notice only means the launcher exited. Count `' run [0-9]'` lines in each run's log, or wait for the output file. Do not edit `SKILL.md` while a run is in flight: the runs read it live.
- Reading skill-arm tasks for invented facts: dump each result's `text` to a `.md` file and read it against the fixture. The linter and a path count cannot find an invented fact that is not a path.
- Generated-task linter: `scripts/lint_task.py TASK.md --repo ROOT`. It checks the section contract, placeholders, cited paths and loop limits. Use `--repo .` (the whole repository) for examples that cite sibling skills.
- Trigger tests: `../hep-analysis/tests/routing_eval.py --target task-authoring` (isolated `claude -p` with the 7 repo skills). Sets: `tests/trigger_queries.json` (22) and `tests/trigger_queries_holdout.json` (16). Sonnet recall 20/24 and 12/16 (2026-10-02, 0 false triggers); Haiku 0 in this harness. The holdout was spent on the Round 3k trial and is no longer clean; rerun both sets with the next description change and treat the holdout as a second main set.

## Decisions

- 12-section template: stays fixed.
- Description: stays at 1017 characters. Round 3k tried a 925-character version with a stack-trace trigger and a `claude-api` negative trigger: no gain (19/24, 12/16), reverted. Stack-trace-to-task and self-healing-loop queries load no skill on Sonnet, and token-budget and ReAct queries go to `claude-api`; wording did not move either. Do not retry the same trim.
- Archetype-example tooling (`references/example-authoring.md`, `generate_skill_example.py`, `validate_skill_example.py`, `check_example_diversity.py`): keep and test it, although no skill in this repo ships an archetype `examples/` set any more. `check_example_diversity.py` is documented as historical; running or removing it is undecided.
- Open: which task consumers matter most (Claude Code, Codex or human engineers). The answer sets which adapters and prompts come first.

## Next

Nothing is required. New work should come from a failure, a repository change that stales an example, or a request for a new consumer. Optional, in order of value:

1. **Agentic-loop example, real run.** `examples/agentic-loop-task.md` asks for `--retry-passes N` in `behavior_eval.py run` and one real 2-prompt `--model haiku` run recorded in `VALIDATION.md`. Nothing of it is built (the implementer's version in Round 3m was discarded). Building it is new scope: ask first. A fresh Sonnet implementer got all criteria passing with a stub `claude`; its guesses are now settled in the example: the cap value and the usage-limit text stay Open Questions, and `--retry-passes N` is defined as the total number of passes.
2. **Premise rule on Haiku.** Only if a Haiku failure shows up in real use: the invented history for `legacy_id` (T12, 3 of 3 runs) and T8's "signup exists" premise (2 of 3) are unchanged by the Round 3j rule. Do not tune for them without a new failure.

## Known Haiku limits (do not over-tune)

- T6(a): the eval frame's own `## Task document` and `## Message to user` headings fail the "no other headings" rubric. A frame artifact, not a skill fault.
- T11(d): page size is not marked as an Open Question.
- Partial on T9(c)/(e) and T12(b) (iteration ceiling stated as a requirement; irreversibility and rollback). After the premise rule (3j), T12 backup and rollback is a question in 2 of 3 runs, out of scope in 2 of 2 before.
- The request's premise written as repository fact: T8 "signup exists" (2 of 3), T12 invented `legacy_id` history (3 of 3), one over-hedge on the benign T14 (1 of 3). Sonnet and Opus show none of these.

## Open items

- **Validator blind spots (example tooling).** Done: the test-first Red failure marker and Green metric must sit inside a fence (3 tests, Round 3f). Still not checked: that a fence is actually a diff, log or failing test (other archetypes); the postmortem monitoring rule (metric + threshold + action), which is read from prose; a wrong causal chain; assertions where executed output is required; an invented API in a diff; fabricated numeric inputs; pre-written outcomes; leading elicitation options; the role/stance words. Decide which deserve a mechanical check, if any; most are review-step items.
- **Example currency.** The performance, CMS and AMS examples still carry their September snapshot notes; re-check them if the repository changes. The feature, bug, research, migration, agentic-loop and data-ml examples were verified on 2026-10-02.
- **Multi-platform.** Not verified: the external documentation URLs in `references/adapters/*.md`, whether the Codex install path is current (the adapter says "commonly"), and anything for Cursor or Copilot beyond the generic adapter.
- **Skill-reviewer proposals (Round 3d, model output, undecided):** a three-line job-routing block and one imperative rule per non-task job in the Decision Rules; collapse the 13-point Generic Agent Instruction into outcome checks; trim the 14 example prompts in `SKILL.md`; move the maintainer note out of the Decision Rules; stop restating the archetype list and script flags in the README. Any trim to `SKILL.md` needs a Haiku and Sonnet rerun, since Haiku reads only that file.

## Recurring

- After each pass, update the `VALIDATION.md` header date and the counts (30 files, 104 tests) and this file's State line.
- Run the trigger sets after any change to the `SKILL.md` description.
- `scripts/__pycache__` and `tests/__pycache__` are untracked and git-ignored. Nothing to do.
