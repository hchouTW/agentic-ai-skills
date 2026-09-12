---
role: test-driven Staff Prompt Engineer
skill: skill-router
archetype: test-first
target: Bundle validator must reject a SKILL.md whose full frontmatter block exceeds the 1024-character plugin spec limit
---

## 1. Acceptance Invariants & Boundary Constraints

`scripts/validate_skill_bundle.py`'s CLI must exit non-zero with the
message `SKILL.md frontmatter exceeds 1024 characters` when the YAML
frontmatter block (the text between the two `---` delimiters) is longer
than 1024 characters - the same limit this repository has already hit once
in practice (an earlier `description:` field had to be manually trimmed to
fit a real plugin-loader spec limit). The bundle validator currently has no
automated check for this at all, so a future edit that regrows a
`description:` field past the limit would pass `validate_skill_bundle.py`
locally and only fail later, at plugin-load time, somewhere harder to
diagnose.

- A frontmatter block at or under 1024 characters: CLI exits 0 (unchanged).
- A frontmatter block over 1024 characters: CLI exits 1 and names the exact
  limit in the message - the boundary this test targets, currently
  unenforced.

## 2. Executable Failing Test (Red)

```python
# tests/test_bundle_validator_frontmatter_length.py
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_EXAMPLES = [
    "01-adding-a-routing-rule-without-overlap", "02-multi-skill-primary-secondary-routing",
    "03-negative-carve-out-not-a-match", "04-decision-tree-multi-skill-ambiguous-routing",
    "05-trajectory-single-clean-match-academic-papers", "06-trajectory-generic-verb-vs-domain-specific-rule",
    "07-trajectory-clean-no-match-proceed-normally", "08-gated-pipeline-adding-a-new-rule",
    "09-gated-pipeline-disambiguating-figure-interpretation", "10-gated-pipeline-expanding-a-carve-out",
    "11-decision-tree-figure-interpretation-routing", "12-decision-tree-multiple-false-positive-keywords",
    "13-adversarial-audit-new-routing-rule-proposal", "14-test-first-routing-parser-primary-secondary",
]


def _write_minimal_bundle(scratch: Path, skill_md_text: str) -> None:
    for rel in ("scripts", "tests", "agents", "examples"):
        (scratch / rel).mkdir(parents=True)
    (scratch / "scripts/validate_skill_bundle.py").write_text(
        (ROOT / "scripts/validate_skill_bundle.py").read_text(encoding="utf-8")
    )
    (scratch / "tests/test_skill_router.py").write_text("# placeholder\n")
    (scratch / "agents/openai.yaml").write_text("interface:\n  display_name: x\n")
    (scratch / "VALIDATION.md").write_text("# placeholder\n")
    (scratch / "README.md").write_text(
        "## Installation and invocation\n## Quick checks\n"
        "## Coverage and boundaries\n## Example prompts\n"
    )
    (scratch / "examples/README.md").write_text("# placeholder\n")
    for name in REQUIRED_EXAMPLES:
        (scratch / f"examples/{name}.md").write_text("# placeholder\n")
    (scratch / "SKILL.md").write_text(skill_md_text)


def test_rejects_frontmatter_over_1024_characters():
    with tempfile.TemporaryDirectory() as tmp:
        scratch = Path(tmp) / "skill-router"
        scratch.mkdir()
        oversized_description = "x" * 1100
        skill_md = f"---\nname: skill-router\ndescription: {oversized_description}\n---\n# Skill Router\n"
        _write_minimal_bundle(scratch, skill_md)

        result = subprocess.run(
            [sys.executable, str(scratch / "scripts/validate_skill_bundle.py")],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 1, f"expected exit 1, got {result.returncode}"
        assert "SKILL.md frontmatter exceeds 1024 characters" in result.stdout, (
            f"expected the length-limit message, got: {result.stdout!r}"
        )
```

```
$ python3 -m pytest tests/test_bundle_validator_frontmatter_length.py -v
tests/test_bundle_validator_frontmatter_length.py::test_rejects_frontmatter_over_1024_characters FAILED

================================== FAILURES ==================================
______ test_rejects_frontmatter_over_1024_characters ______
AssertionError: expected exit 1, got 0
assert 0 == 1
1 failed in 0.06s
```

Current `main()` (pre-fix) checks that `name:`/`description:` are present
but never checks the frontmatter block's overall length:

```python
# scripts/validate_skill_bundle.py (pre-fix excerpt)
frontmatter = skill.split("---", 2)[1]
for field in ("name:", "description:"):
    if field not in frontmatter:
        print(f"SKILL.md frontmatter is missing {field}")
        raise SystemExit(1)
```

## 3. Minimal Code Implementation

```python
# scripts/validate_skill_bundle.py (fixed excerpt)
FRONTMATTER_CHAR_LIMIT = 1024

frontmatter = skill.split("---", 2)[1]
for field in ("name:", "description:"):
    if field not in frontmatter:
        print(f"SKILL.md frontmatter is missing {field}")
        raise SystemExit(1)
if len(frontmatter) > FRONTMATTER_CHAR_LIMIT:
    print(f"SKILL.md frontmatter exceeds {FRONTMATTER_CHAR_LIMIT} characters")
    raise SystemExit(1)
```

## 4. Verified Passing Execution (Green)

```
$ python3 -m pytest tests/test_bundle_validator_frontmatter_length.py -v
tests/test_bundle_validator_frontmatter_length.py::test_rejects_frontmatter_over_1024_characters PASSED
1 passed in 0.06s
```

```
$ python3 scripts/validate_skill_bundle.py
Bundle OK: 31 files present and non-empty, 5 routing entries found (academic-papers, agile-development, deep-learning, hep-analysis, task-authoring).
```

Full regression suite (this test plus the 2 existing `ValidateSkillBundleCliTests`
cases: shipped bundle succeeds, missing README section reported) - 3 cases -
passes in 0.24s, and the real, shipped `SKILL.md`'s current frontmatter
length stays comfortably under the 1024-character limit this check now
enforces.

## 5. Regression Guard Summary

This test guards against a repeat of the exact incident that motivated the
1024-character limit in the first place: a `description:` field grown past
a real plugin-loader spec limit, discovered only after the fact rather than
by a local check. Any future edit that regrows the description without
re-trimming it will now fail `validate_skill_bundle.py` locally, before it
ever reaches a plugin loader that enforces the same limit less legibly.
