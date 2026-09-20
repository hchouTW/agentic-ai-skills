#!/usr/bin/env python3
"""Check the diagram sources embedded in this skill's markdown files.

Purpose: keep the DOT/Mermaid snippets in references/, templates/, and examples/ from rotting.

What it does: extracts fenced ```dot and ```mermaid blocks from markdown files.
- dot: compiled with Graphviz `dot -Tsvg` when `dot` is on PATH (skipped with a notice otherwise).
- mermaid: rendered with Mermaid CLI (`mmdc`) when it is on PATH; otherwise only a cheap
  structural lint (known diagram keyword on the first line, balanced brackets/parentheses/
  braces/quotes outside of quoted labels) - NOT a real Mermaid parse.
LaTeX/TikZ blocks are never compiled here.

Usage: `python3 scripts/check_diagram_sources.py [path ...]` (default: the whole bundle).
Exit status 1 if any checked block fails. Standard library only.
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

FENCE_RE = re.compile(r"```(dot|mermaid)\n(.*?)```", re.S)
MERMAID_STARTS = (
    "flowchart", "graph", "sequenceDiagram", "stateDiagram", "stateDiagram-v2",
    "erDiagram", "classDiagram", "gantt", "journey", "mindmap", "timeline",
)
OPEN, CLOSE = "([{", ")]}"


def extract_blocks(text: str) -> list[tuple[str, str]]:
    """Return (language, source) pairs for every dot/mermaid fence in text."""
    return [(m.group(1), m.group(2)) for m in FENCE_RE.finditer(text)]


def lint_mermaid(source: str) -> list[str]:
    """Return lint problems for a Mermaid source (empty list if it looks sane)."""
    lines = [ln for ln in source.splitlines() if ln.strip() and not ln.strip().startswith("%%")]
    if not lines:
        return ["empty Mermaid block"]
    if not lines[0].strip().startswith(MERMAID_STARTS):
        return [f"unknown diagram type on first line: {lines[0].strip()!r}"]
    if lines[0].strip().startswith("erDiagram"):
        return []  # crow's-foot tokens (|o--o{) are deliberately unbalanced
    problems = []
    for n, line in enumerate(lines, 1):
        stripped = re.sub(r'"[^"]*"', '""', line)
        stripped = re.sub(r"--?\)", "", stripped)  # sequence async arrows -) and --)
        if stripped.count('"') % 2:
            problems.append(f"line {n}: unbalanced quote")
        stack = []
        for ch in stripped:
            if ch in OPEN:
                stack.append(ch)
            elif ch in CLOSE:
                if not stack or OPEN.index(stack.pop()) != CLOSE.index(ch):
                    problems.append(f"line {n}: mismatched {ch!r}")
                    break
        else:
            if stack and not any(w in line for w in ("subgraph",)):
                problems.append(f"line {n}: unclosed bracket")
    return problems


def check_dot(source: str) -> str | None:
    """Return an error string if `dot` rejects the source, else None."""
    result = subprocess.run(
        ["dot", "-Tsvg", "-o", "/dev/null"], input=source, text=True, capture_output=True
    )
    return result.stderr.strip() or "dot failed" if result.returncode else None


def check_mermaid(source: str, mmdc: str = "mmdc") -> str | None:
    """Return an error string if Mermaid CLI cannot render the source, else None."""
    with tempfile.TemporaryDirectory() as tmp:
        src, out = Path(tmp) / "in.mmd", Path(tmp) / "out.svg"
        src.write_text(source, encoding="utf-8")
        result = subprocess.run(
            [mmdc, "-q", "-i", str(src), "-o", str(out)], text=True, capture_output=True
        )
        if result.returncode or not out.exists():
            return (result.stderr.strip() or result.stdout.strip() or "mmdc failed")[:500]
    return None


def main(argv: list[str]) -> int:
    root = Path(__file__).resolve().parents[1]
    paths = [Path(a) for a in argv] or sorted(root.rglob("*.md"))
    have_dot = shutil.which("dot") is not None
    if not have_dot:
        print("note: Graphviz `dot` not found; skipping DOT compilation")
    mmdc = shutil.which("mmdc")
    if not mmdc:
        print("note: Mermaid CLI `mmdc` not found; Mermaid blocks get the structural lint only")
    failures = checked = 0
    for path in paths:
        for lang, source in extract_blocks(path.read_text(encoding="utf-8")):
            checked += 1
            if lang == "dot":
                error = check_dot(source) if have_dot else None
                problems = [error] if error else []
            else:
                problems = lint_mermaid(source)
                if mmdc and not problems:
                    error = check_mermaid(source, mmdc)
                    problems = [error] if error else []
            for problem in problems:
                failures += 1
                print(f"{path}: {lang}: {problem}")
    print(f"Checked {checked} block(s); {failures} problem(s).")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
