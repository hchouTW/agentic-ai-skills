---
role: Lead Experimental Particle Physicist
skill: hep-analysis
archetype: decision-tree
scenario: an unexpected excess appears in a background-dominated control region, and the team must triage among background mismodeling, new physics, a detector effect, and a statistical fluctuation before committing resources to any one explanation
---

## Triage Matrix

| Trigger | Resolution Strategy |
|---|---|
| Excess is localized to one kinematic bin, and the same bin shows an anomaly in an unrelated, physics-orthogonal control sample (e.g. a same-sign or same-flavor sideband with no signal sensitivity) | Treat as a detector or reconstruction effect local to that bin/region; investigate hardware/reconstruction logs for that run range before touching the background model |
| Excess is broad across many bins in the same direction, and a background-only fit's post-fit nuisance pulls are large and coherent for one systematic source | Treat as background mismodeling; that systematic's template or correlation assumption is the primary suspect, per `references/06-systematics.md`'s guidance to check pulls before invoking new physics |
| Excess is localized to a small region consistent with a specific mass/kinematic hypothesis, absent from all orthogonal control samples and detector-effect checks, and stable when the analysis selection is varied within reason | Treat as a new-physics candidate; proceed to the full statistical-significance and look-elsewhere-corrected procedure per `references/08-inference.md` and `references/09-statistical-tools.md`, not before |
| Excess disappears or is not significant once the correct trials factor for the number of bins/selections scanned is applied | Treat as a statistical fluctuation; report the corrected, non-significant result rather than the pre-trials number |

## Selected Branch

The reported excess is a broad ~1.3-sigma-per-bin excess across the four
highest-mass bins of a control region dominated by one background process,
in the same direction in every bin. A background-only fit shows the
nuisance parameter for that background's shape systematic pulled 1.8 sigma
from its nominal value, coherently across those same bins, while an
orthogonal same-sign control sample (sensitive to detector mismeasurement
but not to this background's physics) shows no anomaly. This matches the
second row: background mismodeling, not new physics or a detector effect.

## End-to-End Execution Script

1. Confirm the orthogonal-sample check: rerun the same-sign selection and
   verify no coherent excess there (already done - no anomaly found), ruling
   out a shared detector-level cause per the first row's own contrast case.
2. Inspect the pulled systematic's template per
   `references/06-systematics.md`'s "Template validation": check whether the
   Up/Down shape variations were built with the correct fit-range extrapolation
   documented in `references/05-backgrounds.md`'s "Sidebands and data-driven
   shapes" section, since this background's normalization is sideband-derived.
3. Rebuild the sideband fit using an alternative functional form and compare:
   the original fit's chi-square is only marginally better than the
   alternative, consistent with that section's warning that "selecting the
   best chi-square alone is insufficient" as a way to fix functional-form
   choice.
4. Communicate to the analysis team, verbatim: "The control-region excess
   traces to functional-form uncertainty in the sideband background fit, not
   new physics or a detector effect - same-sign control shows no anomaly, and
   the pulled nuisance is consistent with a known, previously
   under-covered systematic. Adding a discrete functional-form uncertainty
   per the backgrounds reference resolves the pull without invoking any new
   effect."
5. Add the missing functional-form systematic to the registry per
   `references/06-systematics.md`'s "Variation registry" pattern, and re-run
   the background-only fit to confirm the nuisance pull returns to within 1
   sigma of nominal.

## Fallback Safeguards

If adding the functional-form systematic does not resolve the pull back to
within 1 sigma, the trigger classification was likely wrong: re-triage
against the third row (new-physics candidate) only after re-confirming the
orthogonal-sample and detector-log checks from the first row, rather than
proceeding directly to a significance calculation on an unresolved
background pull. If the same coherent pull reappears in a completely
different control region using the same background process, treat that as
evidence the mismodeling is a property of the process itself (escalate to
revisiting the background's underlying model, not just its fit range) rather
than re-deriving another one-off functional-form correction.
