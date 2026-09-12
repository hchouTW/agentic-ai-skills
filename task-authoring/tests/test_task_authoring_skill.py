"""Tests for the task-authoring bundle validator and its template-section check.

Run from the skill directory with python3 -m unittest discover -s tests -v.
Standard library only.
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import validate_skill_bundle  # noqa: E402


class ExtractHeadingsTests(unittest.TestCase):
    def test_extracts_all_three_levels_in_order(self):
        text = "# Title\n\nSome text.\n\n## Section One\n\n### Sub Section\n\n## Section Two\n"
        self.assertEqual(
            validate_skill_bundle.extract_headings(text),
            ["# Title", "## Section One", "### Sub Section", "## Section Two"],
        )

    def test_ignores_non_heading_hash_usage(self):
        text = "Not a heading: #hashtag\n\n## Real Heading\n"
        self.assertEqual(validate_skill_bundle.extract_headings(text), ["## Real Heading"])


class CheckTemplateSectionsTests(unittest.TestCase):
    def _valid_template_text(self) -> str:
        lines = ["# {{Task Title}}", ""]
        for section in validate_skill_bundle.REQUIRED_TEMPLATE_SECTIONS:
            lines.append(section)
            lines.append("<!-- placeholder -->")
            lines.append("")
        return "\n".join(lines)

    def test_shipped_template_has_no_problems(self):
        text = (ROOT / "templates/task-template.md").read_text(encoding="utf-8")
        self.assertEqual(validate_skill_bundle.check_template_sections(text), [])

    def test_synthetic_valid_template_has_no_problems(self):
        self.assertEqual(
            validate_skill_bundle.check_template_sections(self._valid_template_text()), []
        )

    def test_missing_section_is_reported(self):
        text = self._valid_template_text().replace("## Open Questions\n", "")
        problems = validate_skill_bundle.check_template_sections(text)
        self.assertTrue(any("missing sections" in p for p in problems))
        self.assertTrue(any("Open Questions" in p for p in problems))

    def test_extra_section_is_reported(self):
        text = self._valid_template_text() + "\n## Unexpected Extra Section\n"
        problems = validate_skill_bundle.check_template_sections(text)
        self.assertTrue(any("unexpected extra sections" in p for p in problems))

    def test_out_of_order_sections_are_reported(self):
        lines = ["# {{Task Title}}", "", "## Objective", "## Background"]
        for section in validate_skill_bundle.REQUIRED_TEMPLATE_SECTIONS[2:]:
            lines.append(section)
        problems = validate_skill_bundle.check_template_sections("\n".join(lines))
        self.assertTrue(any("out of order" in p for p in problems))

    def test_missing_top_level_title_is_reported(self):
        text = "\n".join(validate_skill_bundle.REQUIRED_TEMPLATE_SECTIONS)
        problems = validate_skill_bundle.check_template_sections(text)
        self.assertTrue(any("top-level title" in p for p in problems))

    def test_two_top_level_titles_is_reported(self):
        text = "# First Title\n# Second Title\n" + "\n".join(
            validate_skill_bundle.REQUIRED_TEMPLATE_SECTIONS
        )
        problems = validate_skill_bundle.check_template_sections(text)
        self.assertTrue(any("top-level title" in p for p in problems))


class ValidateSkillBundleCliTests(unittest.TestCase):
    def test_cli_succeeds_on_the_shipped_bundle(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts/validate_skill_bundle.py")],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        self.assertIn("Bundle OK", result.stdout)

    def test_cli_reports_missing_readme_section(self):
        # Run the validator against a scratch copy with a doctored README to confirm
        # it actually catches a broken section header rather than always passing.
        with tempfile.TemporaryDirectory() as tmp:
            scratch = Path(tmp) / "task-authoring"
            for rel_dir in ("scripts", "tests", "agents", "templates", "references/adapters", "examples"):
                (scratch / rel_dir).mkdir(parents=True)

            for rel in validate_skill_bundle.REQUIRED_PATHS:
                if rel in ("SKILL.md", "README.md", "templates/task-template.md"):
                    continue
                (scratch / rel).write_text("# placeholder\n")

            (scratch / "SKILL.md").write_text(
                "---\nname: task-authoring\ndescription: x\n---\n# Task Authoring\n"
            )
            (scratch / "templates/task-template.md").write_text(
                CheckTemplateSectionsTests()._valid_template_text()
            )
            # README is missing every required section on purpose.
            (scratch / "README.md").write_text("# Task Authoring\n\nNo sections here.\n")

            # The validator resolves paths relative to its own location, not cwd, so
            # point it at a copy of itself placed inside the scratch bundle.
            (scratch / "scripts/validate_skill_bundle.py").write_text(
                (ROOT / "scripts/validate_skill_bundle.py").read_text(encoding="utf-8")
            )
            result = subprocess.run(
                [sys.executable, str(scratch / "scripts/validate_skill_bundle.py")],
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 1)
            self.assertIn("README.md is missing sections", result.stdout)

    def test_cli_reports_broken_template_section_contract(self):
        with tempfile.TemporaryDirectory() as tmp:
            scratch = Path(tmp) / "task-authoring"
            for rel_dir in ("scripts", "tests", "agents", "templates", "references/adapters", "examples"):
                (scratch / rel_dir).mkdir(parents=True)

            for rel in validate_skill_bundle.REQUIRED_PATHS:
                if rel in ("SKILL.md", "README.md", "templates/task-template.md"):
                    continue
                (scratch / rel).write_text("# placeholder\n")

            (scratch / "SKILL.md").write_text(
                "---\nname: task-authoring\ndescription: x\n---\n# Task Authoring\n"
            )
            (scratch / "README.md").write_text(
                "# Task Authoring\n\n"
                + "\n\n".join(validate_skill_bundle.REQUIRED_README_SECTIONS)
                + "\n"
            )
            # Template is missing the "## Validation" section on purpose.
            broken = CheckTemplateSectionsTests()._valid_template_text().replace(
                "## Validation\n<!-- placeholder -->\n\n", ""
            )
            (scratch / "templates/task-template.md").write_text(broken)

            (scratch / "scripts/validate_skill_bundle.py").write_text(
                (ROOT / "scripts/validate_skill_bundle.py").read_text(encoding="utf-8")
            )
            result = subprocess.run(
                [sys.executable, str(scratch / "scripts/validate_skill_bundle.py")],
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 1)
            self.assertIn("section contract violated", result.stdout)
            self.assertIn("Validation", result.stdout)


if __name__ == "__main__":
    unittest.main()
