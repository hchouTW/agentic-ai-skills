"""Unit tests for scripts/validate_skill_bundle.py.

Run with:
    python3 -m unittest discover -s tests -v

from within the paper-writing/ skill folder.
"""
from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SKILL_ROOT / "scripts"))

import validate_skill_bundle as vsb  # noqa: E402


class TestRealBundle(unittest.TestCase):
    """The actual shipped skill bundle should pass its own validator cleanly."""

    def test_real_bundle_has_no_errors(self):
        errors = vsb.validate(SKILL_ROOT)
        self.assertEqual(errors, [], f"validator found issues in the real bundle: {errors}")


class TestSyntheticBundles(unittest.TestCase):
    def setUp(self):
        self.tmpdir = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmpdir, ignore_errors=True)

    def _write(self, rel_path: str, content: str) -> Path:
        p = self.tmpdir / rel_path
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        return p

    def test_missing_skill_md(self):
        errors = vsb.validate(self.tmpdir)
        self.assertTrue(any("SKILL.md not found" in e for e in errors))

    def test_missing_frontmatter(self):
        self._write("SKILL.md", "# Not a frontmatter file\n\nJust prose.\n")
        errors = vsb.validate(self.tmpdir)
        self.assertTrue(any("frontmatter" in e for e in errors))

    def test_name_mismatch(self):
        bundle = self.tmpdir / "my-skill"
        bundle.mkdir()
        (bundle / "SKILL.md").write_text(
            "---\nname: wrong-name\ndescription: A description long enough to pass the length check.\n---\n\nBody.\n",
            encoding="utf-8",
        )
        errors = vsb.validate(bundle)
        self.assertTrue(any("does not match folder name" in e for e in errors))

    def test_valid_minimal_bundle(self):
        bundle = self.tmpdir / "sample-skill"
        bundle.mkdir()
        (bundle / "SKILL.md").write_text(
            "---\n"
            "name: sample-skill\n"
            "description: A description long enough to pass the length check for this test.\n"
            "---\n\n"
            "# Sample Skill\n\n"
            "See `references/notes.md` and `scripts/helper.py`.\n",
            encoding="utf-8",
        )
        (bundle / "references").mkdir()
        (bundle / "references" / "notes.md").write_text("notes", encoding="utf-8")
        (bundle / "scripts").mkdir()
        (bundle / "scripts" / "helper.py").write_text("x = 1\n", encoding="utf-8")

        errors = vsb.validate(bundle)
        self.assertEqual(errors, [])

    def test_orphaned_file_detected(self):
        bundle = self.tmpdir / "sample-skill"
        bundle.mkdir()
        (bundle / "SKILL.md").write_text(
            "---\nname: sample-skill\ndescription: A description long enough to pass the length check.\n---\n\nBody.\n",
            encoding="utf-8",
        )
        (bundle / "references").mkdir()
        (bundle / "references" / "orphan.md").write_text("nobody points to me", encoding="utf-8")

        errors = vsb.validate(bundle)
        self.assertTrue(any("orphan.md" in e and "not referenced" in e for e in errors))

    def test_bad_python_syntax_detected(self):
        bundle = self.tmpdir / "sample-skill"
        bundle.mkdir()
        (bundle / "SKILL.md").write_text(
            "---\nname: sample-skill\ndescription: A description long enough to pass the length check.\n---\n\n"
            "See `scripts/broken.py`.\n",
            encoding="utf-8",
        )
        (bundle / "scripts").mkdir()
        (bundle / "scripts" / "broken.py").write_text("def f(:\n    pass\n", encoding="utf-8")

        errors = vsb.validate(bundle)
        self.assertTrue(any("syntax error" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
