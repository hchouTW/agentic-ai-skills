---
role: Senior Software Engineer
skill: agile-development
archetype: trajectory
problem_input: a bug report that the cart total is wrong when a percentage discount code and a flat-amount discount code are both applied to the same order
---

## 1. Task Input & Context

Support ticket, pasted verbatim:

> SUPPORT-4821: Customer applied code `SAVE10` (10% off) and code `FREE5`
> (flat $5 off) to a $50.00 cart. They expected roughly $40.00 (10% off first,
> then $5 off: 50 * 0.9 - 5 = 40) but were charged $45.00. This is the fourth
> report against `apply_discounts` in `checkout/pricing.py` in the last two
> months - SUPPORT-4102, SUPPORT-4340, and SUPPORT-4560 were each patched
> individually for other specific code pairs (`SUMMER15`+`SHIP0`,
> `WELCOME20`+`GIFT10`, `VIP25`+`LOYALTY5`).

## 2. Root-Cause Triage & Action Plan

Reading `checkout/pricing.py` shows why: each discount is computed against the
original `total`, not the running result of prior discounts, so only the last
code processed actually affects the final price.

```python
def apply_discounts(total, codes):
    result = total
    for code in codes:
        if code.kind == "percent":
            result = total * (1 - code.value)
        elif code.kind == "flat":
            result = total - code.value
    return result
```

With `codes = [SAVE10, FREE5]`: iteration 1 sets `result = 50 * 0.9 = 45`;
iteration 2 overwrites it with `result = 50 - 5 = 45`, discarding the percent
discount entirely. The three prior "fixes" each added a special-cased branch
for one specific code pair instead of touching this shared reset bug, which is
why a fourth, functionally identical report kept happening.

Action plan:
1. Write a failing test asserting the two discounts compound (percent applied
   first, then flat, per the business's documented stacking order) rather than
   the last one silently winning.
2. Fix `apply_discounts` to compound onto the running `result` in a canonical
   order (percent codes before flat codes) regardless of the entry order in
   the cart, instead of resetting from `total` every iteration.
3. Delete the three prior one-off patches for `SUMMER15`+`SHIP0`,
   `WELCOME20`+`GIFT10`, and `VIP25`+`LOYALTY5` - the general fix subsumes all
   of them - and add a regression test asserting each of those three pairs
   still produces its previously-verified correct total.

## 3. Surgical Execution

```diff
-def apply_discounts(total, codes):
-    result = total
-    for code in codes:
-        if code.kind == "percent":
-            result = total * (1 - code.value)
-        elif code.kind == "flat":
-            result = total - code.value
-    return result
+def apply_discounts(total, codes):
+    # Canonical order: percent discounts compound onto the running total
+    # before flat discounts subtract from it, regardless of entry order.
+    ordered = sorted(codes, key=lambda c: 0 if c.kind == "percent" else 1)
+    result = total
+    for code in ordered:
+        if code.kind == "percent":
+            result = result * (1 - code.value)
+        elif code.kind == "flat":
+            result = result - code.value
+    return round(result, 2)
```

The three special-cased branches from SUPPORT-4102, SUPPORT-4340, and
SUPPORT-4560 (each an `if code_pair == (...): return <hardcoded total>` guard
added ahead of the general loop) were deleted in the same commit; the general
fix produces the correct total for all four reported pairs without them.

## 4. Verification Evidence

```
$ python3 -m pytest tests/test_discounts.py -k stacking -v
tests/test_discounts.py::test_percent_then_flat_stacking_matches_support_4821 PASSED
tests/test_discounts.py::test_stacking_is_independent_of_cart_entry_order PASSED
tests/test_discounts.py::test_previously_reported_pairs_still_correct PASSED
3 passed in 0.06s
```

`test_percent_then_flat_stacking_matches_support_4821` asserts
`apply_discounts(50.00, [SAVE10, FREE5]) == 40.00`, and
`test_stacking_is_independent_of_cart_entry_order` asserts the same result
when the two codes are passed in the reverse order, closing off the
entry-order dependency that let this recur four times.

## 5. Final Deliverable Summary

Replaced the reset-from-`total` bug in `apply_discounts` with a canonical-order
compounding fix, deleted the three superseded one-off patches for previously
reported code pairs, and added three regression tests covering the reported
case, entry-order independence, and the three prior pairs. The SUPPORT-4821
customer's cart now totals $40.00 as expected, and the class of bug (not just
this one code pair) is closed.
