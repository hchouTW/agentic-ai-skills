#!/usr/bin/env python3
"""Generate an Agile story-card markdown file."""

from __future__ import annotations

import argparse
from pathlib import Path


def build_card(args: argparse.Namespace) -> str:
    criteria = args.criteria or [
        "Given the primary context, when the user performs the action, then the expected result is observable.",
        "Given an invalid or boundary context, when the action is attempted, then the system responds safely.",
    ]
    validation = args.validation or ["Run the focused test or check that proves the behavior."]

    criteria_lines = "\n".join(f"- [ ] {item}" for item in criteria)
    validation_lines = "\n".join(f"- [ ] {item}" for item in validation)

    return f"""# Story Card

## Story

As a {args.actor}, I want {args.capability}, so that {args.outcome}.

## Acceptance Criteria

{criteria_lines}

## Assumptions

- {args.assumption}

## Scope

In:
- {args.in_scope}

Out:
- {args.out_of_scope}

## Validation

{validation_lines}

## Risks

- {args.risk}
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a markdown Agile story card.")
    parser.add_argument("--actor", required=True, help="User, operator, developer, or system actor.")
    parser.add_argument("--capability", required=True, help="Capability or behavior wanted by the actor.")
    parser.add_argument("--outcome", required=True, help="Measurable benefit or outcome.")
    parser.add_argument("--criteria", action="append", help="Acceptance criterion. Repeat for multiple criteria.")
    parser.add_argument("--validation", action="append", help="Validation step. Repeat for multiple checks.")
    parser.add_argument("--assumption", default="No material assumptions identified yet.")
    parser.add_argument("--in-scope", default="The smallest behavior that satisfies the current request.")
    parser.add_argument("--out-of-scope", default="Follow-up enhancements not required for this increment.")
    parser.add_argument("--risk", default="No material risk identified yet.")
    parser.add_argument("--output", type=Path, help="Optional output path. Prints to stdout when omitted.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    content = build_card(args)
    if args.output:
        args.output.write_text(content, encoding="utf-8")
    else:
        print(content, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
