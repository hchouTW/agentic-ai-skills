# Charged Cosmic Rays: Protons, Helium, Nuclei, and Ratios

## When to read this file

Read for proton, helium, heavier-nuclei flux analyses and secondary-to-primary or species ratios (e.g. B/C-type). Owns the **flux blueprint**, the **ratio/fraction blueprint**, geomagnetic primary selection, and rigidity ↔ kinetic-energy-per-nucleon conversion. Elemental/isotopic identification is in [nuclei-and-isotopes](nuclei-and-isotopes.md); leptons and antimatter in [antimatter-and-leptons](antimatter-and-leptons.md).

## Contents

1. [Estimand and public-evidence boundary](#estimand-and-public-evidence-boundary)
2. [Flux blueprint](#flux-blueprint)
3. [Ratio or fraction blueprint](#ratio-or-fraction-blueprint)
4. [Geomagnetic selection](#geomagnetic-selection)
5. [Variable conversion](#variable-conversion)
6. [Dominant backgrounds and effects](#dominant-backgrounds-and-effects)
7. [Subsystems used](#subsystems-used)
8. [Cross-checks](#cross-checks)
9. [Failure modes / Required source classes / Questions to ask](#failure-modes)

## Estimand and public-evidence boundary

**Purpose.** Decide what is being measured and which corrections are unavoidable. **Inputs.** Species, true variable (rigidity), reconstructed variable, fiducial phase space, time interval, bins. **Definitions.** Differential flux `Φ(R)` in `m^-2 sr^-1 s^-1 GV^-1` for primary cosmic rays of a species at the detector location (**top of the instrument**, not corrected to the local interstellar spectrum unless a solar-modulation model is applied and stated).

**Public evidence** (see [source-index](source-index.md)): AMS has published proton, helium, and many nuclei fluxes and ratios with their data periods and rigidity ranges (e.g. proton flux 1 GV to 1.8 TV on 300 million events, S06; B/C over 1.9 GV to 2.6 TV, S10; heavy nuclei through Ca, S15). What is **not** public here: the selection cuts, bins, efficiencies, acceptance, livetime, systematic sizes, and detailed unfolding of any of them beyond the papers. Use the papers' methods sections when they need these; otherwise remain symbolic.

## Documented AMS practice (full-text, main articles only)

[Documented, S06, S08, S13-S15; claims C20, C23, C30, C31] Public AMS flux analyses: select downward-going particles with a tracker track through the required layers and \|Z\| consistent across Tracker, TOF, and (where used) TRD/RICH; require rigidity above **1.2 times the maximum geomagnetic cutoff** in the field of view (backtracing with IGRF), then vary this factor over 1.0-1.4 (or 1.2-1.4) as a systematic; use only time when the detector is in normal conditions, the instrument pointing is within 40° of the local zenith, and outside the South Atlantic Anomaly; write the flux as `N/(A ε ΔR T)` with `N` corrected for migration by **unfolding** (S06, S08 iterate until successive fluxes agree within 0.1%); correct acceptance for data/MC efficiency differences; add independent systematic sources in quadrature. The migration correction is not small: for phosphorus (S15) it ranges from about +25% at 3 GV to -21% at 1.2 TV. Time-resolved results use Bartels-rotation blocks (four rotations, 108 days; S13, S14). The choices below in the blueprint are general; these are what AMS reports.

## Flux blueprint

Symbolic. Fill with user inputs only.

**Inputs.** Target species; true variable `R_true` (absolute rigidity); reconstructed `R_meas`; fiducial phase space (Tracker configuration, geometry); time interval; true-bin edges `{R_j}`; reconstructed bins `{R_i}`.

0. *(Cutoff safety factor, quality time, and unfolding conventions: see the documented practice above.)*
1. **Raw candidate count and selection flow.** `n_i` per reconstructed bin, with the cut-flow ledger (see [reconstruction-and-data-quality](reconstruction-and-data-quality.md#cut-flow-ledger)) including conditional denominators.
2. **Background yields and covariance.** `b_i = Σ_k b_ik` with covariance from template fits or other estimators (see [efficiency-acceptance-backgrounds](efficiency-acceptance-backgrounds.md#background-ledger)). For charged nuclei: charge-migration background from adjacent `Z`, fragmentation from heavier nuclei, lighter-species contamination, and, for protons, `p`-vs-`D`/`He` and electron contributions depending on rigidity.
3. **Trigger and selection efficiencies.** `ε_j`, each a product of conditional factors with data/MC scale factors (see [efficiency-acceptance-backgrounds](efficiency-acceptance-backgrounds.md#conditional-efficiencies)).
4. **Livetime and geomagnetic transmission.** `T_j` includes livetime and the fraction of time each rigidity is above the local cutoff (with a safety factor if used).
5. **Effective acceptance and survival/interaction corrections.** `A_j` from the generation record; survival probability against upstream material and in-detector interactions with a stated cross-section model.
6. **Response matrix and migration.** `R_ij = P(R_meas ∈ bin i | R_true ∈ bin j, selected)`; tails included; charge-migration `Z`-matrix for nuclei.
7. **Estimator or forward model.**
   - *Diagonal estimator (valid only under negligible migration):* `Φ_i = (n_i - b_i) / (ΔR_i · A_i ε_i T_i)` (m^-2 sr^-1 s^-1 GV^-1, with `A` in m² sr and `T` in s); the bin-center or bin-average convention must be stated.
   - *General response model:* `μ_i = Σ_j R_ij A_j ε_j T_j Φ_j ΔR_j + b_i`; fit `Φ_j` (unfolding) or `θ` in `Φ(R;θ)` (forward folding). See [inference-and-unfolding](inference-and-unfolding.md).
   - The diagonal estimator is **invalid under appreciable migration**: with a steeply falling spectrum, events from lower true bins feed higher reconstructed bins, biasing the flux and leading to a rigidity-dependent error; a validation with the response is required before using it.
8. **Statistical and systematic covariance.** As in [calibration-mc-systematics](calibration-mc-systematics.md#propagation-and-correlations); fluxes in adjacent bins are correlated through unfolding and shared systematics.
9. **Closure, stability, publication-level outputs.** Closure on MC (truth recovery), stability versus time, geometry, detector region, cut variations; output tables of flux with covariance; provide the response and exposure so that others can forward-fold.

## Ratio or fraction blueprint

**Definition.** `f = N / D` for a species ratio (e.g. `p̄/p`, `B/C`) or fraction `N/(N+D')` (e.g. positron fraction). Write numerator and denominator explicitly, including what is common: same time interval, same rigidity (or energy) variable and bin edges, same fiducial definition.

Classify each nuisance as **fully correlated** (cancels or shifts both), **partially correlated**, or **independent**:

| Effect | Likely correlation | Verify by |
|---|---|---|
| Trigger efficiency | Partial (species-dependent) | Trigger efficiency vs species and `R` |
| Geometric acceptance | Largely common if same fiducial region | Same selection geometry; verify by MC |
| Selection efficiency (charge, track quality) | Species-dependent (e.g. charge estimator vs `Z`) | Measured per species |
| Material interaction/survival | Species-dependent cross-sections | Cross-section model variation per species |
| Unfolding/scale | Correlated only if same response used and same `R` scale | Shared vs species-specific response |
| Charge confusion | Species-specific | Charge-sign migration validation |
| Livetime/exposure | Common if same period; geomagnetic transmission differs with charge sign at low rigidity | Identical intervals; per-sign cutoff treatment |

**Same fiducial, not same selection.** For different species (e.g. He/O) share the time interval, variable, bins, geometry, track configuration and cutoff treatment, but keep every `|Z|`-dependent element species-specific: charge-estimator windows, adjacent-element leakage, charge-migration matrix, trigger and selection efficiencies, and survival/fragmentation.

**Cancellation depends on compatible fiducial definitions and response conventions**; ratio bins must use the same variable (`R` for both, or the same energy/nucleon assumption). Do not assume complete cancellation: propagate the combined covariance `Var(N/D) ≈ f² [ (σ_N/N)² + (σ_D/D)² - 2 ρ σ_N σ_D /(N D) ]` (first-order delta method; valid when relative uncertainties are small and Gaussian; use toys otherwise). The `hep-analysis` script `particle_ratio_with_uncertainty.py` implements the two-yield delta method. For a **secondary-to-primary** ratio, the physics (propagation) interpretation is a model step beyond the measurement (see result interpretation in [source-policy](source-policy.md)).

## Geomagnetic selection

**Definitions.** Local cutoff rigidity `R_c(position, direction, time)` computed from a field model (dipole approximations differ from realistic models). A "primary" selection requires `|R| > SF · R_c` with a safety factor `SF`, or uses a time-dependent transmission function; the choice of `SF` and model is analysis input.

**Procedure.** (1) State model and version (user-supplied). (2) Compute `R_c` per event from position/attitude, or the exposure-weighted transmission per bin. (3) Choose the cut/transmission scheme and its validity range (below the cutoff, secondary/albedo populations appear; near cutoff the measured spectrum is sensitive to model error). (4) Vary model and safety factor and propagate as a systematic. (5) Validate with the rigidity distribution vs cutoff (below cutoff the primary rate drops; residual counts are secondary).

`hep-analysis` scripts `geomagnetic_cutoff.py` and `orbit_averaged_geomagnetic_cutoff.py` provide a dipole-level planning estimate only; a real analysis needs full-field back-tracing.

## Variable conversion

For isotope of mass number `A`, charge `Z`, rest energy `m c²`:
- `p c = |Z| |R|` (GeV, with `R` in GV).
- `E = sqrt((pc)² + (mc²)²)`, `T = E - mc²`, `T/A = T / A`.
- **Elemental flux conversion** to `T/A` requires an assumed `A` or an isotope-composition model; the conversion and its uncertainty are part of the result. For protons `A = 1`; helium with `⁴He` dominance is an assumption that carries an uncertainty and needs evidence (see [nuclei-and-isotopes](nuclei-and-isotopes.md)).
- **Reference rest energies** (General method; nuclear masses, check against PDG before high-precision use): p 0.9383 GeV, d 1.8756, ³He 2.8084, ⁴He 3.7274, ¹²C about 11.175 GeV (integer-`A` nuclei in this list are only approximately `A` times the nucleon mass, and the difference matters for `T/A`).
- Flux Jacobian: `Φ(T/A) = Φ(R) · dR/d(T/A)`; the conversion of a binned flux requires the Jacobian and treatment of bin edges (not only relabeling).
- Always report which variable the bins and the flux are in.

## Dominant backgrounds and effects

Charge confusion (wrong sign or wrong `|Z|`), fragmentation/charge-changing interactions in upstream material and detector, adjacent-element leakage in the charge estimator, secondary particles/delta rays affecting track reconstruction, albedo/upward-going particles at low `R`, bin migration from finite rigidity resolution with tails, trigger inefficiency dependence on `R`, and time-dependent acceptance/livetime. See [nuclei-and-isotopes](nuclei-and-isotopes.md) for charge-ladder and fragmentation methods.

## Subsystems used

Tracker (rigidity, charge sign for sign contamination, `|Z|`), TOF (direction, `β`, `|Z|`, trigger), RICH (`β`, `|Z|`, especially for velocity/isotope-related tasks), ACC (side-entry veto), TRD (`|Z|` support; lepton contamination in the proton sample). ECAL is not a standard nucleus charge estimator (see the matrix in [detector-and-observables](detector-and-observables.md#cross-subsystem-matrix)).

## Cross-checks

Loose/tight charge and track-quality cuts; alternate track configurations (different layer sets); time-period splits; detector-region/geometry splits; upward/downward and two-charge-sign splits; MC-based vs data-driven efficiency; alternate response/priors/binning; injected-spectrum closure; comparison with published spectra as a plausibility check only (agreement does not prove correctness). Each check names the failure mode it targets and the deviation that triggers a method change or an added uncertainty.

## Failure modes

- Using the diagonal estimator under strong migration.
- Using unadjusted arithmetic bin centers for a steep spectrum.
- Treating the fitted `β` or a subsystem-shared quantity as independent evidence.
- Applying a ratio's assumed cancellation without a per-effect check; combining uncertainties as independent.
- Converting elemental flux to kinetic energy per nucleon with an unstated `A`.
- Cutoff with a single representative latitude or with an unvalidated dipole approximation for a precision claim.
- Quoting a flux at "top of atmosphere" or interstellar values without a modulation model.

## Required source classes

Tier 1 AMS flux/ratio papers for what AMS measured (S06, S07, S10, S11); Tier 4 PDG (cosmic rays, kinematics) for conversion; Tier 4 methodology papers for unfolding; the propagation interpretation is model-dependent and belongs to the theory literature (Tier 6 unless peer-reviewed methodology).

## Questions to ask the user

Which species and rigidity range? Public data period or internal? Which track configuration and hardware era? True-variable/reconstructed-variable definitions and bins? Do you have acceptance/response inputs? Is the target a flux, a ratio, or a model parameter? Which cutoff model and safety factor? If a ratio: numerator/denominator definitions and shared systematics.
