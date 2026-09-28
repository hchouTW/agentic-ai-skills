# TODO for future Claude sessions (deep-learning)

State (verified 2026-09-28 on `main`): `python3 scripts/validate_skill_bundle.py` OK (61 files; it was 86 before `examples/` was removed on 2026-09-25, commits 0c5530f and 99cc42f); `python3 -m unittest discover -s tests` 106 tests OK, 2 skipped. **No TODO item has been worked on yet.** This is the only repo skill with no behavioral or trigger testing.

Verification so far is mostly `py_compile`, `ast.parse`, NumPy re-implementations and `--help` checks. One exception is `estimate_training_memory.py`, validated against real CPU allocations on 2026-09-09. The six PyTorch-dependent scripts and the `assets/*.py` templates have never been run end to end. Read `VALIDATION.md` first (especially "Limitations"), then this file.

Working rules:
- Work on a branch and ask before pushing or merging.
- Run the unittest command and the bundle validator before committing.
- Keep `SKILL.md`, `README.md`, `scripts/validate_skill_bundle.py` `REQUIRED_PATHS` and `agents/openai.yaml` in sync.
- Record every result, including negative ones, in `VALIDATION.md`.
- Do not change training behavior in an asset or reference without saying so.
- Put temporary files in the scratchpad.

## Environment (checked 2026-09-28; re-check)

- The miniconda `python3` has `torch 2.11.0`, `scipy 1.17.1`, `numpy 2.4.4` and `torchrun`.
- MPS is available; CUDA is not. DDP/FSDP paths can only run on CPU with the `gloo` backend.
- `onnx`, `peft`, `torchvision` and `transformers` are **not** installed. Use a scratchpad venv; never install into the user's conda base.
- The 2 skipped tests are the *missing-torch* degradation tests (`CleanDegradationWithoutTorchTests`). They skip correctly because torch is present. To exercise them, run the suite under a torch-free Python.
- Sibling tooling to reuse instead of hand-run subagents:
  - Trigger tests: `../hep-analysis/tests/routing_eval.py --target deep-learning`. It runs an isolated `claude -p` with the 7 repo skills and grades routing to any owner.
  - Behavior tests: `../academic-papers/tests/run_prompts.py` or `../agile-development/tests/behavior_eval.py` (with and without the skill, blind grader).
  - Findings from the siblings: Haiku loads `SKILL.md` but rarely opens references, so must-do rules belong in `SKILL.md`. Compare at least 2 runs, because Haiku varies between identical runs. A usage-limit notice comes back as an ordinary result, so check for it.

## Questions for the user (ask before P1/P2)

- [ ] Which workloads matter most: vision, LLM fine-tuning, HEP/physics ML, or tabular? The answer sets which prompts and assets come first.
- [ ] Is GPU/CUDA testing available on another machine or in the cloud, for the DDP/FSDP/AMP paths that cannot run on this Mac?

## P1 - verification gaps (things never actually run)

- [ ] Run every `assets/*.py` template on tiny synthetic data on CPU: `train_classifier.py`, `ddp_train_skeleton.py` (2 processes, `gloo`, via `torchrun`), `transformer_classifier.py`, `lora_finetune.py` (needs `peft`), `vision_transfer.py` (needs `torchvision`), `inference.py`, `models.py`, `dataset_template.py`, `metrics.py`. Fix or document any that fail. Add a fast smoke test per asset that skips when a dependency is missing.
- [ ] Run each `scripts/*.py` against real PyTorch objects, not just `--help`:
  - `benchmark_model.py`;
  - `check_dataset_contract.py`;
  - `find_nan_batches.py`, with a NaN injected on purpose;
  - `inspect_checkpoint.py`, with and without optimizer state;
  - `profile_dataloader.py`;
  - `check_split_integrity.py`, with a deliberate leak.
- [ ] Cross-check the calculators against independent references, not only for self-consistency. Record the constants and units each one assumes.
  - `estimate_compute_budget.py`: the 6ND FLOPs rule and the Chinchilla numbers.
  - `serving_capacity.py`: Little's law and the queueing results, by hand.
  - `compare_model_runs.py`: paired bootstrap and seed variance vs `scipy`.
  - `estimate_training_memory.py`: already checked against CPU allocations (2026-09-09). Optionally also check on MPS.
- [ ] Execute the snippets in `references/*.md` that claim to be runnable: the shape tables in `tensor-shapes.md`, AMP/GradScaler in `mixed-precision.md`, `checkpointing.md`, the hooks in `custom-autograd-and-hooks.md`, and export in `export-and-deployment.md`. Flag API drift against torch 2.11:
  - deprecated `torch.cuda.amp.*`;
  - the `torch.load` `weights_only` default;
  - `torch.compile` options;
  - `torch.export`;
  - TorchScript deprecation.
- [ ] Audit the numbers and claims in `references/` against primary sources: scaling laws, MFU figures, memory multipliers, FSDP/ZeRO behavior, calibration thresholds. Remove or soften anything unsourced, and date anything time-sensitive.

## P2 - test that the skill changes model behavior

- [ ] Write 12-15 realistic prompts in `tests/prompts.md`, each with Must and Must-not lists (which rule fires, which reference is read). Cover:
  - NaN loss under AMP;
  - a validation metric that collapses because of group leakage;
  - choosing between DDP and FSDP;
  - missing optimizer state on resume;
  - a slow DataLoader;
  - a shape, device or dtype error;
  - "make it faster" (ambiguous, should ask);
  - "add a SOTA accuracy claim" (should audit);
  - an ECE/calibration claim;
  - a LoRA config;
  - an ONNX export mismatch;
  - a TensorFlow/JAX request (must not trigger);
  - an HEP-ML request (equivariant or physics-informed; check routing with `hep-analysis`);
  - a sklearn-only question (must not trigger).
- [ ] Run the prompts with and without the skill on Haiku and Sonnet, and on Opus if possible, with at least 2 runs each. Log the results in `VALIDATION.md`.
- [ ] Build trigger sets: `tests/trigger_queries.json` for tuning (20 should-trigger, 20 should-not) and a held-out set that is never tuned on. Near-misses to include: TensorFlow/JAX, generic statistics, `hep-analysis` ROOT ML, LLM API usage.
  - Include the isolated routing eval data from 2026-09-26 (`hep-analysis/tests/trigger_queries_holdout.json`, 2 runs per query). Sonnet got 6/6 right and Haiku 2/6. Haiku's results on three queries:
    - "Explain equivariant neural networks for point clouds and when they beat a plain transformer": 0/2 (none).
    - "How do I set up mixed precision and gradient checkpointing for a 1B parameter model in PyTorch?": 1/2.
    - "My GNN for jet tagging overfits after 3 epochs, what regularization should I try?": 0/2 (none once, `hep-analysis` once).
  - The description is 979 of 1024 characters, so there is little headroom.
- [ ] Routing hygiene with `hep-analysis`, `agile-development`, `academic-papers` and `task-authoring`. Run each affected skill's validator and tests after any description change.

## P3 - content and structure

- [ ] Progressive disclosure: `SKILL.md` is 273 lines and the 31 references total about 3,000 lines. Measure the references read per task from the P2 runs; the target is at most 2-3. Add "read only if" hints where a routing row is vague.
- [ ] Look for overlap:
  - `parallelism-strategy.md` vs `distributed-training.md` vs `training-at-scale.md`;
  - `evaluation-strategy.md` vs `evaluation-metrics.md`;
  - `data-strategy.md` vs `data-loading.md`.

  Merge or cross-link duplicated tables.
- [ ] Add coverage only where the prompt tests confirm a gap: FSDP2/`torch.distributed.tensor`, `torch.compile` graph-break debugging, Apple MPS pitfalls, activation checkpointing, metric aggregation in data-parallel eval, and the KV-cache for inference-time attention.
- [ ] Add regression tests for thinly covered scripts, especially error paths: empty dataset, NaN input, wrong checkpoint keys, zero-length split. The current tests mostly check `--help` and the missing-torch exit path.
- [ ] Add a minimal end-to-end smoke test under `assets/` plus `tests/`: synthetic data -> `check_dataset_contract` -> `check_split_integrity` -> `train_classifier` -> `inspect_checkpoint` -> `compare_model_runs`. `examples/` no longer exists.
- [ ] Multi-platform check (Codex, Antigravity): confirm `agents/openai.yaml` is current and that no instructions depend on Claude-only tools.
- [ ] Skill-reviewer pass on `SKILL.md` and `README.md` (`plugin-dev:skill-reviewer`).

## P4 - housekeeping

- [ ] Recurring: update the `VALIDATION.md` header after each pass. It is still dated 2026-09-05 and says PyTorch is not installed. "Limitations" already marks that as superseded, but the header does not. Also record the current counts: 61 files, 106 tests, 2 skipped.
- `.pytest_cache/` and `__pycache__/` are git-ignored; leave them alone.
- Dropped: the two items about the 24 examples (archetype rules, runnable snippets). `examples/` was removed on 2026-09-25, as in the sibling skills.
