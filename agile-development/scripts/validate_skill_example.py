#!/usr/bin/env python3
"""Validate a filled-in canonical `<skill>/examples/*.md` file.

Purpose: mechanically reject structural defects and placeholder content in a
worked example (Weak vs. Expert contrast) before it ships - mirrors
`validate_agile_notes.py`'s role for delivery notes. See
references/example-authoring.md for the format this checks against.

What it does: checks that role/skill/use_case frontmatter fields are present and
non-empty, that the four required sections (Scenario, Common Weak Approach,
Expert-Level Best Practice, Key Takeaways) are present in that order, that Key
Takeaways has between 3 and 6 bullet items, and that no placeholder markers
(TODO/TBD/XXX/FIXME, Lorem ipsum, bracketed stand-ins, leftover scaffold
comments, standalone ellipsis lines) remain anywhere in the file. It cannot judge
domain correctness - that is a review step, not something this script does.

Usage: `python3 scripts/validate_skill_example.py <file.md>`. Exits 0 and prints
"<file>: ok" on success; exits 1 with a description of every problem found;
exits 2 with a one-line message (no traceback) if the file cannot be read.
Standard library only.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

REQUIRED_SECTIONS = [
    "Scenario",
    "Common Weak Approach",
    "Expert-Level Best Practice",
    "Key Takeaways",
]
FRONTMATTER_FIELDS = ["role", "skill", "use_case"]
MIN_TAKEAWAYS = 3
MAX_TAKEAWAYS = 6

SECTION_HEADING_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
BULLET_RE = re.compile(r"^- \S")

PLACEHOLDER_PATTERNS = [
    (re.compile(r"\b(TODO|TBD|FIXME|XXX)\b"), "placeholder marker"),
    (re.compile(r"lorem ipsum", re.IGNORECASE), "Lorem ipsum filler text"),
    (re.compile(r"\[(?:your|insert|placeholder|todo|xxx|tbd)\b[^\]]*\]", re.IGNORECASE),
     "bracketed stand-in"),
    (re.compile(r"<!--.*?-->", re.DOTALL), "leftover scaffold comment"),
]
ELLIPSIS_LINE_RE = re.compile(r"^\s*\.\.\.\s*$", re.MULTILINE)


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    """Returns (fields, body). Fields is empty if there is no --- block."""
    if not text.startswith("---\n"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    fields = {}
    for line in parts[1].splitlines():
        line = line.strip()
        if not line or ":" not in line:
            continue
        key, _, value = line.partition(":")
        fields[key.strip()] = value.strip()
    return fields, parts[2]


def check_frontmatter(fields: dict[str, str]) -> list[str]:
    problems = []
    if not fields:
        problems.append("missing frontmatter block (expected a leading '---' section "
                         "with role/skill/use_case)")
        return problems
    for field in FRONTMATTER_FIELDS:
        if not fields.get(field):
            problems.append(f"frontmatter is missing a non-empty '{field}' field")
    return problems


def check_sections(body: str) -> list[str]:
    headings = SECTION_HEADING_RE.findall(body)
    missing = [s for s in REQUIRED_SECTIONS if s not in headings]
    if missing:
        return [f"missing required section(s): {', '.join(missing)}"]

    positions = [headings.index(s) for s in REQUIRED_SECTIONS]
    if positions != sorted(positions):
        return [f"required sections are present but out of order: found {headings}, "
                f"expected order {REQUIRED_SECTIONS}"]
    return []


def section_text(body: str, name: str) -> str:
    matches = list(SECTION_HEADING_RE.finditer(body))
    for i, match in enumerate(matches):
        if match.group(1) != name:
            continue
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(body)
        return body[start:end]
    return ""


def check_takeaway_count(body: str) -> list[str]:
    takeaways_text = section_text(body, "Key Takeaways")
    count = sum(1 for line in takeaways_text.splitlines() if BULLET_RE.match(line))
    if not MIN_TAKEAWAYS <= count <= MAX_TAKEAWAYS:
        return [f"Key Takeaways has {count} bullet item(s), expected "
                f"{MIN_TAKEAWAYS}-{MAX_TAKEAWAYS}"]
    return []


def check_placeholders(text: str) -> list[str]:
    problems = []
    for pattern, label in PLACEHOLDER_PATTERNS:
        match = pattern.search(text)
        if match:
            snippet = match.group(0).strip().replace("\n", " ")
            if len(snippet) > 60:
                snippet = snippet[:57] + "..."
            problems.append(f"found {label}: {snippet!r}")
    if ELLIPSIS_LINE_RE.search(text):
        problems.append("found a standalone '...' line where real content belongs")
    return problems


def validate(text: str) -> list[str]:
    fields, body = parse_frontmatter(text)
    problems = check_frontmatter(fields)
    problems += check_sections(body)
    if not problems:
        problems += check_takeaway_count(body)
    problems += check_placeholders(text)
    return problems


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate a filled-in canonical skill example.")
    parser.add_argument("file", type=Path, help="Markdown example file to check.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        text = args.file.read_text(encoding="utf-8")
    except FileNotFoundError:
        print(f"{args.file}: file not found")
        return 2
    except OSError as exc:
        print(f"{args.file}: could not read file ({exc})")
        return 2

    problems = validate(text)
    if problems:
        print(f"{args.file}: {len(problems)} problem(s) found:")
        for problem in problems:
            print(f"  {problem}")
        return 1

    print(f"{args.file}: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
