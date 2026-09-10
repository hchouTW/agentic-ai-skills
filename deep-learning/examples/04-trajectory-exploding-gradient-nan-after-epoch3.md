---
role: Senior ML Systems Engineer
skill: deep-learning
archetype: trajectory
problem_input: a training run whose loss is finite through the first three epochs and then turns to nan at the start of epoch 4, with no code changes between epochs
---

## 1. Task Input & Context

Training log excerpt, as received from the team running the job:

```
epoch 1  step 1400  loss 2.184
epoch 2  step 2800  loss 1.607
epoch 3  step 4200  loss 1.312
epoch 4  step 4201  loss nan
epoch 4  step 4202  loss nan
```

The model is a 2-layer LSTM sequence tagger (no attention, no mixed
precision - plain fp32) trained with `torch.optim.AdamW` at a fixed learning
rate of `3e-4` and no gradient clipping configured. Nothing in the training
script changed between epoch 3 and epoch 4; the same optimizer state and data
pipeline carried over across the epoch boundary.

## 2. Root-Cause Triage & Action Plan

Per `references/debugging-pytorch.md`'s NaN checklist, the inputs and the loss
were asserted finite at the start of the failing step:

```python
assert torch.isfinite(batch["inputs"]).all()   # passes - inputs are fine
loss = criterion(model(batch["inputs"]), batch["labels"])
assert torch.isfinite(loss).all()              # fails at epoch 4, step 4201
```

The input is finite but the loss is not, so the defect is inside the forward/
backward path, not the data. Per
`references/optimization-and-training-dynamics.md`'s "Vanishing and exploding
gradients" guidance to localize with a backward hook rather than guess from
the aggregate loss curve, a hook was attached to each LSTM layer:

```python
def make_grad_norm_hook(name):
    def hook(module, grad_input, grad_output):
        norm = grad_output[0].norm().item()
        print(f"{name}: grad_output norm = {norm:.2f}")
    return hook

model.lstm.layers[0].register_full_backward_hook(make_grad_norm_hook("lstm[0]"))
model.lstm.layers[1].register_full_backward_hook(make_grad_norm_hook("lstm[1]"))
```

The hook output shows `lstm[1]`'s gradient norm growing steadily across
training - `340` at epoch 1, `2,900` at epoch 2, `41,000` at epoch 3, then
`inf` at the first step of epoch 4 - rather than appearing suddenly. This
matches `references/optimization-and-training-dynamics.md`'s note that
recurrent architectures are more exposed to exploding gradients than
attention/feed-forward stacks, and that the fix for a gradual blow-up like
this one is clipping and warmup, not a further learning-rate cut after the
fact (which would only delay the same explosion to a later epoch).

Action plan: add `torch.nn.utils.clip_grad_norm_` before the optimizer step,
add a short linear learning-rate warmup over the first 500 steps so the
optimizer isn't taking full-sized steps while the recurrent weights are still
in their highest-curvature region, and verify by rerunning the exact same run
past epoch 4 with gradient-norm logging left in place.

## 3. Surgical Execution

```diff
+from torch.optim.lr_scheduler import LambdaLR
+
+WARMUP_STEPS = 500
+
+def warmup_lr(step: int) -> float:
+    return min(1.0, (step + 1) / WARMUP_STEPS)
+
 optimizer = torch.optim.AdamW(model.parameters(), lr=3e-4)
+scheduler = LambdaLR(optimizer, lr_lambda=warmup_lr)

 for step, batch in enumerate(loader):
     optimizer.zero_grad()
     loss = criterion(model(batch["inputs"]), batch["labels"])
     loss.backward()
-    optimizer.step()
+    grad_norm = torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=5.0).item()
+    optimizer.step()
+    scheduler.step()
+    if step % 200 == 0:
+        print(f"step {step}: grad_norm={grad_norm:.2f} lr={scheduler.get_last_lr()[0]:.2e}")
```

## 4. Verification Evidence

```
$ python3 train.py --resume-from checkpoints/epoch3.pt --epochs 6
epoch 3  step 4200  loss 1.312  grad_norm 3.98  lr 3.00e-04
epoch 4  step 4400  loss 1.201  grad_norm 4.61  lr 3.00e-04
epoch 4  step 4600  loss 1.144  grad_norm 4.87  lr 3.00e-04
epoch 5  step 5800  loss 0.983  grad_norm 4.72  lr 3.00e-04
epoch 6  step 7000  loss 0.891  grad_norm 4.55  lr 3.00e-04
$ python3 -m pytest tests/test_training_stability.py -k epoch3_to_epoch4 -v
tests/test_training_stability.py::test_no_nan_loss_across_epoch3_to_epoch4_boundary PASSED
1 passed in 4.31s
```

The gradient norm, which had grown unbounded to `inf` at epoch 4 before the
fix, now stays bounded near `5.0` (the clip threshold) for the rest of
training, and the run completes all 6 epochs with a finite, decreasing loss.

## 5. Final Deliverable Summary

Localized an exploding-gradient NaN in a 2-layer LSTM tagger to the second
recurrent layer, whose gradient norm grew across three full epochs before
overflowing rather than failing suddenly. Added gradient-norm clipping
(`max_norm=5.0`) and a 500-step linear learning-rate warmup, and added a
regression test that resumes training from the epoch-3 checkpoint and asserts
no NaN loss occurs crossing into epoch 4. The original learning rate (`3e-4`)
was kept; only clipping and warmup were added, confirming those two changes -
not a lower learning rate - were what the fix needed.
