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
