# TODO for future Claude sessions (academic-diagrams)

State at 2026-09-21: skill merged to `main` (PR #5). Tests and validators pass. Read `VALIDATION.md`
"Not verified" first. Work on a branch, run `python3 -m unittest discover -s tests` and
`python3 scripts/validate_skill_bundle.py` before committing, and ask before pushing or merging.

## P1 - close known verification gaps
- [x] Render every ```mermaid block with `mmdc` (done: all pass; checker calls `mmdc` when present, test added).
      Still open: eyeball the rendered SVGs for layout quality.
- [ ] Compile the TikZ / tikz-feynman snippets (`references/tikz-patterns.md`, `examples/hep/07`,
      `examples/statistics/02`) with LuaLaTeX/pdfLaTeX; fix the `calc` library note and any layout bugs.
      Requires a TeX install (none on this machine as of 2026-09-21).
- [ ] Run the 10 prompts in `~/Downloads/task_academic_diagrams_skill.md` section 33 against the skill in fresh
      sessions, record pass/fail and gaps in `VALIDATION.md` (currently checked by design review only).
- [ ] Check column widths and font sizes in `references/academic-figure-style.md` against current APS/JHEP/NeurIPS/ICML author kits.

## P2 - content the task asked for but is thin or missing (done 2026-09-21)
- [x] LHC pipeline example `examples/hep/08` (DOT + Mermaid + TikZ + two-lane variant).
- [x] Repository-inspection example (`general/05`) and Methods -> workflow with Known/Inferred/Assumed (`general/06`).
- [x] PlantUML reference and one component + one sequence example (`computer-science/09-10`); **not compiled** - needs a JRE.
- [x] SVG-spec template and worked example (`templates/svg-spec.md`, `general/07`); rendered and inspected.
- [x] `templates/ml-pipeline.md` and `templates/bayesian-model.md`.
- [x] Sketch-to-spec (`general-diagram-principles.md` section 11).
- [ ] Follow-up: compile the PlantUML sources (install a JRE) and the `hep/08` TikZ (install TeX); tidy the plate label overlap in the Bayesian-model DOT.

## P3 - stretch goals from the task (section 34)
- [ ] Multi-panel figures, poster diagrams, thesis figures, Beamer overlays, talk simplification, equation placement,
      automatic legend generation, symbol-table linking to the paper, SVG/PDF export recipes.
- [ ] Add a `--legend` helper or a legend snippet per format.

## P4 - integration and decisions
- [ ] Add pointers from `academic-papers/references/figures-and-tables.md` and `hep-analysis` to `academic-diagrams`
      (and the reverse); keep `skill-router` tests passing.
- [ ] Decide with the user whether this skill should also carry the repo's "24 examples across 8 archetypes" set
      (`task-authoring/references/example-authoring.md`). It was skipped in favour of the task's own example list.
- [ ] Update the repo memory/README skill counts if more skills are added.
