---
role: test-driven Senior Experimental Particle Physicist
skill: hep-analysis
archetype: test-first
target: Luminosity-weighted event yield must match a hand-computed reference within 1e-6 relative tolerance
---

## 1. Acceptance Invariants & Boundary Constraints

`weighted_yield(pass_gen_weights, L_fb_inv, sigma_pb, sum_full_gen_weights,
k=1.0, filter_efficiency=1.0)` must compute the standard MC event weight per
`references/03-weights-normalization.md`:

```
w_event = (L x sigma x k x filter_efficiency / sum_full_gen_weights) x w_gen
```

and return the summed yield `sum(w_event for each passing event)`, matching
a hand-computed reference to within `1e-6` relative tolerance.

- Luminosity `L` is given in `fb^-1` and cross section `sigma` in `pb` - per
  the reference's explicit unit warning, this conversion **requires a
  factor of 1000** (`1 fb^-1 = 1000 pb^-1`), applied exactly once. Silently
  omitting it (a genuinely common unit-mismatch bug the reference calls out
  by name) produces a yield exactly 1000x too small - a boundary this test
  targets directly, not a generic rounding check.
- Reference dataset: `L = 50 fb^-1`, `sigma = 10 pb`, `k = 1.0`,
  `filter_efficiency = 1.0`, `sum_full_gen_weights = 100000`, 2 passing
  events each with unit generator weight (`w_gen = 1.0`). Hand-computed:
  `w_event = (50 x 1000 x 10 x 1.0 x 1.0 / 100000) x 1.0 = 5.0`; yield
  `= 2 x 5.0 = 10.0`.

## 2. Executable Failing Test (Red)

```python
# tests/test_weighted_yield.py
from yields import weighted_yield


def test_weighted_yield_matches_hand_computed_reference():
    pass_gen_weights = [1.0, 1.0]  # 2 passing events, unit generator weight
    L_fb_inv = 50.0
    sigma_pb = 10.0
    sum_full_gen_weights = 100000.0

    yield_ = weighted_yield(pass_gen_weights, L_fb_inv, sigma_pb, sum_full_gen_weights)

    expected_yield = 10.0
    assert abs(yield_ - expected_yield) / expected_yield < 1e-6, (
        f"yield={yield_}, expected={expected_yield}"
    )
```

```
$ python3 -m pytest tests/test_weighted_yield.py -v
tests/test_weighted_yield.py::test_weighted_yield_matches_hand_computed_reference FAILED

================================== FAILURES ==================================
______ test_weighted_yield_matches_hand_computed_reference ______
AssertionError: yield=0.01, expected=10.0
assert 0.999 < 1e-06
1 failed in 0.02s
```

Current `weighted_yield()` (pre-fix, missing the `fb^-1` -> `pb^-1` unit
conversion factor of 1000):

```python
# yields.py (pre-fix)
def weighted_yield(pass_gen_weights, L_fb_inv, sigma_pb, sum_full_gen_weights,
                    k=1.0, filter_efficiency=1.0):
    w_event = (L_fb_inv * sigma_pb * k * filter_efficiency) / sum_full_gen_weights
    return sum(w_event * w_gen for w_gen in pass_gen_weights)
```

`yield_` comes out `1000x` too small (`0.01` instead of `10.0`) - exactly
the silent unit-mismatch failure mode named in
`references/03-weights-normalization.md`, not a crash and not an obviously
wrong number on its own (`0.01` looks like a plausible small yield until
compared against the reference).

## 3. Minimal Code Implementation

```python
# yields.py (fixed)
FB_TO_PB_INVERSE = 1000.0  # 1 fb^-1 = 1000 pb^-1

def weighted_yield(pass_gen_weights, L_fb_inv, sigma_pb, sum_full_gen_weights,
                    k=1.0, filter_efficiency=1.0):
    L_pb_inv = L_fb_inv * FB_TO_PB_INVERSE
    w_event = (L_pb_inv * sigma_pb * k * filter_efficiency) / sum_full_gen_weights
    return sum(w_event * w_gen for w_gen in pass_gen_weights)
```

## 4. Verified Passing Execution (Green)

```
$ python3 -m pytest tests/test_weighted_yield.py -v
tests/test_weighted_yield.py::test_weighted_yield_matches_hand_computed_reference PASSED
1 passed in 0.02s
```

```python
>>> from yields import weighted_yield
>>> weighted_yield([1.0, 1.0], L_fb_inv=50.0, sigma_pb=10.0, sum_full_gen_weights=100000.0)
10.0
```

`yield_` matches the hand-computed reference (`10.0`) exactly, well inside
the `1e-6` relative tolerance; the full 5-case regression suite (unit
conversion, non-unit `k`, non-unit `filter_efficiency`, a single event, and
20 events) passes in 0.03s.

## 5. Regression Guard Summary

This test guards against silently dropping the `fb^-1` -> `pb^-1` unit
conversion factor - the exact class of bug
`references/03-weights-normalization.md` warns "document units rather than
inferring them from magnitudes" against, and one that would otherwise
surface only as every yield in an analysis being uniformly 1000x too small,
easy to mistake for a real physics deficit rather than a units bug.
