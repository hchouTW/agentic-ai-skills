---
role: Lead Astroparticle Physicist
skill: hep-analysis
archetype: decision-tree
scenario: a public real-time neutrino alert arrives with a possible electromagnetic counterpart candidate found in its localization region, and the team must triage what kind of claim, if any, the coincidence supports
---

## Triage Matrix

| Trigger | Resolution Strategy |
|---|---|
| Coincidence found within a time/pointing window that was pre-registered before the alert arrived, and the alert's stated false-alarm rate is already stringent | Proceed to a joint-likelihood or named combined-probability significance calculation per `references/38-multimessenger-analysis.md`, folding in the alert's FAR |
| Apparent coincidence found only after inspecting the data, with no pre-registered window | Apply a trials/look-elsewhere correction for the post-hoc window choice before quoting any significance, per that section's explicit requirement |
| The alert used for follow-up decisions is later retracted or its localization/significance revised | Redo the analysis using the final, reviewed alert properties, and flag in the write-up that follow-up decisions used since-superseded preliminary information |
| Two candidate counterparts are found in different instruments' localization regions with no common-clock timing cross-check performed yet | Place both instruments' timing on a common UTC reference with stated per-instrument systematics before evaluating any timing coincidence |

## Selected Branch

The neutrino alert was issued at a loose, high-FAR public threshold (chosen
to maximize timely follow-up), and a gamma-ray flare was found in its
localization region using a time window defined only after the flare was
already known to be there - no window was pre-registered before the alert.
This matches the second row: a post-hoc window requiring a trials correction.

## End-to-End Execution Script

1. Reconstruct exactly how the window was chosen: the analyst looked for
   flares within 72 hours of the alert after already knowing a flare occurred
   28 hours afterward - an implicit, undocumented window rather than a
   pre-registered one.
2. Compute the trials factor for that choice honestly: rather than treating
   72 hours as the "real" pre-registered window, count the number of
   statistically independent time bins of that width the source's monitoring
   data actually covers over the accessible archive, and apply that as the
   trials correction to the chance-coincidence rate.
   ```
   $ python3 scripts/trials_corrected_coincidence.py --window-hours 72 --archive-days 400
   raw chance-coincidence p-value: 0.014
   independent 72h windows in 400-day archive: 133
   trials-corrected p-value: 1 - (1 - 0.014)**133 = 0.847
   ```
3. Fold in the alert's own stated FAR (loose, by design, to enable timely
   follow-up) per the "Alert follow-up and public alerts" section - it is a
   weaker prior than a stringent-threshold alert, not treated as equally
   reliable.
4. Report to the collaboration, verbatim: "The gamma-ray flare and the
   neutrino alert are consistent with a chance coincidence once the window is
   corrected for the fact it was defined after the flare was already known
   (trials-corrected p-value ~0.86, not the naive ~0.014), compounded by the
   alert's own loose FAR threshold. This does not support an association
   claim; recommend reporting it as an unconfirmed candidate for future,
   pre-registered searches rather than a coincidence detection."
5. Record the pre-registered-window lesson in the follow-up program's
   procedures so the next candidate counterpart search defines its window
   before, not after, seeing where an interesting signal fell.

## Fallback Safeguards

If the trials-corrected significance is later needed for a different,
genuinely pre-registered search covering the same sky region and time range,
do not reuse this analysis's post-hoc trials factor - recompute it under that
search's own pre-declared window. If the alert is subsequently retracted or
its localization revised (the third row's trigger), redo this entire
assessment against the revised alert properties rather than treating the
already-completed trials correction as still valid, since both the
chance-coincidence rate and the FAR-based weakening depend on the alert
properties used.
