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
| [02-nan-loss-mixed-precision.md](02-nan-loss-mixed-precision.md) | Diagnosing a NaN training loss under automatic mixed precision in a Transformer fine-tune | Lowering the learning rate and clipping harder around an unlocated NaN vs. localizing the fp16 softmax overflow inside a hand-written attention module and fixing it with an explicit fp32 block |
| [03-ddp-vs-fsdp-parallelism-choice.md](03-ddp-vs-fsdp-parallelism-choice.md) | Choosing a parallelism strategy for fine-tuning a 7B-parameter model that no longer fits under plain DDP | Retrying smaller micro-batches against a DDP OOM vs. computing the four-term memory budget, identifying the optimizer state as binding, and switching to block-granularity FSDP full sharding |
