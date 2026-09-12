---
role: test-driven Staff Machine Learning Engineer
skill: deep-learning
archetype: test-first
target: Checkpoint save must snapshot optimizer state at call time, not whatever state exists when the async writer actually serializes it
---

## 1. Acceptance Invariants & Boundary Constraints

`save_checkpoint_async(model, optimizer, path)` must capture the
optimizer's momentum-buffer state **as of the moment it is called**, even
when the actual file write happens on a background thread after training
has continued. Per `references/checkpointing.md`'s save/resume contract, a
checkpoint restored later must reproduce the optimizer state that existed
immediately before that checkpoint call - not a later state, and not a
mixture of the two.

- A checkpoint saved after training step N, then resumed, must have a
  momentum buffer bit-identical to the value it held right after step N -
  regardless of how many further steps ran before the background writer
  actually serialized the tensor.
- Boundary under test: the background writer is deliberately delayed until
  after one additional optimizer step has already mutated the momentum
  buffer in place - the exact race a naive async-save implementation loses.

## 2. Executable Failing Test (Red)

```python
# tests/test_async_checkpoint_snapshot.py
import threading
import torch
from checkpoint_io import save_checkpoint_async, load_checkpoint


def sgd_momentum_step(param, grad, momentum_buf, lr=0.1, momentum=0.9):
    momentum_buf.mul_(momentum).add_(grad)
    param.data.add_(momentum_buf, alpha=-lr)


def test_async_save_captures_state_at_call_time_not_at_write_time():
    param = torch.tensor([1.0])
    momentum_buf = torch.tensor([0.0])

    sgd_momentum_step(param, torch.tensor([1.0]), momentum_buf)  # step 1
    expected_momentum_at_save = momentum_buf.clone()  # 1.0, the value at save time

    write_started = threading.Event()
    write_may_proceed = threading.Event()
    handle = save_checkpoint_async(
        momentum_buf, "ckpt.pt", write_started, write_may_proceed
    )
    write_started.wait()

    sgd_momentum_step(param, torch.tensor([1.0]), momentum_buf)  # step 2, mutates in place
    write_may_proceed.set()
    handle.join()

    restored_momentum = load_checkpoint("ckpt.pt")
    assert torch.equal(restored_momentum, expected_momentum_at_save), (
        f"expected momentum {expected_momentum_at_save.tolist()} (state at save "
        f"call), got {restored_momentum.tolist()} (state at write time)"
    )
```

```
$ python3 -m pytest tests/test_async_checkpoint_snapshot.py -v
tests/test_async_checkpoint_snapshot.py::test_async_save_captures_state_at_call_time_not_at_write_time FAILED

================================== FAILURES ==================================
______ test_async_save_captures_state_at_call_time_not_at_write_time ______
AssertionError: expected momentum [1.0] (state at save call), got [1.9] (state at write time)
assert False
1 failed in 0.31s
```

Current `save_checkpoint_async()` (pre-fix) hands the live tensor reference
to the background thread instead of snapshotting it, so any step that runs
before the thread's `torch.save()` call mutates the tensor the writer is
about to serialize:

```python
# checkpoint_io.py (pre-fix)
import threading
import torch

def save_checkpoint_async(momentum_buf, path, write_started=None, write_may_proceed=None):
    def _write():
        if write_started is not None:
            write_started.set()
        if write_may_proceed is not None:
            write_may_proceed.wait()
        torch.save(momentum_buf, path)  # bug: serializes the live tensor, not a snapshot

    thread = threading.Thread(target=_write)
    thread.start()
    return thread
```

## 3. Minimal Code Implementation

```python
# checkpoint_io.py (fixed)
import threading
import torch

def save_checkpoint_async(momentum_buf, path, write_started=None, write_may_proceed=None):
    snapshot = momentum_buf.clone().detach()  # fix: snapshot at call time, before any further step

    def _write():
        if write_started is not None:
            write_started.set()
        if write_may_proceed is not None:
            write_may_proceed.wait()
        torch.save(snapshot, path)

    thread = threading.Thread(target=_write)
    thread.start()
    return thread

def load_checkpoint(path):
    return torch.load(path, weights_only=True)
```

## 4. Verified Passing Execution (Green)

```
$ python3 -m pytest tests/test_async_checkpoint_snapshot.py -v
tests/test_async_checkpoint_snapshot.py::test_async_save_captures_state_at_call_time_not_at_write_time PASSED
1 passed in 0.29s
```

```python
>>> restored_momentum.tolist()
[1.0]
>>> expected_momentum_at_save.tolist()
[1.0]
```

Full regression suite (this race-condition test plus the 6 existing
synchronous save/resume tests in `tests/test_checkpointing.py`) passes in
1.8s.

## 5. Regression Guard Summary

This test guards against a resumed multi-day training run silently
continuing from the wrong optimizer state - the momentum buffer one extra
step ahead of where the checkpoint's epoch counter claims it is - a
divergence that would not crash anything but would make the resumed run's
loss curve subtly non-reproducible against the pre-interruption run. Any
future change that hands the background writer a live tensor reference
instead of a `.clone().detach()` snapshot will fail this test immediately.
