#!/usr/bin/env python3
"""
check_manuscript.py -- read-only pre-submission checker for a LaTeX manuscript.

Scans a directory of .tex and .bib files and reports, without modifying
anything:
  - \\cite{...} keys that do not resolve to any entry in a .bib file
  - .bib entries that are never cited by any \\cite{...} in the .tex files
  - \\label{...} keys defined more than once
  - \\ref{...} / \\eqref{...} / \\autoref{...} targets with no matching \\label{}
  - leftover TODO / FIXME / XXX / placeholder markers

Standard library only. Intended to be run near the end of a drafting session,
not after every edit.

Usage:
    python3 check_manuscript.py <path-to-manuscript-dir> [--strict]

Exit code is 0 if no issues are found, 1 otherwise (useful in CI / pre-commit
hooks). --strict also treats "unused .bib entry" as an issue for exit-code
purposes (by default it is reported but does not affect the exit code, since
a shared/collaboration .bib file legitimately contains more entries than any
single paper cites).
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

CITE_RE = re.compile(r"\\(?:cite|citep|citet|citealt|citealp)\*?(?:\[[^\]]*\])?\{([^}]+)\}")
LABEL_RE = re.compile(r"\\label\{([^}]+)\}")
REF_RE = re.compile(r"\\(?:ref|eqref|autoref|cref|Cref)\{([^}]+)\}")
BIBENTRY_RE = re.compile(r"@\w+\{\s*([^,\s]+)\s*,")
TODO_RE = re.compile(r"\b(TODO|FIXME|XXX)\b|\[VALUE NEEDED[^\]]*\]|\[CITATION NEEDED[^\]]*\]", re.IGNORECASE)
PLACEHOLDER_RE = re.compile(r"lorem ipsum|\?\?\?|\[FIGURE HERE\]|\[TABLE HERE\]", re.IGNORECASE)


def split_keys(raw: str):
    return [k.strip() for k in raw.split(",") if k.strip()]


def find_tex_and_bib(root: Path):
    tex_files = sorted(root.rglob("*.tex"))
    bib_files = sorted(root.rglob("*.bib"))
    return tex_files, bib_files


def scan(root: Path):
    tex_files, bib_files = find_tex_and_bib(root)

    cite_keys = defaultdict(list)   # key -> [(file, line)]
    label_defs = defaultdict(list)  # label -> [(file, line)]
    ref_targets = defaultdict(list)  # label -> [(file, line)]
    todos = []      # (file, line, text)
    placeholders = []  # (file, line, text)

    for tex in tex_files:
        text = tex.read_text(encoding="utf-8", errors="replace")
        for lineno, line in enumerate(text.splitlines(), start=1):
            for m in CITE_RE.finditer(line):
                for key in split_keys(m.group(1)):
                    cite_keys[key].append((tex, lineno))
            for m in LABEL_RE.finditer(line):
                label_defs[m.group(1)].append((tex, lineno))
            for m in REF_RE.finditer(line):
                ref_targets[m.group(1)].append((tex, lineno))
            if TODO_RE.search(line):
                todos.append((tex, lineno, line.strip()))
            if PLACEHOLDER_RE.search(line):
                placeholders.append((tex, lineno, line.strip()))

    bib_entries = set()
    for bib in bib_files:
        text = bib.read_text(encoding="utf-8", errors="replace")
        for m in BIBENTRY_RE.finditer(text):
            bib_entries.add(m.group(1))

    missing_bib = {k: v for k, v in cite_keys.items() if bib_files and k not in bib_entries}
    unused_bib = sorted(bib_entries - set(cite_keys.keys())) if bib_files else []
    duplicate_labels = {k: v for k, v in label_defs.items() if len(v) > 1}
    undefined_refs = {k: v for k, v in ref_targets.items() if k not in label_defs}

    return {
        "tex_files": tex_files,
        "bib_files": bib_files,
        "missing_bib": missing_bib,
        "unused_bib": unused_bib,
        "duplicate_labels": duplicate_labels,
        "undefined_refs": undefined_refs,
        "todos": todos,
        "placeholders": placeholders,
    }


def fmt_locs(locs):
    return "; ".join(f"{f.name}:{ln}" for f, ln in locs[:5]) + (" ..." if len(locs) > 5 else "")


def report(results, strict: bool) -> int:
    n_tex = len(results["tex_files"])
    n_bib = len(results["bib_files"])
    print(f"Scanned {n_tex} .tex file(s) and {n_bib} .bib file(s).\n")

    issues = 0

    if results["missing_bib"]:
        issues += len(results["missing_bib"])
        print(f"[MISSING BIB ENTRY] {len(results['missing_bib'])} cite key(s) not found in any .bib file:")
        for key, locs in sorted(results["missing_bib"].items()):
            print(f"  - {key}  ({fmt_locs(locs)})")
        print()

    if results["duplicate_labels"]:
        issues += len(results["duplicate_labels"])
        print(f"[DUPLICATE LABEL] {len(results['duplicate_labels'])} label(s) defined more than once:")
        for key, locs in sorted(results["duplicate_labels"].items()):
            print(f"  - {key}  ({fmt_locs(locs)})")
        print()

    if results["undefined_refs"]:
        issues += len(results["undefined_refs"])
        print(f"[UNDEFINED REF] {len(results['undefined_refs'])} \\ref/\\eqref target(s) with no matching \\label:")
        for key, locs in sorted(results["undefined_refs"].items()):
            print(f"  - {key}  ({fmt_locs(locs)})")
        print()

    if results["todos"]:
        issues += len(results["todos"])
        print(f"[TODO / PLACEHOLDER MARKER] {len(results['todos'])} found:")
        for f, ln, line in results["todos"][:20]:
            print(f"  - {f.name}:{ln}: {line}")
        if len(results["todos"]) > 20:
            print(f"  ... and {len(results['todos']) - 20} more")
        print()

    if results["placeholders"]:
        issues += len(results["placeholders"])
        print(f"[PLACEHOLDER TEXT] {len(results['placeholders'])} found:")
        for f, ln, line in results["placeholders"][:20]:
            print(f"  - {f.name}:{ln}: {line}")
        print()

    if results["unused_bib"]:
        print(f"[INFO] {len(results['unused_bib'])} .bib entr{'y is' if len(results['unused_bib']) == 1 else 'ies are'} never cited "
              f"(harmless in a shared library, worth checking in a single-paper .bib):")
        for key in results["unused_bib"][:20]:
            print(f"  - {key}")
        if len(results["unused_bib"]) > 20:
            print(f"  ... and {len(results['unused_bib']) - 20} more")
        if strict:
            issues += len(results["unused_bib"])
        print()

    if issues == 0:
        print("No issues found.")
    else:
        print(f"Total issues: {issues}")

    return 1 if issues > 0 else 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("path", type=Path, help="Directory containing the manuscript's .tex/.bib files")
    parser.add_argument("--strict", action="store_true", help="Treat unused .bib entries as issues for exit code purposes")
    args = parser.parse_args(argv)

    if not args.path.is_dir():
        print(f"error: {args.path} is not a directory", file=sys.stderr)
        return 2

    results = scan(args.path)
    return report(results, strict=args.strict)


if __name__ == "__main__":
    raise SystemExit(main())
