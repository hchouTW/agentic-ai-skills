# PyTorch Engineering Skill

An Agent Skill for PyTorch work: writing, debugging, reviewing and explaining models, training and evaluation code, plus the engineering decisions around them (scaling, evaluation design, serving, drift, calibration). It is PyTorch-only, so it is not for TensorFlow, JAX or scikit-learn. It needs no MCP server, cloud account or paid service; only the scripts that run real tensors need a working PyTorch installation, and none need a GPU.

`SKILL.md` is the entry point. It routes to `references/`, `scripts/` and `assets/` through relative paths, so keep the whole `deep-learning/` folder together.

## Installation and invocation

- **Codex:** place the folder in `~/.codex/skills/` (or wherever your environment loads skills), reload skills, and invoke `$deep-learning`. `agents/openai.yaml` holds optional Codex UI metadata.
- **Claude Code:** copy it to `.claude/skills/deep-learning/` in a project or `~/.claude/skills/deep-learning/` for personal use. Invoke `/deep-learning` or describe a matching task. See the [official Claude Code skill documentation](https://code.claude.com/docs/en/skills).
- **Antigravity:** copy it to `.agents/skills/deep-learning/` in the workspace or `~/.gemini/config/skills/deep-learning/` for a global install (older installs may read `.agent/skills/`). It triggers automatically from the `name`/`description` and needs no explicit invocation. See the [Antigravity skills documentation](https://antigravity.google/docs/skills).
- **Other agents:** tell the agent to read `SKILL.md` first and follow its reference routing, giving the file location explicitly if discovery is unsupported.

Installing only adds this folder; it changes no other agent settings. Install `agile-development` in the same parent directory if you want the C++ design reference that `SKILL.md` links to (`../agile-development/references/cpp-balanced-design-guidelines.md`).

All maintained instructions, templates and metadata are in English. The skill can still answer in the user's language.

## Quick checks

Run from the `deep-learning/` directory:

```bash
python3 scripts/validate_skill_bundle.py
python3 -m unittest discover -s tests
python3 scripts/check_pytorch_env.py
python3 scripts/estimate_training_memory.py assets/scaling_plan.example.json
python3 scripts/estimate_compute_budget.py --params 7e9 --tokens 1.4e12 --gpus 64
python3 scripts/compare_model_runs.py assets/eval_runs.example.json
python3 scripts/serving_capacity.py --qps 500 --batch-size 16 --batch-latency-ms 40 --latency-budget-ms 250
python3 scripts/check_split_integrity.py assets/dataset_splits.example.json
```

- `check_split_integrity.py` exits nonzero on the shipped example, which contains a deliberate group leak.
- Standard library only (no PyTorch): the estimator scripts above, `compare_model_runs.py`, `serving_capacity.py`, `check_split_integrity.py`.
- Need PyTorch: `check_pytorch_env.py`, `inspect_checkpoint.py <checkpoint.pt>`, `check_dataset_contract.py`, `find_nan_batches.py`, `profile_dataloader.py`, `benchmark_model.py` (run the last four with `--help` for arguments).

Validation history and measured results are in `VALIDATION.md`; open items are in `TODO.md`.

## Coverage and boundaries

Covers:

- PyTorch code: models, training and evaluation loops, datasets and DataLoaders, losses, optimizers, mixed precision, checkpointing, DDP/FSDP, reproducibility, inference, and speed/memory tuning.
- Debugging shape, device and dtype errors, NaN or exploding loss, and slow dataloaders.
- Model families and techniques: Transformers, RNN/LSTM, VAE/GAN/diffusion, transfer learning, LoRA and quantization, autograd and hooks, export (TorchScript, ONNX, `torch.compile`).
- Architecture and scaling decisions, ablations and seed noise, parallelism strategy, compute and cost budgets.
- Data and evaluation: splits and leakage, eval design, metrics, serving capacity, drift and lifecycle.
- Scientific ML: uncertainty and calibration, distribution shift, physics-informed and equivariant models, interpretation limits.

Defers or out of scope:

- Other frameworks (TensorFlow, JAX, scikit-learn).
- General C++ design, except where it borders PyTorch (LibTorch, custom ops, CUDA extensions); this points to `agile-development`.
- Engineering process (scoping, testing, review): pair with `agile-development`.
- Statistical validity of a downstream scientific conclusion: pair with `academic-papers`.

## Example prompts

- "Write a training loop for a ResNet18 fine-tune on a custom image dataset."
- "My loss goes to NaN after a few hundred steps; here is my training code."
- "Review this Dataset/DataLoader for correctness and performance."
- "Which parallelism strategy fits a 7B model on 64 GPUs?"
- "Are these two runs actually different, or is it seed noise?"
- "Why does my validation score look too good? Check my splits for leakage."
