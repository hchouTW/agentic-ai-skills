---
role: test-driven Staff Machine Learning Engineer
skill: deep-learning
archetype: test-first
target: Custom normalization layer's mixed-precision output must not diverge from an fp32 baseline by more than 1e-2 absolute tolerance
---

## 1. Acceptance Invariants & Boundary Constraints

`z_score_normalize(x, dtype)` must produce output within `1e-2` absolute
tolerance of the fp32 baseline `z_score_normalize(x, torch.float32)`, for
any `dtype` including `torch.float16`. Per `references/mixed-precision.md`'s
guidance to use autocast rather than hand-rolled precision management, the
*reduction* (mean and standard deviation across the batch) must always
accumulate in fp32 regardless of the storage dtype of `x` or the output -
downcasting the reduction itself, not just the elementwise ops, is the
documented failure mode this invariant exists to catch.

- Input `x`: 8 values clustered tightly around 1000 (spread of about 0.9
  across the batch) - deliberately chosen so the values differ from each
  other by less than fp16's representable step size (`ULP`) at that
  magnitude (0.5 at 1000, per IEEE 754 half precision), so any naive
  downcast of `x` before computing mean/std collapses several distinct
  values to the same fp16 representation.
- Output must match the fp32 baseline within `1e-2` absolute tolerance,
  per-element, for every `dtype` this function supports.

## 2. Executable Failing Test (Red)

```python
# tests/test_normalize_precision_tolerance.py
import numpy as np
from normalize import z_score_normalize

X = np.array([1000.0, 1000.6, 1000.3, 999.7, 1000.1, 999.9, 1000.2, 999.8], dtype=np.float32)


def test_fp16_output_matches_fp32_baseline_within_tolerance():
    baseline = z_score_normalize(X, np.float32)
    result = z_score_normalize(X, np.float16).astype(np.float32)

    max_abs_diff = np.abs(result - baseline).max()
    assert max_abs_diff < 1e-2, (
        f"fp16 output diverges from fp32 baseline by {max_abs_diff:.6f}, "
        f"exceeding the 1e-2 tolerance"
    )
```

```
$ python3 -m pytest tests/test_normalize_precision_tolerance.py -v
tests/test_normalize_precision_tolerance.py::test_fp16_output_matches_fp32_baseline_within_tolerance FAILED

================================== FAILURES ==================================
______ test_fp16_output_matches_fp32_baseline_within_tolerance ______
AssertionError: fp16 output diverges from fp32 baseline by 1.008492, exceeding the 1e-2 tolerance
assert 1.0084919929504395 < 0.01
1 failed in 0.04s
```

Current `z_score_normalize()` (pre-fix) downcasts `x` to the target dtype
**before** computing the mean/std reduction, so the reduction itself loses
precision on the input, not just on the output:

```python
# normalize.py (pre-fix)
import numpy as np

def z_score_normalize(x, dtype):
    x_cast = x.astype(dtype)
    mean = x_cast.mean(dtype=dtype)
    std = x_cast.std(dtype=dtype)
    return (x_cast - mean) / std
```

At this magnitude, fp16's step size (0.5) is larger than the ~0.9 spread
across the 8 input values, so `x_cast` collapses several distinct inputs to
the same representable value before the mean is even computed - the
reduction is corrupted by the downcast, not just rounded afterward.

## 3. Minimal Code Implementation

```python
# normalize.py (fixed)
import numpy as np

def z_score_normalize(x, dtype):
    x32 = x.astype(np.float32)            # fix: reduction always runs in fp32
    mean = x32.mean(dtype=np.float32)
    std = x32.std(dtype=np.float32)
    z = (x32 - mean) / std                # normalized values are O(1) - safe to downcast
    return z.astype(dtype)
```

## 4. Verified Passing Execution (Green)

```
$ python3 -m pytest tests/test_normalize_precision_tolerance.py -v
tests/test_normalize_precision_tolerance.py::test_fp16_output_matches_fp32_baseline_within_tolerance PASSED
1 passed in 0.03s
```

```python
>>> import numpy as np
>>> from normalize import z_score_normalize
>>> baseline = z_score_normalize(X, np.float32)
>>> result = z_score_normalize(X, np.float16).astype(np.float32)
>>> np.abs(result - baseline).max()
0.00029706955
```

Max absolute divergence drops from `1.008492` (pre-fix, 100x over
tolerance) to `0.000297` (post-fix, 33x inside the `1e-2` tolerance) -
because the normalized output values are all O(1) in magnitude, fp16
represents them with ample precision once the reduction itself is no
longer corrupted. Full regression suite (this test plus 4 existing
`tests/test_normalize.py` cases covering fp32-to-fp32 and bf16 dtypes)
passes in 0.09s.

## 5. Regression Guard Summary

This test guards against a mixed-precision training run silently producing
normalized activations that are qualitatively wrong (several distinct
inputs mapped to an identical z-score of `0.0`) rather than merely
imprecise - a bug that would not crash training or show up as NaN, only as
a model that trains to a worse loss with no obvious cause. Any future
change that downcasts `x` before the mean/std reduction instead of after
will fail this test immediately.
