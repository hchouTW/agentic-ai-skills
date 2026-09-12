# Skill Router

A portable Agent Skill maintained entirely in English. It contains no scripts or assets - `SKILL.md` is a lightweight triage rule set that routes a task to one of this collection's domain skills (`academic-papers`, `agile-development`, `deep-learning`, `hep-analysis`, `task-authoring`) before work begins. It requires no specific MCP server, cloud account, or paid service.

## Installation and invocation

Extract the archive and keep the complete `skill-router/` folder alongside the domain skills it routes to.

- **Codex:** place the folder in the skill directory used by your environment, commonly `~/.codex/skills/`, or import it through the mechanism supported by your version. Reload skills; `skill-router` is designed to trigger automatically from its description on any non-trivial task, so explicit `$skill-router` invocation is optional. `agents/openai.yaml` supplies optional Codex UI metadata.
- **Claude Code:** copy it to `.claude/skills/skill-router/` in the project or `~/.claude/skills/skill-router/` for personal use. It is designed to trigger automatically from its description; `/skill-router` also works if you want to invoke the check explicitly. See the [official Claude Code skill documentation](https://code.claude.com/docs/en/skills).
- **Antigravity:** copy it to `.agents/skills/skill-router/` in the workspace (or `~/.gemini/config/skills/skill-router/` for a global install; older installs may still read `.agent/skills/`). It is designed to trigger automatically from its description via Antigravity's progressive disclosure - no explicit invocation needed. See the [Antigravity skills documentation](https://antigravity.google/docs/skills).
- **Other agents:** instruct the agent to read `SKILL.md` first and check the routing rules before proceeding with any other work.

This delivery creates a single folder; it does not change other global agent settings. It only routes to skills that are actually installed - if you don't install `academic-papers`, `agile-development`, `deep-learning`, `hep-analysis`, or `task-authoring`, the corresponding routing row is simply never triggered.

## Quick checks

`skill-router` is pure routing instructions - it has no assets, and its `scripts/`
and `tests/` exist only to check the bundle's own integrity, not to do the routing
itself (that's `SKILL.md`, read by the agent). From the skill directory (pure
Python standard library, no external dependencies):

```bash
python3 scripts/validate_skill_bundle.py
python3 -m unittest discover -s tests -v
```

`validate_skill_bundle.py` also notes (informationally, not as an error) any
routed skill name with no matching sibling folder next to this one - that's
expected when you haven't installed every domain skill.

## Coverage and boundaries

The package covers triage only: matching a task's keywords/intent against `academic-papers` (reading/writing/formatting a scientific paper), `agile-development` (non-trivial software changes, scoping, review process), `deep-learning` (PyTorch engineering), `hep-analysis` (collider/particle-physics data, ROOT/PyROOT/RDataFrame, statistics), and `task-authoring` (writing a standalone task/ticket/spec document, a skill's canonical worked example, or an LLM prompt design/budget - not the implementation itself). It explicitly excludes unrelated senses of overlapping words (e.g. "root" as a Linux user or Android rooting).

It does not perform the underlying work itself - once it identifies a match, it hands off to that domain skill's own workflow. If none of the rules apply, it stays silent and out of the way.

All maintained instructions and metadata are in English. The skill can still answer a user in their requested language.

## Example prompts

"Summarize this paper's method and check whether the comparison baseline was fairly tuned." (routes to `academic-papers`)

"Add an endpoint that lets admins export a CSV of active users." (routes to `agile-development`)

"My loss goes to NaN after a few hundred steps." (routes to `deep-learning`)

"Write an RDataFrame selection for >=2 muons with pT>25 GeV." (routes to `hep-analysis`)

"Fix this bug in my PyTorch training loop." (routes to `deep-learning` primary, with `agile-development` for scoping/review)

"Generate a canonical `examples/` entry for the `hep-analysis` skill." (routes to `task-authoring`)

"Write a ticket for adding a CSV export endpoint that another engineer can pick up cold." (routes to `task-authoring`, not `agile-development` - the deliverable is a standalone spec document, not the implementation itself)
