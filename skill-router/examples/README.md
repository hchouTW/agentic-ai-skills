# skill-router Examples

Canonical worked examples: a "Common Weak Approach" vs. "Expert-Level Best
Practice" contrast plus key takeaways, for a realistic scenario in this skill's
domain. See `agile-development`'s
[references/example-authoring.md](../../agile-development/references/example-authoring.md)
for how these are generated and validated (requires `agile-development`
installed alongside this skill).

| Example | Domain Use Case | Contrast in one line |
|---|---|---|
| [01-adding-a-routing-rule-without-overlap.md](01-adding-a-routing-rule-without-overlap.md) | Adding a new routing rule to the table without creating overlap or ambiguity with an existing rule | A vague, un-scoped rule that passes the structural validator but collides with two existing rules' territory vs. a rule with distinct vocabulary and an explicit "Not for X - see Y" boundary clause, verified against the real validator's parser |
| [02-multi-skill-primary-secondary-routing.md](02-multi-skill-primary-secondary-routing.md) | A single request that legitimately spans two domain skills and must be routed to both, with an explicit primary and secondary | Silently invoking only the first-matching rule and treating the request as fully handled vs. checking every rule, stating "primary... with... for..." per `SKILL.md`'s own behavior rule, and invoking the primary first |
| [03-negative-carve-out-not-a-match.md](03-negative-carve-out-not-a-match.md) | Recognizing when a request only superficially matches a routed keyword and should not trigger that rule, per the rule's own stated negative carve-out | Pattern-matching the bare substring "root" straight to `hep-analysis` vs. checking the rule's own "Not for unrelated uses of 'root'" clause and correctly proceeding with no skill invoked |
