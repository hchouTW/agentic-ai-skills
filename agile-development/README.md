# Agile Development Skill

A portable Agent Skill maintained entirely in English. Its core is `SKILL.md` plus references and templates resolved through relative paths. It requires no specific MCP server, cloud account, or paid service. It supplies a workflow and checklists for turning a software request into a small, verified, reviewable increment - not a project-management tool or ticketing-system integration.

## Installation and invocation

Extract the archive and keep the complete `agile-development/` folder.

- **Codex:** place the folder in the skill directory used by your environment, commonly `~/.codex/skills/`, or import it through the mechanism supported by your version. Reload skills and invoke `$agile-development`. `agents/openai.yaml` supplies optional Codex UI metadata.
- **Claude Code:** copy it to `.claude/skills/agile-development/` in the project or `~/.claude/skills/agile-development/` for personal use. Invoke `/agile-development` or describe a matching task (new feature, bug fix, refactor, scoping, review). See the [official Claude Code skill documentation](https://code.claude.com/docs/en/skills).
- **Antigravity:** copy it to `.agents/skills/agile-development/` in the workspace (or `~/.gemini/config/skills/agile-development/` for a global install; older installs may still read `.agent/skills/`). It triggers automatically - the agent reads every installed skill's `name`/`description` at session start and loads the full `SKILL.md` when a task matches, no explicit invocation needed. See the [Antigravity skills documentation](https://antigravity.google/docs/skills).
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
python3 scripts/generate_skill_example.py --archetype contrast --skill agile-development --role "Staff Software Engineer" --use-case "scoping a bug fix"
python3 scripts/generate_skill_example.py --archetype trajectory --skill agile-development --role "Senior Software Engineer" --problem-input "a raw bug report"
python3 scripts/generate_skill_example.py --archetype gated-pipeline --skill agile-development --role "Principal Software Engineer" --high-stakes-task "a feature-flagged rollout RFC"
python3 scripts/generate_skill_example.py --archetype decision-tree --skill agile-development --role "Engineering Lead" --scenario "an ambiguous incident page"
python3 scripts/validate_skill_example.py examples/01-bug-fix-scoping-review.md
```

`create_story_card.py` prints a filled-in story card to stdout (or `--output <path>`); `validate_agile_notes.py` checks a markdown note for Story/Acceptance Criteria/Validation/Risks headings and exits non-zero with a clear message (not a traceback) if a heading or the file is missing. Two opt-in flags add structure checks from `references/implementation-discipline.md`: `--require-plan-verification` requires every numbered plan step to carry a real verification (rejecting placeholders such as "looks right"), and `--require-assumptions` adds an Assumptions heading to the existing requirements rather than replacing them. Both are off by default, so notes that passed before still pass.

`generate_skill_example.py` scaffolds an empty `<skill>/examples/*.md` skeleton without inventing content, for one of four archetypes selected with `--archetype {contrast,trajectory,gated-pipeline,decision-tree}`: each emits its own fixed section headers plus a matching frontmatter scenario flag (`--use-case` / `--problem-input` / `--high-stakes-task` / `--scenario`); `--takeaways` (3-6, default 4) is valid only with `--archetype contrast`. `validate_skill_example.py` reads the `archetype:` frontmatter field to pick that archetype's rule set (a file with no `archetype:` field is treated as `contrast`, for backward compatibility) and checks required sections in order, archetype-specific structure (a 3-6 item Key Takeaways list for Contrast, fenced code blocks in Trajectory's Surgical Execution/Verification Evidence sections, `**Gate:**` lines in every Gated Pipeline phase, a >=3-row Triage Matrix table for Decision-Tree), and zero placeholder markers. See `references/example-authoring.md` for all four generation prompts, the archetype-selection guide, and the format spec.

## Coverage and boundaries

The package governs *how* to work: identifying the outcome, writing acceptance criteria, slicing scope, matching existing conventions, testing proportionally, reviewing the diff, and reporting honestly. Reference material covers story framing, validation strategy and definition of done, scenario playbooks (bug fix, new feature, endpoint, UI feature, DB migration, dependency update, CLI change, incident response, legacy code without tests), risk areas (API changes, data/persistence, security/privacy, dependencies, config, observability, performance, accessibility, reviewing someone else's change), status-update communication, lightweight design docs/estimation/feature-flagged rollout, software architecture (recognizing architectural decisions, boundaries and dependency direction, data ownership, ADRs), and C++ design guidelines.

It also covers implementation discipline - the failure modes that show up in the diff rather than in the plan: deciding whether to ask or assume when a request is ambiguous (by what being wrong costs, rather than by a fixed default), writing the minimum code that solves the problem instead of speculative features and single-caller abstractions, keeping changes surgical so every changed line traces to the request (including the asymmetry between cleaning up orphans your change created and leaving pre-existing dead code alone), and turning a vague task into verifiable success criteria with a per-step plan.

It also covers authoring a canonical worked example for this or another skill's `examples/` directory, in any of four archetypes - Contrast (Weak vs. Expert plus key takeaways), Execution Trajectory (step-by-step task resolution), Gated Pipeline (multi-phase build with explicit acceptance gates), or Decision-Tree (branching triage matrix plus end-to-end execution script) - see `references/example-authoring.md` for the archetype-selection guide and the `generate_skill_example.py`/`validate_skill_example.py` scripts above.

It also covers prompt engineering and token optimization for LLM-facing work - role framing, few-shot/chain-of-thought examples, structured-output contracts, and guardrails on the design side; token budgets, context-window hygiene, and cheapest-adequate model-tier selection on the cost side; and two optional story-card fields (prompt directive, token budget) for stories whose behavior depends on an LLM call - see `references/prompt-engineering-and-token-optimization.md`.

It does not decide *what* to build - pair it with a domain skill (e.g. `deep-learning`, `hep-analysis`) for specialized code, and it defers to explicit user instructions that override its default workflow (e.g. "don't run tests").

All maintained instructions, templates, and metadata are in English. The skill can still answer a user in their requested language.

## Example prompts

"Add an endpoint that lets admins export a CSV of active users."

"This refactor of the auth middleware shouldn't change behavior - help me do it safely."

"I have a bug report saying the cart total is wrong with discount codes - find and fix it."
