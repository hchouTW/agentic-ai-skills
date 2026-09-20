"""Tests for scripts/validate_evidence_ledger.py and scripts/render_source_index.py.
The shipped ledger must pass; each mutation test starts from the shipped data,
introduces one controlled defect, and asserts the intended diagnostic. Also covers
migration retention (IDs, scope and limitation text survive) and index rendering.
Run from the skill directory with `python3 -m unittest discover -s tests -v`."""
import contextlib
import copy
import io
import json
import re
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import render_source_index as rsi  # noqa: E402
import validate_evidence_ledger as vel  # noqa: E402

TODAY = date(2026, 9, 20)


def ledger():
    sources, claims = vel.load_ledger(ROOT / "data" / "sources.json", ROOT / "data" / "claims.json")
    return copy.deepcopy(sources), copy.deepcopy(claims)


def find(items, item_id):
    return next(i for i in items if i["id"] == item_id)


def codes(report, kind="errors"):
    return {e["code"] for e in report[kind]}


def run(sources, claims, today=TODAY, stale_days=365):
    return vel.check_ledger(sources, claims, today, stale_days)


class ShippedLedgerTests(unittest.TestCase):
    def test_shipped_ledger_is_valid(self):
        report = run(*ledger())
        self.assertEqual(report["status"], "pass", report["errors"] + report["warnings"])
        self.assertEqual(report["counts"], {"sources": 47, "claims": 49})

    def test_migration_retains_every_id(self):
        sources, claims = ledger()
        self.assertEqual([s["id"] for s in sources], [f"S{n:02d}" for n in range(1, 48)])
        self.assertEqual(sorted(c["id"] for c in claims), [f"C{n:02d}" for n in range(1, 50)])

    def test_migration_retains_scope_and_limitation_text(self):
        _, claims = ledger()
        for c in claims:
            self.assertTrue(c["scope"]["text"], c["id"])
        self.assertIn("Supplemental cuts not read", find(claims, "C20")["limitations"])
        self.assertIn("Supplemental Material not read", find(claims, "C27")["limitations"])
        self.assertIn("Gaussian-core widths only", find(claims, "C28")["limitations"])
        self.assertIn("search-limited", find(claims, "C14")["scope"]["text"])
        self.assertIn("re-read in the paper before quoting a breakdown", find(claims, "C23")["limitations"])

    def test_migration_retains_source_qualifications(self):
        sources, _ = ledger()
        self.assertEqual(find(sources, "S10")["verification_note"], "downloaded; only its data period was read")
        self.assertEqual(find(sources, "S27")["verification_level"], "not-opened")
        self.assertIn("main article only", find(sources, "S04")["verification_note"])
        self.assertEqual(find(sources, "S26")["tier_range"], [5, 6])
        self.assertIsNone(find(sources, "S19")["access_date"])
        self.assertEqual(find(sources, "S02")["superseded_by"], ["S03"])
        self.assertEqual(find(sources, "S03")["supersedes"], ["S02"])

    def test_publication_date_and_data_period_are_separate_fields(self):
        s15 = find(ledger()[0], "S15")
        self.assertEqual(s15["publication_date"], "2026-06-17")
        self.assertEqual(s15["data_taking_period"]["end"], "2024-11-26")

    def test_every_cited_source_id_in_references_exists(self):
        sources, claims = ledger()
        known = {s["id"] for s in sources}
        for path in (ROOT / "references").glob("*.md"):
            if path.stem in ("source-index", "tests-and-examples"):
                continue
            for sid in set(re.findall(r"\bS\d\d\b", path.read_text(encoding="utf-8"))):
                self.assertIn(sid, known, f"{path.name}: {sid}")
            for cid in set(re.findall(r"\bC\d\d\b", path.read_text(encoding="utf-8"))):
                self.assertIn(cid, {c["id"] for c in claims}, f"{path.name}: {cid}")


class SourceDefectTests(unittest.TestCase):
    def test_duplicate_source_id(self):
        sources, claims = ledger()
        sources.append(copy.deepcopy(sources[0]))
        self.assertIn("source.duplicate_id", codes(run(sources, claims)))

    def test_invalid_verification_state(self):
        sources, claims = ledger()
        find(sources, "S04")["verification_level"] = "fully-verified"
        self.assertIn("source.bad_verification_level", codes(run(sources, claims)))

    def test_missing_required_field(self):
        sources, claims = ledger()
        del find(sources, "S06")["title"]
        self.assertIn("source.missing_field", codes(run(sources, claims)))

    def test_bad_tier_and_dates(self):
        sources, claims = ledger()
        find(sources, "S04")["tier"] = 9
        find(sources, "S06")["access_date"] = "20-09-2026"
        find(sources, "S08")["publication_date"] = "Sept 2016"
        report = run(sources, claims)
        self.assertTrue({"source.bad_tier", "source.bad_date"} <= codes(report))

    def test_future_access_date_and_published_after_access(self):
        sources, claims = ledger()
        find(sources, "S04")["access_date"] = "2027-01-01"
        find(sources, "S06")["year"] = 2030
        report = run(sources, claims)
        self.assertIn("source.future_access_date", codes(report))
        self.assertIn("source.published_after_access", codes(report))

    def test_read_level_without_access_date(self):
        sources, claims = ledger()
        find(sources, "S04")["access_date"] = None
        self.assertIn("source.level_without_access_date", codes(run(sources, claims)))

    def test_broken_supersession_target(self):
        sources, claims = ledger()
        find(sources, "S04")["superseded_by"] = ["S99"]
        self.assertIn("source.broken_relation", codes(run(sources, claims)))

    def test_asymmetric_supersession(self):
        sources, claims = ledger()
        find(sources, "S03")["supersedes"] = []
        self.assertIn("source.asymmetric_relation", codes(run(sources, claims)))

    def test_self_supersession(self):
        sources, claims = ledger()
        find(sources, "S06")["supersedes"] = ["S06"]
        find(sources, "S06")["superseded_by"] = ["S06"]
        self.assertIn("source.self_supersession", codes(run(sources, claims)))

    def test_supersession_cycle(self):
        sources, claims = ledger()
        for a, b in (("S04", "S05"), ("S05", "S04")):
            find(sources, a)["supersedes"].append(b)
            find(sources, b)["superseded_by"].append(a)
        self.assertIn("source.supersession_cycle", codes(run(sources, claims)))


class ClaimDefectTests(unittest.TestCase):
    def test_duplicate_claim_id(self):
        sources, claims = ledger()
        claims.append(copy.deepcopy(claims[0]))
        self.assertIn("claim.duplicate_id", codes(run(sources, claims)))

    def test_broken_source_reference(self):
        sources, claims = ledger()
        find(claims, "C20")["source_ids"] = ["S08", "S99"]
        self.assertIn("claim.broken_source", codes(run(sources, claims)))

    def test_invalid_claim_type_and_strength(self):
        sources, claims = ledger()
        find(claims, "C20")["claim_types"] = ["rumour"]
        find(claims, "C21")["verification_strength"] = "confirmed"
        report = run(sources, claims)
        self.assertTrue({"claim.bad_type", "claim.bad_verification_strength"} <= codes(report))

    def test_claim_stronger_than_its_source(self):
        sources, claims = ledger()
        find(claims, "C11")["source_ids"] = ["S20"]          # a metadata-only source
        find(claims, "C11")["verification_strength"] = "full-text"
        self.assertIn("claim.stronger_than_sources", codes(run(sources, claims)))

    def test_source_downgrade_exposes_over_strong_claims(self):
        sources, claims = ledger()
        find(sources, "S08")["verification_level"] = "metadata-only"
        report = run(sources, claims)
        flagged = {e["where"] for e in report["errors"] if e["code"] == "claim.stronger_than_sources"}
        self.assertTrue({"C20", "C22", "C23"} <= flagged, flagged)

    def test_numeric_quotation_on_metadata_only_claim(self):
        sources, claims = ledger()
        find(claims, "C16")["numeric_quotation_allowed"] = True
        self.assertIn("claim.numeric_without_reading", codes(run(sources, claims)))

    def test_ams_practice_claim_resting_on_third_party_source(self):
        sources, claims = ledger()
        c = find(claims, "C15")
        c["support_kind"] = "primary"
        self.assertIn("claim.no_primary_source", codes(run(sources, claims)))

    def test_ams_practice_claim_resting_on_tier_3_source(self):
        sources, claims = ledger()
        c = find(claims, "C14")
        c.update({"support_kind": "primary", "source_ids": ["S24"]})  # thesis/talk, tier 3
        self.assertIn("claim.no_primary_source", codes(run(sources, claims)))

    def test_missing_scope_blocks_a_claim(self):
        sources, claims = ledger()
        find(claims, "C20")["scope"] = {"text": ""}
        self.assertIn("claim.missing_scope", codes(run(sources, claims)))

    def test_bad_review_date(self):
        sources, claims = ledger()
        find(claims, "C20")["last_reviewed"] = "yesterday"
        self.assertIn("claim.bad_date", codes(run(sources, claims)))

    def test_malformed_ledger(self):
        self.assertIn("ledger.malformed", codes(vel.check_ledger({}, [], TODAY)))


class StalenessTests(unittest.TestCase):
    def test_stale_dates_are_notes_not_errors(self):
        sources, claims = ledger()
        report = run(sources, claims, today=date(2028, 1, 1))
        self.assertEqual(report["status"], "pass")
        self.assertIn("stale.source", codes(report, "notes"))
        note = next(n for n in report["notes"] if n["code"] == "stale.source")
        self.assertIn("does not mean the source is obsolete", note["message"])

    def test_fresh_ledger_has_no_stale_notes(self):
        report = run(*ledger())
        self.assertFalse({"stale.source", "stale.claim"} & codes(report, "notes"))


class RenderTests(unittest.TestCase):
    def test_shipped_index_is_in_sync(self):
        sources, claims = ledger()
        text = (ROOT / "references" / "source-index.md").read_text(encoding="utf-8")
        ok, detail = rsi.check_index(text, sources, claims)
        self.assertTrue(ok, detail)

    def test_changed_claim_is_detected(self):
        sources, claims = ledger()
        find(claims, "C31")["claim"] += " (edited)"
        text = (ROOT / "references" / "source-index.md").read_text(encoding="utf-8")
        ok, detail = rsi.check_index(text, sources, claims)
        self.assertFalse(ok)
        self.assertIn("C31", detail)

    def test_write_is_idempotent_and_repairs_drift(self):
        sources, claims = ledger()
        text = (ROOT / "references" / "source-index.md").read_text(encoding="utf-8")
        self.assertEqual(rsi.write_index(text, sources, claims), text)
        drifted = text.replace("| S06 |", "| S06 | DRIFT", 1)
        self.assertFalse(rsi.check_index(drifted, sources, claims)[0])
        self.assertTrue(rsi.check_index(rsi.write_index(drifted, sources, claims), sources, claims)[0])

    def test_prose_outside_markers_is_untouched(self):
        sources, claims = ledger()
        text = (ROOT / "references" / "source-index.md").read_text(encoding="utf-8")
        marker = "\n## Failure modes\n"
        self.assertIn(marker, text)
        rewritten = rsi.write_index(text.replace("| S06 |", "| S06 | DRIFT", 1), sources, claims)
        self.assertEqual(rewritten.split(marker)[1], text.split(marker)[1])

    def test_missing_markers_reported(self):
        sources, claims = ledger()
        ok, detail = rsi.check_index("# no tables here\n", sources, claims)
        self.assertFalse(ok)
        self.assertIn("missing GENERATED block", detail)
        with self.assertRaises(ValueError):
            rsi.write_index("# no tables here\n", sources, claims)

    def test_pipe_in_cell_is_escaped(self):
        sources, claims = ledger()
        self.assertIn("\\|Z\\|", rsi.render_tables(sources, claims)["claim-ledger"])

    def test_compress_only_long_runs(self):
        self.assertEqual(rsi._compress(["S30", "S31", "S32", "S33", "S34"]), "S30-S34")
        self.assertEqual(rsi._compress(["S08", "S04", "S05", "S06"]), "S08, S04, S05, S06")


class CliTests(unittest.TestCase):
    def cli(self, module, *argv):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(io.StringIO()):
            code = module.main(list(argv))
        return code, buf.getvalue()

    def test_validator_exit_codes(self):
        self.assertEqual(self.cli(vel, "--today", "2026-09-20")[0], 0)
        sources, claims = ledger()
        claims.append(copy.deepcopy(claims[0]))
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / "claims.json"
            bad.write_text(json.dumps(claims), encoding="utf-8")
            code, out = self.cli(vel, "--claims", str(bad), "--today", "2026-09-20")
            self.assertEqual(code, 1)
            self.assertEqual(json.loads(out)["status"], "fail")
            self.assertEqual(self.cli(vel, "--claims", str(Path(tmp) / "absent.json"))[0], 2)
        self.assertEqual(self.cli(vel, "--today", "not-a-date")[0], 2)

    def test_renderer_exit_codes(self):
        self.assertEqual(self.cli(rsi)[0], 0)
        with tempfile.TemporaryDirectory() as tmp:
            index = Path(tmp) / "index.md"
            index.write_text("# nothing\n", encoding="utf-8")
            self.assertEqual(self.cli(rsi, "--index", str(index))[0], 1)
            self.assertEqual(self.cli(rsi, "--index", str(index), "--write")[0], 2)
        self.assertEqual(self.cli(rsi, "--index", "/nonexistent/index.md")[0], 2)


if __name__ == "__main__":
    unittest.main()
