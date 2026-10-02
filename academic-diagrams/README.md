# Academic Diagrams Skill

Turns Methods sections, algorithms, code, and rough sketches into editable diagram sources (Mermaid, Graphviz DOT, PlantUML, TikZ, SVG) for papers, theses, posters, and talks, with a caption and validation notes. It builds the scientific model of the figure first and renders second. It is not a drawing GUI, does not render images by itself, and is not for data plots. It needs no MCP server, cloud account, or paid service; Graphviz, a Mermaid renderer, and LaTeX are optional, only for rendering your own diagrams.

All maintained instructions, templates, and metadata are in English. The skill can still answer in the language you use.

## Installation and invocation

Keep the complete `academic-diagrams/` folder; all links are relative.

- **Codex:** copy it to `~/.codex/skills/` (or the skill directory your version uses), reload skills, and invoke `$academic-diagrams`. `agents/openai.yaml` supplies optional Codex UI metadata.
- **Claude Code:** copy it to `.claude/skills/academic-diagrams/` in a project or `~/.claude/skills/academic-diagrams/` for personal use. Invoke `/academic-diagrams` or describe a matching task. See the [official Claude Code skill documentation](https://code.claude.com/docs/en/skills).
- **Antigravity:** copy it to `.agents/skills/academic-diagrams/` in the workspace or `~/.gemini/config/skills/academic-diagrams/` globally (older installs may read `.agent/skills/`). It triggers automatically from the `name`/`description`. See the [Antigravity skills documentation](https://antigravity.google/docs/skills).
- **Other agents:** tell the agent to read `SKILL.md` first and follow its reference routing.

## Quick checks

From the skill directory (Python standard library only):

```bash
python3 scripts/validate_skill_bundle.py
python3 -m unittest discover -s tests
python3 scripts/check_diagram_sources.py            # whole bundle
python3 scripts/check_diagram_sources.py my_figure.md
```

- `validate_skill_bundle.py`: shipped files exist, `SKILL.md` frontmatter matches the folder name, relative links resolve, each `examples/` subfolder is populated, and this README has its required sections.
- `check_diagram_sources.py`: checks fenced `dot`, `mermaid`, `plantuml`, and `svg` blocks in markdown. It uses `dot`, `mmdc`, and `plantuml` when installed and skips with a notice otherwise; without `mmdc` Mermaid gets only a structural lint. It never compiles TikZ.
- Routing and quality prompts live in `tests/prompts.md`; `tests/run_prompts.py` runs them against a model. Results are in `VALIDATION.md`, open items in `TODO.md`.

## Coverage and boundaries

Covers:

- Research and analysis workflows, algorithm flowcharts, system, agent, RAG, and ML architectures, data-flow and sequence diagrams.
- HEP: analysis pipelines, Monte Carlo chains, detector schematics, decay trees, Feynman diagrams, regions and likelihoods.
- Statistics: plate notation, causal DAGs, Bayesian and frequentist workflows, MCMC.
- Converting Mermaid, DOT, or PlantUML to publication-quality SVG, PDF, or TikZ; simplifying and reviewing existing figures.
- Bundled content: 11 reference files, 9 templates, 32 worked examples (7 general, 8 HEP, 7 statistics, 10 computer science).

Defers or declines:

- Data plots (histograms, spectra, ROC curves): use `hep-analysis` or `academic-papers`.
- Figure and table policy, narrative: `academic-papers`. Physics content: `hep-analysis`, `ams-analysis`. PyTorch code: `deep-learning`.
- No engineering-accurate detector drawings without supplied geometry, no invented Feynman interactions, no causal edges inferred from correlation.
- Exact widths and fonts come from the venue author kit. Compile and inspect your own edits before publishing.

## Example prompts

- "Turn this Methods section into a publication-quality analysis workflow."
- "Draw the event-processing pipeline for an LHC-style analysis."
- "Show signal regions, control regions, and a simultaneous likelihood fit."
- "Turn this Bayesian hierarchical model into plate notation."
- "Create a causal DAG from these stated assumptions."
- "Convert this MCMC algorithm into a flowchart."
- "Inspect this repository and draw its software architecture."
- "Make a Mermaid overview and a TikZ publication version of this workflow."
