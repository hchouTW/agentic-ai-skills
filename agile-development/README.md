# Agile Development Skill

A portable Agent Skill that turns a software request into a small, verified, reviewable increment: acceptance criteria, a validation plan, minimal changes and an honest report. It is a workflow with checklists, not a project-management tool or ticketing integration. It needs no MCP server, cloud account or paid service; the helper scripts use only the Python standard library.

## Installation and invocation

Copy or symlink the whole `agile-development/` folder.

- **Codex:** put it in `~/.codex/skills/` (or your environment's skill directory), reload skills and invoke `$agile-development`. `agents/openai.yaml` holds optional UI metadata.
- **Claude Code:** copy to `.claude/skills/agile-development/` (project) or `~/.claude/skills/agile-development/` (personal). Invoke `/agile-development` or describe a matching task. See the [Claude Code skills documentation](https://code.claude.com/docs/en/skills).
- **Antigravity:** copy to `.agents/skills/agile-development/` (workspace) or `~/.gemini/config/skills/agile-development/` (global). It triggers automatically from the `name`/`description`. See the [Antigravity skills documentation](https://antigravity.google/docs/skills).
- **Other agents:** tell the agent to read `SKILL.md` first and follow its reference routing.

Models rarely load a process skill for a plain "add X" or "fix Y" from the description alone. A line in the project `CLAUDE.md` (or `AGENTS.md`/`GEMINI.md`) that names the skill, gives example phrasings and lists exclusions works best. Edit the exclusions to match your installed skills:

> Before starting a task, check the skill list and call the Skill tool for the skill that fits. For a non-trivial change to software in this repository (feature, bug fix, refactor, migration, dependency update), a code or PR review, an incident postmortem, a design or architecture decision, estimation or sprint planning, that is "agile-development" - call it before reading files or asking questions. It also covers requests phrased like "take a look at my pull request", "which datastore should we use for X", "is this too complicated", "upgrade package X", "add a column to table Y" or "move X to a new schema". It is not for one-line or typo fixes, writing a ticket or spec for someone else (task-authoring), PyTorch/ML code (deep-learning), physics analysis (hep-analysis), papers (academic-papers) or diagrams (academic-diagrams).

Measured loading rates for this line and its variants are in `VALIDATION.md` (Rounds 2-5) and `TODO.md`.

## Quick checks

From this directory:

```bash
python3 -m unittest discover -s tests
python3 scripts/validate_skill_bundle.py
python3 scripts/create_story_card.py --actor "user" --capability "export a CSV" --outcome "download active users"
python3 scripts/validate_agile_notes.py assets/story-card.md
```

- `create_story_card.py` prints a filled story card (or writes it with `--output <path>`).
- `validate_agile_notes.py` checks a note for Story, Acceptance Criteria, Validation and Risks headings. Optional `--require-plan-verification` and `--require-assumptions` add the structure checks from `references/implementation-discipline.md`.
- `tests/behavior_eval.py` and the routing harness (`python3 ../hep-analysis/tests/routing_eval.py tests/trigger_queries.json --target agile-development --model haiku`) call the `claude` CLI and cost money. They are not part of the unit tests; see `tests/prompts.md` and `VALIDATION.md`.

## Coverage and boundaries

- Covers: story framing, acceptance criteria, validation strategy, definition of done.
- Covers: playbooks for bug fixes, features, endpoints, UI, DB migrations, dependency updates, CLI changes, incidents and legacy code without tests.
- Covers: risk review, PR review, status updates, design docs, estimation, sprint planning, feature-flagged rollout, architecture decisions and ADRs.
- Covers: implementation discipline (ask vs. assume, minimal changes, verifiable success criteria) and C++, Python and Bash design guidelines.
- Defers to `task-authoring`: standalone tickets and specs, worked examples for a skill's `examples/`, and LLM prompt or token-budget design (install it alongside).
- Defers to domain skills (`deep-learning`, `hep-analysis`) for specialized code, and to explicit user instructions that override its workflow.

All maintained instructions, templates and metadata are in English. The skill can still answer in the user's language.

## Example prompts

- "Add an endpoint that lets admins export a CSV of active users."
- "This refactor of the auth middleware shouldn't change behavior - help me do it safely."
- "The cart total is wrong with discount codes - find and fix it."
- "Review my pull request that adds rate limiting."
- "Which datastore should we use for session data? Write it up as an ADR."
- "Is this too complicated for what it does?"
- "Plan a sprint from this backlog of 12 stories."
