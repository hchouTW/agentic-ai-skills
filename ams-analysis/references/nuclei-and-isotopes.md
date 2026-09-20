# Nuclei and Isotopes

## When to read this file

Read for elemental charge identification (`Z` ladders), fragmentation and survival, and isotope (mass) measurements such as `D/p`, `³He/⁴He`, Li isotopes. Owns the **nuclei blueprint** and the mass-from-`R`-`Z`-`β` procedure. Observable definitions and mass-error propagation are in [detector-and-observables](detector-and-observables.md#core-observables-and-conventions); the flux blueprint in [charged-cosmic-rays](charged-cosmic-rays.md#flux-blueprint).

## Contents

1. [Public-evidence boundary](#public-evidence-boundary)
2. [Charge ladder and fragmentation](#charge-ladder-and-fragmentation)
3. [Nuclei blueprint](#nuclei-blueprint)
4. [Isotope separation](#isotope-separation)
5. [Ratios](#ratios)
6. [Cross-checks](#cross-checks)
7. [Failure modes / Required source classes / Questions to ask](#failure-modes)

## Public-evidence boundary

Published AMS nuclei and isotope results (see [source-index](source-index.md)): He, C, O and He/C/O rigidity dependence (S11); many primary and secondary nuclei (S20, S15); helium isotopes `³He`, `⁴He` (S12: 100 million `⁴He` nuclei 2.1-21 GV and 18 million `³He` 1.9-15 GV, May 2011-Nov 2017); deuteron flux (S13: 21×10⁶ D, 1.9-21 GV, May 2011-April 2021); lithium isotopes (S14: `⁶Li`, `⁷Li`, 1.9-25 GV). The isotope samples are much smaller than the elemental ones and are bounded to a rigidity range set by the velocity measurement. Details of the isotope fits (templates, RICH range, radiator choice, resolution) are in the papers and are not restated here.

## Documented AMS practice (full-text, main articles only)

[Documented, S12-S15; claims C27-C30] Nuclei: downward-going, tracker track through L1, and the same charge number required on **L1, upper TOF, inner tracker and lower TOF** (\|Z\| = 1 for deuterons, 2 for helium, 3 for lithium); charge confusion of non-interacting nuclei is small (< 0.01% for Li; < 2% for P in the heavy-nuclei paper); the dominant background is **interaction of heavier nuclei in material above tracker L2** (or He → D fragmentation above L1), evaluated from data (S13: reaction ⁴He + (C, Al) → T + X; S15: fit of the L1 charge distribution with Si-Ti charge templates for the part arising from interactions between L1 and L2; S14: survival probability measured with AMS cosmic-ray data). **Isotopes** (S12, S13): rates are **unfolded** using rigidity and inverse-velocity resolution functions of the TOF and the two RICH radiators (NaF, Agl) obtained from MC and validated at β ≈ 1 with data, in velocity bins per detector; the rigidity-resolution systematic is estimated by varying the resolution width by 10% (S12); the quoted Gaussian-core widths (TOF Δ(1/β) 0.02; RICH-Agl 7 × 10⁻⁴ at β = 1) are cores, not tails. The template-fit workflow in the isotope section below is a general design, not a description of these analyses.

## Charge ladder and fragmentation

**Purpose.** Assign `|Z|` for a measured element, and quantify migration between neighbors. **Inputs.** Layer-by-layer charge estimates from Tracker, TOF (upper and lower), RICH (if within acceptance), and optionally TRD. **Definitions.** Charge estimator peak positions and widths per `Z`; consistency requirement across subsystems and across depth.

**Mechanism.** Nuclear interactions in material above or inside the detector change `Z` (fragmentation, charge-changing) so that charge can differ upstream vs downstream of a subsystem; a heavier primary can appear as a lighter nucleus (feed-down); pick-up/spallation can raise `Z` less commonly. Delta rays and secondary tracks affect Tracker charge estimation.

**Procedure.**
1. Select `|Z|` at multiple detector depths (upper TOF/Tracker top, inner Tracker, lower TOF/RICH) with each layer's estimator response modeled per `Z`.
2. Require consistency across depths within validated tails; the requirement defines a charge-selection efficiency and a fragmentation/feed-down background.
3. Estimate migration matrices between neighboring `Z` (data-driven using abundant elements as tag/probe: e.g. estimator in the lower detector conditioned on `Z` in the upper detector) and survival probability through the material above the measured region.
4. Model the interaction cross-sections used for survival and validate against data-driven interaction rates; vary cross-section and material models.
5. Correct or unfold to the true element; propagate uncertainties with correlated migration.

**Dependencies.** Alignment and gain calibration (charge response), saturation of the estimators at large `Z`, path length corrections, matching between subsystems, detector configuration.

**Validation.** Charge-peak position and width stability vs time/rigidity/geometry; data-MC agreement of estimators including tails; measured versus simulated charge-changing probabilities; adjacent-element leakage tests using loosened cuts.

## Nuclei blueprint

Symbolic; uses the flux blueprint with these additions.

1. **Define** element and, where relevant, isotope; truth variable (`R`), reconstructed variable, fiducial region, data period, bins.
2. **Elemental selection at multiple depths** (above): conditional efficiency per depth; charge-selection efficiency measured per `Z` and per rigidity.
3. **Fragmentation feed-down/up.** Feed-down from heavier nuclei (background of the target element) and loss of target nuclei to lighter charges (survival probability `P_surv(Z, R)`): both enter the response/efficiency; they depend on cross-section models and material.
4. **Isotope templates** where relevant (see below); otherwise state the isotope composition assumption.
5. **Rigidity ↔ kinetic energy per nucleon conversion.** Requires an explicit `A` assumption or isotope composition model for an elemental flux; propagate its uncertainty; do not convert without it (see [charged-cosmic-rays](charged-cosmic-rays.md#variable-conversion)).
6. **Response and unfolding** as in [inference-and-unfolding](inference-and-unfolding.md) including a charge migration matrix.
7. **Systematics** by family (see [calibration-mc-systematics](calibration-mc-systematics.md#required-systematic-families)) with emphasis on interaction cross-sections/material, charge-estimator tails, and template statistics for small samples.
8. **Closure and cross-checks** below.

## Isotope separation

**Purpose.** Measure the fraction or flux of one isotope of a given element (e.g. `D` vs `p`, `³He` vs `⁴He`, `⁶Li` vs `⁷Li`). **Definition.** Mass from `m = |Z||R|/(γβ)` (GeV/c² with `R` in GV); for `Z = 1` deuteron vs proton the mass ratio is about 2, for helium isotopes about 4/3, for lithium isotopes about 7/6 (rest-mass ratios; a smaller relative difference makes separation harder).

**Mechanism.** Two independent measurements, `R` from the Tracker and `β` from RICH (and TOF at lower `β`), give mass; the separation power is set by the mass-resolution formula in [detector-and-observables](detector-and-observables.md): `(δm/m)² = (δR/R)² + (γ² δβ/β)²` (+ cross-term). As `β → 1` (rising rigidity for a given mass), `γ²` grows so the mass distributions of isotopes overlap; a rigidity or `T/A` upper limit for the measurement follows from the `β` resolution, not from statistics.

**Procedure.**
1. Restrict to the `β` range and radiator acceptance where the velocity detector has usable resolution (see [source-index](source-index.md) for the relevant detector descriptions); apply ring-quality and containment cuts.
2. Choose the discriminant: reconstructed mass, or `β` at fixed `R`, or `1/β` versus `R/|Z|` distribution (a per-bin distribution of a variable in which isotopes are separated).
3. Build **templates** for each isotope and for backgrounds: `β`-resolution tails, wrong-`Z`, wrong-ring, secondary-particle contamination. Templates are usually MC-based with data-driven tuning of the resolution/tail; validate on a sample with known mass composition (e.g. abundant `p`, `⁴He`) that populates the same `β` range.
4. Fit the isotope fraction (or flux ratio) in each rigidity (or `T/A`) bin with finite-template nuisances; constrain shared resolution parameters across bins only with a stated model.
5. **Template overlap.** Report the overlap and the correlation between the isotope fractions and the resolution nuisances; a strong correlation is a diagnostic that the bin is at the sensitivity edge.
6. **Ring-quality dependence.** Study efficiency and template shape versus ring quality and versus radiator region; systematics from ring-selection variations.
7. **Fragmentation.** For `D` and `³He`, secondary production by interactions of heavier nuclei (e.g. `⁴He` fragmenting) in the material contaminates the isotope sample and depends on material and cross-section models; treat as a background with its own control.
8. **Simulated-shape validation.** The simulated `β` and mass shapes must be validated in data with an independent sample and tails (not only the core).
9. **Output.** Isotope fraction or flux ratio vs `R` (or `T/A` with a stated assumption), correlation matrix, and the range of validity.

**Proposal vs fact.** The above is a general workflow; AMS's published analyses (S12-S14) determine what was actually used. Do not attribute template forms, cuts, or resolution values to AMS without reading the relevant paper.

## Ratios

Isotope and element ratios (e.g. `D/p`, `³He/⁴He`, `B/C`) share acceptance and material effects only partially; the survival probabilities differ by species. Do not claim efficiency cancellation without evidence (see the ratio blueprint in [charged-cosmic-rays](charged-cosmic-rays.md#ratio-or-fraction-blueprint)). A measured ratio's rigidity dependence (e.g. a power law at high rigidity) is an empirical description; the physical interpretation (propagation, source) is a model step (see [source-policy](source-policy.md#result-interpretation)).

## Cross-checks

Orthogonal `|Z|` chains; alternative discriminants (mass vs `β`-at-fixed-`R`); loose/tight ring quality; radiator-region and detector-half splits; time-period splits (particularly for low-rigidity isotopes influenced by solar modulation); alternative templates (different resolution/tail models); pseudo-data with injected isotope fractions; fit-bias tests; abundant-sample tail validation; comparison with published results as plausibility only.

## Failure modes

- Mass estimated at `β → 1` without accounting for `γ²` amplification; rigidity-`β` correlation ignored.
- Templates taken from MC without tail validation in data; overlapping templates not diagnosed.
- Fragmentation feed-down/up and adjacent-element leakage neglected; cross-section model unvaried.
- Elemental to `T/A` conversion with an unstated `A`.
- Efficiency cancellation in a ratio asserted without verification; survival probabilities assumed equal.
- Radiator boundaries or ring-quality effects ignored; ring from secondary particle accepted.

## Required source classes

Tier 1: S11-S15, S20 for what AMS measured and how; Tier 2 detector papers for RICH and Tracker performance (S17-S19); Tier 4 PDG for nuclear interaction and kinematics conventions; Tier 4/5 for nuclear cross-section models (state model provenance, do not attribute to AMS).

## Questions to ask the user

Which element and isotope pair? Rigidity/`T/A` range and data period? Which subsystem provides `β` in your range (TOF vs RICH radiator)? Do you have per-`Z` charge-migration and survival inputs? What isotope composition assumption is used for `T/A`? Do you have known-mass control samples in the same `β` range? Template provenance and statistics?
