# Grades G2: ams-analysis T29-T32 (round 5)

Grader: independent (G2). Rubric: `references/tests-and-examples.md`, section "Scoring and evaluation rules". Every C##/S## ID and every AMS number in the answers was checked against `data/claims.json` and `data/sources.json`. Checker error codes quoted by the answers were grepped in `scripts/`. Quoted reference text was grepped in `references/`.

| Test | Sample | scientific_correctness | ams_specificity | uncertainty_and_validation | source_discipline | usefulness | Total /10 | Blocking failure |
|---|---|---|---|---|---|---|---|---|
| T29 | A | 1 | 2 | 1 | 1 | 1 | 6 | none |
| T29 | B | 1 | 2 | 1 | 1 | 1 | 6 | none |
| T30 | A | 2 | 2 | 1 | 2 | 2 | 9 | none |
| T30 | B | 2 | 2 | 2 | 2 | 2 | 10 | none |
| T31 | A | 1 | 2 | 1 | 2 | 2 | 8 | none |
| T31 | B | 1 | 1 | 2 | 1 | 1 | 6 | none |
| T32 | A | 2 | 2 | 2 | 1 | 2 | 9 | none |
| T32 | B | 2 | 2 | 2 | 0 | 2 | 8 | none |

Suite subtotal for these 8 answers: 62/80 = 77.5%. The pass line is 90%, so these tests fail on score but have no blocking failure.

Note on ams_specificity for T30: the prompt is general covariance and response methodology. Both answers correctly add no AMS numbers and use the skill's own checkers and metadata conventions, so I gave full credit and did not mark them down for leaving out detector detail.

---

## T29_A (6/10)

ID verification:
- C09 and C28 (S12). The ranges ⁴He 2.1-21 GV and ³He 1.9-15 GV for May 2011-Nov 2017 match the ledger. OK.
- C59-C61 (S07). Elemental He over 1.9 GV-3 TV in the first 30 months matches the ledger. OK.
- C86 (S01). The formula `C(R/4 GV)^Δ` with Δ = -0.294 ± 0.004 is correct, and numeric quotation is allowed. **But the answer misstates the claim** (see defect 1).
- S39 is the PDG Review of Particle Physics, so it is the right citation for the ⁴He mass (3.7274 GeV, labeled [General method]). OK.

Defects:
1. The answer misuses C86: "³He/⁴He is itself rigidity/time-dependent above 4 GV per **[Documented, C86, S01]**". C86 and C09 both say the opposite. Above 4 GV the ³He/⁴He ratio is **time-independent**, and the time variation (δ = -0.21 ± 0.02 ± 0.05) is only below 4 GV. The answer inverts the documented scope of a cited claim.
2. The answer leaves out S11/C62, which also measures He to 3 TV over five years. "What AMS *has* published to 3 TV is the **elemental** He flux ... first 30 months" and "Neither documented He measurement's period matches..." present S07 as the only He-to-3-TV result.
3. The brief is missing required sections. It has no selections with conditional denominators, no backgrounds with control regions, no section keeping efficiency, acceptance, livetime and response distinct (this appears only in the self-check prose), no inference section, and no validation plan with metric, threshold and action. The observable decisions for T29 require all of these.
4. It never states the T/A (kinetic energy per nucleon) conversion and what it needs. "state `Z`,`A` on every conversion" is a general reminder and does not address the conversion explicitly.
5. It does not say that S07 is read at main-article level only, which the test requires. It gives the period scope ("first 30 months") but not the reading level.
6. The self-check cannot be verified: "7 warnings (... an unregistered numeric threshold in the selection text)". The brief shown has no selection text, so the audited JSON differs from what the reader sees.
7. There is no explicit [Unknown/needs input] label. Open inputs are listed but not labeled.

Good: the isotope versus elemental flag is correct, the mass-resolution argument (`γ²` amplifying δβ) is correct, the two-regime estimand is marked [Proposal], and subsystem roles are correct (TRD does not give charge sign).

## T29_B (6/10)

ID verification:
- S07/C59-C61. The cutoff factor 1.2 (varied 1.0-1.4), the systematic ledger items, core resolution 9%-64% over 10 GV-2 TV, tails 3%-11% and MDR 3.2 TV all match C59-C61.
- S11/C62. He/C/O to 3 TV over five years matches the ledger.
- The ⁴He mass is labeled [General method]. OK.

Defects:
1. A scientific error: "Whether the ~13+ year span implied by reaching 3 TV statistics needs a time-averaging...". S07, which the answer itself cites, reached 3 TV with 30 months of data. No 13-year span is implied, so this contradicts the answer's own evidence.
2. It mislabels a real double count as a placeholder. The audit found an "`exposure`/`acceptance` overlap in `estimator.applies`", and the answer calls these "'fill this in before running' gaps ... not evidence that the design is wrong". Exposure already contains acceptance, so this is a real design error, and the answer never fixes it.
3. It blurs attribution: "both give worked examples of the selection ... and rigidity-resolution behavior (Gaussian core 9%-64% ..., non-Gaussian tails 3%-11%, MDR 3.2 TV)". The core and tail numbers come only from S07/C61. C62 gives only the MDR and resolution-systematic sizes. No per-number claim ID is given.
4. It embellishes C59: "downward-going single track". C59 says "inner-tracker track". The ledger has no single-track requirement.
5. The brief is incomplete. It says it is "not a full specification" and has no selections section, no background controls, no inference section and no validation plan with metric, threshold and action.
6. It does not say that S07 is read at main-article level only, and it does not name the AMS isotope-resolved reach (C09, up to 21 GV) when it raises ⁴He isolation.

Good: the T/A conversion via a mass-per-nucleon Jacobian with A=4 and the mass is stated, the precedent numbers are explicitly marked non-transferable, rigidity versus momentum (`p = |Z|R`) is stated, and there is a useful open-input list.

## T30_A (9/10)

No AMS numbers. Checker codes `correlation_bound`, `not_psd`, `double_counting.inefficiency` (an f-string in `validate_response.py`), `normalization.truth_sum` and `overflow.lost_probability` exist. The quotes from `inference-and-unfolding.md` are verbatim.

Defects:
1. It never offers the eigenvalue clip as a labeled diagnostic with its effect quantified, which is an observable decision. It only refuses the clip.
2. It does not ask for the response **orientation**, and it does not mention a symmetry check on the covariance. It asks only for the `inefficiency` and `underflow_overflow` fields.
3. The causal link is speculative: "most likely candidate is the response/unfolding regularization, given problem 2". A column sum of 0.85 says nothing about conditioning.
4. The wording is inconsistent. It says `numerical_rank`/`condition_number` "will tell you if this is an over-regularized/degenerate unfolding", but earlier it named *under*-regularization as the source of anticorrelation.

Good: the verdict comes first, it separates round-off from construction error correctly, and it runs both response readings with the correct verdict for each, including the conditional case where the 15% is lost probability outside the tabulated range.

## T30_B (10/10)

No AMS numbers, and it explicitly scopes itself as general method. Minor points that do not cost a point:
- The clip-effect quantification is delegated to the script ("can show the effect of a clip as a labeled proposal") and not shown.
- "very likely being applied twice" is stated before the conditional-matrix exception is fully spelled out, but point 2 covers that exception.

Side note for the skill, not the answer: `references/inference-and-unfolding.md` line 29 says columns sum "to the fraction reconstructed within the selected sample (inefficiency in `A_j`) or to one (inefficiency inside `R`)". That appears inverted relative to `scripts/validate_response.py` (conditional_on_selected means sum = 1, and includes_efficiency means sum = efficiency). T30_B follows the script, which is correct.

## T31_A (8/10)

No AMS numbers. The checker codes quoted (`exposure.decomposed_and_composite`, `correction.double_applied`, `correction.response_and_estimator`) exist in `audit_analysis_spec.py`. The reference quotes were verified.

Defects:
1. It gets the bias direction wrong. It says "Each error makes the flux artificially small" and "All three errors bias the corrected flux the same direction (too low ...), so they won't cancel". An efficiency applied twice in the denominator, and an extra efficiency correction for drift, make the flux **too high**, not too low. The claim that the three effects do not cancel is therefore unsupported.
2. It mishandles the livetime double count. The answer calls it "an extra factor of `T_live`" and argues from livetime being below the calendar interval. It does not point out that dividing by livetime twice leaves the flux with the wrong units (an extra s⁻¹).
3. It does not ask for the user's exposure definition. It asserts the skill's definition and never considers that the user's "exposure" may mean acceptance only, which T31_B catches. Its request for response normalization is partial ("name explicitly which efficiency `response.includes`").

Good: the verdict is blocked with three named defects, each has a single-category fix, the residual after the veto goes into a systematic only (correct), and it names the spec fields `estimator.applies`, `response.includes`, the correction `effect_id`s and `double_counting_checks`.

## T31_B (6/10)

No AMS numbers.

Defects:
1. It allows a borderline form of the prohibited claim: "double-charges the same physical effect unless the efficiency correction is demonstrably for a **different, residual** drift in the runs that survived the veto". Under the skill's one-category rule, the residual after a veto belongs in a systematic, not in a second (efficiency) correction. This leans toward "a veto plus an efficiency correction is acceptable".
2. It alters a quote: "is a time-dependent drift counted as both a veto and a systematic [efficiency correction]?". The inserted bracket changes the meaning of the checklist item quoted from `calibration-mc-systematics.md` (e).
3. The verdict is hedged and not "blocked": "very likely double-counts at least two effects". It gives no concrete per-effect fix (which factor to remove), only a generic ledger instruction.
4. It has little AMS-specific content beyond restating the prompt.

Good: it asks for the exposure definition and catches that acceptance may be missing, it gives the conditional-efficiency and factorization caveat, and it names `corrections`/`effect_id`, `response.includes` and `estimator.applies`.

## T32_A (9/10)

ID verification:
- C48/S42 (the Bartels lepton fluxes are in energy) is correct.
- C27/S13 and C29/S14 (108-day blocks) are correct and explicitly "not a rule".
- C24/S04 and C26/S05 (the 2D template fit in (Λ_TRD, Λ_CC)) are correct. C25 is the estimator claim, so it is tangential.
- C90/S01 (Δt = 830 ± 30 days, energy-independent, t_rev = 1 July 2013 as a stated choice) is correct.
- C45/C52/S43 (wavelet with lag-1 AR Monte Carlo; trial factor not described) is correct.

Defects:
1. A number is quoted without a claim ID: "binning (1.00-41.9 GV, rigidity) **[Documented, S45/S46]**". The ledger claims are C40 and C41 (abstract+metadata), and the test requires claim IDs.
2. The C90 scope is incomplete. It does not say that the fits are in *energy* over 1-21 GeV and that the amplitude is consistent with zero above 20 GeV, which matters for a 5-50 GV design. "not verified beyond the review's own restatement" is inaccurate, because C39 (the S42 abstract) carries the same 830 ± 30 days.
3. There are small inaccuracies. The heading reads "e⁺/(e⁺+e⁻)-style ratio" although the body uses e⁺/e⁻. "the e⁺/e⁻(or similar) time structure" hedges needlessly, since C90 is exactly Φ(e⁺)/Φ(e⁻). The mechanisms given for the annual cycle ("Sun-Earth distance ... geomagnetic and detector thermal") are speculative and unlabeled.

Good: every observable decision is present. That covers per-sign cutoff and exposure, counts per cell, the classification table plus the time×rigidity covariance with a Kronecker test, a predefined band, local and global significance with Gross-Vitells, no Wilks, control series, joint versus separate fits, and the [Unknown] AMS trial factor.

## T32_B (8/10)

Numbers checked against the ledger:
- 1.00-41.9 GV comes from C40/C41.
- 1-50 GeV comes from C39.
- 830 ± 30 days and 1 July 2013 come from C90 and C39.
- Hysteresis below about 8.5 GV comes from C40/C41.
- Positrons modulated more than protons below about 7 GV comes from C41.
- The wavelet with red-noise Monte Carlo comes from C52.

All of these exist in the ledger, so there is no invented number and no blocking failure.

Defects:
1. **It quotes AMS numbers without claim IDs or source IDs**: 1.00-41.9 GV, 1-50 GeV, "Δt = 830 ± 30 days, energy-independent, reversal date fixed at 1 July 2013", "hysteresis below ~8.5 GV", "below ~7 GV". The test's critical requirement is "Documented items only with claim IDs and scope".
2. It overstates verification strength: "all AMS-Collaboration full-text-verified". C39, C40 and C41 are `abstract+metadata`.
3. It makes an uncited documented claim: "27 days = one Bartels rotation — a documented AMS choice of granularity (used for proton/helium/nuclei/lepton Bartels-rotation products)".
4. It paraphrases C40/C41 loosely: "positron/proton-vs-electron hysteresis". The ledger has electron-versus-proton (C40) and electron-versus-positron (C41) hysteresis.

Good: the physics and design are complete. That covers rigidity versus energy flagged as a new combination, per-bin per-sign transmission, the charge-confusion tail as a migration matrix, a predefined band, Gross-Vitells with no Wilks, instrumental controls, the logistic fit correctly kept separate from a periodicity claim, and an explicit list of unknowns.
