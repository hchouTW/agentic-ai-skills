"""Tests for the skill-router bundle validator and its routing-table parsing.

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


class ExtractRoutedSkillNamesTests(unittest.TestCase):
    def test_extracts_names_from_real_skill_md(self):
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        names = validate_skill_bundle.extract_routed_skill_names(text)
        self.assertEqual(names, ["agile-development", "deep-learning", "hep-analysis"])

    def test_extracts_names_from_synthetic_routing_table(self):
        text = (
            "## Routing rules\n\n"
            "- **foo-skill** - does foo things.\n"
            "- **bar-skill** - does bar things, not baz.\n"
        )
        self.assertEqual(validate_skill_bundle.extract_routed_skill_names(text), ["foo-skill", "bar-skill"])

    def test_ignores_bold_text_outside_bullet_position(self):
        text = "Some **bold-word** in prose, not a routing bullet.\n"
        self.assertEqual(validate_skill_bundle.extract_routed_skill_names(text), [])


class FindSiblingSkillDirsTests(unittest.TestCase):
    def test_finds_sibling_with_skill_md_and_excludes_self(self):
        with tempfile.TemporaryDirectory() as tmp:
            parent = Path(tmp)
            this_skill = parent / "skill-router"
            this_skill.mkdir()
            sibling_a = parent / "agile-development"
            sibling_a.mkdir()
            (sibling_a / "SKILL.md").write_text("---\nname: agile-development\n---\n")
            not_a_skill = parent / "not-a-skill"
            not_a_skill.mkdir()  # no SKILL.md inside

            found = validate_skill_bundle.find_sibling_skill_dirs(this_skill)
            self.assertEqual(found, {"agile-development"})

    def test_empty_when_no_siblings_look_like_skills(self):
        with tempfile.TemporaryDirectory() as tmp:
            parent = Path(tmp)
            this_skill = parent / "skill-router"
            this_skill.mkdir()
            (parent / "just-a-folder").mkdir()

            self.assertEqual(validate_skill_bundle.find_sibling_skill_dirs(this_skill), set())


class ValidateSkillBundleCliTests(unittest.TestCase):
    def test_cli_succeeds_on_the_shipped_bundle(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts/validate_skill_bundle.py")],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("Bundle OK", result.stdout)

    def test_cli_reports_missing_readme_section(self):
        # Run the validator against a scratch copy with a doctored README to confirm
        # it actually catches a broken section header rather than always passing.
        with tempfile.TemporaryDirectory() as tmp:
            scratch = Path(tmp) / "skill-router"
            scratch.mkdir()
            (scratch / "scripts").mkdir()
            (scratch / "tests").mkdir()
            (scratch / "agents").mkdir()
            for rel in ("scripts/validate_skill_bundle.py", "tests/test_skill_router.py"):
                (scratch / rel).write_text("# placeholder\n")
            (scratch / "agents/openai.yaml").write_text("interface:\n  display_name: x\n")
            (scratch / "VALIDATION.md").write_text("# placeholder\n")
            (scratch / "SKILL.md").write_text("---\nname: skill-router\ndescription: x\n---\n# Skill Router\n")
            # README is missing every required section on purpose.
            (scratch / "README.md").write_text("# Skill Router\n\nNo sections here.\n")

            # The validator resolves paths relative to its own location, not cwd, so
            # point it at a copy of itself placed inside the scratch bundle.
            (scratch / "scripts" / "validate_skill_bundle.py").write_text(
                (ROOT / "scripts/validate_skill_bundle.py").read_text(encoding="utf-8")
            )
            result = subprocess.run(
                [sys.executable, str(scratch / "scripts/validate_skill_bundle.py")],
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 1)
            self.assertIn("README.md is missing sections", result.stdout)


if __name__ == "__main__":
    unittest.main()
