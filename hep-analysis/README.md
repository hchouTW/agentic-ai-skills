# High-Energy Physics Experimental Analysis and Statistics Skill

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
bash scripts/check_root_cpp_env.sh
```

The first six use only the Python standard library. `check_root_cpp_env.sh` and the
remaining `scripts/*_root*`/`inspect_root_file.*`/`compare_root_histograms.py`/
`summarize_histogram_statistics.py`/`roofit_workspace_summary.py` scripts require a
ROOT/PyROOT installation to run (they were syntax-checked, not executed, in an
environment without ROOT - see [VALIDATION.md](VALIDATION.md)). See
[VALIDATION.md](VALIDATION.md) for results and limitations. ROOT, uproot, pyhf, and
Combine snippets require their respective environments; their execution is not
implied by the helper tests.

## Coverage and boundaries

The package covers data quality, object selection, triggers, MC normalization, histograms, efficiencies, data-driven backgrounds, systematic uncertainties, joint likelihoods, fit diagnostics, significance, CLs, intervals, Bayesian inference, cross sections, unfolding, ML validation, and preservation - plus the ROOT C++/PyROOT/RDataFrame/uproot coding layer itself: API selection, event-loop and histogram code patterns, CMake/root-config builds, debugging ROOT/PyROOT errors, and code style/naming/documentation conventions. It also covers physics-object-level detail (jet clustering/JES/JER, b-tagging, MET, pileup jets, overlap removal), trigger and luminosity methodology (tag-and-probe efficiency measurement with exact binomial intervals, turn-on curves, prescales, luminosity normalization, pileup reweighting), and multivariate-classifier practice (choosing between BDTs/NNs/cuts, feature engineering, training, calibration, and validating classifier stability under systematic variations).

It primarily addresses event counts, templates, and common particle-physics measurements. Time-dependent oscillations, full amplitude analyses, heavy-ion centrality and flow, hardware calibration, and lattice QCD require additional specialized models. Follow the experiment's data-governance and unblinding rules when using internal data.

All maintained instructions, templates, metadata, comments, and validation notes are in English. The skill can still answer a user in their requested language.

## Example prompts

"Use this skill to inspect my sample manifest and cutflow while preserving the selection. Identify yield-changing issues and produce a minimal correction with comparison commands."

"Use this skill to build a nuisance-correlation table and likelihood from my SR/CR templates. Start with Asimov data, assess fit diagnostics and coverage requirements, then calculate the expected limit."

"Write an RDataFrame selection for >=2 muons with pT>25 GeV, make a pT histogram with a cutflow, and set up the CMake build for it."
