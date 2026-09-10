# hep-analysis Examples

Canonical worked examples: a "Common Weak Approach" vs. "Expert-Level Best
Practice" contrast plus key takeaways, for a realistic scenario in this skill's
domain. See `agile-development`'s
[references/example-authoring.md](../../agile-development/references/example-authoring.md)
for how these are generated and validated (requires `agile-development`
installed alongside this skill).

| Example | Domain Use Case | Contrast in one line |
|---|---|---|
| [01-jes-systematic-cutflow.md](01-jes-systematic-cutflow.md) | Estimating the jet-energy-scale systematic uncertainty on a cutflow-based cross-section measurement | Reusing the nominal selection mask for the JES up/down variations (reporting a suspicious 0.000% uncertainty) vs. recomputing the selection on each shifted branch (recovering the true 4.06% migration-driven uncertainty) |
| [02-tag-and-probe-background-subtraction.md](02-tag-and-probe-background-subtraction.md) | Measuring a tag-and-probe trigger/identification efficiency with sideband background subtraction | Counting raw pass/fail window totals as pure signal (efficiency biased to 0.7761 with no uncertainty) vs. sideband-subtracting the signal yield in each category first and propagating the correlated-ratio uncertainty (0.8800 +/- 0.0143, plus a stated background-model systematic) |
| [03-li-ma-significance-iact.md](03-li-ma-significance-iact.md) | Computing the detection significance of a candidate gamma-ray source from on/off counts in an IACT analysis | A naive Gaussian S/sqrt(B)-style formula reported as a single-trial 1.826 sigma vs. the Li & Ma (1983) likelihood-ratio significance (2.222 sigma) corrected for 25 independent scan trials (0.578 sigma globally) |
