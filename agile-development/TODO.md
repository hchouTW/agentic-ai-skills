# TODO for future Claude sessions (agile-development)

State (verified 2026-09-28 on `main`, all work merged; round 2 via PR #27): `python3 scripts/validate_skill_bundle.py` OK (28 files; it was 48 before `examples/` was removed on 2026-09-25, commit 0c5530f); `python3 -m unittest discover -s tests` 44 tests OK. The skill has been run on fresh models:
- H1-H9 were run on Sonnet, Haiku and Opus. Round 2 re-ran them on Haiku with open and blind scorers.
- On Haiku the skill measurably adds the header block, planned tests, a target plus per-step verification for performance work, and irreversibility handling.

The open problem is **triggering**: from the description alone the skill rarely loads. Read `VALIDATION.md` first, especially "Round 2" and "Limitations", then this file.

Working rules:
- Work on a branch and ask before pushing or merging.
- Run the tests and the bundle validator before committing.
- Keep `SKILL.md`, `README.md`, `scripts/validate_skill_bundle.py` and `agents/openai.yaml` in sync.
- Record every result, including negative ones, in `VALIDATION.md`.
- Put temporary files in the scratchpad, not the repo.

Tooling:
- `tests/behavior_eval.py` runs the H-prompts from `tests/prompts.md` in isolated `claude -p` children and scores them in open and blind modes. 54 Haiku runs cost about $1.
- `hep-analysis/tests/routing_eval.py --fixture tests/fixtures/shop_repo` is the real-harness trigger test. It uses `tests/trigger_queries.json` (tuning) and `tests/trigger_queries_holdout.json`.
- Earlier trigger results (40/40, 50/50) came from a subagent classifying descriptions and are **not valid**.

Note: `scripts/__pycache__` and `tests/__pycache__` hold stale `.pyc` files for modules that moved to `task-authoring` (`test_example_authoring`, `generate_skill_example`, `validate_skill_example`, `check_example_diversity`). They are git-ignored; do not treat them as live code.

## Questions for the user (asked 2026-09-27 and not answered; ask again before acting)

- [ ] Is the Code File Requirement (a top-of-file comment block on every changed file) still wanted? It is the rule most likely to conflict with repository conventions. It is now scoped: not for one-line, docs or review tasks. On Haiku it is the clearest measured effect (H1 (a): 3/3 with the skill, 0/3 without).
- [ ] Which languages or stacks matter most? The answer decides which design guide gets its design advice reviewed first (see section 2).
- [ ] Sprint planning was put in scope without an answer: a subsection in `references/design-and-estimation.md` plus the description wording. Confirm it or revert it.

## 1. Triggering (highest value)

- [ ] From the description alone, the skill rarely loads on ordinary coding requests. Measured with `routing_eval.py --fixture tests/fixtures/shop_repo`, 2 runs per query:
  - Sonnet loads it in about 20% of should-trigger runs; Haiku in 0 of 232.
  - A one-line project `CLAUDE.md` rule lifts Sonnet to 48/52 (held-out 21/24), with 0 false triggers. It does not help Haiku.
  - A more directive description did not help and was reverted.
  - The README now recommends the `CLAUDE.md` line.

  Open:
  - (a) Rerun with the user's plugins installed. The harness drops the ~112 plugin skills, so real recall may be lower.
  - (b) Find anything that makes Haiku load the skill: an AGENTS.md-style rule that names the skill directly, or a SessionStart hook. Otherwise accept that Haiku needs the skill named.
  - (c) "Review my diff" is answered directly even with the `CLAUDE.md` rule.

## 2. Verification gaps

- [ ] Language design guides (`references/cpp-`, `python-`, `bash-balanced-design-guidelines.md`, about 3,000 lines): snippets were syntax-checked, and accuracy reviews fixed 8 Python and 5 Bash/C++ issues. The **design advice itself is not reviewed**. Do this after the stack-priority answer.
- [ ] Behavior after the round-2 `SKILL.md` edits (header prominence, sprint subsection) was measured on Haiku only, plan-only. If it matters, rerun H1-H9 on Sonnet and Opus with `tests/behavior_eval.py`.
  - The blind scorer is not truly blind: it guessed the arm right 41 of 54 times from plan structure. Redaction cannot hide structure, so treat the blind mode as a consistency check, not a bias check.
- [ ] One Haiku skill run broke the H5 four-question cap. Watch for it in the next behavior run.

## 3. Housekeeping

- [ ] Recurring: update the `VALIDATION.md` header date and counts after each pass. Last done 2026-09-27, but it still quotes 48 files. Record the current 28 files and 44 tests, and note the removal of `examples/`.
- [ ] The `VALIDATION.md` "Limitations" section is stale. It still says the C++ guide "was not re-validated for guidance accuracy", but the 2026-09-21 reviews checked accuracy. It also says the workflow guidance has never been exercised, which rounds 1-2 did. Update it.

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

**P4 - decisions**
- The Code File Requirement is scoped out of one-line, docs and review tasks. The step-verify guidance was folded into workflow step 3.
