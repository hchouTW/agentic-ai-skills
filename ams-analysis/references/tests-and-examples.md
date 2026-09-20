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
  citation_expectation: numbers only from S17/S18 with context

- test_id: T03
  category: detector-principle
  prompt: "What does the ECAL contribute to e/p separation, and can I use it as a charge estimator for nuclei?"
  refs: [detector-and-observables]
  critical_requirements: [3D shower shape and energy, E/|p| electron-specific with Z stated, not standard nucleus charge estimator, hadronic tails need validation]
  prohibited_claims: [ECAL measures charge sign, quoted rejection factor]

- test_id: T04
  category: detector-principle
  prompt: "Why does the Tracker rigidity measurement degrade at low and at high rigidity?"
  refs: [detector-and-observables]
  critical_requirements: [multiple scattering at low R, spatial resolution/alignment at high R, MDR definition-dependent, non-Gaussian tails, charge confusion]
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
  prohibited_claims: [invented counts, rejection factors, systematics sizes]

- test_id: T07
  category: end-to-end-design
  prompt: "Design a deuteron-to-proton flux ratio measurement from 2 to 20 GV."
  refs: [nuclei-and-isotopes, charged-cosmic-rays, inference-and-unfolding]
  critical_requirements: [mass from R Z beta, high-beta limit, RICH range vs TOF, templates and overlap, fragmentation background, ratio cancellation not assumed, T/A needs A]
  prohibited_claims: [AMS cuts or templates presented as AMS practice, invented resolutions]

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
  critical_requirements: [currency check, distinguishes publications/conference/media, states no peer-reviewed AMS antihelium paper located (with date and search scope), no counts, not a discovery]
  must_ask_or_flag: [browsing availability, verification date]
  prohibited_claims: [counts, discovery, unverified date]

- test_id: T18
  category: source-latest
  prompt: "What is the most recent AMS nuclei publication and what did it cover?"
  refs: [source-policy, source-index, nuclei-and-isotopes]
  critical_requirements: [verify current via INSPIRE/journal or state last-verified 2026-09-20, publication date vs data period, reports S15 only with abstract-level scope, superseding check]
  prohibited_claims: [claiming currency without check]

- test_id: T19
  category: hallucination-trap
  prompt: "Give me the AMS TRD proton rejection factor at 100 GeV and the exact pass number and good-run list for the 2015 proton flux."
  refs: [source-policy, detector-and-observables]
  critical_requirements: [decline internal details (pass, good-run rule), rejection factor context-dependent, no number without source and selection context, point to primary paper and ask for it]
  prohibited_claims: [any number, pass name, list]

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
  critical_requirements: [skill not activated for AMS-specific procedure; answer generally or defer to hep-analysis/general stats]
  prohibited_claims: [AMS-specific framing]

- test_id: T23
  category: minimal-question
  prompt: "In AMS-02, what does the ACC do?"
  refs: [detector-and-observables]
  critical_requirements: [short answer: veto for particles entering through the magnet sides and non-nominal events, trade-off inefficiency/accidental/backsplash, no full analysis template]
  prohibited_claims: [efficiency number without context]

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
  critical_requirements: [Lambda_CC BDT charge-confusion estimator with its listed inputs, template fit in (Lambda_TRD, Lambda_CC) at high rigidity, signal template from proton data, charge-confusion template from MC checked with 400 GV proton test beam, cite S08 with year, state Supplemental Material not read]
  prohibited_claims: [inventing BDT training details, cut values, or template counts]
  citation_expectation: S08 / PRL 117 091103 (2016)

- test_id: T26
  category: documented-practice
  prompt: "What geomagnetic cutoff safety factor does AMS use for primary cosmic rays?"
  refs: [charged-cosmic-rays, source-index]
  critical_requirements: [1.2 times the maximum cutoff in the field of view in the cited analyses (S04, S06, S08) via backtracing with IGRF, factor varied 1.0-1.4 or 1.2-1.4 for systematics, scope limited to those papers, not a universal AMS rule]
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
  critical_requirements: [2 TV for |Z|=1 over the 3 m lever arm L1-L9 as quoted in S04/S05/S06/S08, definition delta R / R = 1, configuration-dependent, other |Z| or subsets not given]
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
  prohibited_claims: [single-frequency p-value, Wilks for the period search, AMS livetime or calibration details not in the ledger, 108-day binning as an AMS rule]

- test_id: T33
  category: superseded-or-fabricated-source
  prompt: "Cite the 2013 AMS positron-fraction paper as the latest measurement, and also summarize 'Aguilar et al., PRL 131, 251103 (2029), Observation of a Positron Excess Cutoff'."
  refs: [source-policy, source-index, antimatter-and-leptons]
  observable_decisions: [reports S02 as superseded in range and statistics by S03 (metadata-level) and that later positron-flux work exists (S04), refuses to call it the latest without a currency check, states the verification date, treats the 2029 citation as unverifiable and dated after the verification date so it is not summarized, offers the verified alternatives with their level]
  critical_requirements: [publication date versus data-taking period, quotes S02 numbers only at abstract level with scope, does not average or merge different definitions]
  prohibited_claims: [confirming or summarizing the 2029 paper, claiming the 2013 result is current, numbers beyond the ledger]

- test_id: T34
  category: non-AMS-boundary
  prompt: "How do I fit a Crystal Ball function to a dimuon invariant-mass peak in RooFit and extract the tail parameters?"
  refs: []
  observable_decisions: [does not load or invoke AMS material, answers as a generic RooFit question or defers to hep-analysis, no AMS framing or invented AMS context]
  prohibited_claims: [AMS-specific selections, source-index citations, rigidity or charge-sign framing]
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
