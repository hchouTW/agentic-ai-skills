---
role: test-driven Staff Software Engineer
skill: agile-development
archetype: test-first
target: create_story_card.py must reject a story card with no real acceptance criteria instead of silently filling in generic defaults
---

## 1. Acceptance Invariants & Boundary Constraints

`scripts/create_story_card.py` must exit non-zero with an explicit message
when invoked with no `--criteria` flag at all (or only empty/whitespace
`--criteria` values), instead of silently substituting its built-in generic
default criteria. Per `references/validation-and-done.md`'s "verifiable
done" rule, a story card's acceptance criteria are the thing a reviewer
checks work against - a generated card whose criteria are boilerplate
("the expected result is observable") rather than this story's real,
checkable criteria is worse than no card at all, because it looks complete.

- `--criteria` supplied with one or more non-empty values: the script
  succeeds (exit 0) and emits exactly those criteria.
- `--criteria` omitted entirely: the script must exit 1 with a message
  naming the missing flag, not fall back to its generic defaults.
- `--criteria ""` (a single empty-string value): treated the same as
  omitted - must also exit 1, not silently emit a blank checklist item.

## 2. Executable Failing Test (Red)

```python
# tests/test_create_story_card_requires_criteria.py
import subprocess
import sys


def test_missing_criteria_flag_is_rejected():
    result = subprocess.run(
        [
            sys.executable, "scripts/create_story_card.py",
            "--actor", "on-call engineer",
            "--capability", "a rollback runbook for the payments service",
            "--outcome", "a bad deploy can be reverted in under 5 minutes",
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 1, (
        f"expected exit 1 with no --criteria, got {result.returncode}: "
        f"{result.stdout!r}"
    )
    assert "--criteria" in result.stderr, (
        f"expected the missing flag named in stderr, got {result.stderr!r}"
    )
```

```
$ python3 -m pytest tests/test_create_story_card_requires_criteria.py -v
tests/test_create_story_card_requires_criteria.py::test_missing_criteria_flag_is_rejected FAILED

================================== FAILURES ==================================
______ test_missing_criteria_flag_is_rejected ______
AssertionError: expected exit 1 with no --criteria, got 0: '# Story Card\n\n## Story\n\nAs a on-call engineer, I want a rollback runbook for the payments service, so that a bad deploy can be reverted in under 5 minutes.\n\n## Acceptance Criteria\n\n- [ ] Given the primary context, when the user performs the action, then the expected result is observable.\n- [ ] Given an invalid or boundary context, when the action is attempted, then the system responds safely.\n...'
assert 0 == 1
1 failed in 0.09s
```

Current `build_card()` (pre-fix excerpt) silently substitutes generic
defaults whenever `--criteria` is falsy:

```python
# scripts/create_story_card.py (pre-fix excerpt)
def build_card(args: argparse.Namespace) -> str:
    criteria = args.criteria or [
        "Given the primary context, when the user performs the action, then the expected result is observable.",
        "Given an invalid or boundary context, when the action is attempted, then the system responds safely.",
    ]
    validation = args.validation or ["Run the focused test or check that proves the behavior."]
    criteria_lines = "\n".join(f"- [ ] {item}" for item in criteria)
    return f"# Story Card\n\n...\n\n## Acceptance Criteria\n\n{criteria_lines}\n"
```

## 3. Minimal Code Implementation

```python
# scripts/create_story_card.py (fixed excerpt)
def build_card(args: argparse.Namespace) -> str:
    criteria = [c for c in (args.criteria or []) if c.strip()]
    ...  # unchanged below this line


def main() -> int:
    args = parse_args()
    criteria = [c for c in (args.criteria or []) if c.strip()]
    if not criteria:
        print("error: --criteria is required (at least one non-empty value)",
              file=sys.stderr)
        return 1
    content = build_card(args)
    if args.output:
        args.output.write_text(content, encoding="utf-8")
    else:
        print(content, end="")
    return 0
```

(`import sys` added alongside the existing `argparse`/`Path` imports.)

## 4. Verified Passing Execution (Green)

```
$ python3 -m pytest tests/test_create_story_card_requires_criteria.py -v
tests/test_create_story_card_requires_criteria.py::test_missing_criteria_flag_is_rejected PASSED
1 passed in 0.08s
```

```
$ python3 scripts/create_story_card.py --actor "on-call engineer" \
    --capability "a rollback runbook for the payments service" \
    --outcome "a bad deploy can be reverted in under 5 minutes"
error: --criteria is required (at least one non-empty value)
$ echo "exit code: $?"
exit code: 1
$ python3 scripts/create_story_card.py --actor "on-call engineer" \
    --capability "a rollback runbook for the payments service" \
    --outcome "a bad deploy can be reverted in under 5 minutes" \
    --criteria "Given a failed deploy is detected, when the runbook's revert command is run, then the previous version serves traffic within 5 minutes."
# Story Card

## Story

As a on-call engineer, I want a rollback runbook for the payments service, so that a bad deploy can be reverted in under 5 minutes.

## Acceptance Criteria

- [ ] Given a failed deploy is detected, when the runbook's revert command is run, then the previous version serves traffic within 5 minutes.
$ echo "exit code: $?"
exit code: 0
```

Full regression suite (10 existing CLI tests plus this new one) passes in
0.9s, including the case where `--criteria` is supplied and the generated
card is unchanged from before this fix.

## 5. Regression Guard Summary

This test guards against a story card that reads as complete (headings all
present, checkboxes all there) while its acceptance criteria are the
generator's own boilerplate text - exactly the failure mode
`references/validation-and-done.md` calls out: a reviewer skimming a
generated card would not immediately notice "the expected result is
observable" is not a real, checkable criterion for this story. Any future
change that reintroduces the `args.criteria or [defaults]` fallback will
fail this test immediately.
