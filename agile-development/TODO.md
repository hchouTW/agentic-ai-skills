# TODO for future Claude sessions (agile-development)

State (2026-09-29, round 3 on branch `agile-development-todo-round3`; round 2 merged via PR #27): `python3 scripts/validate_skill_bundle.py` OK (28 files); `python3 -m unittest discover -s tests` 44 tests OK. The skill has been run on fresh models:
- H1-H9 were run on Sonnet, Haiku and Opus. Round 2 re-ran them on Haiku with open and blind scorers.
- On Haiku the skill measurably adds the header block, planned tests, a target plus per-step verification for performance work, and irreversibility handling.

The open problem is still **triggering**: from the description alone the skill rarely loads. A project `CLAUDE.md` line that names the skill and its exclusions (now in the README) fixes Sonnet (51/52) and half-fixes Haiku (30/52). Read `VALIDATION.md` first, especially "Round 2", "Round 3" and "Limitations", then this file.

Working rules:
- Work on a branch and ask before pushing or merging.
- Run the tests and the bundle validator before committing.
- Keep `SKILL.md`, `README.md`, `scripts/validate_skill_bundle.py` and `agents/openai.yaml` in sync.
- Record every result, including negative ones, in `VALIDATION.md`.
- Put temporary files in the scratchpad, not the repo.

Tooling:
- `tests/behavior_eval.py` runs the H-prompts from `tests/prompts.md` in isolated `claude -p` children and scores them in open and blind modes. 54 Haiku runs cost about $1.
- `hep-analysis/tests/routing_eval.py --fixture tests/fixtures/shop_repo` is the real-harness trigger test. It uses `tests/trigger_queries.json` (tuning) and `tests/trigger_queries_holdout.json`. `--user-setup` runs with the user's plugins, hooks and global CLAUDE.md; `--any-skill` counts the target even if another skill loads first. To test a rule, copy the fixture to the scratchpad and add a `CLAUDE.md` or `.claude/settings.json` hook there.
- Several runs in a row can hit the account usage limit; errored runs are excluded and printed, so rerun them.
- Earlier trigger results (40/40, 50/50) came from a subagent classifying descriptions and are **not valid**.

Note: `scripts/__pycache__` and `tests/__pycache__` hold stale `.pyc` files for modules that moved to `task-authoring` (`test_example_authoring`, `generate_skill_example`, `validate_skill_example`, `check_example_diversity`). They are git-ignored; do not treat them as live code.

## User decisions (answered 2026-09-28)

- The Code File Requirement stays as scoped (not for one-line, docs or review tasks).
- Sprint planning stays in scope.
- All three language design guides were to be reviewed for design advice; done in round 3.

## 1. Triggering (highest value)

- [ ] Haiku with the recommended scoped `CLAUDE.md` line: 30/52 tuning, 16/24 held-out, 0 false triggers. It still misses
  PR reviews ("can you look over this PR"), design questions ("Redis or Postgres?"), migrations, dependency bumps and
  "is this over-engineered?". Options: add example phrasings to the line and re-measure on both sets (watch the false
  triggers, which a broader line pushed to 12-14 of 40), or accept that Haiku needs the skill named.
- [ ] The scoped line was tested in the project-only harness. Test it together with the user's plugins
  (`--user-setup` with a fixture `CLAUDE.md`). There the superpowers process skills (`brainstorming`,
  `systematic-debugging`) take many requests first, and the agile skill never loads afterwards.
- [ ] Decide whether bug reports should route to `systematic-debugging` rather than here when superpowers is installed.
  If yes, mark it `also_ok` for bug queries in `trigger_queries*.json`.
- [ ] The global `~/.claude/CLAUDE.md` rule is the generic kind that reached Sonnet 42/52 in the real setup and Haiku
  11/52. Suggest the scoped wording to the user; do not edit their global file without asking.

## 2. Verification gaps

- [ ] Language guides: Bash 4+/5 behavior (namerefs, `declare -A`, `mapfile -d ''`, errexit on `((c++))`) is checked for
  syntax only; run it if a newer Bash becomes available (`brew install bash`). The round-3 design review was one pass by
  one session; an independent reviewer pass is optional.
- [ ] Behavior after the round-2 `SKILL.md` edits (header prominence, sprint subsection) was measured on Haiku only, plan-only. If it matters, rerun H1-H9 on Sonnet and Opus with `tests/behavior_eval.py`.
  - The blind scorer is not truly blind: it guessed the arm right 41 of 54 times from plan structure. Redaction cannot hide structure, so treat the blind mode as a consistency check, not a bias check.
- [ ] One Haiku skill run broke the H5 four-question cap. Watch for it in the next behavior run.

## 3. Housekeeping

- [ ] Recurring: update the `VALIDATION.md` header date and counts after each pass. Last done 2026-09-28 (28 files, 44 tests).

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
