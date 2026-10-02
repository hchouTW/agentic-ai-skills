# hep-analysis

An Agent Skill for collider and astroparticle physics analysis: ROOT C++, PyROOT, uproot/awkward and RDataFrame code, plus the physics and statistics layer on top of it (selections, weights, systematics, fits, limits, unfolding, validation, detector and reconstruction questions, cosmic-ray and gamma-ray statistics). It gives analysis decisions and verification procedures. It is not a source of experiment-internal calibrations or official collaboration policy. It needs no MCP server, cloud account or paid service; ROOT, uproot, pyhf and Combine are optional and only needed to run the code you ask for.

All maintained instructions, templates, metadata, comments and validation notes are in English. The skill can still answer in the language you use.

## Installation and invocation

Keep the complete `hep-analysis/` folder (`SKILL.md` plus `references/`, `scripts/`, `assets/`).

- **Codex:** put it in `~/.codex/skills/` (or wherever your version looks), reload skills, and invoke `$hep-analysis`. `agents/openai.yaml` holds optional Codex UI metadata.
- **Claude Code:** copy to `.claude/skills/hep-analysis/` (project) or `~/.claude/skills/hep-analysis/` (personal). Invoke `/hep-analysis` or describe a matching task. See the [Claude Code skills documentation](https://code.claude.com/docs/en/skills).
- **Antigravity:** copy to `.agents/skills/hep-analysis/` (workspace) or `~/.gemini/config/skills/hep-analysis/` (global). It triggers automatically from the skill `description`. See the [Antigravity skills documentation](https://antigravity.google/docs/skills).
- **Other agents:** tell the agent to read `SKILL.md` first and follow its reference routing.

If an old `hep-experiment-analysis` skill is still installed, remove it; it was merged into this one and keeping both can cause duplicate triggering.

## Quick checks

Run from this directory:

```bash
python3 scripts/validate_skill_bundle.py
python3 -m unittest discover -s tests
# ROOT integration tests skip unless PyROOT imports; point them at a ROOT-capable Python:
HEP_ROOT_PYTHON=/opt/homebrew/bin/python3.14 python3 -m unittest tests.test_root_integration -v
# End-to-end pyhf smoke test (skips without numpy + pyhf):
HEP_PYHF_PYTHON=/path/to/python-with-pyhf python3 -m unittest tests.test_end_to_end -v
# Combine datacard check (skips unless combine is on PATH or a wrapper runs it):
HEP_COMBINE_WRAPPER=/path/to/run-in-combine-env python3 -m unittest tests.test_combine_template -v
```

Helper scripts in `scripts/` (most are standard-library Python; each takes `--help`):

```bash
python3 scripts/counting_reference.py --observed 0 --background 0 --level 0.95
python3 scripts/li_ma_significance.py --on 15 --off 5 --alpha 0.5
python3 scripts/cosmic_ray_flux.py --counts 42 --exposure 1.5e7 --bin-width 10
python3 scripts/tag_and_probe_efficiency.py --pass-count 92 --total 100
python3 scripts/make_synthetic_nanoaod.py --out sample.root --events 400 --seed 1  # needs numpy, awkward, uproot
bash scripts/check_root_cpp_env.sh                                                # needs ROOT
```

Model-behavior and routing evals (graded prompts, trigger-query sets, `routing_eval.py`, `evals/`) are run by hand; see `tests/` and [VALIDATION.md](VALIDATION.md) for commands, results and limitations. Open work is in [TODO.md](TODO.md).

## Coverage and boundaries

- Analysis and statistics: design, data quality, object selection, triggers and luminosity, MC normalization, histograms, efficiencies, data-driven backgrounds, systematics, likelihoods, fit diagnostics, significance, CLs, intervals, unfolding, ML validation, preservation, and pyhf/HistFactory/Combine model mapping (references 01-13, 18-20).
- Coding layer: ROOT/PyROOT/RDataFrame/uproot API choice, event-loop patterns, CMake builds, debugging, C++ design and ownership (references 14-17).
- Detectors and reconstruction: tracking, calorimetry, PID, reconstruction performance, event generation, Geant4, calibration and alignment, and a technology-level detector measurement framework (references 21-29, 39-50).
- Astroparticle: cosmic-ray spectrum and composition, air showers, ground arrays, IACT gamma-ray analysis, neutrino telescopes, space-based detection (geomagnetic cutoff, solar modulation), multi-messenger analysis, Li & Ma and trials-factor statistics, flux from counts (references 30-37).
- Defers to siblings: AMS-02-specific design, review, published results and currency checks go to `ams-analysis` (reference 38 is only a short overview); paper writing to `academic-papers`; diagrams to `academic-diagrams`; PyTorch to `deep-learning`.
- Out of scope without extra models: time-dependent oscillations, full amplitude analyses, heavy-ion centrality and flow, hardware calibration, lattice QCD. Follow your experiment's data-governance and unblinding rules for internal data.

## Example prompts

- "Inspect my sample manifest and cutflow while preserving the selection. Find yield-changing issues and give a minimal correction with comparison commands."
- "Build a nuisance-correlation table and likelihood from my SR/CR templates. Start with Asimov data, check fit diagnostics, then compute the expected limit."
- "Write an RDataFrame selection for >=2 muons with pT>25 GeV, make a pT histogram with a cutflow, and set up the CMake build."
- "Is my gamma-ray source excess significant once the sky-scan trials factor is included?"
- "Fit the break energy of the cosmic-ray spectrum in my flux table."
- "Compute the differential flux and exact Poisson uncertainty from raw counts and exposure."
