---
role: Site Reliability / Principal Machine Learning Engineer
skill: deep-learning
archetype: postmortem
incident: Model-serving p99 latency silently regressed 3x after a routine tokenizer library upgrade, undetected for four days until customer complaints
---

## 1. Incident Symptom & Alert Payload

```
[Customer support ticket #88213, filed 2025-04-10]
"Our integration's response times tripled starting around April 6th.
Nothing changed on our side. Please investigate."

--- retroactive query against the ops metrics store (no alert fired at
    the time) ---
metric: inference_p99_latency_ms{service="text-classifier-v3"}
2025-04-05 23:00  412ms
2025-04-06 00:00  1180ms   <- tokenizer-lib bump deployed 2025-04-05 23:40
2025-04-06 01:00  1205ms
2025-04-10 09:00  1240ms   (still elevated, no alert ever fired)
```

The deploy itself completed successfully with no errors, no crash-looping,
and no change in error rate - only p99 latency moved, and no
latency-regression alert existed to catch it.

## 2. Immediate Triage & Blast-Radius Mitigation

Per `references/monitoring-and-lifecycle.md`'s incident-response guidance
to "roll back first, diagnose second," the on-call engineer rolled the
tokenizer library back to its pinned pre-upgrade version immediately upon
confirming the correlation between the deploy timestamp and the latency
step-change, without first identifying the exact mechanism - p99 latency
returned to baseline (~410ms) within the first post-rollback deployment
cycle. The rollback carried negligible risk since the library bump was a
routine dependency update with no accompanying feature change to give up.

## 3. 5-Whys Root Cause Deep-Dive

1. **Why did p99 latency triple immediately after the tokenizer library
   upgrade?** Because the new library version's default tokenizer
   implementation switched from a fast, Rust-backed byte-pair-encoding
   path to a pure-Python fallback path for this service's specific
   vocabulary configuration (a custom added-tokens list), and the
   pure-Python path is roughly 8x slower per request.
2. **Why did the upgrade silently select the slower fallback path?**
   Because the new library version added stricter validation of custom
   added tokens and this service's added-tokens list contained a token
   with characters the new validation flags as needing the fallback
   tokenizer, whereas the previous version accepted the same list on the
   fast path without that check.
3. **Why wasn't this behavior change caught before the upgrade reached
   production?** Because the dependency-update process ran the existing
   regression suite, which checks output *correctness* (does the model
   produce the same predictions) but has no latency assertion - the
   upgraded tokenizer produced identical token sequences and identical
   predictions, so every correctness check passed while the
   performance characteristic silently changed underneath.
4. **Why did no automated alert fire when p99 latency tripled in
   production?** Because `references/monitoring-and-lifecycle.md`'s
   "operational" monitoring layer (latency, error rate, throughput) was
   configured for this service with only an *absolute* latency threshold
   set well above the new, degraded baseline (a static 2000ms threshold,
   set once at initial launch and never revisited), not a
   relative-regression check against the service's own recent history.
5. **Why did it take a customer complaint, rather than internal
   monitoring, to surface a 3x regression?** Because the static threshold
   was never tuned after being set, and no dashboard or review process
   periodically re-examines whether an existing alert threshold is still
   meaningfully tighter than current normal operating latency - a
   threshold set once at launch silently became four years stale as the
   service's baseline improved through unrelated optimizations, then a
   regression that would have breached a properly-tuned threshold went
   undetected entirely.

Root cause: the regression suite validates prediction correctness but not
latency, and the only latency alert configured was a static absolute
threshold set at launch and never revisited, so a 3x latency regression
that left correctness completely unaffected had no monitoring layer
positioned to catch it.

## 4. Permanent Surgical Fix (Diff)

```diff
--- a/ci/regression_suite.py
+++ b/ci/regression_suite.py
@@ -18,6 +18,16 @@ def run_regression_suite(candidate_model, baseline_model, eval_set):
     correctness_diff = compare_predictions(candidate_model, baseline_model, eval_set)
     assert_no_unexplained_regression(correctness_diff)
+
+    # Latency regression check (see postmortem: silent tokenizer
+    # slow-path regression). A dependency bump that changes latency
+    # without changing predictions must still fail this suite.
+    baseline_p99 = measure_p99_latency(baseline_model, eval_set, n=500)
+    candidate_p99 = measure_p99_latency(candidate_model, eval_set, n=500)
+    regression_ratio = candidate_p99 / baseline_p99
+    if regression_ratio > 1.15:
+        raise AssertionError(
+            f"p99 latency regressed {regression_ratio:.2f}x "
+            f"({baseline_p99:.0f}ms -> {candidate_p99:.0f}ms)"
+        )
```

```diff
--- a/ops/alerts/serving_latency.yaml
+++ b/ops/alerts/serving_latency.yaml
@@ -1,5 +1,11 @@
 - alert: inference-p99-absolute
   expr: inference_p99_latency_ms > 2000
   for: 5m
+
+- alert: inference-p99-relative-regression
+  # Compares current p99 to the trailing 7-day median rather than a
+  # static threshold, so a regression from an already-fast baseline
+  # still fires (see postmortem: 412ms -> 1200ms never crossed 2000ms).
+  expr: inference_p99_latency_ms > 1.5 * inference_p99_latency_ms_7d_median
+  for: 15m
```

## 5. Blameless Postmortem & Preventative Monitoring Rules

No individual is at fault: the dependency upgrade passed every existing
automated check, and the engineer who approved it had no tooling that
would have surfaced a latency-only regression - the gap is a missing check
category, not a missed review step.

**What worked:** once the correlation between the deploy timestamp and the
latency step-change was identified, rolling back was fast, low-risk, and
fully resolved the customer-facing symptom within one deploy cycle.

**What didn't work:** a static absolute latency threshold set once at
launch and never revisited gave a four-day false sense of safety - the
regression was three times the pre-incident baseline but never came close
to breaching a threshold set for a very different baseline years earlier.

**Preventative monitoring rule:** `ci/regression_suite.py` fails any
candidate model or dependency change where measured p99 latency regresses
by more than 15% relative to the current baseline, and
`inference-p99-relative-regression` pages the owning team whenever
production p99 latency exceeds 1.5x its own trailing 7-day median for more
than 15 minutes, independent of the static absolute threshold.
