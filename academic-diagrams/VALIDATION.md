# Package Validation Record

Validation date: 2026-09-21 (follow-ups 2026-09-25, round 2 on 2026-10-01). Helper test environment: Python 3, standard library only; Graphviz `dot` present, no LaTeX (Mermaid CLI available through npx).

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
guide itself states no figure widths, and 17.8 cm for a full-width figure was an unverified default then (checked against the class geometry on 2026-10-02, see "APS full-width check").

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

## Round 2: description length and triggering (2026-10-01)

- The frontmatter description was 1180 characters (limit 1024). It is now 1014: it names conversion of Mermaid/DOT/PlantUML to SVG, PDF or TikZ and "schematic", and drops the long species lists. `scripts/validate_skill_bundle.py` now fails a description over 1024 characters (quotes stripped before counting); 2 new tests (the real bundle is within the limit; a copy with a padded description makes the validator exit 1). Suite: 27 tests OK, 2 skipped (no `mmdc`/`plantuml`). Sibling validators and tests all pass (academic-papers 48, agile-development 44, ams-analysis 366, deep-learning 114 with 3 skipped, hep-analysis 205 with 12 skipped, task-authoring 78).
- New trigger sets: `tests/trigger_queries.json` (tuning: 12 target queries, 10 sibling or generic negatives) and `tests/trigger_queries_holdout.json` (written separately: 10 target, 8 negatives). Harness: `hep-analysis/tests/routing_eval.py --target academic-diagrams`, all 7 repo skills, bare query, 2 runs per query. Shown as recall over target runs; 0 false triggers in every run; routing to the expected owner overall was 34/44 and 25/36 runs on Sonnet and 12/44 and 9/36 on Haiku (positives and negatives together).

| Model | Tuning recall | Holdout recall |
|---|---|---|
| Sonnet | 22/24 | 14/20 |
| Haiku | 5/24 | 5/20 |

- The two queries from the earlier eval: "Mermaid sequence diagram into a publication-quality SVG" 2/2 on Sonnet (was 0/2), still 0/2 on Haiku (the built-in `dataviz` skill loads both times); "TikZ schematic of a layered detector cross-section" 2/2 on both models (Haiku was 0/2).
- Sonnet misses: "review this causal DAG" (no skill, 2/2), "convert my PlantUML component diagram to a clean PDF" (none, 2/2), "draw the data flow of our distributed training setup" (none, 2/2), and single misses on an agentic block diagram and a likelihood-fit-region review. Haiku mostly loads no skill, or `dataviz`, for architecture-figure and graphical-model queries, and never loaded one for the DAG review, DOT conversion, setup schematic, slide simplification, unfolding workflow, calorimeter TikZ, PlantUML-to-PDF or fit-region review queries. The same Haiku pattern is in the sibling skills (it often calls no skill in this harness).
- No description tuning was done after these runs, so the holdout is still clean for one more change. Early queries were chosen by the author of the description, so the tuning set is not independent evidence.

## Round 3: behavioral samples and trigger retune (2026-10-01)

**Runner.** `tests/prompts.md` (D01-D10: the ten manual-run prompts with small concrete inputs and Must / Must-not rubrics) and `tests/run_prompts.py`
(ported from `academic-papers/tests/run_prompts.py`: fresh `claude -p` per answer, skill arm vs baseline arm, no shell or network, blind Opus grader). Answers cannot be rendered
in this harness, so graders judge source text only. 2 samples per prompt per arm.

| Model | Skill arm (20 runs) | Baseline arm (20 runs) |
|---|---|---|
| Opus | 19 PASS, 1 PARTIAL, 0 FAIL | 11 PASS, 3 PARTIAL, 6 FAIL |
| Haiku (before SKILL.md edit) | 7 PASS, 12 PARTIAL, 1 FAIL | 8 PASS, 2 PARTIAL, 10 FAIL |
| Haiku (after SKILL.md edit) | 13 PASS, 5 PARTIAL, 2 FAIL | not rerun |

- Opus follows the skill reliably; the one PARTIAL (D08) drew shared-memory edges as dashed but never separated control flow from data flow. Baseline Opus fails mainly D07 (invented counts or edges), D08 and D02.
- Haiku with the skill was PARTIAL on 12 of 20 runs, and read no reference files in any run (only SKILL.md is injected), so rules that lived only in references were not applied: state what arrows mean, say a figure was drawn from a listing only, separate control from data flow, add no unrequested nodes. Haiku with the skill was *not* better than Haiku baseline on pass count (7 vs 8) but far fewer FAILs (1 vs 10).
- **Fix:** four lines added to SKILL.md "Output Style" covering those four points. Rerun (same prompts, 2 samples, skill arm only): 13 PASS, 5 PARTIAL, 2 FAIL. The two FAILs (D01 invented "maximum-likelihood fit" and no signal-model flag; D05 implied a direct S->C edge) are scientific-judgment slips on prompts that passed 2/2 before, so with n=2 this looks like sampling noise but is not shown to be. Still small samples; 20 runs per cell is not a success rate.
- Concern: Haiku D04 once drew sigma (fixed 0.5) as a shaded circle; D07 once invented call edges between scripts despite the new rule.

**Trigger retune (one attempt).** Description now 1010 characters: dropped the format list ("Outputs editable sources (Mermaid, DOT, ...)") and added the trigger phrases 'review this causal DAG', 'PlantUML to PDF', 'data flow of our training setup'. Same harness, 2 runs per query:

| Model | Tuning recall | Holdout recall | False triggers |
|---|---|---|---|
| Sonnet | 22/24 (was 22/24) | 15/20 (was 14/20) | 0 |
| Haiku | 4/24 (was 5/24) | 2/20 (was 5/20) | 0 |

The three Sonnet misses named in round 2 (causal-DAG review, PlantUML-to-PDF, distributed-training data flow) no longer miss. Sonnet's remaining misses: Feynman diagram in TikZ (1 run), talk-slide simplification (1), calorimeter TikZ (2), agentic block diagram (2), fit-region review (1). Haiku got worse (-1 tuning, -3 holdout; 4/44 runs, within what two samples can swing, but not an improvement), and its misses are still mostly "no skill loaded" or `dataviz`, as for the sibling skills. The holdout was used for this check, so it is no longer clean; stopped after one attempt as agreed.

## Round 4: Sonnet on the behavioral runner, larger samples (2026-10-02)

Same runner and prompts as Round 3 (D01-D10, blind Opus grader, no SKILL.md or description changes). Sonnet: 6 samples per prompt per arm. Opus: 4 more skill-arm samples per prompt (6 per cell with Round 3's 2; reported separately, and SKILL.md is unchanged since Round 3).

| Model | Skill arm | Baseline arm |
|---|---|---|
| Sonnet (60 runs per arm) | 51 PASS, 9 PARTIAL, 0 FAIL | 23 PASS, 22 PARTIAL, 15 FAIL |
| Opus, new runs only (40) | 37 PASS, 3 PARTIAL, 0 FAIL | not rerun |

- Per prompt, Sonnet skill arm: D01, D03-D07, D09, D10 are 6/6 PASS; D02 1/6 PASS; D08 2/6 PASS (rest PARTIAL). Sonnet baseline fails D07 5/6 (invented counts or edges), D08 6/6, D01 2/6 and D05 2/6; D09 and D10 pass without the skill, so they do not discriminate.
- **D08 (control vs data flow) is a real gap, not noise.** Sonnet PARTIAL 4/6, Opus PARTIAL 1/4 (and 1/2 in Round 3). The answers draw data flow and memory read/write but state control flow is omitted on purpose, instead of showing it in a second line style or legend.
- **D02 is mostly a rubric conflict.** All 7 PARTIALs (5 Sonnet, 2 Opus; I read the grader notes for 4 Sonnet and both Opus ones) fail the same item: the lanes meet at "Physics result" and reconstruction/analysis is raised as an open question instead of drawn. That is the skill's no-invented-steps rule working as written against a rubric item that asks for the stage. Decide whether the rubric or the skill should change before treating it as a skill failure. Not changed here, so results stay comparable.
- Opus skill arm over Round 3 and 4 combined: 56 PASS, 4 PARTIAL, 0 FAIL of 60 runs (D08 accounts for 2 PARTIALs and D02 for 2). Still one grader (Opus) and no rendering.
- Reads: Sonnet read a reference file in most skill runs (HEP and TikZ references for D02); Haiku did not in Round 3.

**Follow-up edits (2026-10-02).** D08: SKILL.md "Output Style" now says control and data flow both appear whenever a component splits, dispatches or calls others, so control edges are drawn in a second style with a legend entry instead of omitted. D02: the rubric item now asks for parallel paths meeting at a shared result, with a reconstruction/analysis stage optional (the skill must not invent it). Rubric changed after seeing results, so D02 numbers before and after are not strictly comparable.

| Sonnet skill arm after the edits | Result |
|---|---|
| D02 + D08, 6 samples each | 11 PASS, 1 PARTIAL (D02: the answer added its own Reconstruction box and drew one linear chain). D08 was 6/6 PASS (was 2/6) |
| Regression, all of D01-D10, 4 samples each | 37 PASS, 3 PARTIAL. All 3 are D06 (was 6/6): two used single-`$` math in Mermaid labels, which Mermaid does not render, and one gave no stopping criterion. Neither relates to the new line; unresolved, n=4 |

Not rerun: Opus, Haiku. Possible next step: a SKILL.md or Mermaid-reference line on `$$...$$` math in Mermaid labels, if D06 stays PARTIAL on a larger sample.

**D06 recheck (2026-10-02).** Skill arm, D06 only, same SKILL.md as the follow-up edits: Sonnet 20 samples 17 PASS, 3 PARTIAL, 0 FAIL; Opus 10 samples 10 PASS. All 3 Sonnet PARTIALs fail the same item, valid source without unsupported label syntax (Mermaid math); none lacked a stopping criterion. So the 3/4 PARTIAL above was mostly sampling noise; the residual is about 15% (3/20, so roughly 5-35% at 95%) for Sonnet on Mermaid math labels. Not tuned. Haiku not run.

**Mermaid math rule (2026-10-02).** Added to SKILL.md "Publication Standards" and `references/mermaid-patterns.md`: single-`$` math does not render in Mermaid; use `$$...$$` or plain Unicode. D06, Sonnet, 20 more samples: 18 PASS, 2 PARTIAL (was 17/20). Neither remaining PARTIAL is about Mermaid math: both use TikZ `rounded rectangle` without `shapes.misc`. So the Mermaid-math slip no longer appears (0 of 20, was 3 of 20), but the pass count is not clearly better; the effect is not shown, only the failure mode is gone. Regression, all prompts, 3 Sonnet samples each: 29 PASS, 1 PARTIAL (D03: the text says dashed means fit output while the DOT draws CR to L dashed; a text/source mismatch, unrelated).

**Haiku run (skill arm, D01-D10, 4 samples each, after all SKILL.md edits).** 23 PASS, 13 PARTIAL, 4 FAIL of 40 (57% PASS; Round 3 after its edit was 13/20 = 65% PASS, 2 FAIL). Not distinguishable at these sizes. FAILs: D05 x2 (adds a direct S->C edge in the notes or caption, and wrong identification remarks: the same invented-detail slip as before), D02 (names Geant4 and detector parts as facts), D09 (labels a pre-norm layer "post-norm" in the caption). Haiku still does not read references, so the new Mermaid line lives in SKILL.md. No tuning for Haiku, per the standing decision.

## Round 5: Opus rerun and a Haiku invented-details attempt (2026-10-02)

**Opus** (skill arm, D01-D10, 4 samples each, after the Round 4 and Mermaid edits): 40 PASS, 0 PARTIAL, 0 FAIL.

**Haiku attempt (reverted).** Added three sentences to SKILL.md "Output Style": notes and captions must not mention an edge, effect or path the request did not state; never call an unmeasured variable adjustable; take pre-norm/post-norm from the code order; use generic labels, not named software or detector parts. Haiku skill arm, all prompts, 4 samples each: 19 PASS, 14 PARTIAL, 7 FAIL (before the edit: 23 / 13 / 4). Targeted rerun, 8 samples on D02, D05, D09: 15 PASS, 8 PARTIAL, 1 FAIL.

| Prompt | Before (4) PASS | After, full run (4) PASS | After, targeted (8) PASS |
|---|---|---|---|
| D02 | 2 | 4 | 6 |
| D05 | 1 | 0 | 5 |
| D09 | 2 | 1 | 5 |

The same configuration gave D05 0/4 and 5/8 PASS, so the run-to-run spread is as large as any effect. The targeted prompts may have improved (D02 12 samples: 10 PASS vs 2/4), but D04, D06, D07 got worse in the full run (D07 0 PASS vs 3/4), and the overall FAIL count rose from 4 to 7. No effect shown, so the SKILL.md edit was reverted to keep the file short, consistent with the standing decision not to tune for Haiku. Haiku invents details in 5-35% of runs depending on the prompt; treat it as a known limitation.

**Export snippets (2026-10-02).** Run with Tectonic 0.17.0, poppler and a standalone TikZ figure: standalone compile OK with the font embedded; `pdftoppm -r 300 -png` gave a 574x101 PNG; `pdftocairo -svg` gave a valid SVG (text as glyph outlines, so not selectable); the `subcaption` `figure*` snippet compiled in `\documentclass[twocolumn]{article}` and produced both panels (a), (b) and the caption on a float page. `dvisvgm` 3.6.1 (installed with Homebrew; conda-forge was refused pending channel terms): negative result. `dvisvgm fig.xdv` on Tectonic's output warns "86 PDF specials ignored", drops the TikZ boxes and arrow and overlaps the text (rendered and inspected); `dvisvgm --pdf` fails with "Ghostscript < 10.01.0 or mutool is required" (installed Ghostscript 10.08.0). After `brew install mupdf-tools` (mutool 1.28.5), `dvisvgm --pdf fig.pdf -o fig.svg` worked: rendered and inspected, boxes, arrow and both labels correct, text kept as 2 `<text>` elements (selectable), 5 path/rect elements. Beamer overlays were already compiled in Round 1.

**APS full-width check (2026-10-02).** Compiled `revtex4-2` under Tectonic 0.17.0 and printed the lengths: two-column `\textwidth` = 510 pt = 17.92 cm and `\columnwidth` = 246 pt = 8.65 cm in `reprint`, `aps,prl,twocolumn` and `aps,prd,reprint`; `aps,prd,preprint` (single column) `\textwidth` = 468 pt = 16.45 cm. So `figure*` can be up to 17.92 cm wide, and the 17.8 cm (7 in) default fits; the single-column 8.6 cm figure is consistent with 8.65 cm. These are class geometry, not an APS figure rule, and APS journals' author guidelines were not checked online.

**Math labels and font-heavy export (2026-10-02).** One standalone TikZ figure with `amsmath`/`bm` labels (posterior, `\mathcal{L}`, `\hat{\bm\mu}`, `\sqrt{s}`, integral, `\mathrm` text) and bold, italic, mono and small-caps text (13 embedded fonts: CM, LM). Rendered with rsvg and inspected against the `pdftoppm` PNG, which matched the PDF. `pdftocairo -svg` (glyph outlines) matched. `dvisvgm --pdf --no-fonts` matched. Plain `dvisvgm --pdf` (42 `<text>` elements, system fonts) did not: sans fallback, detached radical and integral limits, lost bold/italic, overlapping words (in rsvg; a browser with the fonts missing would behave similarly). `dvisvgm --pdf --font-format=woff2` embeds `@font-face` fonts (13 faces, 25 KB); not checked in a browser. Mermaid KaTeX labels and Graphviz were not retested here.

## Not verified

- The `dvisvgm` `.xdv` route is broken with Tectonic output (use `--pdf` with mutool). Only two small figures were exported; browser rendering of `--font-format=woff2` SVGs was not checked.
- ICML/NeurIPS/ICLR/JHEP/APS (single and full-width) were checked (see above and Round 5 follow-up).
- The PlantUML component diagram's automatic layout depends on the Graphviz version; the render was inspected with Graphviz from Homebrew only.
- The prompt run used one fresh agent per prompt and one sample each (Sonnet on 10, Haiku on 4; the Round 3 runner later added 2 samples each on Haiku and Opus); it shows the skill can be followed, not how often it succeeds. The table
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
