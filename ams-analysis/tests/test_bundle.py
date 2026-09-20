"""Tests for scripts/validate_skill_bundle.py: the shipped bundle passes, and each
induced structural defect is caught. Run from the skill directory with
`python3 -m unittest discover -s tests -v`. Standard library only."""
import json
import shutil
import subprocess
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

    def test_missing_script_detected(self):
        tmp = self.stage()
        (tmp / "scripts/validate_response.py").unlink()
        self.assertTrue(any("validate_response" in e for e in vsb.check(tmp)))

    def test_missing_ledger_file_detected(self):
        tmp = self.stage()
        (tmp / "data/claims.json").unlink()
        self.assertTrue(any("claims.json" in e for e in vsb.check(tmp)))

    def test_ledger_defect_detected(self):
        tmp = self.stage()
        path = tmp / "data/claims.json"
        claims = json.loads(path.read_text(encoding="utf-8"))
        claims[0]["source_ids"] = ["S99"]
        path.write_text(json.dumps(claims), encoding="utf-8")
        self.assertTrue(any("claim.broken_source" in e for e in vsb.check(tmp)))

    def test_invalid_ledger_json_detected(self):
        tmp = self.stage()
        (tmp / "data/sources.json").write_text("{broken", encoding="utf-8")
        self.assertTrue(any("not valid JSON" in e for e in vsb.check(tmp)))

    def test_source_index_drift_detected(self):
        tmp = self.stage()
        index = tmp / "references/source-index.md"
        index.write_text(index.read_text(encoding="utf-8").replace("| S06 |", "| S06 | drift", 1), encoding="utf-8")
        self.assertTrue(any("out of sync" in e for e in vsb.check(tmp)))

    def test_unknown_claim_id_detected(self):
        tmp = self.stage()
        ref = tmp / "references/nuclei-and-isotopes.md"
        ref.write_text(ref.read_text(encoding="utf-8") + "\nSee C99.\n", encoding="utf-8")
        self.assertTrue(any("C99" in e for e in vsb.check(tmp)))

    def test_new_reference_without_read_condition_detected(self):
        tmp = self.stage()
        skill = tmp / "SKILL.md"
        text = skill.read_text(encoding="utf-8")
        row = [l for l in text.splitlines() if l.startswith("| [time-dependent-analysis]")][0]
        skill.write_text(text.replace(row, "| [time-dependent-analysis](references/time-dependent-analysis.md) | x |"), encoding="utf-8")
        self.assertTrue(any("read condition" in e and "time-dependent-analysis" in e for e in vsb.check(tmp)))

    def test_skill_must_stay_a_concise_router(self):
        tmp = self.stage()
        skill = tmp / "SKILL.md"
        skill.write_text(skill.read_text(encoding="utf-8") + "\nextra line\n" * (vsb.MAX_SKILL_LINES + 1), encoding="utf-8")
        self.assertTrue(any("concise router" in e for e in vsb.check(tmp)))

    def test_script_without_documented_exit_codes_detected(self):
        tmp = self.stage()
        script = tmp / "scripts/audit_analysis_spec.py"
        script.write_text(script.read_text(encoding="utf-8").replace("Exit code", "Return values"), encoding="utf-8")
        self.assertTrue(any("exit codes" in e and "audit_analysis_spec" in e for e in vsb.check(tmp)))

    def test_every_script_has_help_and_a_test_module(self):
        for script, test_module in vsb.SCRIPT_TESTS.items():
            self.assertTrue((ROOT / "tests" / f"{test_module}.py").exists(), script)

    def test_every_cli_prints_help_and_exits_zero(self):
        for script in vsb.SCRIPT_TESTS:
            if script == "validate_skill_bundle":
                continue
            done = subprocess.run([sys.executable, str(ROOT / "scripts" / f"{script}.py"), "--help"],
                                  capture_output=True, text=True, check=False)
            self.assertEqual(done.returncode, 0, f"{script}: {done.stderr}")
            self.assertIn("usage:", done.stdout, script)


if __name__ == "__main__":
    unittest.main()
