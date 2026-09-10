# hep-analysis Examples

Canonical worked examples: a "Common Weak Approach" vs. "Expert-Level Best
Practice" contrast plus key takeaways, for a realistic scenario in this skill's
domain. See `agile-development`'s
[references/example-authoring.md](../../agile-development/references/example-authoring.md)
for how these are generated and validated (requires `agile-development`
installed alongside this skill).

| Example | Domain Use Case | Contrast in one line |
|---|---|---|
| [01-jes-systematic-cutflow.md](01-jes-systematic-cutflow.md) | Estimating the jet-energy-scale systematic uncertainty on a cutflow-based cross-section measurement | Reusing the nominal selection mask for the JES up/down variations (reporting a suspicious 0.000% uncertainty) vs. recomputing the selection on each shifted branch (recovering the true 4.06% migration-driven uncertainty) |
