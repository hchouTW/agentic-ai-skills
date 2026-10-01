# TODO for future Claude sessions (academic-diagrams)

State (verified 2026-10-01 on `main`, all work merged; skill via PR #5, tooling follow-ups via PR #22, round 2 via PR #57, round 3 via PR #64): `python3 scripts/validate_skill_bundle.py` OK (28 files); `python3 -m unittest discover -s tests` 28 tests OK (re-run 2026-10-01 after the merge). 2 tests skip when `mmdc` or `plantuml` is not on PATH. P1-P4 are done. Open: Haiku under-triggering (likely harness cap; the holdout set is spent), Haiku scientific-judgment slips (invented details), D06 Mermaid math (fixed 2026-10-02 by a `$$` line; the slip is gone, remaining D06 PARTIALs are a missing TikZ `shapes.misc`), Haiku invented-details slips (D05 direct S->C edge, D02 Geant4, D09 pre-norm called post-norm): Round 5 tried three SKILL.md sentences, no effect shown (19/40 vs 23/40 PASS), reverted; closed as a known Haiku limitation. Opus rerun 40/40 PASS (Round 5). Read `VALIDATION.md` "Not verified" first, then this file.

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
- [x] **Under-triggering, round 3 (2026-10-01):** one retune attempt (description 1010 chars; names causal-DAG review, PlantUML to PDF, training-setup data flow). Sonnet 22/24 tuning and 15/20 holdout; the three named misses now route. Haiku 4/24 and 2/20 (slightly worse than 5/24 and 5/20; harness cap likely, no skill is loaded on most Haiku runs). The holdout is spent. Remaining Sonnet misses: TikZ Feynman, talk simplification, calorimeter TikZ, agentic block diagram, fit-region review. Do not keep rewording for Haiku. See `VALIDATION.md` "Round 3".
- [x] **Behavioral samples (2026-10-01):** `tests/prompts.md` (D01-D10) and `tests/run_prompts.py` (blind Opus grader, skill vs baseline). Opus skill arm 19/20 PASS (baseline 11/20); Haiku skill arm 7/20 PASS before and 13/20 after four lines added to SKILL.md "Output Style". Round 4 (2026-10-02): Sonnet 6 samples per cell skill 51/60 PASS (0 FAIL) vs baseline 23/60; Opus 4 more skill samples 37/40 PASS. Fixed in Round 4: **D08** control flow was omitted (Sonnet 4/6 PARTIAL); one line added to SKILL.md Output Style, now 6/6 PASS. **D02** rubric changed (the skill refuses to invent a reconstruction stage), 5/6 PASS. Closed: **D06** Mermaid math. Open: Haiku still invents details (D01 fit method, D05 extra edge, D07 call edges) and was not rerun; answers are never rendered here.

Not verified (only if a user need arises):
- APS full-width (`figure*`) size: 17.8 cm is an unverified default, and the REVTeX 4.2 guide states none.
- `dvisvgm --pdf` works with `mutool` (verified 2026-10-02 on a small figure; Homebrew `dvisvgm` 3.6.1 and `mupdf-tools`). Its `.xdv` route is broken with Tectonic output. Not tried: math labels and font-heavy figures. The `subcaption` `figure*` snippet, `pdftoppm`, `pdftocairo -svg` and the TikZ standalone compile were also run.
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
