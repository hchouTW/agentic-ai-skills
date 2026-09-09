#!/usr/bin/env python3
"""
validate_skill_bundle.py -- integrity checker for the paper-writing skill bundle
itself (not for the user's manuscript -- see check_manuscript.py for that).

Checks:
  1. SKILL.md exists and has YAML frontmatter with non-empty `name` and
     `description` fields.
  2. The frontmatter `name` matches the containing folder's name.
  3. Every relative path referenced in backticks in SKILL.md that looks like
     it belongs to this bundle (references/..., scripts/..., assets/...)
     actually exists on disk.
  4. Every file under references/, scripts/, and assets/ is mentioned
     somewhere in SKILL.md (catches orphaned files nobody points to).
  5. Every .py file under scripts/ parses as valid Python (syntax check only;
     does not execute anything).

Standard library only. Exit code 0 on success, 1 if any check fails.

Usage:
    python3 scripts/validate_skill_bundle.py [path-to-skill-folder]

If no path is given, assumes it is being run from within the skill folder
(i.e. this script's grandparent directory).
"""
from __future__ import annotations

import ast
import re
import sys
from pathlib import Path

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
FIELD_RE = re.compile(r"^(\w[\w-]*):\s*(.*)$", re.MULTILINE)
BACKTICK_PATH_RE = re.compile(r"`((?:references|scripts|assets)/[^`\s]+)`")


def find_skill_root(explicit: Path | None) -> Path:
    if explicit is not None:
        return explicit
    # this file lives at <skill_root>/scripts/validate_skill_bundle.py
    return Path(__file__).resolve().parent.parent


def check_frontmatter(skill_md: Path, skill_root: Path, errors: list[str]) -> None:
    if not skill_md.is_file():
        errors.append(f"SKILL.md not found at {skill_md}")
        return

    text = skill_md.read_text(encoding="utf-8", errors="replace")
    m = FRONTMATTER_RE.match(text)
    if not m:
        errors.append("SKILL.md does not start with a --- ... --- YAML frontmatter block")
        return

    fields = dict(FIELD_RE.findall(m.group(1)))
    name = fields.get("name", "").strip()
    description = fields.get("description", "").strip()

    if not name:
        errors.append("frontmatter `name` field is missing or empty")
    elif name != skill_root.name:
        errors.append(f"frontmatter name '{name}' does not match folder name '{skill_root.name}'")

    if not description:
        errors.append("frontmatter `description` field is missing or empty")
    elif len(description) < 20:
        errors.append("frontmatter `description` looks too short to describe when to trigger this skill")

    return text


def check_referenced_paths_exist(skill_md_text: str, skill_root: Path, errors: list[str]) -> set[str]:
    referenced = set(BACKTICK_PATH_RE.findall(skill_md_text))
    for rel in sorted(referenced):
        if not (skill_root / rel).exists():
            errors.append(f"SKILL.md references '{rel}' but it does not exist on disk")
    return referenced


def check_no_orphaned_files(skill_root: Path, referenced: set[str], errors: list[str]) -> None:
    for subdir in ("references", "scripts", "assets"):
        d = skill_root / subdir
        if not d.is_dir():
            continue
        for f in sorted(d.rglob("*")):
            if f.is_dir():
                continue
            if "__pycache__" in f.parts or f.suffix == ".pyc":
                continue
            rel = f.relative_to(skill_root).as_posix()
            # allow this validator and the test suite to be unreferenced
            if f.name in ("validate_skill_bundle.py",):
                continue
            if rel not in referenced and not any(rel.startswith(r.rstrip("/") + "/") for r in referenced):
                errors.append(f"'{rel}' exists but is not referenced anywhere in SKILL.md")


def check_python_syntax(skill_root: Path, errors: list[str]) -> None:
    scripts_dir = skill_root / "scripts"
    if not scripts_dir.is_dir():
        return
    for f in sorted(scripts_dir.glob("*.py")):
        source = f.read_text(encoding="utf-8", errors="replace")
        try:
            ast.parse(source, filename=str(f))
        except SyntaxError as e:
            errors.append(f"{f.relative_to(skill_root)}: syntax error: {e}")


def validate(skill_root: Path) -> list[str]:
    errors: list[str] = []
    skill_md = skill_root / "SKILL.md"
    text = check_frontmatter(skill_md, skill_root, errors)
    if text:
        referenced = check_referenced_paths_exist(text, skill_root, errors)
        check_no_orphaned_files(skill_root, referenced, errors)
    check_python_syntax(skill_root, errors)
    return errors


def main(argv=None) -> int:
    path_arg = Path(argv[0]).resolve() if argv else None
    skill_root = find_skill_root(path_arg)

    if not skill_root.is_dir():
        print(f"error: {skill_root} is not a directory", file=sys.stderr)
        return 2

    errors = validate(skill_root)

    if errors:
        print(f"FAILED: {len(errors)} issue(s) in {skill_root}")
        for e in errors:
            print(f"  - {e}")
        return 1

    print(f"OK: {skill_root} passed all checks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
