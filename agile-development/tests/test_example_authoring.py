"""Behavioral tests for the example-authoring helper scripts.

Purpose: cover `generate_skill_example.py` (scaffold) and
`validate_skill_example.py` (structural + placeholder checks) across all four
archetypes (contrast, trajectory, gated-pipeline, decision-tree) - the tooling
behind references/example-authoring.md.

Usage: run from the skill directory with
`python3 -m unittest discover -s tests -v`. Standard library only; no external
services or dependencies are needed.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import generate_skill_example  # noqa: E402
import validate_skill_example  # noqa: E402


GOOD_CONTRAST = """---
role: Staff Software Engineer
skill: agile-development
archetype: contrast
use_case: scoping a discount-code bug fix
---

## Scenario

A customer reports the cart total is wrong when a discount code is applied
alongside a shipping promotion. The team must scope and fix the bug.

## Common Weak Approach

```python
def apply_discount(total, code):
    return total * 0.9
```

This ignores stacking rules entirely.

## Expert-Level Best Practice

```python
def apply_discount(total, code, promotions):
    for promo in promotions:
        total = promo.apply(total)
    return total
```

This composes promotions explicitly and is covered by a regression test.

## Key Takeaways

- Reproduce the bug with a failing test before writing a fix.
- Model discount stacking as an explicit, ordered list rather than a single multiplier.
- Add a regression test that encodes the specific reported combination.
"""

LEGACY_CONTRAST_NO_ARCHETYPE_FIELD = """---
role: Staff Software Engineer
skill: agile-development
use_case: scoping a discount-code bug fix
---

## Scenario

A customer reports the cart total is wrong. The team must scope and fix it.

## Common Weak Approach

Patches the one reported case with no test.

## Expert-Level Best Practice

Writes a failing test first, then fixes the underlying stacking contract.

## Key Takeaways

- Reproduce the bug with a failing test before writing a fix.
- Model discount stacking as an explicit, ordered list rather than a single multiplier.
- Add a regression test that encodes the specific reported combination.
"""

GOOD_TRAJECTORY = """---
role: Senior Software Engineer
skill: agile-development
archetype: trajectory
problem_input: a bug report that the cart total is wrong with a discount code
---

## 1. Task Input & Context

A customer reports the cart total is wrong when a 10% code and a $5 flat code
are both applied. This is the fourth report against the same code path.

## 2. Root-Cause Triage & Action Plan

Reproducing the report shows the flat discount is applied before the
percentage discount, halving its effect. Plan: reorder to percentage-then-flat
and add a regression test for this exact combination.

## 3. Surgical Execution

```diff
-    total = apply_flat(total, flat_code)
-    total = apply_percent(total, percent_code)
+    total = apply_percent(total, percent_code)
+    total = apply_flat(total, flat_code)
```

## 4. Verification Evidence

```
$ python3 -m pytest tests/test_discounts.py -k stacking
1 passed in 0.04s
```

## 5. Final Deliverable Summary

Reordered discount application and added a regression test covering the
percent-then-flat stacking case; the reported total now matches expectations.
"""

GOOD_GATED_PIPELINE = """---
role: Principal Software Engineer
skill: agile-development
archetype: gated-pipeline
high_stakes_task: drafting an RFC for a feature-flagged checkout rollout
---

## Phase 1: Input Extraction & Gap Formulation

Extracted the rollout requirements from the checkout team and identified that
the rollback trigger and metric thresholds were not yet defined.

**Gate:** proceed only once rollback trigger and success metrics are named.

## Phase 2: Draft Synthesis

Drafted the RFC aligning to `references/design-and-estimation.md`'s
feature-flag rollout checklist, naming the specific staged-rollout percentages
and the metric dashboard used to gate each stage.

**Gate:** proceed only once the draft cites that checklist section by name.

## Phase 3: Red-Team Review & Final Artifact Packaging

Stress-tested the assumption that the flag system fails closed; a review
found it actually fails open under a config-fetch timeout, so the RFC was
revised to require a fail-closed default before rollout.

**Gate:** merge only once the fail-closed default is implemented and tested.
"""

GOOD_DECISION_TREE = """---
role: Engineering Lead
skill: agile-development
archetype: decision-tree
scenario: triaging an incident page for a checkout outage with unclear cause
---

## Triage Matrix

| Trigger | Resolution Strategy |
|---|---|
| Error rate spike immediately after a deploy | Roll back the deploy first |
| Error rate spike with no recent deploy | Check upstream dependency status pages |
| Elevated latency only, no errors | Check database connection pool saturation |
| Page with no corresponding dashboard signal | Treat as a possible false alarm; page secondary on-call to confirm |

## Selected Branch

The page fired one minute after a deploy completed, so the first row applies:
roll back the deploy first.

## End-to-End Execution Script

Run `deploy rollback checkout-service --to-previous`, confirm the error rate
returns to baseline within two minutes, then post in #incidents: "Rolled back
checkout-service to the prior release; error rate recovering, investigating
root cause of the regression before re-attempting the deploy."

## Fallback Safeguards

If the rollback does not restore baseline error rates within five minutes,
escalate to the database on-call in parallel and assume a coincident second
cause rather than continuing to wait on the rollback alone.
"""


def _scaffold_args(**overrides) -> argparse.Namespace:
    defaults = dict(
        archetype="contrast",
        skill="agile-development",
        role="Staff Software Engineer",
        use_case="scoping a bug fix",
        problem_input=None,
        high_stakes_task=None,
        scenario=None,
        takeaways=4,
        output=None,
    )
    defaults.update(overrides)
    return argparse.Namespace(**defaults)


class GenerateSkillExampleTests(unittest.TestCase):
    def test_contrast_skeleton_has_frontmatter_and_all_sections_in_order(self):
        skeleton = generate_skill_example.build_skeleton(_scaffold_args())
        self.assertIn("role: Staff Software Engineer", skeleton)
        self.assertIn("skill: agile-development", skeleton)
        self.assertIn("archetype: contrast", skeleton)
        self.assertIn("use_case: scoping a bug fix", skeleton)
        sections = ["## Scenario", "## Common Weak Approach",
                    "## Expert-Level Best Practice", "## Key Takeaways"]
        positions = [skeleton.index(s) for s in sections]
        self.assertEqual(positions, sorted(positions))

    def test_takeaway_count_matches_requested_number(self):
        skeleton = generate_skill_example.build_skeleton(_scaffold_args(takeaways=6))
        self.assertEqual(skeleton.count("<!-- Takeaway"), 6)

    def test_trajectory_skeleton_has_five_sections_in_order(self):
        args = _scaffold_args(archetype="trajectory", use_case=None, problem_input="a raw bug report", takeaways=None)
        skeleton = generate_skill_example.build_skeleton(args)
        self.assertIn("archetype: trajectory", skeleton)
        self.assertIn("problem_input: a raw bug report", skeleton)
        sections = [
            "## 1. Task Input & Context",
            "## 2. Root-Cause Triage & Action Plan",
            "## 3. Surgical Execution",
            "## 4. Verification Evidence",
            "## 5. Final Deliverable Summary",
        ]
        positions = [skeleton.index(s) for s in sections]
        self.assertEqual(positions, sorted(positions))

    def test_gated_pipeline_skeleton_has_three_phases_with_gate_placeholders(self):
        args = _scaffold_args(archetype="gated-pipeline", use_case=None, high_stakes_task="a rollout RFC", takeaways=None)
        skeleton = generate_skill_example.build_skeleton(args)
        self.assertIn("archetype: gated-pipeline", skeleton)
        sections = [
            "## Phase 1: Input Extraction & Gap Formulation",
            "## Phase 2: Draft Synthesis",
            "## Phase 3: Red-Team Review & Final Artifact Packaging",
        ]
        positions = [skeleton.index(s) for s in sections]
        self.assertEqual(positions, sorted(positions))
        self.assertEqual(skeleton.count("**Gate:**"), 3)

    def test_decision_tree_skeleton_has_matrix_and_fixed_sections(self):
        args = _scaffold_args(archetype="decision-tree", use_case=None, scenario="an ambiguous incident page", takeaways=None)
        skeleton = generate_skill_example.build_skeleton(args)
        self.assertIn("archetype: decision-tree", skeleton)
        sections = [
            "## Triage Matrix",
            "## Selected Branch",
            "## End-to-End Execution Script",
            "## Fallback Safeguards",
        ]
        positions = [skeleton.index(s) for s in sections]
        self.assertEqual(positions, sorted(positions))
        self.assertIn("| Trigger | Resolution Strategy |", skeleton)

    def test_cli_rejects_takeaways_out_of_range(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts/generate_skill_example.py"),
             "--archetype", "contrast", "--skill", "agile-development", "--role", "X",
             "--use-case", "Y", "--takeaways", "10"],
            capture_output=True, text=True,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("--takeaways must be between", result.stderr)

    def test_cli_rejects_takeaways_for_non_contrast_archetype(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts/generate_skill_example.py"),
             "--archetype", "trajectory", "--skill", "agile-development", "--role", "X",
             "--problem-input", "Y", "--takeaways", "4"],
            capture_output=True, text=True,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("--takeaways is only valid with --archetype contrast", result.stderr)

    def test_cli_missing_required_flag_fails_with_usage(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts/generate_skill_example.py"), "--skill", "x"],
            capture_output=True, text=True,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("usage:", result.stderr)

    def test_cli_missing_scenario_flag_for_archetype_fails(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts/generate_skill_example.py"),
             "--archetype", "decision-tree", "--skill", "agile-development", "--role", "X"],
            capture_output=True, text=True,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("--archetype decision-tree requires --scenario", result.stderr)

    def test_cli_rejects_wrong_scenario_flag_for_archetype(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts/generate_skill_example.py"),
             "--archetype", "contrast", "--skill", "agile-development", "--role", "X",
             "--use-case", "Y", "--scenario", "Z"],
            capture_output=True, text=True,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("--scenario is only valid with --archetype decision-tree", result.stderr)

    def test_cli_writes_to_output_path(self):
        out_path = ROOT / "tests" / "_scratch_scaffold.md"
        try:
            result = subprocess.run(
                [sys.executable, str(ROOT / "scripts/generate_skill_example.py"),
                 "--archetype", "contrast", "--skill", "agile-development", "--role", "X",
                 "--use-case", "Y", "--output", str(out_path)],
                capture_output=True, text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(out_path.exists())
            self.assertIn("## Scenario", out_path.read_text(encoding="utf-8"))
        finally:
            out_path.unlink(missing_ok=True)


class ValidateContrastTests(unittest.TestCase):
    def test_valid_example_passes(self):
        self.assertEqual(validate_skill_example.validate(GOOD_CONTRAST), [])

    def test_legacy_example_without_archetype_field_defaults_to_contrast(self):
        self.assertEqual(validate_skill_example.validate(LEGACY_CONTRAST_NO_ARCHETYPE_FIELD), [])

    def test_missing_frontmatter_field_is_reported(self):
        broken = GOOD_CONTRAST.replace("skill: agile-development\n", "")
        problems = validate_skill_example.validate(broken)
        self.assertTrue(any("skill" in p for p in problems))

    def test_missing_frontmatter_block_is_reported(self):
        no_frontmatter = GOOD_CONTRAST.split("---\n", 2)[-1]
        problems = validate_skill_example.validate(no_frontmatter)
        self.assertTrue(any("missing frontmatter" in p for p in problems))

    def test_unknown_archetype_value_is_reported(self):
        broken = GOOD_CONTRAST.replace("archetype: contrast", "archetype: bogus")
        problems = validate_skill_example.validate(broken)
        self.assertTrue(any("unknown archetype" in p for p in problems))

    def test_missing_section_is_reported(self):
        broken = GOOD_CONTRAST.replace("## Key Takeaways", "## Something Else")
        problems = validate_skill_example.validate(broken)
        self.assertTrue(any("Key Takeaways" in p for p in problems))

    def test_out_of_order_sections_are_reported(self):
        scenario = "## Scenario\n\nSome scenario text.\n\n"
        weak = "## Common Weak Approach\n\nweak\n\n"
        expert = "## Expert-Level Best Practice\n\nexpert\n\n"
        takeaways = "## Key Takeaways\n\n- a\n- b\n- c\n"
        frontmatter = "---\nrole: X\nskill: agile-development\narchetype: contrast\nuse_case: Y\n---\n\n"
        reordered = frontmatter + weak + scenario + expert + takeaways
        problems = validate_skill_example.validate(reordered)
        self.assertTrue(any("out of order" in p for p in problems))

    def test_too_few_takeaways_is_reported(self):
        broken = GOOD_CONTRAST.replace(
            "- Add a regression test that encodes the specific reported combination.\n", "")
        problems = validate_skill_example.validate(broken)
        self.assertTrue(any("Key Takeaways has 2 bullet item(s)" in p for p in problems))

    def test_too_many_takeaways_is_reported(self):
        extra = GOOD_CONTRAST + "- A seventh takeaway.\n- An eighth takeaway.\n- A ninth takeaway.\n- A tenth.\n"
        problems = validate_skill_example.validate(extra)
        self.assertTrue(any("bullet item(s), expected 3-6" in p for p in problems))

    def test_todo_marker_is_flagged(self):
        broken = GOOD_CONTRAST.replace("This ignores stacking rules entirely.", "TODO: explain this")
        problems = validate_skill_example.validate(broken)
        self.assertTrue(any("placeholder marker" in p for p in problems))

    def test_lorem_ipsum_is_flagged(self):
        broken = GOOD_CONTRAST.replace("This ignores stacking rules entirely.", "Lorem ipsum dolor sit amet.")
        problems = validate_skill_example.validate(broken)
        self.assertTrue(any("Lorem ipsum" in p for p in problems))

    def test_bracketed_stand_in_is_flagged(self):
        broken = GOOD_CONTRAST.replace("This ignores stacking rules entirely.", "[Your explanation here]")
        problems = validate_skill_example.validate(broken)
        self.assertTrue(any("bracketed stand-in" in p for p in problems))

    def test_leftover_scaffold_comment_is_flagged(self):
        broken = GOOD_CONTRAST + "\n<!-- fill this in -->\n"
        problems = validate_skill_example.validate(broken)
        self.assertTrue(any("leftover scaffold comment" in p for p in problems))

    def test_standalone_ellipsis_line_is_flagged(self):
        broken = GOOD_CONTRAST.replace(
            "This composes promotions explicitly and is covered by a regression test.",
            "This composes promotions explicitly.\n\n...\n")
        problems = validate_skill_example.validate(broken)
        self.assertTrue(any("standalone '...' line" in p for p in problems))

    def test_generated_scaffold_fails_validation_until_filled_in(self):
        skeleton = generate_skill_example.build_skeleton(_scaffold_args())
        self.assertNotEqual(validate_skill_example.validate(skeleton), [])

    def test_cli_ok_on_valid_file(self):
        path = ROOT / "tests" / "_scratch_valid.md"
        path.write_text(GOOD_CONTRAST, encoding="utf-8")
        try:
            result = subprocess.run(
                [sys.executable, str(ROOT / "scripts/validate_skill_example.py"), str(path)],
                capture_output=True, text=True,
            )
            self.assertEqual(result.returncode, 0, result.stdout)
            self.assertIn(": ok", result.stdout)
        finally:
            path.unlink(missing_ok=True)

    def test_cli_missing_file_fails_cleanly_not_with_traceback(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts/validate_skill_example.py"),
             str(ROOT / "tests/does-not-exist.md")],
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("file not found", result.stdout)
        self.assertNotIn("Traceback", result.stderr)


class ValidateTrajectoryTests(unittest.TestCase):
    def test_valid_example_passes(self):
        self.assertEqual(validate_skill_example.validate(GOOD_TRAJECTORY), [])

    def test_missing_section_is_reported(self):
        broken = GOOD_TRAJECTORY.replace("## 5. Final Deliverable Summary", "## Something Else")
        problems = validate_skill_example.validate(broken)
        self.assertTrue(any("5. Final Deliverable Summary" in p for p in problems))

    def test_missing_code_fence_in_execution_section_is_reported(self):
        broken = GOOD_TRAJECTORY.replace(
            "```diff\n-    total = apply_flat(total, flat_code)\n"
            "-    total = apply_percent(total, percent_code)\n"
            "+    total = apply_percent(total, percent_code)\n"
            "+    total = apply_flat(total, flat_code)\n```",
            "Reordered the two calls.",
        )
        problems = validate_skill_example.validate(broken)
        self.assertTrue(any("3. Surgical Execution" in p and "fenced code block" in p for p in problems))

    def test_missing_code_fence_in_verification_section_is_reported(self):
        broken = GOOD_TRAJECTORY.replace(
            "```\n$ python3 -m pytest tests/test_discounts.py -k stacking\n1 passed in 0.04s\n```",
            "The test suite passed.",
        )
        problems = validate_skill_example.validate(broken)
        self.assertTrue(any("4. Verification Evidence" in p and "fenced code block" in p for p in problems))

    def test_generated_scaffold_fails_validation_until_filled_in(self):
        args = _scaffold_args(archetype="trajectory", use_case=None, problem_input="a raw bug report", takeaways=None)
        skeleton = generate_skill_example.build_skeleton(args)
        self.assertNotEqual(validate_skill_example.validate(skeleton), [])


class ValidateGatedPipelineTests(unittest.TestCase):
    def test_valid_example_passes(self):
        self.assertEqual(validate_skill_example.validate(GOOD_GATED_PIPELINE), [])

    def test_missing_gate_line_is_reported(self):
        broken = GOOD_GATED_PIPELINE.replace(
            "**Gate:** proceed only once rollback trigger and success metrics are named.\n", "")
        problems = validate_skill_example.validate(broken)
        self.assertTrue(any("Phase 1" in p and "Gate" in p for p in problems))

    def test_phase_three_without_assumption_language_is_reported(self):
        broken = GOOD_GATED_PIPELINE.replace(
            "Stress-tested the assumption that the flag system fails closed; a review\n"
            "found it actually fails open under a config-fetch timeout, so the RFC was\n"
            "revised to require a fail-closed default before rollout.",
            "Reviewed the draft once more and polished the wording.",
        )
        problems = validate_skill_example.validate(broken)
        self.assertTrue(any("Phase 3" in p and "assumption" in p for p in problems))

    def test_generated_scaffold_fails_validation_until_filled_in(self):
        args = _scaffold_args(archetype="gated-pipeline", use_case=None, high_stakes_task="a rollout RFC", takeaways=None)
        skeleton = generate_skill_example.build_skeleton(args)
        self.assertNotEqual(validate_skill_example.validate(skeleton), [])


class ValidateDecisionTreeTests(unittest.TestCase):
    def test_valid_example_passes(self):
        self.assertEqual(validate_skill_example.validate(GOOD_DECISION_TREE), [])

    def test_too_few_matrix_rows_is_reported(self):
        broken = GOOD_DECISION_TREE.replace(
            "| Elevated latency only, no errors | Check database connection pool saturation |\n"
            "| Page with no corresponding dashboard signal | Treat as a possible false "
            "alarm; page secondary on-call to confirm |\n", "")
        problems = validate_skill_example.validate(broken)
        self.assertTrue(any("Triage Matrix" in p and "data row" in p for p in problems))

    def test_missing_table_is_reported(self):
        broken = GOOD_DECISION_TREE.replace(
            "| Trigger | Resolution Strategy |\n"
            "|---|---|\n"
            "| Error rate spike immediately after a deploy | Roll back the deploy first |\n"
            "| Error rate spike with no recent deploy | Check upstream dependency status pages |\n"
            "| Elevated latency only, no errors | Check database connection pool saturation |\n"
            "| Page with no corresponding dashboard signal | Treat as a possible false "
            "alarm; page secondary on-call to confirm |\n",
            "A prose description of the triage logic instead of a table.\n",
        )
        problems = validate_skill_example.validate(broken)
        self.assertTrue(any("missing a markdown table" in p for p in problems))

    def test_generated_scaffold_fails_validation_until_filled_in(self):
        args = _scaffold_args(archetype="decision-tree", use_case=None, scenario="an ambiguous incident page", takeaways=None)
        skeleton = generate_skill_example.build_skeleton(args)
        self.assertNotEqual(validate_skill_example.validate(skeleton), [])


if __name__ == "__main__":
    unittest.main()
