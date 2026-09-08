# Package Validation Record

Validation date: 2026-09-05. Helper test environment: Python 3, standard library
plus PyYAML.

## Deep test pass (2026-09-05)

A more thorough pass tested actual behavior, not just structure, working from the
files as they existed on disk after the merge and rename (staged fresh rather than
reused from an earlier local copy, to avoid testing stale content).

- `audit_histograms.py` was exercised against deliberately broken bundles covering
  every documented failure mode: a NaN in `sumw`, negative `sumw2`, a negative
  Poisson-expectation rate, a missing required `Down` variation, an
  identical-to-nominal variation, and mismatched edges between nominal and a
  variation. Each produced exactly the documented error or warning and the correct
  exit code; a clean bundle round-tripped through the module without mutating the
  input in place.
- `counting_reference.py`'s documented zero-observed/zero-background 95% bound
  (2.9957322735539895) was cross-checked against an independent calculation of
  `-log(0.05)` (agrees to floating-point precision), plus additional points and its
  documented input-range rejection (observed must be an integer from 0 through 500).
- `make_yield_table.py` was run against a real CSV (including a row with a blank
  uncertainty) and produced correctly formatted per-region Markdown tables; missing
  required columns and a missing input file both raised a clear, correctly-exited
  error.
- `validate_skill_bundle.py` was tested against four induced failures (a missing
  file, an emptied file, a broken SKILL.md frontmatter field, a renamed README
  section) and correctly caught each one, then confirmed clean again after
  restoring.
- All five PyROOT-dependent scripts (`inspect_root_file.py`,
  `check_systematic_variations.py`, `compare_root_histograms.py`,
  `summarize_histogram_statistics.py`, `roofit_workspace_summary.py`) defer
  `import ROOT` into the function body, so `--help` and file-existence/argument
  validation work with no ROOT installed, and the ROOT-dependent path fails with a
  deliberate `SystemExit("PyROOT is required ...")` message rather than a raw
  `ModuleNotFoundError` traceback.
- `scripts/new_root_cpp_project.sh` was run to scaffold a project, and the result was
  fed to `cmake -S . -B build`: configuration proceeds correctly through
  `cmake_minimum_required`/`project`/`CMAKE_CXX_STANDARD` and fails only at
  `find_package(ROOT REQUIRED ...)`, confirming the generated `CMakeLists.txt` is
  syntactically correct up to the point that genuinely requires a ROOT installation
  this environment doesn't have.
- Cross-checked every `references/NN-*.md` filename mentioned in `SKILL.md`'s routing
  table, `scripts/validate_skill_bundle.py`'s manifest, and the reference files'
  own internal cross-links against the files that actually exist on disk: all
  consistent, no typos, no orphaned files.
- Confirmed the shipped `assets/analysis_config.yaml` template actually satisfies
  every config key `assets/uproot_awkward_analysis.py` reads from it
  (`inputs.tree`, `inputs.files`, `branches.required`, `output.directory`,
  `output.root_file`).

Two defects were found and fixed as part of this pass:

- `scripts/new_root_cpp_project.sh` accepted a project-name argument, created the
  directory with that name, and printed build instructions referencing it, but the
  `CMakeLists.txt` it generated always hardcoded `project(root_cpp_analysis ...)`
  regardless of the argument. Fixed to interpolate the actual project name while
  keeping `${ROOT_INCLUDE_DIRS}`/`${ROOT_LIBRARIES}` as literal CMake variables.
- `assets/plot_branch.C` used `TTree` (via `file->Get<TTree>(...)`,
  `tree->GetBranch(...)`, `tree->Print()`) without including `<TTree.h>`, unlike
  every other template in the package that touches `TTree`. Added the missing
  include.

Housekeeping: the executable bit on `scripts/*.py` and `scripts/*.sh` did not survive
an earlier file transfer and has been restored; stray `__pycache__` directories left
behind by earlier interactive test runs were removed from the live folder.

## Merge and rename (2026-09-05)

This package (published at the time as `hep-experiment-analysis`) absorbed the
content of a separate, coding-focused `hep-analysis` skill (ROOT C++/PyROOT/
RDataFrame/uproot coding patterns, CMake builds, debugging, code conventions, and
additional ROOT-based helper scripts and starting-template assets). The folder and
the `name:` field in SKILL.md were then renamed back to `hep-analysis`, so this single
package now carries both the original `hep-analysis` coding content and the former
`hep-experiment-analysis` statistics content under the `hep-analysis` name. The
following checks were run after the merge:

- `python3 -m unittest discover -s tests -v`: all 13 tests passed unchanged.
- `python3 scripts/validate_skill_bundle.py`: confirmed all 53 files this package's
  SKILL.md/README.md depend on (references, scripts, assets, tests) are present and
  non-empty, and that SKILL.md carries valid frontmatter and README.md its expected
  section headers.
- `python3 -m py_compile` on every `.py` file in the package: all compiled without
  error, including the newly added ROOT/PyROOT-dependent scripts (syntax only - see
  limitation below).
- `bash -n` on every `.sh` file: no syntax errors.
- All relative Markdown links across every reference file were resolved against the
  filesystem: none broken.
- All YAML files (`assets/*.yaml`, `agents/openai.yaml`) and the SKILL.md frontmatter
  were parsed with PyYAML; both JSON assets were parsed with the standard library
  `json` module.
- Searched the full package for stale references to the old per-file names from the
  original `hep-analysis/references/*.md` layout: none found. After the rename, the
  remaining mentions of `hep-experiment-analysis` are the intentional migration notes
  in README.md and this file.
- Re-ran the original synthetic histogram CLI check: for zero observations, zero
  background, and a 95% flat-signal-prior credible bound, the result is unchanged at
  2.9957322735539895.

## Coverage expansion pass (2026-09-05)

Added three new reference files to broaden and deepen physics-object, trigger/
luminosity, and multivariate-classifier coverage:
`references/20-physics-objects-jets-btagging-met.md`,
`references/21-triggers-luminosity-pileup.md`, and
`references/22-multivariate-classifiers-bdt-nn.md`. Added two new standard-library
scripts implementing the concrete methodology those references describe -
`scripts/tag_and_probe_efficiency.py` (exact Clopper-Pearson binomial confidence
intervals) and `scripts/pileup_reweight.py` (data/MC pileup reweighting with
explicit undefined-bin flagging) - plus `assets/pileup_profiles.example.json` as a
synthetic input for the latter. `SKILL.md`'s reference-routing table, executable-
resources list, and frontmatter `description`, `README.md`'s coverage section and
quick checks, and `scripts/validate_skill_bundle.py`'s `REQUIRED_PATHS` were all
updated to match (bundle now reports 59 files).

Unlike the ROOT/PyROOT-dependent scripts, both new scripts are pure Python
standard library and were verified numerically, not just for syntax:

- `tag_and_probe_efficiency.py`'s Clopper-Pearson interval (implemented via a
  from-scratch, log-space exact binomial tail and bisection - no SciPy dependency
  at runtime) was checked against two independent references: the well-known
  textbook exact values for 0/10 and 10/10 at 95% (0 to 0.30849710781876385, and
  its 0.6915028921812392-to-1 mirror image), and, more broadly, against
  `scipy.stats.beta.ppf`-derived Clopper-Pearson bounds (SciPy happened to be
  available in this validation environment, used here only as an independent
  correctness oracle, not as a runtime dependency of the script) across 12
  (pass, total) cases - including the boundaries 0/n, n/n, and totals up to the
  documented 200000 cap - and 4 confidence levels each (48 cases total), agreeing
  to within 2.4e-11. Interval containment of the point estimate and monotonic
  widening with confidence level were also checked directly.
- `pileup_reweight.py`'s reweighting formula was checked for self-consistency: the
  mean of a synthetic MC pileup profile, reweighted by the computed factors, was
  confirmed to match the target data profile's mean to within 1e-6 (a closure
  check, using the shipped `assets/pileup_profiles.example.json` - a Poisson-like
  data profile at mean 38 vs. an MC profile generated assuming mean 30). The
  explicit-flagging behavior for a data-populated, MC-empty bin (an undefined
  reweighting factor) was verified to report `None`/a flagged bin index and a
  nonzero exit code, rather than silently producing `inf` or `0`, and to leave a
  bin where *both* profiles are zero unflagged (nothing needs reweighting there).
- Both scripts' CLIs were exercised for invalid input (`pass_count > total`,
  out-of-range `total`, mismatched profile lengths, a missing input file) and
  confirmed to fail with a clear one-line message and a nonzero exit code rather
  than a raw traceback.
- 16 new tests were added to `tests/test_helpers.py` (13 pre-existing + 16 new =
  29 total, `python3 -m unittest discover -s tests -v`) covering all of the above.

## Limitations

- ROOT is not installed in the validation environment, so `check_root_cpp_env.sh`
  correctly reports it missing (exit 1) rather than being runnable end to end, and the
  PyROOT-dependent scripts (`inspect_root_file.py`, `check_systematic_variations.py`,
  `compare_root_histograms.py`, `summarize_histogram_statistics.py`,
  `roofit_workspace_summary.py`) and the `.cpp`/`.C` template assets were checked for
  Python syntax only, not executed or compiled against real ROOT headers/libraries.
  This mirrors the same limitation already recorded for RooFit/pyhf/Combine snippets
  before the merge.
- No real experiment data, full-production regression, coverage study, or
  collaboration approval was available. Helper tests do not establish the physical
  correctness of arbitrary analyses.
- The counting reference intentionally limits observed counts and known background to
  at most 500. Extreme tails can underflow in floating-point arithmetic. It is not a
  general statistics package and does not calculate CLs.
- The skill-creator `quick_validate.py` was not run in this environment.

In an environment with ROOT/PyROOT and skill-creator, additionally run the
ROOT-dependent scripts against a real file and `quick_validate.py`. In the target
analysis environment, perform the relevant physical and statistical checks described
in references/12-validation.md.
