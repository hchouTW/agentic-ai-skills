# Round 7 grades, group Gc (T32)

Grader: Opus (independent of the Sonnet answerers). Graded only against `references/tests-and-examples.md` (scoring rules, T32 entry) and `data/claims.json` / `data/sources.json`. No earlier grades or answers were consulted.

Prompt (T32): "Design a 27-day-bin positron-to-electron ratio over the solar cycle from 5 to 50 GV and search it for a one-year periodicity."

| Test | Sample | Score /10 | Blocking failure |
|---|---|---|---|
| T32 | C | 9 | none |
| T32 | D | 10 | none |

Rubric per answer: scientific_correctness (SC), ams_specificity (AS), uncertainty_and_validation (UV), source_discipline (SD), usefulness (U), 0-2 each.

---

## T32_C: 9/10 (SC 2, AS 2, UV 2, SD 1, U 2). Blocking failure: none

### Claim verification

| Cited | What the answer says | Ledger check | Verdict |
|---|---|---|---|
| C36-C41 (line 8) | "AMS published daily and Bartels-rotation e+ and e- fluxes with recurrent 27-day, 13.5-day and 9-day structure", abstract level | C36, C37, C38 are proton/helium claims (S43, S44, S41). C39 (Bartels leptons) reports months-scale structures, with no 27/13.5/9-day periods. C40 (daily e-) has the 27/13.5/9-day periods. C41 (daily e+) states that e+ variations differ from e- and resemble p, but gives no periods. | **Overscoped.** A range of six claims, three of them for other species, is used to attribute the periods to both leptons and to the Bartels product. Only C40 supports the electron part. |
| C40, C41 | Daily e-/e+ in rigidity, 1.00-41.9 GV | Matches (abstract+metadata) | OK |
| C39, C48 | Bartels lepton paper in energy, 1-50 GeV | C39 range 1-50 GeV (energy); C48 energy bins to 49.33 GeV | OK |
| C90, S01 | Four-parameter logistic for e+/e- across the 2013 reversal; Delta t = 830 +- 30 days, energy independent; t_rev = 1 July 2013 is a stated choice; descriptive | Matches C90 (full-text, numeric allowed) and its limitations | OK. The answer omits C90's energy domain (fits 1-21 GeV, amplitude C consistent with zero above 20 GeV), which matters for a 5-50 GV trend model. |
| C07, S09 | Antiprotons vary less than p, e-, e+ over 11 years, 1.00-41.9 GV, abstract level, "not a statement about the e+/e- ratio" | Matches, and the verification level is stated correctly | OK (marginal relevance) |
| C45, C52 | Wavelet, normalized power, 95% levels from lag-1 red-noise MC, daily protons; trial-factor use is unknown | Matches, including the limitation that no trial-factor treatment is described | OK |
| C25 | "the lepton flux analyses use bin widths at least twice the energy resolution" | C25 covers the positron flux (S04) only | Minor overgeneralization ("lepton analyses", plural). It is labeled "a choice of that analysis". |
| C43, C46, C48, C49 | Migration unfolded independently per time bin; exposure from livetime-weighted seconds above cutoff, normal conditions, 40 deg zenith, outside SAA | C43 (daily p/He), C46 (daily leptons, unfolding), C48 (rotation exposure definition), C49 (per-rotation unfolding) | OK, labeled as choices of those analyses |
| C24-C26 | Template fit in (Lambda_TRD, Lambda_CC) with correct-sign lepton, correct-sign proton, charge-confused lepton | C24 (e+) matches. C26 (e-) uses charge-confusion positron and proton templates, not a correct-sign proton. | Acceptable as "consistent with documented practice"; it is slightly imprecise for e- |
| C27, C31, C49 | Cutoff factor 1.2 with scans 1.0-1.4 | C31 gives 1.2 (no scan). C27 and C49 give the 1.0-1.4 scan. C49 gives nominal 1.2. | OK in combination; "not a universal value" is stated |
| C40, C41 (sec 4.1) | Hysteresis below about 8.5 GV (e-/p and e-/e+); e+ modulated more than p below about 7 GV; "do not merge the two thresholds" | Matches | OK |
| C27, C29 | 108-day (four-rotation) binning of the deuteron/Li analyses, not a rule | Matches | OK; satisfies the critical requirement |
| S37 | Gross and Vitells for local/global significance | Tier-4 method reference, metadata-only | OK as a method citation |

No number in the answer is attributed to AMS outside the ledger. The verification level is never overstated: abstract-level claims are labeled "abstract level".

### Defects
1. **Source scope (SD, deducted).** The "[Documented, C36-C41]" range attributes 27/13.5/9-day lepton periodicities to claims about protons and helium, and to C39/C41, which do not state them. This is the kind of correct-sounding statement attached to the wrong claim that T35-T41 were built to catch.
2. Uncited quantitative statement: "the e- flux is about an order of magnitude larger than the e+ flux". This is general knowledge, not blocking, but it is not in the ledger and has no label.
3. C25 is generalized to "the lepton flux analyses", but it is positron-only.
4. The phrase "the positron-free combined e+ + e- flux" contradicts itself; it is probably meant to be the electron flux or the e+ + e- sum.
5. "About 150 bins at most" for 10-12 years: 12 years is about 162 Bartels rotations. Small arithmetic slip.
6. C90's energy scope (1-21 GeV fits; transition amplitude consistent with zero above 20 GeV) is not carried into the trend-model discussion. The trend shape should differ across 5-50 GV.

### Critical requirements and prohibited claims
- Documented items have claim IDs and scope: met except defect 1. The 108-day binning is correctly scoped (C27, C29).
- Rigidity versus energy flagged for leptons: met well. It notes R approximately equals E for |Z| = 1, the Tracker measures R and the ECAL measures E, the binning variable sets the migration and scale systematics, and the 41.9 GV versus 50 GeV edge mismatch.
- No invented AMS periodicity result or significance: met. The trial-factor use is stated as unknown.
- Prohibited claims: no single-frequency p-value for a scan, and it says so explicitly. No Wilks for the period search. No AMS livetime or calibration details beyond the ledger. 108-day binning is not presented as a rule.
- Observable decisions: all present. These are per-bin and per-sign exposure and cutoff transmission; a counts-limited rigidity ceiling or merging; a cancellation table plus a (time, rigidity, species) covariance; sign-specific charge-confusion tails; a predefined band with local/global significance; control series for exposure, efficiency and the single species; joint versus separate fits; and the evidence gap. It also includes strong extras: aliasing of 13.5- and 9-day structure, the heliolatitude annual term, and injection-based sensitivity giving an amplitude upper limit.

### Missing expected cross-citations
- C44 (time-dependent versus time-independent systematics split; no cross-day covariance model in S43/S45/S46). This is the documented basis for the "[Unknown/needs input]" covariance statement, but it is not cited.
- C51 (data-derived cutoff in the daily proton analysis) as the documented alternative to a fixed safety factor.
- C39's content that months-scale structures common to e+ and e- are not visible in the ratio. C39 is cited only for its energy range, but this result bears directly on what the ratio's time series should look like.

---

## T32_D: 10/10 (SC 2, AS 2, UV 2, SD 2, U 2). Blocking failure: none

### Claim verification

| Cited | What the answer says | Ledger check | Verdict |
|---|---|---|---|
| (header) | "Nothing below states an AMS result for a one-year periodicity ... I found no such claim in the ledger" | Correct, since no ledger claim covers an annual e+/e- periodicity | OK |
| C40, C41 | Daily e+/e- in rigidity, 1.00-41.9 GV; 5-50 GV not covered above 41.9 GV | Matches | OK |
| C48 | Bartels lepton paper in energy, up to 49.33 GeV | Matches the C48 scope text exactly | OK |
| C27, C29 | 108-day (four-rotation) blocks are those analyses' choice, not a rule | Matches | OK; satisfies the critical requirement |
| C41 | e+/e- hysteresis below about 8.5 GV; e+ modulated more than p below about 7 GV; do not merge thresholds | Matches | OK |
| C63 | Review gives Delta R/R = 0.1 below 20 GV; review-level, "use only as a scale" | Matches (full-text, numeric allowed, review) | OK. The nine-layer configuration scope of C63 is not stated (minor). |
| C24, C48 | Lepton analyses used 1.2 x cutoff (in energy) and a 40-degree pointing cut | C24: E > 1.2 x max Stormer cutoff. C48: 40 deg from zenith. | OK in combination; "not a standard" is stated |
| C51 | One daily proton analysis computed the cutoff from data | Matches | OK |
| C49, C27 | Safety factor scanned 1.0-1.4 | Matches | OK |
| C24 | 2D template fit (Lambda_TRD vs BDT Lambda_CC), correct-sign lepton, correct-sign proton, charge-confusion lepton templates | Matches C24 (positron). Described as "public lepton analyses". | OK (C26 for e- not cited; minor) |
| C65 | Review: electron charge-confusion fraction below 8% up to 1 TeV after selection; electrons only, not a general rate; not to be used without per-bin estimate | Matches C65 and its limitation exactly | OK, exemplary scoping |
| C43, C49 | Unfold per time bin independently | Matches (daily p/He; per-rotation p/He/nuclei) | OK |
| C48, C51 | Exposure: livetime-weighted seconds above cutoff | Matches | OK ("cf.") |
| C44 | Time-independent versus time-dependent systematics, time-dependent added in quadrature; scope S43 daily proton only; AMS cross-day correlation not described | Matches C44 and its limitation | OK |
| C45, C52 | Morlet wavelet, normalized power, 95% CL from lag-1 AR MC matched in variance and lag-1 autocorrelation; S43 daily proton only; not a rule | Matches C52 exactly | OK |
| C90 | Logistic across the 2013 reversal; Delta t = 830 +- 30 days, energy independent; descriptive review-level fit; t_rev = 1 July 2013 a stated choice | Matches | OK. As in C, it omits the 1-21 GeV fit domain and that C is consistent with zero above 20 GeV. |
| S37 | Gross and Vitells trial factors | Method reference | OK |
| Source note | "ledger last verified 2026-09-20"; currency check via INSPIRE/ams02.space | Consistent with the claims' last_reviewed dates | OK |

No invented AMS numbers, procedures or results. Every quoted number has a matching claim with numeric_quotation_allowed = true.

### Defects (minor, not deducted)
1. The rigidity-versus-energy flag is mostly about the data product: the public lepton products differ in variable, and the binning must not be copied. It is thinner than ideal, because it does not say that the ECAL measures energy while the Tracker measures rigidity, or how the binning variable sets the scale systematics. The critical requirement is still met.
2. The verification level of the abstract-level claims C40 and C41 (abstract+metadata) is not stated. It is not overstated, and the header limits use to "the stated scope".
3. C63's nine-layer configuration scope is not mentioned when using the 0.1 resolution as a binning scale.
4. C90's energy domain (1-21 GeV, amplitude consistent with zero above 20 GeV) is not used in the trend-model discussion.
5. The answer does not discuss aliasing or leakage of the 27-, 13.5- or 9-day solar structure under 27-day sampling, beyond "not in scope". The grid-phase-shift cross-check (sec 7) partly compensates. Physical annual sources such as the Earth's heliolatitude are not named as confounders.

### Critical requirements and prohibited claims
- Documented items have claim IDs and scope: met, with consistently careful scoping (C44, C45, C52, C65 limitations carried).
- Rigidity versus energy flagged for leptons: met (minimal; see defect 1).
- No invented AMS periodicity result or significance: met, and stated explicitly.
- Prohibited claims: none. A single-frequency p-value is used only when one frequency is pre-registered, and the scan requires a trial factor and toys. There is no Wilks for the period search; the a = b = 0 test is at fixed P with toy calibration. No AMS livetime or calibration details beyond the ledger. 108-day binning is scoped.
- Observable decisions: all present. These are per-bin and per-sign exposure and cutoff; counts-driven bin edges and a stated supported range; an effect-classification table and (time, rigidity) covariance; a sign-specific charge-confusion migration matrix; a predefined band with local/global significance and correlated rigidity-bin trials via toys; control series for exposure, livetime, transmission, efficiency, contamination and charge-confusion fraction versus time; joint versus separate fits; and an explicit evidence-gap list (sec 8).

### Missing expected cross-citations
- C39 (the Bartels-rotation lepton paper's abstract: months-scale structures not visible in the e+/e- ratio, smooth 830-day transition with energy-dependent midpoint delay). This is the closest published e+/e- time result and is not cited.
- C26 (electron template set), to complement C24 for the e- denominator.
- C46 (daily-lepton flux estimator and background treatment) for the lepton-specific form of the estimator; the answer cites the proton/nuclei analogues C43 and C49 instead.
