#!/usr/bin/env python3
"""Check markdown notes for common Agile delivery sections."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


DEFAULT_SECTIONS = [
    "story",
    "acceptance criteria",
    "validation",
    "risks",
]


def normalize_heading(line: str) -> str | None:
    match = re.match(r"^\s{0,3}#{1,6}\s+(.+?)\s*$", line)
    if not match:
        return None
    heading = match.group(1).strip().lower()
    return re.sub(r"\s+", " ", heading)


def check_file(path: Path, required: list[str]) -> tuple[list[str], list[str]]:
    text = path.read_text(encoding="utf-8")
    headings = {heading for line in text.splitlines() if (heading := normalize_heading(line))}
    missing = [section for section in required if section.lower() not in headings]
    return sorted(headings), missing


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate common sections in Agile markdown notes.")
    parser.add_argument("file", type=Path, help="Markdown file to inspect.")
    parser.add_argument(
        "--require",
        action="append",
        dest="required",
        help="Required heading. Repeat to override defaults.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    required = [item.lower() for item in (args.required or DEFAULT_SECTIONS)]
    try:
        headings, missing = check_file(args.file, required)
    except FileNotFoundError:
        print(f"{args.file}: file not found")
        return 2
    except OSError as exc:
        print(f"{args.file}: could not read file ({exc})")
        return 2

    if missing:
        print(f"{args.file}: missing required headings: {', '.join(missing)}")
        print(f"found headings: {', '.join(headings) if headings else '(none)'}")
        return 1

    print(f"{args.file}: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
