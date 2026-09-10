---
role: Senior Software Engineer
skill: agile-development
archetype: trajectory
problem_input: a routine dependency version bump was merged and CI passed, but a specific edge case in production started silently returning wrong results afterward
---

## 1. Task Input & Context

Finance reconciliation report, three weeks after a routine dependency bump
merged with a passing CI run:

> Ledger reconciliation for the last 3 weeks shows total invoiced amounts are
> $342.18 lower than the sum of individual line-item ledger entries.
> 34,218 invoices are affected, each short by exactly $0.01. No errors were
> logged; invoices generated, sent, and paid normally. The only change in
> that window to the invoicing service was bumping `moneyfmt` (the shared
> currency-rounding helper) from `3.2.0` to `3.3.0`.

## 2. Root-Cause Triage & Action Plan

Reading `moneyfmt`'s changelog for `3.3.0`: "switched internal cent-rounding
from round-half-up to round-half-to-even (banker's rounding), for consistency
with accounting standards." The package's own version number called this a
minor release, but changing a rounding default is a behavior change, not a
compatible addition.

Reproducing locally against a subtotal that lands exactly on a rounding
boundary confirms the mechanism:

```python
from decimal import Decimal, ROUND_HALF_UP, ROUND_HALF_EVEN
subtotal = Decimal("12.345")
print(subtotal.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))   # 12.35 (moneyfmt 3.2.0's behavior)
print(subtotal.quantize(Decimal("0.01"), rounding=ROUND_HALF_EVEN)) # 12.34 (moneyfmt 3.3.0's new default)
```

Both invoices and CI fixtures round-trip correctly for ordinary subtotals;
the two rounding modes only disagree when a subtotal lands exactly on a
`...X5` cent boundary where the preceding digit `X` is even (as in `12.345`
above) - a narrow, easy-to-miss case. Per
`references/engineering-playbook.md`'s Dependency Update playbook step 2
("review compatibility with supported runtimes and neighboring dependencies")
and step 5 ("run affected tests... when available"), the actual gap is that
none of the existing test fixtures for the invoicing service happened to use
an exact rounding-boundary subtotal, so CI passed without ever exercising the
behavior that changed.

Action plan: pin `moneyfmt` back to the explicit rounding mode the invoicing
service actually requires (round-half-up, matching the accounting team's
stated policy) rather than depending on the library's default, add a
regression test using an exact-boundary subtotal so this class of change is
caught next time regardless of the library's default, and issue $0.01 credit
adjustments for the 34,218 affected invoices.

## 3. Surgical Execution

```diff
 from moneyfmt import round_currency

-def invoice_total(subtotal):
-    return round_currency(subtotal)
+from decimal import ROUND_HALF_UP
+
+def invoice_total(subtotal):
+    # Pin the rounding mode explicitly; do not depend on moneyfmt's default,
+    # which changed between 3.2.0 and 3.3.0 with no corresponding major bump.
+    return round_currency(subtotal, rounding=ROUND_HALF_UP)
```

## 4. Verification Evidence

```
$ python3 -m pytest tests/test_invoice_rounding.py -v
tests/test_invoice_rounding.py::test_rounds_ordinary_subtotal_up PASSED
tests/test_invoice_rounding.py::test_rounds_exact_boundary_subtotal_half_up PASSED
tests/test_invoice_rounding.py::test_matches_moneyfmt_3_2_0_behavior_regardless_of_installed_version PASSED
3 passed in 0.03s
$ python3 scripts/reconcile_ledger.py --since 2026-08-01 --after-fix
34,218 invoices credited $0.01 each; total adjustment $342.18
reconciliation delta: $0.00 (matches ledger exactly)
```

`test_matches_moneyfmt_3_2_0_behavior_regardless_of_installed_version` pins
the rounding mode explicitly and asserts the `12.345 -> 12.35` result
independent of which `moneyfmt` version is installed, closing off the same
failure mode recurring on a future upgrade.

## 5. Final Deliverable Summary

Traced a silent $0.01-per-invoice discrepancy to a "minor" dependency bump
that changed a rounding default from round-half-up to round-half-to-even,
undetected because no existing test used an exact rounding-boundary
subtotal. Pinned the rounding mode explicitly at the call site instead of
relying on the library default, added a regression test that is independent
of the installed `moneyfmt` version, and credited the 34,218 affected
invoices for the exact discrepancy found.
