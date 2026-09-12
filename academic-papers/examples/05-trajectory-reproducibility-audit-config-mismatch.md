---
role: Reproducibility Auditor
skill: academic-papers
archetype: trajectory
problem_input: auditing whether a paper's headline fitted slope can be reproduced by rerunning the authors' released code and data, and finding the rerun initially disagrees
---

## 1. Task Input & Context

Audit request: "Reproduce Table 2's headline result - a fitted slope of
2.31 ± 0.04 from an ordinary-least-squares regression on the released
dataset `data/release_v1.csv` - by rerunning the authors' released analysis
script against the released data." Per
`references/reproducibility-auditing.md`'s scoping requirement, the agreed
operational scope is stated explicitly before starting: rerunning the
provided artifact as released, compared against the reported value, not an
independent reimplementation.

## 2. Root-Cause Triage & Action Plan

Per `references/reproducibility-auditing.md`'s "Execute only the agreed
scope," the released script was inspected before running it, then run
as-is:

```
$ python3 fit_slope.py --config config_as_released.yaml
slope=2.58 se=0.05
```

`2.58` does not agree with the reported `2.31 ± 0.04` within any reasonable
tolerance. Per "Trace results to artifacts," the released config was checked
against the manuscript's Methods section rather than assuming the code is
wrong: the paper's Methods section states "regression weighted by the
inverse-variance column `w`, per the standard treatment for heteroscedastic
residuals," but `config_as_released.yaml` sets `weight_column: none`. The
released code does not, as shipped, apply the weighting the manuscript's own
text describes.

Action plan: rerun with a config that adds the inverse-variance weighting
described in the Methods section, and compare the result to the reported
value under a pre-declared comparison criterion (agreement within combined
1σ), decided before looking at the reweighted output, per that same
reference's instruction not to loosen criteria after seeing a mismatch.

## 3. Surgical Execution

```diff
--- a/config_as_released.yaml
+++ b/config_weighted.yaml
@@ -1,4 +1,4 @@
 data_path: data/release_v1.csv
 model: ols
-weight_column: none
+weight_column: w
 output: results/slope_fit.json
```

```
$ python3 fit_slope.py --config config_weighted.yaml
slope=2.30 se=0.04
```

## 4. Verification Evidence

```
$ python3 compare_to_reported.py --reported 2.31 --reported-se 0.04 \
    --rerun 2.30 --rerun-se 0.04
combined_se=0.057
difference=0.01
within_1_sigma=True
```

`2.30 ± 0.04` agrees with the reported `2.31 ± 0.04` well within the
pre-declared 1σ combined-uncertainty criterion, confirming the weighting
change - not a code defect in the fit itself - explains the entire
discrepancy.

## 5. Final Deliverable Summary

Delivered a result-level matrix entry per
`references/reproducibility-auditing.md`'s "Report evidence and limits":
claim = Table 2 slope; artifacts required = release script, `release_v1.csv`,
config; evidence inspected = script and config contents; run performed = two
reruns (as-released and weighted); comparison criterion = agreement within
combined 1σ, declared before the weighted rerun; observed outcome = rerun
disagrees as released (2.58 vs. 2.31 ± 0.04), rerun agrees once the
manuscript-described inverse-variance weighting is applied (2.30 ± 0.04);
next action = disclose to the requester that the released
`config_as_released.yaml` omits the weighting the manuscript's Methods
section states was used, since this is a discrepancy between the release and
the paper's own text to flag, not something to silently patch in the
authors' repository on the auditor's own authority.
