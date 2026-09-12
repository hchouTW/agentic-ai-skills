---
role: ruthless Staff ML Engineer / Red-Teamer
skill: deep-learning
archetype: adversarial-audit
candidate_artifact: a training writeup claiming 95% accuracy, SOTA, with a training script
---

## 1. Initial Candidate Artifact

Writeup submitted to the model-review channel by the applied-science team,
requesting sign-off to promote the checkpoint to the model registry:

> **Pneumonia detector v3 - SOTA result, ready to ship**
>
> We retrained the chest X-ray pneumonia classifier (ResNet-18 backbone,
> binary output) on the refreshed 18,432-image dataset. Test accuracy: **95.1%**,
> beating the published baseline of 91.4% and our own v2 production model's
> 89.7%. This is a new SOTA for this dataset. Training script attached below;
> checkpoint `pneumonia_v3_seed42.pt` is in the artifact store.

```python
import torch
from torch.utils.data import DataLoader, random_split
from torchvision import transforms, datasets, models

def compute_mean_std(dataset):
    loader = DataLoader(dataset, batch_size=256, shuffle=False, num_workers=4)
    mean = torch.zeros(3)
    sq = torch.zeros(3)
    n = 0
    for x, _ in loader:
        b = x.size(0)
        mean += x.mean(dim=[0, 2, 3]) * b
        sq += (x ** 2).mean(dim=[0, 2, 3]) * b
        n += b
    mean /= n
    std = (sq / n - mean ** 2).sqrt()
    return mean, std

raw = datasets.ImageFolder("data/chest_xray_all", transform=transforms.ToTensor())
mean, std = compute_mean_std(raw)  # fit on the FULL 18,432-image pool

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean.tolist(), std.tolist()),
])
full_ds = datasets.ImageFolder("data/chest_xray_all", transform=transform)

torch.manual_seed(42)
n_train = int(0.8 * len(full_ds))
n_test = len(full_ds) - n_train
train_ds, test_ds = random_split(
    full_ds, [n_train, n_test], generator=torch.Generator().manual_seed(42)
)

model = models.resnet18(num_classes=1)
optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)
criterion = torch.nn.BCEWithLogitsLoss()

train_loader = DataLoader(train_ds, batch_size=32, shuffle=True)
test_loader = DataLoader(test_ds, batch_size=32, shuffle=False)

for epoch in range(15):
    model.train()
    for x, y in train_loader:
        optimizer.zero_grad(set_to_none=True)
        loss = criterion(model(x).squeeze(1), y.float())
        loss.backward()
        optimizer.step()

model.eval()
correct, total = 0, 0
with torch.no_grad():
    for x, y in test_loader:
        pred = (torch.sigmoid(model(x).squeeze(1)) > 0.5).long()
        correct += (pred == y).sum().item()
        total += y.size(0)
print(f"test accuracy: {correct / total:.3f}")  # 0.951
```

The writeup includes one run, one seed (`42`), and no reported variance.

## 2. Attack Vectors & Stress-Tests

**Attack Vector 1: normalization statistics fit on the full pool before the
split (train/test contamination).** `compute_mean_std` runs over `raw`, an
`ImageFolder` built from `data/chest_xray_all` with *no* train/test
partitioning applied yet - it is the entire 18,432-image pool, test images
included. The resulting `mean`/`std` are then baked into the `transform` used
to build `full_ds`, which is only split into `train_ds`/`test_ds` *after* that
transform is already fixed. Per `references/reproducibility.md`'s "Data
splits" guidance, a split must be performed before any dataset-derived
statistic is computed downstream of it; here the model's normalization layer
has already seen a summary statistic of every test image before a single
training step runs. This is not the "genuinely i.i.d., random split is
correct" case from the leakage taxonomy - it is a direct, if subtle, dataset
contamination bug: information from the test partition (its pixel mean/std)
is present in the number every single training example gets divided by.

**Attack Vector 2: a single seed, cherry-picked, with zero variance
reporting, dressed up as "SOTA."** The script hard-codes `torch.manual_seed(42)`
for both the split and training, runs exactly once, and the writeup reports
that one number as *the* result. `references/reproducibility.md`'s
"Reproducing across seeds" level requires "running multiple seeds and
reporting the spread" before a comparative claim is credible, and its
"Hyperparameter sweeps" section is blunt about the mechanism: "a single held-out
validation split reused... is itself a form of overfitting." A 3.7-point
margin over the v2 baseline (95.1% vs. 89.7% - which itself was presumably
also a single-seed number) is well within the run-to-run noise band that a
5-image-flip difference on an ~3,700-image test split can produce; nothing in
the artifact rules out "we got a lucky seed" as the entire explanation for the
"SOTA" claim, and Attack Vector 1 means the lucky number is inflated on top of
that.

## 3. Concrete Counter-Example / Exploit Proof

Re-running the *identical* script with the only change being that normalization
statistics are computed on the train split alone (post-split, the way
`reproducibility.md` and `data-loading.md`'s "Reproducible split" section both
require) shows how much of the 95.1% was contamination:

```python
# leak_repro.py - same script, mean/std now fit AFTER the split, on train_ds only
import torch
from torch.utils.data import DataLoader, random_split
from torchvision import transforms, datasets, models

raw = datasets.ImageFolder("data/chest_xray_all", transform=transforms.ToTensor())
torch.manual_seed(42)
n_train = int(0.8 * len(raw))
n_test = len(raw) - n_train
train_idx_ds, test_idx_ds = random_split(
    raw, [n_train, n_test], generator=torch.Generator().manual_seed(42)
)

def compute_mean_std(subset):
    loader = DataLoader(subset, batch_size=256, shuffle=False, num_workers=4)
    mean, sq, n = torch.zeros(3), torch.zeros(3), 0
    for x, _ in loader:
        b = x.size(0)
        mean += x.mean(dim=[0, 2, 3]) * b
        sq += (x ** 2).mean(dim=[0, 2, 3]) * b
        n += b
    mean /= n
    return mean, (sq / n - mean ** 2).sqrt()

mean, std = compute_mean_std(train_idx_ds)  # TRAIN SPLIT ONLY, computed after the split
print("train-only mean/std:", mean.tolist(), std.tolist())
print("full-pool mean/std (original script):", [0.4831, 0.4831, 0.4831], [0.2367, 0.2367, 0.2367])
```

```
$ python3 leak_repro.py
train-only mean/std: [0.4809, 0.4809, 0.4809] [0.2401, 0.2401, 0.2401]
full-pool mean/std (original script): [0.4831, 0.4831, 0.4831] [0.2367, 0.2367, 0.2367]

$ python3 train_with_fixed_stats.py --seed 42     # identical model/training, corrected stats
epoch 15  test_accuracy 0.887

$ python3 train_with_fixed_stats.py --seed 7
epoch 15  test_accuracy 0.891

$ python3 train_with_fixed_stats.py --seed 123
epoch 15  test_accuracy 0.879

$ python3 train_with_fixed_stats.py --seed 2024
epoch 15  test_accuracy 0.895

$ python3 train_with_fixed_stats.py --seed 31337
epoch 15  test_accuracy 0.883
```

Fixing only the leakage drops the headline number from 95.1% to 88.7% on the
original seed (42) - a 6.4-point swing from a bug that never touches the
model or the optimizer, only which images the normalization constant is
allowed to see. Running the corrected pipeline across five seeds gives
87.9%-89.5% (mean 88.7%, std 0.6 points), which sits *below* the v2 production
baseline of 89.7%, not above it. The "SOTA" claim does not survive either
attack vector in isolation, let alone both together.

## 4. Hardened Architectural Patch

```diff
-def compute_mean_std(dataset):
-    loader = DataLoader(dataset, batch_size=256, shuffle=False, num_workers=4)
-    mean = torch.zeros(3)
-    sq = torch.zeros(3)
-    n = 0
-    for x, _ in loader:
-        b = x.size(0)
-        mean += x.mean(dim=[0, 2, 3]) * b
-        sq += (x ** 2).mean(dim=[0, 2, 3]) * b
-        n += b
-    mean /= n
-    std = (sq / n - mean ** 2).sqrt()
-    return mean, std
-
-raw = datasets.ImageFolder("data/chest_xray_all", transform=transforms.ToTensor())
-mean, std = compute_mean_std(raw)  # fit on the FULL 18,432-image pool
-
-transform = transforms.Compose([
-    transforms.Resize((224, 224)),
-    transforms.ToTensor(),
-    transforms.Normalize(mean.tolist(), std.tolist()),
-])
-full_ds = datasets.ImageFolder("data/chest_xray_all", transform=transform)
-
-torch.manual_seed(42)
-n_train = int(0.8 * len(full_ds))
-n_test = len(full_ds) - n_train
-train_ds, test_ds = random_split(
-    full_ds, [n_train, n_test], generator=torch.Generator().manual_seed(42)
-)
+def compute_mean_std(dataset, indices):
+    subset = torch.utils.data.Subset(dataset, indices)
+    loader = DataLoader(subset, batch_size=256, shuffle=False, num_workers=4)
+    mean = torch.zeros(3)
+    sq = torch.zeros(3)
+    n = 0
+    for x, _ in loader:
+        b = x.size(0)
+        mean += x.mean(dim=[0, 2, 3]) * b
+        sq += (x ** 2).mean(dim=[0, 2, 3]) * b
+        n += b
+    mean /= n
+    std = (sq / n - mean ** 2).sqrt()
+    return mean, std
+
+# 1. Split FIRST, on raw (untransformed) data, before any statistic is fit.
+raw = datasets.ImageFolder("data/chest_xray_all", transform=transforms.ToTensor())
+n_train = int(0.8 * len(raw))
+n_test = len(raw) - n_train
+all_idx = list(range(len(raw)))
+
+def run_seed(seed):
+    rng = torch.Generator().manual_seed(seed)
+    perm = torch.randperm(len(raw), generator=rng).tolist()
+    train_idx, test_idx = perm[:n_train], perm[n_train:]
+
+    # 2. Fit normalization stats on the TRAIN indices only.
+    mean, std = compute_mean_std(raw, train_idx)
+
+    transform = transforms.Compose([
+        transforms.Resize((224, 224)),
+        transforms.ToTensor(),
+        transforms.Normalize(mean.tolist(), std.tolist()),
+    ])
+    full_ds = datasets.ImageFolder("data/chest_xray_all", transform=transform)
+    train_ds = torch.utils.data.Subset(full_ds, train_idx)
+    test_ds = torch.utils.data.Subset(full_ds, test_idx)
+
+    # Contamination guard: assert disjoint indices every run, not just once.
+    assert set(train_idx).isdisjoint(test_idx), "train/test indices overlap"
+    return train_ds, test_ds, seed
```

```diff
-model = models.resnet18(num_classes=1)
-optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)
-criterion = torch.nn.BCEWithLogitsLoss()
-
-train_loader = DataLoader(train_ds, batch_size=32, shuffle=True)
-test_loader = DataLoader(test_ds, batch_size=32, shuffle=False)
-
-for epoch in range(15):
-    model.train()
-    for x, y in train_loader:
-        optimizer.zero_grad(set_to_none=True)
-        loss = criterion(model(x).squeeze(1), y.float())
-        loss.backward()
-        optimizer.step()
-
-model.eval()
-correct, total = 0, 0
-with torch.no_grad():
-    for x, y in test_loader:
-        pred = (torch.sigmoid(model(x).squeeze(1)) > 0.5).long()
-        correct += (pred == y).sum().item()
-        total += y.size(0)
-print(f"test accuracy: {correct / total:.3f}")  # 0.951
+def train_and_eval(seed):
+    torch.manual_seed(seed)
+    train_ds, test_ds, _ = run_seed(seed)
+    model = models.resnet18(num_classes=1)
+    optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)
+    criterion = torch.nn.BCEWithLogitsLoss()
+    train_loader = DataLoader(train_ds, batch_size=32, shuffle=True)
+    test_loader = DataLoader(test_ds, batch_size=32, shuffle=False)
+
+    for epoch in range(15):
+        model.train()
+        for x, y in train_loader:
+            optimizer.zero_grad(set_to_none=True)
+            loss = criterion(model(x).squeeze(1), y.float())
+            loss.backward()
+            optimizer.step()
+
+    model.eval()
+    correct, total = 0, 0
+    with torch.no_grad():
+        for x, y in test_loader:
+            pred = (torch.sigmoid(model(x).squeeze(1)) > 0.5).long()
+            correct += (pred == y).sum().item()
+            total += y.size(0)
+    return correct / total
+
+results = [train_and_eval(seed) for seed in (42, 7, 123, 2024, 31337)]
+mean_acc = sum(results) / len(results)
+variance = sum((r - mean_acc) ** 2 for r in results) / (len(results) - 1)
+print(f"accuracy over {len(results)} seeds: {mean_acc:.3f} +/- {variance ** 0.5:.3f}")
+print(f"per-seed: {[round(r, 3) for r in results]}")
```

## 5. Proof of Robustness Post-Fix

```
$ python3 train_hardened.py
accuracy over 5 seeds: 0.887 +/- 0.006
per-seed: [0.887, 0.891, 0.879, 0.895, 0.883]

$ python3 -m pytest tests/test_no_split_leakage.py -v
tests/test_no_split_leakage.py::test_train_test_indices_disjoint PASSED
tests/test_no_split_leakage.py::test_norm_stats_fit_after_split_only PASSED
2 passed in 0.31s
```

The hardened pipeline now reports the honest number required for a
comparative claim: **88.7% +/- 0.6%** across five seeds, computed with
normalization statistics fit only on each run's training indices, with an
automated assertion that train/test indices are disjoint on every seed. This
is below the v2 production baseline (89.7%), not above it - the "new SOTA"
claim is retracted, and the writeup is re-filed as "v3 does not yet beat v2;
investigate architecture/hyperparameters, not the split." The two attack
vectors both had to be closed to reach this conclusion: fixing only the
leak still would have left a single, unreported-variance number masquerading
as a stable result.
