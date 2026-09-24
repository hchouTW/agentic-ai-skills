# Grades G3: T33, T35, T36, T37 (ams-analysis, round 5)

Grader: independent (G3). Ledger checked: data/claims.json, data/sources.json (last_reviewed 2026-09-20/21).

| Test | Sample | scientific_correctness | ams_specificity | uncertainty_and_validation | source_discipline | usefulness | Total /10 | Blocking failure |
|---|---|---|---|---|---|---|---|---|
| T33 | A | 2 | 2 | 1 | 1 | 2 | 8 | none |
| T33 | B | 1 | 2 | 1 | 1 | 2 | 7 | none |
| T35 | A | 2 | 2 | 1 | 1 | 2 | 8 | none |
| T35 | B | 2 | 2 | 2 | 1 | 2 | 9 | none |
| T36 | A | 1 | 2 | 1 | 1 | 2 | 7 | none |
| T36 | B | 1 | 2 | 2 | 2 | 2 | 9 | none |
| T37 | A | 2 | 2 | 2 | 1 | 2 | 9 | none |
| T37 | B | 2 | 2 | 2 | 2 | 2 | 10 | none |

Suite slice: 67/80 = 83.75%. No blocking failure. No invented AMS number found: every quoted number traces to a ledger claim with `numeric_quotation_allowed: true` (C03, C08, C24, C35, C67, C72, C84, C97, C99).

## Ledger verification summary

- S02 = PRL 110, 141102 (2013), abstract+metadata, `superseded_by: [S03]`. C03 (0.5-350 GeV, 6.8e6 e+ and e- events, abstract level). Both T33 answers quote these correctly.
- S03 = PRL 113, 121101/121102/221102 (2014), **metadata-only**. S04 = PRL 122, 041102 and S05 = PRL 122, 101101, both full-text (main article). S46 = PRL 131, 151002 (2023), full-text. S01 = Phys. Rept. 894 (2021), full-text.
- C35 (S04): the positron paper's own article body gives 4.07 sigma; the abstract says "more than 4 sigma". C97 (S01): E_s = 810 (+310, -180) GeV, 4.07 sigma, "the same 4.07 sigma", six-parameter region, no look-elsewhere correction, parametrized source term.
- C99 (S01, Sec. 3, Eqs. 8-9, Figs. 50-51): the source parameters are fixed from the positron fit. f = 0.5 (+1.2, -0.6). The data are consistent with f = 0 and f = 1. E_s < 1.9 TeV is excluded at 5 sigma, which is a delta-chi2 scan for that model and range, "not a claim about all cutoff shapes" and "a limit, not a positive detection".
- C67 (S01, Sec. 1.3): the TRD proton rejection is above 1000 at 90% e+- efficiency in 2-200 GeV/c. This is a lower bound for the stated selection. The rejection improves at 65% efficiency. C72 (S01, Sec. 1.7.3): the ECAL gives a further factor of about 3 at 65% versus 90% efficiency. This is "stated to be independent of the TRD rejection" and "should still be validated in a new analysis". No ECAL rejection value is transcribed.
- C24 (S04) supports the 2D (Lambda_TRD, Lambda_CC^e) template fit after an energy-dependent Lambda_ECAL cut, as used in T35 A/B.
- C84 (S01, Sec. 10): Delta[192-3300] - Delta[60.3-192] = 0.140 +- 0.025, stated as above 5 sigma, for the six ratios Li, Be, B over C and O. How the 5 sigma was computed is marked Unknown. The propagation reading is the review's interpretation. C08 (S10): B/C index above 65 GV = -0.333 +- 0.014 (fit) +- 0.005 (syst), first 5 years. C85: the error-propagation convention for the ratio tables.

## Per-answer defects

### T33_A (8/10)
- **Missing critical requirement (publication date versus data-taking period).** The answer never contrasts publication date with data-taking period. It only says citing it as latest "would misstate the publication timeline".
- **No verification levels on the alternatives.** It does not say S03 is metadata-only. "[Documented]" is applied to the whole supersession paragraph, which includes S03 (a metadata-only row).
- **Unsupported negative assertion:** "the volume/page don't match what AMS actually published in PRL 131 — that volume carried AMS's 'Temporal Structures…' PRL 131, 151002 (2023) [S46], not a paper at page 251103". The ledger does not list every AMS paper in PRL 131, so it cannot establish that page 251103 does not exist. The correct status is "not found / unverifiable", which the answer also says elsewhere, so the two statements are inconsistent in strength.
- **No explicit statement that no live currency check was done.** It cites "this skill's last verification (2026-09-20)" but does not say the 2026-09-20 list (C34/S29) was not re-checked.
- **Attribution slightly beyond the ledger:** "AMS's positron flux paper [S04] and the Phys. Rept. review [S01] report … E_s = 810 (+310, −180) GeV". In the ledger the E_s value appears only in C97 (S01). C35 (S04) records only the significance.
- **Correct:** S02/S03/S04/S05/S01/S46 identifiers and titles; C03 numbers with scope; the 2029 date falls after both today and the verification date; refuses to summarize; the 4.07 sigma versus "more than 4 sigma" split (C35).

### T33_B (7/10)
- **Factual misattribution (scientific_correctness):** "source-term cutoff reported (>4σ, later refined to 4.07σ in the 2021 review)". C35 records that S04's own article body gives 4.07 sigma, and C97 says the review gives "the same 4.07 sigma". Nothing was refined.
- **Unsupported comparative claims:** "The 2021 Phys. Rept. review (Part II) restates these with more precision" and "Phys. Rept. 894 (2021) — seven-year review, restates the cutoff with tighter uncertainty". The ledger has no S04 E_s uncertainty to compare against. C97 says the result is the same.
- **Verification-level error:** the list is headed "What I can offer instead, from verified sources in the index", but S03 (PRL 113 x3) is metadata-only and S02 is abstract+metadata. No levels are given.
- **Missing critical requirement (publication date versus data-taking period).** It says only "misrepresent both the publication date and what AMS currently reports".
- **No claim or source IDs** anywhere, so the ledger link is not auditable. (T33 has no explicit citation_expectation, so this costs only part of the source_discipline score.)
- **Correct:** C03 numbers with scope; "superseded in range and statistics"; an explicit statement that there was no live browsing and the evidence index was last verified 2026-09-20 (good currency handling); PRL 131 = 2023 (S46); refuses to summarize the 2029 paper; asks for a DOI.

### T35_A (8/10)
- **Critical requirement not met (ECAL independence must be validated):** "ECAL adds separate rejection, stated as 'independent of the TRD rejection' in the review". This repeats the review's independence statement without saying it must be validated in a new analysis (C72 limitation). The "do not chain" warning is about the template fit, not about TRD×ECAL factorization.
- **Missing "not for a new estimator or cut":** it says the value applies to "one specific efficiency working point" but never says it does not transfer to a different Lambda_TRD definition or cut.
- **Energy versus momentum not flagged:** "100 GeV falls inside that 2–200 GeV/c range". It maps GeV to GeV/c without noting that the lepton mass is negligible or stating the variable.
- **No claim IDs** (citation_expectation: C67 and C72). The review section (1.3) and review-level scope are stated correctly.
- **Correct:** C67 number with efficiency and range, 65% improvement with no number, factor about 3 from C72 with no absolute ECAL value, the C24 template-fit description, and re-validation on a control sample.

### T35_B (9/10)
- **C72 not cited by ID** (citation_expectation: C67 and C72). C67 appears only at the end ("source-index claim C67").
- **Overclaim:** "that's not in the public record at that granularity". The ledger supports only "not in the sources read", not that it is absent from the public record.
- Minor: "the documented figure you can assume" is worded permissively, although it is conditioned on "the same working point … and the same TRD-alone selection".
- **Correct:** C67 with efficiency, range, lower-bound status and the 65% improvement; momentum ≈ energy stated explicitly; the TRD is not a charge-sign detector (C67 limitation); ECAL factor about 3 with "should be checked, not assumed" (C72 limitation); C24 template fit; the seven-year review period; validation on the user's own control sample.

### T36_A (7/10)
- **Overgeneralized exclusion (scientific_correctness):** "if the electron spectrum has a cutoff at all, it must be above ~1.9 TeV". C99 limits this to a delta-chi2 scan for an exponential-cutoff power law in 41.61-1400 GeV, "not a claim about all cutoff shapes".
- **Stretch:** "the electron and positron spectra are explicitly described as behaving differently in this respect". The review's "distinctly different" statement (C98) concerns magnitudes and energy dependence, not the cutoff specifically.
- **Omits f = 0.5 (+1.2, −0.6)** from the free-f fit (critical requirement). It gives only the f = 1 versus f = 0 comparison.
- **Electron 5 sigma scope not framed** (uncertainty_and_validation): it does not say this is a model-specific Δχ² limit, not look-elsewhere corrected, or that the fixed source parameters mean their uncertainty is not propagated.
- **Unsupported attribution:** "restating … PRL 122, 101101 for electrons". In the ledger the f and E_s tests (C99) are sourced to S01 only.
- **No claim IDs** (citation_expectation: C97, C35, C99).
- **Correct:** 4.07 sigma, not 5; E_s = 810 (+310, −180); six-parameter scan without a look-elsewhere correction; the electron data cannot discriminate; source term fixed from the positron fit; the E_s < 1.9 TeV exclusion is not a detection (implied).

### T36_B (9/10)
- **Overstatement:** "the positron cutoff is a real, fitted feature at 4.07σ". Calling it "real" conflicts with C97, which calls it a parametrized source-term cutoff, "not a spectral break of the data", below 5 sigma and model-dependent. The answer itself says this two paragraphs earlier.
- **Overgeneralized exclusion:** "AMS excludes any electron cutoff energy E_s < 1.9 TeV at 5σ. So on its own, the electron spectrum shows no evidence of a low-energy cutoff at all". C99 says the scan covers one model and range and is not about all cutoff shapes.
- **C35 not cited by ID.** Its content ("5 sigma is not supported", same 4.07 sigma) is paraphrased through C97.
- **Correct:** C97 and C99 with section, equation and figure locators matching the ledger; 0.5-1000 GeV fit range; f = 0.5 (+1.2, −0.6) with no χ² improvement; "neither require nor exclude"; no look-elsewhere correction; source term fixed; Supplemental Material not opened.

### T37_A (9/10)
- **No claim IDs** (citation_expectation: C84, plus C85 for the error convention). The C85 error-propagation convention (which systematics were treated as correlated between numerator and denominator) is not mentioned. Paper and section references are correct: Phys. Rept. 894 Sec. 10, and PRL 117, 231102 = S10.
- Minor notation: "hardens by Δ = 0.140 ± 0.025" labels a difference of indices as Δ. The prose that follows clarifies it.
- **Correct:** 192 GV boundary; intervals 60.3-192 and 192-3300 GV; the six ratios; above 5 sigma as stated; propagation versus injection given as the review's interpretation; "no model predicted" (C84); how the 5 sigma was built flagged as [Unknown/needs input]; the C08 value −0.333 ± 0.014 ± 0.005 above 65 GV correctly separated and attributed to S10.

### T37_B (10/10)
- Minor: "(the review's stated boundary — not a round '200 GV,' …)". The review itself also writes "above about 200 GV" (C84), so the user's phrasing is not wrong.
- Minor: C85 (error convention) and C08 are not cited by ID. The B/C value is given as "≈ −0.333" without its errors (acceptable, since it is used only to warn against conflation).
- **Correct:** C84 and S01 cited with full title; exact formula Δ[192–3300] − Δ[60.3–192] = 0.140 ± 0.025; six ratios; above 5 sigma as the review's statement; correlation and trial construction marked [Unknown/needs input]; interval boundaries are the review's choice; propagation reading is a modelling statement; "earlier, smaller dataset" is consistent with C08 (first 5 years) versus the review's seven years.

## Cross-answer defect pattern
1. **Model-scoped limits stated as universal (T36 A and B):** "must be above ~1.9 TeV" and "excludes any electron cutoff". The C99 limitation ("not a claim about all cutoff shapes") was dropped in both samples. T36_B also calls a sub-5-sigma parametrized cutoff "real".
2. **Claim IDs used unevenly.** The A samples cite no C-IDs in T35, T36 and T37. Secondary expected IDs (C35, C72, C85) are missing even in the B samples. Verification levels (S03 metadata-only) are never shown in T33.
3. **T33 critical requirement "publication date versus data-taking period" is missed by both samples.** T33_B also invents a "refinement" from S04 to S01 (4.07 sigma) that C35 and C97 contradict.
