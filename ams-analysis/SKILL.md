---
name: ams-analysis
description: Use for the Alpha Magnetic Spectrometer (AMS-02) on the ISS - its Tracker/permanent magnet, TOF, TRD, ECAL, RICH and ACC; rigidity/charge/velocity/mass observables; and AMS-style charged cosmic-ray analyses (proton/He/nuclei fluxes, B/C-type ratios, positron/electron, antiproton, antihelium/antideuteron searches, deuteron/isotope separation). Covers AMS-specific selections, data quality, efficiency, acceptance, backgrounds, charge confusion, template fits, unfolding, systematics, likelihoods, time-dependent (solar-cycle, periodicity) analyses, structured analysis specifications and formal reviews, and source/"latest result" verification. Not for generic HEP, generic statistics, or other experiments unless the question is tied to AMS.
---

# AMS-02 Detector and Physics Analysis

Guide realistic AMS-02 detector and charged-cosmic-ray analysis work while separating **documented facts** (public AMS sources), **general methods** (textbook/PDG/statistics literature), **proposals** (choices you recommend for this analysis), and **unknowns** (internal AMS detail). Scope: public-domain reasoning only. AMS Collaboration internal data, notes, calibration constants, production software, conditions databases, pass names, trigger bits, good-run rules and cuts are **not available here**; never invent them. This skill does not replace collaboration review, blinding, or peer review. For generic ROOT/statistics/detector questions with no AMS tie, do not use this skill; use `hep-analysis` (whose reference 38 is a brief AMS overview that this skill supersedes for depth).

## Routing: read the minimum references

| Request type | Mode(s) | Read (in this order) |
|---|---|---|
| "How does subsystem X / observable Y work?" | 1 Concept | `detector-and-observables` |
| RICH/TOF/TRD/ECAL/Tracker role in a specific species | 1 | `detector-and-observables` + the species file |
| Design/review a proton, He, nuclei flux or B/C-type ratio | 2, 3 | `charged-cosmic-rays`, `reconstruction-and-data-quality`, `efficiency-acceptance-backgrounds`, `calibration-mc-systematics` |
| Positron/electron flux or fraction, e/p separation | 2, 3 | `antimatter-and-leptons`, `efficiency-acceptance-backgrounds`, `inference-and-unfolding` |
| Antiproton, antideuteron, antihelium, rare-event search | 2, 3, 6 | `antimatter-and-leptons`, `inference-and-unfolding`, `efficiency-acceptance-backgrounds` (+ `source-policy` if status is asked) |
| Isotopes, deuteron/proton, Li/Be/B, mass from R and β | 1, 2 | `nuclei-and-isotopes`, `detector-and-observables` |
| Unfolding, response matrix, forward folding | 3, 6 | `inference-and-unfolding`, `efficiency-acceptance-backgrounds` |
| Template fit / likelihood / limit / significance | 6 | `inference-and-unfolding` + species file |
| Cuts, run selection, time stability, MC-data mismatch | 2, 3 | `reconstruction-and-data-quality`, `calibration-mc-systematics` |
| Systematics list, covariance, calibration drift | 3 | `calibration-mc-systematics`, `inference-and-unfolding` |
| "What did AMS measure / latest result / is this paper real?" | 4, 5 | `source-policy`, `source-index`, + species file |
| Unit conversion or quick mass-resolution estimate | 1 | `charged-cosmic-rays` (Variable conversion) or `detector-and-observables` (mass propagation) only; run `scripts/ams_kinematics.py` for the arithmetic |
| Covariance/response/PSD problems | 3, 6 | `inference-and-unfolding`; run `scripts/validate_covariance.py` / `validate_response.py` on supplied matrices |
| Write a measurement brief, specification, ledger or response card; formal verdict-first review of a design | 2, 3 | `analysis-artifacts`, then the species and topic references it points to; run `scripts/audit_analysis_spec.py` |
| Exact Poisson limit or interval numbers, zero-count bound, seeded coverage check | 6 | `statistical-diagnostics` (after `inference-and-unfolding` for the decision) |
| Time-resolved flux or ratio, solar cycle, periodicity, time stability of a flux result | 2, 3, 6 | `time-dependent-analysis`, `charged-cosmic-rays`, `calibration-mc-systematics` |
| Positron fraction vs flux for a model constraint | 4, 6 | `antimatter-and-leptons`, `inference-and-unfolding` |
| Maintainer regression only (contains grading rubrics; not needed to answer users) | - | `tests-and-examples` |

Multi-mode requests load the union. "Species file" means `antimatter-and-leptons` for e±/antiprotons/antinuclei, `nuclei-and-isotopes` for elements/isotopes, `charged-cosmic-rays` for p/He fluxes and ratios; add a second only if the question crosses species. A simple factual question gets a short answer and loads only the one concept reference, plus `source-index` whenever an AMS number, date, or status is quoted (that is the only exception to "one reference"); do not impose the full design outline on it: answer in a few sentences, without response-chain, failure-mode or validation sections unless asked. For a review request, answer verdict-first, then defects in priority order, then the inputs that would change the verdict. `source-index` is the claim-to-source ledger (generated from `data/*.json`); consult it before quoting any AMS number.

## Common workflow (analytical dependency order, not prose order)

`estimand → observable space → data/MC scope → reconstruction → selection → signal/background model → efficiency/acceptance/response → inference → validation → reporting`

Substantial design/review answers normally cover: measurement target; relevant subsystems; reconstruction and selection; signal, backgrounds, controls; efficiency, livetime, acceptance, response; inference and systematic propagation; closure and cross-checks; sources, unknowns and required inputs. **Detect and flag** a proposal that starts from a preferred algorithm (BDT, Bayesian unfolding, template fit) before the estimand and response are defined. Schemas for measurement, selection, background and systematic ledgers are in `efficiency-acceptance-backgrounds` and `calibration-mc-systematics`; use them internally or show them when they clarify. Load `analysis-artifacts` only when a specification, formal artifact or formal review is the deliverable.

## Non-negotiable invariants

1. Rigidity `R = pc/(Ze)` (GV) is not momentum; `p = |Z|R/c`. Energy, kinetic energy, kinetic energy per nucleon, and rigidity are different variables; every conversion states `Z` and `A` (or mass). Sign of `R` follows a stated convention; `|Z|` and charge sign are separate observables from separate subsystems.
2. Charge sign comes from the Tracker/magnet only. TOF, TRD, ECAL and RICH do not measure charge sign; the TRD is never a standalone charge-sign detector.
3. Acceptance, efficiency, exposure and livetime are distinct. Do not multiply conditional efficiencies as if independent, and do not correct one effect in two categories (veto, calibration, efficiency, response).
4. Charge confusion and rare misidentification are **tail** phenomena. Reject any estimate based on the Gaussian core of the rigidity resolution; require tail validation.
5. Ratios and fractions do not cancel acceptance/efficiency/systematics automatically; classify each nuisance as correlated, partial, or independent and verify.
6. Low counts: use Poisson/exact or toy-validated intervals; no automatic `S/sqrt(B)`, Wilks, or Gaussian errors near boundaries or with weak constraints.
7. Never present another experiment's method as AMS practice. Label it a proposal or an analogy.
8. Never turn an unpublished candidate report (e.g. antihelium) into a discovery claim, and never supply candidate counts, cuts, bins, livetimes, acceptances or systematic sizes that a source does not give.
9. Every AMS-specific number quoted must appear in `source-index` with its context (species, range, period, selection); otherwise answer symbolically or qualitatively. General-method numbers (e.g. the zero-count Poisson bound `-ln α`, kinematics from PDG masses) are exempt but must be labeled [General method]. User-supplied numbers are labeled as such.
10. "Reasonable agreement" is not validation: state a metric and a trigger for changing the method or adding an uncertainty.

## Source-verification rule

Label each AMS-specific statement (pure arithmetic and general statistics answers are labeled [General method], with the assumptions stated): **[Documented]** (every such tag carries the claim ID from `source-index`, e.g. [Documented, C35]; describe its evidence only at the claim's own verification level, never as "verified" or "full text" beyond it), **[General method]**, **[Proposal]**, or **[Unknown/needs input]**. For "latest", "current status", "has AMS published X", or any post-2025 claim: check current primary sources (INSPIRE-HEP, journal, ams02.space) when browsing is available, report publication date versus data-taking period, and check for supplements and superseding papers; when browsing is unavailable say so and do not claim currency (this skill's index was last verified 2026-09-20). Cite the claim ID from the claim's own row in `source-index` (not from memory or a neighbouring row) and check that its species, range, period and paper cover the statement; do not extend a claim to sibling papers or other species. Never cite search snippets, and never validate a paper you cannot locate: say it is unverified. Details: `source-policy`.

## Response policy for missing information

Identify only the missing inputs that materially change the answer: data vs MC; species; rigidity/energy range; charge sign; measurement level (detector, object, flux); public vs internal work; target type (flux, ratio, fraction, limit, discovery). Then proceed with explicit assumptions and symbolic quantities (e.g. `N_i`, `ε_i`, `A_i`) instead of asking a long questionnaire. State what evidence would resolve each assumption. If the user supplies internal numbers, use them as user-supplied and label them so.

## Scripts (deterministic checks)

Run from the skill directory with `python3`; each has `--help`, prints JSON, and exits 0 (ok), 1 (defects found), 2 (input unreadable or rejected). None modifies user data. Details: `analysis-artifacts`.

- `scripts/ams_kinematics.py`: [General method] conversions among rigidity, momentum, energies and T/A with explicit `|Z|`, `A`, mass; never AMS performance. State every converted value from the script's output for that exact input (do not scale by hand; `p = |Z|R` for the top edge as well as the bottom).
- `scripts/validate_covariance.py`, `scripts/validate_response.py`: self-consistency of supplied matrices under their declared metadata; a pass is not physical validity.
- `scripts/audit_analysis_spec.py`: audits a JSON analysis specification into errors, warnings, proposals, unresolved inputs. When reviewing a correction chain or suspected double counting without a specification, use its fields (`corrections` with one `effect_id` per effect, `response.includes`, `estimator.applies`; exposure already contains acceptance and livetime) as the checklist and propose them in the answer.
- `scripts/poisson_diagnostics.py`: exact Poisson upper limit, Garwood interval, seeded coverage; classical limit only, known background.
- `scripts/validate_evidence_ledger.py`, `scripts/render_source_index.py`: check `data/sources.json` and `data/claims.json` and keep `source-index` in sync.

## Reference index

| File | Read when |
|---|---|
| [detector-and-observables](references/detector-and-observables.md) | Any subsystem, response chain, observable definition, unit/convention, cross-subsystem matrix |
| [reconstruction-and-data-quality](references/reconstruction-and-data-quality.md) | Objects, matching, cut flow, run/event quality, conditions model, time stability, leakage between samples |
| [charged-cosmic-rays](references/charged-cosmic-rays.md) | p/He/nuclei flux and ratio blueprints, geomagnetic selection, rigidity ↔ kinetic-energy-per-nucleon |
| [antimatter-and-leptons](references/antimatter-and-leptons.md) | e±, positron fraction/flux, antiproton, antideuteron, antihelium, rare-event design |
| [nuclei-and-isotopes](references/nuclei-and-isotopes.md) | Charge ladder, fragmentation, deuteron/He/Li isotopes, mass from R, Z, β |
| [efficiency-acceptance-backgrounds](references/efficiency-acceptance-backgrounds.md) | Conditional efficiencies, acceptance, exposure, background ledgers, template-fit design |
| [inference-and-unfolding](references/inference-and-unfolding.md) | Response model, likelihood, covariance, unfolding vs forward folding, limits, low counts |
| [calibration-mc-systematics](references/calibration-mc-systematics.md) | Calibrations, MC provenance, data/MC validation, systematic ledger, double counting |
| [analysis-artifacts](references/analysis-artifacts.md) | Only for designing or writing a structured specification, a brief/ledger/registry/response card, running the checker scripts, or a formal verdict-first review |
| [time-dependent-analysis](references/time-dependent-analysis.md) | Only for temporal flux or ratio, solar-cycle or charge-sign modulation, periodicity, time stability, joint fits across periods |
| [statistical-diagnostics](references/statistical-diagnostics.md) | Only when exact Poisson limit/interval numbers, the zero-count bound, or a seeded coverage check are needed |
| [source-policy](references/source-policy.md) | Source tiers, ledger schema, "latest" checks, conflicts, unsupported-claim behavior |
| [source-index](references/source-index.md) | Claim-to-source map with dates, tiers, verification level |
| [tests-and-examples](references/tests-and-examples.md) | Worked examples, behavioral tests, rubrics, results |
