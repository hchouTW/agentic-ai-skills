# Grades G1: ams-analysis round 5 (T05, T08, T23, T24)

Grader: independent (G1). Rubric: `references/tests-and-examples.md` "Scoring and evaluation rules". Every AMS number, claim ID and source ID in the answers was checked against `data/claims.json` and `data/sources.json`. The `poisson_diagnostics.py` outputs quoted in the answers were re-run.

| Test | Sample | scientific_correctness | ams_specificity | uncertainty_and_validation | source_discipline | usefulness | Total /10 | Blocking failure |
|---|---|---|---|---|---|---|---|---|
| T05 | A | 2 | 1 | 2 | 2 | 1 | 8 | none |
| T05 | B | 2 | 1 | 1 | 1 | 1 | 6 | none |
| T08 | A | 2 | 1 | 1 | 2 | 2 | 8 | none |
| T08 | B | 1 | 2 | 1 | 2 | 2 | 8 | none |
| T23 | A | 2 | 2 | 2 | 1 | 2 | 9 | none |
| T23 | B | 2 | 2 | 2 | 1 | 2 | 9 | none |
| T24 | A | 2 | 2 | 1 | 2 | 2 | 9 | none |
| T24 | B | 2 | 2 | 1 | 1 | 2 | 8 | none |

Suite total: 65/80 (81.3%). That is below the 90% pass bar, even though there are no blocking failures.

## Ledger verification summary

- AMS numbers quoted: only T08_B ("400 GV proton test-beam") and T23_B ("0.99999"). No answer quotes a C## claim ID.
  - 400 GV: supported by C22 (S08, antiproton extraction, 1-450 GV, `numeric_quotation_allowed: true`). The use matches the claim.
  - 0.99999: supported by C21 (S08/S04/S05/S06 detector sections, scope |Z| = 1, `numeric_quotation_allowed: true`) and C69 (S01, "a pre-flight long-duration test result"). The number and paper are right. The context the answer gives is partly wrong (see T23_B).
- Source IDs quoted: S06 (T05_B), S22 (T24_B). S22 is "Search for antihelium in cosmic rays, PLB 461, 387 (AMS-01) 1999" and is used correctly. S06 is PRL 114, 171103 (2015), the proton flux paper. The content T05_B attributes to it is not in the ledger (see T05_B).
- Papers cited by name: PRL 117, 091103 (2016) = S08 (T08_B, T23_B). The attributed content matches C22 and C21.
- Script outputs: `upper-limit --n 0 --b 0 --cl 0.95` returns `upper_limit_on_signal = 2.9957322735539904`, as both T24 answers say. With b > 0 above -ln(alpha), it returns `null` plus a warning. The `coverage` subcommand checks the coverage of the **Garwood** interval only.
- Non-existence claims: C14 (antihelium) and C19 (antideuteron) are INSPIRE, search-limited "not found" results marked "re-check for latest".
- No invented AMS number, cut, acceptance, livetime, candidate count or publication. No rigidity/momentum confusion. No validation of a nonexistent paper. Result: no blocking failures.

## Per-answer defects

### T05_A (8/10)
- **Bin centering is missing.** This is a critical requirement. The answer never discusses the representative abscissa of a bin for a steep spectrum.
- **The must_ask_or_flag items are mostly absent.** It does not ask for or flag the rigidity range, the track configuration (inner-only vs L1/L9 full span), or the hardware era. Data vs MC is covered only indirectly: "effective acceptance with data/MC scale factors" and "MC provenance validation".
- **It is barely AMS-specific.** It states outright: "these are structural requirements from the general flux-measurement methodology, independent of which specific AMS proton analysis". There is no Tracker pattern, no TOF/Tracker |Z| = 1 selection, and no L1/L9 reference.
- **Weakly justified background.** "electron contamination" is listed as a proton-flux background without saying that it would need charge confusion plus a failed e/p rejection to enter a positive-rigidity sample.
- Strengths: it covers charge confusion, conditional efficiencies ("factorization-bias check"), geomagnetic transmission, migration for a steep spectrum, closure (nominal, reweighted and distorted), and covariance ("adjacent bins are correlated").

### T05_B (6/10)
- **Covariance is missing.** This is a critical requirement. The answer lists a "systematic budget" but never mentions bin-to-bin correlations or a covariance matrix.
- **Unsupported source statement:** "public AMS papers, e.g. S06, don't give their internal cuts, efficiencies, or correction factors". Nothing in the ledger backs a statement about what S06 lacks. C05 covers only S06's abstract content, and C21 covers only its detector numbers. The claim that S06 gives no efficiencies or corrections is unverified and probably wrong.
- **Must_ask items are incomplete.** It asks for the rigidity range. It does not ask for the track configuration or the hardware era, and it never asks explicitly about data/MC efficiency corrections.
- **Low AMS specificity:** "none of the above is AMS-specific".
- Strengths: bin-centre convention, MC-spectrum dependence (circularity) of the bin-by-bin factor, conditional efficiencies, the double-counting risk between A_eff and the MC factor, closure, geomagnetic transmission, albedo/secondaries below cutoff, and an offer to run `validate_response.py`.

### T08_A (8/10)
- **No template fit, and finite template statistics are never addressed.** "template fit with finite stats" is a critical requirement. The answer lists "template fit" only as one estimator option ("sideband, template fit, MC-corrected"). It proposes a migration matrix "M(p → p̄)" and never discusses the finite statistics of MC or data templates.
- **The documented AMS method is not referenced.** There is no mention of the S08 template fit in (Lambda_TRD, Lambda_CC) (C22), and no π⁻ background.
- **Unsourced qualitative magnitude:** "will badly underestimate (often by orders of magnitude)". This is acceptable as qualitative, but it is not labelled.
- Strengths: it rejects the Gaussian-core estimate outright, requires data-driven tail validation with partial-track fits, demands a control region and closure test for the MC-only electron subtraction, and requires numerator/denominator correlations for p̄/p ("cancellation must be demonstrated, not assumed").

### T08_B (8/10)
- **Physics error:** "especially at high rigidity where the core is narrow but the tail ... is what actually produces sign flips". This is wrong. At high rigidity, sigma(1/R) is roughly constant, so ΔR/R grows and the Gaussian core itself spreads toward the opposite sign as R approaches the MDR. The core is widest in relative terms at high R, not narrow.
- **Doubtful physics:** "the electron background is largest exactly in the low-rigidity tail region where TRD/ECAL rejection is weakest". TRD e/p rejection degrades at high energy, not low. ECAL is not one of the S08 antiproton extraction variables in C22 (Lambda_TRD, Lambda_CC).
- **Finite template statistics are not addressed.** The answer proposes a template fit but never covers limited template statistics.
- **Citation form:** the answer cites PRL 117, 091103 (2016) by title but gives no S08/C22 ID. The content ("template fit with electron/charge-confusion-proton/pion templates, test-beam-validated charge-confusion MC", "400 GV proton test-beam") matches C22 exactly, so no deduction.
- Strengths: it rejects the Gaussian-core estimate, requires data-driven or test-beam tail validation, notes that the TRD does not separate p̄ from charge-confused p or π⁻, and requires correlation classification for the p̄/p denominator.

### T23_A (9/10)
- **Source discipline:** it labels the content "[Documented — public detector description]" but names no source. C13 and C69 support the content, but neither is cited.
- **Minor:** internal jargon ("cross-subsystem matrix", "geometry support") is unexplained in a minimal answer.
- It is correct and short. It covers side-entry veto, non-nominal events, and the accidental/backsplash inefficiency trade-off measured as an efficiency and not double-counted in acceptance. It quotes no numbers.

### T23_B (9/10)
- **The 0.99999 context is partly wrong:** "the ACC side-entry rejection efficiency is quoted as 0.99999 in the antiproton paper ... This number is context-specific (that analysis's selection)". The number and paper are correct (C21, S08, `numeric_quotation_allowed: true`). But C69 says it is "a pre-flight long-duration test result", not a quantity tied to the antiproton analysis's selection. C21's scope is |Z| = 1, and the answer omits that. No claim ID is given. This does not break the prohibition on an "efficiency number without context", because context is given, but that context is inaccurate.
- **Minor:** the "Failure modes" paragraph slightly exceeds the minimal-answer brief. It is still not a full analysis template.
- Otherwise correct: location in the magnet bore, side-entry and extra-activity veto, backsplash/accidental trade-off as an efficiency, and no role in sign, |Z| or beta.

### T24_A (9/10)
- **The background-only and S+B likelihoods are never written out.** This is a critical requirement. The expected limit is taken "from the background-only model", and FC/CLs with profiled nuisances is named, but the two likelihoods are never stated.
- **Terminology error:** blinding "to avoid look-elsewhere bias on your own analysis choices". That is tuning (experimenter) bias, not the look-elsewhere effect.
- **Thin candidate policy:** the candidate/excess/evidence/discovery policy is dismissed as not applicable for n = 0 ("never a candidate/excess/evidence/discovery claim"). It does not say that thresholds must be predeclared before unblinding in case candidates appear.
- Verified correct: `s_UL = −ln(1 − CL) − b`, and 2.9957 from the script. The shrinking and unphysical behaviour as b grows is correctly described. The flat-prior Bayesian/CLs limit being b-independent at n = 0 is correct. The coverage script is correctly identified as Garwood-only. "no peer-reviewed AMS-02 result for either currently appears in this skill's source index ... needs to be checked" matches C14 and C19. There is no S/sqrt(B), no Gaussian errors, and no invented sensitivity.

### T24_B (8/10)
- **Expected sensitivity is missing.** This is a critical requirement. There is no median expected limit or bands computed before unblinding.
- **Coverage script misapplied:** "Validate the interval's coverage with seeded toys (`scripts/poisson_diagnostics.py coverage`)" is said of the Feldman-Cousins/CLs interval. The script only checks the coverage of the Garwood interval (docstring and help: "seeded toy coverage of the Garwood interval").
- **Source statement stronger than the ledger:** "AMS has not published an antihelium or antideuteron search/limit paper". C14 and C19 record only that INSPIRE searches were search-limited and found nothing, flagged "re-check for latest". The closing section's hedge ("No ... paper is indexed") is correct. The opening sentence is not.
- **The background-only and S+B likelihoods are not written out.** Only "profile likelihood and toys" is named.
- Verified correct: the classical and CLs formulas at n = 0, the script output 2.9957, the S22 identification (AMS-01 1999 limit), `m = |Z||R|/(γβ)` with γ² amplification, the Feldman & Cousins PRD 57, 3873 (1998) reference, and the candidate/excess/evidence/discovery policy with thresholds declared before unblinding.

## Cross-answer defect pattern
1. Critical requirements are dropped unevenly across samples. Each A/B pair covers a different subset:
   - T05: A drops bin centering, B drops covariance.
   - T08: both drop finite template statistics.
   - T24: B drops expected sensitivity; neither states the background-only and S+B likelihoods explicitly.
   Review-type answers also consistently skip the must_ask items for track configuration and hardware era (T05).
2. Source-provenance statements drift beyond the ledger: T05_B on what S06 lacks, T23_B's selection-specific framing of the 0.99999 pre-flight ACC figure, and T24_B's flat "AMS has not published".
3. No answer cites claim IDs even where a claim (C21, C22, C14/C19) directly supports the text.
