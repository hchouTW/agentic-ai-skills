---
role: Senior ML Systems Engineer
skill: deep-learning
use_case: diagnosing a NaN training loss that appears partway through a Transformer fine-tune run under automatic mixed precision
---

## Scenario

A team is fine-tuning a 12-layer Transformer encoder on a long-document
classification task under CUDA automatic mixed precision (`torch.autocast` +
`GradScaler`) to fit a larger batch on the same GPUs. Training looks healthy
for the first few hundred steps, then the loss prints `nan` at step 612 and
every step after it is `nan` as well, wasting the rest of the training budget.
The model uses a hand-written multi-head attention module (predating the
team's adoption of `torch.nn.functional.scaled_dot_product_attention`) instead
of a library attention op.

## Common Weak Approach

The on-call engineer sees `nan` in the loss log, assumes the optimizer stepped
too aggressively, and reacts by turning two generic dials without looking at
where the `nan` actually originates:

```python
import torch
from torch import nn

def train_step(model, batch, optimizer, scaler, criterion):
    optimizer.zero_grad()
    with torch.autocast("cuda", dtype=torch.float16):
        logits = model(batch["input_ids"], batch["attention_mask"])
        loss = criterion(logits, batch["labels"])

    scaler.scale(loss).backward()
    scaler.unscale_(optimizer)
    # "Fix" for the NaN at step 612: clip harder and drop the LR.
    torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=0.1)
    scaler.step(optimizer)
    scaler.update()
    return loss
```

```python
# lr dropped from 3e-4 to 5e-5 "to be safe", with no diagnosis of why step 612
# produced a NaN in the first place.
optimizer = torch.optim.AdamW(model.parameters(), lr=5e-5)
```

The run survives past step 612 this time, so the fix is declared successful and
merged. Three days later, a different fine-tune of the same model on a longer
sequence length NaNs again at a different step, because the actual defect - an
fp16 numeric overflow inside the attention module, described below - was never
found or fixed. The lower learning rate and tighter clip norm only made the bad
values slightly less likely to be reached, and only for this particular dataset
and sequence length; they did not remove the overflow.

## Expert-Level Best Practice

The engineer first localizes the failure instead of reacting to the printed
loss value. `GradScaler`'s own inf/NaN check is read from, rather than worked
around, and a backward hook is added at the module that is the leading suspect
(attention, since it is the one hand-written, non-library op in the model):

```python
import torch
from torch import nn


def train_step(model, batch, optimizer, scaler, criterion, step: int):
    optimizer.zero_grad()
    with torch.autocast("cuda", dtype=torch.float16):
        logits = model(batch["input_ids"], batch["attention_mask"])
        loss = criterion(logits, batch["labels"])

    if not torch.isfinite(loss):
        raise RuntimeError(f"non-finite loss at step {step}: {loss.item()!r}")

    scaler.scale(loss).backward()
    scaler.unscale_(optimizer)
    grad_norm = torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
    if not torch.isfinite(grad_norm):
        raise RuntimeError(f"non-finite grad norm at step {step}: {grad_norm.item()!r}")

    # scaler.step() silently skips the optimizer step (and scaler.update() backs
    # off the loss scale) when it finds inf/NaN in the unscaled gradients - the
    # *intended* mixed-precision safety net, not something to bypass by clipping
    # harder around it.
    scale_before = scaler.get_scale()
    scaler.step(optimizer)
    scaler.update()
    if scaler.get_scale() < scale_before:
        print(f"step {step}: GradScaler backed off scale to {scaler.get_scale()} "
              f"(an inf/NaN gradient was found and this optimizer step was skipped)")
    return loss
```

Running with `torch.autograd.set_detect_anomaly(True)` for a few steps around
the failure (debugging-only - it is slow) points at the manual softmax inside
the attention module's forward, not at the loss or the optimizer. Reading that
module's code shows why: it computes attention scores and a hand-rolled softmax
entirely under `autocast`'s default fp16 casting, instead of calling
`torch.nn.functional.softmax` (which `autocast`'s op-level policy keeps in
fp32 automatically):

```python
class WeakAttention(nn.Module):
    def forward(self, q, k, v, mask):
        scores = q @ k.transpose(-2, -1) / (q.size(-1) ** 0.5)   # fp16 under autocast
        scores = scores.masked_fill(mask == 0, float("-inf"))
        exp_scores = scores.exp()                                # can overflow fp16 (max ~65504)
        probs = exp_scores / exp_scores.sum(dim=-1, keepdim=True)
        return probs @ v
```

For a long document (this model's sequence length grew from 512 to 2048 in the
fine-tuning run that first triggered the NaN), unnormalized attention scores
from `q @ k.transpose(-2, -1)` easily exceed fp16's ~65504 max magnitude before
the softmax has a chance to normalize them, and `exp_scores.sum()` on a row that
already overflowed to `inf` produces `nan` on the very next divide. The fix
keeps the score computation and softmax in fp32 explicitly, which is the same
guarantee `F.softmax` gets for free under `autocast`'s built-in op policy, and
casts back to the surrounding dtype only after normalizing:

```python
class FixedAttention(nn.Module):
    def forward(self, q, k, v, mask):
        with torch.autocast("cuda", enabled=False):  # force fp32 for this block
            q32, k32, v32 = q.float(), k.float(), v.float()
            scores = q32 @ k32.transpose(-2, -1) / (q32.size(-1) ** 0.5)
            scores = scores.masked_fill(mask == 0, float("-inf"))
            probs = torch.softmax(scores, dim=-1)   # numerically stable, fp32
        return (probs @ v32).to(q.dtype)
```

With the attention fix in place, the run trains past step 612 and past the
longer-sequence run that reproduced the same failure, at the original learning
rate (`3e-4`) and clip norm (`1.0`) - confirming the learning rate and clip
norm were never the cause.

## Key Takeaways

- Localize the NaN to the operation that produced it before changing anything.
  `torch.autograd.set_detect_anomaly(True)` and a backward hook on the leading
  suspect module both point at the exact forward op; a learning-rate or
  clip-norm change changes how *likely* a numeric failure is to be hit, not
  whether the underlying operation can overflow.
- `autocast`'s fp32-for-numerically-sensitive-ops policy only covers the ops it
  knows about (`F.softmax`, `F.layer_norm`, reductions, and similar) - a
  hand-rolled softmax built from `.exp()` and `.sum()` bypasses that policy
  entirely and runs in fp16 like any other elementwise op, which is exactly
  where this defect hid.
- Treat `GradScaler`'s inf/NaN detection as the intended safety mechanism, not
  an obstacle to clip around harder. `scaler.step()` already skips the
  optimizer step and backs off the scale on a bad gradient; surfacing that
  event (as done above) turns a silent skipped step into a diagnostic signal
  instead of hiding it behind a smaller learning rate.
- A fix that only makes a specific run survive (lower LR, tighter clipping)
  without identifying the operation that overflowed is not verified - it is
  untested until a different sequence length, batch, or dataset exercises the
  same code path again. The expert fix is verified by reproducing the failure
  at a longer sequence length and confirming it no longer occurs at the
  *original* hyperparameters, not just the safer ones.
