# Physicist review packet: the ams-analysis evidence ledger

Snapshot generated 2026-10-02 from `data/sources.json` (49 sources) and `data/claims.json` (106 claims) at the commit that adds this file. It is a reading aid, not part of the skill: it is not wired to the ledger and goes stale when the JSON changes (regenerate rather than edit). Nothing in the ledger has been changed for this packet.

## What is being asked, and how long it takes

The skill answers AMS-02 questions by quoting numbers only from a claim ledger. Every claim has a scope (species, range, period, analysis), a `verification_strength` (how much of the source the author actually read), a `support_kind` and a flag `numeric_quotation_allowed`. These fields were set by the skill author (an LLM-assisted workflow reading public papers) and have **not been checked by a domain physicist**. Please confirm or correct them.

- **30 minutes:** answer Part 1 (the 8 judgement calls). The claim lists under each call say which rows are affected.
- **2 hours:** also skim Part 2 (all claims) and mark the verdict column (OK / change / unsure) wherever the one-line claim looks wrong, too broad, or attributed to the wrong paper.
- Part 3 lists sources with tier and verification level.

What a correction looks like: edit the field in `data/claims.json` or `data/sources.json`, run `python3 scripts/validate_evidence_ledger.py`, then `python3 scripts/render_source_index.py --write`. A claim's strength may never be raised without reading the source at that level.

Scope: this is about **ledger bookkeeping and scope of claims**, not about whether the physics reasoning in the reference files is right (that is a separate, larger review).

Definitions used below (from `references/source-policy.md`). *Tier*: 1 = peer-reviewed AMS Collaboration papers and supplements; 2 = official AMS detector papers, website, technical documents, formal data releases; 3 = public conference material or theses by AMS authors (preliminary unless a paper says otherwise); 4 = PDG, textbooks, peer-reviewed methodology papers (general principles only); 5 = other experiments (methodological comparison only, never AMS practice); 6 = reviews, press, slides, secondary articles, encyclopedias (navigation only). *Verification level*: `full-text` = the main article text was read (supplements only where a record says so), `abstract+metadata`, `metadata-only` (titles/records only), `page` (a web page), `not-opened`, `not-verified`.

## Part 1. Judgement calls to confirm

### 1. Numbers quoted from an abstract or a web page (22 claims)
`numeric_quotation_allowed` is true for claims whose strength is only `abstract+metadata` or `page`: C01, C02, C03, C04, C05, C06, C07, C08, C09, C10, C11, C12, C34, C36, C37, C38, C39, C40, C41, C42, C101, C102.
**Question:** is quoting a headline number (range, sample size, significance) from an abstract acceptable if the claim text carries its scope, or should the skill say "abstract-level" and withhold such numbers? Anything that you would not want quoted without the paper's selection and systematics context: flag it. (C34, C101, C102 are website/news pages.)

### 2. Claim strength below the source's level (17 claims)
For these, the paper behind the claim is `full-text` in the ledger but the claim is held at a lower strength: C01, C02, C04, C05, C06, C08, C09, C10, C11, C12, C36, C37, C38, C39, C40, C41, C42.
The C01-C12 group was deliberately kept abstract-level at migration (the claims were written from abstracts); C36-C42 were re-checked against abstracts only.
**Question:** are these correctly conservative, or understated? (An understated claim is harmless but makes the skill hedge unnecessarily.)

### 3. Support kinds other than `primary` (6 claims)
C14 (absence_search), C19 (absence_search), C15 (third_party_context), C17 (general_method), C18 (general_method), C102 (third_party_context).
`absence_search` means "a search of INSPIRE found no AMS peer-reviewed paper on X" (antihelium C14, antideuteron C19), `third_party_context` rests on Tier 5/6 titles (C15, C102), `general_method` is textbook statistics or PDG (C17, C18).
**Question:** are the absence claims worded narrowly enough (search-limited, dated 2026-09-20)? Is C15's use of third-party titles as "context only" reasonable?

### 4. Numeric quotation withheld although the source was read in full (11 claims)
C46, C53, C57, C58, C66, C75, C79, C85, C104, C105, C106. These are conventions, qualitative statements, review-level interpretation (C75, C104), table layouts (C105, C106) or numbers without selection context.
**Question:** is any of these over-restricted (a number a physicist would want quoted) or, conversely, is a claim missing from this list that should be non-quotable because the number has no meaning outside its selection?

### 5. Multi-source claims (11 claims)
C14, C21, C33, C17, C43, C46, C47, C49, C53, C101, C105. A claim attached to several papers risks being stretched across them (the grading rounds repeatedly caught claim-ID stretching).
**Question:** does each of these hold for every listed paper as written, or should it be split per paper? (C21 spans the proton, positron, electron and antiproton selections; C33 the three isotope papers; C17 eight statistics papers.)

### 6. Performance numbers and ranges (27 claims with `performance_number`)
C21, C23, C25, C28, C30, C51, C54, C55, C56, C59, C60, C61, C62, C63, C64, C65, C66, C67, C68, C69, C70, C71, C72, C73, C80, C93, C94.
**Question:** for each, are the stated range, particle species and selection the ones the number actually belongs to (for example TRD rejection at a given e+ efficiency, charge-confusion fractions for electrons only)? Part 2 gives the scope the ledger records.

### 7. Tiers and supersession
- S26 (a theory paper pair on "tentative antihelium events") is stored as tier 5 with range [5, 6], and S28 (antideuteron: the only AMS-tagged INSPIRE hit is a 2008 conference paper; a 2013 JCAP paper on AMS-02/GAPS prospects is third party) as tier 3 with range [3, 6]. **Question:** the tier table has no class for a theory paper (tier 5 is "other experiments"); is 5 or 6 the better home for S26, and are S24/S25 (antihelium search items with no journal reference; their type, talk or thesis, was never established) correctly held at tier 3 and treated as preliminary? Also, S01 (the collaboration's own Physics Reports review) is tier 1 although tier 6 lists "reviews": is that right for a collaboration-authored review?
- S02 (PRL 110, 141102, 2013) is marked superseded by S03 (a row grouping PRL 113, 121101, 121102 and 221102, 2014) in range and statistics, taken from the author's earlier note. **Question:** is "superseded" the right relation (rather than "extended by"), and is it right to treat the three 2014 PRLs as one row? Neither S02's body nor S03 was read (APS blocked access; S02 is abstract-level and S03 metadata-only).
- The 11 tier-4 rows are statistics/method papers (Feldman-Cousins, Barlow-Beeston, Read CLs, TUnfold, pyhf, PDG, ...): **Question:** is "general method" the right label for how the skill uses them, and are any of them cited for something they do not say?

### 8. Things the ledger does not know (please say if any is wrong or important)
- Supplemental tables (daily and per-rotation fluxes, S43-S47) were surveyed for layout only (C105, C106); no correlation across days or rotations and no trial-factor correction is tabulated in the text read. The skill marks both unknown rather than zero.
- S16 and S20 are grouped navigation pointers (not cited for claims); individual PRLs are S41-S47.
- Figure-only content (resolution curves, rejection curves, cross sections, limits) is not transcribed by design.
- S02 and S03 full texts and the S41/S42 supplement figures were not read.

## Part 2. All claims

Columns: ID | source(s) | scope (species; range; period) | strength | support | numbers quotable | claim (first 170 characters) | verdict (OK / change / unsure) and note.

| ID | Src | Scope | Strength | Support | Num | Claim | Verdict |
|---|---|---|---|---|---|---|---|
| C01 | S01 | - | abstract+metadata | primary | yes | AMS was installed on the ISS on 19 May 2011 after a 16-year construction/test period and precursor shuttle flight |  |
| C02 | S01 | e+/e-/antiproton/proton/nuclei; first seven years | abstract+metadata | primary | yes | S01 presents results on 120 billion charged cosmic-ray events, covering fluxes of positrons, electrons, antiprotons, protons, and nuclei |  |
| C03 | S02 | e+/e-; 0.5-350 GeV | abstract+metadata | primary | yes | Positron fraction measured 0.5-350 GeV on 6.8×10⁶ positron and electron events |  |
| C04 | S04 | e+; to 1 TeV | abstract+metadata | primary | yes | Positron flux: 1.9 million positrons up to 1 TeV; an excess starting near 25 GeV, a dropoff above ~284 GeV, and a source-term cutoff (>4σ) |  |
| C05 | S06 | proton; 1 GV-1.8 TV | abstract+metadata | primary | yes | Proton flux 1 GV-1.8 TV, 300 million events; spectral index hardens with rigidity |  |
| C06 | S08 | antiproton/proton; 1-450 GV | abstract+metadata | primary | yes | Antiproton flux and `p̄/p` for 1-450 GV based on 3.49×10⁵ antiprotons and 2.42×10⁹ protons; `p̄`, `p`, `e⁺` fluxes have nearly identical rigidity dependence about 60-500… |  |
| C07 | S09 | antiproton; 1.00-41.9 GV; 11-year solar cycle | abstract+metadata | primary | yes | Antiproton results over an 11-year solar cycle: 1.1×10⁶ events, 1.00-41.9 GV; smaller time variation than `p`, `e⁻`, `e⁺` |  |
| C08 | S10 | boron/carbon; 1.9 GV-2.6 TV; first 5 years | abstract+metadata | primary | yes | B/C measured 1.9 GV-2.6 TV on 2.3 million B and 8.3 million C; above 65 GV power law index -0.333±0.014(fit)±0.005(syst), which the abstract reports as in good agreement… |  |
| C09 | S12 | 3He/4He; 4He 2.1-21 GV; 3He 1.9-15 GV; May 2011-Nov 2017 | abstract+metadata | primary | yes | `³He`, `⁴He` fluxes: 100 million `⁴He` (2.1-21 GV) and 18 million `³He` (1.9-15 GV), May 2011-Nov 2017; above 4 GV `³He/⁴He` time-independent, power-law index -0.294±0.0… |  |
| C10 | S13 | deuteron; 1.9-21 GV; May 2011-April 2021 | abstract+metadata | primary | yes | Deuteron flux: 21×10⁶ D nuclei, 1.9-21 GV, May 2011-April 2021, time variation nearly identical to p, ³He, ⁴He |  |
| C11 | S14 | 6Li/7Li; 1.9-25 GV | abstract+metadata | primary | yes | Li isotopes ⁶Li, ⁷Li measured 1.9-25 GV (9.7×10⁵ ⁶Li, 1.04×10⁶ ⁷Li) |  |
| C12 | S15 | P/Cl/Ar/K/Ca; 13.5 years | abstract+metadata | primary | yes | About one million P, Cl, Ar, K, Ca events over 13.5 years; fluxes described as sums of primary and secondary components |  |
| C13 | S17 | - | page | primary | no | Subsystem roles: Tracker in magnet (momentum, charge sign), TOF (trigger, direction, velocity, dE/dx), TRD (e±/p separation), ACC (side-entry veto), RICH with NaF and ae… |  |
| C14 | S22, S24, S25, S26 | antihelium | metadata-only | absence_search | no | No peer-reviewed AMS antihelium paper was found in INSPIRE (only the 1999 AMS-01 limit S22 among AMS-authored results; other hits are theses/talks and third-party interp… |  |
| C19 | S28 | antideuteron | metadata-only | absence_search | no | No AMS antideuteron measurement or search paper was found in INSPIRE; only a 2008 sensitivity conference paper and third-party prospects exist |  |
| C20 | S08 | antiproton/proton; 1-450 GV; 2011-05-19 to 2015-05-26 | full-text | primary | yes | Antiproton analysis data: 19 May 2011 to 26 May 2015 (over 65 billion events in the first 48 months); events need a TRD track and inner-tracker track, TOF β > 0.3 downwa… |  |
| C21 | S08, S04, S05, S06 | /Z/=1 | full-text | primary | yes | Performance quoted in S08 (also in S04, S05, S06 for the nine-layer tracker): maximum detectable rigidity 2 TV for /Z/ = 1 (3 m lever arm L1-L9); tracker charge resoluti… |  |
| C22 | S08 | antiproton; 1-450 GV | full-text | primary | yes | Antiproton extraction: template fit to the negative-rigidity sample using TRD estimator Λ_TRD (per-layer log-likelihood ratio, e vs p hypothesis) and a BDT charge-confus… |  |
| C23 | S08 | antiproton; 1-450 GV | full-text | primary | yes | Antiproton flux: iterative unfolding, acceptance folded with MC, iteration stopped when fluxes of two consecutive steps agree within 0.1%; four systematic sources added… |  |
| C24 | S04 | e+; 0.5 GeV-1 TeV; 2011-05-19 to 2017-11-12 | full-text | primary | yes | Positron flux data: 19 May 2011 to 12 Nov 2017 (1.07 × 10¹¹ events in about 6.5 years); E > 1.2 × maximum Størmer cutoff (backtracing gives the same result); χ²/d.o.f. <… |  |
| C25 | S04 | e+ | full-text | primary | yes | Positron flux estimator Φ = N/(A(1+δ)TΔE) in energy at the top of AMS; δ (data/MC efficiency corrections from the high-statistics electron sample) about -5% at 1 GeV, -2… |  |
| C26 | S05 | e-; 0.5 GeV-1.4 TeV | full-text | primary | yes | Electron flux: negative-rigidity sample; energy-dependent Λ_ECAL cut leaves antiproton background < 10⁻³ of the sample; template fit with an electron template and two ch… |  |
| C27 | S13 | deuteron; 1.9-21 GV; May 2011-April 2021 | full-text | primary | yes | Deuteron analysis: downward-going, track through tracker layer L1, charge Z = 1 required on L1, upper TOF, inner tracker, lower TOF; 26 rigidity bins 1.9-21 GV; an unfol… |  |
| C28 | S12 | 3He/4He; 1.92-21.1 GV; May 2011-Nov 2017 | full-text | primary | yes | Helium isotopes: 26 rigidity bins 1.92-21.1 GV; velocity bins for TOF, RICH-NaF and RICH-Agl; rates unfolded with resolution functions; TOF Δ(1/β) core width 0.02; RICH-… |  |
| C29 | S14 | 6Li/7Li; 1.9-25 GV; May 2011-Oct 2023 | full-text | primary | yes | Lithium isotopes: Z = 3 on L1, upper TOF, inner tracker, lower TOF; charge confusion from non-interacting nuclei < 0.01%; residual background from heavier nuclei interac… |  |
| C30 | S15 | P/Cl/Ar/K/Ca; 2011-05-19 to 2024-11-26 | full-text | primary | yes | Heavy nuclei P-Ca: 19 May 2011 to 26 Nov 2024 (2.4 × 10¹¹ events); bin-to-bin migration corrected by unfolding, with corrections to the P flux of about +25% at 3 GV, +8%… |  |
| C31 | S06 | proton; 1 GV-1.8 TV; 2011-05-19 to 2013-11-26 | full-text | primary | yes | Proton flux: first 30 months (19 May 2011 to 26 Nov 2013); 72 rigidity bins 1 GV-1.8 TV; live time > 50%, z axis within 40° of zenith, outside the South Atlantic Anomaly… |  |
| C32 | S10 | boron/carbon; 2011-05-19 to 2016-05-26 | full-text | primary | yes | B/C data period: 19 May 2011 to 26 May 2016 |  |
| C33 | S12, S13, S14 | D/4He/3He/4He/7Li/6Li | full-text | primary | yes | AMS combines independent systematic sources in quadrature for fluxes, and accounts for correlations of systematic errors when forming isotope ratios (D/⁴He, ³He/⁴He, ⁷Li… |  |
| C34 | S29 | as of 2026-09-20 | page | primary | yes | The Collaboration publications page lists, as its five most recent papers on 2026-09-20: PRL 136, 241002 (17 June 2026, P, Cl, Ar, K, Ca); PRL 134, 201001 (20 May 2025,… |  |
| C35 | S04 | e+ | full-text | primary | yes | Positron source-term energy cutoff significance: the abstract states "more than 4σ" and the article body gives 4.07σ (the point where 1/E_s reaches 0), so a claim of 5σ… |  |
| C15 | S26 | antihelium | metadata-only | third_party_context | no | Third-party literature (S26) discusses "tentative" AMS antihelium events, consistent with the events not being an established published result |  |
| C16 | S16 | - | metadata-only | primary | no | AMS time-structure results published as matched pairs across species/charge sign |  |
| C17 | S30, S31, S32, S33, S34, S35, S36, S37 | - | metadata-only | general_method | no | General statistical methods (asymptotics, Feldman-Cousins, CLs, Barlow-Beeston, unfolding, trial factors) |  |
| C18 | S39 | - | not-opened | general_method | no | Kinematic relations and Cherenkov/Bethe-Bloch/Highland formulae |  |
| C36 | S43 | proton; 1-100 GV; May 2011-October 2019 | abstract+metadata | primary | yes | Daily proton fluxes May 2011-October 2019, 1-100 GV: recurrent flux variations with a 27-day period in 2014-2018 and shorter 9-day and 13.5-day cycles in 2016; the stren… |  |
| C37 | S44 | helium/proton; about 2-7 GV and above (see abstract); May 2011-Octobe… | abstract+metadata | primary | yes | Daily helium fluxes: helium flux and helium-to-proton ratio vary on multiple timescales, with 27-day recurrence in 2014-2018 and 9 and 13.5-day cycles in 2016; below abo… |  |
| C38 | S41 | proton/helium; 1-60 GV; May 2011-May 2017 | abstract+metadata | primary | yes | Proton and helium fine time structures over 79 Bartels rotations (May 2011-May 2017), 1-60 GV: below 40 GV the proton and helium fluxes show nearly identical fine struct… |  |
| C39 | S42 | electron/positron; 1-50 GeV (energy); May 2011-May 2017 | abstract+metadata | primary | yes | Electron and positron fluxes over 79 Bartels rotations (May 2011-May 2017) in energy from 1 to 50 GeV: charge-sign dependent modulation during solar maximum studied with… |  |
| C40 | S45 | electron/proton; 1.00-41.9 GV; 11 years | abstract+metadata | primary | yes | Daily electron fluxes over 11 years, 1.00-41.9 GV: recurrent variations with periods of 27, 13.5 and 9 days; electron and proton variations differ, with a hysteresis bet… |  |
| C41 | S46 | positron/electron/proton; 1.00-41.9 GV; 11 years | abstract+metadata | primary | yes | Daily positron fluxes over 11 years, 1.00-41.9 GV: positron time variations differ distinctly from electron variations at short and long timescales and are similar to pr… |  |
| C42 | S47 | He/Li/Be/B/C/N/O; 1.92-60.3 GV; May 2011-November 2022 | abstract+metadata | primary | yes | Nuclei He, Li, Be, B, C, N, O over May 2011-November 2022, 1.92-60.3 GV: similar but not identical time variations with amplitudes decreasing with rigidity; the differen… |  |
| C43 | S43, S44 | proton/helium; proton 1.00-100 GV; helium 1.71-100 GV; 2011-05-20 to… | full-text | primary | yes | Daily-flux analyses: Phi_ji = N_ji / (A_ji eps_ji T_ji DeltaR_i) for rigidity bin i and day j, with N_ji corrected for bin-to-bin migration by unfolding performed indepe… |  |
| C44 | S43 | proton; 1.00-100 GV; 2011-05-20 to 2019-10-29 | full-text | primary | yes | Systematic errors in the daily proton flux are split into time-independent parts (inelastic interactions, rigidity resolution function, absolute rigidity scale) and time… |  |
| C45 | S43 | proton; 1-100 GV; 2011-05-20 to 2019-10-29 | full-text | primary | yes | Periodicity search in the daily proton flux: a wavelet time-frequency technique was used to locate the time intervals in which periodic structures emerge, with normalize… |  |
| C46 | S45, S46 | electron/positron; 1.00-41.9 GV; 11 years of daily data | full-text | primary | no | Lepton daily fluxes use Phi = N / (A(1+delta) eps T DeltaR): N corrected for background and migration by unfolding, A the MC effective acceptance, and delta a data/MC se… |  |
| C47 | S45, S46 | electron/positron/proton; 1.00-8.5 GV region; 2011-2021 | full-text | primary | yes | Hysteresis analysis: one flux is plotted against another (electron versus proton; electron and proton versus positron) using moving averages over 14 Bartels rotations (s… |  |
| C48 | S42 | electron/positron; energy bins to 49.33 GeV; 2011-05 to 2017-05 | full-text | primary | yes | Bartels-rotation lepton fluxes in energy: the exposure time T_i(E) for each rotation is determined by counting livetime-weighted seconds at each location above the geoma… |  |
| C49 | S41, S47 | proton/helium/nuclei; proton 1-60 GV; helium 1.9-60 GV; nuclei 1.92-6… | full-text | primary | yes | Bartels-rotation proton, helium and nuclei fluxes use Phi_i = N_i / (A_i eps_i T_i DeltaR_i) per rotation with bin-to-bin migration unfolded independently for each rotat… |  |
| C50 | S04 | e+/e-/proton; test beam 10-290 GeV/c (e+-), 180 and 400 GeV/c (p) | full-text | primary | yes | Detector description in the positron-flux paper: the three-dimensional imaging capability of the 17 radiation length ECAL allows an accurate measurement of the electron/… |  |
| C51 | S43 | proton; 1.00-100 GV; 2011-05-20 to 2019-10-29 | full-text | primary | yes | Daily proton analysis, collection time and cutoff: the collection time includes only seconds with the detector in normal operating conditions, AMS pointing within 40 deg… |  |
| C52 | S43 | proton; 1.00-100 GV; 2011-05-20 to 2019-10-29 | full-text | primary | yes | Wavelet analysis details for the daily proton periodicities: a continuous wavelet transform with a Morlet wavelet; normalized power defined as the wavelet power divided… |  |
| C53 | S46, S45 | positron/electron/proton; 1.00-11.0 GV; 2011-2021 | full-text | primary | no | Hysteresis significance procedure in the positron paper: choose two time intervals with the same electron flux, one before and one after 2014-2015, that show the most si… |  |
| C54 | S44 | helium; rigidity bins from 1.71 GV (upper edge not read from the SM t… | full-text | primary | yes | Daily helium analysis, selection and cutoff: the daily collection time counts only seconds in normal operating conditions, AMS pointing within 40 degrees of the local ze… |  |
| C55 | S44 | helium/proton; 1.71-1.92 GV bin for the single-bin significances; com… | full-text | primary | yes | Daily helium analysis, wavelet and hysteresis procedures: same construction as the proton case (Morlet wavelet, variance-normalized power, 95% confidence level from lag-… |  |
| C56 | S47 | helium/lithium/beryllium/boron/carbon/nitrogen/oxygen; from about 2 G… | full-text | primary | yes | Bartels-rotation nuclei analysis (He, Li, Be, B, C, N, O), selection and trigger: the collection time counts only seconds in normal operating conditions with AMS pointin… |  |
| C57 | S41 | proton/helium; tabulated rigidity bins from 1.00 GV; 2011-05 to 2017-… | full-text | primary | no | Table conventions in the Bartels-rotation proton and helium supplement: each rotation table gives statistical, time-dependent systematic (trigger and reconstruction effi… |  |
| C58 | S42 | electron/positron; from 0.50 GeV; 2011-05-20 to 2017-05-11 | full-text | primary | no | Time-averaged electron and positron supplement table: fluxes and the ratio Re are tabulated in energy (from 0.50-0.65 GeV) with statistical and total systematic uncertai… |  |
| C59 | S07 | helium; 1.9 GV-3 TV; first 30 months from 2011-05 | full-text | primary | yes | Helium flux selection and backgrounds (first 30 months): collection time counts only seconds in normal operating conditions with AMS within 40 degrees of the local zenit… |  |
| C60 | S07 | helium; 1.9 GV-3 TV; first 30 months from 2011-05 | full-text | primary | yes | Helium flux systematic-error ledger (first 30 months): trigger efficiency (below 0.2% under 100 GV, 1% at 3 TV, limited by the 1% prescaled sample); geomagnetic cutoff f… |  |
| C61 | S07 | helium; 1.9 GV-3 TV; first 30 months from 2011-05 | full-text | primary | yes | Helium rigidity resolution and its verification (first 30 months): the resolution function has a Gaussian core with width sigma/(1/R) = 9% at 10 GV, 14% at 100 GV, 20% a… |  |
| C62 | S11 | helium/carbon/oxygen; 2.2 GV-3.0 TV; first five years from 2011-05 | full-text | primary | yes | Helium, carbon and oxygen flux paper (first five years): the same selection as the helium paper with 40-degree pointing, 8.5x10^10 events collected and a collection time… |  |
| C63 | S01 | proton/helium/carbon/oxygen/iron; below 20 GV for the resolution; MDR… | full-text | primary | yes | Tracker rigidity measurement (review): tracks are found with a cellular-automaton track-finding algorithm and fitted with a Kalman filter that accounts for energy loss a… |  |
| C64 | S01 | electron/positron; 2-300 GeV in 72 bins; 2011-05 to 2018-05 | full-text | primary | yes | Absolute rigidity scale (review): the rigidity scale is the largest systematic at the highest energies for all Z; a coherent inner-tracker shift below 0.5 micrometre is… |  |
| C65 | S01 | electron/positron; up to 1 TeV (energy); 2011-05 to about 2018 (revie… | full-text | primary | yes | Charge-sign identification and charge confusion (review): charge confusion, meaning particles reconstructed with the wrong charge sign because of finite tracker resoluti… |  |
| C66 | S01 | n/u/c/l/e/i/ /Z/ /=/ /1/ /t/o/ /2/8; Z = 1-28; 2011-05 to about 2018… | full-text | primary | no | Tracker charge measurement (review): the nine tracker layers each measure /Z/ from ionization energy loss proportional to Z^2, on both x and y strips; strip amplitudes a… |  |
| C67 | S01 | e/+/-/,/ /p/r/o/t/o/n/,/ /n/u/c/l/e/i; Lambda_TRD distributions for 1… | full-text | primary | yes | TRD (review): 5248 proportional tubes of 6 mm diameter, maximum length 2 m, in 328 sixteen-tube modules on 20 layers (twelve y-layers in the middle, four x-layers on top… |  |
| C68 | S01 | Z/ /=/ /1/,/ /2/,/ /6/,/ /2/6/ /a/s/ /s/t/a/t/e/d; Z = 1 to 26; rigid… | full-text | primary | yes | TOF (review): two scintillator planes above and two below the magnet, each plane with 8 or 10 paddles read by 2 or 3 PMTs on each end; the coincidence of the four planes… |  |
| C69 | S01 | c/h/a/r/g/e/d/ /p/a/r/t/i/c/l/e/s; not applicable; 2011-05 to about 2… | full-text | primary | yes | ACC (review): sixteen curved scintillator panels of 800 mm length inside the magnet bore around the tracker, with wavelength-shifting fibres routed to PMTs from two adja… |  |
| C70 | S01 | c/h/a/r/g/e/d/ /n/u/c/l/e/i; beta > 0.75 (NaF), beta > 0.953 (aerogel… | full-text | primary | yes | RICH (review): a central radiator of 16 NaF tiles (85 x 85 x 5 mm^3, refractive index 1.33) surrounded by 92 aerogel tiles (113 x 113 x 25 mm^3, index 1.05); detection t… |  |
| C71 | S01 | e/+/-; 10-300 GeV beam-test; simulation above; 2011-05 to about 2018… | full-text | primary | yes | ECAL structure and reconstruction (review): a lead and scintillating-fibre sandwich of 9 superlayers (18.5 mm each, 11 grooved 1 mm lead foils and 10 layers of 1 mm fibr… |  |
| C72 | S01 | p/r/o/t/o/n/,/ /e/+/-; 1-2000 GeV/c; 2011-05 to about 2018 (review of… | full-text | primary | yes | ECAL proton rejection (review): the estimator Lambda_ECAL uses 16 variables, covering the compatibility of cell energy depositions with an electromagnetic shower and the… |  |
| C73 | S01 | e/+/-/,/ /Z/ /=/ /1/ /p/a/r/t/i/c/l/e/s; electron efficiency measured… | full-text | primary | yes | Trigger and data acquisition (review): about 300,000 channels are digitized only after a two-level trigger; the fast trigger is the OR of (1) a coincidence within 240 ns… |  |
| C74 | S01 | a/n/t/i/p/r/o/t/o/n; 1-525 GV (rigidity); 2011-05 to about 2018 (revi… | full-text | primary | yes | Antiproton flux in the review: the latest measurement covers 1 to 525 GV with 5.6e5 antiproton events, agrees with the earlier AMS publication (3.5e5 events, up to 450 G… |  |
| C75 | S01 | a/n/t/i/p/r/o/t/o/n/,/ /p/r/o/t/o/n; above about 60 GV for the simila… | full-text | primary | no | Interpretation statements in the review on antiprotons (collaboration statements, not measurements): the antiproton-to-proton flux ratio shows an antiproton spectrum sim… |  |
| C76 | S01 | p/o/s/i/t/r/o/n/,/ /p/r/o/t/o/n; 55.58-1000 GeV (energy); 2011-05 to… | full-text | primary | yes | Positron-to-proton flux ratio in the review: with the two spectra normalized at 60 GeV, E^3 times the positron flux decreases above 284 GeV whereas the proton spectrum k… |  |
| C77 | S01 | p/o/s/i/t/r/o/n/,/ /a/n/t/i/p/r/o/t/o/n; 60-525 GeV (energy); 2011-05… | full-text | primary | yes | Positron-to-antiproton flux ratio in the review: above 60 GeV the ratio is consistent with a constant; a constant fit in 60-525 GeV gives 2.00 +- 0.035 (stat.) +- 0.06 (… |  |
| C78 | S01 | p/r/o/t/o/n; 1 GV-1.8 TV flux; fit 45 GV-1.8 TV; 2011-05 to about 201… | full-text | primary | yes | Proton flux in the review: the latest measurement covers 1 GV to 1.8 TV with 1 billion proton events, in complete agreement with the earlier published result (300 millio… |  |
| C79 | S01 | p/r/o/t/o/n/,/ /p/o/s/i/t/r/o/n/,/ /e/l/e/c/t/r/o/n; protons 45 GV-1.… | full-text | primary | no | Conventions of the review's proton and lepton tables and fits: the three fit uncertainties are (fit) = statistical plus uncorrelated systematic errors, (sys) = the remai… |  |
| C80 | S01 | H/e/,/ /L/i/,/ /B/e/,/ /B/,/ /C/,/ /N/,/ /O/,/ /N/e/,/ /M/g/,/ /S/i;… | full-text | primary | yes | Nuclear interaction cross sections in AMS material (review): averaged over path lengths in the acceptance the material traversed is 73% carbon, 17% aluminium by mass wit… |  |
| C81 | S01 | h/e/l/i/u/m/,/ /c/a/r/b/o/n/,/ /o/x/y/g/e/n; He, C: 1.9 GV-3 TV; O: 2… | full-text | primary | yes | Helium, carbon and oxygen fluxes in the review: 125 million He, 14 million C and 12 million O nuclei give fluxes from 1.9 GV to 3 TV for He and C and 2.2 GV to 3 TV for… |  |
| C82 | S01 | p/r/o/t/o/n/,/ /h/e/l/i/u/m; 1.9-1800 GV; fit above 3.5 GV; 2011-05 t… | full-text | primary | yes | Proton-to-helium flux ratio in the review: the ratio is not constant, decreasing over 1.9-1800 GV with a rate of decrease that vanishes at high rigidity; above 3.5 GV (c… |  |
| C83 | S01 | l/i/t/h/i/u/m/,/ /b/e/r/y/l/l/i/u/m/,/ /b/o/r/o/n; 1.9 GV-3.3 TV; ide… | full-text | primary | yes | Lithium, beryllium and boron fluxes in the review: 3.0 million Li, 1.7 million Be and 4.2 million B nuclei over 1.9 GV to 3.3 TV, with a total error of 3% at 100 GV for… |  |
| C84 | S01 | l/i/t/h/i/u/m/,/ /b/e/r/y/l/l/i/u/m/,/ /b/o/r/o/n/ /o/v/e/r/ /c/a/r/b… | full-text | primary | yes | Secondary-to-primary ratios and the high-rigidity hardening in the review: the Li, Be and B fluxes were divided by the C and O fluxes (Li/C, Be/C, B/C, Li/O, Be/O, B/O);… |  |
| C85 | S01 | L/i/,/ /B/e/,/ /B/ /o/v/e/r/ /O/ /(/a/n/d/ /C/); 2.15-3300 GV; 2011-0… | full-text | primary | no | Table conventions for the review's ratio tables (Li/O, Be/O, B/O, and similar): each ratio table gives sigma_stat, sigma_acc (trigger, acceptance and background), sigma_… |  |
| C86 | S01 | h/e/l/i/u/m/-/3/,/ /h/e/l/i/u/m/-/4; 1.9-21 GV; power law above 4 GV;… | full-text | primary | yes | Helium isotopes in the review: 100 million 4He (2.1-21 GV) and 18 million 3He (1.9-15 GV), the 3He and 4He fluxes vary nearly identically with time when binned per 4 Bar… |  |
| C87 | S01 | s/t/r/a/n/g/e/l/e/t/ /c/a/n/d/i/d/a/t/e/s/ /(/Z///A/ /</ /0/./1/)/,/… | full-text | primary | yes | Strangelet search in the review: strangelets are characterized by Z/A < 0.1; the search uses inner tracker L2-L8 for rigidity and the TOF for velocity and, because of th… |  |
| C88 | S01 | p/r/o/t/o/n/,/ /h/e/l/i/u/m; 1-60 GV (p), 1.9-60 GV (He); fine struct… | full-text | primary | yes | Time-dependent proton and helium fluxes in the review: 846 million proton events (1-60 GV) and 112 million helium events (1.9-60 GV) over 79 Bartels rotations (27 days e… |  |
| C89 | S01 | e/l/e/c/t/r/o/n/,/ /p/o/s/i/t/r/o/n; 1-50 GeV (energy); 2011-05 to 20… | full-text | primary | yes | Time-dependent electron and positron fluxes in the review: 23.5 million events over the same 79 Bartels rotations (May 2011 to May 2017) in 1-50 GeV with 49 energy bins;… |  |
| C90 | S01 | e/l/e/c/t/r/o/n/,/ /p/o/s/i/t/r/o/n; 1-21 GeV fits; transition amplit… | full-text | primary | yes | Logistic-function analysis of the positron-to-electron ratio in the review: the 3871 independent R_e = Phi(e+)/Phi(e-) measurements in energy and time are described with… |  |
| C91 | S01 | n/i/t/r/o/g/e/n/ /(/w/i/t/h/ /o/x/y/g/e/n/ /a/n/d/ /b/o/r/o/n/ /a/s/… | full-text | primary | yes | Nitrogen flux in the review: 3.9 million nitrogen nuclei over 2.2 GV to 3.3 TV with a total flux error of 3.8% at 100 GV, consistent with the published AMS result with s… |  |
| C92 | S01 | n/e/o/n/,/ /m/a/g/n/e/s/i/u/m/,/ /s/i/l/i/c/o/n/ /(/r/e/f/e/r/e/n/c/e… | full-text | primary | yes | Neon, magnesium and silicon fluxes in the review: 1.8 million Ne, 2.2 million Mg and 1.6 million Si nuclei over 2.15 GV to 3.0 TV (first rigidity-dependent measurements… |  |
| C93 | S01 | n/o/t/ /s/p/e/c/i/e/s/-/s/p/e/c/i/f/i/c; not applicable; 2011-05 to a… | full-text | primary | yes | Permanent magnet (review): 64 Nd-Fe-B sectors assembled in a cylindrical shell 800 mm long with 1115 mm inner diameter, giving a field of 1.4 kG at the centre with negli… |  |
| C94 | S01 | n/u/c/l/e/i/ /(/H/e/,/ /C/,/ /O/ /f/o/r/ /t/h/e/ /a/c/c/u/r/a/c/y/ /f… | full-text | primary | yes | Tracker layout and coordinate measurement (review): 192 ladders of double-sided silicon sensors with 196,608 readout channels in nine layers; L3-L8 sit on three honeycom… |  |
| C95 | S01 | p/o/s/i/t/r/o/n; up to 1 TeV (energy); 2011-05 to about 2018 (review… | full-text | primary | yes | Positron flux in the review (positron chapter): the measurement uses 1.9 million positrons up to 1 TeV; selection uses an energy-dependent cut on Lambda_ECAL to remove t… |  |
| C96 | S01 | p/o/s/i/t/r/o/n; 7.10-1000 GeV (energy); 2011-05 to about 2018 (revie… | full-text | primary | yes | Power-law-with-transition fits to the positron flux in the review (Eq. 4: Phi = C (E/55.58 GeV)^gamma for E <= E0 and C (E/55.58 GeV)^gamma (E/E0)^Delta gamma above; the… |  |
| C97 | S01 | p/o/s/i/t/r/o/n; 0.5-1000 GeV fit; anisotropy above 16 GeV; 2011-05 t… | full-text | primary | yes | Diffuse-plus-source parametrization of the positron flux and the isotropy limit in the review: Phi(E) = (E^2 / E^^2) [C_d (E^/E1)^gamma_d + C_s (E^/E2)^gamma_s exp(-E^/E… |  |
| C98 | S01 | e/l/e/c/t/r/o/n; 20.04-1400 GeV for the fit; indices 3.36-1400 GeV; 2… | full-text | primary | yes | Electron flux in the review: 28.1 million electron events up to 1.4 TeV, analysed like the positrons; the review states that the GALPROP secondary-electron contribution… |  |
| C99 | S01 | e/l/e/c/t/r/o/n/ /(/w/i/t/h/ /t/h/e/ /p/o/s/i/t/r/o/n/ /s/o/u/r/c/e/… | full-text | primary | yes | Tests of the positron source term and of an energy cutoff in the electron flux (review): the electron flux was fitted with a power law plus the positron source term with… |  |
| C100 | S01 | e/l/e/c/t/r/o/n/,/ /p/o/s/i/t/r/o/n; 0.5-1400 GeV for the fit; anisot… | full-text | primary | yes | Two-component description of the electron flux, arrival directions and combined flux in the review: over 0.5-1400 GeV the electron flux is fitted with the sum of two pow… |  |
| C101 | S48, S49 | - | page | primary | yes | The Tracker Layer-0 upgrade is a new silicon tracker layer on top of the AMS detector, stated by the AMS website to increase AMS acceptance by 300% (the CERN news item s… |  |
| C102 | S49 | planned 2027 detector era | page | third_party_context | yes | Planned schedule as of the CERN news item of 21 August 2026: Layer-0 final acceptance test at INFN-University of Perugia until 30 August, a last series of measurements a… |  |
| C103 | S01 | 2011-05 to about 2018 (review of the first seven years) | full-text | primary | yes | Mission context in the review's introduction: AMS-02 was launched on the Space Shuttle Endeavour and installed on the ISS on May 19, 2011, following the AMS-01 precursor… |  |
| C104 | S01 | 2011-05 to about 2018 (review of the first seven years) | full-text | primary | no | Summary of the review (chapter 17, p. 111): the review states that the precision and characteristics of the AMS data, measured simultaneously for many types of cosmic ra… |  |
| C105 | S43, S44, S45, S46 | proton/helium/electron/positron; proton 1.00-100 GV; helium, electron… | full-text | primary | no | Daily-flux supplement tables (S43-S46), layout and content, read on 2026-10-02 from the extracted table text: each daily flux is a separate table of rigidity bins with t… |  |
| C106 | S47 | helium/lithium/beryllium/boron/carbon/nitrogen/oxygen; rigidity bins… | full-text | primary | no | Per-rotation nuclei supplement tables (S47): 1029 tables, one per species per Bartels rotation, 147 rotations (numbers 2426 to 2581, from May 15 2011 to November 25 2022… |  |

Full wording, location, scope and limitations of every claim: `references/source-index.md` (generated from the same JSON) or `data/claims.json`.

## Part 3. Sources

| ID | Tier | Level | Published | Data period | Note |
|---|---|---|---|---|---|
| S01 | 1 | full-text | 2021 | - | AMS on the ISS, Part II: Results from the first seven years, Phys. Re… (Full text (116 pages) obtained from the INSPIRE-hosted file on 2026-09-21 and converted wi) |
| S02 | 1 | abstract+metadata | 2013 | - | First Result from AMS on the ISS: Precision Measurement of the Positr… (superseded by S03; Full text not obtained; only the INSPIRE abstract and metadata were read.) |
| S03 | 1 | metadata-only | 2014 | - | High Statistics Measurement of the Positron Fraction 0.5-500 GeV (PRL… (supersedes S02; Metadata-only; treat titles as navigation.) |
| S04 | 1 | full-text | 2019 | 2011-05-19 to 2017-11-12 | Towards Understanding the Origin of Cosmic-Ray Positrons, PRL 122, 04… (Supplemental Material not opened, so per-cut definitions and many tables are missing.) |
| S05 | 1 | full-text | 2019 | - | Towards Understanding the Origin of Cosmic-Ray Electrons, PRL 122, 10… (Supplemental Material not opened, so per-cut definitions and many tables are missing.) |
| S06 | 1 | full-text | 2015 | 2011-05-19 to 2013-11-26 | Precision Measurement of the Proton Flux, 1 GV-1.8 TV, PRL 114, 171103 (Supplemental Material not opened, so per-cut definitions and many tables are missing.) |
| S07 | 1 | full-text | 2015 | - | Precision Measurement of the Helium Flux, 1.9 GV-3 TV, PRL 115, 211101 (Main article read from the publisher PDF (pdftotext) on 2026-09-21; Supplemental Material) |
| S08 | 1 | full-text | 2016 | 2011-05-19 to 2015-05-26 | Antiproton Flux, Antiproton-to-Proton Flux Ratio, and Properties of E… (Supplemental Material not opened, so per-cut definitions and many tables are missing.) |
| S09 | 1 | abstract+metadata | 2025-02-03 | - | Antiprotons and Elementary Particles over a Solar Cycle, PRL 134, 051… |
| S10 | 1 | full-text | 2016 | 2011-05-19 to 2016-05-26 | Precision Measurement of the Boron to Carbon Flux Ratio, 1.9 GV-2.6 T… (Only the data period was read from the downloaded main article; Supplemental Material not) |
| S11 | 1 | full-text | 2017 | - | Identical Rigidity Dependence of He, C, and O at High Rigidities, PRL… (Main article read from the publisher PDF (pdftotext) on 2026-09-21; Supplemental Material) |
| S12 | 1 | full-text | 2019 | 2011-05 to 2017-11 | Properties of Cosmic Helium Isotopes, PRL 123, 181102 (Supplemental Material not opened, so per-cut definitions and many tables are missing.) |
| S13 | 1 | full-text | 2024-06-25 | 2011-05 to 2021-04 | Properties of Cosmic Deuterons, PRL 132, 261001 (Supplemental Material not opened, so per-cut definitions and many tables are missing.) |
| S14 | 1 | full-text | 2025-05-20 | 2011-05 to 2023-10 | Properties of Cosmic Lithium Isotopes, PRL 134, 201001 (Supplemental Material not opened, so per-cut definitions and many tables are missing.) |
| S15 | 1 | full-text | 2026-06-17 | 2011-05-19 to 2024-11-26 | Properties of Heavy Cosmic Nuclei P, Cl, Ar, K, Ca, PRL 136, 241002 (Supplemental Material not opened, so per-cut definitions and many tables are missing.) |
| S16 | 1 | metadata-only | 2018-2023 | - | Time-structure and periodicity PRLs: 121, 051101; 121, 051102 (2018);… (Metadata-only; treat titles as navigation.) |
| S17 | 2 | page | page fetched 2026-09-20 | - | AMS-02 detector web page (subsystem summaries) |
| S18 | 2 (may be proceedings; check) | metadata-only | 2011-2026 | - | Subsystem NIM A papers: Tracker performance (Haino, NIM A 699, 221, 2… |
| S19 | 2 | not-verified | 2017 | - | Tracker cross-strip nonlinearity (NIM A 869, 29, 2017); ECAL 3D showe… (Not verified this session (carried from hep-analysis reference 38).) |
| S20 | 1 | metadata-only | 2018-2025 | - | Additional AMS nuclei PRLs with year: N (121, 051103, 2018); Li, Be,… (Metadata-only; treat titles as navigation.) |
| S21 | 1 (metadata) | metadata-only | 2026-09-20 | - | Precision timeline check: AMS PRL list (30 PRLs 2013-2026) |
| S22 | 1 (historical, AMS-01) | metadata-only | 1999 | - | Search for antihelium in cosmic rays, Phys. Lett. B 461, 387 (AMS-01) |
| S23 | 1 (historical) | metadata-only | 2002 | - | AMS on the ISS, Part I: results from the test flight on the space shu… |
| S24 | 3 (unverified type) | metadata-only | 2026 | - | "Combined Machine Learning Analysis for Antihelium Search with the AM… (Type (talk, thesis, other) and content not established; the skill supplies no counts.) |
| S25 | 3 (unverified type) | metadata-only | 2023 | - | "Search for antihelium nuclei in cosmic rays with the AMS-02 experime… (Type (talk, thesis, other) and content not established; the skill supplies no counts.) |
| S26 | 5/6 (third-party interpretation; use only to show the events were discussed as tentative) | metadata-only | 2017; 2019 | - | Theory discussion of "tentative AMS antihelium events": Coogan and Pr… (Third-party interpretation; unverified in content beyond the titles.) |
| S27 | 6 | not-opened | 2020-2021 | - | Reviews mentioning conference antihelium statements: arXiv:2112.15255… (Found through a search-result listing only; not evidence for counts.) |
| S28 | 3 / 5-6 | metadata-only | 2008; 2013 | - | Antideuteron: only AMS-tagged INSPIRE hit is a 2008 conference paper… |
| S29 | 2 | page | page fetched 2026-09-20 | - | AMS Collaboration publications page (dated list of papers) |
| S30 | 4 | metadata-only | 2011 | - | Asymptotic formulae for likelihood-based tests of new physics, EPJC 7… |
| S31 | 4 | metadata-only | 1998 | - | A Unified Approach to the Classical Statistical Analysis of Small Sig… |
| S32 | 4 | metadata-only | 1993 | - | Fitting using finite Monte Carlo samples, CPC 77, 219 |
| S33 | 4 | metadata-only | 2011 | - | Incorporating nuisance parameters in likelihoods for multisource spec… |
| S34 | 4 | metadata-only | 1995 | - | A multidimensional unfolding method based on Bayes' theorem, NIM A 36… |
| S35 | 4 | metadata-only | 2012 | - | TUnfold, JINST 7, T10003 |
| S36 | 4 | metadata-only | 1999 | - | Confidence level computation for combining searches with small statis… |
| S37 | 4 | metadata-only | 2010 | - | Trial factors for the look elsewhere effect, EPJC 70, 525 |
| S38 | 4 | metadata-only | 2021 | - | pyhf: pure-Python implementation of HistFactory, JOSS 6, 2823 |
| S39 | 4 | metadata-only | 2024 | - | Review of Particle Physics, PRD 110, 030001 (kinematics, passage of p… (Metadata only; general formulas are standard but must be cited to a specific PDG section w) |
| S40 | 4 | not-verified | 2002 | - | Read, "Presentation of search results: the CLs technique," J. Phys. G… (Not verified this session.) |
| S41 | 1 | full-text | 2018 | 2011-05 to 2017-05 | Observation of Fine Time Structures in the Cosmic Proton and Helium F… (Main article (publisher PDF) and the Supplemental Material text were read with pdftotext () |
| S42 | 1 | full-text | 2018 | 2011-05 to 2017-05 | Observation of Complex Time Structures in the Cosmic-Ray Electron and… (Main article (publisher PDF) and the Supplemental Material text were read with pdftotext () |
| S43 | 1 | full-text | 2021 | 2011-05 to 2019-10 | Periodicities in the Daily Proton Fluxes from 2011 to 2019 Measured b… (Main article and the text of the Supplemental Material (publisher PDFs, pdftotext, 2026-09) |
| S44 | 1 | full-text | 2022 | 2011-05 to 2019-10 | Properties of Daily Helium Fluxes, PRL 128, 231102 (Main article (publisher PDF) and the Supplemental Material text were read with pdftotext () |
| S45 | 1 | full-text | 2023 | - | Temporal Structures in Electron Spectra and Charge Sign Effects in Ga… (Main article and the text of the Supplemental Material (publisher PDFs, pdftotext, 2026-09) |
| S46 | 1 | full-text | 2023 | - | Temporal Structures in Positron Spectra and Charge-Sign Effects in Ga… (Main article and the text of the Supplemental Material (publisher PDFs, pdftotext, 2026-09) |
| S47 | 1 | full-text | 2025 | 2011-05 to 2022-11 | Solar Modulation of Cosmic Nuclei over a Solar Cycle: Results from th… (Main article (publisher PDF) and the Supplemental Material text were read with pdftotext () |
| S48 | 2 | page | page fetched 2026-10-01 | - | AMS-02 Tracker Layer-0 Upgrade web page (Web-fetch summary of the page; no installation status or timeline on the page.) |
| S49 | 6 | page | 2026-08-21 | - | Final tests for the AMS upgrade before spaceflight (CERN news) (Web-fetch summary; schedule dates are planned and may have slipped since 2026-08-21.) |
