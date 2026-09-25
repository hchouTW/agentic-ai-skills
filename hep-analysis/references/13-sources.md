# Primary Sources and Version Checks

This package is original operational guidance, not a complete summary of the manuals below. Apply formulas with their stated assumptions. Experiment-specific prescriptions must follow the formal sources supplied by the user. Links were consulted during preparation on 2026-09-05, with the astroparticle-physics entries added 2026-09-09; rolling/development pages do not pin an API version.

| Topic | Primary source | Purpose |
|---|---|---|
| HEP statistics | [PDG Statistics review](https://pdg.lbl.gov/2026/reviews/rpp2026-rev-statistics.pdf) | Check interval, likelihood, and inference terminology |
| Profile likelihood and Asimov data | [Cowan et al., arXiv:1007.1727](https://arxiv.org/abs/1007.1727) | Check statistics and asymptotic assumptions |
| RooStats | [ROOT AsymptoticCalculator, version 6.26](https://root.cern.ch/doc/v626/classRooStats_1_1AsymptoticCalculator.html) | Historical API reference; use installed-version documentation for implementation |
| pyhf models | [Likelihood specification](https://scikit-hep.org/pyhf/likelihood.html) | Schema, modifiers, and auxiliary data; may be a development page |
| pyhf preservation | [pyhf paper](https://arxiv.org/abs/2211.15838) | Background on HistFactory serialization |
| Combine | [Official documentation](https://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/latest/) | Match methods/options to the installed release |
| uproot | [Official getting-started guide](https://uproot.readthedocs.io/en/latest/basic.html) | Chunked I/O and array APIs |
| Passage of particles through matter | [PDG review](https://pdg.lbl.gov/2026/reviews/rpp2026-rev-passage-particles-matter.pdf) | Bethe-Bloch, Highland multiple scattering, radiation length, Cherenkov and transition radiation |
| Particle detectors at accelerators | [PDG review](https://pdg.lbl.gov/2026/reviews/rpp2026-rev-particle-detectors-accel.pdf) | Detector technologies, resolution parameterizations, calorimeter terms |
| Particle detectors for non-accelerator physics | [PDG review](https://pdg.lbl.gov/2026/reviews/rpp2026-rev-particle-detectors-non-accel.pdf) | Spectrometer, TOF, and Cherenkov practice outside collider geometries |
| Particle masses and properties | [PDG Particle Listings](https://pdg.lbl.gov/) | Masses used by `pid_separation_power.py` and `cherenkov_angle.py` |
| Geant4 physics | [Physics Reference Manual](https://geant4.web.cern.ch/support/user_documentation) | Physics lists, production cuts, hadronic model validity ranges |
| Cosmic rays and particle physics (textbook) | Gaisser, Engel & Resconi, *Cosmic Rays and Particle Physics*, 2nd ed. (Cambridge University Press, 2016) | Acceleration, propagation, air-shower, and detection-technique background for references 32-39 |
| Cosmic-ray astrophysics (textbook) | Longair, *High Energy Astrophysics*, 3rd ed. (Cambridge University Press, 2011) | Acceleration mechanisms, multi-messenger astrophysics context |
| ON/OFF significance | Li & Ma, *Astrophysical Journal* 272, 317 (1983) | Derivation of the likelihood-ratio significance in `scripts/li_ma_significance.py` |
| Cosmic-ray and astroparticle physics reviews | [PDG](https://pdg.lbl.gov/) | Cosmic-ray, astrophysical-constants, and related review chapters; check the current edition's table of contents for the exact chapter |
| Pierre Auger Observatory | [Official site](https://www.auger.org/) | Hybrid surface-array/fluorescence UHECR methodology and publications |
| IceCube Neutrino Observatory | [Official site](https://icecube.wisc.edu/) | In-ice Cherenkov neutrino-telescope methodology and publications |
| CTA Observatory | [Official site](https://www.cta-observatory.org/) | Imaging atmospheric Cherenkov technique and next-generation IACT array design |
| Alpha Magnetic Spectrometer (AMS-02) | NASA and AMS collaboration mission/science pages (exact URL not pinned here - verify current link before citing); `ams02.space/detector`, `ams02.space/advances-data-analysis`, and `ams02.space/publications` checked directly 2026-09-10; Aguilar et al., "The Alpha Magnetic Spectrometer (AMS) on the International Space Station: Part II - Results from the First Seven Years," Phys. Rept. 894 (2021) 1-116 is the best single primary-source cross-check for instrument-parameter claims | Official mission overview for the AMS-02 case study in reference 40; check any specific instrument parameter or published result against an AMS collaboration publication (the Phys. Rept. 894 review first) before quoting it. The 2019-2020 EVA cooling-system repair is independently corroborated by NASA/Scientific American/phys.org/NASASpaceflight.com reporting; subsystem numeric specs (RICH radiator configuration, ACC efficiency, tracker/ECAL resolution) are website-sourced only as of the 2026-09-10 check and still need checking against Phys. Rept. 894 or a later instrument publication before being quoted as measured fact. This is a live-changing fact set (further servicing/upgrades, and further publications, are plausible) - re-verify before reuse past this date. |
| Detector textbooks | Leo, *Techniques for Nuclear and Particle Physics Experiments*, 2nd ed. (Springer, 1994), [DOI 10.1007/978-3-642-57920-2](https://doi.org/10.1007/978-3-642-57920-2); Grupen & Shwartz, *Particle Detectors*, 2nd ed. (Cambridge University Press, 2008), [DOI 10.1017/CBO9780511534966](https://doi.org/10.1017/CBO9780511534966); Wigmans, *Calorimetry*, 2nd ed. (Oxford University Press, 2017), [DOI 10.1093/oso/9780198786351.001.0001](https://doi.org/10.1093/oso/9780198786351.001.0001); Blum, Riegler & Rolandi, *Particle Detection with Drift Chambers*, 2nd ed. (Springer, 2008), [DOI 10.1007/978-3-540-76684-1](https://doi.org/10.1007/978-3-540-76684-1) | Signal formation, drift/diffusion, calorimetry, gas detectors for references 39-45 |
| Track fitting | Fruhwirth, "Application of Kalman filtering to track and vertex fitting", Nucl. Instrum. Methods A262 (1987) 444, [DOI 10.1016/0168-9002(87)90887-4](https://doi.org/10.1016/0168-9002(87)90887-4) | Kalman track/vertex fit behind references 22, 41, 43 |
| Multiple scattering | Highland, Nucl. Instrum. Methods 129 (1975) 497, [DOI 10.1016/0029-554X(75)90743-0](https://doi.org/10.1016/0029-554X(75)90743-0); Lynch & Dahl, Nucl. Instrum. Methods B58 (1991) 6, [DOI 10.1016/0168-583X(91)95671-Y](https://doi.org/10.1016/0168-583X(91)95671-Y) | Highland approximation used in reference 40 (PDG review above gives the current form) |
| Geomagnetic cutoff | Smart & Shea, "A review of geomagnetic cutoff rigidities for earth-orbiting spacecraft", Adv. Space Res. 36 (2005) 2012 | Stormer form and the vertical `14.9 cos^4(lambda)/r^2` GV cutoff in `scripts/geomagnetic_cutoff.py` (added 2026-09-24) |
| Solar modulation | Gleeson & Axford, Astrophys. J. 154 (1968) 1011 | Force-field approximation in `scripts/solar_modulation_force_field.py`; shift `|Z| phi` in total kinetic energy, `(|Z|/A) phi` per nucleon |
| Solar cycle 24 and Voyager heliopause dates | [SILSO: 2014, maximum year for cycle 24](https://www.sidc.be/SILSO/news004); [NASA Voyager interstellar mission](https://science.nasa.gov/mission/voyager/interstellar-mission/); Stone et al., Science 341 (2013) 150 (Voyager 1); [Voyager 2 enters interstellar space, arXiv:1912.02476](https://arxiv.org/abs/1912.02476) | Cycle 24 minimum Dec 2008, maximum Apr 2014 with a Nov 2011 first peak; Voyager 1 heliopause 25 Aug 2012, Voyager 2 5 Nov 2018 (reference 35; checked by web search 2026-09-25) |
| Exact binomial/Poisson intervals | Clopper & Pearson, Biometrika 26 (1934) 404; Garwood, Biometrika 28 (1936) 437 | `tag_and_probe_efficiency.py` and `cosmic_ray_flux.py`; cross-checked against `scipy.stats` beta/chi2 quantiles in `tests/test_reference_values.py` |
| Longitudinal shower profile | Gaisser & Hillas, Proc. 15th ICRC (Plovdiv) 8 (1977) 353 | Functional form in `scripts/xmax_gaisser_hillas.py` |
| Detector-performance definitions | Experiment technical design reports and official performance papers for the apparatus in question (cite by name, configuration, and phase space; none is pinned here) | Any numeric performance claim in references 39-49 must come from one of these, not from this package |

| Claude Code skills | [Official documentation](https://code.claude.com/docs/en/skills) | Skill directories and invocation |

Do not claim that an API is supported by the latest version without checking. Read local version/help output and lock files, then consult matching release documentation. Mark unverified points when network access is unavailable. Example luminosities, cross sections, and model parameters in documentation are not experimental inputs. The detector geometries, material budgets, and resolution values in this package's assets and examples are synthetic and illustrative; they are not measurements of any real apparatus.

## Latest-results policy

Measured values move: spectral-break positions, flux normalizations, limits, detector
performance and mission status are superseded by later publications. Rules:

- Any "latest", "current", "best", or "world-leading" statement, and any experimental
  number quoted as a result, must name its source and the date it was checked
  (`checked YYYY-MM-DD`). Without both, present it as an illustrative order of magnitude.
- Before quoting such a number to a user, re-check it if the check date is older than
  12 months, or state that it was not re-checked.
- Standard physics constants and textbook formulas (PDG constants, Bethe-Bloch, Highland,
  Stormer, force field) are stable and exempt, but still cite the edition they came from.
- Items to re-verify on each pass. Live check done 2026-09-25 (the 2026-09-24 pass was
  from knowledge only):
  - PDG edition: the 2026 edition is current; the links above now point to it (all four
    PDFs resolve). Checked 2026-09-25.
  - Knee/ankle/GZK energies and indices (reference 30): checked 2026-09-25 against the
    [PDG 2026 cosmic-ray review](https://pdg.lbl.gov/2026/reviews/rpp2026-rev-cosmic-rays.pdf)
    (revised March 2026). Reference 30 corrected to match: knee at a few PeV, `gamma`
    ~2.7 -> ~3; second knee ~100 PeV, -> ~3.3; ankle ~5 EeV, -> ~2.5; instep from ~10 EeV;
    suppression from ~50 EeV. Note: PDG 2026 (section 30.6) words the instep as "a further
    flattening beginning at 10 EeV", but the Auger fit it cites (PRL 125 (2020) 121106)
    has `gamma` rising from ~2.5 to ~3.0 near 13 EeV, i.e. a steepening. Reference 30
    follows Auger.
  - IACT energy-scale systematic (reference 33): checked 2026-09-25. Current IACTs report
    ~10-15% (H.E.S.S., MAGIC; MAGIC performance paper arXiv:1508.04575) up to ~20%
    (VERITAS); CTA calibration target ~15% (arXiv:1508.07225). Reference 33 changed from
    "~15-20%" to "~10-20%".
  - AMS-02 mission status (reference 38): checked 2026-09-25 on
    [ams02.space/tracker-layer-0-upgrade](https://ams02.space/tracker-layer-0-upgrade).
    The Layer-0 silicon tracker upgrade (a new layer on top of the detector, quoted
    acceptance gain ~300%) passed qualification tests in June 2025 and is **not yet
    installed**. Secondary sources (a conference contribution and CERN news, seen only
    as search snippets and not opened) put launch at the end of 2026 and completion via
    spacewalks by about May 2027. Re-check after that. Instrument parameters: still only
    checked against the website on 2026-09-10, not against Phys. Rept. 894.

