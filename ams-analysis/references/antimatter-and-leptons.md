# Antimatter and Leptons: e±, Antiprotons, Antideuterons, Antihelium

## When to read this file

Read for positron/electron fluxes and the positron fraction, electron/proton separation, antiproton analysis, and searches for rare antinuclei (antideuteron, antihelium). Owns the **electron/positron blueprint**, the **rare-antimatter blueprint**, and the reporting policy distinguishing candidate, excess, evidence, and discovery. Shared machinery: [efficiency-acceptance-backgrounds](efficiency-acceptance-backgrounds.md), [inference-and-unfolding](inference-and-unfolding.md); observables in [detector-and-observables](detector-and-observables.md).

## Contents

1. [Public-evidence boundary](#public-evidence-boundary)
2. [Electrons and positrons](#electrons-and-positrons)
3. [Electron/positron blueprint](#electronpositron-blueprint)
4. [Antiprotons](#antiprotons)
5. [Rare-antimatter blueprint](#rare-antimatter-blueprint)
6. [Reporting policy](#reporting-policy)
7. [Cross-checks](#cross-checks)
8. [Failure modes / Required source classes / Questions to ask](#failure-modes)

## Public-evidence boundary

Published (see [source-index](source-index.md)): positron fraction (S02: 0.5-350 GeV, 6.8×10⁶ positron and electron events; later S03), positron flux (S04: 1.9 million positrons up to 1 TeV, source-term energy cutoff reported), electron flux (S05), antiproton flux and `p̄/p` (S08: 1-450 GV, 3.49×10⁵ antiprotons, 2.42×10⁹ protons; S09 time dependence over a solar cycle). **Antihelium: no peer-reviewed AMS paper was found in INSPIRE-HEP (checked 2026-09-20); public statements are conference/talk statements and third-party discussion (see S24-S27).** Do not state candidate counts, do not describe any candidate as established. **Antideuteron: no AMS measurement or search paper was found in INSPIRE (S28, C19; only a 2008 sensitivity conference paper and third-party prospects);** treat any antideuteron statement like antihelium unless a primary source is located.

## Electrons and positrons

**Estimand.** Positron fraction `e⁺/(e⁺+e⁻)`, separate `e⁺` and `e⁻` fluxes, or the combined `(e⁺+e⁻)` flux. Distinguish denominators (fraction denominator is the sum; separate fluxes each have their own acceptance/efficiency), correlated errors (fraction shares proton contamination and acceptance), and variable (published leptons results use **energy**, whereas Tracker measures **rigidity** and ECAL measures **energy**; state which enters the binning and how they are related).

**Subsystem roles (independent evidence chain).**
- *Tracker/magnet:* charge sign and rigidity; the only charge-sign source; also `|Z| = 1` selection.
- *TRD:* lepton/hadron separation through transition radiation (γ-dependent); not a charge-sign detector.
- *ECAL:* shower shape and energy; `E/|p|` compatibility with Tracker for electrons (`E ≈ pc`); hadronic tails must be validated.
- *TOF/ACC/RICH:* direction, `β`, veto, `|Z|`; RICH is limited for lepton ID.
- Independence: TRD and ECAL exploit different physics, but ECAL shape and `E/p` share the ECAL energy; Tracker charge and `E/p` share the track. Track the correlations explicitly.

**Backgrounds.** Protons misidentified as leptons (dominant, abundance orders of magnitude above positrons); charge confusion (electron reconstructed as positron: a Tracker tail and a source-of-primary-electron contamination of the positron sample); secondary/albedo leptons and the geomagnetic effect; bremsstrahlung and photon conversion changing the matching; hadronic showers with large electromagnetic fractions. Public rejection factors are context-dependent (selection efficiency, energy); none is quoted here.

## Documented AMS practice (full-text, main articles only)

[Documented, S04, S05, S08; claims C22, C24-C26] **Positrons/electrons:** the positive (negative) rigidity sample contains the signal plus protons (antiprotons) and charge-confusion leptons; an energy-dependent cut on the ECAL estimator Λ_ECAL removes most of the hadronic background (antiproton background < 10⁻³ of the negative sample after the electron cut); the yield is then extracted by a **template fit in the two-dimensional (Λ_TRD, Λ_CC) plane** with three templates (correct-sign lepton, correct-sign proton, charge-confusion lepton), where Λ_CC is a BDT-based charge-confusion estimator; the signal template comes from high-purity electron data (below 100 GeV) and electron MC above; the charge-confusion template comes from MC verified with test-beam e± (10-290 GeV) and flight e⁻ data; the flux is defined in energy at the top of AMS with data/MC efficiency corrections estimated from the electron sample, bin widths at least twice the energy resolution, unfolding for the small migration, and the energy-scale uncertainty treated as an uncertainty of the bin boundaries. **Antiprotons:** template fit to the negative-rigidity sample with the signal template taken from proton data, background (electron, π⁻, charge-confusion proton) templates from data and MC, in three overlapping rigidity regions, charge-confusion MC checked with 400 GV proton test-beam data. The two blueprints below are general designs consistent with, but not identical to, these papers; details not in the main articles (Supplemental Material) are not reproduced.

## Electron/positron blueprint

**Inputs.** Target quantity; energy/rigidity binning; Tracker charge-sign and `|Z|=1` selection; TRD and ECAL discriminants; `E/p` variable; control samples.

**Branch A: cut-and-count.**
1. Define the lepton selection (TRD, ECAL shape, `E/p` compatibility) and a proton-rich control (reversed cuts) and a charge-confusion control.
2. Estimate the residual proton contamination from the control via a transfer factor; validate the transfer with orthogonal cuts; quantify the tail.
3. Estimate charge confusion from the Tracker tail (data-driven or calibrated MC; the Gaussian core is not enough) as a **migration matrix in charge sign** `M(e⁺←e⁻)`, `M(e⁻←e⁺)` vs energy.
4. Efficiencies as conditional factors (see [efficiency-acceptance-backgrounds](efficiency-acceptance-backgrounds.md#conditional-efficiencies)), acceptance and exposure with a lepton-specific generation record, energy response (bremsstrahlung tail), and unfolding or forward folding.
5. Fraction/flux with the covariance of shared systematics.

**Branch B: template fit.**
1. Choose the discriminant (TRD estimator, ECAL classifier, `E/p`, or a combination) per energy bin; define templates for: true `e⁺`, true `e⁻`, proton background (charge-positive), charge-confused `e⁻→e⁺` (shape near `e⁻`), and other components.
2. Templates: provenance (MC vs data-derived with a control), finite statistics nuisances, smoothing, morphing in energy, cross-contamination (signal in the proton template).
3. Fit `n_i^{(c)}` in each charge-sign selection simultaneously (positive and negative charge samples share templates and charge-confusion parameters), with constraints from control regions.
4. Validate with injected charge confusion and alternative proton shapes; goodness of fit; pulls; correlations.
5. Propagate to fraction or flux with correlated errors; closure of the combined chain.

### Choosing fraction versus flux for interpretation

Both are direct measurements; the physical interpretation (dark matter, pulsars, secondary production) is a model step. The fraction `e⁺/(e⁺+e⁻)` moves if the electron spectrum moves, so a model must describe both leptons; it also shares acceptance and proton contamination between numerator and denominator (cancellation is to be shown). The separate positron flux is what a source-plus-background model predicts directly, but carries its own acceptance and charge-confusion systematics. Do not fit the fraction and the fluxes as independent data: they come from the same events and share systematics, so carry the joint covariance or choose one. State the background (secondary-production and propagation) model and vary it as a nuisance; do not extrapolate beyond the measured energy range; account for solar modulation and geomagnetic effects at low energy.

## Antiprotons

**Estimand.** `p̄` flux and `p̄/p` versus `|R|`. **Signal signature.** Negative charge sign, `|Z| = 1`, hadron-like TRD/ECAL response, `β` consistent with the rigidity. **Backgrounds.** Electron (negative sign) is the dominant one at some rigidities (rejected with TRD and ECAL; residual modeled), charge-confused protons (positive → negative sign; the tail of the Tracker rigidity response), and secondary/interacting particles. **Design.** Rigidity is used as the variable (charge sign known through Tracker); a template fit of a charge-sign-sensitive variable (e.g. signed rigidity or an estimator that combines Tracker-tail information) in reconstructed bins, with templates for `p̄`, charge-confused `p`, and `e⁻`; the `p` denominator with its own acceptance and efficiency (partial cancellation: verify). See the symbolic likelihood in [Example 6 of tests-and-examples](tests-and-examples.md#example-6-antiproton-template-likelihood). **Do not present the recipe as AMS practice**: it is a proposal; the published analysis details are in S08/S09.

## Rare-antimatter blueprint

For antideuteron, antihelium, or any rare event class. All steps are **proposals** unless a primary source states them.

1. **Define signal topology and region.** Charge `|Z|`, sign, mass hypothesis region in the `(R, β, |Z|)` space; state which observables carry the discriminating power (sign: Tracker; `|Z|`: multiple subsystems; mass: `R` and `β`).
2. **Blinded or masked region.** Define before examining data; mask the signal region in plots, logs, and optimization; state who may unblind and when.
3. **Misidentification paths.** Charge-sign confusion of the abundant same-`|Z|` matter (e.g. `He → anti-He`) via Tracker tails and bad hit assignment; `|Z|` confusion from fragmentation and charge-changing interactions; secondary tracks; wrong mass from `β` errors; interactions producing antiparticles.
4. **Redundant signed-rigidity fits and hit-pattern checks.** Compare independent partial fits (e.g. different layer subsets or upper/lower segments) for sign consistency; require consistency on data and MC.
5. **Subsystem charge consistency** before and after the magnet and material traversal; TOF, Tracker, and RICH `|Z|` estimators agree within validated tails.
6. **Charge-changing interactions and secondary tracks** modeled and validated on abundant samples.
7. **Data-driven validation of non-Gaussian tails.** Use abundant matter samples (e.g. helium and protons under looser cuts) to measure the sign-flip tail probability as a function of rigidity, and its extrapolation to the tight selection; ensure the extrapolation assumptions are tested.
8. **Candidate-level diagnostics** defined before unblinding (event display checklist, hit pattern, residuals, partial-fit consistency, subsystem estimators).
9. **Likelihoods.** Background-only and signal-plus-background (see [inference-and-unfolding](inference-and-unfolding.md#rare-and-low-count-inference)); with nuisance parameters for tail probability, efficiency, and exposure; constructed interval or CLs with toys; check coverage in the low-count regime.
10. **Expected sensitivity and coverage before examining the signal region.**
11. **Exposure.** Rigidity-dependent acceptance × efficiency × livetime × geomagnetic transmission for the signal species; a flux limit `Φ_UL = N_UL/(E·Δx)` or a ratio limit relative to matter.

## Reporting policy

Distinguish four levels, with predefined thresholds and wording: **candidate** (an event that passes the full selection, subject to diagnostics), **excess** (a statistical deviation with stated local/global significance), **evidence** (a predefined significance threshold exceeded with validated background), **discovery** (a higher predefined threshold, validated tails, independent review). A candidate list is not an excess; an excess is not a discovery. A conference statement is preliminary unless a paper says otherwise; media and rumor are navigation aids only. Never invent counts, rigidities, masses, significances, or sensitivities.

## Cross-checks

Orthogonal identification chains; alternative discriminants; loose/tight variations; alternate track fits and hit patterns; period/geometry splits; charge-sign splits; data-driven vs MC backgrounds; alternate templates, responses, priors; signal injection; closure, pulls, coverage; abundant-sample validation for rare tails; comparison with published results as plausibility only.

## Failure modes

- Charge confusion estimated from the Gaussian core only.
- Positron fraction denominators or shared systematics ignored; the fraction treated as if acceptance cancels fully.
- ECAL variables used both to define the lepton sample and to derive the template that measures it.
- Rare-candidate analysis without blinding, sidebands, or predefined diagnostics; candidates reported as discovery.
- Fabricated candidate counts, significances, or rejection factors.
- Template fit tuned repeatedly on the fitted data; signal-contaminated proton template.

## Required source classes

Tier 1: S02-S05 (e±), S08-S09 (antiproton), Phys. Rept. Part II (S01). Antihelium/antideuteron: Tier 1 if a paper exists (check INSPIRE, ams02.space), else Tier 3 conference material labeled preliminary and Tier 5/6 theory interpretation labeled as third-party; AMS-01 limit (S22) is Tier 1 but historical. Tier 4 for finite-count statistics and CLs.

## Questions to ask the user

Which target: fraction, separate fluxes, combined flux, antiproton, or a rare-antimatter search? Energy vs rigidity variable? Public results or internal? Which charge-confusion control do you have? Is the signal region blinded? Which data period and hardware era? Do you have template provenance and finite-statistics inputs?
