#!/usr/bin/env python3
"""Scaffold an empty canonical example for a skill's `examples/` directory.

Purpose: give every `<skill>/examples/*.md` file the same shape - frontmatter plus
Scenario / Common Weak Approach / Expert-Level Best Practice / Key Takeaways
sections - before an agent fills in the actual domain content. Mirrors how
`create_story_card.py` scaffolds a story card without inventing the story.

What it does: prints (or writes) a markdown skeleton with `role`/`skill`/`use_case`
frontmatter and the four required section headers, with one HTML-comment
placeholder per section and one placeholder bullet per requested takeaway. It does
not generate content - see references/example-authoring.md for the generation
prompt and format spec, and `validate_skill_example.py` for checking a filled-in
file.

Usage: `python3 scripts/generate_skill_example.py --skill hep-analysis --role
"Senior Experimental Particle Physicist" --use-case "..." [--takeaways 4]
[--output ../hep-analysis/examples/01-slug.md]`. Prints to stdout when `--output`
is omitted. Standard library only.
"""

from __future__ import annotations

import argparse
from pathlib import Path

MIN_TAKEAWAYS = 3
MAX_TAKEAWAYS = 6


def build_skeleton(args: argparse.Namespace) -> str:
    takeaway_lines = "\n".join(
        f"- <!-- Takeaway {i}: why the expert approach differs architecturally, not just what changed. -->"
        for i in range(1, args.takeaways + 1)
    )

    return f"""---
role: {args.role}
skill: {args.skill}
use_case: {args.use_case}
---

## Scenario

<!-- 2-4 sentences describing the realistic scenario: {args.use_case} -->

## Common Weak Approach

<!-- A complete, realistic artifact showing the failure mode - not a caricature. -->

## Expert-Level Best Practice

<!-- A complete artifact solving the same scenario correctly, with zero placeholders. -->

## Key Takeaways

{takeaway_lines}
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scaffold an empty canonical example skeleton for a skill's examples/ directory."
    )
    parser.add_argument("--skill", required=True, help="Target skill folder name, e.g. hep-analysis.")
    parser.add_argument("--role", required=True, help="Senior role to author as, e.g. 'Staff Software Engineer'.")
    parser.add_argument("--use-case", required=True, dest="use_case", help="Realistic, narrow domain scenario.")
    parser.add_argument(
        "--takeaways",
        type=int,
        default=4,
        help=f"Number of key-takeaway placeholders ({MIN_TAKEAWAYS}-{MAX_TAKEAWAYS}, default 4).",
    )
    parser.add_argument("--output", type=Path, help="Optional output path. Prints to stdout when omitted.")
    args = parser.parse_args()
    if not MIN_TAKEAWAYS <= args.takeaways <= MAX_TAKEAWAYS:
        parser.error(f"--takeaways must be between {MIN_TAKEAWAYS} and {MAX_TAKEAWAYS}")
    return args


def main() -> int:
    args = parse_args()
    content = build_skeleton(args)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(content, encoding="utf-8")
    else:
        print(content, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
