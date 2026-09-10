# Package Validation Record

Validation date: 2026-09-05. Helper test environment: Python 3, standard library
only. PyTorch is not installed in this environment and could not be installed
(network egress to PyPI is blocked), so the scripts' actual tensor/model behavior
under real PyTorch was not exercised here - see Limitations.

## Completeness pass (2026-09-05)

This pass brought the package in line with the completeness level already
established for `hep-analysis` in this collection: a structural bundle validator,
an automated test suite, dual-environment (Codex/Claude Code) install docs
(`README.md`, `agents/openai.yaml`), and this validation record.

- `scripts/validate_skill_bundle.py` was added and confirmed to report all 32
  expected files present and non-empty.
- `tests/test_deep_learning_skill.py` was added (4 tests, each parameterized with
  `subTest` across the 5 diagnostic scripts that take command-line arguments -
  `benchmark_model.py`, `check_dataset_contract.py`, `find_nan_batches.py`,
  `inspect_checkpoint.py`, `profile_dataloader.py` - for 4 x 5 = 20 effective
  checks, `python3 -m unittest discover -s tests -v`):
  - `--help` exits 0 and prints a `usage:` line for every script, confirmed with no
    PyTorch installed.
  - Each script's guarded `import torch` leaves consistent module-level state:
    `torch is None` and `_TORCH_IMPORT_ERROR` set to the `ModuleNotFoundError` when
    PyTorch is absent (verified directly here), or `torch` bound to the real module
    with `_TORCH_IMPORT_ERROR is None` when present (this branch is exercised
    automatically in any environment where PyTorch is installed, via
    `unittest.skipIf`).
  - With PyTorch absent, every script exits 1 with a `PyTorch is required ...`
    message and no `Traceback` in stderr, instead of a raw `ModuleNotFoundError`
    crash - this is the specific defect fixed in this pass, see below.
  - `check_pytorch_env.py`'s own pre-existing graceful-degradation behavior
    (`ERROR: Could not import torch`, exit 1, no traceback) was also regression-
    tested.
- `README.md`'s documented quick-check commands were run as documented: all five
  guarded scripts show `--help` output, and `check_pytorch_env.py` reports the
  missing PyTorch installation cleanly.
- `agents/openai.yaml` was parsed with PyYAML and confirmed to carry
  `display_name`/`short_description`/`default_prompt`.

One defect was found and fixed as part of reaching this completeness level (during
the preceding cross-environment audit):

- `benchmark_model.py`, `check_dataset_contract.py`, `find_nan_batches.py`,
  `inspect_checkpoint.py`, and `profile_dataloader.py` all did a bare
  module-level `import torch`. With PyTorch not installed, this meant *any*
  invocation - including `--help` - crashed with a raw `ModuleNotFoundError`
  traceback, before argparse ever ran. Only `check_pytorch_env.py` already
  guarded its import. Fixed all five to guard the import the same way
  `check_pytorch_env.py` does, deferring the hard failure until after argparse
  has parsed arguments (so `--help` and argument-validation errors still work
  with no PyTorch installed), then exiting with a one-line
  `PyTorch is required to run this script but could not be imported: ...`
  message.

## Coverage expansion pass (2026-09-05)

Added six new reference files and two new starting-point templates to broaden and
deepen the skill's PyTorch coverage: `references/transformer-architectures.md`,
`references/sequence-models.md`, `references/generative-models.md`,
`references/efficient-finetuning.md`, `references/custom-autograd-and-hooks.md`,
`references/export-and-deployment.md`, `assets/transformer_classifier.py`, and
`assets/lora_finetune.py`. Also extended `references/reproducibility.md` with a
new "Hyperparameter sweeps" section. `SKILL.md`'s reference-routing table, its
frontmatter `description`, `README.md`'s coverage section, and
`scripts/validate_skill_bundle.py`'s `REQUIRED_PATHS` were all updated to match
(bundle now reports 40 files).

PyTorch remains uninstallable here (see Limitations), so the two new asset
templates were verified by a combination of methods rather than end-to-end
execution:

- Both compile cleanly (`python3 -m py_compile`) and parse as valid Python
  (`ast.parse`).
- `assets/transformer_classifier.py`'s core tensor operations - the QKV
  reshape/permute into per-head tensors, the scaled dot-product attention
  score/mask/softmax sequence, and the mean-pooling over non-pad positions - were
  independently re-implemented in NumPy against synthetic inputs (including a
  sequence with real padding) and checked for correct output shapes, for padded
  key positions receiving ~0 attention weight, and for real softmax rows summing
  to 1. This caught a class of bug (mask/broadcast shape errors) that
  `py_compile` cannot detect.
- `assets/lora_finetune.py`'s `LoRALinear` forward math
  (`base_out + scale * (x @ A^T) @ B^T`) was independently re-implemented in
  NumPy and checked against an equivalent single-matmul form using
  `merged_weight()`'s formula (`W + scale * B @ A`), confirming the two are
  numerically identical - this is the property the reference file's "merge for
  zero-overhead inference" guidance depends on. Also checked that with `B`
  initialized to zeros (as the real code does), the adapted output exactly
  equals the frozen base layer's output, confirming the documented "adapted
  model is numerically identical to the base model at step 0" property.
- `apply_lora`'s module-replacement logic was reviewed and found to mutate a
  model's `_modules` dict while a generator (`named_modules()`) was still
  iterating over it - a real bug that can silently skip replacements or raise
  depending on dict-mutation-during-iteration behavior. Fixed to collect all
  matches in a first pass and apply replacements only in a second, non-mutating
  pass.
- All new/edited Markdown cross-links (both within the new files and from
  existing files that now point to them) were checked against the files that
  actually exist on disk: none broken.

## Senior-architect expansion pass (2026-09-09)

Added eight reference files covering the decisions made around the code rather than
in it: `references/architecture-selection.md`,
`references/ablation-and-design-review.md`, `references/parallelism-strategy.md`,
`references/training-at-scale.md`, `references/serving-architecture.md`,
`references/monitoring-and-lifecycle.md`, `references/data-strategy.md`, and
`references/evaluation-strategy.md`. Added five new standard-library scripts -
`estimate_training_memory.py`, `estimate_compute_budget.py`, `compare_model_runs.py`,
`serving_capacity.py`, and `check_split_integrity.py` - plus
`assets/scaling_plan.example.json`, `assets/eval_runs.example.json`, and
`assets/dataset_splits.example.json`. `SKILL.md`'s reference routing, helper-script
list, example prompts and frontmatter `description`; `README.md`'s quick checks and
coverage section; `agents/openai.yaml`; and `scripts/validate_skill_bundle.py`'s
`REQUIRED_PATHS` were updated to match (bundle now reports 56 files, up from 40). The
sibling `skill-router` skill and the repository README were extended with the same
routing keywords.

**Scope decision: TensorFlow was deliberately excluded.** The request that prompted
this pass named "PyTorch/TensorFlow", and the framework question was put explicitly;
the answer was architect content, PyTorch only. `SKILL.md`'s "Not in scope: non-PyTorch
deep learning frameworks" boundary, `README.md`'s "explicitly PyTorch-only" statement,
and `skill-router`'s matching exclusion were therefore all left intact. A
TensorFlow/Keras layer remains a clean separate pass; nothing added here blocks it.

Unlike the previous passes, PyTorch **is** installed in this environment (2.11.0), so
the memory model was validated against real allocations rather than only against closed
forms:

- `estimate_training_memory.py`'s parameter formula was checked against a real
  `nn.Module` transformer built to the same geometry (4 layers, hidden 256, 8 heads,
  FFN ratio 4, vocab 1000): predicted and actual parameter counts agree **exactly**
  (3,401,728 both ways), not approximately. Its bytes-per-parameter table was checked
  by building that model, running a real forward/backward and an `Adam` step, and
  summing actual tensor bytes: measured 4.000 bytes/param for parameters, 4.000 for
  gradients, and 8.000 for optimizer state, against the table's 4/4/8, and the
  predicted total model-state bytes equalled the measured 54,427,648 to the byte.
  The sharding arithmetic was checked separately: ZeRO-1 shards only optimizer state,
  ZeRO-2 also gradients, ZeRO-3 all three, each by exactly the data-parallel degree,
  and tensor parallelism shards weights independently of the ZeRO stage. Activation
  formulas were checked against the closed forms of Korthikanti et al.
  (arXiv:2205.05198) for all three recomputation modes, including the strict ordering
  none > selective > full, exact linearity in microbatch, superlinearity in sequence
  length, and the fact that sequence parallelism divides activations by exactly the
  tensor-parallel degree while tensor parallelism alone leaves an unsharded remainder.
- `estimate_compute_budget.py`'s `6ND` rule reproduces the published GPT-3-scale
  training compute: 175e9 parameters over 300e9 tokens gives 3.15e23 FLOPs against the
  widely quoted ~3.14e23, agreeing to within 1%. The MFU calculation was verified by
  round-trip: feeding back the throughput implied by a chosen MFU recovers that MFU to
  12 decimal places. The tokens-per-parameter regime classifier correctly labels
  GPT-3's 1.7 tokens/param as undertrained, 20 as near compute-optimal, and 1000 as
  overtrained.
- `compare_model_runs.py`'s percentile bootstrap was checked against the analytic
  `mean +/- 1.96 * stderr` interval on a 20-point sample, agreeing within 30% of one
  standard error; reproducibility under a fixed seed and widening with confidence level
  were verified directly. The minimum-detectable-effect formula was checked against its
  closed form and its `1/sqrt(n)` scaling. Identical arms are correctly reported as not
  significant, a uniform paired improvement as significant, and a single lucky seed
  triggers the best-of-N warning. The shipped asset is the instructive case: the paired
  difference is real while being smaller than either arm's own seed spread, and both
  facts are reported.
- `serving_capacity.py`'s replica sizing, utilization, and M/M/1 p99 sojourn time were
  checked against closed forms, including the ceiling behavior (utilization never
  exceeds the configured cap for any load from 10 to 9000 QPS) and the tail divergence
  as utilization approaches 1, which is the quantitative claim the reference makes
  about provisioning headroom. The batch-fill check has an exact analytic floor:
  because utilization is capped, per-replica arrivals are bounded and the fill time
  cannot fall below `batch_size / (capacity * max_utilization)` regardless of total
  load - verified at 50.0 ms for the example configuration.
- `check_split_integrity.py` was checked on constructed inputs with known answers for
  duplicates, pairwise overlap, group leakage, and temporal violations. The key case is
  covered explicitly: a manifest whose split IDs do **not** overlap at all but whose
  groups do is correctly reported as leaking, which is the failure no metric shows.
  The shipped asset exercises it and exits nonzero.
- All five CLIs were exercised for invalid input (a plan file missing a required field,
  a `TP x PP` factorization that does not divide world size, an out-of-range MFU, a
  single-element score array, a nonexistent file) and confirmed to exit nonzero with a
  one-line message rather than a traceback.
- 102 new tests were added to `tests/test_deep_learning_skill.py` (4 pre-existing +
  102 new = 106 total, `python3 -m unittest discover -s tests -v`), of which 3 are the
  PyTorch cross-checks above and skip cleanly when PyTorch is absent.

Two defects were found and fixed during this pass rather than shipped: the
memory estimator initially advised dropping to plain DDP whenever utilization was low,
including for configurations whose unsharded states would not fit at all (it now
computes the stage-0 total and only suggests a lower stage when that would actually
fit), and the serving planner's batch-fill condition compared the full fill time
against twice the timeout, conflating it with the average wait (now compared directly,
with the fill time itself reported).

Structural checks: every relative Markdown link in the package resolves; all eight new
references end in a `## Deliverables` section and cross-link down into the
implementation references they sit on top of (1-7 links each); and their lengths
(4.2-6.8 KB) sit inside the range of the bundle's existing content references, so the
terse, code-forward house style is preserved.

## Consistency audit (2026-09-10)

A "check and reorganize" pass with no new content: read every reference file in
full, checked every relative Markdown link's display text against its actual
target, verified the eight architect-level references each still end in a
`## Deliverables` section, re-ran every README-documented command, and
`py_compile`'d every script/asset/test file.

- Found and fixed **17 link-text/target mismatches across 6 files**
  (`custom-autograd-and-hooks.md` x3, `efficient-finetuning.md` x3,
  `generative-models.md` x2, `export-and-deployment.md` x6,
  `transformer-architectures.md` x1, `sequence-models.md` x2): each showed a
  `references/`-prefixed path as the link's visible text while the href
  (correctly, since these files live inside `references/` themselves) pointed
  at the bare sibling filename. The links all resolved, so this was never a
  broken-link bug, but the display text was misleading to a reader scanning
  cross-references. All 17 now show the bare filename as both text and
  target, matching the convention most of the package's files (e.g.
  `parallelism-strategy.md`, `training-at-scale.md`) already followed.
- Re-ran every command in `README.md`'s Quick Checks section, including the
  five standard-library estimator scripts against their shipped example
  assets: all match documented behavior and exit codes
  (`check_split_integrity.py` still exits 1 on its deliberately-leaky example).
- Confirmed `references/cpp-balanced-design-guidelines.md` is still
  byte-identical to `agile-development`'s copy (untouched by this pass).
- No other inconsistencies found: `SKILL.md`'s reference-routing list, helper-
  script list, and asset list all match the files that actually exist on
  disk (no orphans, no dangling references either direction).
- Bundle validator and the full test suite (106 tests, 2 skipped) re-run
  clean after the fixes.

## Research-grade scientific reasoning expansion pass (2026-09-10)

Strengthened the skill from PyTorch engineering into research-grade deep-learning
reasoning for scientific ML/HEP, per a capability audit against the actual repository
(SKILL.md, README.md, and all 26 non-shared reference files were read in full before
any file was created). Added six reference files -
`references/optimization-and-training-dynamics.md`,
`references/uncertainty-and-calibration.md`,
`references/robustness-and-distribution-shift.md`,
`references/scientific-machine-learning.md`,
`references/geometric-and-equivariant-learning.md`, and
`references/interpretability-and-explainability.md` (the last folding in
representation learning rather than adding a seventh file). Declined two of the
spec's optional files: representation learning folded into
`interpretability-and-explainability.md`, and experiment provenance folded into an
expansion of the existing `references/reproducibility.md` (new "Reproducibility
levels" and "Experiment provenance" sections) rather than a new file, per the reuse-
before-create ordering the spec itself specifies. Also lightly extended
`references/evaluation-strategy.md` (an "Evaluation hierarchy" section),
`references/data-strategy.md` (a simulation-artifact leakage note),
`references/architecture-selection.md` (a symmetry cross-link), and
`references/ablation-and-design-review.md` (an ablation-vs-causal-explanation
distinction). `SKILL.md`'s frontmatter `description`, its "Architect-level
references" routing list, its example prompts, and its Caveats section (a new
`academic-papers` boundary line); `README.md`'s coverage section; `agents/openai.yaml`;
and `scripts/validate_skill_bundle.py`'s `REQUIRED_PATHS` were all updated to match
(bundle now reports 62 files, up from 56).

This is a markdown-only pass; no scripts, assets, or tests changed in content, so no
PyTorch execution was needed or performed.

- `scripts/validate_skill_bundle.py` was run and confirmed all 62 expected files
  present and non-empty.
- `python3 -m unittest discover -s tests -v` was re-run and still passes (106 tests,
  2 skipped for absent PyTorch) - unaffected by this pass, confirmed rather than
  assumed.
- Every relative Markdown link added or edited in this pass was checked against the
  files that actually exist on disk: none broken (including the two deliberately
  forward-declared links in Task 1/Task 4 that resolve once later tasks in the same
  pass complete).
- All six new references end in a `## Deliverables` section, matching the convention
  the "Senior-architect expansion pass" established.
- Checked for accidental duplication of `academic-papers` (statistical inference,
  likelihoods, coverage, discovery/exclusion) and `agile-development` (service
  architecture, deployment design) responsibilities: none found: the new content
  stays at "is the model trained/calibrated/robust," not "is the resulting scientific
  claim statistically valid" or "how should this service be architected."
- Mentally ran the ten capability-test scenarios from the driving task spec (training
  failure, generalization failure, calibration, scientific performance, simulation
  shift, interpretation, representation, equivariance, lucky seed, emulator) against
  the final file set; each is addressed by the diagnostic flow, principle, or
  checklist in the relevant new/expanded reference.

## Limitations

- **Superseded as of the 2026-09-09 pass:** the two earlier passes recorded that
  PyTorch could not be installed here. PyTorch 2.11.0 *is* available in the current
  environment, and was used to validate `estimate_training_memory.py` against real
  allocations. The original limitation still stands for the files it named: the
  tensor/model code paths in the six PyTorch-dependent `scripts/*.py` and the eight
  `assets/*.py` templates were checked for syntax, argument parsing, and graceful
  degradation at the time of those passes, and have not since been executed
  end to end against real data or a GPU/MPS device.
- No GPU is available here, so all memory and throughput figures are analytic
  estimates validated against CPU-side tensor accounting; they were not compared
  against `torch.cuda` allocator reports, and they exclude fragmentation,
  communication buffers, and CUDA context overhead.
- The five new standard-library scripts are design-level estimators. The serving
  planner assumes Poisson arrivals and exponential service, which overstates the
  latency tail for regular workloads and understates it for bursty ones; no load test
  was run. `check_split_integrity.py` detects exact-ID and group leakage only, not
  near-duplicates.
- No real dataset, training run, or checkpoint file was available, so
  `assets/train_classifier.py`, `assets/vision_transfer.py`,
  `assets/ddp_train_skeleton.py`, and the synthetic-data `create_dataset()`
  helpers in the diagnostic scripts were reviewed for correctness but not run
  end to end.
- `references/cpp-balanced-design-guidelines.md` is shared verbatim with
  `agile-development`'s copy of the same file; consistency between the two copies
  was checked (byte-identical) but the guidance itself was not re-validated here.

In an environment with PyTorch installed, additionally run
`python3 scripts/check_pytorch_env.py` to confirm the real environment, then run
each diagnostic script against real data/models and the templates in `assets/`
through an actual training step.
