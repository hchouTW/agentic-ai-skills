---
role: Senior Experimental Particle Physicist
skill: hep-analysis
use_case: estimating the jet-energy-scale systematic uncertainty on a cutflow-based cross-section measurement
---

## Scenario

A cross-section measurement selects events with a leading-jet transverse
momentum above 30 GeV. The analysis needs the jet-energy-scale (JES) systematic
on the signal selection efficiency that enters the cross-section formula. The
JES variation shifts every jet's reconstructed `p_T` by a correlated ±3%; the
question is how much that shift changes the fraction of simulated signal
events passing the `p_T > 30 GeV` cut.

## Common Weak Approach

```python
import numpy as np

PT_THRESHOLD_GEV = 30.0
JES_SHIFT = 0.03  # representative JES magnitude


def selection_efficiency(pt_nominal: np.ndarray) -> tuple[float, np.ndarray]:
    mask = pt_nominal > PT_THRESHOLD_GEV
    return mask.sum() / len(pt_nominal), mask


def jes_uncertainty_weak(pt_nominal: np.ndarray) -> dict[str, float]:
    eff_nominal, mask_nominal = selection_efficiency(pt_nominal)

    # Reuse the nominal selection on the varied samples instead of recomputing
    # it against the shifted pT.
    n_up = mask_nominal.sum()
    n_down = mask_nominal.sum()

    eff_up = n_up / len(pt_nominal)
    eff_down = n_down / len(pt_nominal)
    rel_unc = abs(eff_up - eff_down) / (2 * eff_nominal)

    return {
        "eff_nominal": eff_nominal,
        "eff_up": eff_up,
        "eff_down": eff_down,
        "jes_relative_uncertainty": rel_unc,
    }
```

`jes_uncertainty_weak` never applies the ±3% shift to the selection itself -
`pt_up`/`pt_down` are never computed, and `n_up`/`n_down` both reduce to the
same `mask_nominal.sum()`. On a 200,000-event toy signal sample generated for
this example (leading-jet `p_T` drawn from an exponential falling spectrum with
meaningful density near 30 GeV, the region where migration effects matter
most), this reports `eff_up = eff_down = eff_nominal` exactly and a JES
relative uncertainty of **0.000%** - a suspiciously clean number that would be
the first thing a reviewer should distrust, per this skill's own guidance that
"identical variations are an investigation flag, not proof of a bug." The
actual defect is exactly the one named in `references/06-systematics.md`:
"failing to recompute [selections] for a shape variation that moves objects
across thresholds" is a common bug, and jet `p_T` crossing a selection
threshold is precisely a shape effect, not a weight effect.

## Expert-Level Best Practice

```python
import numpy as np

PT_THRESHOLD_GEV = 30.0
JES_SHIFT = 0.03  # representative JES magnitude


def selection_efficiency(pt: np.ndarray) -> tuple[float, np.ndarray]:
    mask = pt > PT_THRESHOLD_GEV
    return mask.sum() / len(pt), mask


def jes_uncertainty(pt_nominal: np.ndarray) -> dict[str, float]:
    pt_up = pt_nominal * (1.0 + JES_SHIFT)
    pt_down = pt_nominal * (1.0 - JES_SHIFT)

    eff_nominal, mask_nominal = selection_efficiency(pt_nominal)
    eff_up, mask_up = selection_efficiency(pt_up)          # selection recomputed on the shifted branch
    eff_down, mask_down = selection_efficiency(pt_down)    # selection recomputed on the shifted branch

    rel_unc = abs(eff_up - eff_down) / (2 * eff_nominal)

    migrated_in = mask_up & ~mask_nominal    # enter the selection only under the up shift
    migrated_out = mask_nominal & ~mask_down  # leave the selection only under the down shift

    return {
        "eff_nominal": eff_nominal,
        "eff_up": eff_up,
        "eff_down": eff_down,
        "jes_relative_uncertainty": rel_unc,
        "n_migrated_in": int(migrated_in.sum()),
        "n_migrated_out": int(migrated_out.sum()),
    }
```

Each variation gets its own shifted `p_T` array and its own selection mask, so
an event whose nominal `p_T` sits just below 30 GeV but crosses above it under
the +3% shift is correctly counted as selected under "up" and not under
nominal or "down" - and symmetrically for events that migrate out under the
−3% shift. On the same 200,000-event toy sample used above, this reports
`eff_nominal = 0.3213`, `eff_up = 0.3340`, `eff_down = 0.3079`, and a JES
relative uncertainty of **4.059%**, with 2,539 events migrating into the
selection under the up shift and 2,677 migrating out under the down shift -
the population the weak version silently dropped. A relative uncertainty of
essentially zero from a 3% detector-scale shift on a selection sitting inside
the bulk of the `p_T` spectrum was never plausible; this recovers the actual
migration-driven effect and propagates it into the cross-section measurement's
efficiency term instead of hiding it.

## Key Takeaways

- A selection threshold on a shifted quantity is a shape effect, not a weight
  effect - recompute the selection mask against each variation's own shifted
  branch. Reusing the nominal mask, as the weak approach does, silently turns
  "how many events migrate across the cut" into zero by construction, no
  matter how large the real migration is.
- A suspiciously exact result is a signal to investigate, not a result to
  report. Two independent variations producing *identical* selected yields
  down to the count is far more likely to mean the variation was never applied
  to the selection than that the systematic genuinely has zero effect - verified
  above: the weak method's 0.000% is an artifact of an unapplied shift, not a
  physical result.
- Verify a systematic's magnitude against a sanity expectation before trusting
  it. A 3% scale shift on a threshold that sits inside the bulk of the
  distribution should move a non-trivial number of events across that
  threshold; an uncertainty estimate that implies otherwise deserves the same
  scrutiny this skill's own guidance gives an implausible number before it is
  used.
- Build the variation into the same selection code path as the nominal, not a
  separate shortcut that skips re-evaluating the cuts. The expert version's
  `selection_efficiency` is one function called three times, once per
  variation branch - there is only one place the selection logic can drift out
  of sync with itself, instead of three copies that can silently disagree.
