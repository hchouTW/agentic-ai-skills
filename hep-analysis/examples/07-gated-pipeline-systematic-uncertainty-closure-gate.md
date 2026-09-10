---
role: Principal Experimental Particle Physicist
skill: hep-analysis
archetype: gated-pipeline
high_stakes_task: estimating the systematic-uncertainty budget for a b-tagging scale-factor correction, with a closure-test gate before the correction enters the final fit
---

## Phase 1: Input Extraction & Gap Formulation

Extracted the b-tagging scale-factor correction's uncertainty sources per
`references/06-systematics.md`'s "Types and propagation": a rate-only
component (overall normalization of the tagging efficiency), a shape
component (working-point-dependent mistag rate versus jet pt), and a
calibration-sample-statistics component. Checked these against the "Variation
registry and implementation pattern" section's required fields and found a
gap: no registry entry yet states the correlation model across the two
data-taking eras for any of the three components - the analysis note simply
says "b-tagging systematic, treated as correlated," with no per-component
breakdown.

**Gate:** proceed to Phase 2 only once every one of the three sources has a
full registry entry - variation name, type, samples affected, exclusion
rule, correlation model across eras, and validation tolerance - per
`references/06-systematics.md`'s "Variation registry and implementation
pattern".

## Phase 2: Draft Synthesis

Built the nominal and variation histograms following that same section's
implementation pattern: iterated over the configured variation list rather
than hand-writing each one, replaced only the weight expression for the two
weight-type components, and recomputed the affected selection for the shape
component (since its working-point-dependent mistag shift can move a jet
across the tagging threshold, unlike a pure weight reweighting).

Checked every resulting template against `references/06-systematics.md`'s
"Template validation" checklist as the phase's specific acceptance criterion:
edges and flow bins, finite values everywhere, variance bookkeeping present,
and no zero-nominal/nonzero-variation bin left with an arbitrary epsilon
ratio. One shape-component bin failed this check on the first pass (a
zero-nominal bin with a nonzero Down-variation entry, from a jet migrating
into an otherwise-empty high-pt tagged category); per that section's guidance
this was investigated with additional MC rather than patched with an epsilon,
and resolved by regenerating the shape template with a larger auxiliary MC
sample for that category.

**Gate:** proceed to Phase 3 only once every variation template - all three
components, both eras - passes the Template-validation checklist with no
unresolved zero-nominal/nonzero-variation bins.

## Phase 3: Red-Team Review & Final Artifact Packaging

The assumption most worth stress-testing was the registry's default: "the
b-tagging systematic is fully correlated across the two data-taking eras."
Applying `references/06-systematics.md`'s "Model validation" guidance -
evaluate the nuisance at -1, 0, +1 and check the consequences on the fit
result - showed this assumption was **wrong for one of the three
components**: the calibration-sample-statistics component is, by
construction, drawn from a different calibration dataset each era and cannot
share a common nuisance parameter across eras, while the rate and shape
components genuinely do share a physical source (the same tagging-algorithm
training) and are correctly kept correlated. Treating all three as uniformly
correlated had been silently double-suppressing the calibration-statistics
contribution to the total uncertainty, understating it in exactly the way
`references/06-systematics.md`'s "Source inventory" warns against: "Neither
'all uncertainties in one year are correlated' nor 'different years are
independent' is a valid blanket rule."

The registry was revised to decompose the single "b-tagging systematic" entry
into two: a correlated component (rate + shape, shared training) and an
era-uncorrelated component (calibration-sample statistics), each with its own
nuisance parameter.

**Gate:** enter the final fit only once the decomposed registry entries are
in place, the era-uncorrelated component's Model-validation nuisance scan
shows finite, continuous predicted rates at -1, 0, and +1 in both eras
independently, and the total-uncertainty impact of the decomposition (versus
the original single-correlated treatment) is quoted explicitly in the
analysis note rather than silently absorbed - this is the release criterion
for the correction to enter the fit, not an intermediate check.
