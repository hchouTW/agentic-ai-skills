# AMS-02 Case Study: A Long-Duration Space-Based Spectrometer

Applies the generic detector-technology references
([23-detector-systems-overview.md](23-detector-systems-overview.md)
through [particle identification](26-particle-identification.md)) and
[space-based direct detection](37-space-based-direct-detection.md) to a specific,
real instrument: the Alpha Magnetic Spectrometer (AMS-02), operating on the
International Space Station since 2011. This is a worked case study of how those
generic principles combine in one apparatus, not a substitute for the AMS
collaboration's own technical publications - instrument parameters and results
quoted from a real publication must be cited to that publication; anything not so
cited here is illustrative only, per this skill's general sourcing discipline (see
[13-sources.md](13-sources.md)).

## Subsystem stack

AMS-02 combines, in the layered order described generically in
[23-detector-systems-overview.md](23-detector-systems-overview.md):

- **A silicon microstrip tracker inside a permanent magnet**, giving rigidity via
  curvature as in any magnetic spectrometer - see the rigidity, maximum-detectable-
  rigidity, and multiple-scattering treatment in
  [23-detector-systems-overview.md](23-detector-systems-overview.md) and
  `scripts/multiple_scattering.py`. The magnet is a **permanent** magnet, not a
  superconducting one - a deliberate choice for a decade-plus space mission with no
  possibility of on-orbit cryogenic servicing, trading a smaller bending power
  (and hence a lower maximum detectable rigidity than a comparable superconducting
  design) for operational reliability over the mission lifetime.
- **A transition radiation detector (TRD)** above the tracker/magnet, for
  electron/positron versus proton/nucleus separation via the Lorentz-factor-dependent
  yield described in [particle identification](26-particle-identification.md) - the
  primary handle for the positron-fraction and electron-flux measurements, since a
  TRD's rejection is a `gamma`-dependent property that dE/dx and the calorimeter alone
  cannot provide at the relevant energies.
- **Upper and lower time-of-flight (TOF) planes**, bracketing the tracker, giving
  velocity, the trigger, and - critically for a space-based (not accelerator-
  synchronized) instrument - the **direction of travel**: distinguishing genuine
  downward-going cosmic rays from upward-going albedo/backscattered particles is a
  TOF-timing measurement, not an assumption, per the general TOF discussion in
  [particle identification](26-particle-identification.md).
- **Anti-coincidence counters (ACC)**, a scintillator veto lining the magnet bore
  around the tracker, rejecting tracks from particles entering through the side
  rather than along the instrument's acceptance cone. This is the second
  independent handle (alongside TOF timing/directionality) for excluding
  non-genuine tracks before any charge or rigidity measurement is trusted - an
  event failing the ACC veto should not enter a flux or ratio measurement's
  denominator at all, rather than being corrected for downstream.
- **A ring-imaging Cherenkov detector (RICH)** below the tracker, with two
  radiators of different refractive index (a sodium-fluoride radiator and a
  silica-aerogel radiator, per the collaboration's own site - verify the exact
  configuration against the instrument publication before quoting it) giving
  velocity coverage across a wider β range than a single radiator could, plus a
  precise independent velocity measurement for charge and, combined with
  rigidity, isotope separation - the most demanding PID application described in
  [particle identification](26-particle-identification.md).
- **An electromagnetic calorimeter (ECAL)** at the bottom, giving an independent
  energy measurement and shower-shape discrimination that, combined with the TRD and
  the tracker's `E/p`-like consistency check, is the second independent handle (beyond
  the TRD) separating positrons from the far more abundant proton background - the
  same "do not sum correlated PID inputs as independent" caution in
  [particle identification](26-particle-identification.md) applies directly:  ECAL
  shower shape and TRD yield are largely independent (different physical processes),
  but either combined naively with tracker dE/dx double-counts the ionization
  information already used elsewhere.

Every rare-species measurement AMS-02 makes - positron fraction, antiproton/proton
ratio, individual elemental spectra, an antihelium search - depends on combining
several of these subsystems' PID information into a single background-rejection
likelihood or a sequential-cut selection, exactly the combination discipline in
[particle identification](26-particle-identification.md).

## What is distinctive about a decade-plus space-based mission

- **Servicing is the rare, hard-won exception, not the default to assume.** Most
  space-based instruments get zero post-launch hardware access; AMS-02 is a
  notable exception precisely because it was not designed for it. NASA astronauts
  performed a multi-EVA campaign (November 2019-January 2020) to repair its
  thermal/cooling system - reported independently by NASA, *Scientific American*,
  phys.org (as among "the most challenging spacewalks since Hubble"), and
  NASASpaceflight.com - and the collaboration's own site describes a 2025 Tracker
  Layer-0 hardware upgrade (an added tracker plane, +300% acceptance). Neither
  changes the general planning assumption for *other* missions - budget for zero
  servicing unless a mission specifically provides for it - but for AMS-02
  specifically, an analysis spanning these dates must account for the actual
  hardware configuration active in each period, not assume the instrument was
  static for its full run. Any time-dependent drift in tracker alignment or
  magnet field within a stable-hardware period (from thermal cycling on each ISS
  orbit, or long-term aging) must still be tracked and corrected per data-taking
  period, not calibrated once - see
  [calibration and alignment](31-calibration-and-alignment.md) for the general
  alignment-weak-mode and conditions-time-dependence treatment this requires.
  Verify the exact servicing/upgrade dates and scope against NASA/AMS collaboration
  sources before citing them in an analysis; this summary is current as of
  2026-09-10 (see [13-sources.md](13-sources.md)).
- **Orbital thermal cycling.** The ISS orbit produces a roughly 90-minute thermal
  cycle (day/night per orbit) that can measurably shift detector alignment and gain;
  an analysis spanning many orbits must either correct for or bin out this periodic
  systematic rather than average over it as if conditions were static.
- **A time-varying geomagnetic cutoff along the orbit.** The ISS's ~51.6-degree
  orbital inclination and ~400 km altitude mean the instrument crosses a wide range of
  geomagnetic latitudes on every orbit, so the local geomagnetic cutoff (see
  [space-based direct detection](37-space-based-direct-detection.md) and
  `scripts/geomagnetic_cutoff.py`) is not a single number for the mission but a
  distribution that must be evaluated (or excluded from, for regions/times too close
  to cutoff) per event, using the actual spacecraft position and pointing at the time
  of detection, not a single representative latitude.
  `scripts/orbit_averaged_geomagnetic_cutoff.py` gives the exposure-weighted range for
  planning-level estimates; a real analysis uses the full time-and-position-resolved
  cutoff from orbit ephemeris and field-model backtracing, per the caveat already
  stated for the single-latitude formula in
  [space-based direct detection](37-space-based-direct-detection.md).
- **A mission spanning multiple solar cycles.** Because solar modulation (see
  [space-based direct detection](37-space-based-direct-detection.md) and
  `scripts/solar_modulation_force_field.py`) varies over an ~11-year cycle, a
  multi-year AMS-02 time series is itself a measurement of solar modulation, not just
  a single averaged spectrum - published low-rigidity spectra are commonly split into
  time bins (e.g. Bartels-rotation or multi-month periods) explicitly to resolve this,
  and combining time bins into one spectrum without accounting for the modulation
  potential's variation over the combined period reintroduces the same bias a
  collider analysis avoids by stating its luminosity-weighted running conditions.

## Rare-species measurement pattern

Positron fraction, antiproton/proton ratio, and an antihelium search share a common
analysis structure worth naming explicitly:

1. **They are ratios or fractions of two yields from the same detector and
   (approximately) the same acceptance**, which cancels a large part of the
   acceptance/exposure systematic that an absolute flux measurement cannot avoid -
   the same logic as an efficiency ratio in
   [04-histograms-efficiencies.md](04-histograms-efficiencies.md).
   `scripts/particle_ratio_with_uncertainty.py` implements the corresponding exact
   error propagation for two independent yields with their own uncertainties.
2. **The background for the rarer species is the far more abundant one
   mis-identified**, so the PID working point is chosen for rejection power against
   an overwhelming background rather than for a balanced efficiency/purity trade-off,
   and the residual contamination must be modeled and subtracted (a template fit is
   standard) rather than assumed negligible - see
   [particle identification](26-particle-identification.md)'s priors-and-abundance
   caution, which is exactly the regime a positron measurement (roughly
   10^2-10^4 protons per positron, depending on energy) sits in.
3. **A null or marginal result (e.g. an antihelium search) is reported as an
   exposure-normalized upper limit**, using the same Poisson/likelihood machinery as
   any other rare-event search in
   [08-inference.md](08-inference.md) and
   [39-astroparticle-statistics.md](39-astroparticle-statistics.md), not as
   an absence-of-evidence claim.

## Primary/secondary composition as a propagation diagnostic

AMS-02's elemental-spectrum measurements are a concrete instance of the generic
secondary-to-primary propagation diagnostic in
[cosmic-ray spectrum and composition](32-cosmic-ray-spectrum-and-composition.md#propagation):
a falling secondary-to-primary ratio with rising rigidity signals less material
traversed (shorter effective path length) at higher rigidity, constraining the
Galactic propagation model rather than the source spectrum.

- AMS-02's own published catalog separates cleanly along this line: **primaries**
  it has measured include He, C, O, Fe, Ne, Mg, Si, N, Na, and Al (accelerated and
  injected directly at the source), while **secondaries** include Li, Be, B, and F
  (produced by spallation of primaries on the interstellar medium during
  propagation, per the generic treatment in
  [cosmic-ray spectrum and composition](32-cosmic-ray-spectrum-and-composition.md)).
  Sorting a claimed measurement into the correct bucket before interpreting a
  rigidity dependence is the first check - a primary's spectral shape carries
  source/acceleration information directly, while a secondary's carries mostly
  propagation information convolved with its parent primaries' spectra.
- **Precision Measurement of the Boron to Carbon Flux Ratio**, Phys. Rev. Lett.
  117, 231102 (2016), is AMS-02's direct instance of the B/C propagation
  diagnostic named generically in
  [cosmic-ray spectrum and composition](32-cosmic-ray-spectrum-and-composition.md).
- **Observation of the Identical Rigidity Dependence of He, C, and O Cosmic Rays
  at High Rigidities**, Phys. Rev. Lett. 119, 251101 (2017), is the complementary
  primary-side result: multiple primary species sharing the same rigidity
  dependence at high rigidity is itself evidence about shared acceleration/
  propagation history, distinct from what a single species' spectrum alone could
  establish - the same "compare species, not just fit one spectrum in isolation"
  logic the case study's rare-species pattern above applies to ratios.

## Temporal structure and periodicity analysis

A large fraction of AMS-02's published output is a time-series analysis of its
own flux measurements, applying the periodicity-search technique in
[space-based direct detection](37-space-based-direct-detection.md#searching-for-periodicity-and-time-structure-in-a-flux-time-series)
to a decade-plus, multi-solar-cycle dataset that few other instruments have the
duration to support:

- *Observation of Fine Time Structures in the Cosmic Proton and Helium Fluxes...*,
  Phys. Rev. Lett. 121, 051101 (2018), and its electron/positron counterpart,
  *Observation of Complex Time Structures in the Cosmic-Ray Electron and Positron
  Fluxes*, Phys. Rev. Lett. 121, 051102 (2018) - published as a matched pair,
  consistent with the charge-sign-comparison diagnostic named generically above:
  the same time structure checked across species of different charge sign.
- *Periodicities in the Daily Proton Fluxes from 2011 to 2019... from 1 to 100
  GV*, Phys. Rev. Lett. 127, 271102 (2021), and *Properties of Daily Helium
  Fluxes*, Phys. Rev. Lett. 128, 231102 (2022) - a multi-year daily-cadence
  analysis, the regime where the bin-cadence-versus-systematic-stability tradeoff
  named generically above is most consequential.
- *Temporal Structures in Positron Spectra and Charge-Sign Effects...*, Phys.
  Rev. Lett. 131, 151002 (2023), and *Temporal Structures in Electron Spectra and
  Charge Sign Effects...*, Phys. Rev. Lett. 130, 161001 (2023) - again published
  as a matched particle/antiparticle (or opposite-charge-species) pair, for the
  same reason: a shared instrumental or environmental artifact would show up
  identically in both, while a genuine heliospheric-transport effect should not.

The consistent pattern across this cluster - publish matched pairs across a
charge-sign boundary rather than a single species' time series alone - is worth
recognizing as a deliberate analysis design choice, not a coincidence of what
happened to be measured.

## Analysis-technique improvements are sometimes their own publication

Not every incremental analysis improvement a long-running collaboration makes
stays internal - some are published as dedicated instrumentation papers, separate
from the physics-result letters. Two concrete, independently citable examples for
AMS-02's tracker and calorimeter:

- **A cross-strip charge-division nonlinearity correction for tracker coordinate
  measurement**, published in G. Ambrosi et al., *Nucl. Instrum. Methods Phys.
  Res. A* **869**, 29 (2017): the standard two-strip amplitude-ratio position
  estimator is corrected by a charge-dependent function derived from the known
  isotropy of cosmic-ray arrival directions (deviations from a uniform position
  distribution reveal the detector's own nonlinearity), improving position
  resolution by roughly a factor of 2 for carbon and more for heavier nuclei.
  This is a concrete instance of the general position-resolution treatment in
  the tracking references - a correction derived from a physics prior (isotropy)
  applied to remove a detector-response artifact, not a physics effect.
- **A seven-parameter three-dimensional shower parametrization for ECAL energy
  reconstruction**, published in A. Kounine et al., *Nucl. Instrum. Methods Phys.
  Res. A* **869**, 110 (2017): shower energy, three-dimensional shower-maximum
  position, two axis angles, and a longitudinal scale parameter, fit per-event to
  the cell-by-cell energy deposition. A concrete worked instance of the
  shower-shape-based reconstruction and discrimination discussed generically for
  calorimetry.

**The lesson for any collaboration's own "advances" page or internal analysis
notes**: don't assume a uniform answer to "is this citable literature or just an
internal note" across an entire category of page. Checking `ams02.space/
advances-data-analysis` directly shows a mixed picture - the two techniques above
each resolve to a specific NIM A paper, while other pages on the same site
section (checked for a different purpose in `academic-papers`'s coverage of this
site) show no such citation for a *different*, apparently more recent in-house
improvement. Check each specific claimed technique's publication status
individually (INSPIRE-HEP, the journal, or asking the collaboration) rather than
generalizing from one checked example to the whole category, in either direction.

## Deliverables

- Which subsystems' PID information contributed to a reported selection, the
  correlation structure between them (if any inputs share the same underlying
  ionization or timing measurement), and the working-point efficiency/rejection at
  each stage.
- Whether reported results are time-binned to resolve solar-modulation and
  geomagnetic-cutoff variation over the analyzed period, or averaged over it, and (if
  averaged) the resulting systematic.
- The tracker/magnet alignment and gain calibration cadence relative to the orbital
  thermal cycle and to any long-term aging trend.
- Whether the analyzed period spans a known hardware-configuration change (the
  2019-2020 cooling-system EVA repair, the 2025 Tracker Layer-0 upgrade, or any
  later servicing) - if so, whether the analysis treats the periods separately or
  states why a combined treatment is still valid.
- For a fraction/ratio measurement: confirmation that the two yields share
  (approximately) the same acceptance, and the exact error propagation used (see
  `scripts/particle_ratio_with_uncertainty.py`) rather than a naive quadrature
  combination that assumes independence when the two yields may share systematics.
- For any concrete instrument parameter or published result quoted from AMS-02: the
  specific publication or official source it was checked against.
- For any claimed analysis-technique improvement: whether it resolves to a
  specific instrumentation paper (as with the two NIM A examples above) or is
  only illustrative in-house/website content - checked individually, not assumed
  from another technique's citation status.
