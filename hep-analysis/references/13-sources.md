# Primary Sources and Version Checks

This package is original operational guidance, not a complete summary of the manuals below. Apply formulas with their stated assumptions. Experiment-specific prescriptions must follow the formal sources supplied by the user. Links were consulted during preparation on 2026-09-05; rolling/development pages do not pin an API version.

| Topic | Primary source | Purpose |
|---|---|---|
| HEP statistics | [PDG Statistics review](https://pdg.lbl.gov/2025/reviews/rpp2025-rev-statistics.pdf) | Check interval, likelihood, and inference terminology |
| Profile likelihood and Asimov data | [Cowan et al., arXiv:1007.1727](https://arxiv.org/abs/1007.1727) | Check statistics and asymptotic assumptions |
| RooStats | [ROOT AsymptoticCalculator, version 6.26](https://root.cern.ch/doc/v626/classRooStats_1_1AsymptoticCalculator.html) | Historical API reference; use installed-version documentation for implementation |
| pyhf models | [Likelihood specification](https://scikit-hep.org/pyhf/likelihood.html) | Schema, modifiers, and auxiliary data; may be a development page |
| pyhf preservation | [pyhf paper](https://arxiv.org/abs/2211.15838) | Background on HistFactory serialization |
| Combine | [Official documentation](https://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/latest/) | Match methods/options to the installed release |
| uproot | [Official getting-started guide](https://uproot.readthedocs.io/en/latest/basic.html) | Chunked I/O and array APIs |
| Claude Code skills | [Official documentation](https://code.claude.com/docs/en/skills) | Skill directories and invocation |

Do not claim that an API is supported by the latest version without checking. Read local version/help output and lock files, then consult matching release documentation. Mark unverified points when network access is unavailable. Example luminosities, cross sections, and model parameters in documentation are not experimental inputs.
