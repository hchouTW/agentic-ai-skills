# Round 5 rerun grades (independent grader)

Rubric: references/tests-and-examples.md "Scoring and evaluation rules". Every claim ID and number was checked against data/claims.json and data/sources.json.

| Test | Sample | scientific_correctness | ams_specificity | uncertainty_and_validation | source_discipline | usefulness | Total /10 | Blocking failure |
|---|---|---|---|---|---|---|---|---|
| T29 | C | 1 | 2 | 1 | 1 | 1 | 6 | none |
| T30 | C | 1 | 1 | 2 | 2 | 2 | 8 | none |
| T35 | C | 1 | 2 | 1 | 1 | 2 | 7 | none |
| T36 | C | 1 | 2 | 2 | 2 | 2 | 9 | none |
| T40 | C | 2 | 1 | 2 | 1 | 2 | 8 | none |
| T41 | C | 2 | 2 | 2 | 1 | 2 | 9 | none |
| **Suite** | | | | | | | **47/60 (78%)** | **0** |

The suite is below the 90% pass threshold. There are no blocking failures.

## Claim-ID verification summary

- **Correct as used:** C09 (S12, 4He 2.1-21 GV, 3He 1.9-15 GV, May 2011-Nov 2017, 100M 4He), C30 (P migration +25% at 3 GV / -21% at 1.2 TV, labeled as not He), C35 (S04, PRL 122 041102, ">4σ", 4.07σ), C67 (S01 sec. 1.3, >1000 at 90% e± efficiency, 2-200 GeV/c, lower bound), C77 (2.00 ± 0.035 ± 0.06, 60-525 GeV, χ²/dof 7.2/12), C75 (numeric_quotation_allowed=false, and no numbers are quoted from it), C90 (all numbers: 3871, Δt 830 ± 30 d, Δ80 = 4.39, t_rev 1 July 2013, ρ, τ, 260 ± 30 d, Δt fixed above 6 GeV), C97 (E_s = 810 +310/-180 GeV, six-parameter scan, 4.07σ), C98 (E0 = 42.1 +5.4/-5.2 GeV, 7σ), C99 (41.61-1400 GeV, f = 0.5 +1.2/-0.6, E_s < 1.9 TeV excluded at 5σ).
- **Mis-attributed or mis-scoped:** T29 cites "C59, S07/S11": C59 comes only from S07, and the cutoff-factor scan "1.0–1.4 as a systematic" is in C60, not C59. T35 quotes the S05 "<10⁻³" antiproton background with no claim ID (it is C26). T35 turns C72's "further factor of about 3 when tightening 90%→65%" into "an ECAL-only proton rejection of about a further factor of 3".
- **Expected citations missing:** T40 does not cite C06. T41 does not cite C39/C89 and does not attribute the result to the lepton time-structure paper S42. T29 does not state that S07 was read at main-article level only (C59-C61 scope).

## Per-answer defects

### T29 (6/10)
1. **Critical requirement missed: T/A.** The answer gives `A = 4` and `mass ≈ 3.7274 GeV` but never says that a T/A conversion needs A and the mass. It also never discusses T/A at all.
2. **Critical requirement missed: S07 scope.** It never says S07 is read at main-article level only (C59-C61), so its numbers carry that scope.
3. **Mis-citation.** "[Documented, C59, S07/S11]": C59's only source is S07. Also "(scanned 1.0–1.4 as a systematic)" is C60 content, cited as C59.
4. **Scientific gap: period mismatch not flagged.** "Below ~21 GV, use the S12 isotope-separated flux directly. Above ~21 GV ... built from the total-He flux (S07)". S12 covers May 2011-Nov 2017, while S07 covers the first 30 months. The answer never flags stitching two data periods in a solar-modulated low-rigidity region. It also misses the 2.0-2.1 GV gap below S12's 2.1 GV lower edge.
5. **Unsupported negative claim.** "above that range no public AMS analysis separates ³He from ⁴He" is asserted as [Documented], but no ledger claim supports this completeness statement.
6. **Estimand is internally inconsistent.** The brief treats "public AMS data" as published fluxes, yet it specifies event-level selections, conditional denominators, response matrices and trigger efficiencies. Those cannot be applied to published fluxes. The brief never resolves which kind of input is meant.
7. **Validation lacks metric-threshold-action.** It only says "Each needs a named validation metric/threshold/action (e.g. data/MC efficiency ratio in a control sample)". No threshold or action is given for any check.
8. **Odd choice of scale example.** It uses the phosphorus migration (C30) "as an illustration of scale" when the helium paper's own migration (+15% at 2 GV, -19% at 3 TV, C59) is in the ledger. The example is labeled, so this is not an error.
9. **Label set.** It uses "[Unresolved]" instead of the required "[Unknown/needs input]".
10. **Unverifiable self-audit.** "run through scripts/audit_analysis_spec.py: verdict 'needs work' (0 errors, 4 warnings, 1 proposal, 6 unresolved)". The script exists, but the grader cannot check this output from the answer.

### T30 (8/10)
1. **Confused reading (a) of the column sum.** "the matrix is normalized 'conditional on the selected sample' and 0.85 reflects true inefficiency ... that should already live in your acceptance factor". A matrix conditional on the selected sample would not carry inefficiency. The phrase "should already live in your acceptance factor" also reverses the one-place rule that the answer states later. The test's intended reading is different: double counting occurs unless the matrix is conditional and the 15% is probability lost outside the range. That reading is only partly reached, in point 3.
2. **Symmetry handled as a repair, not a check.** "symmetrize `(C+Cᵀ)/2`, take eigenvalues" is given as a routine step. The answer never asks for an asymmetry check first, and silent symmetrization is itself a repair.
3. **Clip not framed as a diagnostic.** The clip is allowed only after the fixes ("clip it, record the change, and confirm your fit/χ² result is unchanged") and not silently. It is not framed as a labeled diagnostic with the size of the change quantified (for example, Frobenius or eigenvalue shift).
4. **No AMS-specific content.** There is no AMS-specific context, such as how AMS flux papers put trigger efficiency inside A_eff (C59/C95). This is a legitimate generic answer, but ams_specificity = 1.
5. **Covered correctly:** |ρ| > 1 is called a construction error rather than round-off, with the Cauchy-Schwarz argument. The answer points to validate_covariance.py and validate_response.py with orientation/normalization metadata, never declares the response valid, and does not recommend dropping correlations.

### T35 (7/10)
1. **Misdescribed C72.** "The review separately quotes an ECAL-only proton rejection of about a further factor of 3 (independent of TRD) when tightening from 90% to 65%". C72 gives no ECAL rejection value. The factor of about 3 is the further reduction from tightening the e± efficiency, and independence from the TRD is the review's statement for its own samples. The answer states "(independent of TRD)" as fact. It never says that independence must be validated rather than assumed, which is a critical requirement.
2. **Implicit multiplication.** "if you're assuming '>1000' as your total proton rejection ... that's an underestimate of what's achievable with ECAL added" invites combining the two numbers. The answer never warns against multiplying into a total without a joint measurement.
3. **Overreach on transferring the number.** "'above 1000' is a defensible floor to assume for the TRD discriminant alone" and ">1000 at 90% e± efficiency (C67) is a reasonable documented starting assumption for a TRD-only cut at 100 GeV". The test requires that the number not be used for a new estimator or cut. The user's own cut is a new cut, so it must be re-measured on data. The later caveats soften this, but the headline recommendation contradicts them.
4. **Missing claim ID.** "reduces the antiproton background in the negative-rigidity sample to <10⁻³ after the electron cut, per S05" has no claim ID; it should be C26.
5. **Covered correctly:** efficiency and range stated (90%, 2-200 GeV/c); lower bound; the value belongs to the review (S01 sec. 1.3), not to the positron paper; tighter efficiency improves the rejection; data-driven re-validation is required.

### T36 (9/10)
1. **Overreach on the electron cutoff.** "and it is well above the positron's 810 GeV, meaning the electron spectrum is inconsistent with a cutoff as sharp/low as the positron's." The Eq. 9 exclusion (C99) applies to a single power law with an exponential cutoff on the whole electron spectrum. In the same C99 fit, the electrons are consistent with f = 1, that is, with the positron source term including its 810 GeV cutoff added as a component. The sentence contradicts the answer's own point 1 and leans toward the prohibited "electrons exclude the source term".
2. **Loose wording.** "excludes a cutoff as low as 1.9 TeV at 5σ" should read "E_s below 1.9 TeV". "consistent with no cutoff up to ~1.4 TeV" is also loose: the best fit 1/E_s = 0 applies within 41.61-1400 GeV.
3. **Missing caveat.** It does not say that the uncertainty of the fixed source parameters is not propagated in the f = 1 fit (C99 limitation).
4. **Covered correctly:** 4.07σ, not 5σ (C35 with S04 title and PRL number; C97); E_s value and errors; the significance comes from a χ² scan with no look-elsewhere correction; the 5σ is an exclusion, not a detection; f = 0 and f = 1 are both consistent, with f = 0.5 +1.2/-0.6; the E0 = 42.1 GeV 7σ figure is correctly attributed to C98.

### T40 (8/10)
1. **C06 missing.** The answer omits that the earlier antiproton paper reports near-identical rigidity dependence at about 60-500 GV (C06), in a different variable and range.
2. **Energy versus rigidity not stated.** The ratio is quoted in GeV (60-525 GeV) without contrasting it with the rigidity-based statement.
3. **Pulsar statement treated as established.** "explicitly notes antiprotons are not produced by pulsars (ruling out one but not all shared/independent-source scenarios)" treats the review's interpretive statement as an established exclusion. C77 marks the pulsar and dark-matter statements as the review's conditional interpretation.
4. **Scenario (b) not tied to C75.** "both being secondaries from the same cosmic-ray population interacting with the interstellar medium" is offered as a viable reading without noting C75: the review says a spectrum shape similar to the protons is not expected if antiprotons come only from collisions. The point is generic but under-sourced.
5. **Ledger wording presented as a quote.** "the skill's own source ledger flags it directly: 'the constant-ratio result ... does not prove a common origin'" puts the ledger's limitation wording in quotation marks. That is the grader's own ledger, not the paper.
6. **Covered correctly:** C77 numbers exact; "consistent with, does not prove"; C75 used only qualitatively (numeric_quotation_allowed=false respected); no invented significance.

### T41 (9/10)
1. **Attribution to the original paper missing.** The answer never says that the review restates the lepton time-structure paper (S42, PRL 121, 051102). The expected citations C39 (830 ± 30 days in the S42 abstract), C89 and C48 are absent. Everything is attributed to "AMS's collaboration-level fit ... S01 Phys. Rept. review".
2. **Minor wording inconsistency.** "each energy-bin fit had χ²/d.o.f. ≈ 1" and "four fitted parameters per energy bin" are stated before the answer notes that Δt is fixed above 6 GeV. The answer resolves this later, so the effect is minor.
3. **Covered correctly:** all C90 numbers match the ledger. The answer covers the 10-90% definition with Δ80 = 4.39, t_rev as a stated choice with delays depending on it, the midpoint shift of 260 ± 30 d from 1 to 6 GeV, and the amplitude trend. It says the fit is descriptive and not a physical model, and it flags the missing trial factor and cross-bin correlation model as [Unknown/needs input].

## Main defect pattern
The main weakness is source discipline at the boundaries of claims, not invented numbers. Every quoted number matches claims.json, and no blocking failure occurs. The recurring defects are:
- **Missing expected cross-citations:** C06 in T40, C39/C89/S42 in T41, and the S07 main-article scope in T29.
- **Mis-scoped or mis-attributed claims:** C59/C60 and S11 in T29, C72's "factor 3" and independence in T35.
- **Documented results stretched one step too far:** electron "inconsistent with the positron's cutoff" in T36, TRD ">1000" as an assumable floor for a new cut in T35, and a pulsar statement treated as a ruling-out in T40.
