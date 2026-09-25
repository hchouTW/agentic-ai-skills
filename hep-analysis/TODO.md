# TODO for future Claude sessions (hep-analysis)

State at 2026-09-25 (follow-up pass on branch `hep-analysis-followups`, see its VALIDATION.md section): P1-P4 done except open follow-ups (see the 2026-09-24 section of `VALIDATION.md`). Earlier state, 2026-09-21: skill is on `main`; the standard-library tests and `scripts/validate_skill_bundle.py` pass
(see `VALIDATION.md`). Most of the verification so far was structural or numerical on pure-Python helpers. Nothing
in the skill has been checked by running it on a fresh model. Read `VALIDATION.md` first, then this file.

Working rules: work on a branch, run `python3 -m unittest discover -s tests` and
`python3 scripts/validate_skill_bundle.py` before committing, keep `SKILL.md`, `README.md`,
`scripts/validate_skill_bundle.py` `REQUIRED_PATHS` and `agents/openai.yaml` in sync, and ask before pushing or
merging. Record every result (including negative ones) in `VALIDATION.md`. Do not change physics behavior in a
template or reference without saying so.

Environment facts (re-check, they may have changed). 2026-09-24: PyROOT works under
`/opt/homebrew/bin/python3.14`; set `HEP_ROOT_PYTHON` to it for `tests/test_root_integration.py`.
ACLiC (`macro.C+`) fails even for an empty macro (macOS SDK mismatch). Found 2026-09-21:
- `root` 6.38 is installed by Homebrew (`/opt/homebrew/Cellar/root/...`), but `import ROOT` fails under the
  miniconda `python3` (cppyy symbol error, Python ABI mismatch). Try Homebrew's own Python
  (`$(brew --prefix root)/...` or `python3.1x` from Homebrew) before concluding PyROOT is unavailable.
- `pyhf` and `combine` are not installed; `uproot`/`awkward` need a check (`python3 -c "import uproot, awkward"`).
  Install into a scratchpad venv, not the user's conda base.

## P1 - close known verification gaps (things never actually run)
- [x] (2026-09-24) Run the ROOT-dependent assets for real: `assets/cpp_rdataframe_analysis.cpp`, `rdf_analysis.cpp`,
      `fit_histogram.cpp`, `plot_branch.C`, `pyroot_rdataframe_analysis.py`, `pyroot_roofit_signal_background.py`,
      and `scripts/new_root_cpp_project.sh` through a full `cmake` configure + build. Previously only `cmake`
      up to `find_package(ROOT)` and `py_compile` were checked. Make a tiny synthetic TTree to feed them.
- [x] (2026-09-24) Run the five PyROOT scripts (`inspect_root_file.py`, `check_systematic_variations.py`,
      `compare_root_histograms.py`, `summarize_histogram_statistics.py`, `roofit_workspace_summary.py`) against a
      real ROOT file / RooWorkspace, not just `--help`. Add the fixture generator to `tests/` (skip if no ROOT).
- [x] (2026-09-24; fixed missing sumw2) Run `assets/uproot_awkward_analysis.py` with `assets/analysis_config.yaml` on a synthetic file
      (needs `uproot`, `awkward`).
- [x] (2026-09-24: pyhf done; 2026-09-25: Combine v11 built in a scratch conda env, template limit matches pyhf within 1%, `tests/test_combine_template.py`) Validate `assets/pyhf-counting.json` with `pyhf` (schema + a `pyhf cls` run) and
      `assets/combine_datacard_template.txt` with `combine` if obtainable (else mark "not verified" honestly).
- [x] (2026-09-24; `tests/test_reference_values.py`; Stormer vertical-cutoff bug fixed) Numerically cross-check the physics helpers against independent references, not only self-consistency:
      `li_ma_significance.py` (Li & Ma 1983 eq. 17 worked values), `tag_and_probe_efficiency.py`
      (Clopper-Pearson vs `scipy.stats.beta`), `cosmic_ray_flux.py`, `geomagnetic_cutoff.py` (Stormer vs published
      vertical cutoffs), `solar_modulation_force_field.py`, `xmax_gaisser_hillas.py`, `cherenkov_angle.py`,
      `multiple_scattering.py` (PDG Highland formula), `calorimeter_resolution.py`, `pid_separation_power.py`.
      Record which constants/units each script assumes.
- [x] (2026-09-24, checked from knowledge and not re-fetched live; 2 corrections) Audit the physics claims and numbers in `references/18-50` against primary sources
      (PDG review, experiment papers). Every hard number needs a source in `references/13-sources.md`
      or should be removed/softened. Flag anything time-sensitive (latest results) as needing a date.

## P1 follow-ups found 2026-09-24
- [x] (2026-09-25: the config now labels these blocks as documentation-only; templates unchanged) `assets/uproot_awkward_analysis.py` ignores the config's `selection.cuts` and `histograms` (hard-coded
      selection). Either implement config-driven cuts or trim the config so it does not imply they are used.
- [x] (2026-09-25: PDG links -> 2026; ref 30 knee/ankle corrected, instep/second knee added; ref 33 IACT scale -> 10-20%; AMS Layer-0 not yet installed) Live re-check of the numbers in the latest-results policy list (`references/13-sources.md`), with dates.
- [ ] Re-check AMS-02 Layer-0 status after mid 2027 (installation creates a new detector era; ref 38). The schedule is only from secondary sources.
- [x] (2026-09-25: verified with ACLiC on conda-forge ROOT 6.34 in a clean env, bin-identical to interpreted. Homebrew ROOT ACLiC is still broken, and `~/.zshrc`'s `ROOT_INCLUDE_PATH` breaks any other ROOT's cling; see VALIDATION.md) Try `plot_branch.C+` (ACLiC) on a machine where ACLiC works.

## P2 - test that the skill actually changes model behavior
The 24 examples (`examples/01-24`) and the invariants in `SKILL.md` are unproven until a fresh model is run on them.
- [x] (2026-09-24: 16 prompts) Write 10-15 realistic prompts (store in `tests/prompts.md`) covering: RDataFrame cutflow with signed weights,
      uproot jagged selection, JES systematic implemented as a shape variation, ABCD closure failure,
      unblinding request on a masked region, low-count flux with Poisson interval, correlated ratio uncertainty,
      Li & Ma with trials factor, unfolding regularization choice, pyhf model with overlapping regions,
      a tuning-to-agree request (should be refused/redirected per invariants), an AMS-only question
      (should route to `ams-analysis`), and an unrelated "root" (Linux root) question (must not trigger).
      For each prompt write the expected behaviors (which invariant fires, which reference is read).
- [x] (2026-09-24: Opus and Haiku x skill/baseline; results in VALIDATION.md) Run each prompt in a fresh subagent with and without the skill (baseline vs skill); compare against the
      expectations; log pass/fail in `VALIDATION.md`. Repeat with Haiku (weaker model) and Opus if possible.
- [x] (2026-09-24: 20/20 recall, 0/20 false triggers on Opus and Haiku, simulated with descriptions only; `tests/trigger_queries.json`) Trigger test for the frontmatter `description`: 20 should-trigger and 20 should-not-trigger queries
      (include near-misses: `ams-analysis`, `deep-learning` HEP-ML, Linux root, generic statistics).
      Consider `skill-creator` description optimization; keep the description under its length limit.
- [x] (2026-09-24: all near-misses routed to the right sibling; description unchanged) Check routing hygiene with the sibling skills: `hep-analysis` vs `ams-analysis`, `academic-diagrams`,
      `academic-papers`; run each affected skill's validator and tests after any description change.
- [x] (2026-09-24: all 24 validate; test-first examples run end to end) Verify the 24 examples follow their archetype rules (`task-authoring/references/example-authoring.md`) and
      that every code snippet in them runs or is clearly labelled pseudo-code. Run the runnable ones.

## P2 follow-ups found 2026-09-24
- [ ] Re-run `claude plugin eval` (Sonnet too, not only Haiku) after any description change. For a real sibling-routing harness test, the eval child must not load ~112 user skills: the listing then shows plugin skills without descriptions. Find a way to isolate it (a clean HOME/config) and rerun `evals/` with all seven repo skills.
- [ ] Write a fresh trigger query set (not the 40 used for tuning) to check that the revised description generalizes on Haiku.
- [ ] Re-run `tests/prompts.md` on Haiku after any change to references 02/17/37 or the SKILL.md invariants. (Last done 2026-09-25: 9 PASS / 3 PARTIAL / 2 FAIL; P05 blinding and P07 prior-tuning fixed in SKILL.md/ref 01 and re-passed. Next time, run each prompt at least twice and give each agent its own output directory.)
- [x] (2026-09-25: refs 03/35 fixed; Haiku reruns P01 2/2 PASS, P10 2/2 PASS, P08 2/2 PARTIAL with no F signal; see VALIDATION.md) P01/P08/P10 are PARTIAL on Haiku: RDataFrame `Runs`-tree sumw code (ref 03), units on the flux value (ref 35), and the cutoff safety factor plus backtracing (ref 35). Check whether the references state these clearly enough.
- [x] (2026-09-25: scripts allowed + 350-word cap gave 2/2 FAIL ("sqrt(3) is a reasonable approximation", ref 35 never read). The SKILL.md flux invariant now says "no" and links ref 35; ref 37 links there too. Result 2/2 PASS; P09/P10/P12 regression 4 PASS, 2 PARTIAL, 0 FAIL) P08 stays PARTIAL on Haiku.
- [x] (2026-09-25: `claude plugin eval` recall is 20/20 on Sonnet and 12/20 on Haiku; the only false triggers are AMS queries with `ams-analysis` not loaded; see VALIDATION.md) Trigger test was simulated (an agent given the descriptions). If a harness-level trigger eval becomes available
      (e.g. `skill-creator` description optimization or `claude plugin eval`), re-run `tests/trigger_queries.json` through it.
- [x] (2026-09-25, user chose to tune and commit: Haiku recall 22/40 -> 38/40 runs, false triggers 3 -> 5/40, all on sibling-owned queries; simulated 7-skill routing clean; suite in `evals/`) Decide whether to raise Haiku trigger recall.

## P3 - improve content and structure
- [x] (2026-09-25: P2 agents read 1-3 references per task; ref 14 (1,300 lines) got a task-to-section map) `SKILL.md` is ~180 lines and the references total ~7,200 lines: check progressive disclosure. Confirm that a
      typical task needs to read at most 2-3 references, and add "read only if" hints where a routing row is vague.
- [x] (2026-09-25: ref 38 and ams-analysis already cleanly split; 5 duplicated rows removed from ref 49 Table 8; 42/45 tables are complementary) Look for gaps and overlap: `references/21-50` (detector) vs `ams-analysis` and `references/38-ams02-case-study.md`;
      remove duplicated tables (`49-detector-comparison-tables.md` vs the per-detector files).
- [x] (2026-09-25, as the user chose: verified walkthroughs in refs 07/09/20/28/33/35 instead of new archetype examples, keeping 3 per archetype; Geant4 not executed) Add missing worked examples for topics with zero examples today: RooFit fit, pyhf workflow, Geant4 setup,
      IACT/neutrino analysis, cosmic-ray flux from counts, BDT training without leakage.
- [x] (2026-09-24: added `test_yield_table.py`, `test_reference_values.py`, `test_root_integration.py`; every script except the bundle validator now has a test) Add regression tests for scripts that have none (see `tests/`: only `test_helpers.py`, `test_astroparticle.py`,
      `test_ams02.py`). Cover error paths (bad input, zero counts, negative weights).
- [x] (2026-09-25: `assets/end_to_end_sample_analysis.py` + `tests/test_end_to_end.py`) Add a minimal end-to-end sample analysis (synthetic ntuple generator -> cutflow -> histograms -> `pyhf` fit
      -> yield table) under `assets/` or `examples/` that exercises the scripts in sequence and can serve as a smoke test.
- [x] (2026-09-24: no Claude-only tool dependencies; openai.yaml short_description now covers astroparticle) Multi-platform check (Codex, Antigravity): confirm `agents/openai.yaml` is current and that no instructions depend
      on Claude-only tools. See the repo's multi-platform conventions.
- [x] (2026-09-25: verified findings applied, 3 declined with reasons; see VALIDATION.md) Skill-doctor / skill-reviewer pass on `SKILL.md` and `README.md` (`plugin-dev:skill-reviewer`).

## P4 - housekeeping and decisions
- [x] (already gitignored; no action) Remove stray `scripts/__pycache__` and `tests/__pycache__` from the working tree if they are untracked and not ignored.
- [ ] Update `VALIDATION.md` header date and counts (file count, test count) after each pass. (Recurring; last done 2026-09-25, round 3.)
- [x] Asked 2026-09-24: all three matter equally (AMS-02/space-based, CMS/ATLAS collider, IACT/neutrino/air shower), so balance the P2 prompts across them.
- [x] Asked 2026-09-24: yes. Added as "Latest-results policy" in `references/13-sources.md`.
