---
role: Site Reliability / Principal Machine Learning Engineer
skill: deep-learning
archetype: postmortem
incident: Multi-day distributed training run diverges/crashes at hour 30 (NaN loss, NCCL timeout)
---

## 1. Incident Symptom & Alert Payload

```
ALERT [FIRING] training-job-stalled
job: llm-pretrain-7b-run14
rank: 3/32
duration_since_last_step: 612s (threshold: 300s)

--- tail of rank 3 stderr ---
[hour 24, step 118_402] loss=1.842
[hour 24, step 118_403] loss=1.839
[hour 24, step 118_404] loss=nan
[hour 24, step 118_405] loss=nan
[hour 24, step 118_406] loss=nan
... (continues logging nan for 5h51m, no abort)
[hour 30, step 121_988] RuntimeError: NCCL watchdog thread terminated with
  exception: [Rank 3] Watchdog caught collective operation timeout:
  WorkNCCL(SeqNum=118406, OpType=ALLREDUCE) ran for 600017 milliseconds
  before timing out.
```

The job ran for 30 hours across 32 GPUs (4 nodes x 8) before the on-call
engineer was paged - not by the NaN loss itself, but by the downstream NCCL
collective timeout six hours later.

## 2. Immediate Triage & Blast-Radius Mitigation

Per `references/training-at-scale.md`'s guidance that "a diverged run can
burn a day before anyone looks," the on-call engineer's first action was to
kill the job outright rather than attempt to debug it live - the last six
hours of compute (hour 24 to hour 30) were already lost to NaN propagation,
so there was no in-progress state worth preserving. The job was resubmitted
from the last checkpoint *prior to* the NaN onset (hour 18's checkpoint, not
hour 24's, since intermediate checkpoints between hour 18 and 24 were
already contaminated by the same corrupted optimizer state that caused the
divergence) with training paused pending root-cause analysis, avoiding
burning further GPU-hours on a run that would reproduce the same failure.

## 3. 5-Whys Root Cause Deep-Dive

1. **Why did the run crash with an NCCL collective timeout at hour 30?**
   Because rank 3 had been producing NaN gradients since hour 24, and once
   its parameters became NaN, its per-step compute time became erratic
   enough that it fell far enough behind the other 31 ranks for their
   shared all-reduce to exceed the 600-second collective timeout.
2. **Why did rank 3 start producing NaN gradients at hour 24?** Because the
   mixed-precision loss scaler's scale factor was pinned at its default
   initial value (65536) instead of the much lower value (256) it had
   converged to by hour 18 through normal dynamic-scaling backoff, causing
   gradient overflow on the first large-loss batch after hour 18.
3. **Why was the scaler pinned at its default instead of its converged
   value?** Because the job was preempted and automatically resubmitted at
   hour 18 (a routine, expected preemption on this cluster's spot-priority
   queue), and the checkpoint it resumed from did not include the
   `GradScaler`'s internal state, so the resumed process re-initialized the
   scaler from scratch.
4. **Why did the checkpoint not include the `GradScaler` state?** Because
   mixed-precision training was added to this pipeline after the checkpoint
   save/load functions were originally written, and per
   `references/training-at-scale.md`'s "checkpoints must be resumable, not
   just loadable" guidance (model, optimizer, scheduler, step count,
   dataloader position, and RNG state), the `GradScaler`'s state was never
   added to that list when AMP was integrated - an incomplete migration,
   not a one-off mistake.
5. **Why did six hours of NaN losses run to completion instead of aborting
   immediately?** Because the training loop logged `loss.item()` every step
   without checking `math.isfinite()`, exactly the gap
   `references/training-at-scale.md` names directly: "fail loudly on NaN...
   check loss finiteness every step and abort, rather than logging and
   continuing." The loop did the latter for 6 hours and ~3,600 wasted steps
   before an unrelated downstream symptom (the NCCL timeout) finally forced
   a stop.

Root cause: an incomplete checkpoint-schema migration (GradScaler state
omitted when mixed precision was added) combined with the absence of a
per-step NaN-abort check, so a routine, expected preemption silently
corrupted the numerical state of the run, and nothing detected the
resulting divergence for six hours.

## 4. Permanent Surgical Fix (Diff)

```diff
--- a/training/checkpoint.py
+++ b/training/checkpoint.py
@@ -10,6 +10,7 @@ def save_checkpoint(path, model, optimizer, scheduler, scaler, step, rng_state
     torch.save({
         "model": model.state_dict(),
         "optimizer": optimizer.state_dict(),
         "scheduler": scheduler.state_dict(),
+        "scaler": scaler.state_dict(),
         "step": step,
         "rng_state": rng_state,
     }, tmp_path)
@@ -22,6 +23,7 @@ def load_checkpoint(path, model, optimizer, scheduler, scaler):
     ckpt = torch.load(path, map_location="cpu")
     model.load_state_dict(ckpt["model"])
     optimizer.load_state_dict(ckpt["optimizer"])
     scheduler.load_state_dict(ckpt["scheduler"])
+    scaler.load_state_dict(ckpt["scaler"])
     return ckpt["step"], ckpt["rng_state"]
```

```diff
--- a/training/train_loop.py
+++ b/training/train_loop.py
@@ -40,6 +40,10 @@ for step in range(start_step, total_steps):
     loss = compute_loss(model, batch)
+    if not torch.isfinite(loss):
+        logger.error(f"non-finite loss at step {step}: {loss.item()}")
+        raise SystemExit(f"aborting: non-finite loss at step {step}")
     scaler.scale(loss).backward()
     scaler.step(optimizer)
     scaler.update()
```

## 5. Blameless Postmortem & Preventative Monitoring Rules

No individual is at fault: the engineer who added mixed-precision support
followed the existing checkpoint function's signature and had no reason to
audit every call site for a full list of "everything that needs to survive
a resume" - that list was implicit, not enforced anywhere. The gap is a
missing systemic guardrail (a NaN-abort check, a checkpoint-completeness
test), not a lapse in individual diligence.

**What worked:** killing the job immediately on triage, without trying to
diagnose the NCCL timeout live, avoided burning additional GPU-hours on a
run already known to be unrecoverable.

**What didn't work:** the six-hour gap between the actual failure (NaN at
hour 24) and the alert that finally paged someone (the NCCL timeout at hour
30) meant the true failure was invisible to monitoring for the entire
window it was actually happening.

**Preventative monitoring rule:** alert and automatically abort the job
(not just log) if `loss` is non-finite for 1 step, paging the run's owning
team immediately rather than waiting for a downstream symptom like a
collective timeout to surface six hours later.
