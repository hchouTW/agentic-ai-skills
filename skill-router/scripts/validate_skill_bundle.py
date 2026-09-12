#!/usr/bin/env python3
"""Validate the skill-router bundle's structural integrity.

Purpose: catch accidental deletions or truncations of files this skill's SKILL.md
and README.md depend on, and sanity-check the routing table against whatever
sibling skill folders are actually installed.

What it does: checks that every file this package is expected to ship (SKILL.md,
README.md, agents metadata, scripts, tests) exists and is non-empty, that SKILL.md
has YAML frontmatter with name/description, that README.md has its expected
section headers, and (informationally only - a missing sibling is not an error,
since skill-router is designed to route only to whatever is actually installed)
reports any routed skill name with no matching sibling folder next to this one.

Usage: run with no arguments from anywhere; it resolves paths relative to its own
location. `python3 scripts/validate_skill_bundle.py`. No third-party dependencies.
"""
from __future__ import annotations

import re
from pathlib import Path

REQUIRED_PATHS = [
    "SKILL.md",
    "README.md",
    "VALIDATION.md",
    "agents/openai.yaml",
    "scripts/validate_skill_bundle.py",
    "tests/test_skill_router.py",
    "examples/README.md",
    "examples/01-adding-a-routing-rule-without-overlap.md",
    "examples/02-multi-skill-primary-secondary-routing.md",
    "examples/03-negative-carve-out-not-a-match.md",
    "examples/04-decision-tree-multi-skill-ambiguous-routing.md",
    "examples/05-trajectory-single-clean-match-academic-papers.md",
    "examples/06-trajectory-generic-verb-vs-domain-specific-rule.md",
    "examples/07-trajectory-clean-no-match-proceed-normally.md",
    "examples/08-gated-pipeline-adding-a-new-rule.md",
    "examples/09-gated-pipeline-disambiguating-figure-interpretation.md",
    "examples/10-gated-pipeline-expanding-a-carve-out.md",
    "examples/11-decision-tree-figure-interpretation-routing.md",
    "examples/12-decision-tree-multiple-false-positive-keywords.md",
    "examples/13-adversarial-audit-new-routing-rule-proposal.md",
    "examples/14-test-first-routing-parser-primary-secondary.md",
]

REQUIRED_README_SECTIONS = [
    "## Installation and invocation",
    "## Quick checks",
    "## Coverage and boundaries",
    "## Example prompts",
]

# Matches "- **skill-name** - ..." bullet items under "## Routing rules".
ROUTING_ENTRY_RE = re.compile(r"^- \*\*([a-z0-9][a-z0-9-]*)\*\*", re.MULTILINE)


def extract_routed_skill_names(skill_md_text: str) -> list[str]:
    """Return the skill names named in SKILL.md's routing-rule bullets, in order."""
    return ROUTING_ENTRY_RE.findall(skill_md_text)


def find_sibling_skill_dirs(root: Path) -> set[str]:
    """Return the names of sibling folders (next to this skill) that look like
    installed skills, i.e. contain their own SKILL.md."""
    parent = root.parent
    if not parent.is_dir():
        return set()
    return {
        child.name
        for child in parent.iterdir()
        if child.is_dir() and child.name != root.name and (child / "SKILL.md").exists()
    }


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

    routed = extract_routed_skill_names(skill)
    if not routed:
        print("SKILL.md's routing rules did not yield any skill names - check the format")
        raise SystemExit(1)
    siblings = find_sibling_skill_dirs(root)
    if siblings:
        unmatched = [name for name in routed if name not in siblings]
        if unmatched:
            print("note: routed skill(s) not currently installed as a sibling folder "
                  "(not an error - skill-router only routes to what's installed):")
            for name in unmatched:
                print(f"  {name}")

    print(f"Bundle OK: {len(REQUIRED_PATHS)} files present and non-empty, "
          f"{len(routed)} routing entries found ({', '.join(routed)}).")


if __name__ == "__main__":
    main()
