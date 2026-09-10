# Manuscript consistency auditing

Use to reconcile a manuscript's repeated facts and conclusions across the title,
abstract, body, tables, figures/captions, appendices, and supplements. Include only
provided versions and state any missing artifacts. Local reference checks in
`check_manuscript.py` do not validate numerical or scientific consistency. This
file checks *numeric and factual* consistency; for the same failure mode applied
to a term's meaning or an argument's logical structure rather than a value, use
`logical-consistency-and-argument-uniformity.md`.

Create a result ledger for consequential repeated facts: quantity or claim,
definition, dataset/selection, units, central value, uncertainty type, interval
level, source artifact/version, and every manuscript location. Use an identified
analysis output or author-specified source as authoritative when available; do not
choose the most frequently repeated value as the truth.

Compare like with like before flagging a conflict:

- Normalize units and distinguish fractions, percentages, percentage points,
  absolute changes, and relative changes. Allow rounding consistent with the
  displayed precision; retain the underlying value when available.
- Distinguish statistical, systematic, and total uncertainty; confidence versus
  credible intervals; local versus global significance; observed versus expected
  limits. Do not combine uncertainties without the necessary correlation model.
- Match dataset releases, periods, sample counts, exclusions, train/test splits,
  luminosity/exposure, energy ranges, selections, and model/checkpoint versions.
  Different subsets may legitimately have different values.
- Check metric definitions, averaging/weighting, denominators, reference baselines,
  and binning before comparing numbers. Totals need not equal rounded components;
  categories may overlap, so establish their relationship first.
- Compare figure axes, legends, captions, and table headings with prose. If values
  are read from an image, record approximate precision rather than treating them
  as exact source data.
- Ensure abstract and conclusion preserve the conditions and caveats of the
  results. Check that revised numbers have corresponding revised interpretation.

Classify findings as confirmed contradiction, explainable difference needing a
label, or unresolved source conflict. Provide both locations, the comparison and
its context, impact, and proposed correction. When no authoritative value exists,
ask for the source or flag the conflict rather than overwriting scientific results.

If editing is authorized, propagate verified corrections to all affected locations
and reread the resulting sentences and captions. Deliver a compact discrepancy
ledger, resolved changes, unresolved inputs, and scope of verification; do not
equate internal agreement with external accuracy.
