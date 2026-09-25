# Package Validation Record

Validation date: 2026-09-21 (follow-ups 2026-09-25). Helper test environment: Python 3, standard library only; Graphviz `dot` present, no LaTeX (Mermaid CLI available through npx).

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
| 7 | Repo -> architecture | **partial**: read the files and separated Known/Inferred, but a node label said "33 topic files" for a `references/` folder holding 31 (33 is the number of reference links in `SKILL.md`, two of them cross-skill); "24 examples" was correct | counted link mentions instead of files - rule added to `SKILL.md` and `templates/system-architecture.md` |
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
NeurIPS 2026 (5.5 in), JHEP `jheppub` (15.5 cm on a4paper - **wrong**, corrected to 15.1 cm on 2026-09-25, see below). APS single column (8.6 cm) comes from the RMP style guide; the REVTeX 4.2
guide itself states no figure widths, and 17.8 cm for a full-width figure is still an unverified default.

## Second sample with a different model (Haiku) (2026-09-21, follow-up)

Four prompts re-run in fresh Haiku subagents (1 Methods, 4 plates, 5 causal DAG, 7 repo). All four produced usable sources that compile.

| # | Result | Gap found -> fix |
|---|---|---|
| 4 | **fail on a scientific point**: drew mu and tau, which have priors, as bare fixed hyperparameters (its own notes listed the priors); invented "Figure 1." | `references/probability-statistics.md` said "hyperparameter: bare symbol"; `templates/bayesian-model.md` drew mu/tau plaintext. Fixed: a hyperparameter with a prior is a random variable (circle); only fixed constants are bare. Template re-rendered. |
| 5 | structure correct (6 edges, no invented ones); identification notes muddled ("both must be controlled" while G is unmeasured) | added "Identification claims on causal DAGs" to `references/probability-statistics.md` |
| 1 | usable, but invented "(parton shower + hadronization)" on the simulation box and did not flag the ambiguous "Z+jets" background that the Sonnet run caught | added the no-invented-details rule to `SKILL.md` |
| 7 | repeated the "33 references" miscount and wrote "verified by file listing" without listing | rule sharpened: count the things, not mentions of them |

Takeaway: the same skill gives noticeably weaker scientific judgment with a smaller model; the fixes above target the reference text that misled it,
not the model. Still one sample per prompt per model.

## Layout review of all 37 Mermaid renders (2026-09-21)

Rendered every Mermaid block to PNG and reviewed them. Two defects in this bundle's own new examples were fixed: `general/06` (self-loop
label overlapped the test-set node; now a two-node tuning loop) and `general/05` (edge label collided with the router box; now dropped and stated in text).
The Bayesian-model DOT plate labels now sit at the bottom right (`labelloc=b`), clear of the edges. The other renders had no overlaps at this review depth.

## Tooling follow-ups: PlantUML, LuaLaTeX, venue rules (2026-09-25)

Tools installed into a throwaway scratch directory only: OpenJDK + PlantUML 1.2026.8 (conda-forge), and a minimal TeX Live 2026
(`install-tl` infra-only scheme + `luatex`, `latex-bin`, `tikz-feynman`, `standalone` and dependencies).

- **PlantUML.** All 6 PlantUML blocks (`computer-science/09`, `/10`, and 4 in `references/plantuml-patterns.md`) rendered to PNG and
  were inspected. One real defect: the class snippet `class Sample { +id : int  +energy : float }` is a syntax error (one-line member
  bodies are not accepted; PlantUML falls back to a sequence diagram and fails). Fixed (one member per line, `Track` declared) and a
  pitfall added. The fences were retagged from `text` to `plantuml`, and `check_diagram_sources.py` now renders them with `plantuml -pipe`
  when it is on PATH, wrapping fragments in `@startuml`/`@enduml` first (without the markers PlantUML outputs nothing and exits 0).
  Four new tests (fake binary, fragment wrapping, fence extraction, real binary rejects the one-line class body). Full run with
  `plantuml` on PATH: 55 blocks, 0 problems; 25 tests pass (the real-`mmdc` test skipped: `mmdc` not on PATH this time; no Mermaid source changed).
- **LuaLaTeX Feynman.** The `\feynmandiagram [horizontal=a to b]` auto-layout snippet compiled with LuaHBTeX 1.24 and was inspected:
  clean layout, correct arrow orientation on all four fermion lines, but `e^+` is placed on top and `e^-` below (the reverse of the
  manual version) - noted in the text. Under pdfLaTeX the same source exits 0 with a "LuaTeX is required" warning and draws a garbled
  figure, confirming the earlier XeTeX finding. The manual-placement version in `hep/07` compiled under LuaLaTeX and pdfLaTeX with an
  identical, correct layout. `[compat=1.1.0]` added to the `tikz-feynman` loading line (silences a per-run warning; render unchanged).
- **Bayesian-model DOT.** Re-rendered: plate labels are clear of the edges (the `labelloc=b` fix from 2026-09-21 holds). Also set
  `graph [fontname="Helvetica"]` so the plate labels no longer fall back to Times while the nodes use Helvetica.
- **Venue rules**, from the files themselves rather than summaries. ICLR 2026 (`iclr2026_conference.sty` from the official
  Master-Template repository; the 2027 file is identical): 5.5 in text width, 10 pt Times - now verified. NeurIPS 2026 (`neurips_2026.sty`
  and `neurips_2026.tex`): 5.5 in, 10 pt, Type 1/embedded TrueType fonts only. JHEP: compiling `jheppub.sty` v1.1227 with `11pt,a4paper`
  gives `\textwidth` = 430.2 pt = **15.1 cm**, not 15.5 cm (the style sets `.72\paperwidth`); the earlier "float wider than 60% of the
  text width is centered" was a misreading of `\bottomfraction{.6}` and was removed. Figure rules from the JHEP author manual (raster
  150-250 dpi, embedded fonts, no transparency layers, "figure 2" not "fig. 2") added. None of the three sets a minimum font size for
  text inside figures; that is now said explicitly.

## Not verified

- The `subcaption` `figure*` snippet and `dvisvgm` export were not run.
- APS full-width figure size (17.8 cm) is an unverified default; ICML/NeurIPS/ICLR/JHEP/APS-single-column were checked (see above).
- The PlantUML component diagram's automatic layout depends on the Graphviz version; the render was inspected with Graphviz from Homebrew only.
- The prompt run used one fresh agent per prompt and one sample each (Sonnet on 10, Haiku on 4; not yet Opus); it shows the skill can be followed, not how often it succeeds. The table
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
