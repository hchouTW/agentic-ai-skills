---
role: Lead Experimental Particle Physicist
skill: hep-analysis
archetype: decision-tree
scenario: track reconstruction efficiency measured in a new data-taking period is lower than the previous period in a specific momentum/occupancy regime, and the team must triage among several plausible causes before committing to a fix
---

## Triage Matrix

| Trigger | Resolution Strategy |
|---|---|
| Drop is localized to specific sensor modules, and the conditions-data dead/noisy-channel map changed for this run range | Treat as a channel-map/conditions-data problem; confirm against the dead-channel list per `references/31-calibration-and-alignment.md`'s time-dependence guidance before touching pattern-recognition tuning |
| Drop is concentrated at low momentum and in high-occupancy regions, with no channel-map or alignment payload change logged | Treat as pattern-recognition search-window mistuning per `references/24-tracking-and-vertexing.md`'s "From hits to tracks" section - too tight a window loses hits after a scatter, and the effect is momentum- and density-dependent by construction |
| Drop is roughly uniform across momentum and occupancy, and coincides with a new alignment payload deployment | Treat as an alignment-propagation problem: a coherent position error can push genuine hits outside the pattern-recognition search window per "Alignment coupling"'s point that alignment errors propagate directly into trajectory parameters |
| Drop appears only for a small subset of runs clustered near a payload validity boundary | Treat as an interval-of-validity boundary problem per `references/31-calibration-and-alignment.md`'s "Time dependence and conditions data" section, not a real efficiency loss |

## Selected Branch

The reported drop is concentrated in the lowest-momentum bin and in the
highest-occupancy central region; no channel-map or alignment payload change
is logged for this run range. This matches the second row: pattern-
recognition search-window mistuning.

## End-to-End Execution Script

1. Pull the pattern-recognition configuration diff between the two periods
   and find the seed-extrapolation search-window width for the low-momentum
   regime was tightened in a recent software update, intended to reduce the
   fake-track rate in high-occupancy events.
2. Quantify the tradeoff: rerun reconstruction on a validation sample with
   the old (wider) window and compare fake rate and efficiency side by side
   in the affected regime.
   ```
   $ python3 scripts/compare_window_tuning.py --regime low-pt-high-occupancy
   window=tight (current):  efficiency=0.847  fake_rate=0.021
   window=wide (previous):  efficiency=0.901  fake_rate=0.034
   ```
3. Post to the tracking working group, verbatim: "The low-pt/high-occupancy
   efficiency drop traces to the search-window tightening in the last
   pattern-recognition update, which traded roughly 5 points of efficiency
   for a fake-rate reduction from 3.4% to 2.1% in that regime. Proposing an
   occupancy-dependent window: keep the tight window in high-occupancy runs
   generally, but widen it specifically for the low-momentum sub-range where
   this analysis's signal region lives."
4. Implement the occupancy- and momentum-dependent window, rerun on the
   validation sample, and confirm both efficiency recovers in the targeted
   regime and the fake rate elsewhere is unchanged from the tight-window
   baseline.
5. Document the tuning change and its measured tradeoff in the tracking
   group's conditions-data changelog so a future efficiency investigation in
   this regime does not re-derive the same finding from scratch.

## Fallback Safeguards

If widening the window in the targeted regime recovers efficiency but the
fake rate regresses back toward the old 3.4% level even there, the original
tightening was addressing a real problem specific to that regime, not a
blanket one - the fix needs a narrower occupancy cut on where the wide window
applies, not a full revert. If efficiency does not recover after the
window change, re-triage: the trigger may have been misclassified, and the
first or third rows (channel map or alignment) should be checked next rather
than continuing to adjust the search window.
