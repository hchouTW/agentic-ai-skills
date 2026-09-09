"""Unit tests for scripts/check_manuscript.py.

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

import check_manuscript as cm  # noqa: E402


class TestCheckManuscript(unittest.TestCase):
    def setUp(self):
        self.tmpdir = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmpdir, ignore_errors=True)

    def _write(self, rel_path: str, content: str) -> Path:
        p = self.tmpdir / rel_path
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        return p

    def test_clean_manuscript_has_no_issues(self):
        self._write(
            "paper.tex",
            r"""
            \section{Introduction}
            As shown in Fig.~\ref{fig:mass}, the result agrees with theory~\cite{Aad:2012tfa}.
            \label{sec:intro}
            """,
        )
        self._write(
            "figs.tex",
            r"""
            \begin{figure}
            \label{fig:mass}
            \end{figure}
            """,
        )
        self._write("refs.bib", "@article{Aad:2012tfa,\n  title={Observation of a new particle},\n}\n")

        results = cm.scan(self.tmpdir)
        self.assertEqual(results["missing_bib"], {})
        self.assertEqual(results["duplicate_labels"], {})
        self.assertEqual(results["undefined_refs"], {})
        self.assertEqual(results["todos"], [])
        self.assertEqual(results["unused_bib"], [])

    def test_missing_bib_entry_detected(self):
        self._write("paper.tex", r"\cite{DoesNotExist}")
        self._write("refs.bib", "@article{SomeOtherKey,\n  title={x},\n}\n")

        results = cm.scan(self.tmpdir)
        self.assertIn("DoesNotExist", results["missing_bib"])

    def test_unused_bib_entry_detected(self):
        self._write("paper.tex", r"\cite{UsedKey}")
        self._write(
            "refs.bib",
            "@article{UsedKey,\n  title={x},\n}\n@article{UnusedKey,\n  title={y},\n}\n",
        )

        results = cm.scan(self.tmpdir)
        self.assertIn("UnusedKey", results["unused_bib"])
        self.assertNotIn("UsedKey", results["unused_bib"])

    def test_duplicate_label_detected(self):
        self._write(
            "paper.tex",
            "\\label{fig:same}\nsome text\n\\label{fig:same}\n",
        )

        results = cm.scan(self.tmpdir)
        self.assertIn("fig:same", results["duplicate_labels"])
        self.assertEqual(len(results["duplicate_labels"]["fig:same"]), 2)

    def test_undefined_ref_detected(self):
        self._write("paper.tex", r"See Fig.~\ref{fig:missing} for details.")

        results = cm.scan(self.tmpdir)
        self.assertIn("fig:missing", results["undefined_refs"])

    def test_todo_marker_detected(self):
        self._write("paper.tex", "The efficiency is TODO: fill in from the fit.\n")

        results = cm.scan(self.tmpdir)
        self.assertEqual(len(results["todos"]), 1)

    def test_value_needed_marker_detected(self):
        self._write("paper.tex", "The mass is [VALUE NEEDED: fit result] GeV.\n")

        results = cm.scan(self.tmpdir)
        self.assertEqual(len(results["todos"]), 1)

    def test_placeholder_text_detected(self):
        self._write("paper.tex", "Results: ??? need to fill in once fit converges.\n")

        results = cm.scan(self.tmpdir)
        self.assertEqual(len(results["placeholders"]), 1)

    def test_report_exit_code_zero_when_clean(self):
        self._write("paper.tex", r"\cite{K}\label{a}")
        self._write("refs.bib", "@article{K,\n  title={x},\n}\n")
        results = cm.scan(self.tmpdir)
        code = cm.report(results, strict=False)
        self.assertEqual(code, 0)

    def test_report_exit_code_nonzero_when_issues(self):
        self._write("paper.tex", r"\cite{Missing}")
        self._write("refs.bib", "@article{Other,\n  title={x},\n}\n")
        results = cm.scan(self.tmpdir)
        code = cm.report(results, strict=False)
        self.assertEqual(code, 1)


if __name__ == "__main__":
    unittest.main()
