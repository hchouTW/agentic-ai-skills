"""Behavioral tests for the example-authoring helper scripts.

Purpose: cover `generate_skill_example.py` (scaffold) and
`validate_skill_example.py` (structural + placeholder checks) - the tooling
behind references/example-authoring.md.

Usage: run from the skill directory with
`python3 -m unittest discover -s tests -v`. Standard library only; no external
services or dependencies are needed.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import generate_skill_example  # noqa: E402
import validate_skill_example  # noqa: E402


GOOD_EXAMPLE = """---
role: Staff Software Engineer
skill: agile-development
use_case: scoping a discount-code bug fix
---

## Scenario

A customer reports the cart total is wrong when a discount code is applied
alongside a shipping promotion. The team must scope and fix the bug.

## Common Weak Approach

```python
def apply_discount(total, code):
    return total * 0.9
```

This ignores stacking rules entirely.

## Expert-Level Best Practice

```python
def apply_discount(total, code, promotions):
    for promo in promotions:
        total = promo.apply(total)
    return total
```

This composes promotions explicitly and is covered by a regression test.

## Key Takeaways

- Reproduce the bug with a failing test before writing a fix.
- Model discount stacking as an explicit, ordered list rather than a single multiplier.
- Add a regression test that encodes the specific reported combination.
"""


def _scaffold_args(**overrides) -> argparse.Namespace:
    defaults = dict(
        skill="agile-development",
        role="Staff Software Engineer",
        use_case="scoping a bug fix",
        takeaways=4,
        output=None,
    )
    defaults.update(overrides)
    return argparse.Namespace(**defaults)


class GenerateSkillExampleTests(unittest.TestCase):
    def test_skeleton_has_frontmatter_and_all_sections_in_order(self):
        skeleton = generate_skill_example.build_skeleton(_scaffold_args())
        self.assertIn("role: Staff Software Engineer", skeleton)
        self.assertIn("skill: agile-development", skeleton)
        self.assertIn("use_case: scoping a bug fix", skeleton)
        sections = ["## Scenario", "## Common Weak Approach",
                    "## Expert-Level Best Practice", "## Key Takeaways"]
        positions = [skeleton.index(s) for s in sections]
        self.assertEqual(positions, sorted(positions))

    def test_takeaway_count_matches_requested_number(self):
        skeleton = generate_skill_example.build_skeleton(_scaffold_args(takeaways=6))
        self.assertEqual(skeleton.count("<!-- Takeaway"), 6)

    def test_cli_rejects_takeaways_out_of_range(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts/generate_skill_example.py"),
             "--skill", "agile-development", "--role", "X", "--use-case", "Y",
             "--takeaways", "10"],
            capture_output=True, text=True,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("--takeaways must be between", result.stderr)

    def test_cli_missing_required_flag_fails_with_usage(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts/generate_skill_example.py"), "--skill", "x"],
            capture_output=True, text=True,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("usage:", result.stderr)

    def test_cli_writes_to_output_path(self):
        out_path = ROOT / "tests" / "_scratch_scaffold.md"
        try:
            result = subprocess.run(
                [sys.executable, str(ROOT / "scripts/generate_skill_example.py"),
                 "--skill", "agile-development", "--role", "X", "--use-case", "Y",
                 "--output", str(out_path)],
                capture_output=True, text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(out_path.exists())
            self.assertIn("## Scenario", out_path.read_text(encoding="utf-8"))
        finally:
            out_path.unlink(missing_ok=True)


class ValidateSkillExampleTests(unittest.TestCase):
    def test_valid_example_passes(self):
        self.assertEqual(validate_skill_example.validate(GOOD_EXAMPLE), [])

    def test_missing_frontmatter_field_is_reported(self):
        broken = GOOD_EXAMPLE.replace("skill: agile-development\n", "")
        problems = validate_skill_example.validate(broken)
        self.assertTrue(any("skill" in p for p in problems))

    def test_missing_frontmatter_block_is_reported(self):
        no_frontmatter = GOOD_EXAMPLE.split("---\n", 2)[-1]
        problems = validate_skill_example.validate(no_frontmatter)
        self.assertTrue(any("missing frontmatter" in p for p in problems))

    def test_missing_section_is_reported(self):
        broken = GOOD_EXAMPLE.replace("## Key Takeaways", "## Something Else")
        problems = validate_skill_example.validate(broken)
        self.assertTrue(any("Key Takeaways" in p for p in problems))

    def test_out_of_order_sections_are_reported(self):
        scenario = "## Scenario\n\nSome scenario text.\n\n"
        weak = "## Common Weak Approach\n\nweak\n\n"
        expert = "## Expert-Level Best Practice\n\nexpert\n\n"
        takeaways = "## Key Takeaways\n\n- a\n- b\n- c\n"
        frontmatter = "---\nrole: X\nskill: agile-development\nuse_case: Y\n---\n\n"
        reordered = frontmatter + weak + scenario + expert + takeaways
        problems = validate_skill_example.validate(reordered)
        self.assertTrue(any("out of order" in p for p in problems))

    def test_too_few_takeaways_is_reported(self):
        broken = GOOD_EXAMPLE.replace(
            "- Add a regression test that encodes the specific reported combination.\n", "")
        problems = validate_skill_example.validate(broken)
        self.assertTrue(any("Key Takeaways has 2 bullet item(s)" in p for p in problems))

    def test_too_many_takeaways_is_reported(self):
        extra = GOOD_EXAMPLE + "- A seventh takeaway.\n- An eighth takeaway.\n- A ninth takeaway.\n- A tenth.\n"
        problems = validate_skill_example.validate(extra)
        self.assertTrue(any("bullet item(s), expected 3-6" in p for p in problems))

    def test_todo_marker_is_flagged(self):
        broken = GOOD_EXAMPLE.replace("This ignores stacking rules entirely.", "TODO: explain this")
        problems = validate_skill_example.validate(broken)
        self.assertTrue(any("placeholder marker" in p for p in problems))

    def test_lorem_ipsum_is_flagged(self):
        broken = GOOD_EXAMPLE.replace("This ignores stacking rules entirely.", "Lorem ipsum dolor sit amet.")
        problems = validate_skill_example.validate(broken)
        self.assertTrue(any("Lorem ipsum" in p for p in problems))

    def test_bracketed_stand_in_is_flagged(self):
        broken = GOOD_EXAMPLE.replace("This ignores stacking rules entirely.", "[Your explanation here]")
        problems = validate_skill_example.validate(broken)
        self.assertTrue(any("bracketed stand-in" in p for p in problems))

    def test_leftover_scaffold_comment_is_flagged(self):
        broken = GOOD_EXAMPLE + "\n<!-- fill this in -->\n"
        problems = validate_skill_example.validate(broken)
        self.assertTrue(any("leftover scaffold comment" in p for p in problems))

    def test_standalone_ellipsis_line_is_flagged(self):
        broken = GOOD_EXAMPLE.replace(
            "This composes promotions explicitly and is covered by a regression test.",
            "This composes promotions explicitly.\n\n...\n")
        problems = validate_skill_example.validate(broken)
        self.assertTrue(any("standalone '...' line" in p for p in problems))

    def test_generated_scaffold_fails_validation_until_filled_in(self):
        skeleton = generate_skill_example.build_skeleton(_scaffold_args())
        self.assertNotEqual(validate_skill_example.validate(skeleton), [])

    def test_cli_ok_on_valid_file(self):
        path = ROOT / "tests" / "_scratch_valid.md"
        path.write_text(GOOD_EXAMPLE, encoding="utf-8")
        try:
            result = subprocess.run(
                [sys.executable, str(ROOT / "scripts/validate_skill_example.py"), str(path)],
                capture_output=True, text=True,
            )
            self.assertEqual(result.returncode, 0, result.stdout)
            self.assertIn(": ok", result.stdout)
        finally:
            path.unlink(missing_ok=True)

    def test_cli_missing_file_fails_cleanly_not_with_traceback(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts/validate_skill_example.py"),
             str(ROOT / "tests/does-not-exist.md")],
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("file not found", result.stdout)
        self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
