---
role: Senior ML Systems Engineer
skill: deep-learning
archetype: decision-tree
scenario: a training run whose loss isn't improving, with the specific failure mode not yet identified
---

## Triage Matrix

Formalizes `references/optimization-and-training-dynamics.md`'s "Training
failure classification" table and "Diagnostic flow" into a single triage
matrix, so the first response to "loss isn't improving" is a cheap
classification step rather than a guessed hyperparameter change:

| Trigger | Resolution Strategy |
|---|---|
| The model cannot overfit a tiny batch (8-32 examples, no augmentation) | Implementation failure - check loss wiring, label format vs. loss, and gradient flow (all intended parameters `requires_grad` and receiving nonzero gradient) before touching the learning rate |
| Tiny-batch overfit passes, but full-dataset train and validation loss fall together and plateau at a high value | Capacity failure - increase model size per `references/architecture-selection.md`'s sizing guidance, not the optimizer |
| Tiny-batch overfit passes, train loss falls on the full dataset, but validation loss stays flat or rises | Generalization failure - inspect leakage, data distribution, and regularization per `references/data-strategy.md`; the optimizer is doing its job, so do not touch LR/schedule first |
| Tiny-batch overfit passes, train loss falls on the full dataset, and the target metric does not improve even though loss does | Objective mismatch - check loss-vs-metric alignment per `references/evaluation-metrics.md` / `references/evaluation-strategy.md` |
| Loss was finite and improving, then abruptly becomes NaN/inf | Numerical failure - not a "won't improve" case at all; triage separately via the gradient/precision checks in this file's own gradient section and `references/debugging-pytorch.md` |

## Selected Branch

The reported case: tiny-batch overfit passes cleanly (loss reaches near-zero
on a 16-example batch within 200 steps); on the full dataset, training loss
falls steadily from 1.9 to 0.4 over 10 epochs, but validation loss falls from
1.9 to 1.1 and then rises back to 1.3 by epoch 10. This matches the third
row - generalization failure - directly, and rules out implementation and
capacity failure (both already excluded by the passing tiny-batch test).

## End-to-End Execution Script

1. Per `references/optimization-and-training-dynamics.md`'s explicit
   instruction for this branch ("do not assume optimization is broken; the
   optimizer is doing its job"), do not touch the learning rate or schedule
   first.
2. Check for leakage per `references/data-strategy.md`'s "Splits that
   survive contact with reality": confirm the split is genuinely i.i.d. or,
   if entities repeat (users, sessions, documents), confirm no entity
   appears in both train and validation.
3. Check whether any preprocessing statistic (normalization mean/std,
   vocabulary, imputation value) was fit on the full dataset rather than
   training data only - the "subtle, extremely common leak" that file names
   explicitly.
4. If no leakage is found, move to regularization and data distribution:
   compare the train and validation label distributions for drift, and check
   whether augmentation or weight decay were disabled for this run relative
   to a prior, better-generalizing run.
5. Apply whichever specific cause is confirmed (in this case: a
   normalization scaler was `fit()` on `train + val` concatenated, then
   `transform()`-ed separately - refit the scaler on training data only) and
   rerun the identical training configuration to confirm validation loss no
   longer rises.

## Fallback Safeguards

If leakage and regularization checks both come back clean and validation
loss still rises while training loss falls, do not conclude the branch was
correct and keep tuning regularization blindly - re-run the tiny-batch
overfit check first, since a subtly broken data pipeline (e.g., correct on a
tiny in-memory batch but wrong once the full `DataLoader` pipeline's
transforms are involved) can pass the first check and still produce
generalization-failure-shaped symptoms; if that re-check also passes cleanly,
re-triage against the objective-mismatch row instead, since a metric that
diverges from loss for reasons unrelated to overfitting can produce a
similar-looking validation curve.
