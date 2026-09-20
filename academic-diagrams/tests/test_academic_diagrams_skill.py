"""Tests for the academic-diagrams bundle validator and diagram-source checker.

Purpose: guard the helper scripts and the shipped bundle against regressions.
What it does: unit-tests the parsing/lint helpers on synthetic input and runs the validator and
source checker against the real bundle. Usage: `python3 -m unittest discover -s tests -v` from the
skill directory. Standard library only; DOT compilation is skipped when Graphviz is absent.
"""
import importlib.util
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


bundle = load("validate_skill_bundle")
sources = load("check_diagram_sources")


class FrontmatterAndLinks(unittest.TestCase):
    def test_frontmatter_parsed(self):
        fm = bundle.frontmatter_fields('---\nname: x\ndescription: "d"\n---\nbody')
        self.assertEqual(fm["name"], "x")
        self.assertEqual(fm["description"], '"d"')

    def test_frontmatter_absent(self):
        self.assertEqual(bundle.frontmatter_fields("no frontmatter"), {})

    def test_broken_link_detected(self):
        with tempfile.TemporaryDirectory() as d:
            md = Path(d) / "a.md"
            (Path(d) / "ok.md").write_text("x")
            md.write_text("[ok](ok.md) [bad](missing.md#s) [web](https://e.com/x)")
            self.assertEqual(bundle.broken_links(md), ["missing.md"])

    def test_skill_name_matches_folder(self):
        fm = bundle.frontmatter_fields((ROOT / "SKILL.md").read_text(encoding="utf-8"))
        self.assertEqual(fm["name"], ROOT.name)


class MermaidLint(unittest.TestCase):
    def test_good_flowchart(self):
        self.assertEqual(sources.lint_mermaid("flowchart LR\n A[Raw] --> B{ok?}\n"), [])

    def test_sequence_async_arrow_is_not_a_bracket(self):
        self.assertEqual(sources.lint_mermaid("sequenceDiagram\n A--)B: hi\n"), [])

    def test_unbalanced_bracket(self):
        self.assertTrue(sources.lint_mermaid("flowchart LR\n A[Raw --> B\n"))

    def test_unknown_type(self):
        self.assertTrue(sources.lint_mermaid("foo\n A --> B\n"))

    def test_er_crows_foot_allowed(self):
        self.assertEqual(sources.lint_mermaid("erDiagram\n A ||--o{ B : has\n"), [])

    def test_extract_blocks(self):
        text = "x\n```dot\ndigraph{}\n```\n```mermaid\nflowchart LR\n```\n```text\nA\n```"
        self.assertEqual([lang for lang, _ in sources.extract_blocks(text)], ["dot", "mermaid"])


@unittest.skipUnless(shutil.which("dot"), "Graphviz not installed")
class DotCompile(unittest.TestCase):
    def test_valid_dot(self):
        self.assertIsNone(sources.check_dot("digraph G { A -> B; }"))

    def test_invalid_dot(self):
        self.assertTrue(sources.check_dot("digraph G { A -> ; ;; -> }"))


class MermaidRender(unittest.TestCase):
    def fake_mmdc(self, directory, exit_code, stderr=""):
        """Write a stand-in `mmdc` that writes the -o file (or fails) so no browser is needed."""
        script = Path(directory) / "fake_mmdc"
        script.write_text(
            "#!/bin/sh\n"
            'while [ $# -gt 0 ]; do [ "$1" = "-o" ] && out="$2"; shift; done\n'
            f'[ {exit_code} -eq 0 ] && echo "<svg/>" > "$out"\n'
            f'echo "{stderr}" >&2\nexit {exit_code}\n'
        )
        script.chmod(0o755)
        return str(script)

    def test_render_success(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertIsNone(sources.check_mermaid("flowchart LR\n A-->B", self.fake_mmdc(d, 0)))

    def test_render_failure_reports_stderr(self):
        with tempfile.TemporaryDirectory() as d:
            error = sources.check_mermaid("flowchart LR\n A-->", self.fake_mmdc(d, 1, "Parse error"))
            self.assertIn("Parse error", error)

    @unittest.skipUnless(shutil.which("mmdc"), "Mermaid CLI not installed")
    def test_real_mmdc_rejects_bad_syntax(self):
        self.assertTrue(sources.check_mermaid("flowchart LR\n A -.->|x| B --- ??? C"))


class RealBundle(unittest.TestCase):
    def run_script(self, name):
        return subprocess.run(
            [sys.executable, str(ROOT / "scripts" / name)], capture_output=True, text=True
        )

    def test_bundle_validates(self):
        result = self.run_script("validate_skill_bundle.py")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_shipped_diagram_sources_pass(self):
        result = self.run_script("check_diagram_sources.py")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_every_example_has_caption_and_source(self):
        for path in sorted((ROOT / "examples").rglob("[0-9]*.md")):
            text = path.read_text(encoding="utf-8")
            self.assertIn("**Caption:**", text, path.name)
            self.assertIn("```", text, path.name)
            self.assertIn("**Type:**", text.replace("**Diagram type:**", "**Type:**"), path.name)


if __name__ == "__main__":
    unittest.main()
