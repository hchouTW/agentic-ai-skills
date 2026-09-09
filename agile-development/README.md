# Agile Development Skill

A portable Agent Skill maintained entirely in English. Its core is `SKILL.md` plus references and templates resolved through relative paths. It requires no specific MCP server, cloud account, or paid service. It supplies a workflow and checklists for turning a software request into a small, verified, reviewable increment - not a project-management tool or ticketing-system integration.

## Installation and invocation

Extract the archive and keep the complete `agile-development/` folder.

- **Codex:** place the folder in the skill directory used by your environment, commonly `~/.codex/skills/`, or import it through the mechanism supported by your version. Reload skills and invoke `$agile-development`. `agents/openai.yaml` supplies optional Codex UI metadata.
- **Claude Code:** copy it to `.claude/skills/agile-development/` in the project or `~/.claude/skills/agile-development/` for personal use. Invoke `/agile-development` or describe a matching task (new feature, bug fix, refactor, scoping, review). See the [official Claude Code skill documentation](https://code.claude.com/docs/en/skills).
- **Other agents:** instruct the agent to read `SKILL.md` first and follow its reference routing. Provide the file location explicitly if automatic discovery is unsupported.

This delivery creates a single folder; it does not change other global agent settings. Load references selectively instead of pasting the entire package into global instructions.

## Quick checks

From the skill directory (pure Python standard library, no external dependencies):

```bash
python3 -m unittest discover -s tests -v
python3 scripts/validate_skill_bundle.py
python3 scripts/create_story_card.py --actor "user" --capability "export a CSV" --outcome "download active users"
python3 scripts/validate_agile_notes.py assets/story-card.md
python3 scripts/validate_agile_notes.py --help
```

`create_story_card.py` prints a filled-in story card to stdout (or `--output <path>`); `validate_agile_notes.py` checks a markdown note for Story/Acceptance Criteria/Validation/Risks headings and exits non-zero with a clear message (not a traceback) if a heading or the file is missing. Two opt-in flags add structure checks from `references/implementation-discipline.md`: `--require-plan-verification` requires every numbered plan step to carry a real verification (rejecting placeholders such as "looks right"), and `--require-assumptions` adds an Assumptions heading to the existing requirements rather than replacing them. Both are off by default, so notes that passed before still pass.

## Coverage and boundaries

The package governs *how* to work: identifying the outcome, writing acceptance criteria, slicing scope, matching existing conventions, testing proportionally, reviewing the diff, and reporting honestly. Reference material covers story framing, validation strategy and definition of done, scenario playbooks (bug fix, new feature, endpoint, UI feature, DB migration, dependency update, CLI change, incident response, legacy code without tests), risk areas (API changes, data/persistence, security/privacy, dependencies, config, observability, performance, accessibility, reviewing someone else's change), status-update communication, lightweight design docs/estimation/feature-flagged rollout, and C++ design guidelines.

It also covers implementation discipline - the failure modes that show up in the diff rather than in the plan: deciding whether to ask or assume when a request is ambiguous (by what being wrong costs, rather than by a fixed default), writing the minimum code that solves the problem instead of speculative features and single-caller abstractions, keeping changes surgical so every changed line traces to the request (including the asymmetry between cleaning up orphans your change created and leaving pre-existing dead code alone), and turning a vague task into verifiable success criteria with a per-step plan.

It does not decide *what* to build - pair it with a domain skill (e.g. `deep-learning`, `hep-analysis`) for specialized code, and it defers to explicit user instructions that override its default workflow (e.g. "don't run tests").

All maintained instructions, templates, and metadata are in English. The skill can still answer a user in their requested language.

## Example prompts

"Add an endpoint that lets admins export a CSV of active users."

"This refactor of the auth middleware shouldn't change behavior - help me do it safely."

"I have a bug report saying the cart total is wrong with discount codes - find and fix it."
