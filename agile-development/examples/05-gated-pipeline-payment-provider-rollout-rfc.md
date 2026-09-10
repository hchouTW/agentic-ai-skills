---
role: Principal Software Engineer
skill: agile-development
archetype: gated-pipeline
high_stakes_task: drafting and shipping an RFC for a feature-flagged progressive rollout of a new checkout payment provider
---

## Phase 1: Input Extraction & Gap Formulation

Extracted from the payments team's request: replace the legacy card processor
with a new provider that charges 30 basis points less per transaction, without
a big-bang cutover, and without expanding PCI compliance scope (the new
provider must sit behind the same tokenization boundary).

Gaps found when writing this up:
- No rollback trigger had been named - only "if something looks wrong."
- No staged rollout percentages existed, only "roll it out gradually."
- No owner was assigned for the feature-flag kill switch outside business
  hours.

**Gate:** proceed to Phase 2 only once the problem statement, at least one
alternative to the full swap (including "do nothing" and "the smallest
possible version"), and a named rollback trigger are captured in writing, per
`references/design-and-estimation.md`'s "What a lightweight design doc should
contain".

## Phase 2: Draft Synthesis

Drafted the RFC's five required sections, aligned to
`references/design-and-estimation.md`'s "What a lightweight design doc should
contain" checklist:

- **Problem**: legacy processor's per-transaction fee is 30bps above the new
  provider's, costing roughly $180k/year at current volume, and its refund API
  lacks partial-refund support the product team has requested for six months.
- **Options considered**: (1) do nothing - keep paying the fee premium and
  forgo partial refunds; (2) negotiate the legacy provider's rate down without
  switching; (3) a full cutover to the new provider in one deploy; (4) a
  feature-flagged progressive rollout of the new provider alongside the
  legacy one. Option 2 was ruled out (the legacy provider declined to match
  the new rate); option 3 was ruled out as too risky for a payment path.
- **Chosen approach and why**: option 4 - the new provider integrated behind a
  `use_new_payment_provider` flag, enabled per-order rather than globally, so a
  regression affects a bounded fraction of orders rather than all of them.
- **Risks and unknowns**: whether the new provider's webhook delivery is
  exactly-once or at-least-once (flagged for Phase 3 below), and whether its
  sandbox environment's chargeback simulation matches production behavior
  closely enough to trust pre-launch testing.
- **Rollback/rollout plan**: stage at 1% of orders (internal test accounts
  only) for 3 days, then 5% for 3 days, then 25% for a week, then 100% -
  each stage gated on the successful-transaction-rate dashboard staying within
  0.5% of the legacy provider's baseline and the chargeback-rate dashboard
  showing no statistically significant increase, per
  `references/design-and-estimation.md`'s "Feature flags and progressive
  rollout as risk-reduction tools" guidance to enable progressively rather
  than flipping a single global switch. The flag's removal (collapsing both
  code paths into one once the legacy provider is fully retired) is scheduled
  as its own follow-up ticket in the same section, per that same guidance
  against letting a rollout flag become permanent debt.

**Gate:** proceed to Phase 3 only once the Rollback/rollout plan section names
an exact metric threshold for every stage and the flag-removal follow-up
ticket exists.

## Phase 3: Red-Team Review & Final Artifact Packaging

Red-teamed the draft's assumptions before packaging it for review. The
assumption that most needed stress-testing was: "the new provider's webhook
retries are idempotent, so re-processing a delayed refund webhook is safe."

Testing against the provider's sandbox showed this assumption was **false**:
under a simulated network partition, the provider retries a refund webhook
without including a de-duplication key, and the draft RFC's refund handler
would have processed each retry as a separate refund - double-crediting the
customer. As a result:

- Added a new requirement to the Problem/Options sections: the integration
  must generate and check its own idempotency key before crediting a refund,
  independent of whatever the provider's webhook guarantees turn out to be.
- Added "duplicate refund detected for the same order" as an automatic
  rollback trigger in the Rollback/rollout plan section, in addition to the
  transaction-rate and chargeback-rate thresholds from Phase 2.
- Confirmed with the payments team that this idempotency-key requirement adds
  approximately three days to the timeline before Stage 1 can begin, and got
  written sign-off on that delay rather than shipping Phase 2's draft as-is.

**Gate:** merge only once the idempotency-key requirement is implemented and
covered by a test reproducing the double-webhook scenario above, and the
named flag owner has signed off on the final Rollback/rollout plan - this is
the release/merge criterion, not an intermediate one.
