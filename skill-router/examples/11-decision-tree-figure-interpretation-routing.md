---
role: Lead Platform / Developer-Experience Engineer
skill: skill-router
archetype: decision-tree
scenario: a request to interpret or discuss a figure/plot, which could belong to academic-papers, hep-analysis, or deep-learning depending on what is actually being asked
---

## Triage Matrix

Formalizes the disambiguation drafted in
`examples/09-gated-pipeline-disambiguating-figure-interpretation.md` into a
reusable trigger -> resolution mapping for any figure/plot request, rather
than re-deriving the reasoning each time one arrives:

| Trigger | Resolution Strategy |
|---|---|
| Request asks what a paper's own already-published figure claims, for a lit-review, critique, or summary, with no recomputation asked for | `academic-papers` applies - its rule covers restating/critiquing a published figure |
| Request asks to recompute, re-derive, or check a physics quantity (a yield, a significance, a systematic) shown in a plot from raw counts or an ntuple | `hep-analysis` applies - its rule covers the underlying analysis, not just the figure |
| Request is about a training/loss/metric curve from a model run, not a physics plot | `deep-learning` applies - loss curves and evaluation-metric plots are training-run artifacts, not publication or physics-analysis figures |
| Request asks both "what does this figure show" and "is the underlying number right" in the same ask | Both apply - state `hep-analysis` (or `deep-learning`) as primary, `academic-papers` as secondary for the prose, per Behavior rule 3, as in example `02` |
| Request's only figure-related word is generic ("chart," "graph," "plot") with no paper, physics, or training-run context at all | Neither `academic-papers` nor `hep-analysis` applies from the figure keyword alone - check the rest of the request for other rules, or proceed per Behavior rule 4 if none apply |

## Selected Branch

A request arrives: "This histogram's uncertainty band looks too narrow - is
that right?" (the second real misrouted case that motivated example `09`).
This asks whether an underlying number (the uncertainty band's width) is
correct, not what the figure's caption claims - it matches the second row.
Selected branch: `hep-analysis` applies alone; `academic-papers` is not
invoked, since no prose or manuscript-writing task was requested.

## End-to-End Execution Script

> Using `hep-analysis` skill.
>
> [`hep-analysis` recomputes the uncertainty band from the underlying counts
> rather than commenting on the figure's appearance: the histogram plots a
> background estimate with only the statistical uncertainty on the MC yield
> propagated, omitting a data-driven normalization systematic that this
> analysis independently estimated elsewhere but never fed into this
> particular plot's error band. Per `references/06-systematics.md`'s caution
> that correlated impacts are not independent errors to add in quadrature,
> the two terms here were first checked for correlation and found
> independent (different sources: MC statistics vs. a data control-region
> normalization), so combining them in quadrature is valid here and widens
> the band from ±4.1% to ±7.8% - the user's instinct that it looked too
> narrow was correct, and the fix is adding the missing systematic term to
> the plotting script, not adjusting the figure's cosmetics.]

No `academic-papers` invocation was needed because the request never asked
for prose about the figure - had the user instead asked "how should I phrase
the uncertainty band in the caption," that would have shifted to the first
row (or, if both were asked together, to the fourth).

## Fallback Safeguards

If the recomputed uncertainty turns out to match the original figure after
all (the trigger was misclassified as "something's wrong" when nothing
was), report that finding plainly rather than manufacturing a fix, and treat
the case as resolved with no action needed - not a failure of the triage
matrix, since the resolution strategy is "recompute and report," not
"recompute and assume the recomputation must show a problem." If instead the
recomputation reveals the discrepancy is large enough to change a
significance claim already stated in a submitted or published manuscript,
escalate beyond a single recomputation: this becomes a second, distinct ask
(whether the published record itself needs a correction) that is
`academic-papers`'s territory, not `hep-analysis`'s alone, and should be
re-triaged per Behavior rule 3 as a primary/secondary case rather than
resolved silently inside the original `hep-analysis` response.
