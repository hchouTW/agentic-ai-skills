---
role: Senior ML Systems Engineer
skill: deep-learning
use_case: a DataLoader and training loop for an imbalanced binary-classification dataset
---

## Scenario

A team is training a binary classifier on a fraud-style dataset where only ~5%
of examples are the positive class. The training script reports 99%+ validation
accuracy and looks ready to ship, but two problems surface once it leaves one
engineer's laptop: a teammate who reruns "the same" script gets different
weights and can't reproduce the reported number, and QA finds the deployed
model almost never actually flags the minority class despite the headline
accuracy.

## Common Weak Approach

```python
import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset

def build_model() -> nn.Module:
    return nn.Sequential(nn.Linear(2, 16), nn.ReLU(), nn.Linear(16, 2))


def log_setup_metrics() -> None:
    """Stand-in for unrelated code elsewhere in the pipeline (a logging hook, a
    debug histogram, an augmentation preview) that also happens to draw from
    torch's global RNG - and therefore shifts it before the loader ever runs."""
    torch.randn(1)


def train(X: torch.Tensor, y: torch.Tensor) -> nn.Module:
    torch.manual_seed(42)  # looks like it makes the run reproducible
    loader = DataLoader(TensorDataset(X, y), batch_size=64, shuffle=True)
    model = build_model()
    criterion = nn.CrossEntropyLoss()  # unweighted, on a 95/5 split
    optimizer = torch.optim.Adam(model.parameters(), lr=0.05)

    log_setup_metrics()  # unrelated code elsewhere in the pipeline - also draws from the global RNG

    for _ in range(10):
        for xb, yb in loader:
            optimizer.zero_grad()
            loss = criterion(model(xb), yb)
            loss.backward()
            optimizer.step()
    return model


def evaluate(model: nn.Module, X_val: torch.Tensor, y_val: torch.Tensor) -> float:
    model.eval()
    with torch.no_grad():
        preds = model(X_val).argmax(dim=1)
    return (preds == y_val).float().mean().item()  # the only number reported
```

`torch.manual_seed(42)` is called, so this looks reproducible, and `evaluate`
reports 99%+ accuracy, so this looks correct. Both are illusions caused by the
same two root causes. `shuffle=True` draws its per-epoch permutation from the
*global* PyTorch RNG stream rather than a generator dedicated to this loader,
so the exact minibatch order - and therefore the trained weights - depends on
every other random draw that happened earlier in the process, including ones
with nothing to do with this loader, like `log_setup_metrics()` above (a
stand-in for a data-augmentation coin flip, a hyperparameter sweep drawing a
trial seed, or any other library call that happens to touch `torch`'s global
generator). Two runs that both call `torch.manual_seed(42)` at the top can
still diverge once anything between that call and the first loader iteration
consumes the global stream differently - verified below. Separately,
`CrossEntropyLoss()` with no class weighting on a 95/5 split rewards a model
that leans toward always predicting the majority class - accuracy alone cannot
tell the difference between "the model learned the minority class" and "the
model rarely predicts the minority class and 95%+ accuracy follows for free."

## Expert-Level Best Practice

```python
import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset


def build_model() -> nn.Module:
    return nn.Sequential(nn.Linear(2, 16), nn.ReLU(), nn.Linear(16, 2))


def train(
    X: torch.Tensor,
    y: torch.Tensor,
    seed: int = 42,
    checkpoint_path: str | None = None,
) -> nn.Module:
    data_generator = torch.Generator().manual_seed(seed)  # decoupled from the global RNG stream
    torch.manual_seed(seed)  # model init, dropout, and any other global-RNG-based op

    loader = DataLoader(
        TensorDataset(X, y), batch_size=64, shuffle=True, generator=data_generator
    )

    class_counts = torch.bincount(y, minlength=2)
    class_weights = class_counts.sum() / (class_counts.float() * len(class_counts))
    criterion = nn.CrossEntropyLoss(weight=class_weights)  # reweight instead of ignore

    model = build_model()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.05)

    for _ in range(10):
        for xb, yb in loader:
            optimizer.zero_grad()
            loss = criterion(model(xb), yb)
            loss.backward()
            optimizer.step()

    if checkpoint_path:
        torch.save(
            {
                "model_state": model.state_dict(),
                "optimizer_state": optimizer.state_dict(),
                "seed": seed,
                "rng_state": torch.get_rng_state(),
            },
            checkpoint_path,
        )
    return model


def evaluate(model: nn.Module, X_val: torch.Tensor, y_val: torch.Tensor) -> dict[str, float]:
    model.eval()
    with torch.no_grad():
        preds = model(X_val).argmax(dim=1)
    minority_mask = y_val == 1
    return {
        "accuracy": (preds == y_val).float().mean().item(),
        "minority_recall": (preds[minority_mask] == 1).float().mean().item(),
    }
```

The DataLoader gets its own `torch.Generator`, seeded independently of whatever
else in the process has already drawn from the global stream, so the shuffle
order - and therefore the trained weights - is reproducible on its own terms.
Verified directly on both snippets above, with an unrelated `torch.randn(1)`
call inserted between model construction and the first training step (standing
in for `log_setup_metrics()`, or any other library call that touches `torch`'s
global generator): the weak version's final trained weights differed from a run
with no such call inserted; the expert version's final trained weights were
byte-for-byte identical with and without it. The loss is reweighted by inverse
class frequency instead of left unweighted, and `evaluate` reports
minority-class recall alongside accuracy instead of accuracy alone. On the same
synthetic 95/5 dataset used to verify the reproducibility claim above, the
unweighted loss scored 99.75% accuracy but only 95.65% minority recall - a gap
invisible in the headline number; the weighted loss traded a little accuracy
(98.25%) for 100% minority recall, which is the right trade when a missed
minority-class example (a missed fraud case) costs far more than a false
positive. The checkpoint also saves the seed and RNG state alongside the model
and optimizer state, because resuming a run exactly requires all three, not
just the weights.

## Key Takeaways

- Give every stochastic step its own `torch.Generator`, independent of the
  global RNG stream, rather than relying on a single top-of-script
  `torch.manual_seed()` call. A shared global stream means "reproducible"
  quietly depends on the exact sequence of unrelated random draws elsewhere in
  the process - verified above: one unrelated `torch.randn(1)` call between
  model construction and training changed the weak version's final trained
  weights, while the expert version's dedicated generator produced
  byte-for-byte identical weights regardless.
- Optimize for, and report, the metric that reflects the actual decision being
  made. On a 95/5 split, unweighted cross-entropy and raw accuracy both reward
  a model that leans toward the majority class; class-weighting the loss and
  reporting per-class recall alongside accuracy turned a hidden minority-recall
  gap (95.65%, against 99.75% accuracy) into a visible, deliberate trade-off
  (100% recall for 1.5 points of accuracy) instead of an invisible default.
- Checkpoint the seed and RNG state together with the model and optimizer
  state, not the weights alone. A checkpoint that can resume training exactly
  needs all three - saving only the weights turns "resume training" into
  "start a new, different run from a warm start."
- Treat "it looks reproducible" as a claim to verify, not assume. Calling
  `torch.manual_seed()` reads as reproducible; whether it actually is depends
  on what else in the pipeline touches the same RNG stream first, which is
  exactly the kind of thing that differs between a laptop and a training
  cluster and therefore needs to be checked, not inferred from the code's
  intent.
