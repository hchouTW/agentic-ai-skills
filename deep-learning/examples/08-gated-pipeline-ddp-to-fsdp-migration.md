---
role: Principal ML Systems Engineer
skill: deep-learning
archetype: gated-pipeline
high_stakes_task: migrating a growing model's training job from single-node DDP to a multi-node FSDP setup
---

## Phase 1: Input Extraction & Gap Formulation

Extracted from the request: the model has grown to 6.7B parameters and no
longer fits under single-node `DistributedDataParallel` (8x GPUs) even at
micro-batch size 1, and the team's initial plan already proposes "switch to
FSDP across 2 nodes" without having measured which memory term is actually
binding.

Checked this against `references/parallelism-strategy.md`'s "Diagnosing the
binding constraint" guidance: it explicitly warns against adding a
parallelism dimension before knowing which term is binding, and lists
"Adding FSDP to a run that was activation-bound, and gaining nothing" as a
common failure. The initial plan has no memory breakdown at all - it jumped
straight from "OOM under DDP" to "use FSDP" without measuring whether
parameters, optimizer states, or activations are the actual binding term, and
there is no existing single-node DDP step-time baseline to compare the new
setup's cost against.

**Gate:** proceed to Phase 2 only once the binding memory term is measured
(not assumed) via a memory breakdown at the current batch size, and a
measured single-node DDP step-time number exists for comparison, per
`parallelism-strategy.md`'s "Diagnosing the binding constraint" and
"Deliverables".

## Phase 2: Draft Synthesis

Measured the memory breakdown at micro-batch size 1: optimizer states (AdamW
moment estimates, fp32 master weights) account for 61% of per-GPU memory,
parameters 24%, activations 9%, the rest overhead - matching
`parallelism-strategy.md`'s "Optimizer states dominate (large model, small
batch) -> ZeRO-1/2" case, not the parameter- or activation-dominated cases.

Drafted the migration plan against that file's "Deliverables" list: chosen
factorization is FSDP full-shard (sharding parameters, gradients, and
optimizer state together, the ZeRO-3-equivalent option, since sharding
optimizer state alone under ZeRO-1/2 was measured to still exceed per-GPU
memory at the target batch size) across 2 nodes x 8 GPUs, with no tensor or
pipeline parallelism added, since no single layer was identified as a
per-layer bottleneck. The migration mechanics themselves follow
`references/distributed-training.md`'s "Essentials" checklist: read
`LOCAL_RANK`/`RANK`/`WORLD_SIZE`, use `DistributedSampler` with
`set_epoch()` per epoch, save checkpoints only on rank 0, and properly
destroy the process group at shutdown.

**Gate:** proceed to Phase 3 only once the chosen factorization
(`TP x PP x DP` against `world_size`) is stated explicitly and its product
matches the actual GPU count - `parallelism-strategy.md` notes this
mismatch "typically hangs at init rather than failing," which would be an
expensive way to discover it.

## Phase 3: Red-Team Review & Final Artifact Packaging

Stress-tested the assumption that "the validation metric reported by the new
multi-node FSDP run is directly comparable to the old single-node numbers."
This assumption did not hold: the evaluation loop computes accuracy as a
running mean local to each process and only rank 0's number was ever logged.
On the old single-node run this was invisible, because rank 0's local
subset happened to be the *entire* evaluation set run through a single
process. On the new 2-node, 16-GPU setup, rank 0 only sees 1/16th of the
validation set, so the logged "validation accuracy" silently became a small,
unrepresentative subset instead of the full aggregate - exactly the gap
`references/distributed-training.md`'s "Metric aggregation" section exists
to close ("use `dist.all_reduce` to aggregate sums and counts across
processes").

Fixed the eval loop to accumulate per-rank sums and counts, `all_reduce`
them, and compute the metric once on the aggregated totals. Re-ran a small
2-node dry run and confirmed the corrected metric now matches the known
single-node baseline value within statistical noise on a shared held-out
slice, whereas the uncorrected per-rank metric had overstated variance
run-to-run by more than 4x (an artifact of averaging over 1/16th of the data
rather than the whole set).

**Gate:** merge and begin the full-scale multi-node run only once the
corrected, all-reduced evaluation metric on the small-scale dry run matches
the single-node baseline within statistical noise - this is the release
criterion, not the factorization choice from Phase 2 alone.
