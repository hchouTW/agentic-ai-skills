# Package Validation Record

Validation date: 2026-09-21. Helper test environment: Python 3, standard library only; Graphviz `dot` present, no LaTeX (Mermaid CLI available through npx).

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

## Mermaid rendering (2026-09-21, follow-up)

All 37 `dot`/`mermaid` blocks in the bundle pass `scripts/check_diagram_sources.py` with Mermaid CLI
(`@mermaid-js/mermaid-cli` via `npx`, exposed as `mmdc`) rendering every Mermaid block to SVG; no
source needed fixing. The script now calls `mmdc` when it is on PATH and keeps the structural lint
as the fallback and as a pre-filter. Checked that a syntax error the lint misses is caught by `mmdc`.
Rendered output was not visually inspected, only that it parsed and rendered without error.

## P2 content additions (2026-09-21, follow-up)

Added: examples `general/05-07`, `hep/08`, `computer-science/09-10`; templates `svg-spec`, `ml-pipeline`,
`bayesian-model`; `references/plantuml-patterns.md`; sketch-to-spec section 11 in
`references/general-diagram-principles.md`. The checker now also parses fenced `svg` blocks as XML.
Full-bundle run: 47 `dot`/`mermaid`/`svg` blocks, 0 problems (Mermaid rendered with `mmdc`, DOT with `dot`).
The SVG example was rasterized with `rsvg-convert` and inspected; that found two real defects (test set with no
outgoing edge, clipped footnote), both fixed. The Bayesian-model DOT was rendered and inspected (plate label
sits close to an edge). `general/05` was drawn from files actually read in this repository.
TikZ in `hep/08` and both PlantUML examples were **not** compiled (no TeX, and `java` is only a stub here).

## P3/P4 additions (2026-09-21, follow-up)

`references/legends-panels-and-export.md` (its Mermaid and DOT legend snippets pass the checker; export commands for
Graphviz, `rsvg-convert`, and `mmdc` were run; TikZ/Beamer/`dvisvgm` snippets were not compiled). Cross-links added in
`academic-papers/references/figures-and-tables.md` and `hep-analysis/SKILL.md`; those skills' validators and tests pass.

## Fresh-session prompt run and TeX/venue checks (2026-09-21, follow-up)

**Ten prompts, ten fresh subagents** (Sonnet), each given only `SKILL.md`'s path, one small concrete input where the
prompt says "this ...", and no grading criteria. Outputs were graded afterwards by reading them and rendering the sources.

| # | Prompt | Result | Gap found |
|---|---|---|---|
| 1 | Methods -> workflow | pass: Known/Inferred table, flagged the ambiguous "Z+jets" background and the missing signal model instead of guessing | - |
| 2 | LHC pipeline | pass: data/simulation merge only at reconstruction, conceptual-diagram assumption stated | - |
| 3 | SR/CR + simultaneous fit | pass: shared parameters, VR outside the fit, blinding noted | invented CR1/CR2/VR with a stated assumption (allowed for a generic pipeline) |
| 4 | Hierarchical model -> plates | pass: factorization matches graph, fixed vs latent distinguished | - |
| 5 | Causal DAG | pass: no edges beyond the stated ones; noted the strong no-direct-effect claim; identification notes correct | added front-door discussion the user did not ask for |
| 6 | MCMC -> flowchart | pass: loops and stopping criterion, flagged the missing max-iteration guard | used `\n` in a label; `<br/>` guidance was missing from `mermaid-patterns.md` (both render in `mmdc`) - added |
| 7 | Repo -> architecture | **partial**: read the files and separated Known/Inferred, but node labels carried wrong counts ("33 topic files", "24 examples", "3 sections" vs 31, 25, 14) | numbers in labels were not measured - rule added to `SKILL.md` and `templates/system-architecture.md` |
| 8 | Multi-agent system | pass: data vs control edges, no invented orchestrator, open questions listed | - |
| 9 | Transformer code -> figure | pass: pre-norm order, tied weights, causal mask, dropout locations all match the code | - |
| 10 | Mermaid overview + TikZ | pass: TikZ compiled with Tectonic (independently re-compiled here, layout inspected) | - |

All ten outputs said honestly whether they had rendered anything. The agents could not render Mermaid (`mmdc` was not on their PATH), so all ten
outputs were run through `check_diagram_sources.py` afterwards: 10 blocks (8 DOT compiled, 2 Mermaid rendered with `mmdc`), 0 problems.
DOT layouts were not inspected visually except where noted.

**TeX.** `tectonic` (XeTeX-based) is installed under miniconda, so the earlier "no TeX" note was wrong. Compiled and inspected:
`hep/08`, `statistics/02` (needs `calc`: confirmed, fails without it), `tikz-patterns.md` plate and pipeline snippets, the legend `matrix`,
the Beamer overlay snippet (3 pages), and a manual-placement tikz-feynman diagram. **Important finding:** the shipped `\feynmandiagram`
automatic-layout examples "compile" under XeTeX but ignore the layout keys (LuaTeX only) and draw a garbled figure; a clean compile
is not evidence of a correct figure. `hep/07` and `tikz-patterns.md` now lead with the manual-placement version (checked orientation
of incoming/outgoing fermion arrows) and keep the auto-layout one with a warning. LuaLaTeX itself is not installed, so that variant is unverified.

**Venue widths** (`references/academic-figure-style.md`, checked against sources, not just the doc's earlier defaults): ICML 2026 (6.75 in
overall, 0.25 in gutter, so 3.25 in = 8.26 cm per column; the earlier "~8.5 cm" was slightly off and the row conflated ICML with NeurIPS),
NeurIPS 2026 (5.5 in), JHEP `jheppub` (15.5 cm on a4paper). APS single column (8.6 cm) comes from the RMP style guide; the REVTeX 4.2
guide itself states no figure widths, and 17.8 cm for a full-width figure is still an unverified default.

## Not verified

- All PlantUML sources (no working Java runtime), the LuaLaTeX automatic-layout Feynman variants (no LuaTeX), the
  `subcaption` `figure*` snippet, and `dvisvgm` export were not run.
- APS full-width figure size (17.8 cm) and ICLR width are unverified defaults; ICML/NeurIPS/JHEP/APS-single-column were checked (see above).
- The prompt run used one fresh agent per prompt and one sample each; it shows the skill can be followed, not how often it succeeds. The table
  below records which file supplies each capability.

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
