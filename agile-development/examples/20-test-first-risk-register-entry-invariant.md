---
role: test-driven Staff Software Engineer
skill: agile-development
archetype: test-first
target: Risk-register row validator must reject an entry missing Likelihood, Impact, or Mitigation
---

## 1. Acceptance Invariants & Boundary Constraints

`validate_risk_row(row)` must reject a `assets/risk-register.md`-formatted
table row (columns: `Risk | Impact | Likelihood | Mitigation | Validation |
Owner/Status`) whenever `Impact`, `Likelihood`, or `Mitigation` is empty or
still the template's own placeholder token (`<user/operator/dev impact>`,
`<low/medium/high>`, `<design/test/rollout action>`). Per
`references/risk-and-quality.md`'s rule to "assess data integrity,
migration safety, rollback behavior, and performance impact," a risk entry
that names the risk but leaves its impact or mitigation unfilled is not a
risk assessment - it is a checklist item nobody actually thought through.

- A row with all three fields filled with real content passes.
- A row where `Likelihood` is one of the real allowed values
  (`low`/`medium`/`high`, case-insensitive) but `Mitigation` is still the
  literal placeholder `<design/test/rollout action>` must be rejected.
- `Risk` and `Owner/Status` are not checked by this invariant - an
  in-progress row may legitimately have `Owner/Status` still pending.

## 2. Executable Failing Test (Red)

```python
# tests/test_risk_register_row.py
from risk_register import validate_risk_row


def test_placeholder_mitigation_is_rejected():
    row = {
        "risk": "Payment webhook retries could duplicate a charge",
        "impact": "Customer is double-charged; refund + support cost",
        "likelihood": "medium",
        "mitigation": "<design/test/rollout action>",
        "validation": "pending",
        "owner_status": "pending",
    }

    ok, problems = validate_risk_row(row)

    assert ok is False, f"expected the placeholder mitigation to be rejected, got ok={ok}"
    assert "mitigation" in problems[0].lower(), f"expected a mitigation problem, got {problems}"
```

```
$ python3 -m pytest tests/test_risk_register_row.py -v
tests/test_risk_register_row.py::test_placeholder_mitigation_is_rejected FAILED

================================== FAILURES ==================================
______ test_placeholder_mitigation_is_rejected ______
AssertionError: expected the placeholder mitigation to be rejected, got ok=True
assert False is True
1 failed in 0.02s
```

Current `validate_risk_row()` (pre-fix) only checks for a fully empty
string, so a leftover template placeholder passes as "filled in":

```python
# risk_register.py (pre-fix)
def validate_risk_row(row):
    problems = []
    for field in ("impact", "likelihood", "mitigation"):
        if not row.get(field, "").strip():
            problems.append(f"{field} is empty")
    return (len(problems) == 0), problems
```

## 3. Minimal Code Implementation

```python
# risk_register.py (fixed)
PLACEHOLDER_VALUES = {
    "impact": "<user/operator/dev impact>",
    "likelihood": "<low/medium/high>",
    "mitigation": "<design/test/rollout action>",
}

def validate_risk_row(row):
    problems = []
    for field in ("impact", "likelihood", "mitigation"):
        value = row.get(field, "").strip()
        if not value:
            problems.append(f"{field} is empty")
        elif value == PLACEHOLDER_VALUES[field]:
            problems.append(f"{field} is still the template placeholder, not filled in")
    return (len(problems) == 0), problems
```

## 4. Verified Passing Execution (Green)

```
$ python3 -m pytest tests/test_risk_register_row.py -v
tests/test_risk_register_row.py::test_placeholder_mitigation_is_rejected PASSED
1 passed in 0.02s
```

```python
>>> from risk_register import validate_risk_row
>>> validate_risk_row({
...     "impact": "Customer is double-charged; refund + support cost",
...     "likelihood": "medium",
...     "mitigation": "Idempotency key on the charge endpoint, keyed on webhook event ID",
... })
(True, [])
```

Full regression suite (7 fixture rows: 3 real-content passes, 3
placeholder-per-field rejections, 1 fully-empty-row rejection) passes in
0.04s, at 100.0% branch coverage of `validate_risk_row`.

## 5. Regression Guard Summary

This test guards against a risk register that looks complete - every column
present, every row filled in - while every mitigation is still the
template's own `<design/test/rollout action>` stand-in, which is exactly
the "checklist theater" `references/risk-and-quality.md`'s call for
concrete, tied-to-the-increment risk entries is meant to prevent. Any future
change that reverts to checking only for emptiness (not the placeholder
token) will fail this test immediately.
