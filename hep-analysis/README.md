# High-Energy Physics and Astroparticle Physics Experimental Analysis and Statistics Skill

A portable Agent Skill maintained entirely in English. Its core is `SKILL.md` plus references resolved through relative paths. It requires no specific MCP server, cloud account, or paid service. It supplies analysis decisions and verification procedures, not experiment-internal calibrations or official collaboration policy.

This package covers writing and reviewing the underlying ROOT C++, PyROOT,
uproot/awkward-array, and RDataFrame code itself (event loops, CMake builds,
debugging, style) in addition to the statistical/physics-analysis layer on top of it
(design, weights, systematics, fitting, inference, unfolding, validation); see
[references/14-cpp-root-coding.md](references/14-cpp-root-coding.md) onward for the
coding-level guidance. This folder was previously shipped as two separate skills - a
coding-focused `hep-analysis` and a statistics-focused `hep-experiment-analysis`;
their content has since been merged into this single `hep-analysis` skill.

## Installation and invocation

Extract the archive and keep the complete `hep-analysis/` folder.

- **Codex:** place the folder in the skill directory used by your environment, commonly `~/.codex/skills/`, or import it through the mechanism supported by your version. Reload skills and invoke `$hep-analysis`. `agents/openai.yaml` supplies optional Codex UI metadata.
- **Claude Code:** copy it to `.claude/skills/hep-analysis/` in the project or `~/.claude/skills/hep-analysis/` for personal use. Invoke `/hep-analysis` or describe a matching task. See the [official Claude Code skill documentation](https://code.claude.com/docs/en/skills).
- **Other agents:** instruct the agent to read `SKILL.md` first and follow its reference routing. Provide the file location explicitly if automatic discovery is unsupported.

This delivery creates a single folder; it does not change other global agent settings. If a separate `hep-experiment-analysis` skill installation still exists from before the merge, remove it - keeping both risks duplicate or conflicting skill triggering. Load references selectively instead of pasting the entire package into global instructions.

## Quick checks

From the skill directory:

```bash
python3 -m unittest discover -s tests -v
python3 scripts/audit_histograms.py assets/histograms.example.json
python3 scripts/counting_reference.py --observed 0 --background 0 --level 0.95
python3 scripts/make_yield_table.py --help
python3 scripts/tag_and_probe_efficiency.py --pass-count 92 --total 100
python3 scripts/pileup_reweight.py assets/pileup_profiles.example.json
python3 scripts/multiple_scattering.py assets/detector_stack.example.json --rigidity 100
python3 scripts/calorimeter_resolution.py --fit assets/calorimeter_response.example.json
python3 scripts/pid_separation_power.py --mode tof --species pi K --momentum 2.0 --path 1.2 --time-resolution 60
python3 scripts/cherenkov_angle.py --index 1.05 --species pi K --momentum 10
python3 scripts/li_ma_significance.py --on 15 --off 5 --alpha 0.5
python3 scripts/geomagnetic_cutoff.py --latitude 41.5
python3 scripts/cr_spectrum_powerlaw_fit.py --input assets/cosmic_ray_spectrum.example.json --break-energy 4.0e15
python3 scripts/xmax_gaisser_hillas.py --n-max 2e7 --x-max 750 --x0 -60 --lambda-param 60 --depths 400,750,900
python3 scripts/orbit_averaged_geomagnetic_cutoff.py --inclination 51.6 --altitude-re 1.0627
python3 scripts/solar_modulation_force_field.py --modulate --energy 1.0 --mass 0.938272 --charge 1 --phi 0.5 --lis-normalization 1e4 --lis-index 2.7
python3 scripts/particle_ratio_with_uncertainty.py --n1 1200 --sigma1 40 --n2 85000 --sigma2 300
python3 scripts/cosmic_ray_flux.py --counts 42 --exposure 1.5e7 --bin-width 10
bash scripts/check_root_cpp_env.sh
```

The first seventeen use only the Python standard library. `check_root_cpp_env.sh` and the
remaining `scripts/*_root*`/`inspect_root_file.*`/`compare_root_histograms.py`/
`summarize_histogram_statistics.py`/`roofit_workspace_summary.py`/
`check_systematic_variations.py` scripts require a
ROOT/PyROOT installation to run (they were syntax-checked, not executed, in an
environment without ROOT - see [VALIDATION.md](VALIDATION.md)). See
[VALIDATION.md](VALIDATION.md) for results and limitations. ROOT, uproot, pyhf, and
Combine snippets require their respective environments; their execution is not
implied by the helper tests.

## Coverage and boundaries

The package covers data quality, object selection, triggers, MC normalization, histograms, efficiencies, data-driven backgrounds, systematic uncertainties, joint likelihoods, fit diagnostics, significance, CLs, intervals, Bayesian inference, cross sections, unfolding, ML validation, and preservation, including pyhf/HistFactory/Combine workspace-and-datacard model mapping (channels, normfactor/normsys/histosys/shapesys, shared-parameter naming) - plus the ROOT C++/PyROOT/RDataFrame/uproot coding layer itself: API selection, event-loop and histogram code patterns, CMake/root-config builds, debugging ROOT/PyROOT errors, code style/naming/documentation conventions, and general C++ class/struct/RAII/ownership design beyond ROOT-specific patterns. It also covers physics-object-level detail (jet clustering/JES/JER, b-tagging, MET, pileup jets, overlap removal), trigger and luminosity methodology (tag-and-probe efficiency measurement with exact binomial intervals, turn-on curves, prescales, luminosity normalization, pileup reweighting), and multivariate-classifier practice (choosing between BDTs/NNs/cuts, feature engineering, training, calibration, and validating classifier stability under systematic variations).

It further covers the detector, reconstruction, and simulation layers beneath all of that, organized by detector technology and assuming no particular experiment: subsystem layout, magnetic spectrometry (rigidity versus momentum, material budget, multiple scattering, maximum detectable rigidity, charge confusion), silicon and gas tracking with pattern recognition and Kalman fitting, vertexing, electromagnetic and hadronic calorimetry (shower development, the stochastic/noise/constant resolution decomposition, e/h non-compensation, leakage), and particle identification across TRD, time-of-flight, RICH/Cherenkov, dE/dx, and muon systems including combined PID likelihoods and isotope separation. On top of that it covers event reconstruction (clustering, track-cluster association and particle-flow subtraction, ambiguity resolution, reconstruction under pileup) and reconstruction performance (truth-matching criteria, efficiency versus fake rate versus purity, resolution and bias, scale factors, closure tests), and the full simulation chain from event generation (matching/merging, negative weights, PDF and scale variations) through Geant4 full simulation (geometry and material budget, physics lists, production cuts, digitization, fast simulation) to calibration and alignment (test-beam versus in-situ, alignment weak modes and charge-antisymmetric rigidity bias, time-dependent conditions).

It also covers astroparticle and cosmic-ray physics: the cosmic-ray spectrum and its knee/ankle/GZK features, composition observables and the muon-content/X_max discrepancy, Fermi acceleration and the Hillas criterion, Galactic propagation and secondary/primary ratios, extensive air showers (Heitler-Matthews toy model, Gaisser-Hillas/Greisen longitudinal profiles, shower universality), ground-based detection (surface arrays, fluorescence, hybrid reconstruction, atmospheric monitoring), imaging atmospheric Cherenkov gamma-ray astronomy (Hillas-parameter and multivariate gamma/hadron separation, ON/OFF background estimation), high-energy neutrino telescopes (track/cascade/double-bang topologies, atmospheric-background rejection), space-based and balloon direct detection (geomagnetic cutoff, solar modulation, antiparticle-excess interpretation), multi-messenger coincidence analysis, and the Li & Ma significance and sky-scan/catalog trials-factor statistics this domain requires. It includes a case study of the Alpha Magnetic Spectrometer (AMS-02) on the ISS - combining a permanent-magnet tracker, TRD, TOF, RICH, and ECAL, its orbital and solar-cycle-driven systematics (inclined-orbit geomagnetic cutoff, solar modulation over a multi-year mission), and the positron-fraction/antiproton-ratio rare-species measurement pattern - plus general differential cosmic-ray flux calculation from raw counts with exact Poisson statistics and background subtraction.

It primarily addresses event counts, templates, and common particle-physics measurements. Time-dependent oscillations, full amplitude analyses, heavy-ion centrality and flow, hardware calibration, and lattice QCD require additional specialized models. Follow the experiment's data-governance and unblinding rules when using internal data.

All maintained instructions, templates, metadata, comments, and validation notes are in English. The skill can still answer a user in their requested language.

## Example prompts

"Use this skill to inspect my sample manifest and cutflow while preserving the selection. Identify yield-changing issues and produce a minimal correction with comparison commands."

"Use this skill to build a nuisance-correlation table and likelihood from my SR/CR templates. Start with Asimov data, assess fit diagnostics and coverage requirements, then calculate the expected limit."

"Write an RDataFrame selection for >=2 muons with pT>25 GeV, make a pT histogram with a cutflow, and set up the CMake build for it."

"Use this skill to check whether my gamma-ray source excess is significant once the sky-scan trials factor is included, and to fit the cosmic-ray spectrum's break energy from my flux table."

"Use this skill to estimate the geomagnetic cutoff range for an AMS-02-like ISS orbit, propagate the uncertainty on a positron-fraction measurement from independent yields, and compute the differential flux and its exact statistical uncertainty from raw counts and exposure."
