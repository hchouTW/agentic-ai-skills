#!/usr/bin/env python3
"""Validate the hep-analysis skill bundle's structural integrity.

Purpose: catch accidental deletions or truncations of files this skill's SKILL.md
and README.md depend on - e.g. after merging in content from another skill.

What it does: checks that every file this package is expected to ship (SKILL.md,
README.md, references, scripts, assets, tests) exists and is non-empty, that
SKILL.md has YAML frontmatter with name/description, and that README.md has its
expected section headers.

Usage: run with no arguments from anywhere; it resolves paths relative to its own
location. `python3 scripts/validate_skill_bundle.py`. No third-party dependencies.
"""
from __future__ import annotations

from pathlib import Path

REQUIRED_PATHS = [
    "SKILL.md",
    "README.md",
    "VALIDATION.md",
    "agents/openai.yaml",
    "assets/analysis-contract.yaml",
    "assets/histograms.example.json",
    "assets/pyhf-counting.json",
    "assets/report-template.md",
    "assets/systematics.csv",
    "assets/uproot_awkward_analysis.py",
    "assets/pyroot_rdataframe_analysis.py",
    "assets/cpp_rdataframe_analysis.cpp",
    "assets/rdf_analysis.cpp",
    "assets/pyroot_roofit_signal_background.py",
    "assets/fit_histogram.cpp",
    "assets/plot_branch.C",
    "assets/CMakeLists.txt",
    "assets/analysis_config.yaml",
    "assets/systematics_config.yaml",
    "assets/statistical_histogram_config.yaml",
    "assets/combine_datacard_template.txt",
    "references/01-analysis-design.md",
    "references/02-data-pipelines.md",
    "references/03-weights-normalization.md",
    "references/04-histograms-efficiencies.md",
    "references/05-backgrounds.md",
    "references/06-systematics.md",
    "references/07-likelihood-fitting.md",
    "references/08-inference.md",
    "references/09-statistical-tools.md",
    "references/10-measurements-unfolding.md",
    "references/11-ml-analysis.md",
    "references/12-validation.md",
    "references/13-sources.md",
    "references/14-cpp-root-coding.md",
    "references/15-cmake-and-build.md",
    "references/16-debugging-root.md",
    "references/17-python-hep-coding.md",
    "references/18-code-conventions.md",
    "references/19-cpp-balanced-design-guidelines.md",
    "references/20-physics-objects-jets-btagging-met.md",
    "references/21-triggers-luminosity-pileup.md",
    "references/22-multivariate-classifiers-bdt-nn.md",
    "references/23-detector-systems-overview.md",
    "references/24-tracking-and-vertexing.md",
    "references/25-calorimetry-ecal-hcal.md",
    "references/26-particle-identification.md",
    "references/27-event-reconstruction.md",
    "references/28-reconstruction-performance-and-truth-matching.md",
    "references/29-event-generation.md",
    "references/30-detector-simulation.md",
    "references/31-calibration-and-alignment.md",
    "references/32-cosmic-ray-spectrum-and-composition.md",
    "references/33-extensive-air-showers.md",
    "references/34-ground-based-detection-arrays.md",
    "references/35-imaging-atmospheric-cherenkov.md",
    "references/36-neutrino-astronomy.md",
    "references/37-space-based-direct-detection.md",
    "references/38-multimessenger-analysis.md",
    "references/39-astroparticle-statistics.md",
    "assets/pileup_profiles.example.json",
    "assets/cosmic_ray_spectrum.example.json",
    "assets/detector_stack.example.json",
    "assets/calorimeter_response.example.json",
    "scripts/audit_histograms.py",
    "scripts/counting_reference.py",
    "scripts/tag_and_probe_efficiency.py",
    "scripts/pileup_reweight.py",
    "scripts/multiple_scattering.py",
    "scripts/calorimeter_resolution.py",
    "scripts/pid_separation_power.py",
    "scripts/cherenkov_angle.py",
    "scripts/inspect_root_file.py",
    "scripts/inspect_root_file.C",
    "scripts/check_root_cpp_env.sh",
    "scripts/new_root_cpp_project.sh",
    "scripts/check_systematic_variations.py",
    "scripts/compare_root_histograms.py",
    "scripts/make_yield_table.py",
    "scripts/summarize_histogram_statistics.py",
    "scripts/roofit_workspace_summary.py",
    "scripts/li_ma_significance.py",
    "scripts/geomagnetic_cutoff.py",
    "scripts/cr_spectrum_powerlaw_fit.py",
    "scripts/xmax_gaisser_hillas.py",
    "scripts/validate_skill_bundle.py",
    "tests/test_helpers.py",
    "tests/test_astroparticle.py",
]

REQUIRED_README_SECTIONS = [
    "## Installation and invocation",
    "## Quick checks",
    "## Coverage and boundaries",
    "## Example prompts",
]


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    missing = [path for path in REQUIRED_PATHS if not (root / path).exists()]
    empty = [
        path
        for path in REQUIRED_PATHS
        if (root / path).exists() and (root / path).stat().st_size == 0
    ]

    if missing or empty:
        if missing:
            print("missing files:")
            for path in missing:
                print(f"  {path}")
        if empty:
            print("empty files:")
            for path in empty:
                print(f"  {path}")
        raise SystemExit(1)

    skill = (root / "SKILL.md").read_text(encoding="utf-8")
    if not skill.startswith("---\n"):
        print("SKILL.md is missing YAML frontmatter")
        raise SystemExit(1)
    frontmatter = skill.split("---", 2)[1]
    for field in ("name:", "description:"):
        if field not in frontmatter:
            print(f"SKILL.md frontmatter is missing {field}")
            raise SystemExit(1)

    readme = (root / "README.md").read_text(encoding="utf-8")
    missing_sections = [s for s in REQUIRED_README_SECTIONS if s not in readme]
    if missing_sections:
        print("README.md is missing sections:")
        for section in missing_sections:
            print(f"  {section}")
        raise SystemExit(1)

    print(f"Bundle OK: {len(REQUIRED_PATHS)} files present and non-empty.")


if __name__ == "__main__":
    main()
