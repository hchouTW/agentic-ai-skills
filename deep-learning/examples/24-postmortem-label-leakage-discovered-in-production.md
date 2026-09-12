---
role: Site Reliability / Principal Machine Learning Engineer
skill: deep-learning
archetype: postmortem
incident: A data-pipeline bug leaked label-derived information into a training feature, inflating offline validation metrics; only discovered after the model shipped and underperformed badly in production
---

## 1. Incident Symptom & Alert Payload

```
[Weekly model-quality dashboard, 2025-05-19]
metric: production_auc (churn-risk-classifier-v4)
offline_validation_auc: 0.94
production_auc_rolling_7d: 0.61   <- flagged RED, first time observed

--- production monitoring alert ---
ALERT [FIRING] model-quality-degradation
model: churn-risk-classifier-v4
production_auc: 0.61 (offline validation reported: 0.94)
delta: -0.33 (threshold for review: -0.05)
```

The model had been in production for eleven days before the weekly
dashboard flagged the gap between its offline-reported and production-
observed performance - there was no automated comparison against the
offline number at deploy time.

## 2. Immediate Triage & Blast-Radius Mitigation

Per `references/monitoring-and-lifecycle.md`'s "roll back first, diagnose
second" incident response, the on-call engineer immediately reverted
production traffic to `churn-risk-classifier-v3` (the previous model),
since a production AUC of 0.61 was materially worse than v3's known 0.79
and every day on v4 risked more downstream business decisions (retention-
offer targeting) being made on effectively near-random risk scores.
Rollback completed within the standard model-serving rollback procedure
(re-pointing the serving config to the previous versioned model artifact),
restoring production AUC to v3's baseline within one serving cycle.

## 3. 5-Whys Root Cause Deep-Dive

1. **Why did the model perform far worse in production (AUC 0.61) than
   offline validation suggested (AUC 0.94)?** Because one of the model's
   input features, `days_since_last_support_contact`, was computed in the
   training pipeline using each customer's *entire* historical support-
   contact log, including contacts that occurred *after* the churn label's
   observation date - a customer who churned often generated a support
   contact around cancellation, so this feature was inadvertently encoding
   information from the future relative to the label.
2. **Why does the training feature use contacts after the label date?**
   Because the feature-computation function takes a customer ID and
   queries "most recent support contact" against the live support-ticket
   table at the time the training dataset is built, rather than
   reconstructing the feature as it would have been known *as of* the
   label's observation date - the function has no concept of a reference
   date at all.
3. **Why wasn't this caught by `scripts/check_split_integrity.py`, which
   this pipeline does run?** Because that script checks for entity/group
   leakage across train/test splits (the same customer appearing in both),
   per `references/data-strategy.md` - it does not check for *temporal*
   leakage within a single feature's computation, which is a different
   failure mode the tool was never designed to catch.
4. **Why did offline validation not reveal the problem, if the leakage
   was present in both train and validation data?** Because the same
   future-looking computation was applied consistently to the validation
   set as well, so the leaked signal was available and predictive in both
   - offline validation measures whether train and validation agree with
   each other, not whether either reflects the information genuinely
   available at prediction time in production.
5. **Why is there no check that a feature's information is limited to
   what was actually knowable as of the label date?** Because
   `references/data-strategy.md`'s temporal-leakage guidance ("any feature
   computed using information unavailable at prediction time... vanishes
   in production") is documented as a review principle, but this pipeline
   has no automated point-in-time correctness check enforcing it - feature
   correctness relative to a reference date was left to manual review,
   and the manual review for this specific feature did not happen.

Root cause: the `days_since_last_support_contact` feature was computed
without any reference-date boundary, silently pulling in post-label
information identically in both training and validation data, and no
automated check exists in this pipeline for temporal (as opposed to
entity/group) leakage - only the latter is currently enforced by tooling.

## 4. Permanent Surgical Fix (Diff)

```diff
--- a/features/support_contact_recency.py
+++ b/features/support_contact_recency.py
@@ -4,8 +4,11 @@ def days_since_last_support_contact(customer_id, support_log):
-def compute(customer_id, support_log):
-    contacts = support_log.filter(customer_id=customer_id)
-    most_recent = contacts.order_by("-contact_date").first()
-    return (today() - most_recent.contact_date).days
+def compute(customer_id, support_log, as_of_date):
+    """as_of_date must equal the label's observation date in training,
+    and the actual prediction time in production - never 'today()'."""
+    contacts = support_log.filter(
+        customer_id=customer_id, contact_date__lte=as_of_date
+    )
+    most_recent = contacts.order_by("-contact_date").first()
+    return (as_of_date - most_recent.contact_date).days if most_recent else None
```

```diff
--- a/scripts/check_split_integrity.py
+++ b/scripts/check_split_integrity.py
@@ -30,3 +30,15 @@ def check_group_leakage(train_df, test_df, group_col):
     overlap = set(train_df[group_col]) & set(test_df[group_col])
     if overlap:
         raise AssertionError(f"group leakage: {len(overlap)} shared group id(s)")
+
+def check_temporal_leakage(feature_fn, sample_customer_id, label_date,
+                            support_log):
+    """Fail if a feature's value changes when future support-log rows
+    (after label_date) are added - a feature that is truly point-in-time
+    correct must be invariant to data that didn't exist yet."""
+    value_at_label_date = feature_fn(sample_customer_id, support_log, label_date)
+    log_with_future_row = add_synthetic_future_contact(support_log, sample_customer_id)
+    value_with_future_data = feature_fn(sample_customer_id, log_with_future_row, label_date)
+    if value_at_label_date != value_with_future_data:
+        raise AssertionError(
+            f"feature changed when future data was added: "
+            f"{value_at_label_date} != {value_with_future_data}"
+        )
```

## 5. Blameless Postmortem & Preventative Monitoring Rules

No individual is at fault: the feature-engineering pattern used here
("query the current state of a table for this customer") is the default,
natural way to write a feature function, and nothing in the existing
tooling or review checklist specifically prompted a check for whether
"current state" silently includes information from after the label date.

**What worked:** the weekly production-vs-offline comparison dashboard,
even though it took eleven days to run against this model, was what
actually surfaced the problem - without it, the gap could have persisted
indefinitely since no other signal indicated a problem.

**What didn't work:** `check_split_integrity.py` gave false confidence
that leakage checks were "handled" for this pipeline, when in fact it only
covers one leakage class (entity/group) and not the one that actually
occurred (temporal); the existing tool's name and role were not
re-examined for scope gaps before assuming pipeline safety.

**Preventative monitoring rule:** `scripts/check_split_integrity.py` now
also runs `check_temporal_leakage` on every feature in the pipeline as a
required pre-training gate (blocking training on failure), and
`model-quality-degradation` now alerts and blocks promotion to full
traffic if production AUC on the first 24 hours of canary traffic
diverges from offline validation AUC by more than 5%, rather than waiting
for a weekly dashboard review to catch it after full rollout.
