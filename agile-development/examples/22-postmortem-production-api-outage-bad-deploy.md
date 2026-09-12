---
role: Site Reliability Engineer
skill: agile-development
archetype: postmortem
incident: production API outage (500s spike) after a routine deploy of the checkout-api service
---

## 1. Incident Symptom & Alert Payload

```
ALERT [FIRING] api-5xx-rate-high
service: checkout-api
region: us-east-1
condition: rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m]) > 0.05
current_value: 0.187
started: 2026-08-14T14:02:11Z
runbook: https://runbooks.internal/checkout-api-5xx
```

PagerDuty paged the on-call SRE two minutes after `checkout-api` v2.14.0
finished a routine, low-risk-labeled rolling deploy. Within 5 minutes, the
5xx rate climbed from a baseline of ~0.1% to 18.7%, and customer support
opened three tickets citing "unable to complete purchase."

## 2. Immediate Triage & Blast-Radius Mitigation

The on-call SRE checked the deploy timeline first (per
`references/engineering-playbook.md`'s Incident Response step 1: establish
impact and correlate with recent changes before investigating root cause)
and found the 5xx spike started 91 seconds after v2.14.0's rollout completed
- a strong correlation, and rollback carries no comparable risk here since
v2.13.9 had been stable in production for three weeks. Per step 2
("mitigate before you fully understand"), the SRE rolled back immediately
rather than debugging the new version live:

```
$ deploy rollback checkout-api --to-previous
Rolling back checkout-api: v2.14.0 -> v2.13.9
Rollback complete. 40/40 pods healthy.
```

5xx rate returned to the 0.1% baseline within 3 minutes of the rollback
command. Total customer-facing impact window: approximately 12 minutes.
Support was told to close the three open tickets with a "resolved, retry
your purchase" note, and a status-page update was posted on the fixed
incident-communication cadence per `references/communication.md`.

## 3. 5-Whys Root Cause Deep-Dive

1. **Why did the 5xx rate spike?** Because a subset of `checkout-api` v2.14.0
   pods crash-looped on startup, reducing healthy capacity and causing the
   load balancer to route requests to pods that were still initializing.
2. **Why did those pods crash on startup?** Because v2.14.0 added a new
   required config key, `payment.retry_backoff_ms`, and the pods that
   crashed were reading from a production ConfigMap that predated the change
   and did not have that key set.
3. **Why did the production ConfigMap not have the new key?** Because the
   deploy pipeline updates application code and ConfigMaps in two separate,
   independently-triggered steps, and this deploy's ConfigMap update step
   was queued behind an unrelated, slower pipeline job and had not yet run
   when the code deploy completed.
4. **Why does the pipeline allow the code deploy to finish before its
   corresponding config update lands?** Because the two steps were designed
   as independent, parallelizable pipeline stages for speed, with no
   ordering dependency or precondition check between "new config key
   introduced" and "config value present before the depending code ships."
5. **Why was there no precondition check for that?** Because the schema
   validation added when config-driven feature flags were introduced two
   years ago only checks that a submitted ConfigMap is internally
   well-formed (valid YAML, known keys) - it was never extended to check
   that a new required key referenced by an in-flight code deploy is already
   present in the target environment's live ConfigMap before that deploy is
   allowed to proceed.

Root cause: a missing ordering guarantee between code deploys that introduce
new required config keys and the config-update pipeline stage that supplies
them, not an individual's mistake in this specific deploy.

## 4. Permanent Surgical Fix (Diff)

```diff
--- a/deploy/pipeline.yaml
+++ b/deploy/pipeline.yaml
@@ -18,10 +18,16 @@ stages:
   - name: update-configmap
     trigger: on_config_change
     runs: scripts/apply_configmap.sh
+    blocking: true
 
   - name: deploy-code
     trigger: on_image_push
+    depends_on:
+      - update-configmap
+    preconditions:
+      - script: scripts/check_required_config_keys.sh
+        description: >
+          Fails the deploy if any config key referenced by the new image's
+          startup schema is absent from the target environment's live
+          ConfigMap.
     runs: scripts/rollout.sh
```

`scripts/check_required_config_keys.sh` diffs the new image's declared
required-config schema against the live ConfigMap and blocks `deploy-code`
with a clear error (naming the missing key) if any key is absent, instead of
letting the code deploy race ahead of its config dependency.

## 5. Blameless Postmortem & Preventative Monitoring Rules

This incident was not caused by any individual acting unreasonably: the
deploy was labeled low-risk by the same process that had correctly labeled
dozens of prior deploys, and the engineer who added
`payment.retry_backoff_ms` followed the existing "add a config key, update
the ConfigMap" convention exactly as documented - the convention itself had
a race condition between two independently-triggered pipeline stages. The
fix targets that structural gap (an ordering precondition), not individual
diligence.

**What worked:** the deploy-correlation check in step 1 of the incident
runbook led to a correct, fast rollback decision (12-minute impact window)
without needing to understand the root cause first.

**What didn't work:** nothing caught the missing precondition before
production; there was no staging environment step that exercises the
code-deploy-ahead-of-config-update race, because staging's ConfigMap updates
are applied manually and synchronously, masking the race that only shows up
when both pipeline stages run independently in production.

**Preventative monitoring rule:** alert `deploy-precondition-skipped` fires
if `deploy-code` ever runs while `update-configmap`'s `blocking: true` gate
for the same release has not reported success within the preceding 10
minutes, paging the deploying engineer's team (not just SRE on-call) so a
future race is caught before rollout completes rather than after customer
impact begins.
