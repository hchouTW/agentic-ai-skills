# TODO for future Claude sessions (deep-learning)

State at 2026-09-21: skill is on `main`; `python3 -m unittest discover -s tests` (106 tests, 2 skipped) and
`python3 scripts/validate_skill_bundle.py` (86 files) pass. `VALIDATION.md` is dated 2026-09-05 and says PyTorch was
not installable, so most `assets/` and `scripts/` were only checked with `py_compile`, `ast.parse`, NumPy
re-implementations, or `--help`. Nothing has been checked by running the skill on a fresh model. Read
`VALIDATION.md` first, then this file.

Working rules: work on a branch, run the unittest command and the bundle validator before committing, keep
`SKILL.md`, `README.md`, `scripts/validate_skill_bundle.py` `REQUIRED_PATHS` and `agents/openai.yaml` in sync, and
ask before pushing or merging. Record every result (including negative ones) in `VALIDATION.md`. Do not change
training behavior in an asset or reference without saying so. Use the scratchpad for temp files.

Environment facts found on 2026-09-21 (re-check, they may have changed):
- `python3` now has `torch 2.11.0`, so the "PyTorch not installed" limitation in `VALIDATION.md` is stale. Check
  `python3 scripts/check_pytorch_env.py` for CUDA/MPS availability (this is a Mac: expect MPS/CPU only, no CUDA, so
  DDP/NCCL/FSDP paths can only be tested on CPU with the `gloo` backend).
- The 2 skipped tests are the `torch`-present branches; find out which ones and whether they now run.
- Do not install into the user's conda base; use a scratchpad venv if extra packages (`onnx`, `peft`, `torchvision`) are needed.

## P1 - close known verification gaps (things never actually run)
- [ ] Run every `assets/*.py` template for real on tiny synthetic data (CPU): `train_classifier.py`,
      `ddp_train_skeleton.py` (2 processes, `gloo`, via `torchrun`), `transformer_classifier.py`, `lora_finetune.py`,
      `vision_transfer.py`, `inference.py`, `models.py`, `dataset_template.py`, `metrics.py`. Fix or document any
      that fail; add a fast smoke test per asset to `tests/` (skip when a dependency is missing).
- [ ] Run each `scripts/*.py` against real PyTorch objects, not just `--help`: `benchmark_model.py`,
      `check_dataset_contract.py`, `find_nan_batches.py` (inject a NaN on purpose), `inspect_checkpoint.py`
      (checkpoints with and without optimizer state), `profile_dataloader.py`, `check_split_integrity.py`
      (with a deliberate leak), plus the pure-Python calculators.
- [ ] Cross-check the calculators against independent references, not only self-consistency:
      `estimate_training_memory.py` (measure real peak memory of a small model on CPU/MPS vs the estimate),
      `estimate_compute_budget.py` (6ND FLOPs rule, Chinchilla numbers), `serving_capacity.py` (Little's law / queueing
      by hand), `compare_model_runs.py` (paired bootstrap / seed-variance vs `scipy`). Record assumed constants/units.
- [ ] Execute the code snippets in `references/*.md` that claim to be runnable (shape tables in `tensor-shapes.md`,
      AMP/GradScaler in `mixed-precision.md`, `checkpointing.md`, hooks in `custom-autograd-and-hooks.md`,
      export in `export-and-deployment.md`). Flag API drift against torch 2.11 (deprecated `torch.cuda.amp.*`,
      `torch.load` `weights_only` default, `torch.compile` options, `torch.export`, TorchScript deprecation).
- [ ] Audit numbers and claims in `references/` (scaling laws, MFU figures, memory multipliers, FSDP/ZeRO
      behavior, calibration thresholds) against primary sources; remove or soften anything unsourced and date
      anything time-sensitive.

## P2 - test that the skill actually changes model behavior
The 24 examples (`examples/01-24`) and the rules in `SKILL.md` are unproven until a fresh model is run on them.
- [ ] Write 12-15 realistic prompts (store in `tests/prompts.md`) with expected behaviors (which rule fires, which
      reference is read): NaN loss under AMP, val metric collapse from group leakage, DDP vs FSDP choice, missing
      optimizer state on resume, slow DataLoader, shape/device/dtype error, "make it faster" (ambiguous, should
      elicit), "add a SOTA accuracy claim" (should audit), ECE/calibration claim, LoRA config, ONNX export mismatch,
      a TensorFlow/JAX request (must not trigger), an HEP-ML request (equivariant/physics-informed, check routing to
      `hep-analysis` as secondary), and a sklearn-only question (must not trigger).
- [ ] Run each prompt in a fresh subagent with and without the skill (baseline vs skill); compare against
      expectations; log pass/fail in `VALIDATION.md`. Repeat with Haiku (weaker) and Opus if possible.
- [ ] Trigger test for the frontmatter `description`: 20 should-trigger and 20 should-not-trigger queries
      (near-misses: TensorFlow/JAX, generic statistics, `hep-analysis` ROOT ML, LLM API usage). Consider
      `skill-creator` description optimization; keep under the length limit.
- [ ] Routing hygiene with sibling skills (`hep-analysis`, `agile-development`, `academic-papers`,
      `task-authoring`); run each affected skill's validator and tests after any description change.
- [ ] Data point from the isolated routing eval (2026-09-26, `hep-analysis/tests/routing_eval.py` on `hep-analysis/tests/trigger_queries_holdout.json`, all 7 repo skills loaded as project skills, 2 runs per query; "none" = the model answered without invoking any skill): Sonnet 6/6 correct; Haiku 2/6. "Explain equivariant neural networks for point
      clouds and when they beat a plain transformer" 0/2 (none); "How do I set up mixed precision and gradient
      checkpointing for a 1B parameter model in PyTorch?" 1/2; "My GNN for jet tagging overfits after 3 epochs, what
      regularization should I try?" 0/2 (none once, `hep-analysis` once). Include these in the trigger test above.
- [ ] Verify the 24 examples follow their archetype rules (`task-authoring/references/example-authoring.md`) and
      that every code snippet runs or is clearly labelled pseudo-code.

## P3 - improve content and structure
- [ ] `SKILL.md` is 273 lines and `references/` totals ~3,000 lines: check progressive disclosure. Confirm a typical
      task needs at most 2-3 references, and add "read only if" hints where a routing row is vague.
- [ ] Look for overlap: `parallelism-strategy.md` vs `distributed-training.md` vs `training-at-scale.md`;
      `evaluation-strategy.md` vs `evaluation-metrics.md`; `data-strategy.md` vs `data-loading.md`. Merge or
      cross-link duplicated tables.
- [ ] Add missing coverage if a gap is confirmed by the prompt tests: FSDP2/`torch.distributed.tensor`, `torch.compile`
      graph-break debugging, Apple MPS pitfalls, gradient checkpointing (activation), data-parallel eval metric
      aggregation, KV-cache/inference-time attention.
- [ ] Add regression tests for scripts that have thin coverage (error paths: empty dataset, NaN input, wrong
      checkpoint keys, zero-length split). Current tests mostly check `--help` and the missing-torch exit path.
- [ ] Add a minimal end-to-end sample (synthetic data -> `check_dataset_contract` -> `check_split_integrity` ->
      `train_classifier` -> `inspect_checkpoint` -> `compare_model_runs`) under `examples/` or `assets/` as a smoke test.
- [ ] Multi-platform check (Codex, Antigravity): confirm `agents/openai.yaml` is current and no instructions depend
      on Claude-only tools. See the repo's multi-platform conventions.
- [ ] Skill-reviewer pass on `SKILL.md` and `README.md` (`plugin-dev:skill-reviewer`).

## P4 - housekeeping and decisions
- [ ] Update `VALIDATION.md` header date, the stale "PyTorch not installed" text, and file/test counts (86 files,
      106 tests) after each pass.
- [ ] `.pytest_cache/` and `__pycache__/` are gitignored; leave them alone.
- [ ] Ask the user: which workloads matter most (vision, LLM fine-tuning, HEP/physics ML, tabular)? This sets
      which prompts and assets to prioritise in P1/P2.
- [ ] Ask the user whether GPU/CUDA testing is available (another machine, cloud) for DDP/FSDP/AMP paths that
      cannot run on this Mac.
