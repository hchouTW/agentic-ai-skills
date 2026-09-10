---
role: Principal ML Systems Engineer
skill: deep-learning
archetype: gated-pipeline
high_stakes_task: proposing and evaluating a new Transformer-encoder architecture to replace an LSTM baseline for a long-sequence tagging model
---

## Phase 1: Input Extraction & Gap Formulation

Extracted from the proposal request: the current production sequence tagger
is a 2-layer LSTM; sequence lengths have grown from a median of 180 tokens to
1,400 tokens as the product expanded to longer documents, and the team
suspects the LSTM's bounded recurrent state is now the limiting factor.

Checked the draft proposal against `references/architecture-selection.md`'s
"Reviewing an architecture proposal" checklist and found real gaps, not just
missing polish:
- No parameter count, training cost, or inference latency was stated for
  either model.
- The LSTM baseline in the proposal's comparison had not been re-tuned at the
  new sequence length - it was using the same learning rate chosen for
  180-token sequences.
- No measured evidence yet that recurrence, not something else, is the
  binding constraint.

**Gate:** proceed to Phase 2 only once the LSTM baseline has been re-tuned at
the current sequence length (not just reused from the old setting) and
parameter count/training cost/inference latency are measured for both
candidates, per `references/architecture-selection.md`'s explicit checklist
items.

## Phase 2: Draft Synthesis

Re-tuned the LSTM baseline's learning rate at 1,400-token sequences (a 3x
increase from the original, following a small sweep) before drafting the
comparison, then completed the proposal against
`references/architecture-selection.md`'s "Match inductive bias to data
structure" table: "Long-range dependence, variable-length" data structure
maps to "Global mixing, content-based routing" bias, typically a Transformer
- directly matching this task, where the LSTM's bounded recurrent state must
propagate information across 1,400 steps while a Transformer attends across
the full sequence directly.

Stated per the "Reviewing an architecture proposal" checklist: parameter
count (LSTM: 34M; Transformer encoder: 41M), training FLOPs (Transformer
~1.6x the LSTM's at this sequence length, from attention's quadratic term),
and inference p99 latency measured on the same hardware (LSTM: 42ms;
Transformer: 58ms, still inside the serving budget). The retuned LSTM
baseline reaches 89.1% tag-level F1; the initial Transformer run reaches
91.2%.

**Gate:** proceed to Phase 3 only once every deliverable in
`architecture-selection.md`'s checklist has a number attached (not "roughly"
or "should be fine"), and the re-tuned baseline's result, not the stale one,
is what the comparison uses.

## Phase 3: Red-Team Review & Final Artifact Packaging

Stress-tested the proposal's central claim - "the Transformer's +2.1 F1
point improvement over the retuned LSTM baseline is a real architectural
effect" - against `references/ablation-and-design-review.md`'s "Seed
variance is the floor" guidance, which the initial comparison had skipped:
it compared a single LSTM run against the *best of three* Transformer runs.

Re-ran both models across 5 seeds each. The retuned LSTM baseline's own
seed-to-seed spread turned out to be +/-1.6 F1 points; the Transformer's
spread was +/-1.1 points. Comparing the two seed distributions directly
(paired on the same validation splits, per that section's "use paired
comparisons" guidance) gives a mean gap of 0.9 F1 points with overlapping
intervals - the initial 2.1-point claim was an artifact of best-of-3
selection on one side and a single run on the other (the assumption that
"the +2.1 point gap is a real architectural effect" does not survive this
check), not a supported result as originally drafted.

Revised the proposal's conclusion from "adopt the Transformer, +2.1 F1" to
"the current 5-seed evidence does not yet separate the two architectures at
the observed sample size; recommend either a larger, pre-registered seed
count before deciding, or a cheaper interim step (right-sizing the LSTM's
hidden dimension) that does not require an architecture change at all."

**Gate:** adopt the new architecture only once a matched-budget, multi-seed
comparison shows a mean gap that exceeds the combined seed variance of both
models - this is the actual adoption criterion, not the single best-of-N
comparison the initial draft used.
