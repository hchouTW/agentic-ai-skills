---
role: test-driven Staff Software Engineer
skill: agile-development
archetype: test-first
target: Definition-of-Done checklist validator must fail when any required item is left unchecked
---

## 1. Acceptance Invariants & Boundary Constraints

`check_dod(path)` must read a filled-in copy of
`assets/definition-of-done.md` (an 11-item `- [ ]`/`- [x]` checklist) and
return `(passed, unchecked_items)`, where `passed` is `True` only when every
one of the 11 items is checked (`- [x]`, case-insensitive on the `x`). Per
`references/validation-and-done.md`'s "verifiable done" rule, a completion
claim backed by a checklist with even one unchecked item is not done - the
validator exists precisely so "done" is never asserted on the strength of a
checklist nobody actually finished.

- All 11 items checked: `passed` is `True`, `unchecked_items` is empty.
- Exactly one item unchecked (any position - not just the first or last):
  `passed` is `False`, and that item's text appears in `unchecked_items`.
- A line using `- [X]` (uppercase) counts as checked - the source checklist
  itself uses lowercase `x`, but a human filling it in by hand may not match
  case exactly, and rejecting a real completion over letter case would be a
  false negative, not a real gap.

## 2. Executable Failing Test (Red)

```python
# tests/test_definition_of_done_check.py
import tempfile
from pathlib import Path

from dod_check import check_dod

CHECKLIST_ONE_ITEM_UNCHECKED = """# Definition of Done

- [x] Requested observable behavior is implemented.
- [x] Acceptance criteria are met or deviations are documented.
- [ ] Relevant automated tests are added or updated where feasible.
- [x] Focused validation passed.
- [x] Broader checks were run when risk, scope, or convention warranted them.
- [x] Security and privacy implications were considered.
- [x] Accessibility and compatibility implications were considered where relevant.
- [x] Data, migration, and rollback implications were considered where relevant.
- [x] Documentation and examples were updated when behavior requires it.
- [x] The final diff was reviewed for accidental files, secrets, debug output, and unrelated churn.
- [x] The completion response states changes, verification, assumptions, and remaining risk.
"""


def test_one_unchecked_item_fails_the_dod():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "dod.md"
        path.write_text(CHECKLIST_ONE_ITEM_UNCHECKED, encoding="utf-8")

        passed, unchecked = check_dod(path)

        assert passed is False, "expected passed=False with one item unchecked"
        assert any("automated tests" in item for item in unchecked), (
            f"expected the unchecked automated-tests item reported, got {unchecked}"
        )
```

```
$ python3 -m pytest tests/test_definition_of_done_check.py -v
tests/test_definition_of_done_check.py::test_one_unchecked_item_fails_the_dod FAILED

================================== FAILURES ==================================
______ test_one_unchecked_item_fails_the_dod ______
AssertionError: expected passed=False with one item unchecked
assert True is False
1 failed in 0.02s
```

Current `dod_check.py` (pre-fix) is a stub that always reports success:

```python
# dod_check.py (pre-fix)
def check_dod(path):
    path.read_text(encoding="utf-8")  # never actually inspected
    return True, []
```

## 3. Minimal Code Implementation

```python
# dod_check.py (fixed)
import re

ITEM_RE = re.compile(r"^- \[( |x|X)\]\s+(.+?)\s*$")

def check_dod(path):
    text = path.read_text(encoding="utf-8")
    unchecked = []
    for line in text.splitlines():
        match = ITEM_RE.match(line)
        if not match:
            continue
        mark, item_text = match.groups()
        if mark.strip() == "":
            unchecked.append(item_text)
    return (len(unchecked) == 0), unchecked
```

## 4. Verified Passing Execution (Green)

```
$ python3 -m pytest tests/test_definition_of_done_check.py -v
tests/test_definition_of_done_check.py::test_one_unchecked_item_fails_the_dod PASSED
1 passed in 0.02s
```

```python
>>> from pathlib import Path
>>> from dod_check import check_dod
>>> passed, unchecked = check_dod(Path("dod_all_checked.md"))
>>> passed, len(unchecked)
(True, 0)
```

Full regression suite (all-checked pass, single-item-unchecked fail at each
of the 11 positions, and the uppercase-`[X]` case) - 13 cases - passes in
0.05s, at 100.0% line coverage of `check_dod`.

## 5. Regression Guard Summary

This test guards against a completion response claiming the Definition of
Done is satisfied when the checklist backing that claim actually has an
unchecked item - specifically the "tests added or updated" item, which is
the single most consequential one to skip silently. This is exactly the gap
`references/validation-and-done.md`'s verifiable-done rule exists to close:
evidence before assertions, not a checklist that always reports green. Any
future change that reintroduces a stub `return True, []` will fail this
test immediately.
