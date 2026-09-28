# TODO for future Claude sessions (academic-diagrams)

State (verified 2026-09-28 on `main`, all work merged; skill via PR #5, tooling follow-ups via PR #22): `python3 scripts/validate_skill_bundle.py` OK (28 files); `python3 -m unittest discover -s tests` 25 tests OK. 2 tests skip when `mmdc` or `plantuml` is not on PATH. P1-P4 are done. Open: the description (over the length limit, and it under-triggers) and more behavioral samples. Read `VALIDATION.md` "Not verified" first, then this file.

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

- [ ] **Description over the length limit.** The frontmatter `description` is 1180 characters; the limit is 1024, and siblings keep under it (hep-analysis 1019, academic-papers 1014). It dates from the initial build (2026-09-21), and `scripts/validate_skill_bundle.py` does not check the length. Fix this together with the item below.
  - Add a length check to the validator, with a test.
  - `task-authoring` has the same problem (1274 characters). Tell its TODO.
- [ ] **Under-triggering** found by the isolated routing eval (2026-09-26). Setup: `hep-analysis/tests/routing_eval.py` on `hep-analysis/tests/trigger_queries_holdout.json`, all 7 repo skills loaded as project skills, 2 runs per query. "none" means the model answered without invoking any skill.
  - "Turn this Mermaid sequence diagram into a publication-quality SVG": 0/2 Haiku, 0/2 Sonnet (none every time).
  - "Make a TikZ schematic of a layered detector cross-section for my paper": 0/2 Haiku (none once, built-in `dataviz` once), 2/2 Sonnet.

  To fix, name Mermaid-to-SVG conversion and "schematic" in the shortened description, then write this skill's own trigger sets. Follow the siblings' pattern: `tests/trigger_queries.json` for tuning and a held-out set that is never tuned on. Rerun with the harness on Haiku and Sonnet, and run the sibling validators and tests after the change.
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
