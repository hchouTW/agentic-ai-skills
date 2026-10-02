# Task Authoring Skill

Turns a short request ("create a task for...", a bug report, a feature idea) into an implementation-ready Task Markdown document that another person or agent can pick up without the original conversation. It reads the repository, marks each claim as Confirmed, Inferred, or Unresolved, and fills a fixed template (Background through References). It also helps author canonical worked examples for a skill's `examples/` directory and design or budget LLM prompts.

It is not for implementing a change, scoping one live in the current conversation, or integrating with a ticketing system. It needs no MCP server, cloud account, or paid service; everything is plain Markdown plus Python standard-library scripts.

## Installation and invocation

Copy the whole `task-authoring/` folder; do not split it.

- **Codex:** put it in `~/.codex/skills/` (or the skill directory your version uses), reload skills, and invoke `$task-authoring`. `agents/openai.yaml` holds optional UI metadata. See [references/adapters/codex.md](references/adapters/codex.md).
- **Claude Code:** copy to `.claude/skills/task-authoring/` (project) or `~/.claude/skills/task-authoring/` (personal). Invoke `/task-authoring` or describe a matching task. See [references/adapters/claude-code.md](references/adapters/claude-code.md) and the [official Claude Code skill documentation](https://code.claude.com/docs/en/skills).
- **Antigravity:** copy to `.agents/skills/task-authoring/` (workspace) or `~/.gemini/config/skills/task-authoring/` (global); older installs may read `.agent/skills/`. It triggers automatically from the `name`/`description`. See [references/adapters/antigravity.md](references/adapters/antigravity.md) and the [Antigravity skills documentation](https://antigravity.google/docs/skills).
- **Other agents:** tell the agent to read `SKILL.md` first and follow its reference routing. See [references/adapters/generic-agent.md](references/adapters/generic-agent.md).

Installing adds one folder and changes no global agent settings. All maintained instructions, templates, and metadata are in English; the skill can still reply in the user's language.

## Quick checks

Run from the skill directory (standard library only):

```bash
python3 scripts/validate_skill_bundle.py
python3 -m unittest discover -s tests
python3 scripts/lint_task.py examples/migration-task.md --repo ..
```

- `validate_skill_bundle.py` checks that shipped files exist, `SKILL.md` frontmatter is valid, this README keeps its section headings, and `templates/task-template.md` matches the fixed section contract.
- `lint_task.py TASK.md [--repo REPO_ROOT]` checks a generated task: cited paths exist, and agent/retry-loop tasks state a maximum-iteration limit.
- `generate_skill_example.py --archetype A --skill S --role R` scaffolds an empty example skeleton for one of eight archetypes (contrast, trajectory, gated-pipeline, decision-tree, elicitation, adversarial-audit, test-first, postmortem), plus the matching scenario flag; `validate_skill_example.py FILE` checks a filled example. Details and flags: `references/example-authoring.md`.
- `check_example_diversity.py` is historical and not part of authoring.

## Coverage and boundaries

Covers:

- Task authoring: intent, repository inspection, evidence model, fixed template (`SKILL.md`, `templates/task-template.md`).
- Verifiable acceptance criteria and a final quality gate (`references/acceptance-criteria.md`, `references/task-quality-checklist.md`).
- Canonical worked examples in eight archetypes (`references/example-authoring.md`).
- Prompt design and token budgets (`references/prompt-engineering-and-token-optimization.md`).
- Tasks for agentic or iterative systems: loop pattern, error feedback, termination and iteration limits (`references/loop-engineering.md`).

Defers or excludes:

- Implementing the task: use `agile-development` or a domain skill.
- Ambiguous product or domain decisions: left as Open Questions for a human.
- Building an LLM, a vendor-specific API integration, or an autonomous development agent.

Validation history and open items are in `VALIDATION.md` and `TODO.md`.

## Example prompts

- "Create a task for RICH reconstruction performance analysis."
- "Write a task for adding a CSV export endpoint for admins."
- "Turn this bug report into an implementation-ready task doc."
- "Generate a canonical `examples/` entry for the `hep-analysis` skill contrasting a weak vs. expert systematics writeup."
- "Design a prompt template for a classification pipeline and give me a token budget."
- "Create a task for an autonomous log-triage agent that retries a flaky search API until it finds the root cause or hits an iteration limit."
