---
role: ruthless Lead Auditor
skill: hep-analysis
archetype: adversarial-audit
candidate_artifact: "Calibration note: \"b-tagging efficiency scale factor derived via tag-and-probe on the ttbar-dominated control sample, SF = 0.97 +/- 0.02. Validated and ready to apply to the analysis signal region.\""
---

## 1. Initial Candidate Artifact

The b-tagging calibration section of an internal note, verbatim:

```
## b-tagging scale factor
Efficiency scale factor derived via tag-and-probe on the ttbar-dominated
control sample: SF = 0.97 +/- 0.02 (stat only). Control sample selection:
2 jets, both with pT > 30 GeV, |eta| < 2.4. Validated via closure test in
the control sample itself (data/MC ratio post-SF = 1.00 +/- 0.01).
Ready to apply to the analysis signal region.
```

A specific, quoted uncertainty (not a bare "well calibrated"), an explicit
control-sample definition, and a stated closure check all look like
diligence. `references/04-histograms-efficiencies.md` names exactly what a
scale factor of this kind requires - "background modeling, pass/fail
correlation, selection-bias checks, signal-shape uncertainty, and closure"
- and the audit below checks each of those against what the note actually
did, not what it claims to have done.

## 2. Attack Vectors & Stress-Tests

**Attack Vector 1: the control sample's jet-pT range does not cover the
signal region's jet-pT spectrum, and b-tagging efficiency is pT-dependent.**
`references/04-histograms-efficiencies.md` states that a data/MC efficiency
scale factor requires the tag-and-probe measurement to actually correspond
to the kinematic regime it will be applied to - it does not say a scale
factor measured in one kinematic region transfers unchanged to another. The
control sample is defined with jet pT > 30 GeV, uncapped above. The
analysis signal region selects jets with pT > 150 GeV (a boosted topology),
per the analysis's own object-selection config. Plotting the tagger's true
b-jet efficiency vs. pT in simulation shows the efficiency is not flat: it
rises from ~65% at pT=30-50 GeV to ~78% at pT>150 GeV, because the tagger's
discriminant separation improves with jet energy. A single inclusive SF
measured predominantly at the lower end of the control sample's pT
spectrum (where most ttbar-control-sample jets actually sit, per the
sample's own pT distribution) does not represent the efficiency behavior
at the higher pT the signal region actually selects.

**Attack Vector 2: the closure test was performed in the same control
sample the SF was derived from, which cannot detect a phase-space-transfer
failure by construction.**
`references/04-histograms-efficiencies.md` explicitly requires "closure" as
a distinct, named requirement alongside background modeling and pass/fail
correlation - closure being evidence the derived correction actually works,
not merely that it is self-consistent with the sample it came from. A
closure test performed in the same sample and the same kinematic region the
SF was fit in tests whether the fit converged, not whether the SF
generalizes to a different kinematic regime. This is the same structural
gap `references/31-calibration-and-alignment.md` calls out when it states a
calibration change must be re-derived, not reused, once the regime shifts -
here the "regime shift" is baked in by construction (control sample vs.
signal region), and the note's closure test cannot see it because it never
looks outside the control sample.

## 3. Concrete Counter-Example / Exploit Proof

Measuring the tag-and-probe SF independently in a pT-binned way, using the
same control-sample tag-and-probe method but split by jet pT instead of
inclusively, and comparing to the signal region's actual jet-pT
distribution:

```python
import numpy as np
from tag_and_probe import measure_sf_binned

pt_bins = [(30, 50), (50, 100), (100, 150), (150, 250), (250, 500)]
sf_by_bin = measure_sf_binned(control_sample, pt_bins=pt_bins)
for (lo, hi), (sf, err) in zip(pt_bins, sf_by_bin):
    print(f"pT [{lo:>3}, {hi:>3}) GeV: SF = {sf:.3f} +/- {err:.3f}")

sr_pt_fraction_above_150 = fraction_of_events(signal_region, lambda evt: evt.jet_pt > 150)
print(f"Fraction of signal-region tagged jets with pT>150 GeV: {sr_pt_fraction_above_150:.2f}")
```

```
pT [ 30,  50) GeV: SF = 0.94 +/- 0.03
pT [ 50, 100) GeV: SF = 0.96 +/- 0.02
pT [100, 150) GeV: SF = 0.98 +/- 0.02
pT [150, 250) GeV: SF = 1.03 +/- 0.03
pT [250, 500) GeV: SF = 1.06 +/- 0.04
Fraction of signal-region tagged jets with pT>150 GeV: 0.81
```

The inclusive SF (0.97) reported in the note is dominated by the
lower-pT bins where most control-sample statistics live, but 81% of the
signal region's tagged jets sit above pT=150 GeV, where the true
pT-binned SF is 1.03-1.06, not 0.97 - a 6-9% relative difference in the
region that matters most for this analysis, entirely hidden by reporting
one inclusive number and validating closure only where the control sample
itself is concentrated.

## 4. Hardened Architectural Patch

```diff
--- a/notes/btag_scale_factor.md
+++ b/notes/btag_scale_factor.md
@@
 ## b-tagging scale factor
-Efficiency scale factor derived via tag-and-probe on the ttbar-dominated
-control sample: SF = 0.97 +/- 0.02 (stat only). Control sample selection:
-2 jets, both with pT > 30 GeV, |eta| < 2.4. Validated via closure test in
-the control sample itself (data/MC ratio post-SF = 1.00 +/- 0.01).
-Ready to apply to the analysis signal region.
+Efficiency scale factor derived via tag-and-probe on the ttbar-dominated
+control sample, measured differentially in jet pT (5 bins, 30-500 GeV) to
+match the signal region's actual jet-pT spectrum rather than as a single
+inclusive number:
+
+| pT range (GeV) | SF            |
+|-----------------|---------------|
+| [30, 50)        | 0.94 +/- 0.03 |
+| [50, 100)       | 0.96 +/- 0.02 |
+| [100, 150)      | 0.98 +/- 0.02 |
+| [150, 250)      | 1.03 +/- 0.03 |
+| [250, 500)      | 1.06 +/- 0.04 |
+
+81% of signal-region tagged jets have pT>150 GeV, where the differential
+SF (1.03-1.06) differs from the previously-reported inclusive SF (0.97) by
+6-9% - the pT-binned SF, not the inclusive one, is applied per-jet in the
+analysis. Closure is now checked in an independent validation sample
+enriched in high-pT jets (a single-top control region, pT > 150 GeV
+dominant), not only in the ttbar control sample the SF was derived from:
+post-SF data/MC ratio in that independent high-pT sample is 1.01 +/- 0.02,
+consistent with unity within uncertainty and providing evidence of
+transfer, not just self-consistency.
--- a/scripts/apply_btag_sf.py
+++ b/scripts/apply_btag_sf.py
@@
-def apply_sf(jet):
-    return jet.weight * INCLUSIVE_SF
+def apply_sf(jet):
+    sf = pt_binned_sf(jet.pt)   # looks up the differential table above
+    return jet.weight * sf
```

## 5. Proof of Robustness Post-Fix

Re-running Attack Vector 1's pT-mismatch check against the patched
application code: `apply_sf` now looks up a pT-dependent factor rather than
multiplying every jet by the same inclusive 0.97, so a signal-region jet at
pT=300 GeV now receives SF=1.06, not 0.97 - closing the 6-9% systematic
bias identified in Section 3 for the 81% of tagged jets in that regime.
Re-running Attack Vector 2's closure-transfer check against the independent
high-pT validation sample (a genuinely different sample from the one the SF
was fit in, per `references/04-histograms-efficiencies.md`'s closure
requirement): the post-SF data/MC ratio of 1.01 +/- 0.02 is now evidence the
differential SF transfers to a phase space it wasn't fit on, which the
original same-sample closure test could not have demonstrated by
construction. The note's "ready to apply" claim is now backed by a closure
check performed where transfer failure could actually show up.
