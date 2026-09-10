# agile-development Examples

Canonical worked examples: a "Common Weak Approach" vs. "Expert-Level Best
Practice" contrast plus key takeaways, for a realistic scenario in this skill's
domain. See [../references/example-authoring.md](../references/example-authoring.md)
for how these are generated and validated.

| Example | Domain Use Case | Contrast in one line |
|---|---|---|
| [01-bug-fix-scoping-review.md](01-bug-fix-scoping-review.md) | Scoping and reviewing a bug fix for a cart total that is wrong when a discount code is applied | A one-off patch that special-cases the reported codes vs. a failing-test-first fix that states and implements the missing stacking contract with exact decimal arithmetic |
| [02-new-feature-slicing-and-acceptance-criteria.md](02-new-feature-slicing-and-acceptance-criteria.md) | Scoping a new "let admins export a CSV of active users" feature request | A broad, unreviewable PR bundling a dashboard, job queue, and email notifier on a silently-guessed "active user" definition vs. given/when/then acceptance criteria, an explicit stated assumption, and the smallest vertical slice with deferred follow-ups |
| [03-production-incident-response-postmortem.md](03-production-incident-response-postmortem.md) | Responding to and writing the postmortem for a checkout outage caused by a locking database migration | Root-causing during live impact and a blaming, vague postmortem vs. stabilize-first rollback and a blameless, timestamped postmortem with systemic contributing factors and owned action items |
