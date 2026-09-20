# Source Index and Claim-to-Source Map

## When to read this file

Read before quoting any AMS number, date, or status, and when a user asks where a statement comes from. Schema and rules are in [source-policy](source-policy.md). Access/verification date for every row: **2026-09-20** unless stated.

## Contents

1. [Verification levels](#verification-levels)
2. [Source table](#source-table)
3. [Claim ledger](#claim-ledger)
4. [Items lacking primary or full-text verification](#items-lacking-primary-or-full-text-verification)
5. [Failure modes / Required source classes / Questions to ask](#failure-modes)

## Verification levels

`abstract+metadata`: title, authors, journal reference, DOI, date and abstract read from the INSPIRE-HEP record (inspirehep.net API) on the access date; the paper body was **not** opened (journal access unavailable). `full-text`: the open-access PDF of the main article was downloaded and read on the access date (**the Supplemental Material, which holds many selection details, was not opened**; the Phys. Rept. review was not obtainable). `page`: the public web page was fetched and read. `metadata-only`: record found, no abstract or body read. `not-verified`: named from memory or a prior repository file; must be checked before use. A claim's strength never exceeds its level. Numbers in rows not marked full-text come from abstracts; for full-text rows see claims C20-C32.

## Source table

Columns: ID | Title (short) | Author/institution | Year | DOI/URL | Tier | Level.

| ID | Title | Authors | Year | DOI / URL | Tier | Level |
|---|---|---|---|---|---|---|
| S01 | AMS on the ISS, Part II: Results from the first seven years, Phys. Rept. 894, 1 | AMS Collaboration (M. Aguilar et al.) | 2021 | 10.1016/j.physrep.2020.09.003 | 1 | abstract+metadata |
| S02 | First Result from AMS on the ISS: Precision Measurement of the Positron Fraction in Primary Cosmic Rays of 0.5-350 GeV, PRL 110, 141102 | AMS | 2013 | 10.1103/PhysRevLett.110.141102 | 1 | abstract+metadata |
| S03 | High Statistics Measurement of the Positron Fraction 0.5-500 GeV (PRL 113, 121101); Electron and Positron Fluxes (PRL 113, 121102); (e⁺+e⁻) Flux 0.5 GeV-1 TeV (PRL 113, 221102) | AMS | 2014 | 10.1103/PhysRevLett.113.121101 / .121102 / .221102 | 1 | metadata-only |
| S04 | Towards Understanding the Origin of Cosmic-Ray Positrons, PRL 122, 041102 | AMS | 2019 | 10.1103/PhysRevLett.122.041102 | 1 | full-text (main article only) |
| S05 | Towards Understanding the Origin of Cosmic-Ray Electrons, PRL 122, 101101 | AMS | 2019 | 10.1103/PhysRevLett.122.101101 | 1 | full-text (main article only) |
| S06 | Precision Measurement of the Proton Flux, 1 GV-1.8 TV, PRL 114, 171103 | AMS | 2015 | 10.1103/PhysRevLett.114.171103 | 1 | full-text (main article only) |
| S07 | Precision Measurement of the Helium Flux, 1.9 GV-3 TV, PRL 115, 211101 | AMS | 2015 | 10.1103/PhysRevLett.115.211101 | 1 | metadata-only |
| S08 | Antiproton Flux, Antiproton-to-Proton Flux Ratio, and Properties of Elementary Particle Fluxes, PRL 117, 091103 | AMS | 2016 | 10.1103/PhysRevLett.117.091103 | 1 | full-text (main article only) |
| S09 | Antiprotons and Elementary Particles over a Solar Cycle, PRL 134, 051002 | AMS | 2025 | 10.1103/PhysRevLett.134.051002 | 1 | abstract+metadata |
| S10 | Precision Measurement of the Boron to Carbon Flux Ratio, 1.9 GV-2.6 TV, PRL 117, 231102 | AMS | 2016 | 10.1103/PhysRevLett.117.231102 | 1 | full-text downloaded; only its data period was read |
| S11 | Identical Rigidity Dependence of He, C, and O at High Rigidities, PRL 119, 251101 | AMS | 2017 | 10.1103/PhysRevLett.119.251101 | 1 | metadata-only |
| S12 | Properties of Cosmic Helium Isotopes, PRL 123, 181102 | AMS | 2019 | 10.1103/PhysRevLett.123.181102 | 1 | full-text (main article only) |
| S13 | Properties of Cosmic Deuterons, PRL 132, 261001 | AMS | 2024 | 10.1103/PhysRevLett.132.261001 | 1 | full-text (main article only) |
| S14 | Properties of Cosmic Lithium Isotopes, PRL 134, 201001 | AMS | 2025 | 10.1103/PhysRevLett.134.201001 | 1 | full-text (main article only) |
| S15 | Properties of Heavy Cosmic Nuclei P, Cl, Ar, K, Ca, PRL 136, 241002 | AMS | 2026 | 10.1103/d2vf-fw3v | 1 | full-text (main article only) |
| S16 | Time-structure and periodicity PRLs: 121, 051101; 121, 051102 (2018); 127, 271102 (2021); 128, 231102 (2022); 130, 161001; 131, 151002 (2023) | AMS | 2018-2023 | 10.1103/PhysRevLett.121.051101 (and siblings) | 1 | metadata-only |
| S17 | AMS-02 detector web page (subsystem summaries) | AMS Collaboration website | page fetched 2026-09-20 | https://ams02.space/detector | 2 | page |
| S18 | Subsystem NIM A papers: Tracker performance (Haino, NIM A 699, 221, 2013; Rapin NIM A 718, 524, 2013), TRD (Kirn, NIM A 706, 43, 2013), RICH (Pereira NIM A 639, 37, 2011; Giovacchini NIM A 952, 161797, 2020; NIM A 1055, 168434, 2023; NIM A 1086, 171364, 2026) | AMS members | 2011-2026 | 10.1016/j.nima.2012.05.060 ; .05.010 ; 10.1016/j.nima.2010.09.036 ; 10.1016/j.nima.2019.01.024 ; 10.1016/j.nima.2023.168434 ; 10.1016/j.nima.2026.171364 | 2 (may be proceedings; check) | metadata-only |
| S19 | Tracker cross-strip nonlinearity (NIM A 869, 29, 2017); ECAL 3D shower parametrization (NIM A 869, 110, 2017) | AMS members | 2017 | not verified in INSPIRE this session | 2 | not-verified (carried from `hep-analysis` reference 38) |
| S20 | Additional AMS nuclei PRLs with year: N (121, 051103, 2018); Li, Be, B (120, 021101, 2018); Ne, Mg, Si (124, 211102, 2020); Fe (126, 041104, 2021); F (126, 081102, 2021); new group of nuclei incl. Na (127, 021101, 2021); S and primary C/N/O composition (130, 211002, 2023); solar modulation of nuclei (134, 051001, 2025) | AMS | 2018-2025 | e.g. 10.1103/PhysRevLett.134.051001 | 1 | metadata-only |
| S21 | Precision timeline check: AMS PRL list (30 PRLs 2013-2026) | INSPIRE query `collaboration:AMS`, PRL | 2026-09-20 | inspirehep.net API | 1 (metadata) | metadata-only |
| S22 | Search for antihelium in cosmic rays, Phys. Lett. B 461, 387 (AMS-01) | AMS Collaboration | 1999 | 10.1016/S0370-2693(99)00874-6 | 1 (historical, AMS-01) | metadata-only |
| S23 | AMS on the ISS, Part I: results from the test flight on the space shuttle, Phys. Rept. 366, 331 | AMS | 2002 | 10.1016/S0370-1573(02)00013-3 | 1 (historical) | metadata-only |
| S24 | "Combined Machine Learning Analysis for Antihelium Search with the AMS-02 Experiment" (INSPIRE lists year 2026; no journal reference; type, e.g. talk/thesis, not established) | F. Rossi | 2026 | INSPIRE record | 3 (unverified type) | metadata-only |
| S25 | "Search for antihelium nuclei in cosmic rays with the AMS-02 experiment on the ISS" (no journal reference; type not established) | R. Sonnabend | 2023 | INSPIRE record | 3 (unverified type) | metadata-only |
| S26 | Theory discussion of "tentative AMS antihelium events": Coogan and Profumo, PRD 96, 083020 (2017); Poulin and Salati, PRD 99, 023016 (2019) | third-party | 2017; 2019 | 10.1103/PhysRevD.96.083020 ; 10.1103/PhysRevD.99.023016 | 5/6 (third-party interpretation; use only to show the events were discussed as tentative) | metadata-only |
| S27 | Reviews mentioning conference antihelium statements: arXiv:2112.15255 "Antimatter in the Milky Way"; arXiv:2002.04163 | third-party | 2020-2021 | arxiv.org | 6 | not-opened (found via search result listing only; not evidence for counts) |
| S28 | Antideuteron: only AMS-tagged INSPIRE hit is a 2008 conference paper "Cosmic Rays Antideuteron Sensitivity for AMS-02 Experiment"; a 2013 JCAP paper discusses AMS-02/GAPS prospects (third party) | AMS members (2008); third party (2013) | 2008; 2013 | INSPIRE queries 2026-09-20 | 3 / 5-6 | metadata-only |
| S29 | AMS Collaboration publications page (dated list of papers) | AMS Collaboration website | page fetched 2026-09-20 | https://ams02.space/publications | 2 | page |
| S30 | Asymptotic formulae for likelihood-based tests of new physics, EPJC 71, 1554 | Cowan, Cranmer, Gross, Vitells | 2011 | 10.1140/epjc/s10052-011-1554-0 | 4 | metadata-only |
| S31 | A Unified Approach to the Classical Statistical Analysis of Small Signals, PRD 57, 3873 | Feldman, Cousins | 1998 | 10.1103/PhysRevD.57.3873 | 4 | metadata-only |
| S32 | Fitting using finite Monte Carlo samples, CPC 77, 219 | Barlow, Beeston | 1993 | 10.1016/0010-4655(93)90005-W | 4 | metadata-only |
| S33 | Incorporating nuisance parameters in likelihoods for multisource spectra (CERN-2011-006) | Conway | 2011 | 10.5170/CERN-2011-006.115 | 4 | metadata-only |
| S34 | A multidimensional unfolding method based on Bayes' theorem, NIM A 362, 487 | D'Agostini | 1995 | 10.1016/0168-9002(95)00274-X | 4 | metadata-only |
| S35 | TUnfold, JINST 7, T10003 | Schmitt | 2012 | 10.1088/1748-0221/7/10/T10003 | 4 | metadata-only |
| S36 | Confidence level computation for combining searches with small statistics, NIM A 434, 435 | Junk | 1999 | 10.1016/S0168-9002(99)00498-2 | 4 | metadata-only |
| S37 | Trial factors for the look elsewhere effect, EPJC 70, 525 | Gross, Vitells | 2010 | 10.1140/epjc/s10052-010-1470-8 | 4 | metadata-only |
| S38 | pyhf: pure-Python implementation of HistFactory, JOSS 6, 2823 | Heinrich, Feickert et al. | 2021 | 10.21105/joss.02823 | 4 | metadata-only |
| S39 | Review of Particle Physics, PRD 110, 030001 (kinematics, passage of particles through matter, cosmic rays) | Particle Data Group | 2024 | 10.1103/PhysRevD.110.030001 | 4 | metadata-only |
| S40 | Read, "Presentation of search results: the CLs technique," J. Phys. G 28, 2693 | A. L. Read | 2002 | not verified in INSPIRE this session | 4 | not-verified |

## Claim ledger

Only claims used by this skill. `scope` includes the context required by policy.

| claim_id | claim (paraphrased) | type | source | location | supported scope | limitation |
|---|---|---|---|---|---|---|
| C01 | AMS was installed on the ISS on 19 May 2011 after a 16-year construction/test period and precursor shuttle flight | detector_fact | S01 | abstract | Phys. Rept. review, 2021 | abstract only |
| C02 | S01 presents results on 120 billion charged cosmic-ray events, covering fluxes of positrons, electrons, antiprotons, protons, and nuclei | published_result | S01 | abstract | first seven years of data | abstract only |
| C03 | Positron fraction measured 0.5-350 GeV on 6.8×10⁶ positron and electron events | published_result | S02 | abstract | 2013 first result | superseded in range/statistics by S03 |
| C04 | Positron flux: 1.9 million positrons up to 1 TeV; an excess starting near 25 GeV, a dropoff above ~284 GeV, and a source-term cutoff (>4σ) | published_result | S04 | abstract | 2019; numeric values for specific energies to be read from S04 | abstract-level statement; the main article has been read (S04, S06, S08, S10 date only, S12-S15) and contains more detail, see C20-C32 |
| C05 | Proton flux 1 GV-1.8 TV, 300 million events; spectral index hardens with rigidity | published_result | S06 | abstract | data period not stated in the abstract (read it from the full text) | abstract-level statement; the main article has been read (S04, S06, S08, S10 date only, S12-S15) and contains more detail, see C20-C32 |
| C06 | Antiproton flux and `p̄/p` for 1-450 GV based on 3.49×10⁵ antiprotons and 2.42×10⁹ protons; `p̄`, `p`, `e⁺` fluxes have nearly identical rigidity dependence about 60-500 GV | published_result | S08 | abstract | 2016 | abstract-level statement; the main article has been read (S04, S06, S08, S10 date only, S12-S15) and contains more detail, see C20-C32 |
| C07 | Antiproton results over an 11-year solar cycle: 1.1×10⁶ events, 1.00-41.9 GV; smaller time variation than `p`, `e⁻`, `e⁺` | published_result | S09 | abstract | 2025 | abstract only |
| C08 | B/C measured 1.9 GV-2.6 TV on 2.3 million B and 8.3 million C; above 65 GV power law index -0.333±0.014(fit)±0.005(syst), which the abstract reports as in good agreement with the value -1/3 the Kolmogorov turbulence theory predicts asymptotically (model interpretation stays a separate step) | published_result | S10 | abstract | first 5 years | abstract-level statement; the main article has been read (S04, S06, S08, S10 date only, S12-S15) and contains more detail, see C20-C32 |
| C09 | `³He`, `⁴He` fluxes: 100 million `⁴He` (2.1-21 GV) and 18 million `³He` (1.9-15 GV), May 2011-Nov 2017; above 4 GV `³He/⁴He` time-independent, power-law index -0.294±0.004 | published_result | S12 | abstract | 2019 | abstract-level statement; the main article has been read (S04, S06, S08, S10 date only, S12-S15) and contains more detail, see C20-C32 |
| C10 | Deuteron flux: 21×10⁶ D nuclei, 1.9-21 GV, May 2011-April 2021, time variation nearly identical to p, ³He, ⁴He | published_result | S13 | abstract | 2024 | abstract-level statement; the main article has been read (S04, S06, S08, S10 date only, S12-S15) and contains more detail, see C20-C32 |
| C11 | Li isotopes ⁶Li, ⁷Li measured 1.9-25 GV (9.7×10⁵ ⁶Li, 1.04×10⁶ ⁷Li) | published_result | S14 | abstract | 2025 (period truncated in reading) | abstract-level statement; the main article has been read (S04, S06, S08, S10 date only, S12-S15) and contains more detail, see C20-C32 |
| C12 | About one million P, Cl, Ar, K, Ca events over 13.5 years; fluxes described as sums of primary and secondary components | published_result | S15 | abstract | 2026 | abstract-level statement; the main article has been read (S04, S06, S08, S10 date only, S12-S15) and contains more detail, see C20-C32 |
| C13 | Subsystem roles: Tracker in magnet (momentum, charge sign), TOF (trigger, direction, velocity, dE/dx), TRD (e±/p separation), ACC (side-entry veto), RICH with NaF and aerogel radiators (velocity, charge), ECAL (3D shower imaging, energy, e/p separation) | detector_fact | S17 | page | AMS website summary | performance numbers on the page have no selection context; not reproduced |
| C14 | No peer-reviewed AMS antihelium paper was found in INSPIRE (only the 1999 AMS-01 limit S22 among AMS-authored results; other hits are theses/talks and third-party interpretations) | published_result (absence claim) | S22, S24-S26 | INSPIRE queries 2026-09-20 | search-limited: not a proof of absence | INSPIRE coverage of talks incomplete; re-check for "latest" |
| C19 | No AMS antideuteron measurement or search paper was found in INSPIRE; only a 2008 sensitivity conference paper and third-party prospects exist | published_result (absence claim) | S28 | INSPIRE queries 2026-09-20 | search-limited; not proof of absence | re-check for "latest" |
| C20 | Antiproton analysis data: 19 May 2011 to 26 May 2015 (over 65 billion events in the first 48 months); events need a TRD track and inner-tracker track, TOF β > 0.3 downward-going; χ²/d.o.f. < 10 in both projections; TRD, TOF and inner-tracker dE/dx consistent with \|Z\| = 1; rigidity > 1.2 × maximum geomagnetic cutoff (backtracing, IGRF); 57 rigidity bins; requirement on outer tracker layers L1/L9 relaxed with rigidity (neither below 38.9 GV; either 38.9-147 GV; only L9 147-175 GV; both above 175 GV) | analysis_method | S08 | Event selection section | antiproton/proton flux, 1-450 GV | Supplemental cuts not read |
| C21 | Performance quoted in S08 (also in S04, S05, S06 for the nine-layer tracker): maximum detectable rigidity 2 TV for \|Z\| = 1 (3 m lever arm L1-L9); tracker charge resolution ΔZ = 0.05 for \|Z\| = 1; TOF velocity resolution Δβ/β² = 4%; RICH Δβ/β = 0.1% for \|Z\| = 1; ACC efficiency 0.99999 for side-entering rejection | performance_number | S08, S04, S05, S06 | Detector section of each | \|Z\| = 1, the stated analysis and configuration only; not universal | definitions of "efficiency" and per-range validity are in cited detector papers |
| C22 | Antiproton extraction: template fit to the negative-rigidity sample using TRD estimator Λ_TRD (per-layer log-likelihood ratio, e vs p hypothesis) and a BDT charge-confusion estimator Λ_CC (track χ², rigidities from different layer combinations, hits near the track, TOF and tracker charges); three overlapping rigidity regions with different templates (low 1.00-4.02 GV, intermediate 2.97-18.0 GV, high 16.6-450 GV); antiproton signal template taken from the high-statistics proton data (checked against MC and against p̄/p data, 2.97-18.0 GV); electron/π⁻ and charge-confusion-proton templates from data and MC; charge-confusion MC checked with 400 GV proton test-beam data | analysis_method | S08 | Event selection and data samples | 1-450 GV | fit-variable details per region in the paper |
| C23 | Antiproton flux: iterative unfolding, acceptance folded with MC, iteration stopped when fluxes of two consecutive steps agree within 0.1%; four systematic sources added quadratically: (1) one source covering the geomagnetic cutoff-factor definition (varied 1.2-1.4; about 1% at 1 GV, negligible above 2 GV), the event selection (analysis repeated about 1000 times with different cut sets; 4% at 1 GV, 0.5% at 10 GV, 6% at 450 GV) and the template shapes (12% at 450 GV, < 1% below 30 GV); the remaining three sources concern the folded acceptances (interaction cross sections and migration matrices), the normalization of the effective acceptance, and the absolute rigidity scale (see the paper for sizes) | analysis_method / performance_number | S08 | Analysis section | p̄ flux, 1-450 GV | grouping of the four sources should be re-read in the paper before quoting a breakdown |
| C24 | Positron flux data: 19 May 2011 to 12 Nov 2017 (1.07 × 10¹¹ events in about 6.5 years); E > 1.2 × maximum Størmer cutoff (backtracing gives the same result); χ²/d.o.f. < 20; \|Z\| = 1 in TOF and tracker; energy-dependent cut on ECAL estimator Λ_ECAL; template fit in the 2D (Λ_TRD, Λ_CC^e) plane with three templates: positrons and protons with correct charge sign, and charge-confusion electrons; positron template from electron data below 100 GeV and electron MC above 100 GeV; charge-confusion template from MC verified with e± test-beam data (10-290 GeV) and AMS e⁻ data (to 1 TeV); proton template from proton data | analysis_method | S04 | Event selection | e⁺, 0.5 GeV-1 TeV | |
| C25 | Positron flux estimator Φ = N/(A(1+δ)TΔE) in energy at the top of AMS; δ (data/MC efficiency corrections from the high-statistics electron sample) about -5% at 1 GeV, -2.4% at 10 GeV, -2.8% above 50 GeV; bin widths at least twice the energy resolution; small bin migration corrected by unfolding; energy-scale uncertainty (4% at 0.5 GeV, 2% at 2-300 GeV, 2.5% at 1 TeV) treated as an uncertainty of the bin boundaries; total systematic is the quadratic sum of four sources (templates, charge confusion, efficiency corrections, migration); independent analyses by several groups agree | analysis_method / performance_number | S04 | Data analysis | e⁺ flux | |
| C26 | Electron flux: negative-rigidity sample; energy-dependent Λ_ECAL cut leaves antiproton background < 10⁻³ of the sample; template fit with an electron template and two charge-confusion templates (positrons, protons) in (Λ_TRD, Λ_CC^e) | analysis_method | S05 | Detector/analysis | e⁻, 0.5 GeV-1.4 TeV (28.1 × 10⁶ electrons) | |
| C27 | Deuteron analysis: downward-going, track through tracker layer L1, charge Z = 1 required on L1, upper TOF, inner tracker, lower TOF; 26 rigidity bins 1.9-21 GV; an unfolding procedure separates D from the Z = 1 sample using rigidity and inverse-velocity (1/β) resolution functions of the TOF and RICH (from MC, checked at β ≈ 1 with data, corrections < 5%); dominant background He → D fragmentation above L1 computed from data using ⁴He + (C, Al) → T + X (≤ 4%); acceptance corrected for data/MC differences (< 10% total); cutoff factor varied 1.0-1.4 (< 0.1%); four independent analyses agree; 33 time periods of four Bartels rotations (108 days) May 2011-April 2021 | analysis_method | S13 | Selection, Analysis | D flux, 1.9-21 GV | Supplemental Material not read |
| C28 | Helium isotopes: 26 rigidity bins 1.92-21.1 GV; velocity bins for TOF, RICH-NaF and RICH-Agl; rates unfolded with resolution functions; TOF Δ(1/β) core width 0.02; RICH-Agl core width 7 × 10⁻⁴ at β = 1, decreasing to 6.3 × 10⁻⁴ at β ≈ 0.953; resolution functions from MC and validated at β = 1 with data; rigidity-resolution systematic from varying the width by 10% | analysis_method / performance_number | S12 | Selection, Analysis | ³He/⁴He, May 2011-Nov 2017 | Gaussian-core widths only; tails not quoted in main text |
| C29 | Lithium isotopes: Z = 3 on L1, upper TOF, inner tracker, lower TOF; charge confusion from non-interacting nuclei < 0.01%; residual background from heavier nuclei interacting above tracker L2; survival probability of Li in AMS material measured with AMS cosmic-ray data; 42 time periods of four Bartels rotations, May 2011-Oct 2023 | analysis_method | S14 | Selection, Results | ⁶Li, ⁷Li, 1.9-25 GV | |
| C30 | Heavy nuclei P-Ca: 19 May 2011 to 26 Nov 2024 (2.4 × 10¹¹ events); bin-to-bin migration corrected by unfolding, with corrections to the P flux of about +25% at 3 GV, +8% at 10 GV, -2% at 100 GV, -10% at 300 GV, -21% at 1.2 TV; charge confusion from non-interacting nuclei < 2% (P) and < 1% (Cl, Ar, K, Ca); background from interactions above tracker L2 (S, Cl, Ar, K, Ca, Sc, Ti, V, Cr, Fe); the part arising from interactions in the material between L1 and L2 (TRD and upper TOF) is evaluated by fitting the tracker-L1 charge distribution with Si-Ti charge templates (the remaining material is treated as in the paper) | analysis_method / performance_number | S15 | Event selection | P flux | |
| C31 | Proton flux: first 30 months (19 May 2011 to 26 Nov 2013); 72 rigidity bins 1 GV-1.8 TV; live time > 50%, z axis within 40° of zenith, outside the South Atlantic Anomaly; R > 1.2 × maximum cutoff; iterative unfolding correcting bin-to-bin migration | analysis_method | S06 | Analysis | p flux | |
| C32 | B/C data period: 19 May 2011 to 26 May 2016 | published_result | S10 | Introduction | B/C | |
| C33 | AMS combines independent systematic sources in quadrature for fluxes, and accounts for correlations of systematic errors when forming isotope ratios (D/⁴He, ³He/⁴He, ⁷Li/⁶Li) | analysis_method | S12, S13, S14 | Results | isotope ratios | |
| C34 | The Collaboration publications page lists, as its five most recent papers on 2026-09-20: PRL 136, 241002 (17 June 2026, P, Cl, Ar, K, Ca); PRL 134, 201001 (20 May 2025, Li isotopes); PRL 134, 051001 and 051002 (3 Feb 2025, solar modulation of nuclei; antiprotons); PRL 132, 261001 (25 June 2024, deuterons) | published_result | S29 | list page | as of 2026-09-20 | website list, not a journal record; consistent with the INSPIRE list S21 |
| C35 | Positron source-term energy cutoff significance: the abstract states "more than 4σ" and the article body gives 4.07σ (the point where 1/E_s reaches 0), so a claim of 5σ is not supported | published_result | S04 | abstract and final fit discussion | positron flux fit, 2019 | model-dependent fit (source term plus collision term) |
| C15 | Third-party literature (S26) discusses "tentative" AMS antihelium events, consistent with the events not being an established published result | analysis_method (interpretation of context) | S26 | titles | 2017; 2019 | title-level only |
| C16 | AMS time-structure results published as matched pairs across species/charge sign | analysis_method | S16 | titles | 2018-2023 | titles only |
| C17 | General statistical methods (asymptotics, Feldman-Cousins, CLs, Barlow-Beeston, unfolding, trial factors) | general_method | S30-S37 | - | general | not AMS practice |
| C18 | Kinematic relations and Cherenkov/Bethe-Bloch/Highland formulae | general_method | S39 | - | general | not opened this session; standard textbook relations |

## Items lacking primary or full-text verification

- **Full text read (main article only): S04, S05, S06, S08, S10 (data period only), S12, S13, S14, S15** (open-access PDFs, 2026-09-20). Their Supplemental Material was not opened, so per-cut definitions and many tables are still missing. **Not obtained:** the Phys. Rept. review (S01; publisher page blocked and a repository link returned HTML), S02, and every row marked metadata-only. Abstract-only numbers elsewhere in the ledger remain abstract-level.
- **Antihelium:** no primary paper found; S24-S27 are unverified in type/content; the skill supplies no counts. Re-check when the user asks.
- **S19, S40:** not verified this session.
- **S03, S05, S07, S11, S16, S20:** metadata-only; treat titles as navigation.
- **Hardware history** (cooling-system repair EVAs 2019-2020, the Tracker Layer-0 upgrade): described on the AMS website and in `hep-analysis` reference 38; not re-verified here; do not cite dates or scope without checking the AMS site or NASA sources.
- **PDG 2024:** metadata only; general formulas are standard but must be cited to a specific PDG section when quoted.

## Failure modes

- Treating an abstract-level number as a full-text-verified performance value.
- Quoting a website headline figure (rejection, efficiency, resolution) without selection context.
- Letting a Tier 5/6 item support an AMS-specific claim.

## Required source classes

Tier 1 and 2 for AMS-specific entries; Tier 4 for general methods.

## Questions to ask the user

Which result or paper (DOI or arXiv)? Do you have access to the full text so it can be inspected and the ledger upgraded to `full-text`? Is a re-verification for "latest" needed now?
