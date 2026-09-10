# deep-learning Examples

Canonical worked examples: a "Common Weak Approach" vs. "Expert-Level Best
Practice" contrast plus key takeaways, for a realistic scenario in this skill's
domain. See `agile-development`'s
[references/example-authoring.md](../../agile-development/references/example-authoring.md)
for how these are generated and validated (requires `agile-development`
installed alongside this skill).

| Example | Domain Use Case | Contrast in one line |
|---|---|---|
| [01-imbalanced-dataloader-training-loop.md](01-imbalanced-dataloader-training-loop.md) | A DataLoader and training loop for an imbalanced binary-classification dataset | A DataLoader shuffle and loss tied to the global RNG stream and left unweighted vs. a dedicated generator, class-weighted loss, and a checkpoint that saves seed/RNG state alongside the weights |
