---
role: Principal Experimental Particle Physicist
skill: hep-analysis
archetype: gated-pipeline
high_stakes_task: propagating a re-derived tracker alignment (correcting a weak mode found in a cosmic-ray comparison) through a rigidity-spectrum measurement
---

## Phase 1: Input Extraction & Gap Formulation

Extracted the update: a new alignment payload correcting a coherent
deformation identified via a cosmic-ray track comparison. Per
`references/31-calibration-and-alignment.md`'s "Propagating a calibration
change" - "changing it changes efficiencies, resolutions, scale factors,
background estimates derived from control regions, and the trained response
of any classifier that used the affected variables... is therefore not a
local change" - enumerated every downstream product built with the old
alignment: the momentum-scale factor derived from a control sample, the
data-driven background estimate for the rigidity control region, and the
BDT classifier trained on rigidity-dependent inputs (per
[22-multivariate-classifiers-bdt-nn.md](../references/22-multivariate-classifiers-bdt-nn.md)).
None of these had yet been flagged for re-derivation in the draft update
plan - a gap, not an oversight to defer.

**Gate:** proceed to Phase 2 only once every downstream product built with
the old alignment is enumerated by name as an item to re-derive or
re-validate, per that section's explicit list.

## Phase 2: Draft Synthesis

Re-derived the momentum-scale factor from control data using the new
alignment, and re-validated the BDT classifier's rigidity-dependent input
distributions against the new alignment's shifted values. Produced the
explicit before/after comparison that section requires - "event counts per
cut, histogram integrals, maximum absolute and relative bin difference" -
rather than a qualitative "distributions look consistent" statement: event
counts per cut shifted by less than 0.3% at every stage, and the maximum
absolute bin difference in the rigidity spectrum was within the new
alignment's own quoted resolution.

**Gate:** proceed to Phase 3 only once the before/after comparison above is
actually produced (numbers in hand, not a plan to produce them) and shows no
shift outside the new alignment's claimed uncertainty at any cut stage.

## Phase 3: Red-Team Review & Final Artifact Packaging

The assumption most worth stress-testing was that the single cosmic-ray
comparison already performed adequately constrains the charge-antisymmetric
rigidity bias (weak mode) that "Alignment and weak modes" warns is invisible
to the alignment fit's own chi-square. Checking the actual cosmic-ray dataset
used for that comparison found it was accumulated only during a maintenance
period with restricted detector access, sampling cosmic tracks predominantly
from the top hemisphere - not the full azimuthal acceptance a genuine weak-
mode constraint needs, per that section's list of independent constraints
("a resonance of known mass... `E/p` symmetry... cosmic-ray or halo tracks...
comparison of independent subdetectors... field-reversal running"). A single,
azimuthally incomplete cosmic sample is not equivalent to satisfying that
list; the assumption that it alone was sufficient was **false**.

As a result, an independent `E/p` charge-symmetry check was added using an
existing in-situ calibration sample, providing a second, physically distinct
constraint on the same charge-antisymmetric bias per that section's guidance
that weak modes "must be constrained with information the alignment fit does
not use."

**Gate:** release the updated alignment for the rigidity-spectrum measurement
only once at least two independent weak-mode constraints - not the single
azimuthally-restricted cosmic-ray comparison alone - bound the
charge-antisymmetric rigidity bias, and the resulting limit is quoted as a
systematic per `references/31-calibration-and-alignment.md`'s "Deliverables"
list. This is the release criterion, not an intermediate one.
