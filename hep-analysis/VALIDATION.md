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

## Detector, reconstruction, and simulation expansion pass (2026-09-09)

Added nine reference files covering the detector, reconstruction, and simulation
layers beneath the existing analysis/statistics content, organized by detector
technology with no assumed experiment:
`references/23-detector-systems-overview.md`,
`references/24-tracking-and-vertexing.md`,
`references/25-calorimetry-ecal-hcal.md`,
`references/26-particle-identification.md`,
`references/27-event-reconstruction.md`,
`references/28-reconstruction-performance-and-truth-matching.md`,
`references/29-event-generation.md`,
`references/30-detector-simulation.md`, and
`references/31-calibration-and-alignment.md`. Added four new standard-library
scripts implementing the formulas those references rely on -
`scripts/multiple_scattering.py`, `scripts/calorimeter_resolution.py`,
`scripts/pid_separation_power.py`, and `scripts/cherenkov_angle.py` - plus
`assets/detector_stack.example.json` and
`assets/calorimeter_response.example.json` as synthetic inputs. `SKILL.md`'s
reference-routing table, executable-resources list, analysis invariants (two new
entries: no tuning of simulation/calibration to the measured observable, and
detector quantities are inferred rather than observed), example requests, and
frontmatter `description`; `README.md`'s coverage section and quick checks;
`references/13-sources.md`; `agents/openai.yaml`; and
`scripts/validate_skill_bundle.py`'s `REQUIRED_PATHS` were all updated to match
(bundle now reports 74 files, up from 59). The sibling `skill-router` skill and
the repository README were extended with the same routing keywords.

All four new scripts are pure Python standard library and were verified
numerically against independently recomputed closed forms, not merely for syntax:

- `multiple_scattering.py` was checked against the PDG Highland expression
  recomputed inline in the tests, including its exact `1/(beta p)` scaling
  (doubling rigidity halves the angle to 15 decimal places), the `sqrt(x/X0)`
  scaling with the logarithmic correction accounted for separately, and the fact
  that the explicit charge factors cancel in the prefactor (`p = zR`) and survive
  only inside the logarithm. The logarithmic correction turns negative for
  extremely thin layers; the clamp to zero (an RMS may not be negative) was
  verified rather than left to produce a negative angle. The Gluckstern intrinsic
  term was checked against its closed form, its exact linearity in rigidity, and
  its quadratic improvement with lever arm (a factor 4 for a doubled arm, to 12
  decimal places). The crossover rigidity was verified to be exactly where the two
  terms are equal, and the maximum detectable rigidity to be exactly where the
  quadrature sum reaches 1. For the shipped example stack the resulting values
  (0.0357 total x/X0, a 1.07% scattering term, a 33.2 GV crossover, a 3.1 TV MDR)
  were also confirmed by hand.
- `calorimeter_resolution.py` was validated by exact closure: the shipped asset is
  generated analytically from a = 0.10 sqrt(GeV), b = 0.20 GeV, c = 0.007, and the
  fit recovers all three to better than 1e-10 with a maximum residual in squared
  resolution of 2.6e-17. Three further parameter sets were recovered the same way,
  including one with a genuinely zero noise term (recovered to ~7e-9 absolute,
  limited by the conditioning of the 1/E^2 column). The determined case - exactly
  three distinct energies for three unknowns - was confirmed to pass through every
  point. The three analytic crossover energies (b^2/a^2, a^2/c^2, b/c) were checked
  both against their closed forms and by confirming the corresponding term
  contributions are equal there. A fit whose input keeps falling faster than
  1/sqrt(E) drives the constant term negative; that case was verified to be
  reported as a flagged failed separation with `constant: null`, not square-rooted
  into a NaN.
- `pid_separation_power.py` was checked against the defining identity
  `p = m beta gamma`, against the exact inversion `m = p sqrt(1/beta^2 - 1)`, and
  against the `dm/m = gamma^2 dbeta/beta` amplification that the reference text
  claims. Time of flight was checked against `L/(beta c)`, the timing-to-velocity
  conversion against `beta c sigma_t / L`, and TOF separation was confirmed to fall
  as roughly the inverse square of momentum (a factor between 3.5 and 4.5 for a
  doubled momentum). The separation ceiling was verified to be exactly where
  separation equals the requested threshold, to rise with both a longer path and
  better timing, and to be reported as `None` when a species pair is never
  separated. The Bethe-Bloch evaluation reproduces the textbook ionization minimum:
  scanning muons in silicon places it at beta*gamma = 3.17 with a loss of
  1.694 MeV cm^2/g, against the PDG value of about 1.66 MeV cm^2/g near
  beta*gamma = 3.5 - the small excess and the slightly lower position are the
  expected consequence of omitting the density-effect correction, which the script
  reports explicitly (`density_effect_omitted`) and flags when evaluated in the
  relativistic rise. The exact `z^2` charge scaling was verified to 9 decimal
  places.
- `cherenkov_angle.py` was checked against `cos(theta_c) = 1/(n beta)` directly,
  against the threshold `p_thr = m/sqrt(n^2 - 1)` (and, independently, by
  confirming that beta at that momentum equals exactly 1/n), against the
  saturation angle `arccos(1/n)` and the approach to it at high momentum, against
  the `sin^2(theta_c)` photon yield, the `1/sqrt(N)` improvement of the per-track
  angular resolution, and the `dbeta/beta = tan(theta_c) sigma_theta` propagation.
  Threshold ordering across pion, kaon, and proton was confirmed, and a
  below-threshold species was verified to report no ring rather than a spurious
  angle. For an n = 1.05 radiator the resulting thresholds (0.436, 1.542 and
  2.931 GeV/c) and the 309.8 mrad saturation angle were confirmed by hand.
- All four CLIs were exercised for invalid input (a stack file missing a required
  field, fewer than three distinct energies, two identical species, a refractive
  index below 1) and confirmed to fail with a clear one-line message and a nonzero
  exit code rather than a raw traceback.
- 69 new tests were added to `tests/test_helpers.py` (29 pre-existing + 69 new =
  98 total, `python3 -m unittest discover -s tests -v`) covering all of the above.

Additional structural checks for this pass: every relative Markdown link in the
package was confirmed to resolve to an existing file, and the new references,
scripts, and assets were grepped for experiment names (AMS, CMS, ATLAS, ALICE,
LHCb and others) to confirm the technology-organized, experiment-agnostic framing
holds and that no synthetic value is presented as a real detector's measurement.

## Astroparticle physics expansion pass (2026-09-09)

Added eight reference files covering astroparticle and cosmic-ray physics
alongside the existing collider-physics content:
`references/32-cosmic-ray-spectrum-and-composition.md`,
`references/33-extensive-air-showers.md`,
`references/34-ground-based-detection-arrays.md`,
`references/35-imaging-atmospheric-cherenkov.md`,
`references/36-neutrino-astronomy.md`,
`references/37-space-based-direct-detection.md`,
`references/38-multimessenger-analysis.md`, and
`references/39-astroparticle-statistics.md`. Added four new standard-library
scripts implementing the formulas those references rely on -
`scripts/li_ma_significance.py`, `scripts/geomagnetic_cutoff.py`,
`scripts/cr_spectrum_powerlaw_fit.py`, and `scripts/xmax_gaisser_hillas.py` -
plus `assets/cosmic_ray_spectrum.example.json` as a synthetic input, and
`tests/test_astroparticle.py` as a separate test module (kept apart from
`tests/test_helpers.py` given the distinct domain). `SKILL.md`'s title,
frontmatter `description`, reference-routing table, executable-resources list,
analysis invariants (three new entries: ON/OFF region non-overlap and trials
accounting, top-of-atmosphere vs. modulated flux and cutoff reporting, and no
single-observable composition claims given the muon-content/X_max
discrepancy), and example requests; `README.md`'s title, quick checks,
coverage section, and example prompts; `references/13-sources.md` (new
citations, using plain-text book/journal citations rather than a guessed URL
for sources without one, and hyperlinks only to stable official homepages);
`agents/openai.yaml` was left unchanged (its metadata is already
domain-agnostic); and `scripts/validate_skill_bundle.py`'s `REQUIRED_PATHS`
were all updated to match (bundle now reports 88 files, up from 74). The
sibling `skill-router` skill and the repository README were extended with the
same routing keywords.

All four new scripts are pure Python standard library and were verified
numerically, not merely for syntax:

- `li_ma_significance.py` was checked against the closed-form boundary cases:
  `N_off = 0` reduces to `S = sqrt(2*N_on*ln(2))` for alpha=1 (confirmed to
  10 decimal places), `N_on = N_off = 0` returns exactly zero by convention,
  and `N_on = alpha*N_off` (zero excess) returns exactly zero rather than a
  tiny nonzero value from floating-point cancellation in the radicand. The
  sign of the significance was confirmed to track the sign of the excess in
  both directions (a symmetric-magnitude check swapping `N_on`/`N_off`), and
  significance was confirmed to increase monotonically with a growing excess
  at fixed alpha. Invalid input (negative or non-integer counts, nonpositive
  alpha) was confirmed to raise a clear error, and the CLI was confirmed to
  match the library function and to fail cleanly (no traceback) on bad input.
- `geomagnetic_cutoff.py` was checked against the textbook equatorial value
  (`59.6 / (1+sqrt(2))^2 ~= 10.23 GV` at the geomagnetic equator, sea level,
  matching the standard dipole-approximation figure quoted in the cosmic-ray
  literature), confirmed to fall monotonically from equator to pole, to be
  symmetric under latitude sign, to vanish at the pole, and to decrease with
  increasing altitude (larger `r`). The kinetic-energy-per-nucleon conversion
  was checked to stay strictly below the rigidity (momentum) it derives from,
  as required for a nonzero rest mass, and to reject non-positive or
  inconsistent (A < Z) charge/mass-number input. The CLI was confirmed to
  match the library function.
- `cr_spectrum_powerlaw_fit.py` was validated by exact closure: a single
  power law generated with no scatter at index 2.7 is recovered to 8+ decimal
  places with a max log-flux residual below 1e-8, and a two-segment synthetic
  spectrum (index 2.7 below and 3.1 above a break at 4e15 eV, continuous at
  the break) has both indices and their difference recovered to 8+ decimal
  places by the segmented fit - while a single power law forced onto the same
  broken spectrum shows a residual more than 10x larger than either segment
  of the correct fit, confirming the tool actually distinguishes a genuine
  break from noise rather than trivially reporting a good fit either way. A
  weighted fit (per-point `sigma_flux` supplied) was confirmed to still
  recover the known index. Degenerate input (fewer than two distinct
  energies, non-positive energy/flux, too few points on one side of a
  requested break) was confirmed to raise a clear error, and the CLI was
  confirmed to match the library function on the shipped asset and to fail
  cleanly on a missing file.
- `xmax_gaisser_hillas.py` was checked against the profile's defining
  property `N(X_max) = N_max` to 1e-9 relative precision, confirmed to be
  smaller on both sides of `X_max` (unimodality), and confirmed undefined
  (`NaN`, not an exception) at or before the depth offset `X0`. The shower
  age was confirmed to equal exactly 1 at `X_max` and 0 at `X0`, and to
  increase monotonically with depth. The half-maximum-depth bisection was
  confirmed to bracket `X_max` (one root below, one above) and to land within
  0.01% of `N_max/2` at both roots. Geometrically invalid input
  (`X_max <= X0`) was confirmed to raise a clear error rather than producing
  a nonsensical or complex result, and the CLI was confirmed to match the
  library function and fail cleanly on bad geometry.
- 38 new tests were added in `tests/test_astroparticle.py` (98 pre-existing
  in `tests/test_helpers.py` + 38 new = 136 total,
  `python3 -m unittest discover -s tests -v`) covering all of the above.

Additional structural checks for this pass: every relative Markdown link in
the eight new reference files was confirmed to resolve to an existing file.
The new references were grepped for named real observatories (Pierre Auger
Observatory, Telescope Array, IceCube, KM3NeT, H.E.S.S., MAGIC, VERITAS, CTA,
AMS-02) - each appears only as a canonical, publicly documented example of a
detection *technique* (e.g. "hybrid surface-array/fluorescence design" or
"in-ice Cherenkov telescope"), never with a specific numeric value presented
as that facility's measurement, consistent with the same requirement enforced
in the detector/reconstruction/simulation pass above. The sources table's new
entries were checked to use plain-text citations (author/title/venue/year)
for books and pre-arXiv journal papers rather than a guessed URL, and
hyperlinks only for stable, well-known official homepages (PDG, Auger,
IceCube, CTA) rather than a specific document path not independently
confirmed.

## Limitations

- ROOT is not installed in the validation environment, so `check_root_cpp_env.sh`
  correctly reports it missing (exit 1) rather than being runnable end to end, and the
  PyROOT-dependent scripts (`inspect_root_file.py`, `check_systematic_variations.py`,
  `compare_root_histograms.py`, `summarize_histogram_statistics.py`,
  `roofit_workspace_summary.py`) and the `.cpp`/`.C` template assets were checked for
  Python syntax only, not executed or compiled against real ROOT headers/libraries.
  This mirrors the same limitation already recorded for RooFit/pyhf/Combine snippets
  before the merge.
- Geant4 is not installed in the validation environment, and no detector
  simulation, reconstruction framework, generator, or conditions database was run.
  The detector, reconstruction, and simulation references
  (`23`-`31`) are methodological guidance checked for internal consistency and
  against the cited PDG and Geant4 documentation; they were not validated against
  a running simulation or a real detector's performance. The four new scripts
  compute design-level analytic estimates (Highland/Gluckstern, the three-term
  calorimeter parameterization, Bethe-Bloch without the density effect, Cherenkov
  kinematics with a single refractive index) and are not substitutes for a track
  fit, a shower simulation, or a ring-reconstruction algorithm.
- The `pid_separation_power.py` dE/dx mode omits the density-effect correction, so
  its numbers above the ionization minimum are optimistic; this is flagged in the
  output rather than silently applied.
- No real experiment data, full-production regression, coverage study, or
  collaboration approval was available. Helper tests do not establish the physical
  correctness of arbitrary analyses.
- The counting reference intentionally limits observed counts and known background to
  at most 500. Extreme tails can underflow in floating-point arithmetic. It is not a
  general statistics package and does not calculate CLs.
- The skill-creator `quick_validate.py` was not run in this environment.
- `geomagnetic_cutoff.py` computes the idealized vertical Stormer dipole cutoff only;
  it does not backtrace particles through a real (non-dipolar, epoch-specific) field
  model, so it does not capture off-vertical arrival directions or the geomagnetic
  penumbra, both flagged explicitly in its docstring and in
  references/37-space-based-direct-detection.md.
- `xmax_gaisser_hillas.py` evaluates a given or externally supplied Gaisser-Hillas
  parameter set; it does not fit those four parameters from raw (X, N) shower-profile
  samples, since that is a nonlinear least-squares problem outside this skill's
  closed-form, no-minimizer script convention (see references/33-extensive-air-showers.md).
- `cr_spectrum_powerlaw_fit.py` fits a spectral index directly from flux points; it
  does not forward-fold through an instrument's energy migration matrix, so it should
  not be used as a substitute for the forward-folding analysis a steeply falling,
  finite-resolution measurement actually requires (see
  references/39-astroparticle-statistics.md).
- `li_ma_significance.py` computes a single ON/OFF significance only; it does not
  itself apply a trials/look-elsewhere correction for a scan over multiple positions,
  energy bins, or time windows (see references/39-astroparticle-statistics.md).
- No real air-shower simulation (CORSIKA or similar), neutrino-telescope Monte Carlo,
  or IACT instrument-response package was run; the astroparticle references
  (`32`-`39`) are methodological guidance checked for internal consistency and
  against the cited textbook/journal sources, not against a running simulation or a
  real observatory's performance.

In an environment with ROOT/PyROOT and skill-creator, additionally run the
ROOT-dependent scripts against a real file and `quick_validate.py`. In the target
analysis environment, perform the relevant physical and statistical checks described
in references/12-validation.md.
