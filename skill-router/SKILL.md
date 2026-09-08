---
name: skill-router
description: Use at the start of any non-trivial task to silently check whether one of the user's domain skills (agile-development, deep-learning, hep-analysis) applies before proceeding. Always consult this routing logic for any non-trivial software change (implement/fix/add/refactor/migrate/update, scoping, acceptance criteria, code review process), PyTorch model/training/DataLoader/debugging tasks, or HEP/CERN/ROOT/PyROOT/RDataFrame/uproot/Awkward/cutflow/systematics/fit/limit tasks, including detector subsystems (tracker, calorimeter, TRD, TOF, RICH, muon), event reconstruction, and Geant4/detector-simulation tasks - even if the user doesn't name a skill explicitly or use the word "skill."
---

# Skill Router

Before starting any non-trivial task, silently check whether it matches one of
the routing rules below. This is a quick triage step, not a replacement for the
domain skill itself - once you identify a match, invoke that skill and follow
its workflow.

## Routing rules

- **agile-development** - any non-trivial software change: new features, bug
  fixes, refactors, endpoints, UI work, migrations, dependency updates. Also
  scoping, task breakdown, acceptance criteria, validation plans, and code
  review process. Triggers on "implement", "fix", "add", "refactor",
  "migrate", or "update" code, even without the word "Agile".
- **deep-learning** - PyTorch engineering: nn.Module models, training and eval
  loops, datasets and DataLoaders, losses, optimizers, schedulers, mixed
  precision, gradient accumulation, checkpointing, distributed training (DDP),
  reproducibility, inference, and performance/memory tuning. Also debugging
  tensor shape/device/dtype errors, NaNs, exploding gradients, and slow
  dataloaders. Not for TensorFlow, JAX, or other frameworks - that skill is
  explicitly PyTorch-only.
- **hep-analysis** - collider and particle-physics data and simulation: ROOT
  C++, PyROOT, RDataFrame, uproot/awkward columnar pipelines, ntuples, event
  selections, cutflows, histograms, efficiencies and scale factors, yields,
  backgrounds, unfolding, systematic uncertainties, RooFit/RooStats, pyhf,
  Combine, CMake/root-config builds, and HEP plotting. Also the detector and
  simulation layers beneath the analysis: detector subsystems and their physics
  (tracker/spectrometer, ECAL/HCAL calorimetry, TRD, TOF, RICH/Cherenkov,
  dE/dx, muon systems), particle identification, event reconstruction and
  truth matching, event generators, Geant4 detector simulation and
  digitization, and calibration/alignment. Not for unrelated uses
  of "root" (Linux root users, Android rooting, certificates, math or plant
  roots).

## Behavior

1. Check the task against the rules above before doing any other work.
2. If exactly one skill is relevant, state "Using `<skill-name>` skill." and
   invoke it, then follow its workflow.
3. If multiple skills are relevant, state the primary skill and any secondary
   skill(s), e.g. "Using `deep-learning` skill (primary), with `agile-development`
   for task breakdown." Invoke the primary skill first.
4. If none of the rules apply, proceed normally without mentioning this skill.

## Helper Scripts

- `scripts/validate_skill_bundle.py` - check that this package's own files
  (SKILL.md, README.md, agents metadata, scripts, tests) are all present and
  non-empty, that SKILL.md/README.md have their expected structure, and that
  the routing table's skill names line up with whatever sibling skill folders
  are actually installed (standard library only).
- `tests/test_skill_router.py` - standard-library tests for the routing-table
  parsing and the bundle validator above. Run
  `python3 -m unittest discover -s tests -v`.
