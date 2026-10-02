"""Tests for the task-authoring bundle validator and its template-section check.

Run from the skill directory with python3 -m unittest discover -s tests -v.
Standard library only.
"""
from __future__ import annotations

import re
import shutil
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




class DescriptionLengthTests(unittest.TestCase):
    def _description(self, skill_md: Path) -> str:
        frontmatter = skill_md.read_text(encoding="utf-8").split("---", 2)[1]
        return re.search(r'^description:\s*"?(.*?)"?\s*$', frontmatter, re.MULTILINE).group(1)

    def test_shipped_description_is_within_the_limit(self):
        self.assertLessEqual(
            len(self._description(ROOT / "SKILL.md")), validate_skill_bundle.DESCRIPTION_LIMIT
        )

    def test_validator_flags_an_overlong_description(self):
        with tempfile.TemporaryDirectory() as tmp:
            scratch = Path(tmp) / "task-authoring"
            shutil.copytree(ROOT, scratch, ignore=shutil.ignore_patterns("__pycache__"))
            skill = scratch / "SKILL.md"
            skill.write_text(
                skill.read_text(encoding="utf-8").replace('description: "', 'description: "' + "x" * 200, 1),
                encoding="utf-8",
            )
            result = subprocess.run(
                [sys.executable, str(scratch / "scripts/validate_skill_bundle.py")],
                capture_output=True,
                text=True,
            )
        self.assertEqual(result.returncode, 1)
        self.assertIn("limit is 1024", result.stdout)


class ShippedExamplesTests(unittest.TestCase):
    def test_every_example_task_follows_the_section_contract(self):
        examples = sorted((ROOT / "examples").glob("*-task.md"))
        self.assertTrue(examples, "no example task files found")
        for path in examples:
            with self.subTest(example=path.name):
                problems = validate_skill_bundle.check_template_sections(
                    path.read_text(encoding="utf-8")
                )
                self.assertEqual(problems, [])


class BundleErrorPathTests(unittest.TestCase):
    """Missing and empty required files, bad frontmatter: exit code 1 and a message naming the problem."""

    def _run_on_scratch(self, mutate):
        with tempfile.TemporaryDirectory() as tmp:
            scratch = Path(tmp) / "task-authoring"
            shutil.copytree(ROOT, scratch, ignore=shutil.ignore_patterns("__pycache__"))
            mutate(scratch)
            return subprocess.run(
                [sys.executable, str(scratch / "scripts/validate_skill_bundle.py")],
                capture_output=True,
                text=True,
            )

    def test_missing_required_file_is_listed(self):
        result = self._run_on_scratch(lambda s: (s / "references/acceptance-criteria.md").unlink())
        self.assertEqual(result.returncode, 1)
        self.assertIn("missing files:", result.stdout)
        self.assertIn("references/acceptance-criteria.md", result.stdout)

    def test_empty_required_file_is_listed(self):
        result = self._run_on_scratch(lambda s: (s / "references/task-quality-checklist.md").write_text(""))
        self.assertEqual(result.returncode, 1)
        self.assertIn("empty files:", result.stdout)
        self.assertIn("references/task-quality-checklist.md", result.stdout)

    def test_missing_frontmatter_is_reported(self):
        def mutate(s):
            skill = s / "SKILL.md"
            skill.write_text(skill.read_text(encoding="utf-8").split("---\n", 2)[2], encoding="utf-8")

        result = self._run_on_scratch(mutate)
        self.assertEqual(result.returncode, 1)
        self.assertIn("missing YAML frontmatter", result.stdout)

    def test_missing_frontmatter_field_is_reported(self):
        def mutate(s):
            skill = s / "SKILL.md"
            skill.write_text(skill.read_text(encoding="utf-8").replace("name:", "nom:", 1), encoding="utf-8")

        result = self._run_on_scratch(mutate)
        self.assertEqual(result.returncode, 1)
        self.assertIn("frontmatter is missing name:", result.stdout)


if __name__ == "__main__":
    unittest.main()
