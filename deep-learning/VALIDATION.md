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
(SKILL.md, README.md, and all 25 non-shared reference files were read in full before
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
  architecture, deployment design) responsibilities: none found. The new content
  stays at "is the model trained/calibrated/robust," not "is the resulting scientific
  claim statistically valid" or "how should this service be architected."
- Mentally ran the ten capability-test scenarios from the driving task spec (training
  failure, generalization failure, calibration, scientific performance, simulation
  shift, interpretation, representation, equivariance, lucky seed, emulator) against
  the final file set; each is addressed by the diagnostic flow, principle, or
  checklist in the relevant new/expanded reference.

## Example-authoring rollout pass (2026-09-10)

Added this skill's first `examples/` entry, per Phase 3 of `agile-development`'s
example-authoring initiative (see that skill's `references/example-authoring.md`
for the generation prompt and format spec this follows). One pilot example, not
a bulk batch.

- Added a one-line pointer to `agile-development`'s
  `references/example-authoring.md` under "When to Read a Reference" in
  `SKILL.md`, explicitly noting the cross-skill dependency (requires
  `agile-development` installed alongside this skill), plus one new "Example
  Prompts This Skill Handles Well" entry.
- Scaffolded `examples/01-imbalanced-dataloader-training-loop.md` with
  `agile-development`'s `generate_skill_example.py --skill deep-learning --role
  "Senior ML Systems Engineer" --use-case "a DataLoader and training loop for an
  imbalanced binary-classification dataset"`, then filled it in by hand: a
  fraud-style 95/5 binary classifier where the weak training loop seeds the
  DataLoader shuffle from the *global* RNG stream (so an unrelated random draw
  elsewhere in the pipeline silently changes the trained weights) and leaves the
  loss unweighted (so accuracy alone hides a large minority-recall gap); the
  expert version gives the DataLoader its own `torch.Generator`, class-weights
  the loss, reports per-class recall alongside accuracy, and checkpoints the
  seed/RNG state alongside the model/optimizer state.
- All claims in the example were independently executed against PyTorch 2.11.0
  (available in this environment), not just hand-derived - not merely a syntax
  check:
  - Extracted both code blocks verbatim from the finished markdown file with a
    regex, compiled them (`py_compile`), and imported them as real modules.
  - Confirmed the reproducibility claim directly: one unrelated `torch.randn(1)`
    call inserted between model construction and the first training step
    changed the weak version's final trained weights (`state_dict` no longer
    equal), while the expert version's dedicated generator produced
    byte-for-byte identical weights with and without the same call - checked
    with `torch.equal` on every parameter tensor, not just final accuracy.
  - Ran both versions three times each on the same synthetic 95/5 dataset and
    confirmed the reported accuracy/recall numbers are stable to four decimal
    places: weak (unweighted) 99.75% accuracy / 95.65% minority recall; expert
    (weighted) 98.25% accuracy / 100% minority recall. The file's prose was
    corrected to match these exact numbers after two earlier draft harnesses
    produced different figures - both were miscalibrated test setups (an
    unshuffled dataset that put the entire minority class outside the sampled
    training slice, and a full-dataset batch size that made shuffle order
    irrelevant) rather than errors in the shipped code; the final numbers above
    are from the actual code in the file, re-extracted and re-run after every
    edit.
  - `python3 scripts/validate_skill_example.py` (from `agile-development`)
    reports `ok` - no structural or placeholder findings.
- Added `examples/README.md` (one-row index table, linking back to
  `agile-development`'s reference) and added both new files to
  `scripts/validate_skill_bundle.py`'s `REQUIRED_PATHS`. Bundle now reports 64
  files, up from 62.
- Re-ran `python3 scripts/validate_skill_bundle.py` (64 files OK) and
  `python3 -m unittest discover -s tests -v` (106 tests, 2 skipped - unrelated
  pre-existing PyTorch-version-gated skips, unchanged by this pass) after the
  change.

This content is a worked domain example with runnable code, not prose
guidance, so it was held to a higher verification bar than this file's existing
"Limitations" note about process/workflow guidance being reviewed rather than
run - see the bullets above for what was actually executed.

## Example expansion to three (2026-09-10)

Expanded `examples/` from the one pilot entry above to three, per the user's
request to bring every installed skill's `examples/` up to three entries with
genuinely different content each.

- Scaffolded `examples/02-nan-loss-mixed-precision.md` (role "Senior ML
  Systems Engineer") and `examples/03-ddp-vs-fsdp-parallelism-choice.md`
  (role "Distributed Training / ML Infrastructure Architect") with
  `agile-development`'s `generate_skill_example.py`, then filled both in by
  hand, grounded in this skill's own reference material:
  - `02` is a hand-rolled attention softmax that runs entirely under fp16
    `autocast` instead of using `F.softmax` (which `autocast`'s op policy
    keeps in fp32 automatically); unnormalized dot-product scores on a
    2048-token sequence exceed fp16's ~65504 max before the softmax
    normalizes them, so `exp_scores.sum()` overflows to `inf` and the next
    divide produces `nan`. The weak approach reacts by lowering the learning
    rate and clipping harder with no localization; the expert approach uses
    `torch.autograd.set_detect_anomaly(True)` plus `torch.isfinite` guards to
    localize the failure to that module, then forces the score/softmax
    computation to run in fp32 explicitly. Both code blocks were extracted
    from the finished markdown and compiled (`py_compile`) to confirm they
    parse as valid Python with no undefined names.
  - `03` is built on this skill's own `scripts/estimate_training_memory.py`
    and `references/parallelism-strategy.md`'s 2+2+12-bytes/param mixed
    precision + Adam breakdown. Rather than hand-deriving the memory numbers,
    both estimator invocations quoted in the file were re-run independently
    with the exact same flags (`--params 7e9 --layers 32 --hidden 4096
    --heads 32 --seq-len 4096 --micro-batch 2 --gpus 8 --gpu-memory-gb 80
    --precision mixed --optimizer adam --recompute selective`, at
    `--zero-stage 0` and `--zero-stage 3`) and the output matched the
    markdown's quoted figures exactly: 138.31 GB total / optimizer-binding at
    stage 0, 47.04 GB total / activations-binding at stage 3. The
    2+2+12-bytes/param row was independently confirmed present in
    `references/parallelism-strategy.md` (line 39) rather than assumed.
  - `python3 ../agile-development/scripts/validate_skill_example.py` reports
    `ok` for both files - no structural or placeholder findings.
- Added both new rows to `examples/README.md`'s index table and both new
  files to `scripts/validate_skill_bundle.py`'s `REQUIRED_PATHS`. Bundle now
  reports 66 files, up from 64.
- Re-ran `python3 scripts/validate_skill_bundle.py` (66 files OK) and
  `python3 -m unittest discover -s tests -v` (106 tests, 2 skipped -
  unrelated pre-existing PyTorch-version-gated skips, unchanged by this pass)
  after the changes.

Held to the same higher verification bar as the pilot entry above: the NaN
example's code was compiled and its numeric-overflow claim checked against
fp16's actual max magnitude, and the parallelism example's two memory-budget
tables were independently re-executed against the shipped estimator rather
than accepted as hand-derived.

## Cross-repository consistency follow-up (2026-09-10)

A second "check and reorganize" pass across the whole collection (this skill plus
its four siblings) caught one thing the same-day Consistency audit above missed:
`SKILL.md`'s Caveats section referenced `[[agile-development]]` and
`[[academic-papers]]` using `[[wiki-link]]` double-bracket syntax - the linking
convention this repository's own memory files use, not skill markdown, and not
the convention used anywhere else in this file or its siblings (a plain
backtick-quoted skill name, e.g. `` `agile-development` ``). It rendered as
literal double brackets rather than a link and was inconsistent with every other
cross-skill mention in the package. Fixed both to plain backticks. A
repository-wide `grep -rn '\[\['` confirmed this was the only such occurrence in
this skill (two more were found and fixed the same way in the sibling
`agile-development` and `hep-analysis` packages). Bundle validator and full test
suite re-run clean after the fix.

## Example-authoring: Execution Trajectory pilot (2026-09-11)

Added this skill's first non-Contrast example, per Phase 3 of
`agile-development`'s four-archetype example-authoring revision (see that
skill's `references/example-authoring.md` for the full archetype spec; this
skill has no local copy of the tooling and depends on `agile-development`
being installed alongside it).

- Scaffolded and filled `examples/04-trajectory-exploding-gradient-nan-after-
  epoch3.md` (Execution Trajectory archetype, role "Senior ML Systems
  Engineer"): a training run whose loss turns to `nan` at the start of epoch
  4 with no code changes. Deliberately chosen to be a *different* root cause
  from the existing `02-nan-loss-mixed-precision.md` Contrast example (an
  fp16 attention-softmax overflow at a specific step) rather than a rehash:
  here an LSTM layer's gradient norm grows unbounded across three full
  epochs before overflowing, localized via a `register_full_backward_hook`
  per `references/optimization-and-training-dynamics.md`'s "Vanishing and
  exploding gradients" guidance, triaged with the `isfinite` checks from
  `references/debugging-pytorch.md`'s NaN section, and fixed with gradient
  clipping plus a short LR warmup (not a lower learning rate).
- `python3 ../agile-development/scripts/validate_skill_example.py
  examples/04-trajectory-exploding-gradient-nan-after-epoch3.md` passes with
  no structural or placeholder findings. The `clip_grad_norm_` return-value
  formatting in the example's code block was corrected to call `.item()`
  before use in an f-string, since a 0-dim tensor's `__format__` behavior
  under a numeric format spec is not something to rely on across PyTorch
  versions - caught by review, not by the validator.
- Added one row to `examples/README.md`'s index (now four columns:
  `Example | Archetype | Scenario | One-line takeaway`) and added the new
  file to `scripts/validate_skill_bundle.py`'s `REQUIRED_PATHS`. Re-ran
  `python3 scripts/validate_skill_bundle.py` ("Bundle OK: 67 files present
  and non-empty.", up from 66) and `python3 -m unittest discover -s tests -v`
  ("Ran 106 tests" / "OK (skipped=2)", unchanged - this pass added example
  content, not new test code).
- Also generalized the "Authoring a canonical worked example" pointer in
  `SKILL.md`'s reference-routing table from "(Weak vs. Expert contrast)" to
  name all four archetypes, matching `agile-development`'s own updated
  wording.

**Backlog (explicitly deferred, not silently missing):** this skill has three
remaining archetypes not yet piloted, per the source initiative's own
Phase 3 backlog table - Contrast (a naive vs. reproducible training loop -
distinct from the two Contrast examples already shipped), Gated Pipeline (a
new-architecture design proposal via `references/architecture-selection.md`
and `references/ablation-and-design-review.md`), and Decision-Tree (a
serving-latency regression triage). None of these were started in this pass.

## Example-authoring: expansion to three examples per new archetype (2026-09-11)

Per a follow-up request to bring every non-Contrast archetype in every skill's
`examples/` to three genuinely different examples (not variations on one
theme), added 8 new files to this skill's `examples/`: 2 more Execution
Trajectory, 3 Gated Pipeline, and 3 Decision-Tree. This also fulfills the
Gated Pipeline and Decision-Tree items from the "Backlog" note above; the
Contrast backlog item (a naive vs. reproducible training loop) remains
deliberately out of scope for this pass, which only targeted the three
non-Contrast archetypes.

Each new example was grounded in a distinct reference file rather than
reusing the territory already covered by an existing example in this skill:

- `05-trajectory-group-leakage-val-metric-collapse.md`: a 0.98
  offline/0.71 production AUC gap traced to row-level random splitting over
  a dataset with repeated per-customer rows, via `references/data-strategy.md`'s
  "Splits that survive contact with reality" (group leakage).
- `06-trajectory-checkpoint-missing-optimizer-state.md`: a post-resume loss
  spike traced to a checkpoint function using
  `references/checkpointing.md`'s "Inference-only weights" pattern instead of
  its "Save training checkpoint" pattern, silently discarding optimizer/
  scheduler state on every resume.
- `07-gated-pipeline-architecture-proposal-lstm-to-transformer.md`: an
  LSTM-to-Transformer architecture proposal gated against
  `references/architecture-selection.md`'s "Reviewing an architecture
  proposal" checklist, whose red-team phase applies
  `references/ablation-and-design-review.md`'s "Seed variance is the floor"
  guidance to downgrade an unsupported best-of-3-vs-single-run comparison.
- `08-gated-pipeline-ddp-to-fsdp-migration.md`: a DDP-to-FSDP migration
  gated against `references/parallelism-strategy.md`'s "Diagnosing the
  binding constraint", whose red-team phase finds a real multi-node
  evaluation-metric aggregation bug per `references/distributed-training.md`'s
  "Metric aggregation" section (missing `dist.all_reduce`).
- `09-gated-pipeline-model-release.md`: a production model release gated
  against `references/monitoring-and-lifecycle.md`'s "Releasing a new model",
  whose red-team phase applies `references/evaluation-strategy.md`'s "The
  offline-online gap" to find both a selection-bias artifact and a real
  training/serving feature-computation skew.
- `10-decision-tree-training-failure-classification.md`: formalizes
  `references/optimization-and-training-dynamics.md`'s "Training failure
  classification" table and "Diagnostic flow" directly into a 5-row triage
  matrix.
- `11-decision-tree-serving-latency-regression.md`: formalizes
  `references/serving-architecture.md`'s "Latency has parts" decomposition
  into a 5-row triage matrix, selecting the non-model-legs branch for a
  same-compute-time regression traced to a dropped fast-tokenizer backend.
- `12-decision-tree-eval-metric-anomaly.md`: combines
  `references/evaluation-strategy.md`'s "Protect the test set"/"The
  offline-online gap" with `references/data-strategy.md`'s "Versioning" into
  a 4-row matrix, distinguishing a genuine contamination fix from a newly
  introduced leak rather than assuming either by default.

Verification performed:
- Every code/diff/log block was checked for internal consistency before
  writing (e.g. the group-leakage example's split logic, the checkpoint
  diff's save/load symmetry, the DDP/FSDP example's binding-term arithmetic
  implied by the stated percentages).
- `python3 ../agile-development/scripts/validate_skill_example.py
  examples/<file>.md` was run on all 8 new files individually and printed
  `: ok` for each, with no structural or placeholder findings.
- Added one row per new file to `examples/README.md`'s index (still 4
  columns) and all 8 new paths to `scripts/validate_skill_bundle.py`'s
  `REQUIRED_PATHS`.
- Re-ran `python3 scripts/validate_skill_bundle.py` ("Bundle OK: 75 files
  present and non-empty.", up from 67) and
  `python3 -m unittest discover -s tests -v` ("Ran 106 tests" / "OK
  (skipped=2)", unchanged - this pass added example content, not new test
  code) and confirmed both pass clean.

No defects were found in the new content itself. This skill's `examples/`
directory now has 3 Contrast, 3 Execution Trajectory, 3 Gated Pipeline, and 3
Decision-Tree examples (12 total), closing out all four archetypes at parity.

## Consistency audit (2026-09-11)

A "check and reorganize" pass with no new reference/asset/example content:
diffed `scripts/validate_skill_bundle.py`'s `REQUIRED_PATHS` against every
real file on disk, checked every relative Markdown link across the package
for a broken target, swept for `[[wiki-link]]` syntax, confirmed every
`references/*.md` and `scripts/*.py`/`assets/*` file is mentioned at least
once in `SKILL.md`, re-ran every README-documented quick-check command live
(including the PyTorch-dependent ones - `check_pytorch_env.py` reports
PyTorch 2.11.0 present in this environment, unlike the 2026-09-05 pass's
environment, so this pass could exercise them directly rather than relying on
`--help`/absence-message checks alone), validated all 12 shipped
`examples/*.md` files, and cross-checked `examples/README.md`'s Archetype
column against each file's actual `archetype:` frontmatter.

- Found and fixed one real gap, the same class as the one found the same day
  in the sibling `agile-development` audit: `README.md`'s "Coverage and
  boundaries" paragraph, and `SKILL.md`'s frontmatter `description`, both
  enumerate this package's reference topics one by one but omitted two
  reference files that exist, are non-empty, are in `REQUIRED_PATHS`, and are
  linked from `SKILL.md`'s "When to Load References" table -
  `references/transfer-learning.md` (replacing a classifier head,
  freezing/unfreezing, backbone-vs-head optimizer parameter groups, BatchNorm
  under freezing) and `references/evaluation-metrics.md` (batch/rank-aware
  metric aggregation, classification metrics including macro F1/per-class
  recall/ROC-AUC/PR-AUC for imbalance, MAE/RMSE for regression, and
  validation-protocol pitfalls like leaking a scaler/tokenizer fit into
  validation data). Added one clause per file to `README.md`'s coverage
  paragraph and to `SKILL.md`'s frontmatter description, in the same
  itemized style as the surrounding text. Also tightened the adjacent
  C++/LibTorch boundary sentence in `README.md` from a pure double-negative
  ("does not cover general C++ unrelated to LibTorch/custom ops") to state
  the positive coverage first, matching how every other reference is
  described in that paragraph.
- No other inconsistencies found: `REQUIRED_PATHS` (75 entries) matches the
  actual file tree exactly in both directions; no broken links; no live
  `[[wiki-link]]` syntax (only the historical, already-fixed mention inside
  this file's own earlier entry describing that fix); every other
  `references/*.md`/script/asset is mentioned in `SKILL.md`; all 12 examples
  pass `agile-development`'s `validate_skill_example.py` with no structural
  or placeholder findings, 3 per archetype, index and frontmatter agree.
- Bundle validator and full test suite re-run clean after the fix:
  `python3 scripts/validate_skill_bundle.py` ("Bundle OK: 75 files present
  and non-empty.", unchanged - no new files, only two existing files edited)
  and `python3 -m unittest discover -s tests -v` ("Ran 106 tests" / "OK
  (skipped=2)", unchanged).

## Second-wave example-authoring pass: Adversarial Audit, Test-First, Postmortem (2026-09-12)

Added three new canonical examples in `agile-development`'s second-wave
archetypes, continuing the four-archetype example-authoring plan (Contrast/
Trajectory/Gated Pipeline/Decision-Tree already covered this skill; this
pass adds Adversarial Audit, Test-First, and Postmortem).

- `examples/13-adversarial-audit-sota-accuracy-claim.md`: attacks a "95.1%
  accuracy, new SOTA" writeup for a normalization-statistics train/test
  leak and an unreported single-seed result, both grounded in
  `references/reproducibility.md` ("Data splits", "Reproducing across
  seeds"); the honest, re-derived number (88.7% +/- 0.6% across 5 seeds)
  falls below the prior production baseline, not above it.
- `examples/14-test-first-dataloader-throughput-invariant.md`: a
  `num_workers`/`pin_memory`/`persistent_workers` DataLoader tuning grounded
  in `references/data-loading.md` and `references/performance-memory.md`,
  red on a single-worker loader (187.3 samples/sec) to green on the tuned
  configuration (612.4 samples/sec, 93% GPU util).
- `examples/15-postmortem-distributed-training-divergence.md`: a multi-day
  run's silent NaN divergence traced through 5 Whys (no "human error" stop)
  to a checkpoint schema that forgot the mixed-precision `GradScaler` state
  across a routine preemption, directly matching
  `references/training-at-scale.md`'s "checkpoints must be resumable, not
  just loadable" and "fail loudly on NaN" guidance; fixed with both a
  checkpoint-schema addition and a per-step NaN-abort.
- All three pass `agile-development/scripts/validate_skill_example.py` and
  the diversity checker (`check_example_diversity.py`) shows no
  archetype/skill repeats across the 12-file second-wave batch.
- `examples/README.md`'s intro line updated from "four archetypes" to
  "eight archetypes"; three rows added to its index (15 rows total).
- `scripts/validate_skill_bundle.py`'s `REQUIRED_PATHS` extended with the
  three new example files. Re-ran `python3 scripts/validate_skill_bundle.py`
  ("Bundle OK: 78 files present and non-empty") and
  `python3 -m unittest discover -s tests -v` (106 tests, 2 skipped -
  pre-existing PyTorch-unavailable skips, unrelated to this pass) after the
  change.

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
