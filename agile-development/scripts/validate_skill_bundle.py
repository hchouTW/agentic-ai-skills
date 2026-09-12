#!/usr/bin/env python3
"""Validate the agile-development skill bundle's structural integrity.

Purpose: catch accidental deletions or truncations of files this skill's SKILL.md
and README.md depend on.

What it does: checks that every file this package is expected to ship (SKILL.md,
README.md, agents metadata, references, assets, scripts, tests) exists and is
non-empty, that SKILL.md has YAML frontmatter with name/description, and that
README.md has its expected section headers.

Usage: run with no arguments from anywhere; it resolves paths relative to its own
location. `python3 scripts/validate_skill_bundle.py`. No third-party dependencies.
"""
from __future__ import annotations

from pathlib import Path

REQUIRED_PATHS = [
    "SKILL.md",
    "README.md",
    "VALIDATION.md",
    "agents/openai.yaml",
    "references/communication.md",
    "references/cpp-balanced-design-guidelines.md",
    "references/design-and-estimation.md",
    "references/engineering-playbook.md",
    "references/implementation-discipline.md",
    "references/product-framing.md",
    "references/risk-and-quality.md",
    "references/software-architecture.md",
    "references/validation-and-done.md",
    "references/example-authoring.md",
    "references/prompt-engineering-and-token-optimization.md",
    "assets/completion-summary.md",
    "assets/definition-of-done.md",
    "assets/risk-register.md",
    "assets/story-card.md",
    "scripts/create_story_card.py",
    "scripts/validate_agile_notes.py",
    "scripts/validate_skill_bundle.py",
    "scripts/generate_skill_example.py",
    "scripts/validate_skill_example.py",
    "scripts/check_example_diversity.py",
    "tests/test_agile_skill.py",
    "tests/test_example_authoring.py",
    "examples/README.md",
    "examples/01-bug-fix-scoping-review.md",
    "examples/02-new-feature-slicing-and-acceptance-criteria.md",
    "examples/03-production-incident-response-postmortem.md",
    "examples/04-trajectory-discount-stacking-bug.md",
    "examples/05-trajectory-database-migration-lock.md",
    "examples/06-trajectory-dependency-update-silent-break.md",
    "examples/07-gated-pipeline-payment-provider-rollout-rfc.md",
    "examples/08-gated-pipeline-legacy-billing-strangler-fig.md",
    "examples/09-gated-pipeline-public-api-contract-change.md",
    "examples/10-decision-tree-incident-mitigation-triage.md",
    "examples/11-decision-tree-pr-review-response-triage.md",
    "examples/12-decision-tree-staging-vs-production-parity-triage.md",
    "examples/13-elicitation-checkout-latency-ambiguous-request.md",
    "examples/14-elicitation-database-migration-ambiguous-request.md",
    "examples/15-elicitation-add-caching-ambiguous-request.md",
    "examples/16-adversarial-audit-hotfix-pr-description.md",
    "examples/17-adversarial-audit-backward-compatible-design-doc.md",
    "examples/18-adversarial-audit-acceptance-criteria-completeness.md",
    "examples/19-test-first-story-card-generator-invariant.md",
    "examples/20-test-first-risk-register-entry-invariant.md",
    "examples/21-test-first-definition-of-done-invariant.md",
    "examples/22-postmortem-production-api-outage-bad-deploy.md",
    "examples/23-postmortem-feature-flag-gap-partial-outage.md",
    "examples/24-postmortem-migration-lock-production.md",
]

REQUIRED_README_SECTIONS = [
    "## Installation and invocation",
    "## Quick checks",
    "## Coverage and boundaries",
    "## Example prompts",
]


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    missing = [path for path in REQUIRED_PATHS if not (root / path).exists()]
    empty = [
        path
        for path in REQUIRED_PATHS
        if (root / path).exists() and (root / path).stat().st_size == 0
    ]

    if missing or empty:
        if missing:
            print("missing files:")
            for path in missing:
                print(f"  {path}")
        if empty:
            print("empty files:")
            for path in empty:
                print(f"  {path}")
        raise SystemExit(1)

    skill = (root / "SKILL.md").read_text(encoding="utf-8")
    if not skill.startswith("---\n"):
        print("SKILL.md is missing YAML frontmatter")
        raise SystemExit(1)
    frontmatter = skill.split("---", 2)[1]
    for field in ("name:", "description:"):
        if field not in frontmatter:
            print(f"SKILL.md frontmatter is missing {field}")
            raise SystemExit(1)

    readme = (root / "README.md").read_text(encoding="utf-8")
    missing_sections = [s for s in REQUIRED_README_SECTIONS if s not in readme]
    if missing_sections:
        print("README.md is missing sections:")
        for section in missing_sections:
            print(f"  {section}")
        raise SystemExit(1)

    print(f"Bundle OK: {len(REQUIRED_PATHS)} files present and non-empty.")


if __name__ == "__main__":
    main()
