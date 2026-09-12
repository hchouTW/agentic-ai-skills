# Task Authoring Skill

A portable Agent Skill maintained entirely in English. Its core is `SKILL.md` plus a template and references resolved through relative paths. It requires no specific MCP server, cloud account, or paid service. It turns a short natural-language request into an implementation-ready Task Markdown document by reading the applicable authoring reference, inspecting the target repository, and classifying every claim as Confirmed, Inferred, or Unresolved - it is not a project-management tool, a ticketing-system integration, or a substitute for human review of ambiguous product decisions.

## Installation and invocation

Extract the archive and keep the complete `task-authoring/` folder.

- **Codex:** place the folder in the skill directory used by your environment, commonly `~/.codex/skills/`, or import it through the mechanism supported by your version. Reload skills and invoke `$task-authoring`. `agents/openai.yaml` supplies optional Codex UI metadata. See [references/adapters/codex.md](references/adapters/codex.md).
- **Claude Code:** copy it to `.claude/skills/task-authoring/` in the project or `~/.claude/skills/task-authoring/` for personal use. Invoke `/task-authoring` or describe a matching task ("create a task for...", "write a task/ticket for..."). See [references/adapters/claude-code.md](references/adapters/claude-code.md) and the [official Claude Code skill documentation](https://code.claude.com/docs/en/skills).
- **Antigravity:** copy it to `.agents/skills/task-authoring/` in the workspace (or `~/.gemini/config/skills/task-authoring/` for a global install; older installs may still read `.agent/skills/`). It triggers automatically - the agent reads every installed skill's `name`/`description` at session start and loads the full `SKILL.md` when a task matches, no explicit invocation needed. See [references/adapters/antigravity.md](references/adapters/antigravity.md) and the [Antigravity skills documentation](https://antigravity.google/docs/skills).
- **Other agents:** instruct the agent to read `SKILL.md` first and follow its reference routing. Provide the file location explicitly if automatic discovery is unsupported. See [references/adapters/generic-agent.md](references/adapters/generic-agent.md).

This delivery creates a single folder; it does not change other global agent settings. Load references selectively instead of pasting the entire package into global instructions.

## Quick checks

From the skill directory (pure Python standard library, no external dependencies):

```bash
python3 -m unittest discover -s tests -v
python3 scripts/validate_skill_bundle.py
python3 scripts/generate_skill_example.py --archetype contrast --skill agile-development --role "Staff Software Engineer" --use-case "scoping a bug fix"
python3 scripts/generate_skill_example.py --archetype trajectory --skill agile-development --role "Senior Software Engineer" --problem-input "a raw bug report"
python3 scripts/generate_skill_example.py --archetype gated-pipeline --skill agile-development --role "Principal Software Engineer" --high-stakes-task "a feature-flagged rollout RFC"
python3 scripts/generate_skill_example.py --archetype decision-tree --skill agile-development --role "Engineering Lead" --scenario "an ambiguous incident page"
python3 scripts/generate_skill_example.py --archetype elicitation --skill agile-development --role "Staff Software Engineer" --user-request "can you make the checkout faster?"
python3 scripts/generate_skill_example.py --archetype adversarial-audit --skill agile-development --role "Lead Auditor" --candidate-artifact "a training writeup claiming SOTA accuracy"
python3 scripts/generate_skill_example.py --archetype test-first --skill agile-development --role "Staff Software Engineer" --target "a DataLoader throughput invariant"
python3 scripts/generate_skill_example.py --archetype postmortem --skill agile-development --role "Site Reliability Engineer" --incident "a production API outage after a bad deploy"
python3 scripts/validate_skill_example.py ../agile-development/examples/01-bug-fix-scoping-review.md
```

`validate_skill_bundle.py` checks that every file this package ships is present and non-empty, that `SKILL.md` has YAML frontmatter with `name`/`description`, that `README.md` has its expected section headers, and that `templates/task-template.md` carries exactly the section contract named in `AI_Agent_Agnostic_Task_Authoring_Workflow.md`'s "Task Generation Requirements" - one top-level title followed by Background, Objective, Scope (In Scope/Out of Scope), Repository Context, Technical Approach, Deliverables, Acceptance Criteria, Validation, Open Questions, and References, in that exact order, no more and no fewer.

`generate_skill_example.py` scaffolds an empty `<skill>/examples/*.md` skeleton without inventing content, for one of eight archetypes selected with `--archetype {contrast,trajectory,gated-pipeline,decision-tree,elicitation,adversarial-audit,test-first,postmortem}`: each emits its own fixed section headers plus a matching frontmatter scenario flag (`--use-case` / `--problem-input` / `--high-stakes-task` / `--scenario` / `--user-request` / `--candidate-artifact` / `--target` / `--incident`); `--takeaways` (3-6, default 4) is valid only with `--archetype contrast`. `validate_skill_example.py` reads the `archetype:` frontmatter field to pick that archetype's rule set (a file with no `archetype:` field is treated as `contrast`, for backward compatibility) and checks required sections in order, archetype-specific structure (a 3-6 item Key Takeaways list for Contrast, fenced code blocks in Trajectory's Surgical Execution/Verification Evidence sections, `**Gate:**` lines in every Gated Pipeline phase, a >=3-row Triage Matrix table for Decision-Tree, 3-4 lettered multiple-choice questions for Elicitation, >=2 labeled attack vectors plus literal fenced artifacts for Adversarial Audit, a raw failure block plus a passing block with a numeric metric for Test-First, and exactly 5 non-"human error" Why-steps plus a fenced diff and a concrete monitoring rule for Postmortem), and zero placeholder markers. `check_example_diversity.py` is retained for reference but historical - it enforced an earlier, narrower rule (one example per skill, no skill repeated) that no longer applies now every skill carries all eight archetypes; it is not run as part of authoring a new batch. See `references/example-authoring.md` for all eight generation prompts, the archetype-selection guide, the actor-stance conventions, the diversity rule, and the format spec.

## Coverage and boundaries

The package governs *how to write the task*, not *how to implement it*: understanding user intent, identifying and reading the applicable authoring reference, inspecting the target repository, and building a Confirmed/Inferred/Unresolved evidence model before drafting - see `SKILL.md`'s Core Workflow and its 13-point Generic Agent Instruction. `references/acceptance-criteria.md` covers what makes a criterion verifiable rather than vague, `references/task-quality-checklist.md` is the final gate before writing the task, and `references/adapters/` holds discovery-only notes per agent environment (Claude Code, Codex, Antigravity, and any other repository-aware agent) - none of them restate the Core Workflow, the evidence model, or the template's section contract.

`templates/task-template.md` defines the exact structural contract for the generated document. `examples/` carries one worked task per category named in the source authoring document - feature, bug, performance, and research - each grounded in this repository's own, actually-verified state, and each with a non-trivial Open Questions section demonstrating that an unresolved detail is marked, not invented.

It also covers authoring a canonical worked example for this or another skill's `examples/` directory, in any of eight archetypes - Contrast (Weak vs. Expert plus key takeaways), Execution Trajectory (step-by-step task resolution), Gated Pipeline (multi-phase build with explicit acceptance gates), Decision-Tree (branching triage matrix plus end-to-end execution script), Interactive Elicitation (Socratic clarification of a vague request into a final spec), Adversarial Audit (ruthlessly attacking a candidate artifact to find and patch real failure modes), Test-First / Red-to-Green (a failing test through a minimal fix to a verified, metric-backed pass), or Incident Postmortem (alert through blameless 5-Whys RCA to a permanent fix and a concrete monitoring rule) - see `references/example-authoring.md` for the archetype-selection guide, the actor-stance conventions, the diversity rule, and the `generate_skill_example.py`/`validate_skill_example.py` scripts above.

It also covers prompt engineering and token optimization for LLM-facing work - role framing, few-shot/chain-of-thought examples, structured-output contracts, and guardrails on the design side; token budgets, context-window hygiene, and cheapest-adequate model-tier selection on the cost side - see `references/prompt-engineering-and-token-optimization.md`. That reference's two optional story-card fields (prompt directive, token budget) extend `agile-development`'s `assets/story-card.md` and require that skill installed alongside this one.

It does not build a new LLM, a vendor-specific API integration, or a full autonomous development agent; it does not enumerate every possible engineering task type; and it does not replace human review for ambiguous product or domain decisions. Once a task is generated and handed off for implementation, pair it with `agile-development` (or a domain skill) for the implementation itself.

All maintained instructions, templates, and metadata are in English. The skill can still answer a user in their requested language.

## Example prompts

"Create a task for RICH reconstruction performance analysis."

"Write a task for adding a CSV export endpoint for admins."

"Turn this bug report into an implementation-ready task doc."

"Generate a canonical `examples/` entry for the `hep-analysis` skill contrasting a weak vs. expert systematics writeup."

"Design a prompt template for a classification pipeline and give me a token budget."
