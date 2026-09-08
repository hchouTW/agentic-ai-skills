"""Behavioral tests for the agile-development helper scripts.

Run from the skill directory with python3 -m unittest discover -s tests -v.
Standard library only; no external services or dependencies are needed.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import create_story_card  # noqa: E402
import validate_agile_notes  # noqa: E402


def _story_args(**overrides) -> argparse.Namespace:
    defaults = dict(
        actor="user",
        capability="export a CSV",
        outcome="download active users",
        criteria=None,
        validation=None,
        assumption="No material assumptions identified yet.",
        in_scope="The smallest behavior that satisfies the current request.",
        out_of_scope="Follow-up enhancements not required for this increment.",
        risk="No material risk identified yet.",
        output=None,
    )
    defaults.update(overrides)
    return argparse.Namespace(**defaults)


class CreateStoryCardTests(unittest.TestCase):
    def test_default_criteria_and_validation_used_when_omitted(self):
        card = create_story_card.build_card(_story_args())
        self.assertIn("Given the primary context", card)
        self.assertIn("Run the focused test or check", card)

    def test_supplied_criteria_and_validation_replace_defaults(self):
        args = _story_args(criteria=["Given X, when Y, then Z"], validation=["Run test_foo"])
        card = create_story_card.build_card(args)
        self.assertIn("Given X, when Y, then Z", card)
        self.assertIn("Run test_foo", card)
        self.assertNotIn("Given the primary context", card)

    def test_story_line_interpolates_actor_capability_outcome(self):
        card = create_story_card.build_card(_story_args())
        self.assertIn("As a user, I want export a CSV, so that download active users.", card)

    def test_cli_end_to_end(self):
        result = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts/create_story_card.py"),
                "--actor", "user",
                "--capability", "export a CSV",
                "--outcome", "download active users",
            ],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("# Story Card", result.stdout)

    def test_cli_missing_required_flag_fails_with_usage(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts/create_story_card.py"), "--actor", "user"],
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("usage:", result.stderr)


class ValidateAgileNotesTests(unittest.TestCase):
    def test_normalize_heading_strips_hashes_and_lowercases(self):
        self.assertEqual(validate_agile_notes.normalize_heading("## Acceptance Criteria"), "acceptance criteria")
        self.assertEqual(validate_agile_notes.normalize_heading("# Story"), "story")
        self.assertIsNone(validate_agile_notes.normalize_heading("not a heading"))

    def test_check_file_reports_missing_sections(self, tmp_text="# Story\n\nAs a user...\n"):
        tmp_path = ROOT / "tests" / "_scratch_note.md"
        tmp_path.write_text(tmp_text, encoding="utf-8")
        try:
            headings, missing = validate_agile_notes.check_file(
                tmp_path, ["story", "acceptance criteria", "validation", "risks"]
            )
            self.assertEqual(headings, ["story"])
            self.assertEqual(missing, ["acceptance criteria", "validation", "risks"])
        finally:
            tmp_path.unlink()

    def test_check_file_passes_with_all_sections_present(self):
        tmp_path = ROOT / "tests" / "_scratch_note.md"
        tmp_path.write_text(
            "# Story\n\n## Acceptance Criteria\n\n## Validation\n\n## Risks\n", encoding="utf-8"
        )
        try:
            _, missing = validate_agile_notes.check_file(
                tmp_path, ["story", "acceptance criteria", "validation", "risks"]
            )
            self.assertEqual(missing, [])
        finally:
            tmp_path.unlink()

    def test_cli_ok_on_shipped_template(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts/validate_agile_notes.py"), str(ROOT / "assets/story-card.md")],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn(": ok", result.stdout)

    def test_cli_missing_file_fails_cleanly_not_with_traceback(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts/validate_agile_notes.py"), str(ROOT / "tests/does-not-exist.md")],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("file not found", result.stdout)
        self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
