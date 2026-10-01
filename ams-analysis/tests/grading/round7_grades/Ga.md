# Round 7 grades, grader Ga (T05, T08)

Grader: Opus, independent of the answerer (Sonnet). Graded only from the rubric in
`references/tests-and-examples.md` ("Scoring and evaluation rules", T05/T08 entries), the prompts in
`tests/grading/round5.md`, and `data/claims.json` / `data/sources.json`. No other answers or grades were read.

| Test | Sample | Score /10 | Blocking failure |
|---|---|---|---|
| T05 | C | 8 | none |
| T05 | D | 9 | none |
| T08 | C | 10 | none |
| T08 | D | 10 | none |

Subtotal: 37/40 = 92.5%.

Dimensions: SC = scientific_correctness, AS = ams_specificity, UV = uncertainty_and_validation,
SD = source_discipline, US = usefulness.

---

## T05_C: 8/10 (SC 2, AS 1, UV 2, SD 1, US 2). Blocking failure: none

### Claim and number check

| Quoted in answer | Ledger | Verdict |
|---|---|---|
| C31: public AMS flux papers correct migration by unfolding | C31 (S06, proton, 1 GV-1.8 TV, full-text, numeric allowed): "iterative unfolding correcting bin-to-bin migration" | OK |
| C30: migration correction about +25% to -21% across the range, phosphorus, "different species, only illustrates scale" | C30 (S15, P flux): +25% at 3 GV ... -21% at 1.2 TV; numeric allowed | OK, scope labeled correctly |
| C31, C20: R > 1.2 x maximum cutoff | C31 (proton), C20 (antiproton) both state 1.2 x maximum cutoff | OK |
| C31, C20: "then vary that factor as a systematic" | Neither C31 nor C20 contains a cutoff-factor variation. It is in C23 (antiproton, 1.2-1.4), C49 (Bartels p/He, 1.0-1.4), C60 (He, 1.0-1.4), C27 (D, 1.0-1.4) | **Mis-attribution**: statement is true for AMS practice but the cited claims do not support it |
| C25, C27 for data/MC efficiency practice | C25 (positron δ data/MC corrections), C27 (D acceptance corrected for data/MC differences) | OK, labeled "for practice"; cross-species but not presented as proton numbers |
| C23, C25: independent sources added in quadrature | C23 four sources added quadratically; C25 quadratic sum of four sources | OK |

No invented cuts, acceptance, livetime or systematic sizes. No AMS number beyond 1.2 (C31) and the scoped C30 percentages.

### Critical requirements
- Background / charge migration: present (item 4, tail-based charge confusion, Invariant 4).
- Conditional efficiencies: present (item 5, named denominators, ordering, combined closure).
- Geomagnetic transmission: present (items 2-3; exposure with transmission, per-rigidity livetime).
- Migration for a steep spectrum: present and prioritized (item 1, response matrix, forward folding).
- Bin centering: present (item 6).
- Covariance: present (item 6 and systematics section).
- Closure: present (injected-slope MC closure with a named trigger).
- Ask for inputs: present.

### Must ask / flag
- Rigidity range: asked. 
- Data vs MC: only indirectly (whether MC spectrum reweighted; data/MC scale factors). The question of data vs MC production consistency is not asked.
- Track configuration: appears only as a stability axis, not asked as an input.
- Hardware era: **absent** (no mention of hardware era, reconstruction/production version or data period).

### Defects
1. (SD) Cutoff-factor variation attributed to C31/C20, which do not contain it; the supporting claims C23/C49/C60/C27 are not cited. Missing the most direct proton-relevant cross-citation C49 (p/He cutoff factor 1.0-1.4, Φ = N/(A ε T ΔR)).
2. (AS) Hardware era, data period and reconstruction/MC production version never asked; track configuration not asked. Two of four must-ask items missing or only implicit.
3. (SD, minor) "Other papers use different scans" is unsourced; C27/C60 would have supported it.
4. (minor) Exposure written with "geomagnetic transmission" but livetime described as including "the fraction of time each rigidity is above the local cutoff", so transmission risks being counted in both; the answer does not say to put it in one place only (it does say so for other effects in item 5).

Missing expected cross-citations: C49 (proton/helium flux estimator and cutoff-factor scan), C23 or C60 for the cutoff variation.

---

## T05_D: 9/10 (SC 2, AS 2, UV 2, SD 1, US 2). Blocking failure: none

### Claim and number check

| Quoted in answer | Ledger | Verdict |
|---|---|---|
| C31: "Public AMS flux papers write the flux as N/(A ε ΔR T), with N corrected for migration by unfolding" | C31 contains unfolding but **not** the estimator formula. The formula is C49 (S41/S47, Bartels-rotation p/He/nuclei, Φ_i = N_i/(A_i ε_i T_i ΔR_i)) | **Mis-attribution** (true statement, wrong claim) |
| C30: P migration +25% at 3 GV, -21% at 1.2 TV, "different species, does not transfer to protons" | C30 exact match | OK, scoped correctly |
| "C31 and C25 context": AMS corrects acceptance for data/MC efficiency differences | C31 does not contain this; C25 is the positron δ correction. Direct support is C27 (D), C60 (He) | **Overloaded citation**, hedged with "context" |
| C31: R > 1.2 x maximum cutoff | C31 | OK |
| C23 and C27: factor varied 1.2-1.4 (antiproton), 1.0-1.4 (deuteron) | C23: 1.2-1.4; C27: 1.0-1.4 | OK, species stated |
| C31: normal detector conditions, pointing within 40° of zenith, ISS outside SAA | C31: live time > 50%, z axis within 40° of zenith, outside SAA. "Normal detector conditions" is in C48/C51/C54, not C31 | Mostly OK; one element borrowed from other claims |
| `scripts/audit_analysis_spec.py` uses `effect_id`, `response.includes`, `estimator.applies` | Verified in script (lines 191-212) | OK |
| `scripts/ams_kinematics.py` "handles the Jacobian" for exact bin-average | Script provides variable-change Jacobian and bin-average factor between variables, not a bin-centering (steep-spectrum) correction | Minor overstatement |

No invented cuts, acceptance, livetime or systematic sizes.

### Critical requirements
All present: background and charge confusion (tail), conditional efficiencies with closures, geomagnetic transmission per bin, migration with steep spectrum and circular MC dependence, bin centering, covariance across bins, MC closure with injected spectra, input requests. The double-count question (what the MC factor contains) is a strong addition.

### Must ask / flag
- Rigidity range: asked. Hardware era: asked. Data vs MC: flagged (same reconstruction/production version and hardware era for data and MC). Track configuration: only as a stability axis, not asked as an input.

### Defects
1. (SD) C31 used for the flux estimator formula and for data/MC acceptance correction, neither of which it contains; C49 (proton estimator, cutoff 1.0-1.4 for p/He) and C27/C60 (data/MC acceptance correction) not cited.
2. (SC, minor) "Livetime ... excludes dead time and prescales": prescaling belongs to trigger efficiency, not livetime.
3. (minor) `ams_kinematics.py` presented as solving the bin-centering issue; it handles variable-change Jacobians.
4. (minor) Track configuration not requested as an input.

Missing expected cross-citations: C49 (most direct proton flux estimator/cutoff scan), C60 or C27 for data/MC acceptance correction.

---

## T08_C: 10/10 (SC 2, AS 2, UV 2, SD 2, US 2). Blocking failure: none

### Claim and number check

| Quoted in answer | Ledger | Verdict |
|---|---|---|
| S08, C06: protons outnumber antiprotons by a large factor, "user-checkable in published sample sizes" | C06 (S08, abstract+metadata, numeric allowed): 3.49x10^5 p̄ and 2.42x10^9 p | OK; no number quoted, no overstatement |
| S08, C22: charge-confusion protons as a template, CC MC checked with 400 GV proton test-beam data | C22 (full-text) exact | OK |
| S08, C22: template fit to negative-rigidity sample; signal template from proton data; e-/π-/CC templates from data and MC | C22 exact | OK |
| S08, C23: iterative unfolding stopped at 0.1% agreement | C23 exact | OK |

No Gaussian estimate confirmed; no invented counts, rejections or widths.

### Critical requirements
- Reject Gaussian-core charge confusion: explicit (item 2, Invariant 4).
- Data-driven tail validation: abundant proton samples, partial-track fits, test beam, extrapolation test.
- MC-only electron subtraction needs control: electron-enriched control region with transfer factor and signal contamination.
- Template fit with finite statistics: Barlow-Beeston nuisances, identifiability, injected-signal closure.
- Correlations with proton denominator: item 4 (cancellation shown not assumed, correlated/partial/independent classification).

### Defects (none score-relevant)
1. (cosmetic) Closing line "I quoted no AMS numbers beyond the source-indexed counts" is inaccurate: no counts were quoted, while 400 GV (C22) and 0.1% (C23) were; both are ledger-backed.
2. (cosmetic) The unfolding requirement in item 4 carries no tag in the body; C23 is cited only in the Sources list.

Optional cross-citations not used: C20 (selection: TRD/TOF/tracker |Z| = 1, 1.2 x cutoff), C65 (review Λ_CC estimator).

---

## T08_D: 10/10 (SC 2, AS 2, UV 2, SD 2, US 2). Blocking failure: none

### Claim and number check

| Quoted in answer | Ledger | Verdict |
|---|---|---|
| S08, C22: CC proton template from MC checked with 400 GV proton test-beam data; "do not present your recipe as AMS practice" | C22 exact | OK |
| S08, C22: template fit to negative-rigidity sample, signal template from proton data, backgrounds from data and MC; not a pure MC subtraction | C22 exact | OK |
| S08, C23: iterative unfolding stopped at 0.1% | C23 exact | OK |

No other AMS numbers. BDT-on-hit-pattern suggestion is consistent with C22's Λ_CC and is labeled [Proposal].

### Critical requirements
All present: Gaussian-core rejection (ranked first, critical), data-driven tail with abundant matter and test beam, tail probability as a nuisance; MC electron subtraction replaced by a template fit with control regions and signal leakage; Barlow-Beeston/Conway finite-template nuisances; p̄/p correlations not assumed to cancel; p̄ vs p interaction differences noted.

### Defects (none score-relevant)
1. (SC, minor) "In the TRD, a sign-confused electron looks exactly like an electron" is muddled: a sign-confused electron leaves the negative sample; the relevant case is a sign-confused positron entering it. Harmless to the conclusions.
2. (minor) Charge sign "from the Tracker/magnet only" tagged [General method]; it is a skill invariant, fine.

Optional cross-citations not used: C20 (selection), C65 (review Λ_CC).
