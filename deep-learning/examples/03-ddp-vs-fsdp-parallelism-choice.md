---
role: Distributed Training / ML Infrastructure Architect
skill: deep-learning
use_case: choosing a parallelism strategy for fine-tuning a large language model that no longer fits under plain DDP
---

## Scenario

A team is fine-tuning a 7B-parameter decoder-only Transformer (32 layers,
hidden size 4096, 32 heads) on 8 GPUs with 80 GB each, mixed precision with
Adam, sequence length 4096, and a micro-batch of 2 per GPU with selective
activation recomputation. The previous model they fine-tuned was small enough
that wrapping it in `DistributedDataParallel` and moving on was the right call;
this one OOMs.

## Common Weak Approach

The team reuses the same DDP setup that worked for the smaller model, and
"fixes" the resulting OOM the same way each time it recurs - by cutting the
micro-batch further, which only delays the same failure at a different batch
size and does not answer what is actually running out of memory:

```python
import torch
import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP

def setup_ddp(model, local_rank):
    torch.cuda.set_device(local_rank)
    dist.init_process_group("nccl")
    model = model.to(local_rank)
    return DDP(model, device_ids=[local_rank])


# micro_batch tried: 8 -> OOM, 4 -> OOM, 2 -> OOM, 1 -> OOM.
# Each retry burns a full node-allocation cycle; no one has checked what the
# per-GPU memory budget actually is for this parameter count.
model = setup_ddp(build_model(layers=32, hidden=4096), local_rank)
optimizer = torch.optim.AdamW(model.parameters(), lr=3e-4)
```

Even at micro-batch 1 the run still OOMs, because DDP replicates the full
optimizer state on every GPU and the team never checked whether that
replication fits before writing the training script - no micro-batch size can
fix a term that doesn't scale with batch size at all.

## Expert-Level Best Practice

The architect computes the per-GPU memory budget before choosing a strategy,
using this skill's own `scripts/estimate_training_memory.py`, rather than
discovering the binding constraint through repeated OOMs:

```bash
python3 scripts/estimate_training_memory.py \
  --params 7e9 --layers 32 --hidden 4096 --heads 32 \
  --seq-len 4096 --micro-batch 2 --gpus 8 --gpu-memory-gb 80 \
  --precision mixed --optimizer adam --zero-stage 0 --recompute selective
```

```
Per-GPU memory:
  parameters       13.04 GB  ( 9.4%)
  gradients        13.04 GB  ( 9.4%)
  optimizer        78.23 GB  (56.6%)
  activations      34.00 GB  (24.6%)
  TOTAL           138.31 GB  (172.9% of 80 GB)

Binding term:      optimizer
Does not fit: 138.3 GB needed vs 80.0 GB available.
Optimizer states dominate. ZeRO-1 shards them across the data-parallel group at little communication cost.
```

This confirms the DDP failure mode directly: at mixed precision + Adam, each
parameter costs 16 bytes across parameters+gradients+optimizer (2+2+12, per
this skill's `references/parallelism-strategy.md`), and DDP replicates all of
it on every GPU. The 78.23 GB optimizer term alone is 98% of the 80 GB budget,
before a single activation is counted - no micro-batch reduction touches that
term, which is why the retries in the weak approach never worked. Re-running
with full parameter/gradient/optimizer sharding (ZeRO-3 / FSDP full shard)
shows what actually fits:

```bash
python3 scripts/estimate_training_memory.py \
  --params 7e9 --layers 32 --hidden 4096 --heads 32 \
  --seq-len 4096 --micro-batch 2 --gpus 8 --gpu-memory-gb 80 \
  --precision mixed --optimizer adam --zero-stage 3 --recompute selective
```

```
Per-GPU memory:
  parameters        1.63 GB  ( 3.5%)
  gradients         1.63 GB  ( 3.5%)
  optimizer         9.78 GB  (20.8%)
  activations      34.00 GB  (72.3%)
  TOTAL            47.04 GB  (58.8% of 80 GB)

Binding term:      activations
Fits as configured.
```

Full sharding drops the total to 47.04 GB (58.8% of the 80 GB budget) with
comfortable headroom, and correctly reports that the binding term has now
*flipped* from optimizer state to activations - so the next lever to pull, if
more headroom is needed, is recomputation mode or microbatch size, not further
sharding. The architect wires this up with `FullyShardedDataParallel`, sharding
at transformer-block granularity (not the whole model as one unit, which would
serialize the per-layer all-gather/reduce-scatter that lets FSDP overlap
communication with compute) and selective activation recomputation, matching
exactly the configuration the estimate was run for:

```python
import torch
import torch.distributed as dist
from torch.distributed.fsdp import FullyShardedDataParallel as FSDP
from torch.distributed.fsdp.wrap import transformer_auto_wrap_policy
from torch.utils.checkpoint import checkpoint
from functools import partial

def setup_fsdp(model, local_rank, transformer_block_cls):
    torch.cuda.set_device(local_rank)
    dist.init_process_group("nccl")
    wrap_policy = partial(
        transformer_auto_wrap_policy,
        transformer_layer_cls={transformer_block_cls},
    )
    return FSDP(
        model.to(local_rank),
        auto_wrap_policy=wrap_policy,
        device_id=local_rank,
        mixed_precision=torch.distributed.fsdp.MixedPrecision(
            param_dtype=torch.float16,
            reduce_dtype=torch.float32,   # gradient all-reduce accumulates in fp32
            buffer_dtype=torch.float16,
        ),
    )


class TransformerBlock(torch.nn.Module):
    def __init__(self, attn, mlp):
        super().__init__()
        self.attn, self.mlp = attn, mlp

    def forward(self, x, mask):
        # Selective recomputation: only the attention sub-block is recomputed
        # in the backward pass, matching --recompute selective above.
        x = x + checkpoint(self.attn, x, mask, use_reentrant=False)
        x = x + self.mlp(x)
        return x


model = setup_fsdp(build_model(layers=32, hidden=4096), local_rank, TransformerBlock)
optimizer = torch.optim.AdamW(model.parameters(), lr=3e-4)
```

The change is justified by the two estimator runs, not by trial and error: the
team can now state which term was binding before sharding (optimizer, 78.23 GB),
which term binds after (activations, 34.00 GB), and that the 8-GPU x 80 GB
budget was never going to work under DDP at any micro-batch size for a
7B-parameter model at this precision and optimizer.

## Key Takeaways

- Compute the four-term memory budget (parameters + gradients + optimizer +
  activations) before choosing a parallelism strategy, instead of discovering
  the binding term through repeated OOMs. `scripts/estimate_training_memory.py`
  turns "try a smaller batch" into "the optimizer term is 78.23 GB and no batch
  size changes that."
- Mixed precision does not halve training memory. At mixed precision + Adam,
  the fp32 master weights and moments make the optimizer term dominate (78.23
  of 138.31 GB above, per the 2+2+12 bytes/param breakdown in
  `references/parallelism-strategy.md`) - the two smaller (2-byte) parameter
  and gradient terms are not where the failure comes from.
- A parallelism decision must re-check the binding term after each change, not
  just whether the run now fits. Full sharding fixed the OOM here, but it also
  flipped the binding term from optimizer state to activations (34.00 of 47.04
  GB) - the next capacity problem in this same run would need recomputation or
  batch tuning, not more sharding, and the estimator's "binding term" line is
  what tells you that instead of another guess.
- Shard at a wrap-unit granularity that matches how the model is actually
  structured (per-transformer-block via `transformer_auto_wrap_policy`), not
  the whole model as a single FSDP unit - block-level sharding is what lets
  FSDP overlap each block's parameter all-gather with the previous block's
  compute; wrapping the whole model serializes that and gives up most of the
  overlap FSDP is chosen for in the first place.
