---
role: Senior Experimental Particle Physicist
skill: hep-analysis
archetype: trajectory
problem_input: the signal MC cutflow yield after full selection measures about 15% higher than the cross-section-based prediction, uniformly across every selection step, with no change in cutflow shape
---

## 1. Task Input & Context

Analysis note excerpt, as handed to the analyzer for review:

> ttbar signal MC cutflow yields are consistently ~15% above the
> cross-section-based prediction (`L x sigma x k x filter_efficiency`) at
> every selection step, from preselection through the full selection. The
> *shape* of the cutflow - the fraction surviving each cut relative to the
> previous step - matches the previous production's cutflow almost exactly.
> No single cut is responsible for the excess.

## 2. Root-Cause Triage & Action Plan

A shape-preserving, uniform excess across every step points away from the
selection logic itself (a mis-applied efficiency correction at one specific
cut would only inflate the steps at and after that cut, not all of them
equally) and toward the overall event-weight normalization constant, per
`references/03-weights-normalization.md`'s "Basic convention": `w_event = (L
x sigma x k x filter_efficiency / sum_full_gen_weights) x w_gen x
product(corrections)`. Since `L`, `sigma`, `k`, and `filter_efficiency` are
fixed inputs from the production request, the remaining suspect is the
denominator, `sum_full_gen_weights`.

Checking the production log: the sample was submitted as 40 jobs; 6 failed on
first submission (a storage-element timeout) and were resubmitted
successfully. The ntuple-merging step picked up all 40 jobs' outputs,
including the 6 resubmissions, and both `N` and the per-event `w_gen`
contributions in the merged ntuples reflect all 40 jobs. But
`sum_full_gen_weights` was read from a metadata snapshot recorded *before* the
resubmission completed, and reflects only the 34 originally-successful jobs -
exactly the failure mode `references/03-weights-normalization.md`'s "Basic
convention" section warns about: "the denominator must cover the
corresponding production with the same generator-weight convention, normally
from preselection metadata." A denominator missing 6/40 jobs' generated
weight makes every event's weight, and therefore every cutflow step's yield,
uniformly too large by the same ratio - matching the observed shape-preserving
excess exactly.

Action plan: recompute `sum_full_gen_weights` from the preselection-stage
per-file sums across all 40 merged job outputs (not the stale metadata
snapshot), rerun the cutflow with the corrected denominator, and cross-check
the corrected yield against an independently-produced validation skim of the
same sample.

## 3. Surgical Execution

```diff
-# Metadata snapshot taken before the 6 failed jobs were resubmitted.
-SUM_FULL_GEN_WEIGHTS = 869_565.22  # covers 34/40 merged job outputs
+# Recomputed directly from the preselection-stage per-file sumw records for
+# every job output actually present in the merged ntuples (40/40, including
+# the 6 resubmissions), per references/03-weights-normalization.md's
+# "denominator must cover the corresponding production" rule.
+SUM_FULL_GEN_WEIGHTS = sum(
+    preselection_metadata.sumw_by_job[job_id] for job_id in merged_ntuple_job_ids
+)
+# = 1_000_000.00
```

## 4. Verification Evidence

```
$ python3 scripts/recompute_cutflow.py --sample ttbar_signal --normalization corrected
Step                N        sumw(step)    yield(old norm)  yield(corrected)  validation skim
preselection        812304   800000.0      920000.0         800000.0          799410 +/- 890
>=4 jets              94220    92150.0      105972.5          92150.0           91980 +/- 305
>=1 b-tag             41880    40510.0       46586.5          40510.0           40470 +/- 205
full selection         6712     6504.0        7479.6           6504.0            6498 +/-  82

$ python3 -m pytest tests/test_cutflow_normalization.py -k denominator -v
tests/test_cutflow_normalization.py::test_denominator_covers_all_merged_jobs PASSED
tests/test_cutflow_normalization.py::test_corrected_yield_matches_validation_skim_within_uncertainty PASSED
2 passed in 0.71s
```

The "yield(old norm)" column reproduces the reported ~15% excess
(`920000.0 / 800000.0 = 1.15`) at every step, confirming the diagnosis; the
"yield(corrected)" column matches the independent validation skim within its
statistical uncertainty at every step, confirming the fix rather than just
the diagnosis.

## 5. Final Deliverable Summary

Traced a uniform, shape-preserving 15% excess in the ttbar signal MC cutflow
to a stale `sum_full_gen_weights` denominator that predated 6 resubmitted
production jobs, undercounting the normalization denominator relative to the
40 jobs actually merged into the ntuples. Recomputed the denominator from the
preselection metadata for all 40 merged job outputs, added a regression test
asserting the denominator always covers every job ID present in the merged
ntuples, and confirmed the corrected cutflow matches an independent
validation skim within uncertainty at every selection step.
