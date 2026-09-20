# Time-Dependent Analysis: Temporal Fluxes, Solar Modulation, Periodicity

## When to read this file

Read only for time-resolved fluxes or ratios, solar-cycle or solar-modulation comparisons, time-stability checks of a result, periodicity or "does the flux oscillate" searches, and joint fits across data-taking periods. Do not load it for a time-integrated flux, a detector question, or a source-status question. Time-integrated blueprints are in [charged-cosmic-rays](charged-cosmic-rays.md); the conditions model and drift handling are in [reconstruction-and-data-quality](reconstruction-and-data-quality.md#conditions-model); nuisance and covariance rules are in [calibration-mc-systematics](calibration-mc-systematics.md#propagation-and-correlations) and [inference-and-unfolding](inference-and-unfolding.md#covariance-requirements).

## Contents

1. [Evidence boundary](#evidence-boundary)
2. [Time binning](#time-binning)
3. [Exposure, livetime and time-dependent detector state](#exposure-livetime-and-time-dependent-detector-state)
4. [Geomagnetic cutoff in time bins](#geomagnetic-cutoff-in-time-bins)
5. [Correlations across time and rigidity](#correlations-across-time-and-rigidity)
6. [Charge-sign-dependent modulation](#charge-sign-dependent-modulation)
7. [Periodicity searches and look-elsewhere](#periodicity-searches-and-look-elsewhere)
8. [Joint likelihood across periods](#joint-likelihood-across-periods)
9. [Failure modes](#failure-modes)
10. [Required source classes](#required-source-classes)
11. [Questions to ask the user](#questions-to-ask-the-user)

## Evidence boundary

Everything below is **[General method]** or **[Proposal]** unless it carries a claim ID. The ledger supports only these time-related AMS statements, each with its own scope in [source-index](source-index.md):

- **[Documented, C27, S13; C29, S14]** The deuteron analysis used 33 time periods of four Bartels rotations (108 days), May 2011 to April 2021; the Li-isotope analysis used 42 such periods to October 2023. This is the choice of those two analyses, not a rule for other species or ranges.
- **[Documented, C10, S13; C09, S12; abstract level]** The deuteron flux time variation is nearly identical to that of protons, ³He and ⁴He; above 4 GV the ³He/⁴He ratio is time-independent.
- **[Documented, C07, S09; abstract level]** Over an 11-year solar cycle, 1.00-41.9 GV, antiprotons show a smaller time variation than protons, electrons and positrons.
- **[Documented, C16, S16; titles only]** AMS published time-structure results as matched pairs across species and charge sign.
- **[Documented, abstract level, C36-C42; S41-S47]** AMS reported daily proton, helium, electron and positron fluxes with recurrent 27-day variations (2014-2018 for protons and helium), shorter 13.5-day and 9-day cycles (2016 for protons and helium), strength that depends on time and rigidity (C36, C37, C40); a hysteresis between electron and proton fluxes, and between electron and positron fluxes, below about 8.5 GV (C40, C41); positron variations similar to proton and unlike electron, with positrons modulated more than protons below about 7 GV (C41); proton and helium fine structures nearly identical below 40 GV (C38); nuclei He-O with similar but not identical variations whose differences correlate with spectral-index differences, with no A/Z velocity-dependence effect observed (C42); the Bartels-rotation lepton paper S42 is in energy (1-50 GeV, C39). Quote only with the species, range and period in the claim, and put the claim ID (C##) on every [Documented] tag in an answer, not only a level label. Do not merge the two thresholds: about 8.5 GV is where the electron/proton and electron/positron hysteresis appears, about 7 GV is where positrons are modulated more than protons (C40, C41).
- **[Documented, full-text main articles, C43-C49; S41-S47; scopes differ: C43-C47 are daily-flux or hysteresis claims, C48-C49 are the Bartels-rotation lepton and nuclei products]** How AMS built its time-resolved results: fluxes per day (proton, helium, electron, positron) or per Bartels rotation (proton, helium, nuclei, leptons) with `Φ = N / (A ε T ΔR)`, migration unfolded independently in each time bin, and acceptance, trigger efficiency and collection time per bin (C43, C46, C49); exposure per rotation from livetime-weighted seconds above the geomagnetic cutoff, in normal conditions, within 40° of zenith and outside the South Atlantic Anomaly, with a small time-dependent acceptance correction (C48); systematics split into time-independent and time-dependent parts, the latter (efficiencies evaluated each day) added in quadrature (C44, daily proton flux S43); a wavelet time-frequency analysis with normalized power and 95% confidence levels for periodicities (C45, C52: daily proton flux S43 only, not all time-structure results); hysteresis shown by plotting one flux against another with 14-rotation moving averages (C47). The daily electron and positron papers bin in rigidity (1.00-41.9 GV, C40, C41), whereas the Bartels-rotation lepton paper and the time-integrated lepton fluxes bin in energy (C48, C24, C25); state which variable defines your bins. Supplemental Material text adds (C51-C53): the daily collection time counts only seconds in normal conditions, within 40° of zenith and outside the South Atlantic Anomaly, and is strongly rigidity dependent because of the geomagnetic field, with the daily-proton cutoff computed from AMS data itself (C51); wavelet normalized power is the wavelet power over the series variance, and the 95% confidence level comes from Monte Carlo lag-1 autoregressive (red-noise) surrogates matched to the measured variance and lag-1 autocorrelation (C52); the hysteresis significance compares the two intervals with equal flux of one species that show the largest difference in the other flux, then repeats over the remaining non-overlapping intervals (C53). These are the choices of those analyses, not rules.
- **[Documented, C31, S06]** One proton analysis kept only quality time with live time above 50%, the instrument axis within 40° of zenith, and outside the South Atlantic Anomaly; that is one analysis's conditions.

**Evidence gap (not filled here).** The main articles of the time-structure, periodicity and nuclei solar-modulation papers (S41-S47, split out of S16 and S20) were read, and the Supplemental Material text of S41-S47 was read (S41, S42, S44, S47 on 2026-09-21: C54-C58, including that the daily helium analysis uses a 40-degree pointing cut and a data-derived cutoff whereas the Bartels-rotation nuclei analysis uses 30 degrees and 1.2 times the IGRF cutoff, so neither is a rule); the supplemental data tables were not transcribed and the Phys. Rept. review was not read. The ledger therefore does not say how the systematic errors are correlated across days or rotations (no covariance model appears in the text read), or whether any trial-factor or look-elsewhere correction was applied to the periodicity or hysteresis significances (none is described in the text read, which is not proof of absence). Treat those as **[Unknown/needs input]**; do not supply AMS operational detail. Closing the gap means reading the numerical supplemental tables and adding scoped claims.

## Time binning

- **[General method]** Choose the bin length from the estimand: a solar-cycle trend needs coarse bins with small statistical error; a periodicity or short-term-stability study needs bins short compared with the shortest period of interest (fewer than two bins per cycle cannot resolve it).
- **[General method]** The bin must contain enough events in the least populated rigidity bin for the chosen inference (Poisson-exact or toy-validated at low counts, see [inference-and-unfolding](inference-and-unfolding.md#rare-and-low-count-inference)). At high rigidity, either lengthen the time bins or merge rigidity bins; state the rigidity range where time resolution is supported.
- **[General method]** A Bartels rotation is a fixed 27-day count; four rotations are 108 days, matching C27. Aligning bins to rotations makes bins comparable but does not remove exposure differences within them.
- **[General method]** Bin edges must include hardware-era and reconstruction-version boundaries (a change breaks the response and templates; see the conditions model). Do not let one bin straddle a boundary.
- **[Proposal]** Fix binning, rigidity range and the stability metric before looking at the time dependence, and record any later change.

## Exposure, livetime and time-dependent detector state

- **[General method]** Every time bin `k` has its own exposure: `Φ_k = (N_k - b_k) / (E_k ΔR)` with `E_k = Σ A_eff T_live × transmission` accumulated inside the bin. Average fluxes only through counts and exposures, never by averaging fluxes of bins with different exposure.
- **[General method]** Livetime, acceptance, efficiency and detector state can each vary with time; keep them distinct ([efficiency-acceptance-backgrounds](efficiency-acceptance-backgrounds.md#acceptance-exposure-livetime)). A drift is corrected in one category only (veto, calibration, efficiency or response), never twice ([reconstruction-and-data-quality](reconstruction-and-data-quality.md#four-categories-of-correction)).
- **[General method]** Show stability with a metric and a trigger: an abundant control species' rate or an efficiency versus time, flat after livetime and cutoff correction; a drift beyond the tolerance adds a period-split, a scale factor with uncertainty, or a systematic.
- **[Unknown/needs input]** Per-period efficiency, acceptance and calibration values are analysis inputs; none are supplied here.

## Geomagnetic cutoff in time bins

- **[General method]** The cutoff depends on position, direction and time, and the fraction of a bin's time spent above a given rigidity varies between bins, so the exposure at low rigidity is bin-dependent. Compute transmission per bin, not once for the whole period.
- **[Documented, C31, S06; C27, S13]** The public analyses used a cutoff safety factor (1.2 in the proton analysis, varied 1.0-1.4 in the deuteron analysis) with the variation treated as a systematic; that is scope-limited practice, not a universal value.
- **[General method]** Low-rigidity bins are the most sensitive to the cutoff model, and the sensitivity can differ between charge signs; propagate the model variation per bin and per sign.

## Correlations across time and rigidity

- **[General method]** Statistical fluctuations are independent between time bins built from disjoint events. Systematics are not: classify each as persistent (calibration, template shape, cross-section model: correlated across all periods), slowly varying (correlated between neighbouring bins), or independent per period, and across rigidity as normalization, smooth shape, or independent.
- **[General method]** Build one covariance over (time, rigidity) with a documented ordering. A Kronecker product of a time matrix and a rigidity matrix is valid only if the correlation truly factorizes; state and test that. Check the combined matrix with `scripts/validate_covariance.py`.
- **[General method]** Normalizing every period to a reference period cancels only the persistent part of the systematics, and correlates the statistical errors of all periods with the reference; carry that covariance.

## Charge-sign-dependent modulation

- **[General method]** Solar modulation depends on the sign of the particle charge through drifts in the heliospheric magnetic field, whose polarity reverses over the solar cycle, so particles of opposite sign need not follow the same time variation. Comparing e⁺ with e⁻ or p̄ with p over time therefore requires the same time bins, rigidity or energy variable, exposure treatment, and sign-specific cutoff and charge-confusion handling.
- **[General method]** A time-dependent ratio or fraction follows the ratio blueprint ([charged-cosmic-rays](charged-cosmic-rays.md#ratio-or-fraction-blueprint)): cancellations are classified per effect and the numerator-denominator covariance is carried through time.
- **[General method]** The measurement is the time dependence of the flux or ratio; a modulation model, a force-field parameter, or a drift interpretation is a separate model step with its own assumptions (see result interpretation in [source-policy](source-policy.md#result-interpretation)).
- **[Documented, C07, S09; abstract level]** Do not quote more than the abstract-level statement: antiprotons vary less than protons, electrons and positrons in the stated range and period.

## Periodicity searches and look-elsewhere

- **[General method]** Define before the analysis: the frequency or period band, the test statistic, the observable (flux, ratio, or a control quantity), and the significance threshold. Unevenly sampled or unequal-exposure series need a method that handles that sampling and weights by the bin uncertainties.
- **[General method]** A search over many trial periods has a look-elsewhere effect: report local and global significance (Gross and Vitells trial factors, S37) and calibrate with toys that reproduce the sampling, the exposure pattern and the correlated systematics; do not use Wilks or a single-frequency p-value.
- **[General method]** Apparent periodicities can come from exposure, orbit, season or detector-state cycles. Apply the same search to an exposure time series, an efficiency series and a control species, and treat a coincident signal there as a systematic, not a discovery.
- **[Unknown/needs input]** Which method and trial-factor treatment AMS used is documented only in part: a wavelet time-frequency analysis with 95% confidence levels from red-noise Monte Carlo surrogates (C45, C52); any trial-factor treatment is not described in the text read. Time-series method references are also not indexed (a Tier 4 gap).

## Joint likelihood across periods

- **[General method]** `L = Π_k Π_i Poisson(n_ki | μ_ki(θ_shared, φ_k, η)) × constraints`, with `θ_shared` for parameters common to all periods (for example spectral shape), `φ_k` for period-specific ones (normalization, modulation), and nuisances `η` shared or per-period according to the correlation classification above. Each period has its own exposure and, if the resolution or efficiency changed, its own response.
- **[General method]** Test the joint model against separate fits with toys before trusting a combined result; a shared-shape hypothesis is a hypothesis, not a definition.
- **[General method]** Do not combine periods that use different definitions (rigidity ranges, track configurations, cutoff treatment); explain the difference instead of averaging ([source-policy](source-policy.md#conflicts-between-sources)).
- **[Proposal]** Report per-period results with their covariance and the exposures, so others can refit; a single combined number hides the time dependence.

## Failure modes

- Averaging fluxes of bins with different exposure; using one cutoff transmission for every bin.
- Treating a time-dependent calibration drift as both a veto and an efficiency correction.
- Independent errors assumed across periods while persistent systematics are shared.
- A periodicity claimed from a single-frequency p-value or without an exposure and control-series check.
- Reading charge-sign differences in modulation as detector-independent physics without sign-specific handling.
- Quoting the deuteron or Li-isotope binning (108 days) or the proton quality-time conditions as AMS-wide rules.
- Filling the evidence gap with invented AMS livetime, calibration, or search details.

## Required source classes

Tier 1 AMS papers for what AMS measured and how a specific analysis binned time (S09, S12-S14, S41-S47 main articles; Supplemental Material text for S43, S45, S46 only); Tier 4 methodology for trial factors and likelihood construction (S30, S37); heliospheric-modulation models are theory-literature interpretation (Tier 6 unless peer-reviewed methodology).

## Questions to ask the user

Which species and rigidity range, and what time span? Time-resolved flux, ratio, stability check, or periodicity search? Do you have per-period livetime, exposure, and calibration records? Which hardware eras and reconstruction versions fall inside the span? Are results to be compared across charge signs? Is the period band and trial range fixed in advance?
