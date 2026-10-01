# TODO for future Claude sessions (deep-learning)

State (verified 2026-10-01 on `main` at 50d048e): `python3 scripts/validate_skill_bundle.py` OK (67 files); `python3 -m unittest discover -s tests` 118 tests OK, 3 skipped (2 missing-torch degradation tests, 1 torchvision-gated test). PRs #32 to #37 are merged: P1 verification, the P2 behavior and trigger tests, the `SKILL.md` rules, the fresh confirmation prompts, the description rewrite, and the natural-invocation arm. `SKILL.md` is 316 lines and the description is 844 of 1024 characters. Read `VALIDATION.md` first (the 2026-10-01 sections are the current results), then this file.

## Where things stand (numbers are in `VALIDATION.md`)

- **Verification (P1):** assets (except `vision_transfer.py`) and PyTorch-dependent scripts were run on CPU/MPS; calculators were cross-checked; reference snippets were executed on torch 2.11. Fixed: DDP skeleton CPU/gloo fallback, MPS timing in `benchmark_model.py`, small-n detectable effect in `compare_model_runs.py`. Documented drift: `torch.load` `weights_only`, TorchScript deprecation, ONNX needing `onnxscript`.
- **Behavior with the skill forced** (3 runs; same plan-only frame; blind Sonnet scorer): H1-H15 Haiku 66.5 to 78.0%, Sonnet 81.6 to 97.1%. On the fresh set H101-H114 (written after the rules, not tuned on) Haiku 58.2 to 80.1%, Sonnet 80.1 to 95.2%, so the `SKILL.md` rules generalize.
- **Behavior with natural invocation** (`behavior_eval.py run --natural`; the model decides to load the skill): the skill loads on only about 30% of plan-only runs (8-9 of 28-30), so the scores sit between baseline and forced (Haiku 67.5 and 68.6%, Sonnet 89.9 and 92.2%). When it loads, scores match the forced arm.
- **Triggering** (`routing_eval.py`, bare query, 2 runs): Sonnet tuning recall 17/40 to 40/40 and holdout 18/20 with 0 false triggers after the description rewrite; Haiku stays near 0 (2/40 tuning, 0/20 holdout) because it rarely calls any skill in this harness, for the sibling skills too. `hep-analysis` routing was not harmed (36/40 vs 38/40 recall, owner routing 73/80 vs 69/80).

Working rules:
- Work on a branch. Ask before committing, pushing or merging. The user merges PRs (`! gh pr merge N --merge` from the prompt); the auto-mode classifier blocks `gh pr merge` and permission-rule changes from Claude.
- Run the unittest command and the bundle validator before committing.
- Keep `SKILL.md`, `README.md`, `scripts/validate_skill_bundle.py` `REQUIRED_PATHS` and `agents/openai.yaml` in sync.
- Record every result, including negative ones, in `VALIDATION.md`.
- Do not change training behavior in an asset or reference without saying so.
- Put temporary files in the scratchpad. Behavior and routing evals call `claude -p` and cost money (about $1-2 per model per routing run, about $2-6 per model per 3-run behavior pass).

## Environment (checked 2026-10-01; re-check)

- The miniconda `python3` has `torch 2.11.0`, `scipy 1.17.1`, `numpy 2.4.4` and `torchrun`.
- MPS is available; CUDA is not (the user confirmed there is no GPU). DDP/FSDP paths run on CPU with `gloo` only; the CUDA/NCCL path is untested.
- `onnx`, `onnxscript`, `peft`, `torchvision` and `transformers` are **not** installed. Use a scratchpad venv; never install into the user's conda base.
- The 2 missing-torch tests skip correctly because torch is present; run the suite under a torch-free Python to exercise them.
- Eval tooling:
  - Triggers: `../hep-analysis/tests/routing_eval.py <file> --target deep-learning --model sonnet --runs 2 -j 3 --out FILE`. Isolated `claude -p`, the 7 repo skills, no fixture repository, bare query.
  - Behavior: `tests/behavior_eval.py` (`run`, `score --blind`, `report`; `--prompts FILE` selects `prompts.md` or `prompts_fresh.md`; `--arms skill` re-runs only the skill arm; `--natural` lets the model decide whether to load the skill). Copy old baseline runs into a new run directory to reuse them.
- Lessons for running evals:
  - The forced skill arm tells the child to read `SKILL.md`, so it cannot test the description; use `--natural` or `routing_eval.py`.
  - The plan-only "planning exercise" frame lowers how often the skill loads, so the routing eval (bare query) is the better trigger estimate and the natural arm is a lower bound.
  - Haiku loads `SKILL.md` when told to but opens almost no references (about 0.3 per run); Sonnet reads about 2.4-3. Must-do rules belong in `SKILL.md`.
  - The blind scorer identifies Sonnet's arm in nearly every plan, so Sonnet comparisons are effectively open-label. It sometimes returns no JSON for a prompt: rescore with `score --only HNNN`.
  - Compare at least 2 runs, because Haiku varies between identical runs. A usage-limit notice comes back as an ordinary result, so check for it.

## P1 - verification leftovers

Round 7 (2026-10-01) executed the assert blocks in `tensor-shapes.md` and `debugging-pytorch.md` (all fine; see `VALIDATION.md`).

- [ ] `vision_transfer.py`: run it with `torchvision` in a scratchpad venv on a tiny `ImageFolder` tree (only `--help` is tested, and only when torchvision is installed). Check the pretrained-weight download path.
- [ ] Run the ONNX snippet in `references/export-and-deployment.md` with `onnx` and `onnxscript` in the venv, on both the dynamo default and `dynamo=False` paths, and confirm the `dynamic_axes` advice.
- [ ] Audit the numbers and claims in `references/` against primary sources: scaling laws, MFU figures, memory multipliers, FSDP/ZeRO behavior, calibration thresholds. Remove or soften anything unsourced, and date anything time-sensitive. Not started.
- [ ] Check `estimate_training_memory.py` on MPS (it was checked against CPU allocations on 2026-09-09).
- [ ] Script rough edges: `find_nan_batches.py` now exits 1 on non-finite values and `check_dataset_contract.py` exits with a message on ragged samples (round 7). Still open: the data scripts (`check_dataset_contract.py`, `find_nan_batches.py`, `profile_dataloader.py`) only accept a dataset through the `create_dataset()` hook, with no CLI path.
- [ ] The CUDA/NCCL path of `ddp_train_skeleton.py` and the AMP/CUDA paths stay untested without a GPU. Say so wherever they are relied on.

## P2 - behavior and trigger testing (first pass done; follow-ups)

- [ ] **Bare-query behavior harness.** Add a mode that gives the prompt with no "planning exercise" frame and the skill available, so the load rate and the behavior approximate real use. Re-measure the natural arm there.
- [ ] **Make advice-style prompts load the skill.** In the natural arm Sonnet loaded on H1, H4, H5, H7 and never on H2, H3, H6, H9, H11. Try a change to the description or the top of `SKILL.md`, then check it with the routing eval. The holdout `tests/trigger_queries_holdout.json` has now been used once; write a new holdout before tuning against it again.
- [ ] **A new prompt set (H201 and up) before changing `SKILL.md` again.** Do not tune against H101-H114. Candidates for the next rule changes: out-of-scope ceremony in the forced arm (Sonnet H14 scikit-learn 83 and H110 XGBoost 83 on bullet (c); it does not occur in the natural arm); keeping the NaN fix minimal (H113: Haiku 79 to 67, Sonnet 88 to 83); Haiku H106 (13B on 40 GB, 62) and H114 (Lorentz equivariance, 58) and H105 bullet (c) (permutation vs Lorentz symmetry); Sonnet H8 and H13; Haiku H5 and H7 bullet (d).
- [ ] Opus runs of the behavior and routing sets (none yet).
- [ ] Routing hygiene: after the 2026-10-01 rewrite, `hep-analysis` was checked on Sonnet only. Check `agile-development`, `academic-papers`, `ams-analysis` and `task-authoring` routing (and Haiku) after any further description change, and run each affected skill's validator and tests.
- [ ] Haiku does not call any skill in the routing harness. Decide whether to say so in the README as a known limit, and whether any claim should be Sonnet-only.

## P3 - content and structure

- [ ] Progressive disclosure: `SKILL.md` is 316 lines and the 31 references total 2,986 lines. Measured references per forced-skill run: Haiku 0.3, Sonnet 2.4-3.0 (target at most 2-3). Add "read only if" hints where a routing row is vague, and move any rule Haiku keeps missing into `SKILL.md` (the 2026-10-01 "Rules to Apply Even Without Opening a Reference" section is the pattern).
- [ ] Look for overlap:
  - `parallelism-strategy.md` vs `distributed-training.md` vs `training-at-scale.md`;
  - `evaluation-strategy.md` vs `evaluation-metrics.md`;
  - `data-strategy.md` vs `data-loading.md`.

  Merge or cross-link duplicated tables.
- [ ] Add coverage only where the prompt tests confirm a gap: FSDP2/`torch.distributed.tensor`, `torch.compile` graph-break debugging, Apple MPS pitfalls, activation checkpointing, metric aggregation in data-parallel eval, and the KV-cache for inference-time attention.
- [ ] Add regression tests for thinly covered scripts, especially error paths: empty dataset, NaN input, wrong checkpoint keys, zero-length split. `tests/test_assets_smoke.py` covers the assets; the scripts' tests mostly check `--help` and the missing-torch exit path.
- [ ] Add a minimal end-to-end smoke test: synthetic data -> `check_dataset_contract` -> `check_split_integrity` -> `train_classifier` -> `inspect_checkpoint` -> `compare_model_runs`.
- [ ] Multi-platform check (Codex, Antigravity): confirm `agents/openai.yaml` is current and that no instructions depend on Claude-only tools. The new "Scope and Proportion" and "Rules" sections in `SKILL.md` were not checked on those platforms.
- [ ] Skill-reviewer pass on `SKILL.md` (now 316 lines) and `README.md` (`plugin-dev:skill-reviewer`).

## P4 - housekeeping

- [ ] Recurring: update the `VALIDATION.md` header after each pass (current: 2026-10-01, 67 files, 118 tests, 3 skipped).
- `.pytest_cache/` and `__pycache__/` are git-ignored; leave them alone.
- Dropped: the two items about the 24 examples (archetype rules, runnable snippets). `examples/` was removed on 2026-09-25, as in the sibling skills.
