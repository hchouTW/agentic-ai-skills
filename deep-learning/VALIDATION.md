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

## Limitations

- PyTorch is not installed in this validation environment and could not be
  installed (PyPI is blocked by network egress policy here), so the actual
  tensor/model code paths in all six `scripts/*.py` files and all eight
  `assets/*.py` templates were checked for syntax (`python3 -m py_compile`) and,
  for the six diagnostic scripts, for correct argument parsing and graceful
  degradation - not executed against real tensors, a real model, or a GPU/MPS
  device.
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
