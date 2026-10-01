# TODO for future Claude sessions (agile-development)

State (2026-10-01, rounds 4-5 on branch `agile-development-todo-round4`, PR #31; round 3 merged via PR #30): `python3 scripts/validate_skill_bundle.py` OK (30 files); `python3 -m unittest discover -s tests` 44 tests OK. The skill has been run on fresh models:
- H1-H9 were run on Sonnet, Haiku and Opus. Round 2 re-ran them on Haiku and round 5 on Sonnet, with open and blind scorers.
- On Haiku the skill measurably adds the header block, planned tests, a target plus per-step verification for performance work, and irreversibility handling.

From the description alone the skill rarely loads. The README's project `CLAUDE.md` line names the skill, gives example phrasings and lists exclusions. With it, Sonnet loads the skill 52/52 times and Haiku 42/52 (24/28 on each of two fresh held-out sets, 46/52 with the user's plugins installed). Read `VALIDATION.md` first, especially "Round 4", "Round 5" and "Limitations", then this file.

Working rules:
- Work on a branch and ask before pushing or merging.
- Run the tests and the bundle validator before committing.
- Keep `SKILL.md`, `README.md`, `scripts/validate_skill_bundle.py` and `agents/openai.yaml` in sync.
- Record every result, including negative ones, in `VALIDATION.md`.
- Put temporary files in the scratchpad, not the repo.

Tooling:
- `tests/behavior_eval.py` runs the H-prompts from `tests/prompts.md` in isolated `claude -p` children and scores them in open and blind modes. 54 Haiku runs cost about $1.
- `hep-analysis/tests/routing_eval.py --fixture tests/fixtures/shop_repo` is the real-harness trigger test. It uses `tests/trigger_queries.json` (tuning), `tests/trigger_queries_holdout.json` (no longer clean for the phrasings line), `tests/trigger_queries_holdout2.json` (written after it by the same session) and `tests/trigger_queries_holdout3.json` (written by a separate session). `--user-setup` runs with the user's plugins, hooks and global CLAUDE.md; `--any-skill` counts the target even if another skill loads first. To test a rule, copy the fixture to the scratchpad and add a `CLAUDE.md` or `.claude/settings.json` hook there.
- Several runs in a row can hit the account usage limit; errored runs are excluded and printed, so rerun them.
- Earlier trigger results (40/40, 50/50) came from a subagent classifying descriptions and are **not valid**.

Note: `scripts/__pycache__` and `tests/__pycache__` hold stale `.pyc` files for modules that moved to `task-authoring` (`test_example_authoring`, `generate_skill_example`, `validate_skill_example`, `check_example_diversity`). They are git-ignored; do not treat them as live code.

## User decisions

- 2026-09-28: the Code File Requirement stays as scoped; sprint planning stays in scope; all three language guides were reviewed (round 3).
- 2026-10-01: bug reports routed to `systematic-debugging` and reviews routed to `code-review` count as correct (`also_ok`); H1-H9 rerun on Sonnet only (not Opus); leave the global `~/.claude/CLAUDE.md` alone and only suggest wording; Homebrew Bash 5.3 is installed at `/opt/homebrew/bin/bash`.

## 1. Triggering

- [ ] Haiku still misses "is this over-engineered?"-type questions (no skill, with either line) and sometimes an
  incident report ("prod is throwing 502s"), where it reads files instead. No fix tried yet that does not add false
  triggers.
- [ ] Sonnet sent "debug the NaN loss in my transformer" here in 2 of 6 runs (rounds 4-5). If it grows, try naming
  "training/NaN/loss debugging" in the "not for" clause and re-measure on all four sets.

## 2. Verification gaps

- [ ] H6 (b): with the skill, the message for a typo fix runs past two sentences (Sonnet ~F~ in round 5, Haiku once in
  round 2). `SKILL.md` already says to collapse trivial summaries; consider moving that rule into the workflow step 9
  text and re-running H6 only (`behavior_eval.py run --only H6`).
- [ ] Opus has not been re-run since 2026-09-22 (user chose Sonnet only on 2026-10-01).
- [ ] The blind scorer is not blind (Sonnet round 5: 54/54 arm guesses right). Treat blind mode as a consistency check.

## 3. Housekeeping

- [ ] Recurring: update the `VALIDATION.md` header date and counts after each pass. Last done 2026-10-01 (30 files, 44 tests).
- [ ] Global `~/.claude/CLAUDE.md`: do not edit it (user decision, 2026-10-01). The wording suggested to the user, to follow
  their existing "check whether one of my domain skills should be applied first" line, is below. It was tested only as
  a project `CLAUDE.md` line, never in the global file:
  > For a non-trivial software change, code or PR review, postmortem, design decision, estimation or sprint planning,
  > that is "agile-development" (also for requests like "take a look at my pull request", "which datastore should we
  > use", "upgrade package X"); not for one-line fixes, tickets for someone else (task-authoring) or PyTorch code
  > (deep-learning).

## Done (do not redo; details in `VALIDATION.md`)

**P1 - behavior and triggering**
- `tests/prompts.md`: 15 prompts, (a)-(o), each with expected behaviors, plus the harder H1-H9. The original 15 mostly do not discriminate between the arms.
- H1-H9 were run 3x per cell per arm on Sonnet, Haiku and Opus (2026-09-21/22), plus a re-check of the question-count cap. Round 2 (2026-09-27) re-ran them on Haiku with open and blind scores: 164/180 verdicts agree, and the direction is the same on every bullet that separates the arms.
- Rubric fixes: H6 (b) now measures the user message; H7-H9 (d) no longer count repo reads in plan-only runs; H6 (a) allows a matching test update.
- Header prominence: workflow step 5 now says "a docstring does not count, do not defer it". Haiku H1 (a) went from 1/3 to 3/3.
- Routing hygiene with `task-authoring`: both descriptions have a "Not for ..." sentence.
- Sprint planning is in scope. Sonnet loads the skill for sprint queries 4-5/12 alone and 12/12 with the `CLAUDE.md` rule.

**P2 - helpers and guidance (2026-09-21)**
- Messy-input probes of `create_story_card.py` and `validate_agile_notes.py` found and fixed BOM, closing-`##`, fenced-code, `Works!` and empty-field defects, with regression tests added. Setext headings stay unsupported by design.
- Snippets in the three language guides were syntax-checked. Accuracy reviews fixed Python 8 and Bash/C++ 5.
- Examples: the validators passed on all 24, and 25/27 Python blocks compiled. The examples were later removed (2026-09-25).
- Dogfood: Sonnet ran 3 tasks in a scratch repo. Gaps were fixed or logged.

**P3 - content and structure (2026-09-21)**
- Progressive disclosure: added "load only when" hints for the language guides. Measured on Haiku: 0.4 references per run, max 3.
- Overlap between the discipline, validation and risk references, and between architecture and estimation, was handled with cross-references; content stays in place.
- Gap probe of perf, flaky tests, security, monorepo, CI failure and superpowers pairing: no new sections needed; one ask-rule wording fix.
- Multi-platform check: no Claude-only tools.
- Skill-reviewer pass: 4 of 9 findings applied, the rest declined with reasons.

**Round 3 (2026-09-28/29)**
- User decisions recorded (header rule kept as scoped, sprint kept, all three guides reviewed).
- Design-advice review of the Python, C++ and Bash guides, with every changed snippet run (mypy, clang with sanitizers, Bash 3.2). Includes the Google `<filesystem>` ban, the Bash errexit-in-condition gap and an arithmetic-injection bug in the Bash validation example.
- Real-setup routing run (`--user-setup`): Sonnet 42/52, Haiku 11/52, 0 false triggers.
- Rule variants for Haiku: a scoped line that names the skill and its exclusions is now in the README (Sonnet 51/52, Haiku 30/52, 0 false triggers). "Review my diff" loads on Sonnet with it.
- `VALIDATION.md` header counts and "Limitations" updated.

**P4 - decisions**
- The Code File Requirement is scoped out of one-line, docs and review tasks. The step-verify guidance was folded into workflow step 3.

**Round 4 (2026-10-01)**
- Example-phrasings sentence added to the README line: Haiku 30->42/52 tuning, 16->24/28 on the new holdout2, 0 false triggers; Sonnet 52/52 with 1/40 false trigger.
- The line tested with the user's plugins: scoped Haiku 39/52, Sonnet 52/52; phrasings Haiku 46/52; 0 false triggers.
- Bug queries carry `also_ok: ["systematic-debugging"]` (user decision).
- Bash 4+ snippets run on Bash 5.3: the dispatch-table example aborted the script on an empty action (fixed); added the `((count++))` and `inherit_errexit` traps.

**Round 5 (2026-10-01)**
- holdout3, written by a separate session: Haiku phrasings 24/28 vs. scoped 23/28, Sonnet 28/28, 0 false triggers. The phrasings help less than holdout2 suggested.
- Sonnet false-trigger check at 4 runs: 104/104, 1/80 (the NaN-loss query).
- H1-H9 on Sonnet: the round-2 edits hold (header, target, per-step verification, no false verification claims); H5 cap held; H6 (b) regressed.
- Independent reviews of the three language guides: 3 C++, 4 Python and 4 Bash findings, all reproduced and fixed.
- Review queries carry `also_ok: ["code-review"]` (user decision).
