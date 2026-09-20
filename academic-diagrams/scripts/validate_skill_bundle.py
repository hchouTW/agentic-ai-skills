#!/usr/bin/env python3
"""Validate the academic-diagrams skill bundle's structural integrity.

Purpose: catch accidental deletions, truncations, or broken relative links in the files
this skill's SKILL.md and README.md depend on.

What it does: checks that every expected file exists and is non-empty, that SKILL.md has
YAML frontmatter with name/description (name must equal the folder name), that README.md has
its expected section headers, that every relative markdown link in SKILL.md resolves, and that
every examples/*/ directory holds at least one example.

Usage: `python3 scripts/validate_skill_bundle.py` from anywhere; paths resolve relative to this
file. Standard library only.
"""
from __future__ import annotations

import re
from pathlib import Path

REQUIRED_PATHS = [
    "SKILL.md",
    "README.md",
    "VALIDATION.md",
    "agents/openai.yaml",
    "references/general-diagram-principles.md",
    "references/academic-figure-style.md",
    "references/high-energy-physics.md",
    "references/probability-statistics.md",
    "references/computer-science.md",
    "references/mermaid-patterns.md",
    "references/graphviz-patterns.md",
    "references/tikz-patterns.md",
    "references/plantuml-patterns.md",
    "references/figure-captions.md",
    "references/legends-panels-and-export.md",
    "templates/research-workflow.md",
    "templates/algorithm-flowchart.md",
    "templates/system-architecture.md",
    "templates/hep-analysis-pipeline.md",
    "templates/probabilistic-graphical-model.md",
    "templates/agentic-ai-architecture.md",
    "templates/svg-spec.md",
    "templates/ml-pipeline.md",
    "templates/bayesian-model.md",
    "examples/README.md",
    "scripts/validate_skill_bundle.py",
    "scripts/check_diagram_sources.py",
    "tests/test_academic_diagrams_skill.py",
]

EXAMPLE_DIRS = ["general", "hep", "statistics", "computer-science"]

REQUIRED_README_SECTIONS = [
    "## Installation and invocation",
    "## Quick checks",
    "## Coverage and boundaries",
    "## Example prompts",
]

LINK_RE = re.compile(r"\]\(([^)#\s]+)(?:#[^)]*)?\)")


def broken_links(md_path: Path) -> list[str]:
    """Return relative link targets in md_path that do not exist."""
    text = md_path.read_text(encoding="utf-8")
    bad = []
    for target in LINK_RE.findall(text):
        if re.match(r"^[a-z]+:", target):
            continue
        if not (md_path.parent / target).exists():
            bad.append(target)
    return bad


def frontmatter_fields(skill_text: str) -> dict[str, str]:
    """Parse the flat `key: value` lines of a SKILL.md frontmatter block."""
    if not skill_text.startswith("---\n"):
        return {}
    block = skill_text.split("---", 2)[1]
    fields = {}
    for line in block.splitlines():
        if ":" in line and not line.startswith(" "):
            key, _, value = line.partition(":")
            fields[key.strip()] = value.strip()
    return fields


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    problems: list[str] = []

    for path in REQUIRED_PATHS:
        p = root / path
        if not p.exists():
            problems.append(f"missing file: {path}")
        elif p.stat().st_size == 0:
            problems.append(f"empty file: {path}")

    for d in EXAMPLE_DIRS:
        files = sorted((root / "examples" / d).glob("*.md"))
        if not files:
            problems.append(f"examples/{d}/ has no example files")

    if (root / "SKILL.md").exists():
        skill = (root / "SKILL.md").read_text(encoding="utf-8")
        fm = frontmatter_fields(skill)
        if not fm:
            problems.append("SKILL.md is missing YAML frontmatter")
        else:
            for field in ("name", "description"):
                if not fm.get(field):
                    problems.append(f"SKILL.md frontmatter is missing {field}")
            if fm.get("name") and fm["name"] != root.name:
                problems.append(f"SKILL.md name {fm['name']!r} != folder {root.name!r}")
        for target in broken_links(root / "SKILL.md"):
            problems.append(f"SKILL.md has a broken relative link: {target}")

    if (root / "README.md").exists():
        readme = (root / "README.md").read_text(encoding="utf-8")
        for section in REQUIRED_README_SECTIONS:
            if section not in readme:
                problems.append(f"README.md is missing section: {section}")

    if problems:
        print("Bundle problems:")
        for problem in problems:
            print(f"  {problem}")
        raise SystemExit(1)
    print(f"Bundle OK: {len(REQUIRED_PATHS)} files present and non-empty.")


if __name__ == "__main__":
    main()
