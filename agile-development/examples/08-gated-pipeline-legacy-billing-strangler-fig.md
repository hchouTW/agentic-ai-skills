---
role: Principal Software Engineer
skill: agile-development
archetype: gated-pipeline
high_stakes_task: replacing a legacy, untested billing-calculation module with a new implementation while it remains load-bearing in production
---

## Phase 1: Input Extraction & Gap Formulation

Extracted from the request: `billing/calculate.py`, a 6-year-old module with
no test suite, computes every customer's monthly invoice total (tax, prorated
plan changes, credits). It needs to be replaced because it cannot support an
upcoming multi-currency requirement, but it is still the only path that
produces real invoices today.

Gaps found before any code could be touched, per
`references/engineering-playbook.md`'s "Legacy Code Without Tests" step 1
("do not refactor and add behavior in the same change - characterize first"):
- No characterization of the module's *actual* current behavior exists -
  only the (possibly stale) original spec.
- No seam exists to run old and new logic side by side on the same request;
  the module is called directly from the request handler with no
  intervening interface.
- No decision has been made about which direction the dependency between
  billing logic and the currency-conversion service should point.

**Gate:** proceed to Phase 2 only once characterization tests exist that
record `calculate.py`'s actual current output (including any surprising
behavior, flagged rather than silently treated as correct) for a
representative sample of real invoice inputs, and a seam has been identified
or created that can route a given request to either the old or new
implementation.

## Phase 2: Draft Synthesis

Added characterization tests first, per the Legacy Code playbook: ran
`calculate.py` against 500 real (anonymized) historical invoices and recorded
its actual output as the test oracle, including one surprising behavior found
in the process - a specific multi-item credit case rounds up instead of down,
inconsistent with the module's own comments, but reproduced faithfully rather
than "fixed" at this stage, and flagged for the product owner to confirm
before Phase 3 whether that quirk needs to be preserved for existing
customers.

Introduced the seam by extracting a `BillingCalculator` interface at the
request handler's existing call site (no behavior change - `calculate.py`
becomes the sole implementation behind it), then drafted the new
implementation behind that same interface. The dependency direction for
currency conversion was decided per
`references/software-architecture.md`'s "Boundaries and dependencies"
question "which direction should the dependency point?": the new
`BillingCalculator` depends on a `CurrencyConverter` interface (billing owns
the decision of *when* to convert), rather than the reverse, so billing logic
stays testable without a live currency-service dependency - matching that
same section's "can the component still be tested independently?" question.
Rollout follows
`references/engineering-playbook.md`'s strangler-fig guidance (step 4): route
a small, explicitly-flagged slice of traffic to the new implementation while
the old one keeps serving everything else, rather than a single cutover.

**Gate:** proceed to Phase 3 only once the new implementation passes every
characterization test from Phase 1 (matching the old behavior exactly,
including the flagged rounding quirk, until the product owner explicitly
approves changing it) and the strangler-fig routing flag exists and defaults
to 100% old-implementation traffic.

## Phase 3: Red-Team Review & Final Artifact Packaging

The assumption most worth stress-testing: "routing a request to the new
implementation and the old implementation is independent per-request, so a
customer's invoices can be safely split between the two during the gradual
rollout." Testing against a customer with a mid-cycle plan change found this
assumption **false**: the old and new implementations round intermediate
proration differently, so if a customer's *first* invoice of a billing cycle
is computed by one implementation and their *correction* invoice later that
cycle is computed by the other, the two don't reconcile to the same total a
single implementation would have produced end-to-end.

As a result:
- Changed the routing flag from per-request to per-customer-per-billing-cycle,
  so a customer's invoices are never split between implementations mid-cycle.
- Added a characterization test specifically for the mid-cycle plan-change
  case, since it was the one that exposed the false assumption.
- Got the product owner's decision on the flagged rounding quirk from Phase 2:
  preserve it for existing customers (grandfathered), fix it only for
  customers who signed up after the new implementation's launch date - added
  as an explicit branch in the new implementation rather than silently
  dropped.

**Gate:** cut the old `calculate.py` implementation over to fully retired
only once 100% of customers have completed at least one full billing cycle
entirely on the new implementation with reconciled totals, and the
per-customer-per-billing-cycle routing flag's removal is scheduled as its own
follow-up ticket - this is the final retirement criterion, not an
intermediate one.
