---
role: Senior ML Systems Engineer
skill: deep-learning
archetype: trajectory
problem_input: a validation AUC of 0.98 during training that collapses to a barely-above-baseline 0.71 in a live production A/B test
---

## 1. Task Input & Context

Handoff note from the modeling team:

> Our churn-risk classifier trains to a validation AUC of 0.98 - it looked
> like a huge win over the previous model's 0.81. We shipped it to a 10%
> production A/B test. Four days in, the A/B dashboard shows the new model's
> real-world AUC at 0.71, barely above the old model's production AUC of
> 0.69. Nothing about the serving pipeline changed between the old and new
> model.

The dataset is one row per (customer, billing-cycle) pair; a typical customer
appears in 12-40 rows spanning their tenure. The train/validation split was
built with `torch.utils.data.random_split` over the full row-level dataset.

## 2. Root-Cause Triage & Action Plan

A validation metric that is far better than production, with no serving
pipeline change to blame, is exactly the failure `references/data-strategy.md`
calls out under "Splits that survive contact with reality": "Group leakage is
the most common serious error... It is invisible in the metrics - the numbers
just look good." This dataset has repeated entities (multiple rows per
customer), which that same section's table marks as a case where a random
split is "optimistic - memorizes entities," not "genuinely i.i.d." where
random splitting would be correct.

Confirming directly: cross-referencing the customer IDs in the training split
against the validation split (after the `random_split` call) shows 91% of
validation-split customers also have at least one row in the training split.
The model at 0.98 AUC is very likely partially recognizing customers it has
already seen, not generalizing to new ones - which is exactly what the A/B
test, seeing only new production traffic, would not reward.

Per `references/optimization-and-training-dynamics.md`'s failure
classification table, this also matches "Generalization failure" territory in
spirit (train-time metric far better than what generalizes), but the fix
belongs in `data-strategy.md` as that table itself points to for this class:
fix the split by group before touching the model or its regularization.

Action plan: replace the row-level random split with a customer-level group
split (every row for a given customer goes entirely to train or entirely to
validation), retrain with the identical model and hyperparameters, and check
whether the resulting validation AUC now tracks the production A/B AUC.

## 3. Surgical Execution

```diff
-train_ds, val_ds = torch.utils.data.random_split(
-    dataset, [n_train, n_val], generator=torch.Generator().manual_seed(42)
-)
+customer_ids = dataset.customer_ids  # one entry per row, aligned with dataset order
+unique_customers = sorted(set(customer_ids))
+rng = random.Random(42)
+rng.shuffle(unique_customers)
+n_val_customers = int(0.2 * len(unique_customers))
+val_customers = set(unique_customers[:n_val_customers])
+train_idx = [i for i, cid in enumerate(customer_ids) if cid not in val_customers]
+val_idx = [i for i, cid in enumerate(customer_ids) if cid in val_customers]
+train_ds = torch.utils.data.Subset(dataset, train_idx)
+val_ds = torch.utils.data.Subset(dataset, val_idx)
+train_customers = {customer_ids[i] for i in train_idx}
+val_customers_check = {customer_ids[i] for i in val_idx}
+assert train_customers.isdisjoint(val_customers_check), "a customer appears in both splits"
```

## 4. Verification Evidence

```
$ python3 -m pytest tests/test_split_integrity.py -k group_leakage -v
tests/test_split_integrity.py::test_no_customer_appears_in_both_splits PASSED
1 passed in 0.09s

$ python3 train.py --split group --epochs 12
epoch 12  val_auc 0.8320
$ python3 scripts/compare_to_production.py --model-version group-split-v2
production_ab_auc (7-day rolling, new candidate): 0.8190
offline_val_auc: 0.8320
gap: 0.0130  (within the 0.01-0.02 offline/online gap this team has observed on prior, non-leaky splits)
```

The corrected offline validation AUC (0.832) is now close to what the model
actually achieves in production (0.819), unlike the leaky split's 0.98-vs-0.71
gap of 0.27.

## 5. Final Deliverable Summary

Traced a 0.98-offline/0.71-production AUC gap to row-level random splitting
over a dataset with repeated per-customer rows, which let the same customers
appear in both training and validation. Replaced the split with a
customer-level group split, added a regression test asserting no customer ID
appears in both splits, and confirmed the corrected offline AUC (0.832) now
sits within this team's normal offline/online gap of the actual production
A/B result (0.819), instead of wildly overstating it.
