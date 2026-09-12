---
role: Principal Software Engineer
skill: agile-development
archetype: elicitation
user_request: "Can you make the checkout faster?"
---

## 1. Raw Ambiguous Input

Slack message from the Head of Growth, posted directly to the on-call
engineering channel:

> Can you make the checkout faster? Customers keep complaining it's slow and
> I want this fixed before the Q3 board review.

No endpoint, no metric, no baseline, and no deadline other than "before the
board review" (a date not stated in the message).

## 2. Missing Constraint Analysis

Per `references/implementation-discipline.md`'s ask-vs-assume rule, this is
"work large enough that the wrong interpretation wastes substantial effort" -
"checkout" spans at least three independently-owned services (cart summary,
payment authorization, order confirmation), each with different latency
budgets and different fix classes (frontend bundle size vs. a third-party
payment-gateway round trip vs. a synchronous email send). Committing to one
without asking risks weeks of work on a step nobody complained about.

Specifically missing:
- **Which step** of checkout is actually slow - the complaint could mean any
  of the three services, or the sum of all three.
- **Baseline and target** - no current latency number and no numeric
  definition of "fast enough" exist yet.
- **Load condition** - whether this is a steady-state problem or only shows
  up under a specific traffic pattern (e.g. a flash-sale spike) changes
  whether the fix is algorithmic or a capacity/scaling fix.
- **Urgency class** - whether this is a new regression (implying a recent
  deploy broke something and should be triaged as an incident) or a
  longstanding gap now getting exec attention (implying a scoped project,
  not a hotfix).

## 3. Socratic Clarification Round

1. Which part of checkout is reported slow?
   a) The cart summary page load
   b) The payment authorization step
   c) The order confirmation / receipt step
   d) Overall time-to-purchase across the whole flow, no single step singled out
2. What's the current baseline latency, and is there a numeric target?
   a) No baseline measured yet - would need to instrument first
   b) p95 is ~4.2s from existing RUM (real-user monitoring) data, no target set
   c) p95 is ~4.2s, and the Q3 OKR states a target of "checkout under 2s p95"
3. Under what load does the slowness show up?
   a) All traffic, all the time, at any volume
   b) Only under peak load (e.g. a flash-sale spike at ~10x normal traffic)
   c) Only for a specific segment (e.g. mobile clients, or one payment method)
4. Is this a sudden regression or a longstanding gap?
   a) Sudden regression since a recent deploy - should be triaged as an incident
   b) Longstanding slowness that's never been prioritized until now
   c) Tied to a hard external deadline (the board review), independent of when it started

## 4. User Feedback Integration

The Head of Growth's answers, received in the same thread:

- Q1 -> **b) The payment authorization step.** Support tickets and the RUM
  dashboard both point at the "Confirm and Pay" click-to-response time, not
  the cart or confirmation pages.
- Q2 -> **c) p95 is ~4.2s, and the Q3 OKR states a target of "checkout under
  2s p95."** The OKR document was linked; it names payment authorization
  specifically.
- Q3 -> **b) Only under peak load.** During the last two flash sales, p95
  latency for this step spiked from ~1.8s (normal) to ~4.2s (peak, ~10x
  traffic) - it is not slow at steady state.
- Q4 -> **b) Longstanding gap.** No recent deploy correlates with the
  slowness; this has been true for at least two quarters and is now
  prioritized because of the OKR, not because something broke.

Each answer resolves one gap from section 2: Q1 names the step, Q2 supplies
both the baseline and the numeric target, Q3 identifies the load condition
that reproduces the problem, and Q4 confirms this is scoped project work
(not an incident) with the board review as a soft deadline, not a hard
regression-response SLA.

## 5. Final Mutually-Agreed Specification Document

**Outcome:** Reduce the payment-authorization step's p95 latency from ~4.2s
to under 2s, specifically under peak load (~10x normal traffic, as observed
during a flash sale), matching the Q3 OKR target.

**In scope:** The payment-authorization service and its synchronous
dependencies (the request path from "Confirm and Pay" click to a
success/failure response).

**Out of scope:** Cart summary and order-confirmation steps - no complaint or
OKR target references them, and bundling them in would exceed the smallest
coherent slice for this OKR item.

**Acceptance criteria (given/when/then):**
- Given peak load equivalent to the last flash sale (~10x normal request
  volume), when a customer submits payment authorization, then p95 latency
  is under 2s, measured by the existing RUM dashboard for this endpoint.
- Given steady-state (normal) load, then p95 latency for this step does not
  regress above its current ~1.8s baseline.

**Explicit non-goals:** This does not commit to fixing cart or confirmation
latency, and does not treat this as an active incident - no rollback or
customer-facing status update is warranted, since this is scoped
optimization work against an OKR, not a live regression.
