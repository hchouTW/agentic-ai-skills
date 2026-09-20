#!/usr/bin/env python3
"""Validate the ams-analysis skill bundle's structure and cross-file consistency.

Purpose: catch structural regressions (missing/empty files, broken links, orphaned
or unindexed references, scaffold placeholders, name drift) that would silently
degrade the skill's progressive disclosure.

What it does: checks required files exist and are non-empty; SKILL.md frontmatter has
name == folder name == the agents/openai.yaml reference, and SKILL.md stays a concise
router (line limit); every reference is linked from SKILL.md with a read condition and
no reference is orphaned; every relative markdown link (and anchor) resolves; every
reference has the mandatory sections; every source ID (Snn) and claim ID (Cnn) cited in
a reference exists in data/sources.json and data/claims.json; the JSON ledger passes
scripts/validate_evidence_ledger.py and references/source-index.md is in sync with it
(scripts/render_source_index.py); every script documents usage and exit codes and has a
test module; the test suite in tests-and-examples.md has at least 20 tests; no scaffold
placeholders remain.

Usage: `python3 scripts/validate_skill_bundle.py` (paths resolve relative to this
file). Standard library only. Exit code 1 on any failure.
"""
from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import render_source_index  # noqa: E402
import validate_evidence_ledger  # noqa: E402

REFERENCES = [
    "detector-and-observables",
    "reconstruction-and-data-quality",
    "charged-cosmic-rays",
    "antimatter-and-leptons",
    "nuclei-and-isotopes",
    "efficiency-acceptance-backgrounds",
    "inference-and-unfolding",
    "calibration-mc-systematics",
    "source-policy",
    "source-index",
    "tests-and-examples",
    "analysis-artifacts",
    "time-dependent-analysis",
    "statistical-diagnostics",
]
SCRIPT_TESTS = {  # script -> the test module that must exist for it
    "ams_kinematics": "test_kinematics",
    "validate_covariance": "test_covariance",
    "validate_response": "test_response",
    "validate_evidence_ledger": "test_evidence_ledger",
    "render_source_index": "test_evidence_ledger",
    "audit_analysis_spec": "test_analysis_spec",
    "poisson_diagnostics": "test_poisson",
    "validate_skill_bundle": "test_bundle",
}
MAX_SKILL_LINES = 120
REQUIRED_PATHS = (
    ["SKILL.md", "README.md", "VALIDATION.md", "agents/openai.yaml", "data/sources.json", "data/claims.json",
     "tests/fixtures/spec_valid.json", "tests/fixtures/cov_valid.json", "tests/fixtures/response_valid.json"]
    + [f"scripts/{name}.py" for name in SCRIPT_TESTS]
    + [f"tests/{name}.py" for name in sorted(set(SCRIPT_TESTS.values()))]
    + [f"references/{name}.md" for name in REFERENCES]
)
REQUIRED_REFERENCE_SECTIONS = [
    "## When to read this file",
    "## Contents",
    "## Failure modes",
    "## Required source classes",
    "## Questions to ask the user",
]
PLACEHOLDER = re.compile(r"\b(TODO|TBD|FIXME|XXX|lorem ipsum|\[insert)\b", re.I)
LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")


def slug(heading: str) -> str:
    """GitHub-style anchor for a heading line."""
    text = re.sub(r"[`*]", "", heading.lstrip("#").strip()).lower()
    text = re.sub(r"[^\w\s-]", "", text)
    return re.sub(r"\s", "-", text)


def anchors(path: Path) -> set[str]:
    return {slug(line) for line in path.read_text(encoding="utf-8").splitlines()
            if line.startswith("#")}


def frontmatter_field(text: str, field: str) -> str | None:
    match = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not match:
        return None
    for line in match.group(1).splitlines():
        if line.startswith(f"{field}:"):
            return line.split(":", 1)[1].strip()
    return None


def check(root: Path) -> list[str]:
    errors: list[str] = []
    for rel in REQUIRED_PATHS:
        path = root / rel
        if not path.exists():
            errors.append(f"missing file: {rel}")
        elif path.stat().st_size == 0:
            errors.append(f"empty file: {rel}")
    if errors:
        return errors

    skill = (root / "SKILL.md").read_text(encoding="utf-8")
    if frontmatter_field(skill, "name") != root.name == "ams-analysis":
        errors.append("SKILL.md name must equal 'ams-analysis' and the folder name")
    if not frontmatter_field(skill, "description"):
        errors.append("SKILL.md frontmatter lacks a description")
    if "ams-analysis" not in (root / "agents/openai.yaml").read_text(encoding="utf-8"):
        errors.append("agents/openai.yaml does not reference ams-analysis")

    if len(skill.splitlines()) > MAX_SKILL_LINES:
        errors.append(f"SKILL.md has {len(skill.splitlines())} lines; it must stay a concise router (limit {MAX_SKILL_LINES})")
    linked = set(re.findall(r"\(references/([\w-]+)\.md\)", skill))
    for name in REFERENCES:
        row = re.search(rf"^\| \[{re.escape(name)}\]\(references/{re.escape(name)}\.md\) \| (.+?) \|$", skill, re.M)
        if not row or len(row.group(1).split()) < 3:
            errors.append(f"SKILL.md reference index lacks a read condition for: {name}")
    for name in REFERENCES:
        if name not in linked:
            errors.append(f"SKILL.md does not link reference: {name}")
    for path in (root / "references").glob("*.md"):
        if path.stem not in REFERENCES:
            errors.append(f"orphaned reference not in manifest: {path.name}")

    markdown = [root / "SKILL.md", root / "README.md", root / "VALIDATION.md"] + [
        root / f"references/{name}.md" for name in REFERENCES]
    for path in markdown:
        text = path.read_text(encoding="utf-8")
        if PLACEHOLDER.search(text):
            errors.append(f"placeholder text in {path.relative_to(root)}")
        for target in LINK.findall(text):
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            file_part, _, anchor = target.partition("#")
            dest = (path.parent / file_part).resolve() if file_part else path
            if not dest.exists():
                errors.append(f"{path.relative_to(root)}: broken link {target}")
            elif anchor and dest.suffix == ".md" and anchor not in anchors(dest):
                errors.append(f"{path.relative_to(root)}: missing anchor {target}")

    index_text = (root / "references/source-index.md").read_text(encoding="utf-8")
    try:
        sources = json.loads((root / "data/sources.json").read_text(encoding="utf-8"))
        claims = json.loads((root / "data/claims.json").read_text(encoding="utf-8"))
    except ValueError as exc:
        return errors + [f"data ledger is not valid JSON: {exc}"]
    ledger = validate_evidence_ledger.check_ledger(sources, claims, today=date(9999, 12, 31))
    for finding in ledger["errors"]:
        errors.append(f"ledger {finding['code']} at {finding['where']}: {finding['message']}")
    in_sync, detail = render_source_index.check_index(index_text, sources, claims)
    if not in_sync:
        errors.append("references/source-index.md is out of sync with data/*.json (run scripts/render_source_index.py --write): "
                      + detail.splitlines()[0][:120])
    known_ids = {s["id"] for s in sources if isinstance(s, dict)}
    known_claims = {c["id"] for c in claims if isinstance(c, dict)}
    for name in REFERENCES:
        text = (root / f"references/{name}.md").read_text(encoding="utf-8")
        if name != "source-index":
            for section in REQUIRED_REFERENCE_SECTIONS:
                if section not in text:
                    errors.append(f"references/{name}.md lacks '{section}'")
        if name in ("source-index", "tests-and-examples"):
            continue
        for sid in set(re.findall(r"\bS\d\d\b", text)):
            if sid not in known_ids:
                errors.append(f"references/{name}.md cites unknown source {sid}")
        for cid in set(re.findall(r"\bC\d\d\b", text)):
            if cid not in known_claims:
                errors.append(f"references/{name}.md cites unknown claim {cid}")

    for script in SCRIPT_TESTS:
        text = (root / f"scripts/{script}.py").read_text(encoding="utf-8")
        doc = re.match(r'#![^\n]*\n"""(.*?)"""', text, re.S)
        body = doc.group(1) if doc else ""
        for needle in ("Purpose", "Usage", "Standard library"):
            if needle not in body:
                errors.append(f"scripts/{script}.py docstring lacks '{needle}'")
        if script != "validate_skill_bundle" and "Exit code" not in body:
            errors.append(f"scripts/{script}.py docstring lacks its exit codes")
        if script != "validate_skill_bundle" and 'if __name__ == "__main__"' not in text:
            errors.append(f"scripts/{script}.py has no command-line entry point")

    tests = (root / "references/tests-and-examples.md").read_text(encoding="utf-8")
    if len(re.findall(r"^- test_id: T\d+", tests, re.M)) < 20:
        errors.append("tests-and-examples.md has fewer than 20 tests")
    return errors


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    errors = check(root)
    if errors:
        print("Bundle FAILED:")
        for error in errors:
            print(f"  {error}")
        raise SystemExit(1)
    print(f"Bundle OK: {len(REQUIRED_PATHS)} required files present, links and anchors resolve.")


if __name__ == "__main__":
    main()
