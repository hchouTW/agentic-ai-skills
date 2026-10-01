# TODO for future Claude sessions (academic-diagrams)

State (2026-10-01, round 2 on branch `academic-diagrams-todo-round2`; skill via PR #5, tooling follow-ups via PR #22): `python3 scripts/validate_skill_bundle.py` OK (28 files); `python3 -m unittest discover -s tests` 27 tests OK. 2 tests skip when `mmdc` or `plantuml` is not on PATH. P1-P4 are done. Open: under-triggering on Haiku and a few Sonnet query types, and more behavioral samples. Read `VALIDATION.md` "Not verified" first, then this file.

Working rules:
- Work on a branch and ask before pushing or merging.
- Run `python3 -m unittest discover -s tests` and `python3 scripts/validate_skill_bundle.py` before committing.
- Record every result, including negative ones, in `VALIDATION.md`.
- A clean compile is not evidence of a correct figure: render and inspect it. The `\feynmandiagram` auto-layout compiles under XeTeX/pdfLaTeX but draws a garbled figure.

User decision (2026-09-25): no "24 examples across 8 archetypes" set for this skill. Keep the 32 diagram examples (`examples/{general,hep,statistics,computer-science}`).

## Environment and tooling (re-check, they may have changed)

- Graphviz `dot` and `rsvg-convert` are present.
- Mermaid CLI works through `npx` but is not always on PATH as `mmdc`.
- `tectonic` (XeTeX, miniconda) is the only system TeX engine.
- LuaLaTeX and PlantUML (with Java) are not installed system-wide; `java` is a stub. On 2026-09-25 they were installed into a throwaway scratch conda env plus a minimal `install-tl` (LuaLaTeX needs `LANG=en_US.UTF-8`).
- `scripts/check_diagram_sources.py` renders mermaid, dot and plantuml fences when the matching binary is on PATH. Its last full run with all tools: 55 blocks, 0 problems.
- Trigger runner: `../hep-analysis/tests/routing_eval.py --target academic-diagrams`, which grades routing to any owner.

## Open

- [x] **Description length (2026-10-01):** now 1014 characters; the validator enforces the 1024 limit (test added). `task-authoring` still has the problem (1274); its TODO is updated.
- [ ] **Under-triggering, round 2 (2026-10-01):** the description now names Mermaid-to-SVG and "schematic", and this skill has its own trigger sets (`tests/trigger_queries.json` for tuning, `tests/trigger_queries_holdout.json` kept for a final check). Measured: Sonnet 22/24 tuning and 14/20 holdout, Haiku 5/24 and 5/20, 0 false triggers. Both queries from the first eval now route on Sonnet; on Haiku the Mermaid-to-SVG query still goes to the built-in `dataviz`. Remaining Sonnet misses: causal-DAG review, PlantUML-to-PDF conversion, distributed-training data flow. If it matters, name "review/convert an existing diagram" and PlantUML in the description (watch the 1024 limit; there is little room), then rerun both sets on Haiku and Sonnet and the sibling validators. Haiku may be capped by the harness the way it is for the siblings.
- [ ] **Behavioral samples.** The prompt run has only one sample per prompt per model: Sonnet on 10 prompts, Haiku on 4, Opus not run. It shows the skill can be followed, not how often it succeeds. Haiku showed weaker scientific judgment: plate notation, causal identification, invented details. Siblings now have scripted `claude -p` runners with blind graders (`academic-papers/tests/run_prompts.py`, `agile-development/tests/behavior_eval.py`). Port one to run the 10 prompts, at least 2 samples each, on Haiku and Opus.

Not verified (only if a user need arises):
- APS full-width (`figure*`) size: 17.8 cm is an unverified default, and the REVTeX 4.2 guide states none.
- The `subcaption` `figure*` snippet and the `dvisvgm` export were never run. The TikZ/Beamer export rows in `references/legends-panels-and-export.md` were not run either.
- The PlantUML component diagram's layout was inspected only with Homebrew Graphviz.

## Done (do not redo; details in `VALIDATION.md`)

**P1 - verification (2026-09-21, follow-ups 2026-09-25)**
- Every Mermaid block rendered with `mmdc`, and all 37 renders reviewed for layout (2 fixes). The checker calls `mmdc` when it is present.
- TikZ and tikz-feynman compiled with Tectonic. The Feynman examples now lead with manual placement, and the `calc` requirement is confirmed. The LuaLaTeX auto-layout variant is verified: clean, but `e^+` is on top. `[compat=1.1.0]` added.
- PlantUML: all 6 blocks rendered; one syntax error (a one-line class body) was fixed. The checker renders plantuml fences, with 4 tests.
- Prompt run with Sonnet on 10 prompts and a Haiku second sample on 4. Fixes: `<br/>` guidance; "count files, not mentions"; a hyperparameter with a prior is a random variable; causal identification claims; a no-invented-details rule.
- Venue widths checked against the style files:
  - ICML 2026: 8.26 cm per column.
  - NeurIPS 2026 and ICLR 2026: 5.5 in.
  - JHEP `jheppub`: corrected from 15.5 cm to 15.1 cm.
  - APS single column: 8.6 cm.
  - None of these sets a minimum font size inside figures. JHEP figure rules were added.

**P2 - content (2026-09-21)**
- LHC pipeline example `hep/08`, repository inspection `general/05`, and Methods-to-workflow with Known/Inferred/Assumed `general/06`.
- PlantUML reference plus examples `computer-science/09-10`.
- SVG-spec template and example `general/07`.
- `templates/ml-pipeline.md` and `templates/bayesian-model.md`; the plate labels and font were fixed.
- Sketch-to-spec: `general-diagram-principles.md` section 11.

**P3 - stretch goals (2026-09-21)**
- `references/legends-panels-and-export.md` covers multi-panel figures, posters, theses, Beamer overlays, talk simplification, equations, symbol tables, export recipes and per-format legend snippets.
- A `--legend` script helper was deliberately not added: a legend must reflect the styles a specific figure uses.

**P4 - integration**
- Pointers added both ways with `academic-papers` and `hep-analysis`; the sibling validators pass.
- No new skills were added, so no skill counts needed updating.
