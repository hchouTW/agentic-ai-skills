---
role: Engineering Lead
skill: agile-development
archetype: decision-tree
scenario: triaging an ambiguous production incident page and choosing the fastest safe mitigation before root-causing
---

## Triage Matrix

Formalizes `references/engineering-playbook.md`'s Incident Response step 2
("mitigate before you fully understand") into an explicit trigger -> strategy
mapping, so the on-call engineer doesn't have to re-derive it under pressure:

| Trigger | Resolution Strategy |
|---|---|
| Error/latency spike began within minutes of a deploy finishing | Roll back the deploy |
| Spike correlates with a specific feature flag being flipped on recently | Disable that feature flag |
| Spike correlates with a traffic surge to one specific endpoint or region, with no recent deploy or flag change | Shift traffic away from the affected instance or region |
| No correlation with a deploy, flag, or traffic pattern, but a known-risky downstream dependency call is timing out | Trip a targeted kill switch on that dependency call |
| The obvious mitigation itself carries comparable risk (e.g. rolling back would reintroduce a different known bug) | Skip that mitigation; escalate immediately to an all-hands root-cause investigation instead of mitigating blind |

## Selected Branch

The page reads: "checkout error rate up 8x, alert fired 4 minutes after the
nightly deploy finished; no feature-flag changes or unusual traffic in the
same window." That matches the first row - deploy-correlated spike with no
competing signal - so the selected branch is **roll back the deploy**.

## End-to-End Execution Script

1. Confirm the correlation: `kubectl rollout history deploy/checkout-service`
   shows the new revision became active 4 minutes before the alert fired, and
   the error-rate dashboard's spike starts at the same timestamp.
2. Roll back:
   ```
   $ deploy rollback checkout-service --to-previous --reason "SUPPORT-page-9142 error rate spike"
   Rolling back checkout-service from rev-214 to rev-213...
   Rollback complete. New pods healthy: 12/12.
   ```
3. Post to `#incidents`, verbatim: "Checkout error rate spiked 8x starting 4
   minutes after tonight's deploy (rev-214). Rolling back to rev-213 now as
   the immediate mitigation; will confirm recovery and follow up with root
   cause once stable."
4. Watch the error-rate and latency dashboards for 5 minutes. If they return
   to baseline, post the follow-up: "Error rate back to baseline 3 minutes
   after the rollback completed. Rollback resolved the immediate impact;
   keeping this incident open while we find the root cause in rev-214 before
   re-attempting the deploy."
5. Once mitigated, root-cause rev-214's diff with the same rigor as a normal
   bug fix (per the Bug Fix playbook), rather than stopping at the first
   plausible explanation, and write the blameless postmortem afterward per
   the Incident Response playbook's steps 5-6.

## Fallback Safeguards

If the error rate has not returned to baseline within 5 minutes of the
rollback completing, do not keep waiting on it: escalate to the database
on-call in parallel, on the assumption that a second, coincident cause is now
in play rather than a slow-to-propagate rollback. If instead the error rate
keeps climbing after the rollback (a sign the trigger was misclassified and
the deploy was not actually the cause), immediately re-triage against the
matrix's third and fourth rows - check for a traffic surge or a timing-out
downstream dependency - rather than re-attempting the same rollback a second
time.
