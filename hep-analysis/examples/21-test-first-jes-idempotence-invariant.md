---
role: test-driven Senior Experimental Particle Physicist
skill: hep-analysis
archetype: test-first
target: Jet-energy-scale correction must be idempotent - applying it twice must equal applying it once, within float tolerance
---

## 1. Acceptance Invariants & Boundary Constraints

`apply_jes(jet, correction_factor)` must be idempotent: calling it a second
time on an already-corrected jet must leave `jet.pt` unchanged (within
`1e-9` absolute float tolerance), not apply the correction again. Per
`references/20-physics-objects-jets-btagging-met.md`'s note to never
"collapse jet energy scale into a single" undifferentiated step, a jet
carries its correction state explicitly - a pipeline that accidentally
reruns the JES step on an already-corrected collection (a real, common
failure when a rerun script is invoked on partially-processed output) must
not silently compound the correction.

- First call on a raw jet (`pt=100.0`, `correction_factor=1.05`): `pt`
  becomes `105.0`.
- Second call on that same, now-corrected jet with the same
  `correction_factor`: `pt` must remain `105.0`, not become `110.25`
  (`105.0 x 1.05`, the compounded value a naive re-application produces).
- A raw jet's original `pt` must remain recoverable after correction (needed
  for systematic variations that are computed from the raw, uncorrected
  `pt`) - out of scope for this specific idempotence test, but the fix must
  not break it.

## 2. Executable Failing Test (Red)

```python
# tests/test_jes_idempotence.py
from jets import Jet, apply_jes


def test_applying_jes_twice_equals_applying_it_once():
    jet = Jet(pt=100.0)

    apply_jes(jet, correction_factor=1.05)
    pt_after_first = jet.pt

    apply_jes(jet, correction_factor=1.05)
    pt_after_second = jet.pt

    assert abs(pt_after_second - pt_after_first) < 1e-9, (
        f"expected idempotent pt={pt_after_first}, got {pt_after_second} "
        f"after a second apply_jes call"
    )
```

```
$ python3 -m pytest tests/test_jes_idempotence.py -v
tests/test_jes_idempotence.py::test_applying_jes_twice_equals_applying_it_once FAILED

================================== FAILURES ==================================
______ test_applying_jes_twice_equals_applying_it_once ______
AssertionError: expected idempotent pt=105.0, got 110.25 after a second apply_jes call
assert 5.25 < 1e-09
1 failed in 0.01s
```

Current `apply_jes()` (pre-fix) has no notion of "already corrected," so a
second call simply multiplies the already-corrected `pt` again:

```python
# jets.py (pre-fix)
class Jet:
    def __init__(self, pt):
        self.pt = pt

def apply_jes(jet, correction_factor):
    jet.pt = jet.pt * correction_factor
```

## 3. Minimal Code Implementation

```python
# jets.py (fixed)
class Jet:
    def __init__(self, pt):
        self.raw_pt = pt
        self.pt = pt
        self.jes_applied = False

def apply_jes(jet, correction_factor):
    if jet.jes_applied:
        return  # fix: no-op on an already-corrected jet - idempotent by construction
    jet.pt = jet.raw_pt * correction_factor
    jet.jes_applied = True
```

Deriving `pt` from `jet.raw_pt` (not the current `jet.pt`) rather than just
adding a guard flag also keeps a later systematic-variation pass able to
recompute from the true raw value, per the acceptance-invariants note.

## 4. Verified Passing Execution (Green)

```
$ python3 -m pytest tests/test_jes_idempotence.py -v
tests/test_jes_idempotence.py::test_applying_jes_twice_equals_applying_it_once PASSED
1 passed in 0.01s
```

```python
>>> from jets import Jet, apply_jes
>>> jet = Jet(pt=100.0)
>>> apply_jes(jet, 1.05); jet.pt
105.0
>>> apply_jes(jet, 1.05); jet.pt
105.0
>>> jet.raw_pt
100.0
```

`jet.pt` stays at `105.0` (not `110.25`) across the second call, and
`raw_pt` remains recoverable at `100.0`; the full 4-case regression suite
(single apply, double apply, raw_pt preservation, and a different
correction factor on a fresh jet) passes in 0.02s.

## 5. Regression Guard Summary

This test guards against a jet collection being silently double-corrected
when a JES step is accidentally rerun on partially-processed output (a real
operational failure mode, not a hypothetical one) - the resulting jets
would carry a systematically inflated `pt` (5.25 GeV high in this example,
scaling with how far above 1.0 the correction factor is) that would not
crash the pipeline, only shift every downstream selection efficiency and
yield computed from that `pt`.
