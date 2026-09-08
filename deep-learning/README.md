# PyTorch Engineering Skill

A portable Agent Skill maintained entirely in English. Its core is `SKILL.md` plus references, helper scripts, and starting-point templates resolved through relative paths. It requires no specific MCP server, cloud account, or paid service beyond a working PyTorch installation for the scripts that exercise real tensors/models.

## Installation and invocation

Extract the archive and keep the complete `deep-learning/` folder.

- **Codex:** place the folder in the skill directory used by your environment, commonly `~/.codex/skills/`, or import it through the mechanism supported by your version. Reload skills and invoke `$deep-learning`. `agents/openai.yaml` supplies optional Codex UI metadata.
- **Claude Code:** copy it to `.claude/skills/deep-learning/` in the project or `~/.claude/skills/deep-learning/` for personal use. Invoke `/deep-learning` or describe a matching task (train a model, fix a NaN loss, review a DataLoader). See the [official Claude Code skill documentation](https://code.claude.com/docs/en/skills).
- **Other agents:** instruct the agent to read `SKILL.md` first and follow its reference routing. Provide the file location explicitly if automatic discovery is unsupported.

This delivery creates a single folder; it does not change other global agent settings. Load references selectively instead of pasting the entire package into global instructions.

## Quick checks

From the skill directory:

```bash
python3 -m unittest discover -s tests -v
python3 scripts/validate_skill_bundle.py
python3 scripts/check_pytorch_env.py
python3 scripts/inspect_checkpoint.py <checkpoint.pt>
python3 scripts/check_dataset_contract.py --help
python3 scripts/find_nan_batches.py --help
python3 scripts/profile_dataloader.py --help
python3 scripts/benchmark_model.py --help
```

All six require PyTorch to actually run (`check_pytorch_env.py` reports its absence clearly; the other five accept `--help` and fail with a clear message rather than a raw traceback when PyTorch is missing). None require a GPU; they fall back to CPU.

## Coverage and boundaries

The package covers writing and reviewing PyTorch code: `nn.Module` models, training and evaluation loops, datasets and DataLoaders, losses, optimizers, schedulers, mixed precision, gradient accumulation, checkpointing, distributed training (DDP), reproducibility, inference, and performance/memory tuning, plus debugging tensor shape/device/dtype errors, NaNs, and slow dataloaders. It also covers Transformer/attention architectures and positional encoding, RNN/LSTM/GRU sequence models (packed sequences, teacher forcing, seq2seq), generative models (VAE/GAN/diffusion training loops and their characteristic failure modes), parameter-efficient fine-tuning (LoRA) and quantization, custom `autograd.Function`s/hooks/activation checkpointing, and model export and deployment (TorchScript, ONNX, `torch.compile` serving modes).

It is explicitly PyTorch-only - not TensorFlow, JAX, or other frameworks - and does not cover general C++ unrelated to LibTorch/custom ops. For broader engineering process (scoping, testing, review), pair it with `agile-development`.

All maintained instructions, templates, and metadata are in English. The skill can still answer a user in their requested language.

## Example prompts

"Write a training loop for a ResNet18 fine-tune on a custom image dataset."

"My loss goes to NaN after a few hundred steps - here's my training code."

"Review this Dataset/DataLoader for correctness and performance."
