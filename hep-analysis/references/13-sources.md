# Primary Sources and Version Checks

This package is original operational guidance, not a complete summary of the manuals below. Apply formulas with their stated assumptions. Experiment-specific prescriptions must follow the formal sources supplied by the user. Links were consulted during preparation on 2026-09-05, with the astroparticle-physics entries added 2026-09-09; rolling/development pages do not pin an API version.

| Topic | Primary source | Purpose |
|---|---|---|
| HEP statistics | [PDG Statistics review](https://pdg.lbl.gov/2025/reviews/rpp2025-rev-statistics.pdf) | Check interval, likelihood, and inference terminology |
| Profile likelihood and Asimov data | [Cowan et al., arXiv:1007.1727](https://arxiv.org/abs/1007.1727) | Check statistics and asymptotic assumptions |
| RooStats | [ROOT AsymptoticCalculator, version 6.26](https://root.cern.ch/doc/v626/classRooStats_1_1AsymptoticCalculator.html) | Historical API reference; use installed-version documentation for implementation |
| pyhf models | [Likelihood specification](https://scikit-hep.org/pyhf/likelihood.html) | Schema, modifiers, and auxiliary data; may be a development page |
| pyhf preservation | [pyhf paper](https://arxiv.org/abs/2211.15838) | Background on HistFactory serialization |
| Combine | [Official documentation](https://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/latest/) | Match methods/options to the installed release |
| uproot | [Official getting-started guide](https://uproot.readthedocs.io/en/latest/basic.html) | Chunked I/O and array APIs |
| Passage of particles through matter | [PDG review](https://pdg.lbl.gov/2025/reviews/rpp2025-rev-passage-particles-matter.pdf) | Bethe-Bloch, Highland multiple scattering, radiation length, Cherenkov and transition radiation |
| Particle detectors at accelerators | [PDG review](https://pdg.lbl.gov/2025/reviews/rpp2025-rev-particle-detectors-accel.pdf) | Detector technologies, resolution parameterizations, calorimeter terms |
| Particle detectors for non-accelerator physics | [PDG review](https://pdg.lbl.gov/2025/reviews/rpp2025-rev-particle-detectors-non-accel.pdf) | Spectrometer, TOF, and Cherenkov practice outside collider geometries |
| Particle masses and properties | [PDG Particle Listings](https://pdg.lbl.gov/) | Masses used by `pid_separation_power.py` and `cherenkov_angle.py` |
| Geant4 physics | [Physics Reference Manual](https://geant4.web.cern.ch/support/user_documentation) | Physics lists, production cuts, hadronic model validity ranges |
| Cosmic rays and particle physics (textbook) | Gaisser, Engel & Resconi, *Cosmic Rays and Particle Physics*, 2nd ed. (Cambridge University Press, 2016) | Acceleration, propagation, air-shower, and detection-technique background for references 32-39 |
| Cosmic-ray astrophysics (textbook) | Longair, *High Energy Astrophysics*, 3rd ed. (Cambridge University Press, 2011) | Acceleration mechanisms, multi-messenger astrophysics context |
| ON/OFF significance | Li & Ma, *Astrophysical Journal* 272, 317 (1983) | Derivation of the likelihood-ratio significance in `scripts/li_ma_significance.py` |
| Cosmic-ray and astroparticle physics reviews | [PDG](https://pdg.lbl.gov/) | Cosmic-ray, astrophysical-constants, and related review chapters; check the current edition's table of contents for the exact chapter |
| Pierre Auger Observatory | [Official site](https://www.auger.org/) | Hybrid surface-array/fluorescence UHECR methodology and publications |
| IceCube Neutrino Observatory | [Official site](https://icecube.wisc.edu/) | In-ice Cherenkov neutrino-telescope methodology and publications |
| CTA Observatory | [Official site](https://www.cta-observatory.org/) | Imaging atmospheric Cherenkov technique and next-generation IACT array design |
| Claude Code skills | [Official documentation](https://code.claude.com/docs/en/skills) | Skill directories and invocation |

Do not claim that an API is supported by the latest version without checking. Read local version/help output and lock files, then consult matching release documentation. Mark unverified points when network access is unavailable. Example luminosities, cross sections, and model parameters in documentation are not experimental inputs. The detector geometries, material budgets, and resolution values in this package's assets and examples are synthetic and illustrative; they are not measurements of any real apparatus.
