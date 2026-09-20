# TODO for future Claude sessions (hep-analysis)

State at 2026-09-21: skill is on `main`; the standard-library tests and `scripts/validate_skill_bundle.py` pass
(see `VALIDATION.md`). Most of the verification so far was structural or numerical on pure-Python helpers. Nothing
in the skill has been checked by running it on a fresh model. Read `VALIDATION.md` first, then this file.

Working rules: work on a branch, run `python3 -m unittest discover -s tests` and
`python3 scripts/validate_skill_bundle.py` before committing, keep `SKILL.md`, `README.md`,
`scripts/validate_skill_bundle.py` `REQUIRED_PATHS` and `agents/openai.yaml` in sync, and ask before pushing or
merging. Record every result (including negative ones) in `VALIDATION.md`. Do not change physics behavior in a
template or reference without saying so.

Environment facts found on 2026-09-21 (re-check, they may have changed):
- `root` 6.38 is installed by Homebrew (`/opt/homebrew/Cellar/root/...`), but `import ROOT` fails under the
  miniconda `python3` (cppyy symbol error, Python ABI mismatch). Try Homebrew's own Python
  (`$(brew --prefix root)/...` or `python3.1x` from Homebrew) before concluding PyROOT is unavailable.
- `pyhf` and `combine` are not installed; `uproot`/`awkward` need a check (`python3 -c "import uproot, awkward"`).
  Install into a scratchpad venv, not the user's conda base.

## P1 - close known verification gaps (things never actually run)
- [ ] Run the ROOT-dependent assets for real: `assets/cpp_rdataframe_analysis.cpp`, `rdf_analysis.cpp`,
      `fit_histogram.cpp`, `plot_branch.C`, `pyroot_rdataframe_analysis.py`, `pyroot_roofit_signal_background.py`,
      and `scripts/new_root_cpp_project.sh` through a full `cmake` configure + build. Previously only `cmake`
      up to `find_package(ROOT)` and `py_compile` were checked. Make a tiny synthetic TTree to feed them.
- [ ] Run the five PyROOT scripts (`inspect_root_file.py`, `check_systematic_variations.py`,
      `compare_root_histograms.py`, `summarize_histogram_statistics.py`, `roofit_workspace_summary.py`) against a
      real ROOT file / RooWorkspace, not just `--help`. Add the fixture generator to `tests/` (skip if no ROOT).
- [ ] Run `assets/uproot_awkward_analysis.py` with `assets/analysis_config.yaml` on a synthetic file
      (needs `uproot`, `awkward`).
- [ ] Validate `assets/pyhf-counting.json` with `pyhf` (schema + a `pyhf cls` run) and
      `assets/combine_datacard_template.txt` with `combine` if obtainable (else mark "not verified" honestly).
- [ ] Numerically cross-check the physics helpers against independent references, not only self-consistency:
      `li_ma_significance.py` (Li & Ma 1983 eq. 17 worked values), `tag_and_probe_efficiency.py`
      (Clopper-Pearson vs `scipy.stats.beta`), `cosmic_ray_flux.py`, `geomagnetic_cutoff.py` (Stormer vs published
      vertical cutoffs), `solar_modulation_force_field.py`, `xmax_gaisser_hillas.py`, `cherenkov_angle.py`,
      `multiple_scattering.py` (PDG Highland formula), `calorimeter_resolution.py`, `pid_separation_power.py`.
      Record which constants/units each script assumes.
- [ ] Audit the physics claims and numbers in `references/18-50` against primary sources
      (PDG review, experiment papers). Every hard number needs a source in `references/13-sources.md`
      or should be removed/softened. Flag anything time-sensitive (latest results) as needing a date.

## P2 - test that the skill actually changes model behavior
The 24 examples (`examples/01-24`) and the invariants in `SKILL.md` are unproven until a fresh model is run on them.
- [ ] Write 10-15 realistic prompts (store in `tests/prompts.md`) covering: RDataFrame cutflow with signed weights,
      uproot jagged selection, JES systematic implemented as a shape variation, ABCD closure failure,
      unblinding request on a masked region, low-count flux with Poisson interval, correlated ratio uncertainty,
      Li & Ma with trials factor, unfolding regularization choice, pyhf model with overlapping regions,
      a tuning-to-agree request (should be refused/redirected per invariants), an AMS-only question
      (should route to `ams-analysis`), and an unrelated "root" (Linux root) question (must not trigger).
      For each prompt write the expected behaviors (which invariant fires, which reference is read).
- [ ] Run each prompt in a fresh subagent with and without the skill (baseline vs skill); compare against the
      expectations; log pass/fail in `VALIDATION.md`. Repeat with Haiku (weaker model) and Opus if possible.
- [ ] Trigger test for the frontmatter `description`: 20 should-trigger and 20 should-not-trigger queries
      (include near-misses: `ams-analysis`, `deep-learning` HEP-ML, Linux root, generic statistics).
      Consider `skill-creator` description optimization; keep the description under its length limit.
- [ ] Check routing hygiene with the sibling skills: `hep-analysis` vs `ams-analysis`, `academic-diagrams`,
      `academic-papers`; run `skill-router`'s validator and tests after any description change.
- [ ] Verify the 24 examples follow their archetype rules (`task-authoring/references/example-authoring.md`) and
      that every code snippet in them runs or is clearly labelled pseudo-code. Run the runnable ones.

## P3 - improve content and structure
- [ ] `SKILL.md` is ~180 lines and the references total ~7,200 lines: check progressive disclosure. Confirm that a
      typical task needs to read at most 2-3 references, and add "read only if" hints where a routing row is vague.
- [ ] Look for gaps and overlap: `references/21-50` (detector) vs `ams-analysis` and `references/38-ams02-case-study.md`;
      remove duplicated tables (`49-detector-comparison-tables.md` vs the per-detector files).
- [ ] Add missing worked examples for topics with zero examples today: RooFit fit, pyhf workflow, Geant4 setup,
      IACT/neutrino analysis, cosmic-ray flux from counts, BDT training without leakage.
- [ ] Add regression tests for scripts that have none (see `tests/`: only `test_helpers.py`, `test_astroparticle.py`,
      `test_ams02.py`). Cover error paths (bad input, zero counts, negative weights).
- [ ] Add a minimal end-to-end sample analysis (synthetic ntuple generator -> cutflow -> histograms -> `pyhf` fit
      -> yield table) under `assets/` or `examples/` that exercises the scripts in sequence and can serve as a smoke test.
- [ ] Multi-platform check (Codex, Antigravity): confirm `agents/openai.yaml` is current and that no instructions depend
      on Claude-only tools. See the repo's multi-platform conventions.
- [ ] Skill-doctor / skill-reviewer pass on `SKILL.md` and `README.md` (`plugin-dev:skill-reviewer`).

## P4 - housekeeping and decisions
- [ ] Remove stray `scripts/__pycache__` and `tests/__pycache__` from the working tree if they are untracked and not ignored.
- [ ] Update `VALIDATION.md` header date and counts (file count, test count) after each pass.
- [ ] Ask the user: which experiment(s) matter most (CMS/ATLAS Combine vs AMS/IACT)? This sets what to prioritise in P2 prompts.
- [ ] Ask the user whether a `hep-analysis` "latest results" policy is wanted (sources/dates to re-verify periodically).
