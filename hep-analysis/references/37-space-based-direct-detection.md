# Space-Based and Balloon-Borne Direct Cosmic-Ray Detection

Covers cosmic-ray measurements made *above the atmosphere* (satellite or long-duration
balloon magnetic spectrometers and calorimeters, e.g. AMS-02-class instruments), where
individual nuclei are measured directly rather than inferred from an air shower. The
detector technology - magnetic spectrometry, calorimetry, TOF, TRD, RICH - is exactly
the material in
[23-detector-systems-overview.md](23-detector-systems-overview.md) through
[26-particle-identification.md](26-particle-identification.md), applied
unchanged; this file covers what is specific to the near-Earth space environment:
geomagnetic and solar effects that ground- and space-based measurements alike must
correct for, and that have no collider-physics analog.

## Rigidity, not energy, is the natural variable

As in any magnetic spectrometer (see
[23-detector-systems-overview.md](23-detector-systems-overview.md)), a
space-based instrument directly measures rigidity `R = pc/(Ze)`, and every
geomagnetic and solar effect below acts on rigidity, not on energy or momentum
separately - because both the geomagnetic field's confinement and a Fermi-accelerated
source's maximum energy are set by how a particle's gyroradius compares to a length
scale, which depends on `p/(Ze)`. Reporting a direct-detection flux in kinetic energy
per nucleon rather than rigidity discards this natural scaling and makes comparison
across species (which differ in `Z` and `A`) needlessly indirect.

## Geomagnetic cutoff

The Earth's magnetic field acts as a rigidity filter: a charged particle arriving from
a given direction at a given geomagnetic location can only reach the top of the
atmosphere (or a near-Earth satellite) if its rigidity exceeds a minimum, the
**geomagnetic cutoff rigidity**. For a simple dipole approximation, the vertical
(zenith-pointing) cutoff at geomagnetic latitude `lambda_m` is the **Störmer cutoff**:

    R_c = (M / r^2) * cos^4(lambda_m) / (1 + sqrt(1 + cos^3(lambda_m)))^2

with `M` the Earth's dipole moment and `r` the geocentric distance, giving a cutoff
of a few tens of GV at the geomagnetic equator falling to essentially zero at the
poles - the reason polar-orbit low-cutoff regions are preferred for measuring the
lowest-rigidity cosmic rays, and why any flux measurement from a satellite in an
inclined orbit must either restrict to high-cutoff geomagnetic regions for a clean
low-energy cutoff or explicitly model the orbit-averaged, direction-dependent cutoff
(off-vertical arrival directions have a higher, angle-dependent cutoff than the
vertical Störmer value, and the real, non-dipolar field further complicates this into
a "penumbra" of partially-forbidden trajectories requiring backtracing simulation
rather than the analytic formula). `scripts/geomagnetic_cutoff.py` evaluates the
analytic vertical Störmer cutoff as a first-order estimate; a rigorous cutoff for a
specific orbit and epoch requires particle backtracing through a full geomagnetic
field model and is not something the analytic formula replaces.

Below its local geomagnetic cutoff, any flux an instrument records at that rigidity
is not primary cosmic radiation reaching from outside the magnetosphere - it is
**re-entrant/albedo** particles (secondaries produced in the atmosphere and reflected
back upward) or trapped radiation-belt particles, and must be excluded from a
primary-spectrum measurement rather than corrected for.

## Solar modulation

The Sun's magnetized wind carries the heliospheric magnetic field outward, and its
turbulence scatters and decelerates incoming Galactic cosmic rays as they diffuse
inward - suppressing the flux below roughly a few tens of GV in a way that varies
with the ~11-year solar activity cycle (weaker suppression near solar minimum,
stronger near solar maximum) and, more weakly, with the ~22-year solar magnetic
polarity cycle (which affects the *charge-sign-dependent* drift pattern of cosmic rays
through the heliosphere, producing measurable differences between particle and
antiparticle modulation, e.g. electrons versus positrons, that a purely diffusive
treatment does not capture).

The standard first-order correction is the **force-field approximation**: treating
modulation as an effective energy loss characterized by a single **modulation
potential** `phi` (units of rigidity/potential, typically hundreds of MV), relating
the flux at 1 AU, `J(E)`, to the flux outside the heliosphere (the local interstellar
spectrum, LIS), `J_LIS(E_LIS)`, via

    J(E) = (2 m E + E^2) / (2 m E_LIS + E_LIS^2) * J_LIS(E_LIS),   E_LIS = E + |Z|*phi

for a particle of rest mass `m` and charge `|Z|`, evaluated at the same time as the
measurement. This is an effective, not physical, one-parameter model - it does not
capture charge-sign dependence, latitude dependence, or short-timescale transients -
and its use should be limited to what it is good for: comparing or combining
measurements made in similar solar conditions, and providing a rough LIS estimate
outside the range where a direct low-cutoff, low-solar-activity measurement exists.
Any comparison of fluxes from different epochs, instruments, or even different
detectors on the same mission across a long enough mission duration to span a
meaningful change in `phi`, must state the modulation potential (or the neutron-
monitor-count-rate proxy commonly used to track it) for each dataset compared.

**Forbush decreases** - sudden, transient flux depressions lasting days, caused by a
coronal mass ejection's magnetic structure sweeping past Earth - and **solar
energetic particle (SEP) events** - direct particle acceleration at the Sun or in
interplanetary shocks, producing a distinct, time-localized, typically softer-
spectrum flux enhancement dominated by protons and heavier ions up to at most a few
GeV/nucleon - are both short-timescale contaminants that a Galactic-cosmic-ray flux
measurement must identify (from neutron-monitor or space-weather-instrument data) and
exclude from the integration time window, rather than average over silently.

## Searching for periodicity and time structure in a flux time series

Beyond excluding transients, a long-duration mission's flux time series is itself
a measurement: heliospheric transport imprints known periodicities on top of the
smooth force-field trend, and finding or bounding them is a distinct statistical
task from fitting the time-averaged spectrum.

- **Know what period you're looking for before choosing a method.** A **known**
  period (the ~27-day solar (Bartels) rotation and its harmonics, or a diurnal
  cycle tied to the detector's own orbital/attitude geometry) is best tested with
  **epoch-folding / superposed-epoch analysis**: fold the time series at the
  candidate period and look for a coherent, above-noise modulation, rather than a
  free periodogram search, which pays an unnecessary trials penalty for a period
  you already have a physical reason to test. Reserve a periodogram (e.g.
  Lomb-Scargle, which handles the uneven sampling and data gaps a satellite
  time series generally has) for a genuinely unknown or approximate period, and
  correct its detection significance for the number of independent frequencies
  scanned - the same look-elsewhere-effect discipline as
  [39-astroparticle-statistics.md](39-astroparticle-statistics.md)'s trials-factor
  treatment, applied to frequency space instead of a sky position or mass bin.
- **Bin fine enough to resolve the structure, coarse enough to keep bins
  statistics-limited rather than systematics-limited.** A daily-flux time series
  needs per-day acceptance, livetime, and geomagnetic-cutoff corrections at that
  same cadence (see the per-event cutoff treatment above) - a periodicity search
  is only as good as the systematic stability of the bin-to-bin normalization it
  sits on top of.
- **Charge-sign dependence is itself a diagnostic, not just a nuisance.** Because
  the heliospheric magnetic polarity cycle produces genuinely different transport
  (gradient/curvature drift-dominated vs. diffusion-dominated, alternating roughly
  every 11 years) for positively- and negatively-charged particles, comparing the
  *same* candidate periodicity's amplitude and phase between a particle and its
  antiparticle (or between species of opposite sign, e.g. protons vs. electrons)
  tests whether an observed structure is drift-related or a shared instrumental/
  environmental artifact that would affect both signs identically.
- **State the epoch and solar-activity phase a periodicity claim covers.** A
  periodicity's amplitude and even its presence is not stationary across a solar
  cycle - report the date range and solar-activity phase (rising/maximum/
  declining/minimum) a detection or non-detection applies to, the same way the
  solar-modulation discussion above requires stating the modulation potential
  for a spectrum.

## Direct-detection composition and the local antiparticle excesses

Because a space-based spectrometer measures charge and mass directly (through the
PID chain in [26-particle-identification.md](26-particle-identification.md)),
it gives an unambiguous species and isotope identification that no ground-based
technique provides - the reason direct detection remains the reference measurement
for composition, isotopic ratios, and antiparticle fluxes, even though its
geometric-factor-limited exposure caps its reach well below the knee. The measured
**positron fraction** (positron flux relative to positron-plus-electron flux) rising
with energy above a few GeV, and a harder-than-secondary-production **antiproton**
spectrum at high rigidity, are the most consequential such results: standard secondary
production (cosmic-ray nuclei spallating on the interstellar medium, per
[cosmic-ray spectrum and composition](32-cosmic-ray-spectrum-and-composition.md))
predicts a falling positron fraction and a softer antiproton spectrum, so the excess
is interpreted either as evidence of nearby primary sources (pulsars are the leading
astrophysical candidate) or, more speculatively, as a signature of dark-matter
annihilation or decay - distinguishing the two requires the spectral shape, an
eventual high-energy cutoff or lack thereof, and consistency with other channels
(gamma-ray, anisotropy), not the excess alone.

## Deliverables

- Whether the reported spectrum is quoted at the top of the atmosphere/instrument
  (rigidity- or kinetic-energy-per-nucleon-binned) or corrected to the local
  interstellar spectrum, and if the latter, the modulation potential and model used.
- The geomagnetic cutoff applied (vertical Störmer as a first-order estimate, or a
  backtraced penumbra), the orbit/epoch it was computed for, and how off-vertical
  arrival directions and re-entrant/albedo contamination below cutoff were handled.
- The solar-activity epoch (dates, and neutron-monitor or modulation-potential proxy)
  the dataset spans, and whether Forbush-decrease or SEP-event periods were
  identified and excluded from the integration window.
- For a composition or isotope result: which PID subsystem(s) established charge and
  mass, and the momentum/rigidity range over which the required separation holds (see
  [particle identification](26-particle-identification.md)).
- For an antiparticle-excess interpretation: the astrophysical secondary-production
  baseline assumed, and what additional evidence (spectral cutoff, anisotropy,
  multi-channel consistency) distinguishes a nearby-source from a dark-matter
  interpretation.
