---
role: Principal ML Engineer
skill: deep-learning
archetype: elicitation
user_request: "Can you fix the model's accuracy?"
---

## 1. Raw Ambiguous Input

Message from a product owner, forwarded from a customer success meeting:

> Can you fix the model's accuracy? Sales says customers are noticing wrong
> predictions.

No metric named, no baseline number, no target, and no indication of
whether the problem is everywhere or concentrated in one segment.

## 2. Missing Constraint Analysis

Per `references/evaluation-strategy.md`, "evaluate against the decision,
not the benchmark" - "accuracy" is ambiguous on two axes at once: which
metric actually matches what the model's output causes to happen (plain
accuracy, F1, calibration, or something asymmetric if false positives and
false negatives have different costs), and whether the complaint is an
aggregate regression or a slice-specific failure the aggregate number is
hiding (per the doc's "slices matter more than the aggregate"). Fixing the
wrong metric, or optimizing the aggregate while an important slice stays
broken, would not resolve the actual customer complaint.

Specifically missing:
- **Which metric** actually reflects the customer-visible failure - "wrong
  predictions" could mean low precision (false alarms), low recall (missed
  cases), or poor calibration (confident but wrong).
- **Current baseline and target** - no number for where the metric stands
  today or what "fixed" means quantitatively.
- **Slice concentration** - whether this is a global regression or
  concentrated in a specific customer segment, input type, or region -
  the fix and its urgency differ sharply between the two.
- **Acceptable tradeoffs** - whether a latency, cost, or model-size
  regression is acceptable if it's the price of hitting the accuracy
  target.

## 3. Socratic Clarification Round

1. What kind of "wrong" is being reported?
   a) False alarms - the model flags things that turn out fine (precision
      problem)
   b) Missed cases - the model fails to flag things that turn out to be
      real (recall problem)
   c) Confident-but-wrong predictions - the model's stated confidence
      doesn't match its actual correctness (calibration problem)
   d) Not yet characterized - customer success only has qualitative
      complaints so far
2. What is the current baseline value and target for the relevant metric?
   a) Baseline is known (e.g. current F1 = 0.81); no explicit target yet
   b) Baseline is known and a target has been set (e.g. F1 >= 0.90, per an
      internal SLA)
   c) Neither is known - this would need to be measured first
3. Is the problem concentrated in one segment or spread across all traffic?
   a) Spread evenly across all traffic - a genuine aggregate regression
   b) Concentrated in one customer segment or input type
   c) Not yet analyzed by slice
4. Is any tradeoff (latency, cost, model size) acceptable to hit the
   accuracy target?
   a) No - latency and cost budgets are fixed and cannot move
   b) A modest latency/cost increase is acceptable if it meaningfully
      improves accuracy
   c) Not sure - depends on how large the required change turns out to be

## 4. User Feedback Integration

The product owner's answers, after pulling three example complaints from
the support queue:

- Q1 -> **b) Missed cases.** All three example complaints are cases the
  model should have flagged but didn't - a recall problem, not false
  alarms or calibration.
- Q2 -> **a) Baseline known, no explicit target yet.** Current recall is
  0.74 on the standing validation set; no SLA target exists for this
  specific metric yet.
- Q3 -> **b) Concentrated in one segment.** All three complaints come from
  the same customer segment (enterprise accounts using a specific input
  format); recall on that segment specifically is 0.52, versus 0.81 on the
  rest of traffic.
- Q4 -> **b) A modest increase is acceptable.** Product confirms up to a
  10% latency increase is acceptable if it closes the segment-specific
  recall gap.

Each answer resolves one gap from section 2: Q1 names the actual metric at
fault (recall, not precision or calibration), Q2 supplies the current
baseline even though no target existed yet, Q3 reveals the aggregate number
(0.74) was masking a much worse segment-specific number (0.52) exactly as
`evaluation-strategy.md` warns, and Q4 confirms a latency tradeoff is
available to close that gap.

## 5. Final Mutually-Agreed Specification Document

**Outcome:** Raise recall on the enterprise-segment, specific-input-format
slice from 0.52 to at least 0.75, without regressing recall on the rest of
traffic below its current 0.81, and within a 10% latency budget increase.

**In scope:** Diagnosing why the segment-specific slice underperforms
(e.g. an underrepresented input format in training data), a slice-targeted
fix (additional training examples, a slice-aware threshold, or a
architecture change if needed), and a per-slice evaluation report per
`evaluation-strategy.md`'s "slices matter more than the aggregate."

**Out of scope:** Precision or calibration work - the confirmed complaint
is specifically about missed cases (recall), and addressing an unreported
metric would not resolve the actual customer complaint.

**Acceptance criteria (given/when/then):**
- Given the fix, when evaluated on the held-out validation set, then
  recall on the enterprise-segment slice is at least 0.75, with the slice's
  sample size reported alongside the metric per `evaluation-strategy.md`.
- Given the fix, when evaluated on the rest of traffic, then recall stays
  at or above 0.81 - no regression on the non-enterprise slice.
- Given the fix is deployed, when latency is measured in production, then
  the increase is no more than 10% over the current baseline.
- Given the ship decision, when the evaluation report is written, then it
  explicitly states what (if anything) got worse, per
  `evaluation-strategy.md`'s ship-criteria guidance.

**Explicit non-goals:** This does not pursue a precision or calibration
improvement in this pass, and does not commit to a zero-latency-cost
solution - a modest, bounded latency tradeoff has been explicitly approved
in exchange for closing the segment-specific recall gap.
