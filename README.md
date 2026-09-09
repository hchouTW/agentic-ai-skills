# Agentic AI Skills

A collection of portable [Agent Skills](https://code.claude.com/docs/en/skills) for
Claude Code, Codex, and other skill-aware agents. Each skill is a self-contained
folder built around a `SKILL.md`, with references, helper scripts, and templates
resolved through relative paths. None require an MCP server, cloud account, or paid
service.

## Skills

| Skill | What it covers |
|---|---|
| [`skill-router`](skill-router/) | Triage step run at the start of any non-trivial task; routes to the right domain skill below. |
| [`agile-development`](agile-development/) | Turning a software request into a small, verified, reviewable increment: scoping, acceptance criteria, validation plans, code review, incident response — plus implementation discipline: ask vs. assume, minimum code, surgical diffs, verifiable done. |
| [`deep-learning`](deep-learning/) | PyTorch engineering: models, training/eval loops, DataLoaders, mixed precision, DDP, LoRA, profiling, export, and debugging NaNs/shapes/perf — plus architect-level work: architecture selection and scaling laws, parallelism strategy and compute budgeting, ablation discipline, serving capacity, and data/evaluation strategy. |
| [`hep-analysis`](hep-analysis/) | High-energy physics: ROOT C++, PyROOT, uproot/awkward, RDataFrame, cutflows, systematics, fits, limits, unfolding — plus detector subsystems (tracking, calorimetry, TRD/TOF/RICH particle ID), event reconstruction, the generator→Geant4→calibration simulation chain, and astroparticle/cosmic-ray physics (spectrum and composition, extensive air showers, ground-based arrays, imaging atmospheric Cherenkov, neutrino telescopes, space-based direct detection, multi-messenger analysis, an AMS-02 case study, and cosmic-ray flux calculation). |
| [`academic-papers`](academic-papers/) | Reading and critically evaluating scientific papers, building literature reviews, and drafting/formatting/submitting a manuscript — REVTeX/JHEP/JCAP/AASTeX/Elsevier/NeurIPS/ICML/ICLR/ACL LaTeX, INSPIRE-HEP/ADS/arXiv/DBLP bibliographies, HEP/astroparticle/cosmic-ray and statistics/ML conventions (exposure vs. luminosity, pre-/post-trial significance, skymaps, reproducibility checklists, single-shot rebuttals). |

## Installation

Copy the skill folders you want into your agent's skill directory:

```bash
# Claude Code (personal)
cp -r academic-papers agile-development deep-learning hep-analysis skill-router ~/.claude/skills/

# Claude Code (project-scoped)
cp -r academic-papers agile-development deep-learning hep-analysis skill-router .claude/skills/

# Codex
cp -r academic-papers agile-development deep-learning hep-analysis skill-router ~/.codex/skills/
```

Each skill's own `README.md` has per-agent invocation details. `skill-router` only
routes to skills that are actually installed, so partial installs are fine.

## Verifying a skill bundle

Every skill ships an integrity checker and unit tests (Python standard library only):

```bash
cd <skill-folder>
python3 scripts/validate_skill_bundle.py
python3 -m unittest discover -s tests -v
```

See each skill's `VALIDATION.md` for what is checked.
