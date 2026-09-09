# AMS-02 Case Study: A Long-Duration Space-Based Spectrometer

Applies the generic detector-technology references
([references/23-detector-systems-overview.md](23-detector-systems-overview.md)
through [particle identification](26-particle-identification.md)) and
[space-based direct detection](37-space-based-direct-detection.md) to a specific,
real instrument: the Alpha Magnetic Spectrometer (AMS-02), operating on the
International Space Station since 2011. This is a worked case study of how those
generic principles combine in one apparatus, not a substitute for the AMS
collaboration's own technical publications - instrument parameters and results
quoted from a real publication must be cited to that publication; anything not so
cited here is illustrative only, per this skill's general sourcing discipline (see
[references/13-sources.md](13-sources.md)).

## Subsystem stack

AMS-02 combines, in the layered order described generically in
[references/23-detector-systems-overview.md](23-detector-systems-overview.md):

- **A silicon microstrip tracker inside a permanent magnet**, giving rigidity via
  curvature as in any magnetic spectrometer - see the rigidity, maximum-detectable-
  rigidity, and multiple-scattering treatment in
  [references/23-detector-systems-overview.md](23-detector-systems-overview.md) and
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
- **A ring-imaging Cherenkov detector (RICH)** below the tracker, giving a
  precise independent velocity measurement for charge and, combined with rigidity,
  isotope separation - the most demanding PID application described in
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

- **No on-orbit repair of the tracking/magnet system.** Unlike a collider detector
  with scheduled shutdowns for maintenance, AMS-02's core subsystems must be stable,
  self-monitoring, and degrade gracefully for the mission's full duration. Any
  time-dependent drift in tracker alignment or magnet field (from thermal cycling on
  each ISS orbit, or long-term aging) must be tracked and corrected per data-taking
  period, not calibrated once - see
  [calibration and alignment](31-calibration-and-alignment.md) for the general
  alignment-weak-mode and conditions-time-dependence treatment this requires.
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
   [references/04-histograms-efficiencies.md](04-histograms-efficiencies.md).
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
   [references/08-inference.md](08-inference.md) and
   [references/39-astroparticle-statistics.md](39-astroparticle-statistics.md), not as
   an absence-of-evidence claim.

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
- For a fraction/ratio measurement: confirmation that the two yields share
  (approximately) the same acceptance, and the exact error propagation used (see
  `scripts/particle_ratio_with_uncertainty.py`) rather than a naive quadrature
  combination that assumes independence when the two yields may share systematics.
- For any concrete instrument parameter or published result quoted from AMS-02: the
  specific publication or official source it was checked against.
