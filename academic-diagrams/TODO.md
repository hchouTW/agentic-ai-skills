# TODO for future Claude sessions (academic-diagrams)

State at 2026-09-21: skill merged to `main` (PR #5). Tests and validators pass. Read `VALIDATION.md`
"Not verified" first. Work on a branch, run `python3 -m unittest discover -s tests` and
`python3 scripts/validate_skill_bundle.py` before committing, and ask before pushing or merging.

## P1 - close known verification gaps
- [x] Render every ```mermaid block with `mmdc` (done: all pass; checker calls `mmdc` when present, test added).
      Layout reviewed (2 fixes); see `VALIDATION.md`.
- [x] Compile the TikZ / tikz-feynman snippets: done with Tectonic (found `tectonic` in miniconda). Fixed the Feynman auto-layout trap
      (manual placement now leads); `calc` requirement confirmed. Still open: verify the `\feynmandiagram` LuaLaTeX variant (needs LuaTeX).
- [x] Ran the 10 prompts (fresh subagent per prompt); results and the 2 skill fixes it produced are in `VALIDATION.md`.
      Second sample with Haiku on 4 prompts found 3 more fixes. Still open: more samples per prompt, and a larger model (Opus).
- [x] Checked column widths against ICML 2026, NeurIPS 2026, JHEP `jheppub`, APS RMP guide; fixed the ICML row.
      APS single column and ICLR now checked (APS states no full-width number). Still open: font-size rules for JHEP/NeurIPS/ICLR.

## P2 - content the task asked for but is thin or missing (done 2026-09-21)
- [x] LHC pipeline example `examples/hep/08` (DOT + Mermaid + TikZ + two-lane variant).
- [x] Repository-inspection example (`general/05`) and Methods -> workflow with Known/Inferred/Assumed (`general/06`).
- [x] PlantUML reference and one component + one sequence example (`computer-science/09-10`); **not compiled** - `java` is only a stub here.
- [x] SVG-spec template and worked example (`templates/svg-spec.md`, `general/07`); rendered and inspected.
- [x] `templates/ml-pipeline.md` and `templates/bayesian-model.md`.
- [x] Sketch-to-spec (`general-diagram-principles.md` section 11).
- [ ] Follow-up: compile the PlantUML sources (needs a JRE); tidy the plate label overlap in the Bayesian-model DOT. (`hep/08` TikZ is done.)

## P3 - stretch goals from the task (section 34) (done 2026-09-21)
- [x] Multi-panel, poster, thesis, Beamer overlays, talk simplification, equation placement, symbol table, export recipes
      -> `references/legends-panels-and-export.md` (Graphviz/`rsvg-convert`/`mmdc` export rows run; TikZ/Beamer/`dvisvgm` not).
- [x] Legend snippet per format (Mermaid, Graphviz, TikZ, SVG) in the same reference. A `--legend` script helper was not added:
      a legend must reflect the styles a specific figure uses, which a text template cannot know.

## P4 - integration and decisions
- [x] Pointers from `academic-papers/references/figures-and-tables.md` and `hep-analysis/SKILL.md` to `academic-diagrams`
      (reverse pointers already existed); `skill-router`, `academic-papers`, `hep-analysis` validators and tests pass.
- [ ] Decide with the user whether this skill should also carry the repo's "24 examples across 8 archetypes" set
      (`task-authoring/references/example-authoring.md`). It was skipped in favour of the task's own example list.
- [x] Skill counts: no new skills were added, so nothing to update.
