---
role: Staff Software Engineer
skill: agile-development
use_case: scoping and reviewing a bug fix for a cart total that is wrong when a discount code is applied
---

## Scenario

A support ticket reports that a customer's cart total came out $1.00 too high:
a $49.99 subtotal with a `20OFF` percentage code stacked on a `FREE5SHIP` flat-rate
code should have charged $34.99, but the checkout page showed $35.99. The bug
tracker already has three closed tickets against the same `calculate_total`
function, each for a different pair of stacked promo codes, each "fixed" by a
one-off patch that never got a regression test. This is the fourth report on the
same code path in two months.

## Common Weak Approach

The on-call engineer reproduces the exact numbers from the ticket by hand,
confirms $35.99 instead of $34.99, and patches the function to special-case this
pair of codes so the reported numbers come out right:

```python
def calculate_total(subtotal: float, codes: list[str]) -> float:
    total = subtotal
    for code in codes:
        if code == "20OFF":
            total *= 0.8
        elif code == "10OFF":
            total *= 0.9
        elif code == "FREE5SHIP":
            total -= 5.0
        elif code == "FREESHIP":
            total -= 7.5

    # Fix for TICKET-4110: 20OFF + FREE5SHIP undercharges by $1 because the
    # flat discount was applied before the percentage discount in this one case.
    if set(codes) == {"20OFF", "FREE5SHIP"}:
        total = subtotal * 0.8 - 5.0

    return round(total, 2)
```

The commit message reads "fix cart total for 20OFF + FREE5SHIP (TICKET-4110)".
No test is added, because the engineer manually re-checked the one number from
the ticket and it now matches. The three earlier one-off patches for other code
pairs (not shown) are left in place, each with the same shape: a general loop
that applies discounts in whatever order they were entered, followed by a
special case that overrides the result for one specific combination once someone
complained about it.

## Expert-Level Best Practice

The engineer starts by writing a failing test that encodes the reported
combination *and* the three previously "fixed" combinations, before changing any
implementation code - this immediately exposes that the ordering, not any one
code pair, is the defect:

```python
import pytest
from decimal import Decimal
from cart import calculate_total, PercentDiscount, FlatDiscount

CASES = [
    # subtotal, discounts, expected total
    (Decimal("49.99"), [PercentDiscount(Decimal("20"))], Decimal("39.99")),
    (Decimal("49.99"), [FlatDiscount(Decimal("5"))], Decimal("44.99")),
    (Decimal("49.99"),
     [PercentDiscount(Decimal("20")), FlatDiscount(Decimal("5"))],
     Decimal("34.99")),  # TICKET-4110
    (Decimal("49.99"),
     [PercentDiscount(Decimal("10")), FlatDiscount(Decimal("7.50"))],
     Decimal("37.49")),  # TICKET-3987
    (Decimal("10.00"),
     [PercentDiscount(Decimal("20")), FlatDiscount(Decimal("20"))],
     Decimal("0.00")),  # discount must never push the total below zero
]


@pytest.mark.parametrize("subtotal,discounts,expected", CASES)
def test_calculate_total_matches_the_documented_contract(subtotal, discounts, expected):
    assert calculate_total(subtotal, discounts) == expected
```

Root cause: the function used `float` for money and applied discounts in
whatever order the caller's list happened to be in, with no stated rule for how
a percentage discount and a flat discount should compose. Sequential
multiplication also silently compounds percentage discounts instead of summing
them, and floats introduce rounding error across repeated multiplication -
neither of which is visible from a single hand-checked example. The fix replaces
the ad hoc loop with an explicit, ordered contract and exact decimal arithmetic:

```python
from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal


@dataclass(frozen=True)
class PercentDiscount:
    percent: Decimal


@dataclass(frozen=True)
class FlatDiscount:
    amount: Decimal


Discount = PercentDiscount | FlatDiscount


def calculate_total(subtotal: Decimal, discounts: list[Discount]) -> Decimal:
    """Apply the store's documented stacking contract:
    1. Sum all percentage discounts (capped at 100%) and apply the combined
       rate once, against the original subtotal.
    2. Subtract the sum of all flat discounts.
    3. Floor the result at zero.
    """
    percent_total = min(
        sum((d.percent for d in discounts if isinstance(d, PercentDiscount)),
            Decimal("0")),
        Decimal("100"),
    )
    flat_total = sum(
        (d.amount for d in discounts if isinstance(d, FlatDiscount)), Decimal("0")
    )

    after_percent = subtotal * (Decimal("100") - percent_total) / Decimal("100")
    total = after_percent - flat_total
    total = max(total, Decimal("0"))
    return total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
```

The three earlier one-off special cases for other code pairs are deleted in the
same change - they are now subsumed by the general contract, and leaving them
in place alongside it would mean two different, silently competing sources of
truth for the same calculation. The PR description states the contract in one
sentence ("percentage discounts stack additively off the original subtotal,
then flat discounts are subtracted, then the result floors at zero"), links all
four tickets as regression cases, and notes that callers must now construct
`PercentDiscount`/`FlatDiscount` values instead of passing raw string codes,
which is called out as the one intentionally breaking change in the diff.

## Key Takeaways

- Reproduce with a failing test before touching implementation code - and make
  that test cover the *pattern* in the bug report (every prior "fixed" code
  pair, plus a boundary case), not only the exact numbers from the ticket. A
  patch that only makes the reported numbers pass, without a test, reveals
  nothing about whether the same defect will resurface under the next
  combination.
- Find the contract, not the combination. The weak fix treated each report as a
  unique pair of codes needing its own branch; the expert fix recognized that no
  version of the code had ever stated a rule for how discounts compose, so every
  new combination was a new bug by construction. Stating and implementing that
  rule once closes the entire class of future tickets a fifth special case would
  not.
- Model money with `Decimal` and an explicit, typed representation
  (`PercentDiscount`/`FlatDiscount`) instead of `float` and string codes handled
  by a chain of `if`/`elif`. This is a correctness property, not a style
  preference: floats introduce rounding error across repeated multiplication,
  and string codes push the "what kind of discount is this" decision into every
  call site instead of the type system.
- Remove what the change orphaned. The three earlier special cases were made
  redundant by this fix, not merely stylistically inconsistent with it; leaving
  them in place would mean the codebase silently carries two different answers
  for the same input depending on which branch executes first. Deleting them is
  in scope for this change precisely because this change is what orphaned them.
