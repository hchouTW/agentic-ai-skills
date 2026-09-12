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

## AMS-02 case study and cosmic-ray flux/statistics pass (2026-09-09)

Added one reference file, `references/40-ams02-case-study.md`, applying the
generic detector-technology references (`23`-`26`) and
[space-based direct detection](references/37-space-based-direct-detection.md) to the
Alpha Magnetic Spectrometer (AMS-02) on the ISS as a worked example: its
actual subsystem stack (permanent-magnet tracker, TRD, TOF, RICH, ECAL),
what is distinctive about a decade-plus space-based mission (no on-orbit
repair, orbital thermal cycling, a time-varying geomagnetic cutoff along the
orbit, a mission spanning multiple solar cycles), and the shared
rare-species-measurement pattern (positron fraction, antiproton/proton ratio,
antihelium search). Added four new standard-library scripts -
`scripts/orbit_averaged_geomagnetic_cutoff.py`,
`scripts/solar_modulation_force_field.py`,
`scripts/particle_ratio_with_uncertainty.py`, and `scripts/cosmic_ray_flux.py`
(the last per explicit request for general cosmic-ray flux calculation and
statistics, not AMS-02-specific) - plus `tests/test_ams02.py` (36 new tests).
`SKILL.md`'s frontmatter `description`, reference-routing table,
executable-resources list, two new analysis-invariant entries (exact Poisson
statistics for low-count flux, and correlation-aware ratio/fraction
uncertainty), and example requests; `README.md`'s quick checks, coverage
section, and example prompts; `references/13-sources.md` (an AMS-02 entry,
left without a pinned URL per this skill's sourcing discipline, since no
specific NASA/AMS page URL was independently confirmed in this pass); and
`scripts/validate_skill_bundle.py`'s `REQUIRED_PATHS` were all updated to
match (bundle now reports 94 files, up from 88). The sibling `skill-router`
skill and the repository README were extended with the same routing
keywords.

All four new scripts were verified numerically, not merely for syntax, and
two real defects were found and fixed during this pass:

- **Defect found and fixed**: `orbit_averaged_geomagnetic_cutoff.py`'s
  quadrature ceiling-search helper had its bracket-growth condition
  inverted - it grew the search bound while the tail probability was *above*
  a threshold instead of *below* it, which for `cosmic_ray_flux.py`'s exact
  Poisson interval search (reused independently, see below) caused every
  call to spuriously report the interval as unbounded. Fixed to grow the
  bracket only while the (monotonically increasing) tail has not yet reached
  the target probability, matching the standard bisection precondition.
- **Defect found and fixed**: `cosmic_ray_flux.py`'s exact Poisson interval
  had its lower- and upper-bound target probabilities swapped (using
  `1 - alpha/2` where the Garwood formula requires `alpha/2` for the lower
  bound, and vice versa for the upper bound), which silently produced a
  lower bound greater than the upper bound. Caught by cross-checking the
  n=42 interval against an independently computed `scipy.stats.chi2`
  Garwood-formula value during development (35.545043400971, 49.5323366625
  at 68.27% confidence) and confirming the two disagreed before the fix and
  matched to 9+ significant figures afterward; also re-checked at 90%
  confidence (31.938130721517, 54.323946486754) with the same exact
  agreement. `scipy` was used only for this one independent development-time
  cross-check and is not a dependency of the shipped script or test suite
  (both remain standard-library only; the test file hardcodes the
  cross-checked expected values).
- `orbit_averaged_geomagnetic_cutoff.py` was further checked to reduce to the
  single-latitude `geomagnetic_cutoff.py` value for a near-equatorial
  (1-degree) inclination, to have its minimum cutoff fall monotonically with
  increasing inclination, to bracket the equator-to-turning-point latitude
  range exactly, and to reject inclinations outside (0, 90] degrees.
- `solar_modulation_force_field.py` was checked for an exact round trip
  (`--modulate` then `--demodulate` on the resulting TOA flux recovers the
  original LIS flux to 8+ decimal places), for the `phi=0` identity (TOA
  flux equals LIS flux exactly when there is no modulation), for the
  modulation direction (a positive `phi` suppresses low-energy flux, as
  physically required), and for a larger energy shift at higher charge at
  fixed `phi` (consistent with `E_LIS = E_TOA + |Z|*phi`).
- `particle_ratio_with_uncertainty.py` was checked against direct arithmetic
  for the central ratio and fraction values, against the closed-form
  independent-quadrature uncertainty formula, for a zero uncertainty on both
  inputs giving exactly zero propagated uncertainty, and for a positive
  correlation coefficient reducing (not increasing) the propagated ratio
  uncertainty as the covariance term requires.
- `cosmic_ray_flux.py` was additionally checked for the flux central value
  matching direct division by exposure and bin width, for background
  subtraction correctly reducing the net count and the reported flux, for a
  larger exposure giving a smaller flux at fixed counts, for a count beyond
  the underlying exact tool's practical range raising a clear error rather
  than silently returning a truncated interval, and for the zero-observed
  case giving a zero lower bound with a positive upper bound.
- All four CLIs were exercised for invalid input (out-of-range inclination,
  missing required LIS parameters, nonpositive yields, a negative count) and
  confirmed to fail with a clear message and nonzero exit code rather than a
  raw traceback, and each CLI was confirmed to match its underlying library
  function's result exactly.

Additional structural checks: every relative Markdown link in
`references/40-ams02-case-study.md` was confirmed to resolve to an existing
file. The file was checked to distinguish real, named AMS-02 subsystems and
mission facts (a permanent, not superconducting, magnet; a TRD, TOF, RICH,
and ECAL; ISS orbital parameters used only descriptively) from any specific
numeric instrument parameter or published measurement value, none of which
are asserted here - the file explicitly directs a reader to verify any such
concrete value against an AMS collaboration publication before quoting it.

## Consistency audit (2026-09-10)

A "check and reorganize" pass with no new content: cross-checked
`scripts/validate_skill_bundle.py`'s `REQUIRED_PATHS` against every file
actually present under `references/`, `scripts/`, and `assets/` (no orphans,
no dangling entries either direction), cross-checked `SKILL.md`'s reference-
routing table against all 40 files under `references/` (every file linked
exactly once, no stale links), read every relative Markdown link's display
text against its actual target, re-ran all 17 standard-library-only quick-
check commands from `README.md` exactly as documented, and `py_compile`'d
every Python file in the package.

- Found and fixed **58 link-text/target mismatches across 19 files**
  (`20-physics-objects-jets-btagging-met.md`,
  `21-triggers-luminosity-pileup.md`, `22-multivariate-classifiers-bdt-nn.md`,
  `23-detector-systems-overview.md`, `24-tracking-and-vertexing.md`,
  `25-calorimetry-ecal-hcal.md`, `26-particle-identification.md`,
  `27-event-reconstruction.md`,
  `28-reconstruction-performance-and-truth-matching.md`,
  `29-event-generation.md`, `30-detector-simulation.md`,
  `31-calibration-and-alignment.md`,
  `32-cosmic-ray-spectrum-and-composition.md`,
  `33-extensive-air-showers.md`, `34-ground-based-detection-arrays.md`,
  `35-imaging-atmospheric-cherenkov.md`, `37-space-based-direct-detection.md`,
  `39-astroparticle-statistics.md`, `40-ams02-case-study.md`): each showed a
  `references/`-prefixed path as the link's visible text while the href
  (correctly, since these files live inside `references/` themselves)
  pointed at the bare sibling filename. Every one of these links already
  resolved correctly - this doesn't change or weaken any "every relative
  Markdown link resolves" claim made in the passes above - the fix is purely
  to the misleading display text, bringing it in line with the majority of
  cross-references in this same file set that already used the bare
  filename as both text and target. This is the same class of bug found and
  fixed in the sibling `agile-development` (3 occurrences) and
  `deep-learning` (17 occurrences) skills in this collection.
- Confirmed `references/19-cpp-balanced-design-guidelines.md` is **not**
  claimed byte-identical to `agile-development`'s/`deep-learning`'s shared
  copy of the same base file anywhere in this package's own docs (unlike
  those two skills, which do make and verify that claim of each other) - it
  legitimately carries an extra hep-analysis-specific scope-setting
  paragraph pointing to `14-cpp-root-coding.md`/`18-code-conventions.md`, so
  no inconsistency here; left untouched.
- All 17 standard-library quick-check commands in `README.md` still exit 0
  and match documented behavior; the ROOT/PyROOT-dependent scripts still
  only parse (`py_compile`) in this environment, consistent with the
  Limitations below (PyROOT itself fails to import here with an unrelated
  Python-ABI error, distinct from "ROOT not installed").
- Bundle validator and the full test suite (172 tests) re-run clean after
  the fixes.

## Example-authoring rollout pass (2026-09-10)

Added this skill's first `examples/` entry, per Phase 3 of `agile-development`'s
example-authoring initiative (see that skill's `references/example-authoring.md`
for the generation prompt and format spec this follows). One pilot example, not
a bulk batch.

- Added a one-line pointer to `agile-development`'s
  `references/example-authoring.md` to the "Reference routing" table in
  `SKILL.md`, explicitly noting the cross-skill dependency (requires
  `agile-development` installed alongside this skill), plus one new "Example
  requests" entry.
- Scaffolded `examples/01-jes-systematic-cutflow.md` with
  `agile-development`'s `generate_skill_example.py --skill hep-analysis --role
  "Senior Experimental Particle Physicist" --use-case "estimating the
  jet-energy-scale systematic uncertainty on a cutflow-based cross-section
  measurement"`, then filled it in by hand around the specific bug named in
  this skill's own `references/06-systematics.md`: "failing to recompute
  [selections] for a shape variation that moves objects across thresholds."
  The weak approach reuses the nominal selection mask for the JES up/down
  variations instead of recomputing it against the shifted jet `p_T`; the
  expert approach recomputes the selection independently per variation and
  reports the resulting migration counts.
- All numeric claims were independently executed with NumPy on a 200,000-event
  synthetic leading-jet `p_T` sample (seeded, `default_rng(20260910)`), not
  merely hand-derived:
  - Extracted both code blocks verbatim from the finished markdown file with a
    regex and imported them as real modules.
  - Weak approach: `eff_up = eff_down = eff_nominal = 0.3213` and a reported
    JES relative uncertainty of exactly `0.000%` - confirmed this is an
    artifact of the unapplied shift, not a coincidence, since `n_up`/`n_down`
    both reduce to `mask_nominal.sum()` by construction.
  - Expert approach: `eff_nominal=0.3213`, `eff_up=0.3340`, `eff_down=0.3079`,
    JES relative uncertainty `4.059%`, with 2,539 events migrating into the
    selection under the +3% shift and 2,677 migrating out under the −3% shift.
  - `python3 scripts/validate_skill_example.py` (from `agile-development`)
    reports `ok` - no structural or placeholder findings.
- No ROOT/PyROOT/uproot installation was available in this environment, so the
  example uses plain NumPy array masking as a dependency-free stand-in for the
  same columnar selection-mask logic `references/17-python-hep-coding.md`
  documents for uproot/awkward pipelines; this is stated explicitly in the
  file's `## Scenario` framing rather than presented as a ROOT-integrated
  analysis. This is a real limitation of this pass, not of the underlying
  physics point, which does not depend on the I/O layer.
- Added `examples/README.md` (one-row index table, linking back to
  `agile-development`'s reference) and added both new files to
  `scripts/validate_skill_bundle.py`'s `REQUIRED_PATHS`. Bundle now reports 96
  files, up from 94.
- Re-ran `python3 scripts/validate_skill_bundle.py` (96 files OK) and
  `python3 -m unittest discover -s tests -v` (172 tests, unchanged - this pass
  added content, not new test code) after the change.

## Cross-repository consistency follow-up (2026-09-10)

A second "check and reorganize" pass across the whole collection (this skill plus
its four siblings) caught two things the same-day Consistency audit above missed:

- `references/22-multivariate-classifiers-bdt-nn.md` referenced `[[deep-learning]]`
  using `[[wiki-link]]` double-bracket syntax - the linking convention this
  repository's own memory files use, not skill markdown, and not the convention
  used anywhere else in this package (a plain backtick-quoted skill name, e.g.
  `` `deep-learning` ``). It rendered as literal double brackets rather than a
  link. Fixed to a plain backtick. A repository-wide `grep -rn '\[\['` confirmed
  this was the only such occurrence in this skill (two more were found and fixed
  the same way in the sibling `agile-development` and `deep-learning` packages).
- This file's own AMS-02 case-study entry linked
  `[space-based direct detection](37-space-based-direct-detection.md)` with no
  `references/` prefix. The earlier Consistency audit's link-text/target check
  only covered links *inside* `references/*.md` files (where a bare sibling
  filename is correct); it didn't catch this prose link inside `VALIDATION.md`
  itself, which sits at the skill root, one directory above the file it points to
  - so the link was genuinely broken, not just misleadingly labeled. Fixed to
  `references/37-space-based-direct-detection.md`. A full anchor-aware relative-
  link check (stripping `#fragment`s before resolving, unlike the quick check
  that first flagged this) was re-run across every `.md` file at the skill root
  and confirmed no other file-level links are broken.

Bundle validator and full test suite (172 tests) re-run clean after both fixes.

## Example expansion to three (2026-09-10)

Expanded this skill's `examples/` from the one pilot entry to three, per the
user's request to bring every installed skill's `examples/` up to three
entries with genuinely different content each.

- Scaffolded `examples/02-tag-and-probe-background-subtraction.md` (role
  "Senior Experimental Particle Physicist") and
  `examples/03-li-ma-significance-iact.md` (role "Astroparticle Physicist /
  IACT Analyst") with `agile-development`'s `generate_skill_example.py`, then
  filled both in by hand, grounded in this skill's own reference material
  rather than invented independently:
  - `02` is built on `references/04-histograms-efficiencies.md`'s guidance
    that "tag-and-probe requires background modeling ... and closure" and its
    stated efficiency-ratio propagation formula `Var(e) ~= Var(A)/B^2 +
    A^2*Var(B)/B^4 - 2*A*Cov(A,B)/B^3`. The weak approach counts raw
    pass/fail window totals as pure signal (efficiency 0.7761, no
    uncertainty); the expert approach sideband-subtracts the signal yield in
    each category first (efficiency 0.8800 +/- 0.0143) and reports a
    background-model systematic (+0.0098) from an alternative sideband
    extrapolation. All four numbers were independently re-executed from the
    finished markdown's own code blocks (not merely hand-derived) and matched
    to 4 decimal places. The weak-approach discussion also notes that the
    shipped `scripts/tag_and_probe_efficiency.py` (exact Clopper-Pearson on a
    pure binomial pass/total count) does not fix this scenario either, since
    it assumes a background-free count - checked by reading that script's own
    docstring rather than assumed.
  - `03` is built on `references/39-astroparticle-statistics.md`'s Li & Ma
    (1983) formula and its look-elsewhere-effect discussion. The weak
    approach uses the naive Gaussian `(N_on - alpha*N_off)/sqrt(N_on +
    alpha^2*N_off)` formula on `N_on=10, N_off=20, alpha=0.2` and reports an
    uncorrected single-trial 1.826 sigma; the expert approach uses the Li & Ma
    likelihood-ratio significance (2.222 sigma) and then applies a Sidak-style
    trials correction for 25 independent scan positions, collapsing it to a
    global 0.578 sigma. The Li & Ma implementation embedded in the example was
    cross-checked line-for-line against the shipped
    `scripts/li_ma_significance.py --on 10 --off 20 --alpha 0.2`, which
    returns the identical `2.2219814487593066` significance.
  - `python3 ../agile-development/scripts/validate_skill_example.py` reports
    `ok` for both files - no structural or placeholder findings.
- Added both new files to `examples/README.md`'s index table and to
  `scripts/validate_skill_bundle.py`'s `REQUIRED_PATHS`. Bundle now reports 98
  files, up from 96.
- Re-ran `python3 scripts/validate_skill_bundle.py` (98 files OK) and
  `python3 -m unittest discover -s tests -v` (172 tests, unchanged - this pass
  added content, not new test code) after the changes.

## Example-authoring: Execution Trajectory pilot (2026-09-11)

Added this skill's first non-Contrast example, per Phase 3 of
`agile-development`'s four-archetype example-authoring revision (see that
skill's `references/example-authoring.md` for the full archetype spec; this
skill depends on `agile-development` being installed alongside it for the
tooling).

- Scaffolded and filled `examples/04-trajectory-cutflow-normalization-
  mismatch.md` (Execution Trajectory archetype, role "Senior Experimental
  Particle Physicist"): a signal MC cutflow yield measuring ~15% high,
  uniformly, at every selection step. Grounded the root cause directly in
  `references/03-weights-normalization.md`'s "Basic convention" (`w_event = (L
  x sigma x k x filter_efficiency / sum_full_gen_weights) x w_gen x
  product(corrections)`, and its explicit warning that "the denominator must
  cover the corresponding production... normally from preselection
  metadata"): a `sum_full_gen_weights` denominator computed from a metadata
  snapshot taken before 6 of 40 production jobs were resubmitted after a
  first-attempt failure, so the merged ntuples' numerator reflects all 40
  jobs while the denominator only reflected 34 - a shape-preserving, uniform
  normalization error rather than a selection-logic bug, which is why no
  single cutflow step was implicated.
- The worked arithmetic (a 1.15 ratio reproducing the reported ~15% excess at
  every step, and the corrected yields matching an independent validation
  skim within stated uncertainty) was checked for internal consistency across
  all four cutflow steps before being written into the example, not just
  asserted.
- `python3 ../agile-development/scripts/validate_skill_example.py
  examples/04-trajectory-cutflow-normalization-mismatch.md` passes with no
  structural or placeholder findings.
- Added one row to `examples/README.md`'s index (now four columns) and added
  the new file to `scripts/validate_skill_bundle.py`'s `REQUIRED_PATHS`.
  Re-ran `python3 scripts/validate_skill_bundle.py` ("Bundle OK: 99 files
  present and non-empty.", up from 98) and
  `python3 -m unittest discover -s tests -v` ("Ran 172 tests" / "OK",
  unchanged - this pass added example content, not new test code).
- Also generalized the "Authoring a canonical worked example" pointer in
  `SKILL.md`'s reference table from "(Weak vs. Expert contrast)" to name all
  four archetypes, matching `agile-development`'s own updated wording.

**Backlog (explicitly deferred, not silently missing):** three archetypes
remain unpiloted for this skill, per the source initiative's Phase 3 backlog
table - Contrast (a systematics writeup, weak vs. expert - distinct from the
three Contrast examples already shipped), Gated Pipeline (systematic-
uncertainty estimation with a closure-test gate), and Decision-Tree (an
unexpected excess in a control region: background vs. new physics vs.
detector effect vs. statistical fluctuation). None were started in this pass.

**Superseded by the pass below (2026-09-11):** the Gated Pipeline and
Decision-Tree backlog items above were fulfilled the same day, each expanded
to three examples rather than a single pilot. The Contrast backlog item (a
systematics writeup) remains open.

## Archetype expansion to three examples each (2026-09-11)

Expanded Execution Trajectory, Gated Pipeline, and Decision-Tree from one
pilot each (the previous entry above) to three examples each, per an explicit
follow-up request that every skill's `examples/` carry three genuinely
different examples per archetype, matching the shape already established for
Contrast. Added 8 new files (`05`-`12`); this skill's `examples/` now holds
12 files total: 3 Contrast, 3 Trajectory, 3 Gated Pipeline, 3 Decision-Tree.

- **Trajectory** (`05`, `06`): a JES systematic template that looks inverted
  in its highest-pt bin - resisting the tempting "swap the Up/Down labels"
  fix per `references/06-systematics.md`'s explicit warning that migration
  can legitimately lower a bin for an Up variation, and instead finding a
  real correction-file copy-paste bug while independently confirming the one
  genuinely-inverted bin via generator-truth migration counts; and an ABCD
  background closure failure traced to a real correlation between the two
  discriminating variables, resolved with a `kappa` correction factor
  measured in an independent validation region (`references/05-backgrounds.md`'s
  "ABCD" section) and verified to reproduce that region's own observation
  exactly.
- **Gated Pipeline** (`07`-`09`): a b-tagging systematic-uncertainty budget
  with a closure-test gate (the backlog item), where the red-team phase finds
  a uniform era-correlation assumption was wrongly double-suppressing a
  calibration-statistics component (`references/06-systematics.md`'s "Source
  inventory" rule against blanket correlation assumptions); an unfolded
  cross-section measurement (`references/10-measurements-unfolding.md`) whose
  red-team phase finds genuine truth-model dependence in one bin via a
  rebuilt response matrix, and excludes that bin explicitly rather than
  quoting an ad hoc extra uncertainty; and an alignment-propagation pipeline
  (`references/31-calibration-and-alignment.md`) whose red-team phase finds a
  single cosmic-ray comparison cannot alone bound a charge-antisymmetric weak
  mode, adding an independent `E/p` symmetry check.
- **Decision-Tree** (`10`-`12`): the backlog's control-region-excess triage
  (background mismodeling vs. new physics vs. detector effect vs. statistical
  fluctuation), selecting the mismodeling branch and tracing it to sideband
  functional-form uncertainty; a tracking-efficiency-drop triage
  (`references/24-tracking-and-vertexing.md`, cross-linking
  `references/31-calibration-and-alignment.md`) selecting a pattern-
  recognition search-window branch and quantifying its efficiency/fake-rate
  tradeoff; and a multi-messenger alert triage
  (`references/38-multimessenger-analysis.md`) selecting the post-hoc-window
  branch and computing a trials-corrected p-value.
- All numeric/arithmetic claims were independently executed with Python
  before being written into the files, not just hand-derived - this caught
  one defect: the multi-messenger trials-corrected p-value was first
  mis-stated as 0.858 and corrected to the actual computed value, 0.847,
  after running `1 - (1 - 0.014)**133` rather than trusting mental
  arithmetic.
- Every new file was validated individually with
  `python3 ../agile-development/scripts/validate_skill_example.py <file>`
  (all report `ok`) before being wired up.
- Added all 8 new file paths to `scripts/validate_skill_bundle.py`'s
  `REQUIRED_PATHS` and one row per file to `examples/README.md`'s index.
  Re-ran `python3 scripts/validate_skill_bundle.py` ("Bundle OK: 107 files
  present and non-empty.", up from 99) and
  `python3 -m unittest discover -s tests -v` ("Ran 172 tests" / "OK",
  unchanged - this pass added example content, not new test code).

**Remaining backlog:** Contrast still has only its original 3 examples (a
systematics writeup, weak vs. expert, from the source initiative's backlog
table, remains unstarted); the other three archetypes are now at parity with
Contrast at 3 examples each.

## Consistency audit (2026-09-11)

A further "check and reorganize" pass, in the same spirit as the same-day
audits of the four sibling skills (each of which found and fixed a real
coverage-documentation gap in `README.md` or its equivalent). Diffed
`scripts/validate_skill_bundle.py`'s `REQUIRED_PATHS` against every real file
on disk, checked every relative Markdown link in the package for a broken
target (using an anchor-aware resolver, matching the method from the
2026-09-10 Cross-repository consistency follow-up above), swept for
`[[wiki-link]]` syntax, confirmed every `references/*.md`/`scripts/*`/
`assets/*` file is mentioned in `SKILL.md`, re-ran all 17 stdlib-only
README-documented quick-check commands plus `check_root_cpp_env.sh` live,
syntax-checked every `scripts/*.py` file, and validated all 12 shipped
`examples/*.md` files.

- **Found and fixed a real gap**, the same class found the same day in
  `agile-development`, `deep-learning`, and `academic-papers`:
  `README.md`'s "Coverage and boundaries" paragraph omitted two topics that
  `SKILL.md`'s own reference-routing table links to explicitly -
  `references/09-statistical-tools.md` (pyhf/HistFactory/Combine
  workspace-and-datacard model mapping: channels, `normfactor`/`normsys`/
  `histosys`/`shapesys`, shared-parameter naming) and
  `references/19-cpp-balanced-design-guidelines.md` (general C++ class/
  struct/RAII/ownership design, as distinct from the ROOT-specific coding
  conventions already named in the same sentence). The only pre-existing
  mentions of "pyhf"/"Combine" in `README.md` were in the "Quick checks"
  section's execution-environment caveat, not in the coverage description
  itself. Added one clause for each to the first coverage paragraph, in the
  same itemized style as the surrounding text; left `SKILL.md`'s own
  frontmatter `description` unchanged, since (unlike `deep-learning`'s, which
  is an exhaustive itemized list) it is already a deliberately terser summary
  that omits many other reference topics by name (debugging, code
  conventions, Python HEP coding) and already names pyhf/Combine once via
  "RooFit/RooStats/pyhf/Combine".
- Considered `references/13-sources.md` (primary-source/version-check
  methodology) for the same treatment and judged it out of scope: it is
  process guidance about how this package sources its own content, not a
  user-facing analysis topic the coverage paragraph enumerates elsewhere
  (comparable to `VALIDATION.md` itself not being described in coverage).
- No other inconsistencies found: `REQUIRED_PATHS` (107 entries) matches the
  file tree exactly in both directions; the one `VALIDATION.md` hit from a
  broken-link grep was a false positive - quoted historical text inside this
  file's own 2026-09-10 entry describing an already-fixed bug, not a live
  link (confirmed by reading the surrounding paragraph and the actual live
  link two paragraphs above it, which already carries the `references/`
  prefix); the one `[[wiki-link]]` hit was the same kind of historical quote
  inside that same entry; all 17 stdlib scripts plus `check_root_cpp_env.sh`
  ran exactly as documented; every `.py` file under `scripts/` parses with no
  syntax errors; all 12 examples pass `agile-development`'s
  `validate_skill_example.py`, 3 per archetype, `examples/README.md`'s index
  (12 rows) matches; `agents/openai.yaml` is a high-level category summary
  (same design choice as `deep-learning`'s and `skill-router`'s) and needed
  no change.
- Re-ran `python3 scripts/validate_skill_bundle.py` ("Bundle OK: 107 files
  present and non-empty.", unchanged - no new files) and
  `python3 -m unittest discover -s tests -v` ("Ran 172 tests" / "OK",
  unchanged) after the fix.

## Second-wave example-authoring pass: Elicitation, Test-First, Postmortem (2026-09-12)

Added three new canonical examples in `agile-development`'s second-wave
archetypes, continuing the four-archetype example-authoring plan (Contrast/
Trajectory/Gated Pipeline/Decision-Tree already covered this skill; this
pass adds Elicitation, Test-First, and Postmortem).

- `examples/13-elicitation-signal-search-ambiguous-request.md`: an
  underspecified "can you check if there's a signal in this dataset?"
  request resolved via 4 clarification questions grounded in
  `references/01-analysis-design.md` (channel, signal-region, background
  model) and `references/08-inference.md` (significance convention,
  look-elsewhere effect) to a fully-specified dijet bump-hunt analysis
  contract.
- `examples/14-test-first-selection-efficiency-numerical-tolerance.md`: a
  weighted-efficiency function (`e = A/B` with the shared-events covariance
  term from `references/04-histograms-efficiencies.md`) red on a naive
  independent-variance implementation (87% overstated uncertainty,
  numerically verified in-session) to green matching a hand-computed
  reference to floating-point precision.
- `examples/15-postmortem-mc-production-pipeline-crash.md`: an overnight
  MC-production crash traced through 5 Whys (no "human error" stop) to a
  batch-pool reconfiguration that silently broke an implicit scratch-cleanup
  assumption, per `references/02-data-pipelines.md`'s "do not silently skip
  failed remote files and report a complete sample" guidance; fixed with an
  automated `TFile::IsZombie()`/`kRecovered` output-integrity gate.
- All three pass `agile-development/scripts/validate_skill_example.py` and
  the diversity checker (`check_example_diversity.py`) shows no
  archetype/skill repeats across the 12-file second-wave batch.
- `examples/README.md`'s intro line updated from "four archetypes" to
  "eight archetypes"; three rows added to its index (15 rows total).
- `scripts/validate_skill_bundle.py`'s `REQUIRED_PATHS` extended with the
  three new example files. Re-ran `python3 scripts/validate_skill_bundle.py`
  ("Bundle OK: 110 files present and non-empty") and
  `python3 -m unittest discover -s tests -v` (172 tests, all passing,
  unchanged from before this pass since no existing test hardcodes the
  example count) after the change.

## Expand all four second-wave archetypes to three examples per skill (2026-09-12)

Every archetype now ships 3 examples per skill (not 3 total, one per skill) -
matching how Contrast/Trajectory/Gated-Pipeline/Decision-Tree already work
here. Added 9 new examples (16-24) to close the gap: Elicitation, Test-First,
and Postmortem each had 1, now have 3; Adversarial Audit had none, now has 3.

- `examples/16-17` (Elicitation): "redo the background estimate", "unfold
  this spectrum" - two underspecified requests resolved via
  `references/05-backgrounds.md`/`06-systematics.md` (method, control
  region, systematic scope) and `references/10-measurements-unfolding.md`
  (method, binning, regularization, uncertainty scope).
- `examples/18-20` (Adversarial Audit): attack a "5.2 sigma - discovery"
  significance claim (uncorrected mass-window look-elsewhere effect, an
  unrecorded unblinding/refit step), a "validated, ready to apply" b-tagging
  scale factor (a kinematic mismatch between control and signal-region
  phase space, a same-sample closure test), and a "closure verified" ABCD
  background estimate (non-factorizable defining variables, a closure test
  performed away from the signal-region-overlapping bins) - grounded in
  `references/09-statistical-tools.md`,
  `references/04-histograms-efficiencies.md`/`31-calibration-and-alignment.md`,
  and `references/05-backgrounds.md`.
- `examples/21-22` (Test-First): a luminosity-weighted-yield numerical
  invariant (a dropped fb^-1 -> pb^-1 factor, understating every yield
  1000x) and a JES-idempotence invariant (a double-corrected jet 5.25 GeV
  high in pT), grounded in `references/03-weights-normalization.md` and
  `references/20-physics-objects-jets-btagging-met.md`.
- `examples/23-24` (Postmortem): a calibration-constant payload silently
  shifting the energy scale for a week, and a shared ntuple-production job's
  path-collision bug overwriting another group's output, grounded in
  `references/31-calibration-and-alignment.md` and
  `references/02-data-pipelines.md`; both 5-Whys chains terminate in a
  missing sanity-check/collision-prevention design gap, not "human error".
- All 9 pass `agile-development/scripts/validate_skill_example.py`; zero
  placeholder markers.
- `examples/README.md`: added 9 rows (16-24), 24 rows total.
- `scripts/validate_skill_bundle.py`'s `REQUIRED_PATHS` extended with the 9
  new example files.
- `agile-development/scripts/check_example_diversity.py`'s cross-skill
  constraint no longer applies to this skill's second-wave archetypes (each
  now deliberately repeats this skill 3x per archetype) - see
  `agile-development/references/example-authoring.md`'s revised "Diversity
  rule". This batch was hand-curated instead: each trio targets a
  conceptually distinct method/claim/invariant/incident.
- Re-ran `python3 scripts/validate_skill_bundle.py` ("Bundle OK: 119 files
  present and non-empty") and `python3 -m unittest discover -s tests -v`
  (172 tests, all passing, unchanged) after the change.

## Renumber examples into canonical per-archetype order (2026-09-12)

The `examples/` numbering had drifted into an inconsistent, historically-
accreted order (the same archetype landing at different numbers in different
skills, and some archetypes' 3 examples not even contiguous within one skill -
e.g. this skill's own Postmortem trio was split across two ranges). Renamed
files (content unchanged) so every skill now uses the same canonical layout:
`01-03` Contrast, `04-06` Trajectory, `07-09` Gated-Pipeline, `10-12`
Decision-Tree, `13-15` Elicitation, `16-18` Adversarial-Audit, `19-21`
Test-First, `22-24` Postmortem - identical across all 5 skills. Updated
`examples/README.md`'s table (re-sorted into the new order) and, where
present, `scripts/validate_skill_bundle.py`'s `REQUIRED_PATHS`; left every
prior dated entry in this file untouched, so filenames named in earlier
entries above refer to a file's *former* name - use the mapping below to
resolve them to the current filename.

Old name -> new name (this skill only):

- `16-elicitation-background-estimate-ambiguous-request.md` -> `14-elicitation-background-estimate-ambiguous-request.md`
- `17-elicitation-unfolding-ambiguous-request.md` -> `15-elicitation-unfolding-ambiguous-request.md`
- `18-adversarial-audit-discovery-significance-claim.md` -> `16-adversarial-audit-discovery-significance-claim.md`
- `19-adversarial-audit-btag-scale-factor-claim.md` -> `17-adversarial-audit-btag-scale-factor-claim.md`
- `20-adversarial-audit-abcd-closure-claim.md` -> `18-adversarial-audit-abcd-closure-claim.md`
- `14-test-first-selection-efficiency-numerical-tolerance.md` -> `19-test-first-selection-efficiency-numerical-tolerance.md`
- `21-test-first-luminosity-weight-invariant.md` -> `20-test-first-luminosity-weight-invariant.md`
- `22-test-first-jes-idempotence-invariant.md` -> `21-test-first-jes-idempotence-invariant.md`
- `15-postmortem-mc-production-pipeline-crash.md` -> `22-postmortem-mc-production-pipeline-crash.md`

Re-ran `python3 scripts/validate_skill_bundle.py` ("Bundle OK: 119 files present and non-empty") and `python3 -m unittest discover -s tests -v` (172 tests, all passing) after the rename. All 24 example files individually re-validated with `agile-development/scripts/validate_skill_example.py` ("ok").

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
- `orbit_averaged_geomagnetic_cutoff.py` treats orbital latitude as geomagnetic
  latitude (ignoring the real dipole's tilt/offset from the rotation axis) and
  assumes a circular orbit; it is a planning-level estimate, not a substitute for
  backtracing a real ephemeris through a full field model (see
  references/40-ams02-case-study.md).
- `solar_modulation_force_field.py` implements only the one-parameter force-field
  approximation; it does not capture charge-sign-dependent drift, heliolatitude
  dependence, or short-timescale transients (Forbush decreases, SEP events), all
  flagged in references/37-space-based-direct-detection.md.
- `particle_ratio_with_uncertainty.py` uses first-order (delta-method/Gaussian) error
  propagation; it is not reliable when either yield's relative uncertainty is large,
  per its own docstring caveat.
- `references/40-ams02-case-study.md` is a methodological case study, not a
  reproduction of any AMS collaboration technical specification or published result;
  no specific numeric instrument parameter or measurement value from AMS-02 is
  asserted in this package, and the sources table intentionally does not pin an
  unverified URL for it.

In an environment with ROOT/PyROOT and skill-creator, additionally run the
ROOT-dependent scripts against a real file and `quick_validate.py`. In the target
analysis environment, perform the relevant physical and statistical checks described
in references/12-validation.md.
