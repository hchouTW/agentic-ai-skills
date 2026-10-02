# Cosmic-Ray Databases: CRDB (LPSC) and the ASI SSDC Cosmic Ray Database

## When to read this file

Read when the user asks to compare AMS with other experiments, to find which paper or dataset holds a published cosmic-ray measurement, to retrieve published data in bulk or from a script, to plot a compilation, or names CRDB or the SSDC cosmic-ray database. Do not read it to answer "what did AMS measure": that comes from the AMS papers through [source-index](source-index.md) (`source-policy`).

## Contents

1. [What the two databases are](#what-the-two-databases-are)
2. [Rules for using them with AMS data](#rules-for-using-them-with-ams-data)
3. [Cross-checking an AMS number](#cross-checking-an-ams-number)
4. [Pitfalls](#pitfalls)
5. [Querying and citing](#querying-and-citing)
6. [Failure modes](#failure-modes)
7. [Required source classes](#required-source-classes)
8. [Questions to ask the user](#questions-to-ask-the-user)

## What the two databases are

Both are Tier 6 secondary compilations of published data: navigation and cross-check only, never the source of an AMS number.

- **CRDB (LPSC Grenoble), https://lpsc.in2p3.fr/crdb/**: [Documented, S50 (website), C125-C128]. Cosmic-ray data and meta-data from 10^6 to 10^21 eV: leptons, nuclei (isotopes, elements, groups), antinuclei and dipole anisotropy, entered from publications with the ADS and DataThief. Access by a website, a REST interface and a pip-installable Python library; exports in USINE, GALPROP and csv formats. On 2026-10-02 the page stated version V4.2 (September 2026) with 143 experiments from 614 publications (C125; the counts change with each release). The four papers to cite are in S51 (C129): 2014, v4.0 (2020), v4.1 (2023) and the v4.2 preprint (2026); the v4.1 abstract says the database includes the hundreds of thousands of AMS-02 and PAMELA time-series points as entered by the CRDB team, whose agreement with the AMS papers was not checked.
- **ASI SSDC Cosmic Ray Database, https://tools.ssdc.asi.it/CosmicRays/sf_search.jsp**: [Documented, S53 abstract, C130; the page itself S52 is not verified]. A 2017 proceedings describes a database "under development" at the Italian Space Agency's Space Science Data Center, originally built to support the retrieval of PAMELA and AMS-02 results and expanding to other charged-cosmic-ray missions, with fluxes and ratios versus energy, rigidity, time and magnetic parameters. **The current page could not be read** (HTTP 429, then timeouts, for scripted requests on 2026-10-02, and a blank page in the maintainer's browser; the tools root redirects to a single-sign-on gateway, and the SSDC home page does list the tool at this address, S52), so its present content, coverage, query options, terms of use and AMS-02 holdings are [Unknown/needs input]; do not describe them, and do not script requests to it aggressively. Re-check (S52) when it answers.

Which AMS datasets these databases hold, and with what values, was **not queried** while writing this file: statements about their contents are [Unknown/needs input] until a query is run and the version and date recorded.

## Rules for using them with AMS data

1. **A database value is a transcription.** Label it `[Secondary: CRDB, version V, retrieved date]` and give the primary AMS paper (S-number from the index) to check it against. An AMS number you quote as a result needs its own claim in the index (invariant 9); if the index has none, answer symbolically or cite the paper without the number.
2. **Keep the native variable.** Each AMS paper states whether its flux is in rigidity or in energy (the ledger claims say which, for example the 2014 lepton fluxes are in energy, C115-C119, and the antiproton flux in rigidity, C120-C122). Query with the same axis and with conversions off (below). Convert only with `|Z|`, `A` and the rest mass stated, and only through exact conversions (isotopic and leptonic fluxes, leptonic ratios, p-bar/p, C127); approximate conversions of element fluxes use a proxy A and mass and can produce systematic errors larger than the data uncertainties (C127), which is the same trap as invariant 1.
3. **Do not merge sub-experiments.** One experiment appears as several datasets (time-averaged, per Bartels rotation, per day, different periods and analyses); the default query returns all datasets regardless of period overlap, and the page advises keeping the datasets over the longest periods (C126). Never average them or treat their union as one measurement; time series are excluded by default (`time_series=no`, C128).
4. **A systematic of 0 in CRDB means "not separately quoted"** for old data (C126). AMS papers quote systematics separately: take them from the paper's claims, not from CRDB.
5. **Record version and date** with anything extracted: counts and content change with each release (C125, C129).
6. **Agreement between experiments is not validation.** Cite a metric and a trigger (invariant 10) rather than "consistent with PAMELA".

## Cross-checking an AMS number

1. Fix the estimand and variable (invariant 1): species, rigidity or energy, time resolution.
2. Query on the native axis with `combo_level=0` and `energy_convert_level=0`, restricted to the AMS sub-experiments (`exp_dates=AMS`, optionally with a time interval); use the Python library or REST (C128).
3. Map each returned `SUBEXP_NAME` to its AMS paper through its name and data-taking range, then to the ledger source and claim (period and range must match the claim's scope).
4. Compare value, bins and uncertainty with the paper's statement; where they differ, the paper wins, and the difference (transcription from a plot, rebinning, a different data period) is worth reporting to the CRDB team.
5. Note the `PUBLI-DATAORIGIN` (table or plot) and the energy-scale column when present (C126).

## Pitfalls

- **Unit labels differ.** CRDB gives kinetic energy per nucleon in GeV (the per-nucleon meaning is in the symbol, since V4.1, C127); `scripts/ams_kinematics.py` labels it GeV/n. The numbers are the same convention; check a conversion with the script and state `Z`, `A` and the mass. The two formulae quoted in C127 agree with the script for one helium-4 point (checked 2026-10-02).
- **Combos and conversions are query-time products.** Combos multiply or divide native data of one sub-experiment within 5% (level 1) or 20% (level 2) in energy and add relative errors in quadrature (C127): a CRDB "B/C" may be a combination of two native fluxes and not a published ratio.
- **Names are not unique across versions.** Sub-experiment names encode period and technique (C126); two AMS datasets with similar names can be different analyses.
- **The two databases are different services** with different maintainers; the SSDC one also uses the abbreviation "CRDB" in its 2017 abstract (C130). Say which one.

## Querying and citing

[General method; the examples were not executed here] The page's own REST example is `curl -L 'http://lpsc.in2p3.fr/crdb/rest.php?num=B&den=C&energy_type=EKN' > db.dat`, and the parameters are in C128 (mandatory `num`, `den`, `energy_type`; a positron is `e%2B`). A native-axis AMS query would add `exp_dates=AMS&combo_level=0&energy_convert_level=0`. The Python library is installed with `pip install crdb` and can generate the list of citations for returned datasets (C128). Cite the CRDB papers (S51) and, for each dataset used, its primary paper; for the SSDC database cite S53 and say that the page itself was not read.

## Failure modes

- Quoting a CRDB or SSDC value as an AMS result, or as "verified" because it came from a database.
- Using approximate element conversions, or default combos, without saying so.
- Treating several AMS sub-experiments as one dataset, or forgetting that time series are excluded by default.
- Reading a CRDB "0 systematics" as an AMS statement.
- Describing the current SSDC page, its holdings or its terms of use (not read).
- Quoting CRDB counts or version without date, or hammering a service that returned 429.

## Required source classes

Tier 6 for the databases and their descriptions (S50-S53); Tier 1 AMS papers (and their ledger claims) for every AMS value; Tier 4 or textbook kinematics for conversions (`scripts/ams_kinematics.py`). Secondary-only evidence must be labeled secondary (`source-policy`).

## Questions to ask the user

Which database (CRDB at LPSC or the ASI SSDC one)? Which species, rigidity or energy range, and which AMS dataset (time-averaged, per rotation, daily)? Is the goal a comparison with other experiments, a data export, or a check of a transcribed value? Which database version and retrieval date should be recorded?
