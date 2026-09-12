---
role: Site Reliability Engineer
skill: agile-development
archetype: postmortem
incident: A feature flag guarded the main request handler but not a secondary retry code path, causing errors for a subset of users once the flag was enabled at 5% rollout
---

## 1. Incident Symptom & Alert Payload

```
ALERT [FIRING] error-rate-spike
service: checkout-api
route: POST /v2/checkout/confirm (retry path only)
error_rate: 41% (threshold: 2%)
window: 5m
started_at: 2025-03-11T14:22:00Z

--- tail of application error log ---
[14:22:03] ERROR NullPointerException at RetryHandler.confirmPayment
  cause: PaymentAdapterV2 not initialized (feature-flag gated construction)
  request_id: 7f2a-91cc
[14:22:03] ERROR NullPointerException at RetryHandler.confirmPayment
  request_id: 7f2a-91cd
[14:22:04] ERROR NullPointerException at RetryHandler.confirmPayment
  request_id: 7f2a-91ce
... (repeats for every retried request routed to a flagged-in user)
```

The primary confirmation path worked correctly for the 5% of users
assigned to the new flag; only requests that hit the *retry* path (issued
automatically after a transient timeout) failed.

## 2. Immediate Triage & Blast-Radius Mitigation

Per `references/engineering-playbook.md`'s incident-response guidance to
mitigate before fully understanding root cause, the on-call engineer
disabled the feature flag globally within four minutes of the alert firing
- reverting all traffic to the old payment adapter, including the 5%
already assigned to the new one - rather than attempting a live fix to the
retry path first. This was chosen over a partial mitigation (e.g. excluding
only the retry path from the flag) because the retry path's flag-check
code was already known to be wrong and untrusted at triage time; a
narrower fix risked missing a second, undiscovered gap. Error rate on the
retry path returned to baseline within one minute of the flag flip.

## 3. 5-Whys Root Cause Deep-Dive

1. **Why did retried checkout-confirmation requests throw a null-pointer
   error?** Because `RetryHandler.confirmPayment` called
   `PaymentAdapterV2`, which is only constructed when the feature flag is
   read as `true`, but the flag check that constructs it lives in the
   primary handler's setup path, which the retry path does not go through.
2. **Why does the retry path skip the primary handler's setup?** Because
   `RetryHandler` is invoked directly by the request-timeout middleware as
   a separate entry point, constructed once at application startup before
   any per-request flag evaluation happens - it was written before
   per-request feature flags existed in this codebase and was never
   updated when they were introduced.
3. **Why wasn't `RetryHandler`'s dependency on the flagged adapter
   noticed when the flag was added?** Because
   `references/design-and-estimation.md`'s guidance to "ship the code path
   behind a flag defaulted off, verify it in production... then enable
   progressively" was followed for the primary path, but no equivalent
   check was made for every other code path that could reach the same
   payment adapter - the flag's blast radius was scoped to "the handler I
   edited," not to every caller of the object it constructs.
4. **Why did code review not catch the missing flag check in
   `RetryHandler`?** Because the pull request that introduced
   `PaymentAdapterV2` and its flag only modified
   `PrimaryCheckoutHandler.java`; `RetryHandler.java` was not part of the
   diff, so a reviewer scanning the changed files had no visual cue that
   an unmodified file also depended on the now-flagged construction path.
5. **Why is there no test that exercises the retry path with the flag
   enabled?** Because the feature's test suite covers the primary
   confirmation path under both flag states, but the retry path's test
   coverage predates the flag entirely and was never re-run against the
   new flagged branch - the two code paths share a dependency but were
   never tested as a pair.

Root cause: the payment-adapter feature flag was scoped to the one file
the implementing engineer edited, but the flagged object is constructed by
a second, older entry point (`RetryHandler`) that has no per-request flag
evaluation of its own - a change's blast radius was defined by which files
were touched, not by which code paths actually depend on the flagged
component.

## 4. Permanent Surgical Fix (Diff)

```diff
--- a/src/main/java/checkout/RetryHandler.java
+++ b/src/main/java/checkout/RetryHandler.java
@@ -12,8 +12,12 @@ public class RetryHandler {
-    private final PaymentAdapterV2 paymentAdapter = new PaymentAdapterV2();
+    private PaymentAdapter resolvePaymentAdapter(FlagContext ctx) {
+        return featureFlags.isEnabled("payment-adapter-v2", ctx)
+            ? paymentAdapterV2
+            : paymentAdapterV1;
+    }
 
     public void confirmPayment(RetryRequest request) {
-        paymentAdapter.confirm(request);
+        resolvePaymentAdapter(request.flagContext()).confirm(request);
     }
```

```diff
--- a/src/test/java/checkout/RetryHandlerTest.java
+++ b/src/test/java/checkout/RetryHandlerTest.java
@@ -20,4 +20,14 @@ class RetryHandlerTest {
+    @Test
+    void confirmPaymentUsesV2AdapterWhenFlagEnabled() {
+        FlagContext ctx = FlagContext.forcedOn("payment-adapter-v2");
+        handler.confirmPayment(retryRequest(ctx));
+        verify(paymentAdapterV2).confirm(any());
+    }
```

## 5. Blameless Postmortem & Preventative Monitoring Rules

No individual is at fault: the engineer who added the flag correctly
followed the rollout guidance for the file they were editing, and the
reviewer correctly reviewed the diff they were shown - the gap is that
"every caller of this component" was never enumerated as part of adding
the flag, and nothing in the review tooling surfaces indirect callers of a
changed dependency.

**What worked:** disabling the flag globally rather than attempting a
targeted fix on the retry path resolved user impact in under five minutes
total and avoided a second incident from an incomplete live patch.

**What didn't work:** the feature's own test suite gave false confidence -
it exercised the primary path under both flag states but never exercised
the retry path under the "flag enabled" state, so a real gap passed CI
cleanly.

**Preventative monitoring rule:** alert if any request to a flag-gated
component's retry or fallback code path returns a 5xx status for more than
1% of requests within a 5-minute window while the corresponding feature
flag is enabled for any percentage of traffic, paging the flag's owning
team rather than waiting for the aggregate service-wide error rate to
cross its own separate threshold.
