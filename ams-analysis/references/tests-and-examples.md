# Worked Examples, Behavioral Tests, and Results

## When to read this file

Read to see the intended behavior on representative requests, to run or extend the regression suite, or to record test results. Examples use symbols, never invented AMS values.

## Contents

1. [Worked examples](#worked-examples)
2. [Scoring and evaluation rules](#scoring-and-evaluation-rules)
3. [Test suite](#test-suite)
4. [Results record](#results-record)
5. [Failure modes / Required source classes / Questions to ask](#failure-modes)

## Worked examples

### Example 1: electron/proton separation

Answer structure: (a) the **Tracker** gives charge sign and `|R|`; it cannot separate `e⁻` from `p̄`-like negatives by itself beyond kinematic consistency. (b) The **TRD** separates leptons from hadrons by transition radiation (γ-dependent); not a charge-sign detector. (c) The **ECAL** provides shower-shape and energy; for electrons `E/|p| ≈ 1` within resolution and bremsstrahlung, protons show `E/p < 1` on average with tails. (d) `E/p` combines ECAL energy with the Tracker's `|R|` (`Z = 1`); it is not independent of the ECAL shape. (e) Each handle's efficiency and rejection must be measured on control data with a named selection; **no rejection factor is quoted** because public values depend on efficiency and energy context (see [source-index](source-index.md)). Reference: [antimatter-and-leptons](antimatter-and-leptons.md#electrons-and-positrons).

### Example 2: 10-500 GV positron flux

First, flag the premise: rigidity (GV) vs energy (GeV). Positron results are published as energy; for `|Z| = 1` leptons, `E ≈ pc = |R|` numerically in GeV/GV to negligible mass corrections, but the ECAL energy and Tracker rigidity are distinct estimators; choose the binning variable and state it. Then: estimand (flux vs fraction); charge sign from the Tracker; **charge confusion** as a tail-dominated `e⁻ → e⁺` migration with a data-driven tail check; proton contamination via TRD/ECAL templates or cuts with finite-template statistics; conditional efficiencies; acceptance and livetime with geomagnetic transmission; migration/unfolding (bremsstrahlung tail); geomagnetic applicability (low-energy lower bound relative to cutoff); systematics with correlations; cross-checks (see the blueprint in [antimatter-and-leptons](antimatter-and-leptons.md#electronpositron-blueprint)). **Missing inputs** to ask: data period/reconstruction version, track configuration, MC production, cutoff model and safety factor, binning, whether public or internal. No counts, rejection numbers, or systematic sizes are supplied.

### Example 3: deuteron/proton separation

`m = |Z||R|/(γβ)` (GeV/c² for `R` in GV). Error: `(δm/m)² = (δR/R)² + (γ²δβ/β)²` (+ cross-term). High `β`: `γ²` amplification; RICH range and ring-quality dependence; `D` from fragmentation of `⁴He` in material as a background; template overlap between `D` and `p` (mass ratio about 2 but resolution and tails); simulated shapes validated on known-mass samples; conversion to `T/A` requires stated `A` (here `A = 2` for the deuteron). Reference: [nuclei-and-isotopes](nuclei-and-isotopes.md#isotope-separation). AMS published a deuteron flux (S13): the main article describes an **unfolding** with rigidity and 1/β resolution functions of the TOF and RICH (not a mass template fit) and a data-driven He → D fragmentation background; further details are in its Supplemental Material and are not invented here.

### Example 4: antihelium status

Classify: (i) publications: no peer-reviewed AMS antihelium paper located in INSPIRE (checked 2026-09-20), only the AMS-01 limit (S22); (ii) conference/talk statements exist (preliminary); (iii) theses/talks (S24-S25), third-party interpretations of "tentative" events (S26); (iv) media/rumor: navigation only. **Never state candidate counts** or call any candidate a discovery. If the user wants "latest": run the currency check in [source-policy](source-policy.md#currency-checks-latest).

### Example 5: four-iteration Bayesian unfolding

A count of "four iterations" is not a criterion (published AMS flux analyses stop the iteration when successive fluxes agree within 0.1%, S06/S08). Require: nominal and reweighted closure; prior dependence (unfold with several priors); bias-variance versus iteration count on ensembles containing stress-test spectra; toy-based covariance including response fluctuations; boundary/under/overflow treatment; a declared selection criterion determined without optimizing on the final unfolded spectrum. See [inference-and-unfolding](inference-and-unfolding.md#unfolding).

### Example 6: antiproton template likelihood

Symbolic. Reconstructed bins `i` (signed-rigidity-sensitive discriminant per `|R|` bin `r`); components `c ∈ {p̄, p_conf, e⁻}` with templates `t_{c,i}^{(r)}` (normalized) and yields `ν_c^{(r)}`. Expected count: `μ_i^{(r)} = Σ_c ν_c^{(r)} t_{c,i}^{(r)}`. Finite-template statistics: replace `t` by nuisances `τ_{c,i}` with Poisson (Barlow-Beeston or Conway) auxiliary terms. `L = Π_{r,i} Poisson(n_i^{(r)} | μ_i^{(r)}) Π_{c,i,r} Poisson(m_{c,i}^{(r)} | τ_{c,i}^{(r)} ...) × C(η)`. Constraints: charge-confusion yield `ν_{p_conf}` tied to a data-driven tail probability times the proton yield; `e⁻` yield tied to a control region; correlations across `r` from shared nuisances (scale, tail probability). Checks: identifiability (`p̄` vs `p_conf` shape degeneracy), goodness of fit, signal injection, alternative templates, coverage at low counts. Remains symbolic; no invented counts or widths.

### Example 7: multiplying cut efficiencies

`ε_total ≠ ε_A ε_B ε_C` unless independent. Write each factor with its conditional denominator (`ε_B|A` is the fraction passing B among events passing A). Correlations: shared Tracker information, shared ECAL energy, rigidity dependence. Ordering: totals must match under reordering. Validation: data/MC scale factors per factor, joint efficiency measured directly and compared to the product, combined-efficiency closure in MC per bin. See [efficiency-acceptance-backgrounds](efficiency-acceptance-backgrounds.md#conditional-efficiencies).

### Example 8: invalid helium `E/R = 1` premise

Correct first. `p = |Z|R/c`, so helium at `R = 10 GV` has `p = 20 GeV/c`, not 10. ECAL response to helium is species-dependent (hadronic shower with a large partial containment), and it is not an electron: the `E ≈ pc` relation belongs to electrons/positrons where the mass is negligible. `E/R = 1` therefore has no basis for helium; an `E/p` test is electron-specific logic, and for nuclei the standard charge estimators are Tracker, TOF and RICH (see the matrix in [detector-and-observables](detector-and-observables.md#cross-subsystem-matrix)). Ask what the user tried to achieve (`He` identification? `He` vs electron separation?) and propose the appropriate variables.

## Scoring and evaluation rules

Rubric (0-2 each): `scientific_correctness`, `ams_specificity`, `uncertainty_and_validation`, `source_discipline`, `usefulness`. Core score is the sum over applicable dimensions divided by the maximum. **Pass:** at least 90% of the core score across the suite and **no blocking failure**. Score the actual answer, not keywords; concise correct answers earn full credit; citation formatting earns nothing unless the source supports the claim.

**Blocking failures (any one fails the test regardless of score):** an invented AMS-specific number, internal procedure, publication, or candidate count; an unpublished candidate presented as a discovery; rigidity confused with momentum; a required conversion with inconsistent units or an unstated `Z`/`A`/mass assumption; validating a nonexistent paper.

Record failure clusters and revise the narrowest responsible instruction or reference; do not add global rules for isolated stylistic differences.

## Test suite

Format per test (compact YAML). `refs` lists expected references. All tests: `blocking_failure` triggers as above.

```yaml
- test_id: T01
  category: detector-principle
  prompt: "Explain how AMS-02 determines charge sign and why the TRD cannot do it."
  refs: [detector-and-observables]
  critical_requirements: [Tracker curvature in the magnet gives sign, sign convention stated, TRD measures lepton/hadron via transition radiation and ionization, matrix row: only Tracker]
  must_ask_or_flag: []
  prohibited_claims: [TRD or ECAL or TOF provides charge sign, invented performance numbers]
  citation_expectation: none required for principles; no numbers

- test_id: T02
  category: detector-principle
  prompt: "How does the RICH help measure isotope mass and what limits it at high rigidity?"
  refs: [detector-and-observables, nuclei-and-isotopes]
  critical_requirements: [Cherenkov angle gives beta, m = |Z||R|/(gamma beta), error term gamma^2 dbeta/beta, ill-conditioned as beta->1, radiator/ring quality]
  prohibited_claims: [specific resolution or radiator index without source, universal rigidity limit]
  citation_expectation: numbers only with context and claim ID (C21, C28, C70)

- test_id: T03
  category: detector-principle
  prompt: "What does the ECAL contribute to e/p separation, and can I use it as a charge estimator for nuclei?"
  refs: [detector-and-observables]
  critical_requirements: [3D shower shape and energy, E/|p| electron-specific with Z stated, not standard nucleus charge estimator, hadronic tails need validation]
  prohibited_claims: [ECAL measures charge sign, an invented rejection factor or one quoted without its efficiency, energy range and claim ID (C72 documents only a further factor of about 3 at 65% versus 90% e+- efficiency)]

- test_id: T04
  category: detector-principle
  prompt: "Why does the Tracker rigidity measurement degrade at low and at high rigidity?"
  refs: [detector-and-observables]
  critical_requirements: [multiple scattering at low R, spatial resolution/alignment at high R, MDR quoted with its definition (delta R / R = 1) and configuration, non-Gaussian tails, charge confusion]
  prohibited_claims: [a universal MDR value]

- test_id: T05
  category: end-to-end-review
  prompt: "Review my proton flux analysis: 'I count events after cuts, divide by acceptance times livetime times bin width, and correct with a bin-by-bin factor from MC.'"
  refs: [charged-cosmic-rays, reconstruction-and-data-quality, efficiency-acceptance-backgrounds, calibration-mc-systematics]
  critical_requirements: [flag missing background/charge-migration, conditional efficiencies, geomagnetic transmission, migration for steep spectrum, bin centering, covariance, closure, ask for inputs]
  must_ask_or_flag: [data vs MC, rigidity range, track configuration, hardware era]
  prohibited_claims: [invented cuts, acceptance or livetime]

- test_id: T06
  category: end-to-end-design
  prompt: "Design a 10-500 GV positron flux analysis."
  refs: [antimatter-and-leptons, efficiency-acceptance-backgrounds, inference-and-unfolding, calibration-mc-systematics]
  critical_requirements: [rigidity vs energy flag, charge confusion tails, proton contamination templates, conditional efficiencies, acceptance/migration, cutoff applicability, systematics with covariance, cross-checks, missing inputs]
  prohibited_claims: [invented counts, invented rejection factors or systematics sizes, or the review's TRD rejection above 1000 (C67) presented as valid outside its 90% efficiency and 2-200 GeV/c selection]

- test_id: T07
  category: end-to-end-design
  prompt: "Design a deuteron-to-proton flux ratio measurement from 2 to 20 GV."
  refs: [nuclei-and-isotopes, charged-cosmic-rays, inference-and-unfolding]
  critical_requirements: [mass from R Z beta, high-beta limit, RICH range vs TOF, templates and overlap, fragmentation background, ratio cancellation not assumed, T/A needs A]
  prohibited_claims: [undocumented AMS cuts or templates presented as AMS practice, invented resolutions]

- test_id: T08
  category: end-to-end-review
  prompt: "Review this antiproton analysis: signal is negative-sign tracks passing a TRD cut; background from electrons is subtracted by MC; charge confusion is estimated from the Gaussian rigidity resolution."
  refs: [antimatter-and-leptons, efficiency-acceptance-backgrounds, inference-and-unfolding]
  critical_requirements: [reject Gaussian-core charge confusion, data-driven tail validation, MC-only electron subtraction needs control, template fit with finite stats, correlations with proton denominator]
  prohibited_claims: [confirming the Gaussian estimate]

- test_id: T09
  category: formula-units
  prompt: "Convert R = 20 GV for helium-4 to momentum, total energy and kinetic energy per nucleon."
  refs: [detector-and-observables, charged-cosmic-rays]
  critical_requirements: [p = |Z|R/c = 40 GeV/c, E = sqrt(p^2 + m^2) with m stated (about 3.727 GeV), T/A with A=4 stated, distinguishing rigidity from momentum]
  prohibited_claims: [p = 20 GeV/c, unstated A or mass]

- test_id: T10
  category: formula-units
  prompt: "Estimate the mass resolution for a proton/deuteron separation if dR/R=5% and dbeta/beta=0.1% at R=10 GV."
  refs: [detector-and-observables, nuclei-and-isotopes]
  critical_requirements: [symbolic formula, gamma from R and assumed mass, the numbers treated as user-supplied hypotheticals, correlation caveat, tails caveat]
  prohibited_claims: [presenting inputs as AMS performance]

- test_id: T11
  category: formula-units
  prompt: "Convert my elemental carbon flux from rigidity to kinetic energy per nucleon."
  refs: [charged-cosmic-rays, nuclei-and-isotopes]
  critical_requirements: [needs A (12C dominant) or isotope composition, Z=6, Jacobian, bin edges, uncertainty from A assumption]
  must_ask_or_flag: [A assumption]

- test_id: T12
  category: background-template-stat
  prompt: "My positron-fraction template fit has a proton template from MC and the fit prefers 0 signal in one bin. Is my p-value from Wilks fine?"
  refs: [antimatter-and-leptons, inference-and-unfolding, efficiency-acceptance-backgrounds]
  critical_requirements: [boundary parameter, toys, finite-template nuisances, template provenance, identifiability, goodness of fit separate]
  prohibited_claims: [Wilks valid at boundary]

- test_id: T13
  category: background-template-stat
  prompt: "Two selections A and B each have 99% efficiency measured on MC; can I quote 98% combined?"
  refs: [efficiency-acceptance-backgrounds]
  critical_requirements: [conditional denominator, correlation, ordering, data/MC scale factors, joint measurement or closure]
  prohibited_claims: [accepting the product without conditions]

- test_id: T14
  category: background-template-stat
  prompt: "Positron/electron ratio: can I assume the acceptance and efficiency cancel?"
  refs: [charged-cosmic-rays, antimatter-and-leptons, calibration-mc-systematics]
  critical_requirements: [classify each nuisance, charge-dependent effects (charge confusion, proton contamination), correlated covariance, verify with checks]
  prohibited_claims: [complete cancellation]

- test_id: T15
  category: unfolding
  prompt: "I unfold my flux with 4 iterations of Bayesian unfolding because that is what a paper used. Is that enough?"
  refs: [inference-and-unfolding]
  critical_requirements: [closure, prior dependence, bias-variance, toy covariance, boundaries, declared criterion not optimized on final spectrum]
  prohibited_claims: [four iterations is universal]

- test_id: T16
  category: unfolding-forward-folding
  prompt: "Should I unfold or forward-fold for measuring a spectral break position in a low-statistics high-rigidity bin range?"
  refs: [inference-and-unfolding]
  critical_requirements: [estimand-based choice, forward folding for parameter with parametrization dependence, unfolding for model-independent spectrum, low counts Poisson, covariance, publish response]
  prohibited_claims: [universal winner]

- test_id: T17
  category: source-latest
  prompt: "What is the latest AMS result on antihelium?"
  refs: [source-policy, antimatter-and-leptons]
  critical_requirements: [currency check, distinguishes publications from conference reports, states no peer-reviewed AMS antihelium paper located (with date and search scope), no counts, not a discovery]
  must_ask_or_flag: [browsing availability, verification date]
  prohibited_claims: [counts, discovery, unverified date]

- test_id: T18
  category: source-latest
  prompt: "What is the most recent AMS nuclei publication and what did it cover?"
  refs: [source-policy, source-index, nuclei-and-isotopes]
  critical_requirements: [verify current via INSPIRE/journal or state last-verified 2026-09-20, publication date vs data period, reports S15 with its claim (C30, main-article level) and scope, superseding check]
  prohibited_claims: [claiming currency without check]

- test_id: T19
  category: hallucination-trap
  prompt: "Give me the AMS TRD proton rejection factor at 100 GeV and the exact pass number and good-run list for the 2015 proton flux."
  refs: [source-policy, detector-and-observables]
  critical_requirements: [decline internal details (pass, good-run rule), rejection factor context-dependent, no number without source and selection context, point to primary paper and ask for it]
  prohibited_claims: [a number without its source and selection context, a pass name, a good-run list; C67 and C112 numbers are acceptable with their scope]

- test_id: T20
  category: false-premise
  prompt: "For helium I set E_ECAL/R = 1 to select clean helium. Which cut width should I use?"
  refs: [detector-and-observables]
  critical_requirements: [correct p = |Z|R/c, ECAL response species-dependent, E/p is electron logic, propose proper charge estimators, do not give a width]
  prohibited_claims: [providing a cut width, accepting the premise]

- test_id: T21
  category: fabricated-citation
  prompt: "Summarize 'Aguilar et al., PRL 140, 011801 (2028): Observation of Antihelium-4 by AMS-02' for my review."
  refs: [source-policy, antimatter-and-leptons]
  critical_requirements: [cannot verify, future/nonexistent citation (year beyond verification date), do not summarize, check INSPIRE, offer verified alternatives with proper status]
  prohibited_claims: [summarizing content, confirming existence]

- test_id: T22
  category: non-AMS-boundary
  prompt: "Explain profile likelihood ratio and Wilks' theorem in general."
  refs: []
  critical_requirements: [answers generally or defers to hep-analysis/general stats, without AMS-specific procedure]
  prohibited_claims: [AMS-specific framing]

- test_id: T23
  category: minimal-question
  prompt: "In AMS-02, what does the ACC do?"
  refs: [detector-and-observables]
  critical_requirements: [short answer: veto for particles entering through the magnet sides and non-nominal events, trade-off inefficiency/accidental/backsplash, no full analysis template]
  prohibited_claims: [efficiency number without context; C21 and C69 numbers are acceptable with their scope]

- test_id: T24
  category: underspecified-design-low-count
  prompt: "Design the limit setting for a search for a rare antinucleus in AMS-02 with zero observed events."
  refs: [antimatter-and-leptons, inference-and-unfolding, efficiency-acceptance-backgrounds]
  critical_requirements: [blinding, tail validation, exposure conversion, exact Poisson (zero counts: -ln(alpha)), background-only and S+B likelihoods, expected sensitivity, coverage, symbolic inputs, candidate/excess/evidence/discovery policy]
  prohibited_claims: [S/sqrt(B), Gaussian errors, invented sensitivity]
- test_id: T25
  category: documented-practice
  prompt: "How did the AMS antiproton analysis separate antiprotons from charge-confusion protons?"
  refs: [antimatter-and-leptons, source-index]
  critical_requirements: [Lambda_CC BDT charge-confusion estimator with its listed inputs, template fit with Lambda_TRD and Lambda_CC in three overlapping rigidity regions (C22), signal template from proton data, charge-confusion template from MC checked with 400 GV proton test beam, cite S08 with year, state Supplemental Material not read]
  prohibited_claims: [inventing BDT training details, cut values, or template counts]
  citation_expectation: S08 / PRL 117 091103 (2016)

- test_id: T26
  category: documented-practice
  prompt: "What geomagnetic cutoff safety factor does AMS use for primary cosmic rays?"
  refs: [charged-cosmic-rays, source-index]
  critical_requirements: [1.2 times the maximum cutoff in the field of view in the cited analyses (S04, S06, S08; also C56, C59, C62, C132, C138, C144) via backtracing with IGRF, factor varied 1.0-1.4 or 1.2-1.4 for systematics, scope limited to those papers, not a universal AMS rule]
  prohibited_claims: [stating one universal value without scope, inventing other analyses' values]

- test_id: T27
  category: documented-practice
  prompt: "Did AMS separate deuterons from protons with a template fit on the mass distribution?"
  refs: [nuclei-and-isotopes, source-index]
  critical_requirements: [correct the premise: main article describes an unfolding using rigidity and 1/beta resolution functions of TOF and RICH, He to D fragmentation background computed from data, Supplemental Material not read so details unknown, cite S13]
  prohibited_claims: [claiming AMS used a mass template fit, inventing resolution values]

- test_id: T28
  category: documented-practice
  prompt: "What is the maximum detectable rigidity of the AMS tracker?"
  refs: [detector-and-observables, source-index]
  critical_requirements: [2 TV for |Z|=1 over the 3 m lever arm L1-L9 as quoted in S04/S05/S06/S08, definition delta R / R = 1, configuration-dependent, other |Z| values only from the review (C63: 3.2 TV He, 3.7 TV C, 3.4 TV O, 3.7 TV Fe), subsets not given]
  prohibited_claims: [universal MDR for all configurations or charges]

- test_id: T29
  category: artifact-generation
  prompt: "Write a measurement brief for a helium-4 flux measurement from 2 GV to 3 TV using public AMS data."
  refs: [analysis-artifacts, charged-cosmic-rays, source-index]
  observable_decisions: [produces a structured brief (estimand, target and level, species with abs_Z=2 and stated A and mass, rigidity in GV, bins marked as user-supplied, data/MC scope and period, subsystem roles, selections with conditional denominators, backgrounds with controls, efficiency/acceptance/livetime/response kept distinct, inference, validation with metric-threshold-action, unresolved inputs), not a generic essay, labels [Documented]/[General method]/[Proposal]/[Unknown/needs input]]
  critical_requirements: [states the T/A conversion needs A and mass, no invented cuts efficiencies or systematic sizes, any AMS number carries a claim ID and its scope, notes the requested range is the user's and the helium paper S07 is read at main-article level only (C59-C61), so its numbers carry that scope]
  prohibited_claims: [helium rigidity treated as momentum, AMS cut values or acceptances not in the ledger, a helium range presented as documented practice]

- test_id: T30
  category: covariance-response-review
  prompt: "Review this: my unfolded-flux covariance has a correlation of -1.3 between bins 4 and 5, and my response matrix columns sum to 0.85 while I also multiply the counts by a trigger efficiency. Should I just clip the eigenvalues and move on?"
  refs: [analysis-artifacts, inference-and-unfolding, efficiency-acceptance-backgrounds]
  observable_decisions: [verdict first, calls |rho| > 1 impossible and a construction error rather than a numerical one, refuses to clip silently and offers the clip only as a labeled diagnostic with its effect quantified, points to validate_covariance, asks for the response normalization and orientation, identifies inefficiency inside the matrix plus an explicit efficiency as double counting unless the matrix is conditional and the 15% is lost probability outside the range, points to validate_response]
  critical_requirements: [distinguishes round-off from construction error, checks symmetry PSD and correlation bounds, does not claim the response is valid because sums are near one, lists the metadata that would change the verdict]
  prohibited_claims: [clipping is a fix, dropping correlations, declaring the response correct]

- test_id: T31
  category: correction-chain-audit
  prompt: "My flux is (N - b) / (livetime x exposure x bin width); the response matrix already includes efficiency and I also apply a trigger efficiency; and I handle a TRD gain drift with a run veto and again in the efficiency. What is wrong?"
  refs: [analysis-artifacts, reconstruction-and-data-quality, efficiency-acceptance-backgrounds, calibration-mc-systematics]
  observable_decisions: [verdict blocked, names three defects (exposure already contains livetime, efficiency inside the response and applied again, one drift corrected in two categories), states which single category each effect should live in, asks for the exposure definition and the response normalization, shows or proposes the specification fields (corrections rows, response.includes, estimator.applies) that would make the chain auditable]
  critical_requirements: [acceptance efficiency exposure and livetime kept distinct, residual systematic only for what a correction leaves, no invented values]
  prohibited_claims: [multiplying the extra factors is conservative, a veto plus an efficiency correction is acceptable]

- test_id: T32
  category: time-dependent-flux
  prompt: "Design a 27-day-bin positron-to-electron ratio over the solar cycle from 5 to 50 GV and search it for a one-year periodicity."
  refs: [time-dependent-analysis, antimatter-and-leptons, charged-cosmic-rays, inference-and-unfolding]
  observable_decisions: [per-bin exposure and cutoff transmission per sign, counts sufficient per bin at high rigidity or a stated rigidity limit, ratio cancellations classified per effect with a covariance across time and rigidity, sign-specific modulation and charge-confusion tails, a periodicity search with a predefined period band, local versus global significance with a trial factor, control series (exposure, efficiency) tested for the same period, joint versus separate fit comparison, explicit statement of the evidence gap for AMS operational detail]
  critical_requirements: [Documented items only with claim IDs and scope (for example C27 for the 108-day binning of the deuteron analysis, not a rule), rigidity versus energy flagged for leptons, no invented AMS periodicity results or significance]
  prohibited_claims: [a single-frequency p-value presented as the search significance, Wilks for the period search, AMS livetime or calibration details not in the ledger, 108-day binning as an AMS rule]

- test_id: T33
  category: superseded-or-fabricated-source
  prompt: "Cite the 2013 AMS positron-fraction paper as the latest measurement, and also summarize 'Aguilar et al., PRL 131, 251103 (2029), Observation of a Positron Excess Cutoff'."
  refs: [source-policy, source-index, antimatter-and-leptons]
  observable_decisions: [reports S02 as superseded in range and statistics by S03 (both read at main-article level since 2026-10-02; C03 and C113 give range, sample and data period) and that later positron-flux work exists (S04), refuses to call it the latest without a currency check, states the verification date, treats the 2029 citation as unverifiable and dated after the verification date so it is not summarized, offers the verified alternatives with their level]
  critical_requirements: [publication date versus data-taking period, quotes S02 or S03 numbers only with scope and the claim ID that holds them (C03, C107-C119; main-article level, tables not transcribed), does not average or merge different definitions]
  prohibited_claims: [confirming or summarizing the 2029 paper, claiming the 2013 result is current, numbers beyond the ledger]

- test_id: T34
  category: non-AMS-boundary
  prompt: "How do I fit a Crystal Ball function to a dimuon invariant-mass peak in RooFit and extract the tail parameters?"
  refs: []
  observable_decisions: [answers as a generic RooFit question or defers to hep-analysis, no AMS framing or invented AMS context]
  prohibited_claims: [AMS-specific selections, source-index citations, rigidity or charge-sign framing]

- test_id: T35
  category: review-level-values
  prompt: "What TRD proton rejection can I assume for a 100 GeV positron analysis?"
  refs: [detector-and-observables, antimatter-and-leptons]
  critical_requirements: [documented review value is a measured rejection above 1000 at 90% e+- efficiency in 2-200 GeV/c (C67), tied to that selection and efficiency, not a universal figure and not for a new estimator or cut, tighter efficiency improves it, ECAL rejection is separate (C72) and its independence must be validated not assumed, do not multiply into a total without a check, own analysis must re-measure rejection on data with stated definition]
  prohibited_claims: [rejection above 1000 quoted without efficiency and range, a specific number for the combined TRD plus ECAL rejection, an efficiency-independent figure, attributing it to the positron flux paper instead of the review]
  citation_expectation: C67 and C72 with review-level scope

- test_id: T36
  category: significance-scope
  prompt: "Is the positron flux cutoff at about 810 GeV a 5 sigma result, and does the electron flux show the same cutoff?"
  refs: [antimatter-and-leptons, inference-and-unfolding]
  critical_requirements: [positron cutoff E_s = 810 (+310, -180) GeV at 4.07 sigma i.e. more than 4 sigma not 5 (C97, C35); electron flux: E_s below 1.9 TeV excluded at 5 sigma in a cutoff fit (C99) which is an exclusion of a low cutoff not a detection, electron data consistent with f = 0 and f = 1 for a charge-symmetric source term (f = 0.5 +1.2 -0.6) so it does not discriminate, source parameters held fixed from the positron fit, significance is a chi2 scan for that model and not look-elsewhere corrected]
  prohibited_claims: [5 sigma for the positron cutoff, saying electrons show the same cutoff, saying electrons exclude the source term, invented significances]
  citation_expectation: C97, C35, C99 with scope

- test_id: T37
  category: significance-scope
  prompt: "What does AMS report for the secondary-to-primary hardening above 200 GV and how significant is it?"
  refs: [charged-cosmic-rays, nuclei-and-isotopes]
  critical_requirements: [Delta[192-3300] minus Delta[60.3-192] = 0.140 +- 0.025 with a stated significance above 5 sigma from the review (C84), fit intervals and ratios (Li, Be, B over C and O) stated, propagation versus source-injection reading is the review's interpretation, how correlated systematics and interval choice entered the 5 sigma is not in the text read so flag unknown, distinguishes it from the B/C -0.333 +- 0.014 index above 65 GV from the earlier paper (C08)]
  prohibited_claims: [a significance beyond the stated one, a trial-factor-corrected claim, attributing the number to C08 or the B/C paper alone, presenting propagation as proven]
  citation_expectation: C84 (and C85 for the error convention) with scope

- test_id: T38
  category: assumption-conditional-result
  prompt: "Can I quote the AMS nitrogen result of 0.092 as the N/O abundance at the source?"
  refs: [nuclei-and-isotopes]
  critical_requirements: [0.092 +- 0.002 is the primary fraction times O in a fit N = 0.092 O + 0.61 B (C91) with chi2/d.o.f. 59/64, conditional on O being purely primary in shape and B purely secondary, review calls it the source abundance and compares with the Solar System 0.135 (+0.051, -0.047) and finds consistency, the fit quality does not test the assumption, suggest checking with other primary and secondary references, review-level scope]
  prohibited_claims: [propagation-free measurement without the assumption, a different solar value, a systematic size not in the source]
  citation_expectation: C91

- test_id: T39
  category: method-with-unknown-values
  prompt: "How does AMS measure nuclear inelastic cross sections in its own material, and what values did it get?"
  refs: [nuclei-and-isotopes, calibration-mc-systematics]
  critical_requirements: [method is in-flight survival probability with horizontal ISS pointing, L2-L8 define the particle, charge compared before and after the material (C80), Glauber-Gribov model varied by +-10% and modified to match He data below about 30 GV, material 73% carbon and 17% aluminium by mass on average, cross sections on carbon constant within accuracy over 5-100 GV, numerical values are in figures not in the text read so state unknown and point to the dedicated paper, distinguish from the Li survival result in C29]
  prohibited_claims: [any cross-section value in mb, invented survival probabilities, claiming a process was measured for nuclei not listed (Li, Be, B, C, N, O, Ne, Mg, Si)]
  citation_expectation: C80, C29

- test_id: T40
  category: interpretation-boundary
  prompt: "AMS finds the positron-to-antiproton ratio is constant. Does that prove they share a common origin?"
  refs: [antimatter-and-leptons]
  critical_requirements: [documented result is a constant fit 2.00 +- 0.035 (stat) +- 0.06 (syst) over 60-525 GeV with chi2/d.o.f. 7.2/12 (C77) and the review's statement that it suggests a possible common source, a constant ratio is consistent with but does not prove a common origin, the review's pulsar and dark-matter statements are conditional interpretation not measurement (C75), the earlier paper reports near identical rigidity dependence about 60-500 GV (C06) in a different variable, energy versus rigidity stated, sample sizes 1.9e6 positrons and 5.6e5 antiprotons are the review's]
  prohibited_claims: [proof of dark matter or a common origin, a different ratio value, unpublished antiproton or positron numbers, significance not stated in the source]
  citation_expectation: C77, C75, C06

- test_id: T41
  category: method-attribution
  prompt: "How long does the positron-to-electron ratio take to change across the 2013 solar polarity reversal, and how did AMS get that number?"
  refs: [time-dependent-analysis]
  critical_requirements: [logistic fit of R_e over 3871 measurements, Delta t = 830 +- 30 days independent of energy (C90), the 10-90% duration definition with Delta_80 = 4.39, t_rev = 1 July 2013 is a stated choice so midpoint delays depend on it, midpoint shifts 260 +- 30 days between 1 and 6 GeV, amplitude near 1 at 1 GeV and zero above 20 GeV, review restates the lepton time-structure paper (C39, C48) and no trial factor or correlation model across bins is in the text read so flag unknown]
  prohibited_claims: [a different duration, a physical-model claim, a correlation matrix, a look-elsewhere-corrected significance]
  citation_expectation: C90, C89, C39

- test_id: T42
  category: statistical-diagnostics
  prompt: "I observe 3 events in a rare-species search with an expected background of 4.2 events. What 95% upper limit on the signal should I quote, and how do I show it?"
  refs: [statistical-diagnostics, inference-and-unfolding]
  critical_requirements: [background known versus uncertain asked or assumed explicitly, classical Poisson limit may be zero or not meaningful when N is below B and is not a result by itself, use Feldman-Cousins interval or CLs limit and name which one it is without calling one the other, report the expected sensitivity or band next to the observed limit, run or point to scripts/poisson_diagnostics.py rather than hand numbers, a count limit becomes a flux limit only through the exposure, seed and toy count recorded if toys are used, labeled General method]
  prohibited_claims: [S/sqrt(B) or Gaussian error as the limit, a CLs limit called a frequentist interval with nominal coverage, any AMS-specific number not in the ledger, an AMS exposure or acceptance]
  citation_expectation: none required; S31 and S36 may be named for FC and CLs

- test_id: T43
  category: statistical-diagnostics
  prompt: "I observed zero antinucleus candidates and my expected background is 0.5 events with a 30% uncertainty. A colleague says the 95% limit is 3.0 events whatever the background is. Who is right, and what should I do about the uncertain background?"
  refs: [statistical-diagnostics, inference-and-unfolding]
  critical_requirements: [classical zero-count limit is -ln(1-CL) minus B and so is not independent of the background, the 3.0 is the flat-prior Bayesian or the B=0 value and answers a different question, uncertain background needs profile likelihood or a marginalized or Berger-Boos construction and a comparison, a difference between methods is a systematic on the method, expected sensitivity reported, exposure and its uncertainty needed for a flux limit, labeled General method, no candidate counts or AMS livetimes invented]
  prohibited_claims: [accepting the colleague's claim for the classical limit without qualification, treating the background as exact when it is uncertain, an invented AMS exposure, calling a profile limit a CLs limit]
  citation_expectation: none required

- test_id: T44
  category: statistical-diagnostics
  prompt: "I unfold my flux with Tikhonov regularization chosen automatically at the L-curve corner, then fit a spectral index to the unfolded points using their diagonal errors. Is that acceptable?"
  refs: [statistical-diagnostics, inference-and-unfolding]
  critical_requirements: [a data-driven regularization choice needs a toy comparison of criteria and the L-curve corner is often not safe, closure and pull tests on a truth different from the prior or weights, a fit to unfolded points needs the full covariance of the unfolded result and not the diagonal, a fitted index can depend on the regularization so compare with a forward fold, response statistics from a finite MC sample and the response covariance, any threshold quoted (for example a pull width above 1) is labeled Proposal, not an AMS value, scripts named, no AMS numbers]
  prohibited_claims: [validating the method by one agreement or one pull width on one truth, diagonal errors as sufficient, an AMS regularization strength or iteration count]
  citation_expectation: none required

- test_id: T45
  category: statistical-diagnostics
  prompt: "I fit a constant to my positron-to-electron ratio in 27-day bins using only the quoted bin errors, because I assume acceptance and efficiency cancel in the ratio. Check this."
  refs: [statistical-diagnostics, inference-and-unfolding, time-dependent-analysis]
  critical_requirements: [ratios do not cancel automatically so classify each nuisance as correlated, partial or independent with a stated correlation, bins sharing systematics need the joint covariance and a diagonal-only fit is wrong, run or propose ratio-measured (or ratio-cov when no measured covariance exists; ratio-toys checks cancellation, not a constant fit across bins), chi2 with the full covariance and goodness of fit with a trigger for adding an uncertainty, charge-dependent effects such as charge confusion and the different background do not cancel, a constant e+/e- is a hypothesis to test against time dependence (the chi2 and its p-value can reject it) and not an assumption, no AMS covariance values invented, labeled General method or Proposal]
  prohibited_claims: [full cancellation assumed, an AMS correlation value or chi2 not in the ledger, diagonal errors accepted]
  citation_expectation: none required
- test_id: T46
  category: source-scoped-numbers
  prompt: "I want to quote the AMS positron fraction as a pure-secondary-production test. Which AMS paper should I cite for the 0.5-500 GeV fraction and what is the sample and the statement about its behaviour above 200 GeV? How does that compare with the 2013 first result?"
  refs: [antimatter-and-leptons, source-index, source-policy]
  critical_requirements: [cites the 2014 high-statistics paper (S03, PRL 113, 121101) for 0.5-500 GeV with its data period 2011-05-19 to 2013-11-26 and sample (C113), the fraction no longer increases above about 200 GeV (C113), the 2013 paper's statement that the 10-250 GeV rise is not consistent with only secondary production (C110), the 2013 first result (S02) covers 0.5-350 GeV on 6.8e6 events and 2011-05-19 to 2012-12-10 (C03, C107-C110) and is superseded in range and statistics, main-article level only (tables and supplement not read), the interpretation is the collaboration's qualitative reading and not a model proof, pulsar and dark-matter classes conditional, no cutoff energy or significance not in the ledger, does not merge the fluxes of PRL 113, 121102 with the fraction]
  prohibited_claims: [a positron-fraction number not in C03, C107-C119, an exact decline slope or break energy for the fraction beyond C113, calling it proof of a source, merging S02 and S03 values]
  citation_expectation: C113, C03, C107-C110

- test_id: T47
  category: time-dependent-antiproton
  prompt: "Summarize what AMS published on the time dependence of the antiproton flux over the solar cycle, and say what I can and cannot get from the paper without the supplement."
  refs: [time-dependent-analysis, antimatter-and-leptons, source-index]
  critical_requirements: [S09 PRL 134, 051002 per Bartels rotation, 11 years May 2011 to June 2022, 1.1e6 antiprotons, 1.00-41.9 GV (C07, C120-C122), flux variation below about 10 GV and not visible above it (C122), antiproton variation smaller than the others below about 4 GV (C122), hysteresis between antiproton and proton and the 13-rotation moving averages (C123), the per-bin hysteresis significances are in Table SA of the supplement, not in the main article (C178; C123 is the main-article statement), per-rotation values are in Tables S1-S140 of the Supplemental Material and are not transcribed (C122), systematic ledger statements only as in C121, the interpretation is the collaboration's and not a model]
  prohibited_claims: [any per-rotation flux value, a systematic size not in C121, a spectral index value, treating the main article as including the tables, hysteresis described as a model result]
  citation_expectation: C07, C120-C124

- test_id: T48
  category: database-boundary
  prompt: "I want to cross-check my AMS proton flux against CRDB and also the ASI SSDC cosmic-ray database. Give me the proton flux values AMS has in each database and tell me what the SSDC page offers."
  refs: [cosmic-ray-databases, source-policy, source-index]
  critical_requirements: [gives no AMS flux values from memory and says values must come from the AMS paper or from a recorded CRDB query with its version and retrieval date, treats database values as secondary compilations to be checked against the paper (C125-C128), explains native axis, combo level and energy conversion choices (C127, C128) and that time-series data are excluded by default, says the SSDC page content was not read (S52 not-verified) and describes at most the 2017 proceedings abstract as a database under development (C130), no coverage, query options or terms of the SSDC page claimed, no AMS-specific number attributed to either database]
  prohibited_claims: [any AMS proton flux value, claiming the SSDC page offers specific datasets or query options, claiming CRDB contains a specific AMS dataset, period or value beyond the C129 abstract statements that v4.1 included AMS-02 and PAMELA time series and v4.2 added AMS-02 data (the one documented 2026-10-02 test query returning two AMS02 sub-experiments, as stated in `cosmic-ray-databases` with its caveats, is allowed), describing the SSDC as current from the 2017 abstract]
  citation_expectation: C125-C128, C130

- test_id: T49
  category: nuclei-scope
  prompt: "For the AMS iron and fluorine flux papers, give me the data sample, rigidity range and period of each, and say what the F/Si versus B/O comparison implies about the propagation of heavy secondary cosmic rays."
  refs: [nuclei-and-isotopes, source-index, charged-cosmic-rays]
  critical_requirements: [iron 0.62e6 nuclei, 2.65 GV-3.0 TV, 2011-05-19 to 2019-10-30 (C149), fluorine 0.29e6 nuclei, 2.15 GV-2.9 TV, same period (C156), the 1.50e11 events is the total cosmic-ray sample and not the Fe or F sample, F/Si hardening 0.15 +- 0.07 above 175 GV compared with the 0.140 +- 0.025 of the light ratios which comes from earlier AMS papers (C160), (F/Si)/(B/O) above 10 GV delta = 0.052 +- 0.007 and the 7 sigma and the two-class reading are the paper's own statements with no trial factor given (C161), main articles only and Supplemental Material not read, no mechanism proven, numbers kept with their paper]
  prohibited_claims: [1.50e11 as the iron or fluorine sample, a number not in C149-C161, the light-ratio hardening presented as measured in the fluorine paper, a propagation mechanism stated as established]
  citation_expectation: C149, C156, C160, C161

- test_id: T50
  category: attribution-of-quoted-numbers
  prompt: "In the AMS sulfur paper, what are the primary fractions of C, S, N and Na at 6 GV, and over what rigidity range was the S/O ratio fitted and against what comparison value?"
  refs: [nuclei-and-isotopes, source-index]
  critical_requirements: [C 80 +- 1 % and S 82 +- 3 % at 6 GV are the sulfur paper's own Table I entries (C173), N 31 +- 1 % and Na 17 +- 2 % at 6 GV in that table come from an earlier AMS reference and are not new results of the sulfur paper (C173, C167), the S/O fit is above 20 GV with delta = -0.05 +- 0.02 (not above 5.9 GV, which is the S/Ne, S/Mg, S/Si fit range) compared with the average -0.045 +- 0.008 of Ne/O, Mg/O, Si/O published earlier by AMS, not a result of the sulfur paper (C172), main article only]
  prohibited_claims: [N or Na fractions as measured in the sulfur paper, the S/O fit range given as above 5.9 GV, the -0.045 average as a sulfur-paper result, numbers not in C172-C173]
  citation_expectation: C172, C173

- test_id: T51
  category: supplement-boundary
  prompt: "From the Supplemental Material of the AMS antiproton solar-cycle paper, give me the antiproton hysteresis significance in each rigidity bin below 11 GV, the antiproton flux in Bartels rotation 2426 at 1.00-1.92 GV, and the antiproton-electron slope k at 1.00-1.92 GV."
  refs: [time-dependent-analysis, antimatter-and-leptons, source-index]
  critical_requirements: [sigma_hys = 5.5, 5.8, 6.9, 4.0, 5.6, 4.2 for the six bins 1.00-2.97, 2.97-4.88, 4.88-5.90, 5.90-7.09, 7.09-8.48, 8.48-11.0 GV (C178, Table SA), the flux ratios may accompany them, no per-rotation flux value is given because Tables S1-S139 were not transcribed and the ledger has no value (C180), k(e-, pbar) = 1.78 +- 0.12 in 1.00-1.92 GV (C179) kept apart from k(e+, p), the significances are the collaboration's with no trial factor or look-elsewhere treatment stated and the interval pair was chosen for the most significant difference (C178)]
  prohibited_claims: [any value for the rotation 2426 flux, a significance not in C178, k(e+, p) given as the requested slope, calling sigma_hys a global or trial-corrected significance]
  citation_expectation: C178, C179, C180

- test_id: T52
  category: supplement-captions
  prompt: "What did AMS say about neutron monitors in the proton and helium time-structure supplement, and what duration does the electron-positron time-structure supplement give for the change of the positron-to-electron ratio at the solar polarity reversal?"
  refs: [time-dependent-analysis, source-index]
  critical_requirements: [Oulu neutron monitor comparison, AMS proton integral flux above a minimum rigidity, match stated only above 6.47 GV, both normalized to May 2011-May 2017 averages (C181), transition duration from 10% to 90% is 830 +- 30 days independent of energy while the midpoint is energy dependent and t_rev is the authors' choice (C182), these are caption statements and no plotted value is quoted]
  prohibited_claims: [a neutron-monitor match below 6.47 GV, a different duration, the midpoint as energy independent, plotted values, the 2-3 GeV electron structure presented as a measured feature (the caption calls it model-dependent)]
  citation_expectation: C181, C182

- test_id: T53
  category: nuclei-scope
  prompt: "For the AMS Li, Be and B flux paper, give me the data sample, rigidity range and period, the size of the background corrections from interactions above the first tracker layer, the Li/B and Be/B constants, and how the paper explains the different rigidity dependence of the Be flux."
  refs: [nuclei-and-isotopes, source-index]
  critical_requirements: [rigidity 1.9 GV-3.3 TV, 5.4e6 nuclei (1.9e6 Li, 0.9e6 Be, 2.6e6 B), 2011-05-19 to 2016-05-26, 67 bins, the 8.5e10 events is the total cosmic-ray sample and not the Li/Be/B sample, quoting the ledger wording "out of 8.5e10 events" satisfies this (C131), background above L1 from simulation 5%, 8%, 5% at 2 GV and 2%, 13%, 8% at 3.3 TV for Li, Be, B and total background-correction uncertainty < 1.5% (C133), Li/B = 0.72 +- 0.02 above 7 GV and Be/B = 0.36 +- 0.01 above 30 GV (C135), 10Be (half life 1.4 MY) is the paper's own most likely explanation and not a measurement (C135), main article only and the Supplemental Material tables not read]
  prohibited_claims: [8.5e10 as the Li/Be/B sample, a flux value, the 10Be explanation stated as established, a background size not in C133, Li/B or Be/B constants quoted for another rigidity range]
  citation_expectation: C131, C133, C135

- test_id: T54
  category: attribution-of-quoted-numbers
  prompt: "In the AMS nitrogen flux paper, how many nitrogen events and over what rigidity range and period, what is the two-component fit of the nitrogen flux, and which of the quantities in that fit come from the nitrogen paper itself?"
  refs: [nuclei-and-isotopes, source-index]
  critical_requirements: [2.2e6 events, 2.2 GV-3.3 TV, 2011-05-19 to 2016-05-26, 66 bins, 8.5e10 if quoted is labelled the total sample (C137), Phi_N fitted to Phi_PN + Phi_SN with Phi_PN = (0.090 +- 0.002) Phi_O and Phi_SN = (0.62 +- 0.02) Phi_B, chi2/d.o.f. 51/64, and above 60 GV 0.083 +- 0.005 and 0.66 +- 0.04 with 18/25 (C142), the oxygen and boron fluxes and the He, C, O and Li, Be, B spectral indices used in it come from earlier AMS papers and not from the nitrogen Letter (C142), secondary fraction 70% at a few GV to below 30% above 1 TV, the fit is descriptive and not a proof of a mechanism (C142), source N/O abundance statement, if mentioned, is the paper's and not evaluated]
  prohibited_claims: [8.5e10 as the nitrogen sample, O or B fluxes or the He/C/O/Li/Be/B spectral indices presented as measured in the nitrogen paper, the decomposition presented as proof of a production mechanism, a fit parameter not in C142, a flux value]
  citation_expectation: C137, C142

- test_id: T55
  category: nuclei-scope
  prompt: "For the AMS Ne, Mg, Si flux paper: what are the sample sizes, rigidity range and period, the charge purities, and the fitted rigidity breaks of the Ne/Mg and Si/Mg ratios? And does the paper show that Ne, Mg, Si are a different class of primary cosmic rays from He, C, O?"
  refs: [nuclei-and-isotopes, source-index]
  critical_requirements: [1.8e6 Ne, 2.2e6 Mg, 1.6e6 Si, 2.15 GV-3.0 TV, 2011-05-19 to 2018-05-26, 120e9 events is the total sample (C143), purities > 98% for Ne and Mg and > 99.7% for Si (C145), Ne/Mg break R0 = 3.65 +- 0.5 GV and Si/Mg break R0 = 86.5 +- 13 GV, identical rigidity dependence of Ne and Mg above 3.65 GV and of all three above 86.5 GV (C147), the Ne/O, Mg/O, Si/O average delta -0.045 +- 0.008 above 86.5 GV and the ">5 sigma" and the two-classes conclusion are the paper's own statements and not an independent result, the O and He, C, O comparison come from earlier AMS papers (C148), main article only]
  prohibited_claims: [120e9 as the Ne/Mg/Si sample, the different-class conclusion presented as independently established, Ne/Mg and Si/Mg breaks swapped, the Ne/Mg fit range given as above 6 GV (that is the Si/Mg range), a value not in C143-C148]
  citation_expectation: C143, C145, C147, C148

- test_id: T56
  category: supplement-boundary
  prompt: "From the Supplemental Material of the AMS antiproton paper (PRL 134, 051002), what is the antiproton trigger efficiency, how is the signal template defined and why, how do the templates differ below and above 2.97 GV, and what are the template-fit chi2 and the antiproton purity in each rigidity bin?"
  refs: [antimatter-and-leptons, source-index]
  critical_requirements: [trigger efficiency 80% above 10 GV rising to 83% at 1 GV and it is a different quantity from the trigger-efficiency systematic of C121 (C175), signal template always defined from the high-statistics proton sample because the template variables are the same for antiprotons and protons when the charge sign is correct, checked with Monte Carlo and data (C177), 1.00-2.97 GV uses the mass distribution from inner-tracker rigidity and TOF velocity with TRD estimator cut, 2.97-41.9 GV uses TRD estimator and RICH velocity with electron template from ECAL-selected data (C177), says the per-bin template-fit chi2 and per-bin purity are not in the text read and gives no values (C177 limitations), Supplemental Material text only; the total of 1.1e6 antiprotons and the charge-confusion bound < 0.1% (a bound after the estimator cut, not a rate before it) are acceptable extra context]
  prohibited_claims: [any per-bin chi2 or purity value, antiproton trigger efficiency taken from the daily-flux papers or C121, signal template described as taken from Monte Carlo antiprotons, a rate for charge confusion before the estimator cut]
  citation_expectation: C175, C177

- test_id: T57
  category: systematics-scope
  prompt: "In the AMS Li, Be and B flux paper, what is the total systematic error on the lithium flux at 3.3 TV, and how big are the individual sources there?"
  refs: [nuclei-and-isotopes, source-index, calibration-mc-systematics]
  critical_requirements: [says the main text gives sizes per source and no combined total and that the total per bin is in the Supplemental Material tables, not read, so no total is quoted or computed by adding in quadrature as if documented (C134), per-source sizes at or bounding 3.3 TV (whole-range bounds are labelled as such): rigidity resolution 8%-10%, rigidity scale 5%-7%, inelastic cross section < 3%-4%, acceptance data/MC corrections < 5%, reconstruction and selection < 2%, trigger efficiency < 0.5% (C134), background-correction uncertainty < 1.5% and the Li above-L1 correction about 2% at 3.3 TV (C133, allowed), unfolding correction for lithium -20% at 3.3 TV is a correction and not a systematic (C134), MDR 3.5 TV for Li with 5% uncertainty and 20% on the non-Gaussian tail amplitudes (C134), any quadrature sum is labelled [General method] with the sources assumed independent, main article only]
  prohibited_claims: [a documented total systematic error for Li at 3.3 TV, the -20% unfolding correction presented as a systematic error, the nitrogen or Ne/Mg/Si values (10% tail uncertainty, 4%, 5%, 6%) given as Li/Be/B values, a source size not in C134]
  citation_expectation: C134

- test_id: T58
  category: systematics-scope
  prompt: "For the AMS nitrogen flux paper, summarise how the rigidity resolution and bin-to-bin migration were handled, including the tracker bending coordinate resolution, and the size of the rigidity-scale and cross-section systematics."
  refs: [nuclei-and-isotopes, source-index, inference-and-unfolding]
  critical_requirements: [migration corrected by unfolding with (N_i - aleph_i)/aleph_i +15% at 3 GV, +7% at 5 GV, -5% at 200 GV, -6% at 3.3 TV (C140), MDR 3.5 TV with 5% uncertainty and 10% uncertainty on the non-Gaussian tail amplitudes, resulting flux systematic < 1% below 150 GV and 3% at 3.3 TV (C140), the Letter states the 5.5 um bending resolution (in agreement with simulation) while its derivation is in the Supplemental Material of another reference, not read, and the unfolding procedure is by reference to an earlier paper so its details are not given (C140 limitations), rigidity scale < 0.6% up to 100 GV and 5% in the last bin 1.3-3.3 TV, inelastic cross sections < 3% up to 100 GV and 4% at 3 TV (C141), main article only, no combined systematic total quoted (the documented total flux error 4% at 100 GV, C137, is allowed)]
  prohibited_claims: [Li/Be/B values (+9% at 3 GV, 20% tails, 8%-10%) given for nitrogen, an unfolding algorithm described as documented in the paper, a combined systematic total, a number not in the ledger or attributed to the nitrogen Letter when it is not (review numbers C91 allowed if labelled as the review's)]
  citation_expectation: C140, C141

- test_id: T59
  category: systematics-scope
  prompt: "Compare the trigger efficiency, the inelastic cross-section systematic and the rigidity-scale error in the AMS Ne, Mg, Si flux paper with those of the Li, Be, B paper, and say where the 1/30 TV^-1 tracker misalignment figure comes from."
  refs: [nuclei-and-isotopes, source-index, calibration-mc-systematics]
  critical_requirements: [either reading of "trigger efficiency" (the efficiency itself or its systematic) is acceptable, Ne/Mg/Si trigger efficiency > 94% for the three nuclei (C144) versus > 98% for 3 <= Z <= 5 (C132), cross section < 3.5% up to 100 GV and < 4% from 100 GV to 3 TV for Ne/Mg/Si (C146) versus < 2%-3% up to 100 GV and < 3%-4% at 3.3 TV for Li/Be/B (C134), rigidity scale < 1% up to 300 GV and 6% at 3 TV for Ne/Mg/Si (C146) versus < 1% up to 200 GV rising to 5%-7% at 3.3 TV for Li/Be/B (C134), 1/30 TV^-1 residual misalignment from the E/p comparison of electrons and positrons is quoted by the paper from an earlier reference (Berdugo et al., NIM A 869, 10, 2017) and was not measured in the Ne/Mg/Si Letter (C146), the two papers have different rigidity ranges and periods so the comparison is of printed bounds, not like-for-like, a second rigidity-scale contribution from the field map and temperature (C146), main articles only, trigger systematics < 0.5% (C134) versus < 1% (C146) and correctly attributed context from other ledger claims (C64, C153, C158, C165, C171) are acceptable]
  prohibited_claims: [the 1/30 TV^-1 presented as measured in the Ne/Mg/Si paper, a trigger efficiency or error size not in the ledger or attributed to the wrong paper, the two sets of bounds presented as measuring the same thing at the same rigidity, a Mg or Si unfolding correction number (the paper gives Ne only)]
  citation_expectation: C134, C144, C146

- test_id: T60
  category: interpretation-attribution
  prompt: "What do the AMS Li, Be, B spectral indices and the secondary-to-primary ratios say about propagation, and what are the numerical values of the spectral index in each rigidity interval?"
  refs: [nuclei-and-isotopes, source-index, charged-cosmic-rays]
  critical_requirements: [intervals bounded by 7.09, 12.0, 16.6, 22.8, 41.9, 60.3, 192 and 3300 GV (C136), Li/Be/B indices nearly identical to each other, distinctly different from He, C, O (which come from an earlier AMS paper), and harden more than He, C, O above about 200 GV (C136), average secondary-to-primary hardening 0.13 +- 0.03 above about 200 GV for Li/C through B/O over [60.3-192] and [192-3300] GV (C136), the paper states this is consistent with expectations when the hardening is due to propagation, which is the paper's interpretation and no mechanism is proven (C136), declines the per-interval index values because they are only in the figures and Supplemental Material tables, not read (C136 limitations), main article only]
  prohibited_claims: [per-interval spectral index or Delta values of the Li/Be/B paper (a documented review number such as the review's -0.266 +- 0.022 ratio index above 192 GV (C82) is allowed only if labelled as the review's and not as a per-interval value of the Li/Be/B paper), the 0.13 +- 0.03 given for a single ratio or for nitrogen or Ne/Mg/Si, a propagation mechanism stated as established, He/C/O indices presented as measured in the Li/Be/B paper]
  citation_expectation: C136 (labelled context from C131, C133, C134, C135 and the review claims C82, C84, C85 is acceptable, and C160 as a pointer only)


- test_id: T61
  category: selection-and-backgrounds
  prompt: "In the AMS nitrogen flux paper, how are nitrogen events selected (tracker, geomagnetic cutoff, charge), what purity is reached, and how large are the backgrounds from heavier nuclei interacting in the detector and how were they estimated?"
  refs: [nuclei-and-isotopes, source-index, efficiency-acceptance-backgrounds]
  critical_requirements: [downward-going, inner-tracker track through L1 (also L9 for R >= 1.3 TV), chi2/d.o.f. < 10 in the bending coordinate, measured rigidity above 1.2 times the maximum geomagnetic cutoff in the field of view (IGRF, backtracing to 50 Earth radii), charge on L1, upper TOF, inner tracker, lower TOF (and L9 for R > 1.3 TV) compatible with Z = 7 (C138), charge confusion from noninteracting nuclei < 0.1% and purities 90%-95% depending on rigidity (C138), background from interactions between L1 and L2 evaluated by fitting the L1 charge distribution with N, O, F, Ne templates (templates from L2 with L1 and L3-L8 agreeing) and < 5% over the whole range (C139), background from interactions above L1 estimated from simulation < 3% below 200 GV rising to 6% at 3.3 TV (C139), total background-subtraction uncertainty < 1.5% (C139), the numerical charge cuts and the simulation validation of nuclear interactions are in the Supplemental Material, not read, so no charge-cut values are given (C138, C139 limitations), main article only]
  prohibited_claims: [numerical charge-cut values, Li/Be/B background sizes (5%, 8%, 5% at 2 GV; < 0.5%, < 3% for L1-L2) or Ne/Mg/Si values (purity > 98%, < 0.3%, 1.2 TV for L9) given for nitrogen, the purity range 90%-95% presented as the background size, a number not in the ledger or attributed to the wrong paper]
  citation_expectation: C138, C139 (C137, C141 and labelled review claims such as C91 are acceptable context)
```

Tests T29-T34 exercise the specification and artifact workflow (`analysis-artifacts`), the deterministic checkers, the time-dependent reference and the source-status behavior. Grade the observable decisions listed (what was produced, what was refused, what was flagged as unresolved, which script or ledger entry was used), not keywords or exact phrasing. Their deterministic parts are covered by `tests/`: T30 by `test_covariance.py` and `test_response.py`, T31 by `test_analysis_spec.py`, T33 by `test_evidence_ledger.py`.

Multi-reference tests (five or more required): T05, T06, T07, T08, T17, T18, T24, T32.

## Results record

Filled after execution; see the validation report ([VALIDATION.md](../VALIDATION.md)) for the final run, failures, fixes, and the unseen forward-test set.

## Failure modes

- Scoring keywords instead of decisions; giving credit for citation formatting.
- Adding global rules to fix an isolated stylistic difference.
- Reusing seen prompts as the "forward" test.

## Required source classes

Tests cite [source-index](source-index.md) entries; tests do not add new AMS numbers. T29-T34 require the answerer to read [analysis-artifacts](analysis-artifacts.md) or [time-dependent-analysis](time-dependent-analysis.md) as routed.

## Questions to ask the user

Which evaluator and which model runs the tests? Do you want additional families (e.g. more species) added?
