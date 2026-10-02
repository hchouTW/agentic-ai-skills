# Agentic AI Skills

Portable [Agent Skills](https://code.claude.com/docs/en/skills) for Claude Code, Codex,
[Antigravity](https://antigravity.google/docs/skills), and other skill-aware agents. Each
skill is a self-contained folder built around a `SKILL.md`, with references, scripts, and
templates resolved through relative paths. None needs an MCP server, cloud account, or paid
service.

## Skills

| Skill | Use it for |
|---|---|
| [`agile-development`](agile-development/) | Turning a software change into a small, verified, reviewable increment: scoping, acceptance criteria, validation plans, code and PR review, incident response, architecture decisions, estimation. Also implementation discipline (ask vs. assume, minimum code, surgical diffs). |
| [`task-authoring`](task-authoring/) | Turning a short request into an implementation-ready Task Markdown document that another person or agent can pick up without the original conversation. Also worked-example authoring and LLM prompt/token budgeting. |
| [`deep-learning`](deep-learning/) | PyTorch engineering: models, training loops, mixed precision, DDP/FSDP, debugging NaNs and shapes, export. Also ML decisions: scaling, parallelism, ablations, data splits, evaluation, serving. |
| [`hep-analysis`](hep-analysis/) | Collider and astroparticle analysis: ROOT, uproot, RDataFrame, cutflows, fits, limits, unfolding, systematics, detector and reconstruction physics, cosmic-ray flux. |
| [`ams-analysis`](ams-analysis/) | AMS-02 detector response and charged cosmic-ray analyses, traced to public AMS literature, with careful handling of unpublished results. |
| [`academic-papers`](academic-papers/) | Reading and critiquing papers, literature reviews, drafting and formatting manuscripts for physics and ML venues, bibliographies, referee responses. |
| [`academic-diagrams`](academic-diagrams/) | Publication-quality diagrams as editable sources (Mermaid, DOT, PlantUML, TikZ, SVG) with captions, including HEP, statistics, and computer-science figures. |

Skills defer to each other where their domains meet (for example `ams-analysis` sends
generic ROOT and statistics questions to `hep-analysis`), but each works on its own.

## Installation

Copy the skill folders you want into your agent's skill directory:

```bash
SKILLS="academic-diagrams academic-papers agile-development ams-analysis deep-learning hep-analysis task-authoring"

cp -r $SKILLS ~/.claude/skills/            # Claude Code (personal)
cp -r $SKILLS .claude/skills/              # Claude Code (project)
cp -r $SKILLS ~/.codex/skills/             # Codex
cp -r $SKILLS .agents/skills/              # Antigravity (workspace; older installs read .agent/skills/)
cp -r $SKILLS ~/.gemini/config/skills/     # Antigravity (global)
```

Keep each folder whole. Each skill's own `README.md` has its per-agent invocation details.

## Verifying a skill bundle

Every skill ships an integrity checker and unit tests (Python standard library only):

```bash
cd <skill-folder>
python3 scripts/validate_skill_bundle.py
python3 -m unittest discover -s tests -v
```

See each skill's `VALIDATION.md` for what is checked and how it was evaluated.

## Worked examples

`academic-diagrams` and `task-authoring` ship an `examples/` directory, each with its own
index (`examples/README.md`). `task-authoring` also holds the tooling to author and validate
new examples for any installed skill; see its `README.md` for the commands.
