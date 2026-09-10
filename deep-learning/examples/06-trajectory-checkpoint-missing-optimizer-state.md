---
role: Senior ML Systems Engineer
skill: deep-learning
archetype: trajectory
problem_input: a training run resumed from a periodic checkpoint whose loss immediately jumps upward and takes thousands of steps to recover, instead of continuing smoothly
---

## 1. Task Input & Context

Incident note from the training infrastructure on-call:

> A 3-day pretraining job was resumed from checkpoint `step_180000.pt` after a
> planned cluster maintenance window. Loss was at 2.41 right before the
> maintenance window. Immediately after resuming, loss jumps to 3.98 and takes
> roughly 2,000 steps to fall back below 2.5. This has happened on every
> resume of this job, not just this one - the team assumed it was normal
> "warmup after a restart" and had been absorbing the wasted compute.

The checkpoint file is written every 5,000 steps by a function the team
describes as "the one that saves the model so we can pick this back up
later."

## 2. Root-Cause Triage & Action Plan

Comparing the actual checkpoint-writing code against
`references/checkpointing.md`'s two documented patterns shows which one is in
use:

```python
# checkpoint_utils.py, as currently written
def save_checkpoint(model, path):
    torch.save(model.state_dict(), path)
```

This is `checkpointing.md`'s "Inference-only weights" pattern - it saves only
`model.state_dict()`. The resume code loads it and constructs a brand-new
optimizer and scheduler from scratch:

```python
model.load_state_dict(torch.load(path))
optimizer = torch.optim.AdamW(model.parameters(), lr=peak_lr)  # fresh state
scheduler = get_cosine_schedule(optimizer, warmup_steps=2000)  # restarts at step 0
```

This matches the symptom exactly: AdamW's per-parameter first/second moment
estimates (`exp_avg`, `exp_avg_sq`) reset to zero on every resume, so the
optimizer takes a few thousand steps to rebuild the same adaptive step sizes
it had before the restart - the "jump then 2,000-step recovery" pattern. The
scheduler also restarts its own step count at 0, briefly re-applying warmup
partway through training. Both effects compound at every resume, and the team
had been treating the resulting wasted compute as expected behavior rather
than a bug.

Action plan: switch `save_checkpoint`/the resume path to
`checkpointing.md`'s "Save training checkpoint" / "Resume training" pattern,
which persists and restores `optimizer_state_dict` and `scheduler_state_dict`
(and the step/epoch count) alongside the model weights, and verify by
resuming a short run from a mid-training checkpoint and confirming the loss
curve shows no discontinuity at the resume boundary.

## 3. Surgical Execution

```diff
 def save_checkpoint(model, path):
-    torch.save(model.state_dict(), path)
+def save_checkpoint(model, optimizer, scheduler, step, path):
+    torch.save({
+        "step": step,
+        "model_state_dict": model.state_dict(),
+        "optimizer_state_dict": optimizer.state_dict(),
+        "scheduler_state_dict": scheduler.state_dict(),
+    }, path)

-model.load_state_dict(torch.load(path))
-optimizer = torch.optim.AdamW(model.parameters(), lr=peak_lr)
-scheduler = get_cosine_schedule(optimizer, warmup_steps=2000)
+ckpt = torch.load(path, map_location=device)
+model.load_state_dict(ckpt["model_state_dict"])
+optimizer = torch.optim.AdamW(model.parameters(), lr=peak_lr)
+optimizer.load_state_dict(ckpt["optimizer_state_dict"])
+scheduler = get_cosine_schedule(optimizer, warmup_steps=2000)
+scheduler.load_state_dict(ckpt["scheduler_state_dict"])
+start_step = ckpt["step"] + 1
```

## 4. Verification Evidence

```
$ python3 train.py --resume-from checkpoints/step_180000_fixed.pt --steps 3000
step 180000  loss 2.41   (loaded from checkpoint)
step 180200  loss 2.39
step 180600  loss 2.35
step 181500  loss 2.28
step 183000  loss 2.19

$ python3 -m pytest tests/test_checkpoint_resume.py -k continuity -v
tests/test_checkpoint_resume.py::test_optimizer_state_restored_matches_pre_save PASSED
tests/test_checkpoint_resume.py::test_loss_does_not_spike_across_resume_boundary PASSED
2 passed in 1.84s
```

No jump: loss continues its pre-maintenance downward trend immediately after
the resume step, in contrast to the previous jump-to-3.98-then-2000-step
recovery pattern.

## 5. Final Deliverable Summary

Traced a recurring post-resume loss spike to a checkpoint function that saved
only inference-time model weights instead of the full training-resumable
state, silently discarding the AdamW optimizer's moment estimates and the LR
scheduler's step count on every resume. Switched to saving and restoring
`optimizer_state_dict`, `scheduler_state_dict`, and the step count alongside
the model weights, added two regression tests, and confirmed a resumed run
now continues its loss curve with no discontinuity - eliminating the
few-thousand-step recovery cost the team had been absorbing on every restart.
