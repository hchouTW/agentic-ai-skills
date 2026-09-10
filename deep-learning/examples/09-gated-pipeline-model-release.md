---
role: Principal ML Systems Engineer
skill: deep-learning
archetype: gated-pipeline
high_stakes_task: releasing a new fraud-detection model candidate to replace the current production model
---

## Phase 1: Input Extraction & Gap Formulation

Extracted from the release request: the candidate model shows a +3.4 F1
point improvement over the current production model on the standard offline
evaluation set, and the team wants to ship it this week.

Checked the request against `references/monitoring-and-lifecycle.md`'s
"Releasing a new model" checklist and found the plan was missing everything
but the offline number:
- No regression suite run - only the aggregate F1 delta, no per-case diff of
  what improved versus what regressed.
- No shadow-mode plan to catch production-only issues before any user is
  exposed.
- No rollback plan - the previous model's weights exist, but its
  preprocessing version and config are not currently pinned together as one
  redeployable unit.

**Gate:** proceed to Phase 2 only once a regression suite (the fixed
evaluation set plus previously-failed specific cases) has been run and
produces an explicit diff of improvements and regressions, and the previous
model, its preprocessing, and its config are confirmed re-deployable as a
single unit, per `monitoring-and-lifecycle.md`'s explicit warning that "an
aggregate gain almost always hides individual regressions" and that "a
rollback that requires rebuilding a pipeline is not a rollback."

## Phase 2: Draft Synthesis

Ran the regression suite: the aggregate +3.4 F1 gain decomposes into gains on
9 of 12 previously-tracked hard cases and **regressions on 3** (a specific
merchant-category pattern the candidate now misses that the current model
catches) - exactly the individual-regression risk
`monitoring-and-lifecycle.md` warns an aggregate number hides.

Drafted the release plan's remaining stages against that same section:
shadow mode (run the candidate on live traffic for 72 hours without serving
its decisions, to catch feature skew or latency issues at zero user risk),
then a canary at 2% of traffic with automatic rollback wired to operational
metrics (error rate, latency) rather than quality metrics, since
"quality metrics usually arrive too late to gate on." Versioned the release
as one unit per the "Versioning" section: model weights, code commit,
preprocessing version, training-dataset version, config, and the offline
regression-suite results, so the release can be rebuilt or explained later
and so a metric change can't later be silently attributed to an eval-set
change.

**Gate:** proceed to Phase 3 only once the 3 regressed hard cases from the
regression suite are triaged (fixed, or explicitly accepted with a stated
reason) and the shadow-mode plan and rollback unit are both concretely
specified, not just referenced as "standard process."

## Phase 3: Red-Team Review & Final Artifact Packaging

Stress-tested the assumption that "the offline +3.4 F1 gain will translate
into a comparable production improvement." Per
`references/evaluation-strategy.md`'s "The offline-online gap," this
assumption is exactly the kind that recurring causes (distribution shift,
training/serving skew, selection bias in how the offline set was collected)
tend to break. Two real issues surfaced from checking each cause instead of
assuming the number would transfer:

- **Selection bias**: the offline eval set was logged under the *current*
  production model's routing decisions, so transactions the current model
  already sends to manual review are underrepresented in it - the exact
  selection-bias mechanism that section names. The 72-hour shadow-mode run
  showed only a +0.8 F1 gain on the operationally-relevant segment (all live
  traffic, not just what the current model chose to score automatically).
- **Training/serving skew**: per `monitoring-and-lifecycle.md`'s explicit
  guidance to compare feature values for identical inputs through both
  paths, one feature (a rolling transaction-velocity window) was found to be
  computed with a different window boundary in the serving path than in
  training - a real skew bug, not a data issue. Fixed by sharing the
  transformation code between training and serving instead of two separate
  implementations.

Re-ran shadow mode after the skew fix: the operationally-relevant F1 gain
rose from +0.8 to +1.6 points, closer to (though still below) the original
offline +3.4 - consistent with `evaluation-strategy.md`'s point that a gap is
expected and should be measured, not treated as zero.

**Gate:** begin the canary rollout only once the skew bug is fixed, the
post-fix shadow-mode F1 gain on the operationally-relevant segment exceeds
the team's pre-agreed minimum of +1.0 F1, and a rollback drill (redeploying
the previous versioned unit end to end) has actually been executed
successfully, not just documented as possible.
