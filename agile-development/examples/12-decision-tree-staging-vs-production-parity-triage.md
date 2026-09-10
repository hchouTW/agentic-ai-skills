---
role: Senior Software Engineer
skill: agile-development
archetype: decision-tree
scenario: a feature works correctly in staging but misbehaves in production, with the cause not yet known
---

## Triage Matrix

Formalizes `references/risk-and-quality.md`'s "Configuration and
Environments" and "Observability" sections - "preserve environment parity
where behavior must be consistent" and "fail clearly when required
configuration is missing" - into an explicit trigger-to-strategy mapping for
a staging-vs-production discrepancy:

| Trigger | Resolution Strategy |
|---|---|
| A required config value or secret is present in staging but missing or stale in production | Check the production config/secret store directly for the specific key the feature reads; add a clear startup-time failure for that key if it fails silently today |
| A feature flag defaults differently per environment (e.g. on in staging, off in production) | Check the flag's per-environment configuration directly rather than assuming code parity implies flag parity |
| Production has meaningfully more scale, data variety, or concurrency than staging ever exercises | Suspect a scale-dependent bug (a race condition, an edge case in real data) rather than a config difference, and reproduce with production-scale data or load |
| Production and staging run genuinely different infrastructure (a managed service in one, a container in the other) | Suspect an infrastructure-parity gap (a different default, version, or network path) rather than the application code itself |
| None of the above differ, and the two environments are otherwise identical | Suspect a data difference specific to the affected production records, not the environment itself |

## Selected Branch

The feature (a scheduled report email) sends correctly in staging every time
but silently never sends in production, with no error logged. Config,
feature flags, scale, and infrastructure were all checked in that order per
the matrix; the first one found different was the third-party email
provider's API key, which is present in staging's config but was never added
to production's secret store during the original deploy - matching the first
row.

## End-to-End Execution Script

1. Confirm the specific key the report-email code reads:
   `EMAIL_PROVIDER_API_KEY` via `os.environ["EMAIL_PROVIDER_API_KEY"]`.
2. Check production's secret store directly rather than assuming parity:
   `secrets-cli get production/EMAIL_PROVIDER_API_KEY` returns "not found";
   the same command against staging returns a value.
3. Read the call site to see why this failed silently instead of erroring:
   the code used `os.environ.get("EMAIL_PROVIDER_API_KEY")`, which returns
   `None` rather than raising, and the email-sending call silently no-ops
   when its API key argument is `None` instead of raising.
4. Fix both the missing secret and the silent-failure pattern per
   `references/risk-and-quality.md`'s "fail clearly when required
   configuration is missing" guidance:
   ```diff
   -api_key = os.environ.get("EMAIL_PROVIDER_API_KEY")
   +api_key = os.environ["EMAIL_PROVIDER_API_KEY"]  # raises KeyError if unset, per
   +                                                  # this skill's fail-clearly guidance
   ```
5. Add the missing key to production's secret store:
   `secrets-cli set production/EMAIL_PROVIDER_API_KEY <value>`, and confirm
   the next scheduled report run in production actually sends.

## Fallback Safeguards

If adding the missing key does not fix the send (the fail-clearly change now
raises a *different* error), the trigger was misclassified: re-triage against
the matrix's second row and check whether the report-sending feature flag
itself is also off in production independent of the key, rather than assuming
the config gap was the only difference. If the fail-clearly change starts
raising `KeyError` in a *different*, previously-working environment that
happens to omit this key for a legitimate reason (e.g. a preview environment
that intentionally disables email), add an explicit opt-out rather than
reverting to the silent-`None` pattern, so environment parity gaps stay loud
everywhere except where they are deliberately, visibly allowed.
