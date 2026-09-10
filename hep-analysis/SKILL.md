---
name: hep-analysis
description: "Use when analyzing collider or astroparticle physics data/simulation: ROOT C++/PyROOT/uproot/awkward/RDataFrame pipelines; event selections, cutflows, histograms, fits, efficiencies, yields, unfolding, systematics, limits; RooFit/RooStats/pyhf/Combine; CMake/root-config builds. Also jets/JES/JER, b-tagging, MET, pileup, tag-and-probe efficiency, BDT/NN classifiers. Also detector subsystems (tracker, ECAL/HCAL, TRD, TOF, RICH, dE/dx, muon), PID, event reconstruction, Geant4 simulation, calibration. Also astroparticle/cosmic-ray physics: spectrum and composition (knee/ankle/GZK), air showers, ground-based arrays, imaging Cherenkov (IACT), neutrino telescopes, space-based direct detection (geomagnetic cutoff, solar modulation), multi-messenger analysis, Li & Ma significance/trials statistics, AMS-02 case study, and cosmic-ray flux from counts/exposure - e.g. 'my ROOT macro' or 'my AMS-02 flux calculation'. Not for unrelated 'root' (Linux/Android root, certificates)."
---

# High-Energy Physics and Astroparticle Physics Experimental Analysis and Statistics

Produce physically traceable, statistically sound, reproducible analyses. Support design, implementation, debugging, review, and explanation. Follow the user's language and established project tools; do not assume an experiment, collision energy, era, or input format. This skill and its reusable resources are maintained in English. Preserve existing physics behavior (cuts, weights, binning, fit models) unless the user explicitly asks for a physics change.

## Working procedure

1. Identify whether the task is inspection, analysis production, statistical inference, refactoring, or review. Inspect project instructions, configurations, entry points, build system, and a small available sample before changing the analysis.
2. Establish the physics objective, data/MC distinction, units, observables, selections, normalization, signal/control/validation regions, parameter of interest (POI), and blinding state. Continue independent inspection when information is missing, and state assumptions. Never invent luminosities, cross sections, calibration values, or correlations for a reported result.
3. Choose the simplest matching API for the task (see API selection below), and read only the relevant references below. Complete a minimal verifiable analysis before scaling to the full dataset. Record software, configuration, sample, and calibration versions.
4. Distinguish successful execution, numerical validation, physical plausibility, and demonstrated statistical coverage. State which checks were not run and why.
5. Deliver the relevant code/configuration, build+run commands, reproduction commands, cutflow, statistical model and diagnostics, assumptions (units, tree/branch names, weights), validation evidence, and limitations. Scale deliverables to the task rather than requiring a full report for every small question.

## API selection

| API | Use for |
|---|---|
| C++ `ROOT::RDataFrame` | new compiled event loops, multithreaded columnar processing, many histograms from one selection, snapshots |
| PyROOT `ROOT.RDataFrame` | ROOT-native workflow with Python orchestration, no compiled helpers needed |
| uproot + awkward-array | Python-native analysis, jagged arrays, fast inspection, no full interactive ROOT |
| `TTreeReader` | manual C++ loops, custom object handling, where RDataFrame would obscure a simple algorithm |
| `SetBranchAddress` | legacy maintenance only - validate addresses/lifetimes carefully |
| RooFit/RooStats, pyhf, Combine | likelihood models, constrained fits, workspaces, toys, limits, intervals |

Don't mix more APIs than needed in one script. If mixing, keep boundaries clear (e.g.
uproot for inspection, RDataFrame for production, ROOT files as interchange).

## Analysis invariants

- Do not silently change cuts, object ordering, binning, weights, corrections, models, parameter bounds, or nuisance correlations during a refactor.
- Preserve signed generator weights. Normalize with the sum of generator weights for the corresponding full production, not the selected entry count. Store both sumw and sumw2.
- Do not count the same events, MC statistical information, or auxiliary measurement twice as independent likelihood information. Remove region overlaps or model them jointly.
- Label observed counts, weighted yields, Asimov expectations, and toy data separately. Arbitrary weighted or background-subtracted data are not ordinary Poisson observations.
- Poisson expectations must be nonnegative. Do not silently clip negative bins; investigate signed weights, sample statistics, binning, or model suitability.
- Propagate shape variations through object corrections, ordering, selections, missing transverse momentum, and category migration where affected. Changing only the final histogram weight is insufficient for a kinematic variation.
- Preserve existing blinding rules and define masks for new analyses. Without authorized unblinding, do not expose masked observations through plots, ratios, logs, temporary tables, or optimization.
- Do not tune a model to obtain a desired significance, exclusion, or goodness-of-fit value. Changes need physical justification and independent validation.
- Do not tune simulation, calibration, or alignment parameters to remove a disagreement in the observable being measured. Tune only on independent control observables, with a stated physical justification, and carry the remaining freedom as a systematic.
- Detector-level quantities are inferred, not observed. Rigidity is `p/q`, not momentum; efficiency is not acceptance; a matched object is matched under a stated criterion. State the definition whenever one of these is quoted.
- Distinguish frequentist confidence intervals from Bayesian credible intervals. Report the statistic, tail convention, nuisance treatment, and validity conditions.
- Never change cuts, weights, binning, or fit models silently during a refactor - if a change risks altering physics output, say so and propose a comparison method (event count per cut, histogram integrals, max absolute/relative bin difference, fit parameters/uncertainties).
- In an ON/OFF or blind sky-scan search, the OFF/background region must not overlap the ON region, and a reported significance must account for the number of independent trials (positions, energy bins, time windows, source catalogs) actually tested, not just the one presented.
- Distinguish a flux measured at the top of the atmosphere or at an instrument from one corrected to the local interstellar spectrum; state the solar-modulation epoch/potential and the geomagnetic cutoff applied whenever a low-rigidity cosmic-ray flux is reported.
- Do not draw a composition conclusion from a single shower observable (X_max or muon content alone) without stating the hadronic interaction model assumed and checking consistency against the other observable, given the current muon-content/X_max modeling discrepancy.
- A flux or rate reported from raw counts must use an exact Poisson interval, not a Gaussian sqrt(N) approximation, whenever counts are low enough for the two to disagree (routine in a steeply falling spectrum's high-energy tail); state the exposure (effective area/geometric factor times live time times solid angle) and bin width used, separately from the raw count.
- A ratio or fraction of two yields (e.g. a positron fraction or an antiproton/proton ratio) must use the yields' actual covariance, not an independence assumption, whenever they share a systematic (the same acceptance, exposure, or background-template shape) - state which systematics are shared and whether they were treated as correlated.

## Reference routing

| Task | Read |
|---|---|
| Analysis design, quality masks, triggers, blinding | [Analysis contract](references/01-analysis-design.md) |
| ROOT/columnar I/O, event loops, performance, ownership | [Data pipelines](references/02-data-pipelines.md) |
| Luminosity, cross sections, signed weights, cutflows | [Normalization](references/03-weights-normalization.md) |
| Histograms, efficiencies, covariance, plotting (statistics) | [Histograms and uncertainties](references/04-histograms-efficiencies.md) |
| Control regions, ABCD, fake rates, sidebands, transfer factors | [Background estimation](references/05-backgrounds.md) |
| Detector/theory uncertainties, MC statistics, correlations, variation implementation | [Systematics](references/06-systematics.md) |
| Binned/unbinned likelihoods, RooFit, nuisance parameters, workspace inspection | [Models and fitting](references/07-likelihood-fitting.md) |
| Intervals, significance, CLs, toys, Bayesian inference | [Statistical inference](references/08-inference.md) |
| pyhf, HistFactory, Combine workspaces/datacards | [Statistical tools](references/09-statistical-tools.md) |
| Cross sections, response matrices, unfolding, combinations | [Measurements and unfolding](references/10-measurements-unfolding.md) |
| Classifiers, leakage, mass sculpting | [Machine learning](references/11-ml-analysis.md) |
| Debugging, verification, preservation, review | [Validation](references/12-validation.md) |
| Versions and methodological sources | [Primary sources](references/13-sources.md) |
| C++/ROOT/RDataFrame code patterns, TTreeReader, style, build commands | [C++/ROOT coding](references/14-cpp-root-coding.md) |
| CMake and root-config builds, project scaffolding | [Build setup](references/15-cmake-and-build.md) |
| Debugging ROOT/PyROOT/C++ (missing symbols, dictionaries, fits) | [Debugging ROOT](references/16-debugging-root.md) |
| Python CLI structure, PyROOT/uproot/awkward code conventions | [Python coding](references/17-python-hep-coding.md) |
| Naming conventions, comments, file-level documentation requirement | [Code conventions](references/18-code-conventions.md) |
| General C++ class/struct/RAII/ownership/inheritance design | [C++ design guidelines](references/19-cpp-balanced-design-guidelines.md) |
| Jet clustering, JES/JER, b-tagging, MET, pileup jets, overlap removal | [Physics objects](references/20-physics-objects-jets-btagging-met.md) |
| Tag-and-probe, trigger turn-ons/prescales, luminosity, pileup reweighting | [Triggers, luminosity, pileup](references/21-triggers-luminosity-pileup.md) |
| BDT/NN classifier choice, training, feature engineering, calibration | [Multivariate classifiers](references/22-multivariate-classifiers-bdt-nn.md) |
| Subsystem layout, rigidity vs. momentum, material budget, acceptance, resolution vocabulary | [Detector systems overview](references/23-detector-systems-overview.md) |
| Silicon/gas tracking, pattern recognition, Kalman fit, charge confusion, vertexing | [Tracking and vertexing](references/24-tracking-and-vertexing.md) |
| EM/hadronic showers, sampling vs. homogeneous, stochastic/noise/constant terms, e/h non-compensation, leakage | [Calorimetry](references/25-calorimetry-ecal-hcal.md) |
| TRD, TOF, RICH/Cherenkov, dE/dx, muon systems, combined PID likelihoods, isotope separation | [Particle identification](references/26-particle-identification.md) |
| Hits to clusters to tracks to objects, particle flow, ambiguity resolution, reconstruction under pileup | [Event reconstruction](references/27-event-reconstruction.md) |
| Truth matching, reconstruction efficiency/fake rate/purity, resolution and bias, scale factors | [Reconstruction performance](references/28-reconstruction-performance-and-truth-matching.md) |
| Generators, LHE/HepMC, matching/merging, negative weights, PDF and scale variations | [Event generation](references/29-event-generation.md) |
| Geant4 geometry/physics lists/production cuts, digitization, fast simulation, simulation validation | [Detector simulation](references/30-detector-simulation.md) |
| Test-beam and in-situ calibration, alignment weak modes, conditions time dependence | [Calibration and alignment](references/31-calibration-and-alignment.md) |
| Cosmic-ray spectrum features (knee/ankle/GZK), composition, acceleration, propagation, solar modulation | [Cosmic-ray spectrum and composition](references/32-cosmic-ray-spectrum-and-composition.md) |
| Extensive air showers, Heitler-Matthews model, Gaisser-Hillas/Greisen profiles, X_max, muon puzzle | [Extensive air showers](references/33-extensive-air-showers.md) |
| Surface detector arrays, fluorescence detectors, hybrid reconstruction, atmospheric monitoring | [Ground-based detection arrays](references/34-ground-based-detection-arrays.md) |
| IACT gamma-ray astronomy, Hillas parameters, gamma/hadron separation, ON/OFF significance | [Imaging atmospheric Cherenkov](references/35-imaging-atmospheric-cherenkov.md) |
| Neutrino telescopes, track/cascade/double-bang topologies, atmospheric background rejection | [Neutrino astronomy](references/36-neutrino-astronomy.md) |
| Balloon/satellite direct detection, geomagnetic cutoff, solar modulation, antiparticle excesses, periodicity/time-structure search (epoch-folding, Lomb-Scargle, charge-sign drift diagnostic) | [Space-based direct detection](references/37-space-based-direct-detection.md) |
| Multi-messenger coincidence analysis, alert follow-up, trials/timing/pointing systematics | [Multi-messenger analysis](references/38-multimessenger-analysis.md) |
| Li & Ma significance, sky-scan/catalog trials factor, exposure/forward-folding for steep spectra | [Astroparticle statistics](references/39-astroparticle-statistics.md) |
| AMS-02 (ISS spectrometer): TRD/tracker/TOF/RICH/ACC/ECAL combination, orbital/solar-cycle systematics, positron-fraction/antiproton-ratio pattern, primary/secondary composition (B/C ratio), temporal-structure worked examples, servicing/upgrade history | [AMS-02 case study](references/40-ams02-case-study.md) |
| Authoring a canonical worked example (Weak vs. Expert contrast) for `examples/` | `agile-development`'s [example-authoring reference](../agile-development/references/example-authoring.md) (requires `agile-development` installed alongside this skill) |

## Code file requirement

When creating or modifying any code file (C++ source/headers, ROOT macros, PyROOT/
uproot scripts, CMake files, config loaders), include a short introductory comment
block at the top covering purpose, what the code does, and usage notes/dependencies/
assumptions (build/run command, expected input format and tree/branch names, units,
weight conventions, ROOT version, preconditions). For existing files, add it if
missing or update it if outdated. See [Code conventions](references/18-code-conventions.md)
for the full naming, comment, and documentation convention.

## Executable resources

- `scripts/audit_histograms.py`: audit the JSON histogram bundle defined by this skill. Detect malformed arrays, nonfinite values, negative variances, negative Poisson rates, missing variations, and identical templates. It does not read ROOT, prove physical correctness, or infer whether Up/Down labels are reversed.
- `scripts/counting_reference.py`: exact Poisson tails and flat-signal-prior Bayesian bounds for a single bin with known background. This is a small-model cross-check, **not a general CLs or nuisance-parameter calculator**.
- `scripts/inspect_root_file.py` / `scripts/inspect_root_file.C`: list keys, trees, branches, and histogram metadata in a real ROOT file (requires PyROOT/ROOT).
- `scripts/check_root_cpp_env.sh`: verify ROOT/root-config/compiler availability and print resolved versions.
- `scripts/new_root_cpp_project.sh`: scaffold a CMake-based ROOT C++ project.
- `scripts/check_systematic_variations.py`: verify Up/Down variation histograms in a real ROOT file exist, aren't swapped, aren't byte-identical to nominal, and share nominal binning (requires PyROOT; complements `audit_histograms.py`, which works on the JSON bundle format instead).
- `scripts/compare_root_histograms.py`: diff two histograms across ROOT files (integral, bin-by-bin, max abs/relative difference) for regression checks (requires PyROOT).
- `scripts/make_yield_table.py`: render a yield CSV (region/sample/yield[/uncertainty]) as Markdown tables (standard library only).
- `scripts/tag_and_probe_efficiency.py`: exact Clopper-Pearson binomial confidence interval for a pass/total efficiency measurement (standard library only; not a Gaussian/Wald approximation).
- `scripts/pileup_reweight.py`: per-bin data/MC pileup reweighting factors from two profile histograms, with a closure-check mean and explicit flagging (not silent inf/0) of data-populated bins where MC has zero probability (standard library only).
- `scripts/multiple_scattering.py`: PDG Highland scattering angle, accumulated material budget, and the scattering/intrinsic terms of a magnetic spectrometer's rigidity resolution, with the crossover rigidity and maximum detectable rigidity (standard library only; a design-level estimate, **not** a substitute for a track fit).
- `scripts/calorimeter_resolution.py`: fit and evaluate the three-term calorimeter resolution `(sigma_E/E)^2 = a^2/E + b^2/E^2 + c^2`. The model is linear in `(a^2, b^2, c^2)`, so the fit is an exact linear least squares with no minimizer; a coefficient that fits negative is reported as a failed separation rather than square-rooted into a NaN (standard library only).
- `scripts/pid_separation_power.py`: species separation in sigma for time-of-flight, Bethe-Bloch ionization, and directly-supplied velocity resolution, with the mass resolution's `gamma^2` degradation and the momentum ceiling where separation is lost. The dE/dx evaluation **omits the density-effect correction** and flags when it is in the relativistic rise (standard library only).
- `scripts/cherenkov_angle.py`: RICH threshold momenta, Cherenkov angle and its saturation, photon yield, per-track angular resolution, and the resulting velocity/mass resolution and species separation (standard library only; a design estimate, not a ring-reconstruction simulation).
- `scripts/summarize_histogram_statistics.py`: entries, integral, sum of weights, bin edges, negative bins for a histogram in a ROOT file (requires PyROOT).
- `scripts/roofit_workspace_summary.py`: summarize a `RooWorkspace` (variables, PDFs, datasets, functions, snapshots) (requires PyROOT).
- `scripts/li_ma_significance.py`: exact Li & Ma (1983) likelihood-ratio significance for an ON/OFF counting measurement, including the N_on=0/N_off=0 boundary terms (standard library only; no trials/look-elsewhere correction - see reference 39).
- `scripts/geomagnetic_cutoff.py`: analytic vertical Stormer dipole geomagnetic cutoff rigidity at a given geomagnetic latitude/altitude, with an optional conversion to minimum kinetic energy per nucleon for a given (Z, A) (standard library only; an idealized-dipole first-order estimate, **not** a substitute for particle backtracing through a full field model).
- `scripts/cr_spectrum_powerlaw_fit.py`: exact (weighted) linear least-squares power-law fit to a flux-vs-energy spectrum in log-log space, single or two-segment (given a break energy), reporting the index(es) and their uncertainty (standard library only).
- `scripts/xmax_gaisser_hillas.py`: evaluate the Gaisser-Hillas air-shower longitudinal profile, shower age, and half-maximum depths for a given or externally fitted parameter set (standard library only; an evaluator, not a nonlinear curve fitter).
- `scripts/orbit_averaged_geomagnetic_cutoff.py`: minimum, maximum, and time-weighted average vertical Stormer cutoff over an inclined low-Earth orbit (e.g. the ISS), by direct numerical quadrature over the orbit's latitude range (standard library only; a planning-level estimate, not a substitute for ephemeris-based backtracing).
- `scripts/solar_modulation_force_field.py`: force-field approximation converting between the local interstellar spectrum and the flux measured at 1 AU, in both directions - modulate a LIS model to a predicted top-of-atmosphere flux, or demodulate one measured flux point back to its equivalent LIS value (standard library only).
- `scripts/particle_ratio_with_uncertainty.py`: ratio or fraction of two independent yields (e.g. a positron-fraction- or antiproton/proton-ratio-style measurement) with exact delta-method error propagation, including an optional correlation term (standard library only; first-order/Gaussian approximation).
- `scripts/cosmic_ray_flux.py`: differential flux from an observed count, exposure, and bin width, with an exact Poisson confidence interval (not a Gaussian sqrt(N) approximation) and optional background subtraction (standard library only; exact interval limited to counts where the underlying Poisson-tail tool's 0-500 rate range suffices - reports a clear error otherwise rather than a silently truncated interval).
- `scripts/validate_skill_bundle.py`: check that this package's own files (SKILL.md, README.md, references, scripts, assets, tests) are all present and non-empty, and that SKILL.md/README.md have their expected structure (standard library only).
- `assets/histograms.example.json`: synthetic audit input for `audit_histograms.py`; see the [schema](references/12-validation.md).
- `assets/pileup_profiles.example.json`: synthetic data/MC pileup profile pair for `pileup_reweight.py`.
- `assets/detector_stack.example.json`: synthetic layered detector stack (material budget per layer, field, lever arm, point resolution) for `multiple_scattering.py`. Illustrative geometry, not any real experiment.
- `assets/calorimeter_response.example.json`: synthetic `(E, sigma_E/E)` points generated exactly from stated `a`, `b`, `c` values, so a correct fit recovers them; input for `calorimeter_resolution.py`.
- `assets/cosmic_ray_spectrum.example.json`: synthetic broken-power-law flux points generated exactly from stated indices and a break energy, so a segmented fit recovers them; input for `cr_spectrum_powerlaw_fit.py`.
- `assets/analysis-contract.yaml`, `assets/systematics.csv`, `assets/report-template.md`: reusable analysis, correlation, and reporting templates.
- `assets/pyhf-counting.json`: a synthetic single-bin workspace. Never present its values as experimental results.
- `assets/uproot_awkward_analysis.py`, `assets/pyroot_rdataframe_analysis.py`, `assets/cpp_rdataframe_analysis.cpp`, `assets/rdf_analysis.cpp`: starting templates (copy and adapt) for uproot+awkward and RDataFrame (Python/C++) selection-and-histogram skeletons.
- `assets/pyroot_roofit_signal_background.py`, `assets/fit_histogram.cpp`, `assets/plot_branch.C`: RooFit signal+background fit and fitting/plotting macro templates.
- `assets/CMakeLists.txt`, `assets/analysis_config.yaml`, `assets/systematics_config.yaml`, `assets/statistical_histogram_config.yaml`, `assets/combine_datacard_template.txt`: build and config templates (copy and adapt).
- `tests/test_helpers.py`: standard-library tests for `audit_histograms.py`/`counting_reference.py`/`tag_and_probe_efficiency.py`/`pileup_reweight.py`. Run `python3 -m unittest discover -s tests -v`.

Resolve relative paths from the skill directory. Read a script's `--help` before use. Write analysis outputs to the appropriate user-project location. Use the project's existing ROOT, PyROOT, uproot, or pyhf environment; loading this skill does not require installing the full software stack, but the PyROOT-dependent scripts above need one.

## Example requests

- "Review this NanoAOD selection and explain the yield difference for the negative-weight sample."
- "Design a simultaneous likelihood for three control regions and identify shared nuisances."
- "Review my CLs limit, including low-statistics and parameter-boundary effects."
- "Build a reproducible differential cross-section analysis with response uncertainties and covariance."
- "Inspect this NanoAOD file and list the muon-related branches."
- "Write an RDataFrame selection for >=2 muons with pT>25 GeV and make a pT histogram with a cutflow."
- "My uproot script gives different yields after a refactor - help me find why."
- "Check that my JES Up/Down systematic histograms aren't swapped or empty."
- "Build a CMake project for this ROOT C++ analysis."
- "Why does my spectrometer's rigidity resolution get worse both below 5 GV and above 200 GV?"
- "Up to what momentum can this TOF separate pions from kaons, and would a RICH do better?"
- "Generate a canonical `examples/` entry for this skill contrasting a weak vs. expert
  JES systematic on a cutflow-based cross-section measurement."
- "My data and simulation disagree in tracking efficiency at low momentum but agree at high - where should I look?"
- "Review how this analysis defines truth matching and reconstruction efficiency."
- "What should I check before trusting fast simulation for this measurement?"
- "Is a 4.8-sigma excess in my ON/OFF gamma-ray source search significant after accounting for the sky scan?"
- "Why does my composition analysis using X_max disagree with the one using muon content?"
- "Estimate the geomagnetic cutoff for a low-inclination low-Earth orbit and what minimum rigidity my spectrometer needs to see."
- "Review my IceCube-style point-source likelihood - is the background estimation and trials factor right?"
- "Fit the spectral break in this cosmic-ray flux and check whether it's consistent with a knee-like feature."
- "What geomagnetic cutoff range does an AMS-02-like instrument on the ISS orbit see, and how should that shape my low-rigidity selection?"
- "Convert this local-interstellar proton spectrum to what we'd expect at 1 AU during solar minimum vs. solar maximum."
- "Propagate the uncertainty on a positron fraction from independent positron and electron template-fit yields."
- "Compute the differential flux and its statistical uncertainty from these raw counts, exposure, and bin width."

See [README.md](README.md) for installation and cross-agent use. For the broader engineering workflow around this code (scoping, tests, review discipline), pair with a general software-engineering skill if one is available.
