"""Tests for scripts/validate_skill_bundle.py: the shipped bundle passes, and each
induced structural defect is caught. Run from the skill directory with
`python3 -m unittest discover -s tests -v`. Standard library only."""
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import validate_skill_bundle as vsb  # noqa: E402


class BundleTests(unittest.TestCase):
    def stage(self):
        tmp = Path(tempfile.mkdtemp()) / "ams-analysis"
        shutil.copytree(ROOT, tmp, ignore=shutil.ignore_patterns("__pycache__"))
        self.addCleanup(shutil.rmtree, tmp.parent, ignore_errors=True)
        return tmp

    def test_shipped_bundle_is_clean(self):
        self.assertEqual(vsb.check(ROOT), [])

    def test_missing_reference_detected(self):
        tmp = self.stage()
        (tmp / "references/source-policy.md").unlink()
        self.assertTrue(any("source-policy" in e for e in vsb.check(tmp)))

    def test_orphaned_reference_detected(self):
        tmp = self.stage()
        (tmp / "references/extra.md").write_text("# extra\n", encoding="utf-8")
        self.assertTrue(any("orphaned" in e for e in vsb.check(tmp)))

    def test_broken_link_detected(self):
        tmp = self.stage()
        skill = tmp / "SKILL.md"
        skill.write_text(skill.read_text(encoding="utf-8") + "\n[x](references/nope.md)\n",
                         encoding="utf-8")
        self.assertTrue(any("broken link" in e for e in vsb.check(tmp)))

    def test_placeholder_detected(self):
        tmp = self.stage()
        ref = tmp / "references/charged-cosmic-rays.md"
        ref.write_text(ref.read_text(encoding="utf-8") + "\nTODO fill in\n", encoding="utf-8")
        self.assertTrue(any("placeholder" in e for e in vsb.check(tmp)))

    def test_unknown_source_id_detected(self):
        tmp = self.stage()
        ref = tmp / "references/nuclei-and-isotopes.md"
        ref.write_text(ref.read_text(encoding="utf-8") + "\nSee S99.\n", encoding="utf-8")
        self.assertTrue(any("S99" in e for e in vsb.check(tmp)))

    def test_name_drift_detected(self):
        tmp = self.stage()
        skill = tmp / "SKILL.md"
        skill.write_text(skill.read_text(encoding="utf-8").replace("name: ams-analysis", "name: ams", 1),
                         encoding="utf-8")
        self.assertTrue(any("name" in e for e in vsb.check(tmp)))


if __name__ == "__main__":
    unittest.main()
