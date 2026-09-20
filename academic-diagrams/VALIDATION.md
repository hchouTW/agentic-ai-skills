# Package Validation Record

Validation date: 2026-09-21. Helper test environment: Python 3, standard library only; Graphviz `dot` present, no Mermaid renderer, no LaTeX.

## Initial build (2026-09-21)

First delivery of `academic-diagrams`, implementing `~/Downloads/task_academic_diagrams_skill.md`
as a bundle matching this repository's sibling-skill convention (`SKILL.md`, `README.md`,
`VALIDATION.md`, `references/`, `templates/`, `examples/`, `scripts/`, `tests/`, `agents/openai.yaml`).

- Structure follows the task's deliverable tree (9 references, 6 templates, examples in `hep/`,
  `statistics/`, `computer-science/`). One improvement: an added `examples/general/` directory for
  the task's four "General Academic" examples. The task's 24-example-per-archetype repository
  convention was not applied; the task's own example list was used instead.
- `scripts/validate_skill_bundle.py`: file presence/non-empty, frontmatter with `name == folder`,
  SKILL.md relative links resolve, examples directories populated, README sections.
- `scripts/check_diagram_sources.py`: compiles fenced `dot` blocks with Graphviz and lints
  `mermaid` blocks (structural only). It was run over the whole bundle after fixing false positives
  (Mermaid async `--)` arrows, ER crow's-foot tokens) and reclassifying two non-standalone DOT
  fragments in `references/graphviz-patterns.md` as `text`.
- `tests/test_academic_diagrams_skill.py`: helper unit tests plus end-to-end runs of both scripts
  against the shipped bundle and a structural check that every example has a type line, source,
  and caption.

## Not verified

- Mermaid sources were only linted structurally; none were rendered by Mermaid.
- TikZ / tikz-feynman snippets were not compiled (no LaTeX installation); the hierarchical-model
  plate example additionally needs the `calc` library (stated in the example).
- Column widths and venue specifics in `references/academic-figure-style.md` are common defaults, not checked
  against current author kits.
- The behavior on the ten final-validation prompts in the task (section 33) was checked by design review
  against the workflow and references, not by running a model against them. The rows below record which
  file supplies each capability.

| Prompt | Supplied by |
|---|---|
| Methods section -> analysis workflow | SKILL.md workflow; `templates/research-workflow.md`; `examples/general/02` |
| LHC-style event-processing pipeline | `references/high-energy-physics.md`; `examples/hep/01` |
| SR/CR + simultaneous fit | `examples/hep/06`; HEP validation checklist |
| Hierarchical Bayesian model -> plates | `references/probability-statistics.md`; `examples/statistics/02` |
| Causal DAG from stated assumptions | `examples/statistics/03`; causal rules in the statistics reference |
| MCMC -> flowchart | `templates/algorithm-flowchart.md`; `examples/statistics/04` |
| Repository -> architecture | SKILL.md "read source files first"; `templates/system-architecture.md` |
| Multi-agent research system | `templates/agentic-ai-architecture.md`; `examples/computer-science/04` |
| Transformer implementation -> figure | `references/computer-science.md` section 6; `examples/computer-science/02` |
| Mermaid overview + TikZ version | multiple-representation guidance in SKILL.md; `references/mermaid-patterns.md`, `references/tikz-patterns.md` |
