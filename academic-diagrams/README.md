# Academic Diagrams Skill

A portable Agent Skill maintained entirely in English. Its core is `SKILL.md` plus references, templates, and worked examples resolved through relative paths. It requires no specific MCP server, cloud account, or paid service (Graphviz, a Mermaid renderer, and a LaTeX installation are optional, only for rendering your own diagrams). It turns scientific ideas, Methods sections, algorithms, code, and rough sketches into publication-oriented, editable diagram sources - it builds the scientific model of the figure first and renders it second. It is not a drawing GUI and does not render images by itself.

## Installation and invocation

Extract the archive and keep the complete `academic-diagrams/` folder.

- **Codex:** place the folder in the skill directory used by your environment, commonly `~/.codex/skills/`, or import it through the mechanism supported by your version. Reload skills and invoke `$academic-diagrams`. `agents/openai.yaml` supplies optional Codex UI metadata.
- **Claude Code:** copy it to `.claude/skills/academic-diagrams/` in the project or `~/.claude/skills/academic-diagrams/` for personal use. Invoke `/academic-diagrams` or describe a matching task ("draw the analysis pipeline", "plate notation for this model"). See the [official Claude Code skill documentation](https://code.claude.com/docs/en/skills).
- **Antigravity:** copy it to `.agents/skills/academic-diagrams/` in the workspace (or `~/.gemini/config/skills/academic-diagrams/` for a global install; older installs may still read `.agent/skills/`). It triggers automatically - the agent reads every installed skill's `name`/`description` at session start and loads the full `SKILL.md` when a task matches. See the [Antigravity skills documentation](https://antigravity.google/docs/skills).
- **Other agents:** instruct the agent to read `SKILL.md` first and follow its reference routing. Provide the file location explicitly if automatic discovery is unsupported.

This delivery creates a single folder; it does not change other global agent settings. Load references selectively instead of pasting the entire package into global instructions. It complements `academic-papers` (scientific narrative, figure/table policy), `hep-analysis` / `ams-analysis` (physics content), and `deep-learning` (PyTorch code) when those are installed, but works without them.

## Quick checks

From the skill directory (pure Python standard library; Graphviz `dot` is used if present):

```bash
python3 -m unittest discover -s tests -v
python3 scripts/validate_skill_bundle.py
python3 scripts/check_diagram_sources.py            # whole bundle
python3 scripts/check_diagram_sources.py my_figure.md
```

`validate_skill_bundle.py` checks that every shipped file is present and non-empty, that `SKILL.md` has frontmatter whose `name` matches the folder, that its relative links resolve, that each `examples/` subdirectory is populated, and that `README.md` has its expected sections. `check_diagram_sources.py` compiles every fenced ```dot block with Graphviz (skipped with a notice if `dot` is missing), renders every ```mermaid block with Mermaid CLI `mmdc` when it is installed (otherwise only a cheap structural lint, which is not a Mermaid parser), and checks that ```svg blocks are well-formed XML; it never compiles TikZ or PlantUML. Use it on your own markdown notes too.

## Coverage and boundaries

`SKILL.md` carries the workflow (context -> purpose -> extract Known/Inferred/Assumed -> edge semantics -> diagram family -> abstraction -> logical graph -> validate -> layout -> render -> caption), the diagram-selection table, output-format guidance (Mermaid, Graphviz DOT, PlantUML, TikZ/tikz-feynman, SVG spec, ASCII), the ask-vs-assume rules, and the shared `figure_style` spec. References hold the detail: general principles (edge semantics, abstraction levels, decomposition, refactoring, type transformations), figure style (typography, grayscale/colorblind-safe color, column widths), the three domain specializations with their validation checklists (HEP: analysis pipelines, MC chain, detector schematics, decay trees vs Feynman diagrams, regions and likelihood; statistics: graphical models and plates, Bayesian/frequentist workflows, MCMC, causal DAGs; computer science: software, agentic, RAG, ML, model, distributed, database architectures), per-format syntax patterns and pitfalls, and captions. `templates/` gives nine starting skeletons and `examples/` carries 32 worked examples (7 general, 8 HEP, 7 statistics, 10 computer science).

Boundaries: it does not produce engineering-accurate detector drawings without supplied geometry, invent interactions for a Feynman diagram, or infer causal edges from correlation; it does not draw quantitative data plots (histograms, spectra, ROC curves - use `hep-analysis`/`academic-papers`); and its Mermaid, DOT, SVG, and TikZ examples were rendered or compiled and inspected, but the PlantUML examples and the LuaLaTeX automatic-layout Feynman variant were not, so compile and inspect before publishing. Exact figure widths and required fonts come from the target venue's author kit, not from this skill.

All maintained instructions, templates, and metadata are in English. The skill can still answer a user in their requested language.

## Example prompts

"Turn this Methods section into a publication-quality analysis workflow."

"Draw the event-processing pipeline for an LHC-style analysis."

"Create a diagram showing signal regions, control regions, and a simultaneous likelihood fit."

"Turn this Bayesian hierarchical model into plate notation."

"Create a causal DAG from these stated assumptions."

"Convert this MCMC algorithm into a flowchart."

"Inspect this repository and draw its software architecture."

"Create a Mermaid overview and a TikZ publication version of this scientific workflow."
