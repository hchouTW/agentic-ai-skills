#!/usr/bin/env python3
"""Validate the deep-learning skill bundle's structural integrity.

Purpose: catch accidental deletions or truncations of files this skill's SKILL.md
and README.md depend on.

What it does: checks that every file this package is expected to ship (SKILL.md,
README.md, agents metadata, references, assets, scripts, tests) exists and is
non-empty, that SKILL.md has YAML frontmatter with name/description, and that
README.md has its expected section headers.

Usage: run with no arguments from anywhere; it resolves paths relative to its own
location. `python3 scripts/validate_skill_bundle.py`. No third-party dependencies
(does not require PyTorch).
"""
from __future__ import annotations

from pathlib import Path

REQUIRED_PATHS = [
    "SKILL.md",
    "README.md",
    "VALIDATION.md",
    "agents/openai.yaml",
    "references/checkpointing.md",
    "references/cpp-balanced-design-guidelines.md",
    "references/custom-autograd-and-hooks.md",
    "references/data-loading.md",
    "references/debugging-pytorch.md",
    "references/distributed-training.md",
    "references/efficient-finetuning.md",
    "references/evaluation-metrics.md",
    "references/export-and-deployment.md",
    "references/generative-models.md",
    "references/mixed-precision.md",
    "references/performance-memory.md",
    "references/reproducibility.md",
    "references/sequence-models.md",
    "references/tensor-shapes.md",
    "references/training-loop.md",
    "references/transfer-learning.md",
    "references/transformer-architectures.md",
    "assets/config.yaml",
    "assets/dataset_template.py",
    "assets/ddp_train_skeleton.py",
    "assets/inference.py",
    "assets/lora_finetune.py",
    "assets/metrics.py",
    "assets/models.py",
    "assets/train_classifier.py",
    "assets/transformer_classifier.py",
    "assets/vision_transfer.py",
    "scripts/benchmark_model.py",
    "scripts/check_dataset_contract.py",
    "scripts/check_pytorch_env.py",
    "scripts/find_nan_batches.py",
    "scripts/inspect_checkpoint.py",
    "scripts/profile_dataloader.py",
    "scripts/validate_skill_bundle.py",
    "tests/test_deep_learning_skill.py",
]

REQUIRED_README_SECTIONS = [
    "## Installation and invocation",
    "## Quick checks",
    "## Coverage and boundaries",
    "## Example prompts",
]


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    missing = [path for path in REQUIRED_PATHS if not (root / path).exists()]
    empty = [
        path
        for path in REQUIRED_PATHS
        if (root / path).exists() and (root / path).stat().st_size == 0
    ]

    if missing or empty:
        if missing:
            print("missing files:")
            for path in missing:
                print(f"  {path}")
        if empty:
            print("empty files:")
            for path in empty:
                print(f"  {path}")
        raise SystemExit(1)

    skill = (root / "SKILL.md").read_text(encoding="utf-8")
    if not skill.startswith("---\n"):
        print("SKILL.md is missing YAML frontmatter")
        raise SystemExit(1)
    frontmatter = skill.split("---", 2)[1]
    for field in ("name:", "description:"):
        if field not in frontmatter:
            print(f"SKILL.md frontmatter is missing {field}")
            raise SystemExit(1)

    readme = (root / "README.md").read_text(encoding="utf-8")
    missing_sections = [s for s in REQUIRED_README_SECTIONS if s not in readme]
    if missing_sections:
        print("README.md is missing sections:")
        for section in missing_sections:
            print(f"  {section}")
        raise SystemExit(1)

    print(f"Bundle OK: {len(REQUIRED_PATHS)} files present and non-empty.")


if __name__ == "__main__":
    main()
