---
name: skill-router
description: Use at the start of any non-trivial task to silently check whether one of the user's domain skills (academic-papers, agile-development, deep-learning, hep-analysis) applies before proceeding. Always consult this routing logic for any non-trivial software change (implement/fix/add/refactor/migrate/update, scoping, acceptance criteria, code review process), PyTorch model/training/DataLoader/debugging tasks, including architecture selection, parallelism strategy, compute/serving budgeting, ablation discipline, and data/evaluation strategy, HEP/CERN/ROOT/PyROOT/RDataFrame/uproot/Awkward/cutflow/systematics/fit/limit tasks, including detector subsystems (tracker, calorimeter, TRD, TOF, RICH, muon), event reconstruction, and Geant4/detector-simulation tasks, or reading/critiquing/summarizing a scientific paper, building a literature review, drafting or formatting a manuscript (LaTeX/REVTeX/JHEP/NeurIPS/ICML/ACL), managing a BibTeX/.bib file, or responding to referee reports or a conference rebuttal - even if the user doesn't name a skill explicitly or use the word "skill."
---

# Skill Router

Before starting any non-trivial task, silently check whether it matches one of
the routing rules below. This is a quick triage step, not a replacement for the
domain skill itself - once you identify a match, invoke that skill and follow
its workflow.

## Routing rules

- **academic-papers** - reading, critiquing, or summarizing a scientific paper
  or a stack of papers; building a literature review or a paper's "related
  work"/Introduction section; drafting, restructuring, or polishing a paper or
  section; formatting a manuscript in LaTeX (REVTeX, JHEP, JCAP, AASTeX,
  NeurIPS/ICML/ICLR/ACL-family style files, JMLR/TMLR); building or cleaning a
  BibTeX/.bib file or an ADS/DBLP/ACL-Anthology reference; designing figures/
  tables for publication; tightening scientific prose; responding to referee
  reports; or writing a single-shot conference rebuttal. Not for the
  underlying statistical/ML/physics analysis itself - see `deep-learning` or
  `hep-analysis` for that; this is the reading/writing/formatting layer on
  top of it.
- **agile-development** - any non-trivial software change: new features, bug
  fixes, refactors, endpoints, UI work, migrations, dependency updates. Also
  scoping, task breakdown, acceptance criteria, validation plans, and code
  review process. Also implementation discipline: whether to ask or assume on
  an ambiguous request, keeping a change minimal and surgical rather than
  overcomplicated, avoiding scope creep and unrelated refactors, and defining
  verifiable success criteria. Triggers on "implement", "fix", "add",
  "refactor", "migrate", or "update" code, and on "is this overcomplicated" or
  "am I over-engineering this", even without the word "Agile".
- **deep-learning** - PyTorch engineering: nn.Module models, training and eval
  loops, datasets and DataLoaders, losses, optimizers, schedulers, mixed
  precision, gradient accumulation, checkpointing, distributed training (DDP),
  reproducibility, inference, and performance/memory tuning. Also debugging
  tensor shape/device/dtype errors, NaNs, exploding gradients, and slow
  dataloaders. Covers senior-architect decisions around that code too:
  choosing and sizing an architecture, scaling laws, parallelism strategy
  (DDP vs. ZeRO/FSDP vs. tensor/pipeline/sequence), compute and cost
  budgeting, MFU, ablation discipline and seed variance, dataset design and
  split leakage, evaluation strategy and ship criteria, inference serving
  capacity, and drift monitoring and rollout. Not for TensorFlow, JAX, or
  other frameworks - that skill is explicitly PyTorch-only.
- **hep-analysis** - collider and particle-physics data and simulation: ROOT
  C++, PyROOT, RDataFrame, uproot/awkward columnar pipelines, ntuples, event
  selections, cutflows, histograms, efficiencies and scale factors, yields,
  backgrounds, unfolding, systematic uncertainties, RooFit/RooStats, pyhf,
  Combine, CMake/root-config builds, and HEP plotting. Also the detector and
  simulation layers beneath the analysis: detector subsystems and their physics
  (tracker/spectrometer, ECAL/HCAL calorimetry, TRD, TOF, RICH/Cherenkov,
  dE/dx, muon systems), particle identification, event reconstruction and
  truth matching, event generators, Geant4 detector simulation and
  digitization, and calibration/alignment. Also astroparticle and cosmic-ray
  physics: the cosmic-ray spectrum and composition (knee/ankle/GZK), extensive
  air showers and X_max, ground-based arrays (surface detector, fluorescence,
  hybrid), imaging atmospheric Cherenkov gamma-ray astronomy, high-energy
  neutrino telescopes, space-based/balloon direct detection (geomagnetic
  cutoff, solar modulation), multi-messenger analysis, Li & Ma
  significance/trials-factor statistics, the AMS-02 (ISS spectrometer) case
  study, and cosmic-ray flux calculation from counts/exposure. Not for
  unrelated uses of "root" (Linux root users, Android rooting, certificates,
  math or plant roots).

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
