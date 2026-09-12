---
role: Principal ML Engineer
skill: deep-learning
archetype: elicitation
user_request: "Can you make training faster?"
---

## 1. Raw Ambiguous Input

Message from a research lead, posted in the ML team's channel:

> Can you make training faster? We're burning too much GPU time on this run.

No profiling data attached, no target speedup, and no statement of whether
accuracy or exact reproducibility must be held constant.

## 2. Missing Constraint Analysis

Per `references/performance-memory.md`'s "first checks," "training is slow"
has at least three structurally different root causes - a data-loading
bottleneck (GPU idles waiting for batches), a compute bottleneck (GPU is
saturated but the model itself is doing more FLOPs than necessary), or a
communication bottleneck (in a distributed job, GPUs wait on gradient
all-reduce). Each has a different fix, and applying the wrong one (e.g.
adding `torch.compile` to a dataloader-bound job) wastes effort without
moving the needle.

Specifically missing:
- **Where the bottleneck actually is** - no GPU-utilization or step-time
  breakdown has been shared; without one, any proposed fix is a guess.
- **Whether this is single-GPU or distributed** - a communication bottleneck
  (per `distributed-training.md`, out of this ticket's referenced doc but
  relevant if this is DDP/FSDP) only exists in a multi-GPU job.
- **Target speedup or budget** - "too much GPU time" has no number; a 10%
  win and a 3x win call for very different levels of effort (config tweaks
  vs. a training-loop rewrite).
- **Reproducibility/accuracy constraints** - some speedups (e.g. mixed
  precision, changing `num_workers` ordering) can change numerical results
  slightly; whether that's acceptable changes which optimizations are in
  scope.

## 3. Socratic Clarification Round

1. Is GPU utilization actually the bottleneck, or is the GPU idling?
   a) GPU utilization is already near 100% - the model itself is
      compute-bound
   b) GPU utilization is low (e.g. under 50%) - it's idling, likely
      waiting on data loading
   c) Not measured yet - no profiling has been done
2. Is this a single-GPU job or a distributed (multi-GPU) job?
   a) Single GPU
   b) Multi-GPU on one machine (DDP)
   c) Multi-node distributed training
3. What speedup or time budget is actually needed?
   a) A modest win (e.g. 10-20%) from low-effort config changes is enough
   b) A large win (e.g. 2-3x) is needed - likely requires a training-loop
      or data-pipeline change, not just config tuning
   c) Not sure - whatever's achievable without much engineering time
4. Must accuracy and exact numerical reproducibility stay unchanged?
   a) Yes - the current run's accuracy and seed-reproducibility must not
      change at all
   b) Accuracy must stay within noise (e.g. current variance across seeds)
      but exact bitwise reproducibility isn't required
   c) Some accuracy tradeoff is acceptable if the speedup is large enough

## 4. User Feedback Integration

The research lead's answers, after running a quick profiling pass:

- Q1 -> **b) GPU utilization is low, ~35%.** A quick `nvidia-smi` check
  during training shows the GPU idling between batches.
- Q2 -> **a) Single GPU.** This run is not distributed, so communication
  overhead is ruled out as a cause.
- Q3 -> **b) A large win, ~2-3x, is needed.** The run currently takes 14
  hours per epoch and needs to fit in an overnight batch window.
- Q4 -> **b) Accuracy within noise, exact reproducibility not required.**
  The team compares runs by validation-metric distribution across seeds,
  not by bitwise-identical output.

Each answer resolves one gap from section 2: Q1 confirms the bottleneck is
data loading, not compute, so the fix targets the dataloader rather than
the model; Q2 rules out a distributed-communication cause entirely; Q3
sets a concrete target (2-3x) that justifies a data-pipeline change rather
than only config tuning; and Q4 permits `pin_memory`/worker-count changes
and mixed precision without requiring bitwise-identical reruns.

## 5. Final Mutually-Agreed Specification Document

**Outcome:** Increase per-epoch training throughput by at least 2x
(from ~14 hours to under 7 hours per epoch) by resolving the data-loading
bottleneck, without degrading validation-metric performance beyond the
run's existing seed-to-seed variance.

**In scope:** Increasing `num_workers` until throughput stops improving,
enabling `pin_memory=True` (per `performance-memory.md`'s data-loading
checklist), moving any expensive CPU-side transforms out of the hot path,
and enabling mixed-precision training (`GradScaler`) given accuracy-within-
noise is acceptable.

**Out of scope:** Model-architecture changes, distributed training
(single-GPU only, per Q2), and `torch.compile` - the bottleneck is
data-loading, not compute, so compiling the model would not address the
measured 35% GPU utilization.

**Acceptance criteria (given/when/then):**
- Given the same dataset and model, when training runs after the change,
  then GPU utilization during steady-state training is at or above 85%
  (up from the measured ~35%).
- Given the change, when a full epoch completes, then wall-clock time is
  under 7 hours (down from ~14 hours), measured on the same hardware.
- Given 3 training runs with different seeds after the change, when
  validation metrics are compared to the pre-change baseline's seed
  variance, then the post-change distribution falls within that existing
  variance - no systematic degradation.

**Explicit non-goals:** This does not pursue distributed training or
`torch.compile` in this pass - both are ruled out by the confirmed
single-GPU, data-loading-bound diagnosis, and revisiting them would be a
separate ticket if the data-loading fix alone doesn't reach the 2x target.
