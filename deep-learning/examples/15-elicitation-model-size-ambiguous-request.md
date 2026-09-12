---
role: Principal ML Engineer
skill: deep-learning
archetype: elicitation
user_request: "Can you make the model smaller?"
---

## 1. Raw Ambiguous Input

Message from an infra lead, posted in the ML platform channel:

> Can you make the model smaller? It doesn't fit on our edge devices anymore.

No target device or memory budget stated, no latency requirement, and no
statement of how much accuracy regression is tolerable.

## 2. Missing Constraint Analysis

Per `references/efficient-finetuning.md`, "make it smaller" could mean
several structurally different techniques - LoRA-style parameter-efficient
adaptation (reduces trainable/adapter size, not necessarily inference
size), post-training quantization (reduces weight precision, changes
memory and sometimes throughput), quantization-aware training (higher
accuracy at a target bit-width but requires a training pass), or
distillation into a smaller architecture entirely (changes the model
itself, not just its numeric representation). Each has a different cost,
timeline, and expected accuracy impact, and without knowing the actual
target device's memory/compute budget, none of them can be sized correctly.

Specifically missing:
- **Target deployment hardware and its memory/compute budget** - "edge
  devices" alone doesn't say whether the constraint is a few hundred MB of
  RAM, a specific NPU's supported bit-widths, or a CPU-only inference path.
- **Latency requirement** - a smaller model that's still too slow doesn't
  solve the actual deployment problem; the request only mentions size, not
  speed.
- **Accuracy regression tolerance** - quantization and distillation both
  trade some accuracy for size/speed; how much is acceptable determines
  which technique (and how aggressive a bit-width or architecture cut) is
  in scope.
- **Timeline and whether a training pass is feasible** - QAT and
  distillation require additional training runs; post-training
  quantization does not. If the deadline is tight, that rules out the
  higher-accuracy but slower-to-execute options.

## 3. Socratic Clarification Round

1. What is the target device's memory budget for the model?
   a) A specific number is known (e.g. under 200 MB total)
   b) Not an exact number, but "significantly smaller than current" is the
      goal
   c) Unknown - would need to check with the edge-device hardware team
2. Is there also a latency requirement, or is size the only constraint?
   a) Size only - current latency is acceptable
   b) Both - there's also a hard per-inference latency budget (e.g. under
      50ms on the target device's CPU)
   c) Not yet measured on the target device
3. How much accuracy regression is acceptable?
   a) None - the model must match current accuracy within noise
   b) A small regression (e.g. up to 1-2 points on the headline metric) is
      acceptable
   c) A larger regression is acceptable if it meaningfully unblocks
      deployment
4. Is a training pass (quantization-aware training or distillation)
   feasible before the deadline, or does this need a technique that
   requires no retraining?
   a) A training pass is feasible - there's time for QAT or distillation
   b) No time for retraining - needs a post-training-only technique
      (dynamic or static quantization)
   c) Deadline unclear - would need to check with the infra lead

## 4. User Feedback Integration

The infra lead's answers, after checking with the edge-device team:

- Q1 -> **a) A specific number: under 150 MB total.** The target NPU has a
  hard 150 MB model-storage limit; the current model is 480 MB.
- Q2 -> **b) Both size and latency.** The NPU also requires per-inference
  latency under 30ms; current latency on a comparable CPU benchmark is
  ~45ms.
- Q3 -> **b) A small regression, up to 1-2 points, is acceptable.** Product
  has signed off on up to a 2-point drop on the headline accuracy metric
  in exchange for shipping on-device.
- Q4 -> **b) No time for retraining.** The deadline is 3 weeks out;
  QAT or distillation's training-time requirement doesn't fit, ruling out
  those options for this pass.

Each answer resolves one gap from section 2: Q1 supplies the exact memory
target (150 MB, a >3x reduction from 480 MB), Q2 adds a latency constraint
the original request didn't mention at all, Q3 sets a concrete accuracy
budget, and Q4 rules out QAT/distillation on timeline grounds, pointing
specifically at post-training (static) quantization per
`efficient-finetuning.md`'s technique comparison.

## 5. Final Mutually-Agreed Specification Document

**Outcome:** Reduce the model from 480 MB to under 150 MB and per-inference
latency from ~45ms to under 30ms on the target NPU, via post-training
static quantization, with accuracy regression on the headline metric no
larger than 2 points.

**In scope:** Static (post-training) quantization with a calibration pass
over representative on-device input data (per
`efficient-finetuning.md`'s "Quantization" section), followed by a
same-held-out-set accuracy comparison against the unquantized baseline
before adoption.

**Out of scope:** Quantization-aware training and distillation - both
ruled out by the 3-week deadline's incompatibility with a retraining pass;
LoRA/PEFT - this is an inference-size problem for an already-trained model,
not a fine-tuning-cost problem.

**Acceptance criteria (given/when/then):**
- Given the quantized model, when its file size is measured, then it is
  under 150 MB.
- Given the quantized model on the target NPU (or a representative
  benchmark), when per-inference latency is measured, then it is under
  30ms.
- Given the quantized model, when evaluated on the same held-out set as
  the unquantized baseline, then the headline accuracy metric regresses by
  no more than 2 points.
- Given the calibration pass, when it is run, then it uses data
  representative of actual on-device traffic - per
  `efficient-finetuning.md`'s note that static-quantization accuracy
  depends on calibration-data representativeness.

**Explicit non-goals:** This does not pursue QAT or distillation in this
pass - both are explicitly deferred past the 3-week deadline as follow-up
options if static quantization alone doesn't hit the accuracy or latency
target.
