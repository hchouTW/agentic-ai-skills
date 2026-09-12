---
role: test-driven Senior Experimental Particle Physicist
skill: hep-analysis
archetype: test-first
target: Selection-efficiency function must match a hand-computed reference within 1e-6
---

## 1. Acceptance Invariants & Boundary Constraints

`weighted_efficiency(pass_weights, total_weights)` must return `(e, sigma_e)`
for a weighted-event selection efficiency `e = A/B`, where `A` is the sum of
weights of passing events (a subset of the total sample) and `B` is the sum
of weights of all events. Per `references/04-histograms-efficiencies.md`'s
weighted-ratio guidance:

- `Var(e) ≈ Var(A)/B² + A²·Var(B)/B⁴ - 2A·Cov(A,B)/B³` (first-order error
  propagation), **not** the naive independent-variance formula that drops
  the covariance term - passing and total events share events, so treating
  them as independent is a real bug, not a simplification.
- `Cov(A,B)` is obtained from the passing sample's own `sumw2` under the
  "shared events" approximation the reference names, since every passing
  event also appears in the total.
- The function must match a hand-computed reference to within an absolute
  tolerance of `1e-6` on both `e` and `sigma_e`, for a concrete 5-event
  weighted dataset with `Var(A) = sumw2(passing) = 6`,
  `Var(B) = sumw2(total) = 11`, `Cov(A,B) = 6`, `A = 4`, `B = 7`.
- Boundary: signed or unusual weights are out of scope for this invariant -
  covered separately per the reference's "do not clip into probabilities" note.

## 2. Executable Failing Test (Red)

```python
# tests/test_weighted_efficiency.py
from fractions import Fraction
import math
from selection import weighted_efficiency

def test_weighted_efficiency_matches_hand_computed_reference():
    # 5 weighted MC events: (weight, pass_flag)
    events = [(1.0, True), (1.0, True), (1.0, False), (2.0, True), (2.0, False)]
    pass_weights = [w for w, p in events if p]
    total_weights = [w for w, _ in events]

    # Hand-computed reference (independent of the implementation under test):
    A = sum(pass_weights)                      # 4.0
    B = sum(total_weights)                     # 7.0
    var_A = sum(w * w for w in pass_weights)    # 6.0  (sumw2 of passing events)
    var_B = sum(w * w for w in total_weights)   # 11.0 (sumw2 of all events)
    cov_AB = var_A                              # shared-events approximation
    expected_e = float(Fraction(4, 7))
    expected_var_e = var_A / B**2 + A**2 * var_B / B**4 - 2 * A * cov_AB / B**3
    expected_sigma_e = math.sqrt(expected_var_e)

    e, sigma_e = weighted_efficiency(pass_weights, total_weights)

    assert abs(e - expected_e) < 1e-6, f"e={e}, expected={expected_e}"
    assert abs(sigma_e - expected_sigma_e) < 1e-6, \
        f"sigma_e={sigma_e}, expected={expected_sigma_e}"
```

Current `selection.weighted_efficiency` (naively treats `A` and `B` as
independent, dropping the covariance term):

```python
# selection.py (pre-fix)
def weighted_efficiency(pass_weights, total_weights):
    A = sum(pass_weights)
    B = sum(total_weights)
    var_A = sum(w * w for w in pass_weights)
    var_B = sum(w * w for w in total_weights)
    e = A / B
    var_e = var_A / B**2 + A**2 * var_B / B**4   # missing -2*A*Cov(A,B)/B**3
    return e, var_e ** 0.5
```

```
$ python3 -m pytest tests/test_weighted_efficiency.py -v
tests/test_weighted_efficiency.py::test_weighted_efficiency_matches_hand_computed_reference FAILED

================================== FAILURES ==================================
_____ test_weighted_efficiency_matches_hand_computed_reference _____
AssertionError: sigma_e=0.44243843650364895, expected=0.23624156944469848
assert abs(0.44243843650364895 - 0.23624156944469848) < 1e-6
1 failed in 0.02s
```

`e` passes (0.5714285714285714 matches), but `sigma_e` is off by roughly
0.206 - not a rounding error, a missing term.

## 3. Minimal Code Implementation

```python
# selection.py (fixed)
def weighted_efficiency(pass_weights, total_weights):
    A = sum(pass_weights)
    B = sum(total_weights)
    var_A = sum(w * w for w in pass_weights)
    var_B = sum(w * w for w in total_weights)
    cov_AB = var_A  # shared-events approximation: passing events' sumw2
    e = A / B
    var_e = var_A / B**2 + A**2 * var_B / B**4 - 2 * A * cov_AB / B**3
    return e, var_e ** 0.5
```

## 4. Verified Passing Execution (Green)

```
$ python3 -m pytest tests/test_weighted_efficiency.py -v
tests/test_weighted_efficiency.py::test_weighted_efficiency_matches_hand_computed_reference PASSED
1 passed in 0.02s
```

```python
>>> from selection import weighted_efficiency
>>> e, sigma_e = weighted_efficiency([1.0, 1.0, 2.0], [1.0, 1.0, 1.0, 2.0, 2.0])
>>> e, sigma_e
(0.5714285714285714, 0.23624156944469848)
>>> abs(sigma_e - 0.23624156944469848) < 1e-6
True
```

`sigma_e` (0.2362415694) matches the hand-computed reference to within
floating-point precision, well inside the required 1e-6 tolerance; the full
test suite runs in 0.02s.

## 5. Regression Guard Summary

This test guards against silently reverting to the independent-variance
formula (dropping the `-2A·Cov(A,B)/B³` term), which understates the true
correlation between passing and total counts and overstates the reported
uncertainty by roughly 87% in this dataset (0.4425 vs. the correct 0.2362) -
exactly the class of bug the "shared events" covariance note in
`references/04-histograms-efficiencies.md` warns about, and one that would
otherwise only surface as a subtly wrong error bar on a physics plot, not a
crash.
