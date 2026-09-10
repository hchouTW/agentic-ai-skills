# Strengthen Mathematical/Statistical/Computational Reasoning in `academic-papers` — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Give the `academic-papers` skill practical, agent-executable guidance for evaluating and constructing mathematical, statistical, and numerical/computational scientific reasoning — so it can answer "is this result mathematically, statistically, and computationally justified?" — without turning it into a math/stats/CS textbook or duplicating `agile-development`, `hep-analysis`, or `deep-learning`.

**Architecture:** Add three new "verification and auditing" mode references (mirroring the existing pattern of `equation-and-notation-auditing.md`, `claim-evidence-mapping.md`, `reproducibility-auditing.md`) — one each for statistical inference, mathematical reasoning/proof, and numerical/computational methods — and fold the smaller requested capabilities (probability errors, Monte Carlo, scientific computing, computational-experiment-design/circular-validation, symbolic/dimensional reasoning) into those three plus a small extension of the existing equation/notation file. Update `SKILL.md`'s routing and cross-link from the existing reading/claim files so the new material is actually reachable.

**Tech Stack:** Markdown only (no code). Validation uses the bundle's own `scripts/validate_skill_bundle.py` (no new tooling).

**Spec:** `/Users/hchou/Downloads/task_Strengthen_Mathematical_Statistical_and_Computational_Scientific_Reasoning_for_HEP.md`

## Global Constraints

- Do not create `computer-science.md`, a math/stats/CS/HEP textbook, a ROOT manual, or a Python guide (spec §13, §26).
- Do not duplicate general software-engineering guidance already owned by `agile-development` (spec §12, §26) — use the boundary table in Task 3.
- Do not duplicate substantive ML-rigor/analysis-execution content owned by `deep-learning` (`ablation-and-design-review.md`) or `hep-analysis` — this skill covers *recognizing* the issue while reading/writing, not running the study (matches existing `statistics-and-ml-papers.md` and `reproducibility-auditing.md` boundary language).
- Prefer fewer, coherent reference files over one-file-per-bullet-in-the-spec (spec §1, §20) — this plan creates **3** new files, not 5+.
- Every substantial section must change agent behavior (a decision procedure or checklist), never textbook exposition of what a concept *is* (spec §24, §25).
- Preserve existing terminology: `claim-evidence-mapping.md`'s support-verdict language (supported/partially supported/unsupported/unresolved), `scientific-style.md`'s σ-based significance table, `reproducibility-auditing.md`'s scope-and-evidence framing — extend/cross-link, don't restate.
- Never claim a check, test, or repository inspection was performed if it wasn't (spec, Final Report instructions).

---

## Capability Audit (spec §1 — completed by inspecting the actual repo)

| Capability | Existing coverage | Gap | Action |
|---|---|---|---|
| Mathematical reasoning / proof status | `equation-and-notation-auditing.md` covers notation/dimensional consistency and per-step derivation checks | No proof-status taxonomy, no approximation-validity workflow, no counterexample-search guidance anywhere | **Add** `mathematical-reasoning-and-proof.md` |
| Statistical inference | `reading-papers.md` and `scientific-style.md` name look-elsewhere effect, significance language, CI-vs-credible-interval — but only as reading-checklist reminders / prose-phrasing rules, not inference-construction procedures (no likelihood, Wilks/Wald, CLs, nuisance mechanics) | The inference-reasoning layer itself is missing | **Add** `statistical-inference-for-physics.md` |
| Probability / stochastic reasoning | Not covered | Missing | **Fold into** statistical-inference-for-physics.md |
| Numerical methods / convergence / optimization | Not covered | Missing | **Add** `numerical-and-computational-methods.md` |
| Monte Carlo / sampling validation | Only a citation-convention mention ("cite generators/tunes by version") in `citations-and-bibliography.md` | Missing | **Fold into** numerical-and-computational-methods.md |
| Scientific computing (repro envs, seeds, provenance) | `reproducibility-auditing.md` lists seeds/checkpoints as artifacts to *trace during an audit*, not as computing practice itself | Partial | **Fold into** numerical-and-computational-methods.md, with an explicit `agile-development` boundary table |
| Computational experiment design / circular validation | `statistics-and-ml-papers.md` explicitly defers ML rigor to `deep-learning`; `reading-papers.md` has one reading-checklist bullet ("train/test contamination") | Recognition-level only | **Fold into** numerical-and-computational-methods.md, keeping the same delegation pattern |
| Symbolic / dimensional reasoning | `equation-and-notation-auditing.md` already covers dimensions, indices, transpose/conjugate, normalization | Missing explicit convention-vs-error distinction; missing Fourier/phase-space/metric-convention terms | **Extend** equation-and-notation-auditing.md |
| Evidence-strength calibration | `claim-evidence-mapping.md` has a support-verdict taxonomy, not a justified-strength ladder (exact/derived/asymptotic/numerical/empirical/heuristic/speculative) | Partial | **Add ladder inside** mathematical-reasoning-and-proof.md; **cross-link from** claim-evidence-mapping.md |
| HEP-specific statistical practice | `reading-papers.md` names look-elsewhere effect, systematics-itemization, blinding as things to check | Names them, doesn't give the procedure | statistical-inference-for-physics.md covers the procedure; reading-papers.md cross-links to it |

Reuse-first outcome: probability, computational-experiment-design, scientific computing, and symbolic/dimensional reasoning are **not** separate files (spec §20 explicitly allows this). Only the two genuinely uncovered high-priority capabilities (statistical inference, mathematical reasoning/proof) plus numerical methods get new files.

## File Structure

```
academic-papers/
├── SKILL.md                                        (modify: routing + description)
└── references/
    ├── statistical-inference-for-physics.md         (create — Priority 1)
    ├── mathematical-reasoning-and-proof.md          (create — Priority 2)
    ├── numerical-and-computational-methods.md       (create — Priority 3)
    ├── equation-and-notation-auditing.md            (modify: convention-vs-error, units/Fourier/phase-space)
    ├── claim-evidence-mapping.md                    (modify: cross-link evidence-strength ladder)
    └── reading-papers.md                            (modify: cross-link look-elsewhere/systematics/leakage bullets)
```

No other files change. No new scripts, assets, or templates.

---

### Task 1: Create `statistical-inference-for-physics.md` (Priority 1)

**Files:**
- Create: `academic-papers/references/statistical-inference-for-physics.md`

**Interfaces:**
- Consumes: none (new file).
- Produces: section anchors `#entry-questions`, `#likelihood-based-inference`, `#frequentist-inference`, `#bayesian-inference`, `#systematic-uncertainty`, `#common-probability-errors`, `#statistical-claim-calibration` — Task 5 and Task 6 link to these anchors, so keep the exact heading text below.

- [ ] **Step 1: Write the file**

```markdown
# Statistical inference for physics

Use when evaluating or constructing a statistical inference — checking whether a
paper's likelihood, test, interval, or limit is set up and interpreted correctly,
or reasoning through one while drafting a Results/Systematic Uncertainties
section. This is inference *reasoning*, not the fit or limit-setting itself —
use `hep-analysis` (pyhf/Combine/RooStats, cutflows, toy generation) or
`deep-learning` (evaluation-harness design) to actually run the computation.
Cross-references: `claim-evidence-mapping.md` for whether the conclusion follows
from the result; `equation-and-notation-auditing.md` for whether the likelihood's
algebra/dimensions are internally consistent; `scientific-style.md` for how to
phrase the resulting claim once it's calibrated correctly.

## Table of contents
- [Entry questions](#entry-questions)
- [Likelihood-based inference](#likelihood-based-inference)
- [Frequentist inference](#frequentist-inference)
- [Bayesian inference](#bayesian-inference)
- [Systematic uncertainty](#systematic-uncertainty)
- [Common probability errors](#common-probability-errors)
- [Statistical claim calibration](#statistical-claim-calibration)

## Entry questions

Before interpreting or accepting a statistical result, answer as many of these
as apply — skip a question only when it's genuinely inapplicable to the method,
not because the paper omitted the answer:

1. What is the estimand — the quantity the analysis is actually trying to learn?
2. What is the statistical model (the data-generating assumption)?
3. What is the likelihood, and does it actually correspond to that model?
4. What data enter the inference, and what was excluded or blinded?
5. What are the parameters of interest?
6. What are the nuisance parameters, and how are they constrained?
7. What assumptions justify the inference procedure (asymptotic regime,
   independence, correct model specification)?
8. What uncertainty is being reported — statistical only, or statistical +
   systematic, and combined how?

A paper that never lets you answer (1)-(3) has an inference that cannot yet be
evaluated — say so rather than assessing the reported number in isolation.

## Likelihood-based inference

- Confirm the likelihood's functional form matches the stated data-generating
  process — a Poisson-counting likelihood used where the described data are
  unbinned, or a Gaussian likelihood used for a small-count regime, is a mismatch
  worth flagging even if the fit converges.
- For maximum-likelihood estimation, check that the reported uncertainty comes
  from the actual curvature/profile of the likelihood (or a calibrated
  approximation to it), not a rule-of-thumb error propagation grafted on
  afterward.
- A likelihood ratio or profile likelihood is only as good as the nuisance-
  parameter treatment it profiles over — check that nuisance parameters
  relevant to the result are actually included, not fixed to their nominal
  value while being described elsewhere as "accounted for."
- For a covariance or correlation matrix used in the fit, check it is positive
  (semi-)definite and that off-diagonal terms have a stated physical origin
  (shared systematic source, shared calibration) — an unexplained correlation
  structure is a modeling assumption in disguise.

## Frequentist inference

Do not treat an asymptotic approximation as universally valid. Before accepting
one:

1. Identify the specific approximation used (Wilks' theorem for a likelihood-
   ratio test statistic, Wald for a Gaussian-limit interval).
2. Identify the assumptions it requires (large sample size, parameter not at a
   boundary, correct model, nested/regular hypotheses).
3. Check whether the analysis's actual sample size and parameter regime
   plausibly satisfy those assumptions — a search near a physical boundary
   (a non-negative signal strength, a cross-section at zero) is a standard case
   where Wilks' theorem needs a corrected asymptotic form or doesn't apply.
4. If the regime is boundary/non-regular/low-count, expect (or perform) a toy
   Monte Carlo calibration of the test statistic rather than accepting the
   asymptotic p-value at face value.
5. Calibrate the final claim to the validated method, not the convenient one.

Other checks:

- **Local vs. global significance**: for any reported local significance, check
  whether a look-elsewhere effect applies (the search scanned more than one
  place — a mass range, multiple channels, multiple sky positions) and whether
  a trials-corrected global significance is also given. A 3σ local excess
  scanned over dozens of independent bins is routinely well below 3σ globally.
  See `reading-papers.md`'s look-elsewhere-effect check for where this surfaces
  during a first read.
- **Upper limits and exclusion**: identify the test statistic and confidence
  construction (e.g. CLs vs. a plain Neyman construction), whether the limit is
  observed or expected (with its uncertainty band), and whether nuisance
  parameters are profiled or fixed at the limit-setting point.
- **Coverage**: a stated confidence level is a coverage property of the
  procedure across repeated experiments, not a probability statement about the
  single observed interval — do not let a paper's phrasing imply otherwise
  without flagging it.
- **Multiple testing**: when several hypotheses or channels are tested, check
  for a stated correction (Bonferroni, Holm, false-discovery-rate) or an
  explicit argument for why none is needed (e.g. a single pre-registered
  channel).

## Bayesian inference

- Identify the prior, the likelihood, and what marginalization was performed to
  obtain the reported posterior or credible interval.
- Check whether nuisance parameters were marginalized (integrated out) or
  profiled (optimized out) — these give numerically different intervals and the
  paper should say which.
- For a result that could plausibly be prior-sensitive (weak data, informative
  prior, a boundary-adjacent parameter), check whether a prior-sensitivity
  check or an alternative prior was reported; its absence is a gap, not
  automatically a flaw.
- A posterior predictive check (does the fitted model reproduce features of the
  data it wasn't directly fit to?) is evidence about model adequacy, not proof
  of it.
- **Never treat a confidence interval and a credible interval as
  interchangeable.** A 95% CI is a statement about the procedure's long-run
  coverage; a 95% credible interval is a posterior probability statement
  conditional on the prior. Reusing one's numeric value while calling it the
  other misstates what was computed. See `scientific-style.md`'s statistical
  reporting section for how to phrase this once verified.

## Systematic uncertainty

For each material source of systematic uncertainty, require an answer to:
*how does it actually enter the final inference?* — a paper that lists sources
without explaining propagation has an inference gap, not just an incomplete
table.

- **Nuisance parameter modeling**: is each systematic represented as a
  constrained nuisance parameter (with a stated constraint term/prior), or
  folded in as a fixed additive/multiplicative shift? These propagate
  differently through a fit.
- **Correlated uncertainties**: when the same systematic source affects
  multiple bins, channels, or measurements, check that the correlation is
  actually modeled (a shared nuisance parameter, an off-diagonal covariance
  term) rather than treated as independent per bin, which understates the true
  uncertainty on any derived quantity.
- **Normalization vs. shape**: a systematic that only rescales a distribution
  behaves very differently in a fit from one that changes its shape — check
  which is claimed and whether the fit setup matches.
- **Uncertainty provenance**: is a given systematic data-driven (calibrated
  against a control sample) or simulation-based (relies on the accuracy of a
  Monte Carlo model)? A simulation-based systematic inherits the simulation's
  own validation status.
- Do not accept a total uncertainty that combines statistical and systematic
  components without stating whether they were added in quadrature under an
  independence assumption or combined with an explicit correlation model.

## Common probability errors

Guard against these specific unjustified leaps, which recur across otherwise
careful analyses:

- **Uncorrelated ⇒ independent.** Zero measured correlation rules out a linear
  relationship, not dependence in general — two variables can be uncorrelated
  and still statistically dependent (e.g. related by a symmetric nonlinear
  function). Flag this jump whenever "no correlation" is used to justify
  treating two quantities as independent in a likelihood or covariance
  structure.
- **Gaussian approximation ⇒ exact Gaussian distribution.** A large-sample or
  central-limit argument justifies treating an estimator as *approximately*
  Gaussian in some regime; it does not make the underlying distribution
  Gaussian, and the approximation can fail exactly where it matters most (tails,
  small samples, boundary parameters).
- **Monte Carlo estimate ⇒ exact probability.** A Monte Carlo integral, toy
  p-value, or sampled expectation carries its own stochastic uncertainty
  (finite sample size, finite number of toys) — report or ask for that
  uncertainty rather than presenting the estimate as an exact value.

## Statistical claim calibration

The written conclusion must match what the inference actually established —
no stronger. These pairs are not interchangeable; require the weaker,
literal reading unless the stronger one is separately justified:

| Reported result | Not the same as |
|---|---|
| "Not excluded at 95% CL" | "The data support the model" |
| "No statistically significant difference" | "The two effects are equivalent" |
| "Local significance of Nσ" | "Global/discovery-level significance of Nσ" |
| "95% confidence interval" | "95% credible interval" |
| "Correlated" | "One causes the other" |

When a paper's abstract or conclusion uses the stronger phrase, check the
Results section for the evidence needed to support it (a dedicated equivalence
test with a stated margin, a global-significance calculation, an actual
posterior) — if that evidence isn't there, the calibration gap is the finding.
See `scientific-style.md`'s significance-language table for the physics σ-based
convention this pairs with, and `claim-evidence-mapping.md` for recording the
gap against the paper's central claim.
```

- [ ] **Step 2: Verify heading anchors match what Tasks 5-6 will link to**

Run: `grep -n '^## ' academic-papers/references/statistical-inference-for-physics.md`
Expected output (7 lines, exact headings):
```
## Entry questions
## Likelihood-based inference
## Frequentist inference
## Bayesian inference
## Systematic uncertainty
## Common probability errors
## Statistical claim calibration
```

- [ ] **Step 3: Commit**

```bash
git add academic-papers/references/statistical-inference-for-physics.md
git commit -m "$(cat <<'EOF'
Add statistical-inference-for-physics reference to academic-papers

Fills the highest-priority gap identified in the capability audit: existing
files (reading-papers.md, scientific-style.md) name statistical concepts
(look-elsewhere effect, CI-vs-credible-interval) as reading-checklist/prose
reminders but never give the inference-construction procedure itself.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01PT3zUgd2GNmGCmkwjUwmxH
EOF
)"
```

---

### Task 2: Create `mathematical-reasoning-and-proof.md` (Priority 2)

**Files:**
- Create: `academic-papers/references/mathematical-reasoning-and-proof.md`

**Interfaces:**
- Consumes: cross-links to `equation-and-notation-auditing.md` (Task 4) and `logical-consistency-and-argument-uniformity.md` (existing) — reference by filename only, no shared code.
- Produces: anchors `#reasoning-workflow`, `#proof-status`, `#approximation-validity`, `#mathematical-checks`, `#counterexample-search`, `#separating-derivation-from-verification` — used by Task 5/6.

- [ ] **Step 1: Write the file**

```markdown
# Mathematical reasoning and proof

Use when evaluating or constructing a mathematical derivation or argument —
checking whether a paper's result actually follows from its stated assumptions,
or reasoning through one's own derivation before writing it up. Distinct from
`equation-and-notation-auditing.md`, which checks the algebra's internal
consistency (dimensions, indices, sign/normalization conventions) once a
derivation is written down; this file checks the argument's *validity and
justified strength* — whether the assumptions are sound, whether the proof
status matches what's claimed, and how to verify the result independently of
the derivation itself. Also distinct from
`logical-consistency-and-argument-uniformity.md`, which checks a paper's prose
argument for cross-section contradictions; this file is about a specific
mathematical derivation's own soundness.

## Table of contents
- [Reasoning workflow](#reasoning-workflow)
- [Proof status](#proof-status)
- [Approximation validity](#approximation-validity)
- [Mathematical checks](#mathematical-checks)
- [Counterexample search](#counterexample-search)
- [Separating derivation from verification](#separating-derivation-from-verification)

## Reasoning workflow

Work through a derivation in this order, and expect a rigorous paper to make
each step identifiable even if not explicitly labeled:

```text
Assumptions → Definitions → Intermediate results → Derivation → Result → Consistency checks
```

For each step, identify:

- **Explicit assumptions** the author states, and **implicit assumptions**
  the derivation actually relies on but doesn't name (smoothness,
  independence, a regime where a series converges).
- **Definitions** — is every symbol introduced before use, with a consistent
  meaning throughout (delegate the symbol-ledger mechanics to
  `equation-and-notation-auditing.md`)?
- **Necessary vs. sufficient conditions** — does the argument establish that a
  condition is required for the result, or merely that the result holds when
  the condition is met (these are not interchangeable when the conclusion is
  later applied outside the stated condition)?
- **Approximation regime** — where in the derivation is an expansion,
  linearization, or asymptotic limit taken?
- **Intermediate dependencies** — does a later step silently reuse an earlier
  intermediate result outside the regime where that result was valid?
- **Final conclusion** — restate it in one sentence and check it doesn't say
  more than the chain of steps established.

## Proof status

Require every mathematical result to carry an explicit status, and never let
one silently become another when the result is reused later in the same paper
or in a summary of it:

- **Formal proof** — every step follows from stated axioms/premises with no
  unstated gap.
- **Analytic derivation** — an exact algebraic/calculus result under stated
  assumptions, not from first principles/axioms.
- **Perturbative argument** — valid to a stated order in an expansion
  parameter; the neglected terms are not shown to vanish, only to be small in
  some regime.
- **Asymptotic argument** — valid in a limit (large N, high energy, weak
  coupling); the rate of approach to the limit is a separate, often unstated,
  question.
- **Heuristic argument** — motivates a result without establishing it
  (dimensional-analysis scaling, a plausibility argument, an analogy to a
  solved case).
- **Numerical evidence** — a computed instance or scan consistent with the
  claim, not a general demonstration of it.
- **Empirical observation** — a pattern seen in data, with no claimed
  theoretical mechanism yet.
- **Conjecture** — an unproven claim offered as a research direction.

**Never silently upgrade a heuristic argument, numerical observation,
perturbative result, or empirical pattern into a proof.** The most common
version of this error is a perturbative or asymptotic result described in the
abstract or conclusion using unqualified language ("the result is X") that
reads as exact — check the Results/Methods section for the actual status
before accepting the abstract's phrasing.

## Approximation validity

For any approximation-based result, identify:

- The **expansion parameter** and its actual numeric value/range in the
  regime being applied.
- The **validity regime** — the condition under which the approximation is
  expected to hold (small parameter, large separation of scales, weak
  coupling).
- The **neglected terms** — what order was dropped, and is there a stated or
  computable bound on their size?
- The **expected order of corrections** — does the paper's own claimed
  precision match what the truncation order can actually support, or does it
  claim finer precision than the retained terms justify?

## Mathematical checks

Use the subset appropriate to the result — not every check applies to every
derivation:

- **Limiting and special cases**: does the result reduce to a known answer in
  a simple limit (zero coupling, one dimension, equal masses)?
- **Symmetry arguments and conservation laws**: does the result respect the
  symmetries the underlying theory/setup actually has (and correctly break
  the ones it explicitly breaks)?
- **Perturbative consistency and asymptotic behavior**: does the next order
  (if computable) actually shrink relative to the claimed order, and does the
  result behave sensibly as parameters go to their extreme values?
- **Order-of-magnitude estimate**: does a quick dimensional/scaling estimate
  land near the detailed result, catching a stray factor of the wrong scale?
- **Sign and normalization checks**: does a probability, rate, or cross
  section come out non-negative and correctly normalized?
- **Numerical spot check**: evaluate the symbolic result at a specific point
  and compare against a direct numerical computation of the same quantity.
- **Symbolic verification**: use a computer-algebra check of an algebraic
  step, especially a long or error-prone one.
- **Independent derivation**: re-derive the result via a different method or
  starting point (see below) — the strongest single check, when feasible.

A numerical spot check or symbolic simplification that succeeds *corroborates*
a derivation; it does not, by itself, establish a general proof. Report which
checks were actually performed and over what domain.

## Counterexample search

When evaluating a broad mathematical claim (holds "for all N," "in general,"
"for any coupling"), actively look for:

- Boundary cases (parameter at zero, at its physical limit).
- Singular or degenerate cases (a matrix losing rank, two masses becoming
  equal, a denominator approaching zero).
- Conditions under which the stated argument's assumptions plausibly fail.

**The absence of an immediately found counterexample is not proof that the
claim is general** — report a counterexample search as "no counterexample
found in {these cases}," not as confirmation.

## Separating derivation from verification

Generating a result and checking it should use partially independent
reasoning wherever the result matters enough to justify the extra effort —
reusing the exact same assumptions and transformation path as the only
verification just re-checks the arithmetic, not the argument.

```text
Derivation: symbolically derive the expression via method A

Verification: evaluate limiting cases, check dimensions
(equation-and-notation-auditing.md), perform a numerical spot check, and —
for an important or novel result — attempt an independent derivation via a
different method or starting point
```

Scale the number and independence of checks to the claim's importance,
novelty, numerical sensitivity, and the cost of being wrong — a routine
intermediate step doesn't need the same treatment as a paper's central result.
This is the general form of the cross-check hierarchy that
`numerical-and-computational-methods.md`'s validation workflow applies
specifically to numerical results, and that
`statistical-inference-for-physics.md` applies to a statistical claim's
calibration — treat all three as instances of the same principle rather than
independent rules.

## Evidence-strength ladder

When recording a theoretical claim in `claim-evidence-mapping.md`'s evidence
matrix, state its justified strength using the proof-status categories above
(exact/formal, analytically derived under stated assumptions, asymptotically
justified, numerically validated, empirically observed, heuristically
motivated, speculative) rather than a bare "supported"/"unsupported" verdict —
the verdict answers whether the evidence matches the claim; this ladder answers
how strong that evidence actually is on its own terms.
```

- [ ] **Step 2: Verify heading anchors**

Run: `grep -n '^## ' academic-papers/references/mathematical-reasoning-and-proof.md`
Expected: 7 headings — `Reasoning workflow`, `Proof status`, `Approximation validity`, `Mathematical checks`, `Counterexample search`, `Separating derivation from verification`, `Evidence-strength ladder`.

- [ ] **Step 3: Commit**

```bash
git add academic-papers/references/mathematical-reasoning-and-proof.md
git commit -m "$(cat <<'EOF'
Add mathematical-reasoning-and-proof reference to academic-papers

Second-priority gap: no existing file distinguished proof status (formal vs.
perturbative vs. heuristic vs. numerical vs. empirical vs. conjecture) or gave
an approximation-validity/counterexample-search workflow; equation-and-
notation-auditing.md covers algebra consistency but not argument validity.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01PT3zUgd2GNmGCmkwjUwmxH
EOF
)"
```

---

### Task 3: Create `numerical-and-computational-methods.md` (Priority 3, folds in Monte Carlo, scientific computing, computational-experiment-design)

**Files:**
- Create: `academic-papers/references/numerical-and-computational-methods.md`

**Interfaces:**
- Consumes: cross-links to `agile-development` (boundary table only, no shared code), `hep-analysis`, `deep-learning`, `reproducibility-auditing.md`, `statistical-inference-for-physics.md` (Task 1).
- Produces: anchors `#numerical-reliability`, `#numerical-validation-workflow`, `#optimization`, `#monte-carlo-and-sampling`, `#scientific-computing`, `#computational-experiment-design`, `#algorithmic-reasoning`.

- [ ] **Step 1: Write the file**

```markdown
# Numerical and computational methods

Use when evaluating or designing a numerical/computational scientific
result — whether a paper's integral, fit, simulation, or scan is actually
trustworthy, or checking one's own computation before reporting it. This is
about *scientific validity of the computation*, not general software
engineering — code architecture, deployment, and service boundaries belong to
`agile-development`; running the actual physics fit or ML training belongs to
`hep-analysis`/`deep-learning`. **A numerical result is not validated merely
because the code runs.**

## Table of contents
- [Numerical reliability](#numerical-reliability)
- [Numerical validation workflow](#numerical-validation-workflow)
- [Optimization](#optimization)
- [Monte Carlo and sampling](#monte-carlo-and-sampling)
- [Scientific computing](#scientific-computing)
- [Computational experiment design](#computational-experiment-design)
- [Algorithmic reasoning](#algorithmic-reasoning)

## Numerical reliability

Check the subset relevant to the computation at hand:

- **Floating-point precision and conditioning**: does the computation involve
  subtracting nearly-equal large numbers, inverting a near-singular matrix, or
  otherwise amplifying rounding error?
- **Convergence**: for an iterative method (fit, ODE solver, series sum), was
  convergence actually verified (residual/step-size below a stated tolerance),
  or just assumed because the loop terminated?
- **Discretization, truncation, integration, and interpolation error**: for a
  numerical integral, grid, or lookup table, is the reported precision
  consistent with the resolution actually used?
- **Extrapolation risk**: is the result being evaluated inside the range the
  numerical method/table/fit was validated over, or extrapolated beyond it?
- **Optimizer/solver tolerance, binning sensitivity, parameter-scan
  resolution**: would a tighter tolerance, finer binning, or denser scan
  change the reported conclusion, not just its last significant digit?
- **Stochastic uncertainty**: for any result with a Monte Carlo component,
  does the reported uncertainty include the simulation's own statistical
  noise, separate from the physical/statistical uncertainty being measured?

## Numerical validation workflow

Use the subset appropriate to the computation:

```text
Known analytic/special case
        ↓
Convergence test (does the result stabilize as resolution/iterations increase?)
        ↓
Tolerance/resolution sensitivity (does the conclusion survive a stricter setting?)
        ↓
Independent implementation or cross-check (different method, tool, or code path)
        ↓
Physics/scientific sanity check (right sign, right order of magnitude, right limit)
```

A single run at one tolerance that "looks stable" has not been shown to be
converged — request or perform at least one point of comparison (a finer
setting, a known limit, or a second implementation) before treating the value
as validated.

## Optimization

Do not equate optimizer termination with proof that the intended (often
global) solution was found. Check:

- The objective and constraints actually being optimized match the stated
  scientific problem.
- Initialization: was more than one starting point tried, for a
  non-convex problem?
- Local vs. global minima: is there a reason to believe the found minimum is
  global (convexity, a scan showing no better basin) or is it merely the one
  the optimizer happened to reach?
- Convergence criteria: what tolerance/gradient-norm/iteration cap defined
  "done," and is it tight enough for the claimed precision?
- Parameter degeneracy and flat directions: does the likelihood/objective have
  a direction along which it barely changes — if so, a "well-determined"
  parameter estimate along that direction is not actually well constrained.

## Monte Carlo and sampling

- **Reproducibility**: is the random seed (or seed-handling scheme) recorded
  well enough that the result could be regenerated?
- **Statistical uncertainty and convergence**: does the reported precision
  reflect the actual number of samples/toys drawn, and was convergence with
  sample size checked rather than assumed?
- **Sampling efficiency, importance weights, variance reduction**: for
  importance sampling or a reweighting scheme, are effective sample size and
  weight variance reported — a few dominant weights can silently invalidate an
  otherwise large nominal sample.
- **Rare-event sampling**: for a small-probability tail estimate, was a
  variance-reduction technique used, or is the estimate resting on a handful of
  rare draws with a large relative uncertainty?

For MCMC specifically, where applicable: burn-in/warmup, mixing, autocorrelation
time, use of multiple independent chains, and a convergence diagnostic
appropriate to the sampler. Do not demand a specific diagnostic (e.g. one named
statistic) unless the sampling method and claim actually call for it.

## Scientific computing

Scope this section to what materially affects scientific correctness or
reproducibility — not general software engineering, which belongs to
`agile-development`:

| Concern | Home |
|---|---|
| Code architecture, service boundaries, deployment | `agile-development` |
| Numerical convergence, precision, reproducible seeds | this file |
| Provenance of a specific reported number (code version, config, inputs) | this file / `reproducibility-auditing.md` |
| General CI/testing practice for a codebase | `agile-development` |
| Monte Carlo/statistical validation of a scientific result | this file / `statistical-inference-for-physics.md` |

Within that scope, check: is the random-state/seed management explicit enough
to reproduce a stochastic result; is there provenance for which code
version/configuration produced a quoted number; and, where numerical
regression matters (a long-lived pipeline whose output feeds later papers), is
there a reference dataset or known-value check that would catch a silent
regression?

## Computational experiment design

Relevant to simulations, phenomenology scans, ML-based scientific analyses, and
detector studies. The core question is whether the same information was used
to both build/tune the method and evaluate it — guard against circular
validation:

1. Design or tune the method.
2. Choose the model/selection based on that tuning.
3. Evaluate the final result.

If steps 1-2 and step 3 draw on overlapping information (the same events used
to optimize a selection and then quote its significance; hyperparameters tuned
against the final test metric) without a stated correction, the reported
performance is optimistically biased — identify this as a data-leakage/implicit-
tuning gap rather than accepting the final number at face value.

Where relevant, check for: a held-out validation sample distinct from the one
used to tune the method; a blinded signal region; closure tests (does the
method recover a known/injected answer on a control sample); injection tests
(does an artificially inserted signal come back at the injected size); null
tests (does the method report nothing when nothing is there); and whether
sensitivity/robustness was checked against the choices that were somewhat
arbitrary (binning, a selection threshold). For the depth of an ML ablation or
matched-budget comparison itself, hand off to `deep-learning`; for a physics
control/validation-region design, hand off to `hep-analysis` — this section is
for recognizing the gap while reading or reviewing, not for running the study.

## Algorithmic reasoning

Consider computational complexity, memory complexity, and scaling with dataset
size only when they affect feasibility, correctness, precision, or
reproducibility — not as abstract complexity-theory commentary. Relevant
questions: does an algorithm's scaling make a claimed dataset size actually
tractable; does an approximation used purely for speed change the numerical
answer beyond the stated tolerance; is a parallel/distributed implementation's
result confirmed to match its serial equivalent?
```

- [ ] **Step 2: Verify heading anchors**

Run: `grep -n '^## ' academic-papers/references/numerical-and-computational-methods.md`
Expected: 7 headings matching the ToC above.

- [ ] **Step 3: Commit**

```bash
git add academic-papers/references/numerical-and-computational-methods.md
git commit -m "$(cat <<'EOF'
Add numerical-and-computational-methods reference to academic-papers

Third-priority gap. Consolidates numerical reliability/convergence,
optimization, Monte Carlo/MCMC validation, scientific-computing scope (with an
explicit agile-development boundary), and computational-experiment-design/
circular-validation recognition into one file rather than three separate ones,
per the spec's preference for fewer coherent references.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01PT3zUgd2GNmGCmkwjUwmxH
EOF
)"
```

---

### Task 4: Extend `equation-and-notation-auditing.md` (symbolic/dimensional reasoning, spec §10)

**Files:**
- Modify: `academic-papers/references/equation-and-notation-auditing.md`

**Interfaces:**
- Consumes: none.
- Produces: no new anchors (edits existing bullet lists and the closing paragraph); Task 1/2 already reference this file by name only.

- [ ] **Step 1: Add a bullet naming the conventions not yet explicit, in the existing "Check the following where applicable" list**

In `academic-papers/references/equation-and-notation-auditing.md`, the list currently reads (lines 15-30):

```
Check the following where applicable:

- Terms added or equated have compatible dimensions and shapes; free indices
  agree and dummy indices are contracted consistently. Check transpose versus
  conjugate transpose and the measure in sums, integrals, and expectations.
- Logarithms and exponentials have dimensionless arguments under the stated
  convention. Establish natural units, normalized variables, or absorbed constants
  before reporting a dimensional error.
- Normalization factors, signs, boundaries, conditioning, and domains are stated.
  Check limiting cases, singular denominators, and probability normalization where
  they can meaningfully reveal mistakes.
- Each derivation step follows under its stated assumptions. Label approximations
  and where they apply; check assumptions such as independence, differentiability,
  invertibility, or interchange of limits/integration when a step depends on them.
- Definitions and numbering remain consistent when equations are reused in
  algorithms, text, or supplementary derivations.
```

Insert a new bullet after the first one (the dimensions/indices bullet), so the
metric/Lorentz/Fourier/phase-space terms named in the task spec are explicit:

```
- Metric signature, Lorentz-index placement (upper/lower) and contraction, and
  Fourier-transform convention (sign and 2π placement) are stated when a result
  depends on them; a Jacobian or phase-space factor (e.g. `d^3p/(2π)^3 2E`) is
  present wherever a variable change or a Lorentz-invariant measure requires one.
```

Use the Edit tool with this old_string/new_string pair (matching the file's
exact current text):

- old_string:
```
- Terms added or equated have compatible dimensions and shapes; free indices
  agree and dummy indices are contracted consistently. Check transpose versus
  conjugate transpose and the measure in sums, integrals, and expectations.
- Logarithms and exponentials have dimensionless arguments under the stated
```
- new_string:
```
- Terms added or equated have compatible dimensions and shapes; free indices
  agree and dummy indices are contracted consistently. Check transpose versus
  conjugate transpose and the measure in sums, integrals, and expectations.
- Metric signature, Lorentz-index placement (upper/lower) and contraction, and
  Fourier-transform convention (sign and 2π placement) are stated when a result
  depends on them; a Jacobian or phase-space factor (e.g. `d^3p/(2π)^3 2E`) is
  present wherever a variable change or a Lorentz-invariant measure requires one.
- Logarithms and exponentials have dimensionless arguments under the stated
```

- [ ] **Step 2: Make the convention-vs-error distinction explicit (spec §10's core requirement)**

The closing paragraph currently reads:

```
For a suspected error, show the specific step or counterexample and the convention
used. Distinguish definite inconsistency, ambiguous notation, and an unverified
derivation. Symbolic simplification and numerical spot checks may corroborate a
finding but do not establish a general proof; record assumptions and test domains.
Never silently repair a scientific formula whose intended meaning is unclear.
```

Edit old_string/new_string:

- old_string:
```
For a suspected error, show the specific step or counterexample and the convention
used. Distinguish definite inconsistency, ambiguous notation, and an unverified
derivation. Symbolic simplification and numerical spot checks may corroborate a
finding but do not establish a general proof; record assumptions and test domains.
Never silently repair a scientific formula whose intended meaning is unclear.
```
- new_string:
```
For a suspected error, show the specific step or counterexample and the convention
used. Distinguish definite inconsistency, ambiguous notation, and an unverified
derivation — and distinguish all three from a mere **convention difference**
(a metric signature, a Fourier 2π placement, a normalization choice) that
differs from another paper's but is internally consistent. Report a convention
difference as a finding only when it produces an internal inconsistency or
changes a physically observable result, not merely because it differs from a
convention used elsewhere. Symbolic simplification and numerical spot checks
may corroborate a finding but do not establish a general proof; record
assumptions and test domains. Never silently repair a scientific formula whose
intended meaning is unclear.
```

- [ ] **Step 3: Verify the edits landed and the file still parses as one coherent document**

Run: `grep -n "convention difference\|Fourier\|Lorentz-index\|phase-space factor" academic-papers/references/equation-and-notation-auditing.md`
Expected: 4 matching lines (one per inserted phrase).

- [ ] **Step 4: Commit**

```bash
git add academic-papers/references/equation-and-notation-auditing.md
git commit -m "$(cat <<'EOF'
Extend equation-and-notation-auditing with convention-vs-error distinction

Adds the explicit Lorentz/Fourier/phase-space/metric-convention terms and the
algebraic-inconsistency-vs-convention-difference-vs-physical-disagreement
distinction requested in the symbolic/dimensional reasoning gap, instead of
creating a separate file for content this reference already mostly owns.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01PT3zUgd2GNmGCmkwjUwmxH
EOF
)"
```

---

### Task 5: Cross-link `claim-evidence-mapping.md` and `reading-papers.md` to the new references

**Files:**
- Modify: `academic-papers/references/claim-evidence-mapping.md`
- Modify: `academic-papers/references/reading-papers.md`

**Interfaces:**
- Consumes: anchors/filenames produced by Tasks 1-3.
- Produces: none new.

- [ ] **Step 1: Edit `claim-evidence-mapping.md`'s theoretical-claim bullet**

Current text (in "Checking evidence against claim type"):

```
- A theoretical claim depends on its assumptions and domain. Empirical examples
  illustrate a theorem but do not prove it.
```

- old_string:
```
- A theoretical claim depends on its assumptions and domain. Empirical examples
  illustrate a theorem but do not prove it.
```
- new_string:
```
- A theoretical claim depends on its assumptions and domain. Empirical examples
  illustrate a theorem but do not prove it. Use
  `mathematical-reasoning-and-proof.md`'s proof-status ladder to state how
  strong the theoretical evidence actually is (formal/analytic/perturbative/
  asymptotic/heuristic/numerical/empirical/conjecture) rather than defaulting
  to a bare supported/unsupported verdict.
- A statistical claim (a significance, an exclusion, a correlation) needs the
  inference actually behind it, not just the reported number — check it
  against `statistical-inference-for-physics.md`'s claim-calibration table
  before accepting the paper's own characterization of its result.
```

- [ ] **Step 2: Edit `reading-papers.md`'s look-elsewhere-effect bullet**

Current text (HEP-specific section):

```
- **Look-elsewhere effect**: for any reported local significance, check whether a
  global significance (accounting for the number of places an excess could have
  appeared) is also quoted — a "3σ local" excess is often much less significant
  globally.
```

- old_string:
```
- **Look-elsewhere effect**: for any reported local significance, check whether a
  global significance (accounting for the number of places an excess could have
  appeared) is also quoted — a "3σ local" excess is often much less significant
  globally.
```
- new_string:
```
- **Look-elsewhere effect**: for any reported local significance, check whether a
  global significance (accounting for the number of places an excess could have
  appeared) is also quoted — a "3σ local" excess is often much less significant
  globally. See `statistical-inference-for-physics.md`'s frequentist-inference
  section for the actual trials-correction/global-significance check.
```

- [ ] **Step 3: Edit `reading-papers.md`'s systematics-treatment bullet**

Current text:

```
- **Systematics treatment**: are systematic uncertainties itemized by source (not
  just a single lumped number), and is it clear how they were evaluated (data-driven
  vs. simulation-based)?
```

- old_string:
```
- **Systematics treatment**: are systematic uncertainties itemized by source (not
  just a single lumped number), and is it clear how they were evaluated (data-driven
  vs. simulation-based)?
```
- new_string:
```
- **Systematics treatment**: are systematic uncertainties itemized by source (not
  just a single lumped number), and is it clear how they were evaluated (data-driven
  vs. simulation-based)? See `statistical-inference-for-physics.md`'s systematic-
  uncertainty section for what "accounted for" should actually mean (nuisance
  modeling, correlation, propagation) before accepting the itemized list at
  face value.
```

- [ ] **Step 4: Edit `reading-papers.md`'s train/test-contamination bullet (Statistics/ML-specific section)**

Current text:

```
- **Train/test contamination**: for a public benchmark or a pretrained model, is
  there a check that the test set didn't leak into pretraining or fine-tuning
  data?
```

- old_string:
```
- **Train/test contamination**: for a public benchmark or a pretrained model, is
  there a check that the test set didn't leak into pretraining or fine-tuning
  data?
```
- new_string:
```
- **Train/test contamination**: for a public benchmark or a pretrained model, is
  there a check that the test set didn't leak into pretraining or fine-tuning
  data? See `numerical-and-computational-methods.md`'s computational-experiment-
  design section for the general circular-validation pattern this is one
  instance of.
```

- [ ] **Step 5: Verify all four edits landed**

Run: `grep -n "mathematical-reasoning-and-proof.md\|statistical-inference-for-physics.md\|numerical-and-computational-methods.md" academic-papers/references/claim-evidence-mapping.md academic-papers/references/reading-papers.md`
Expected: 5 matching lines total (2 in claim-evidence-mapping.md, 3 in reading-papers.md).

- [ ] **Step 6: Commit**

```bash
git add academic-papers/references/claim-evidence-mapping.md academic-papers/references/reading-papers.md
git commit -m "$(cat <<'EOF'
Cross-link claim-evidence-mapping and reading-papers to new reasoning refs

Makes the new statistical-inference/mathematical-reasoning/numerical-methods
references reachable from the two files an agent already consults during an
ordinary read or audit, instead of leaving them discoverable only via SKILL.md.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01PT3zUgd2GNmGCmkwjUwmxH
EOF
)"
```

---

### Task 6: Update `SKILL.md` routing (spec §22)

**Files:**
- Modify: `academic-papers/SKILL.md`

**Interfaces:**
- Consumes: filenames from Tasks 1-3.
- Produces: none (leaf task, consumed only by `validate_skill_bundle.py` in Task 7).

- [ ] **Step 1: Extend the frontmatter description with the new capability**

Current frontmatter (line 3), in part:

```
...auditing reproducibility/equations/consistency/logical-argument-uniformity...
```

- old_string:
```
auditing reproducibility/equations/consistency/logical-argument-uniformity, reviewing accompanying code,
```
- new_string:
```
auditing reproducibility/equations/consistency/logical-argument-uniformity/statistical-or-mathematical-rigor, reviewing accompanying code,
```

- [ ] **Step 2: Add three bullets to "Focused verification and review modes" > "Verification and auditing"**

Current text has, in order: Citation verification, Systematic-review screening,
Reproducibility auditing, Code review report, **Equation and notation
auditing**, Claim–evidence mapping, Logical consistency..., Manuscript
consistency..., Plagiarism...

Insert the three new bullets immediately after the existing "Equation and
notation auditing" bullet and before "Claim–evidence mapping":

- old_string:
```
- **Equation and notation auditing:** check definitions, dimensions, index/shape
  consistency, assumptions, and derivation steps. Read
  `references/equation-and-notation-auditing.md`.
- **Claim–evidence mapping:** connect central claims to results, derivations, and
  citations, and identify unsupported generalizations. Read
  `references/claim-evidence-mapping.md`.
```
- new_string:
```
- **Equation and notation auditing:** check definitions, dimensions, index/shape
  consistency, assumptions, and derivation steps. Read
  `references/equation-and-notation-auditing.md`.
- **Mathematical reasoning and proof status:** check whether a derivation's
  assumptions are sound and its claimed proof status (formal, analytic,
  perturbative, asymptotic, heuristic, numerical, empirical, conjecture)
  matches what was actually established. Read
  `references/mathematical-reasoning-and-proof.md`.
- **Statistical inference for physics:** check whether a likelihood, test,
  interval, or limit is correctly set up and whether the stated conclusion
  matches what the inference actually established. Read
  `references/statistical-inference-for-physics.md`.
- **Numerical and computational methods:** check whether a numerical or
  computational result (integral, fit, simulation, scan) is actually
  validated — convergence, stability, independent cross-check — rather than
  merely having run. Read `references/numerical-and-computational-methods.md`.
- **Claim–evidence mapping:** connect central claims to results, derivations, and
  citations, and identify unsupported generalizations. Read
  `references/claim-evidence-mapping.md`.
```

- [ ] **Step 3: Add the three files to the "Reference files" > "Verification and auditing" group**

Current text in that group starts:

```
**Verification and auditing**
- `references/citation-verification.md` — reference identity/version checks and
  whether cited text supports the manuscript's claim.
```

and ends (before "**Assessment and restructuring**") with the
plagiarism-and-text-reuse-checking.md entry.

- old_string:
```
- `references/equation-and-notation-auditing.md` — definitions, dimensions,
  index/shape consistency, and derivation-step checks
- `references/claim-evidence-mapping.md` — connecting central claims to results,
  derivations, and citations; flagging unsupported generalizations
```
- new_string:
```
- `references/equation-and-notation-auditing.md` — definitions, dimensions,
  index/shape consistency, derivation-step checks, and distinguishing an actual
  inconsistency from a mere notation/convention difference
- `references/mathematical-reasoning-and-proof.md` — the assumptions →
  definitions → derivation → result workflow, proof-status taxonomy (formal
  through conjecture), approximation validity, mathematical checks
  (limiting cases, symmetry, order-of-magnitude), and counterexample search
- `references/statistical-inference-for-physics.md` — likelihood construction,
  frequentist and Bayesian inference, asymptotic-approximation validity,
  systematic-uncertainty propagation, common probability errors, and
  statistical-claim-calibration language (not-excluded vs. supported,
  local vs. global significance, confidence vs. credible interval)
- `references/numerical-and-computational-methods.md` — numerical reliability
  and convergence, optimization pitfalls, Monte Carlo/MCMC validation,
  scientific-computing scope (vs. `agile-development`), and recognizing
  circular validation/data leakage in a computational experiment
- `references/claim-evidence-mapping.md` — connecting central claims to results,
  derivations, and citations; flagging unsupported generalizations
```

- [ ] **Step 4: Verify with the bundle's own validator**

Run: `python3 academic-papers/scripts/validate_skill_bundle.py academic-papers`
Expected: exit code 0, no errors printed (this checks frontmatter, that every
backtick-referenced path in SKILL.md exists on disk, and that every file under
`references/` is mentioned somewhere in SKILL.md — catching a typo'd filename
or an orphaned new file).

- [ ] **Step 5: Commit**

```bash
git add academic-papers/SKILL.md
git commit -m "$(cat <<'EOF'
Route SKILL.md to the new mathematical/statistical/numerical references

Adds the three new files to both the Focused-verification-modes bullet list
and the Reference-files index (matching the existing dual-listing pattern),
and extends the frontmatter description so the skill triggers on
statistical/mathematical-rigor auditing requests, not just paper-writing ones.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01PT3zUgd2GNmGCmkwjUwmxH
EOF
)"
```

---

### Task 7: Final validation pass (spec §29, §30)

**Files:** none modified — verification only.

- [ ] **Step 1: Run the bundle validator one more time on the final state**

Run: `python3 academic-papers/scripts/validate_skill_bundle.py academic-papers`
Expected: exit code 0.

- [ ] **Step 2: Check for accidental duplication of the new material**

Run: `grep -rn "look-elsewhere effect\|Wilks\|profile likelihood\|credible interval" academic-papers/references/*.md`
Expected: each term appears in `statistical-inference-for-physics.md` (the
substantive treatment) plus at most one short cross-reference sentence in
`reading-papers.md`/`scientific-style.md`/`claim-evidence-mapping.md` — no
second full explanation of the same procedure anywhere else.

- [ ] **Step 3: Check every new cross-reference resolves to a real file**

Run:
```bash
grep -ohE '`references/[a-z0-9-]+\.md`' academic-papers/references/*.md academic-papers/SKILL.md | tr -d '`' | sort -u | while read -r f; do [ -f "academic-papers/$f" ] || echo "MISSING: $f"; done
```
Expected: no output (every referenced path exists).

- [ ] **Step 4: Mentally run the seven scenarios from the spec's §30 against the final files**

For each, confirm which file/section would catch it (do not re-run the audit,
just point to the mechanism — this is a design self-check, not a new test):
- **A (perturbative called exact)** → `mathematical-reasoning-and-proof.md`
  "Proof status" + "Never silently upgrade..." principle.
- **B (local significance called discovery)** → `statistical-inference-for-
  physics.md` "Frequentist inference" local-vs-global bullet + "Statistical
  claim calibration" table.
- **C (one-tolerance integral called stable)** → `numerical-and-computational-
  methods.md` "Numerical validation workflow".
- **D (zero correlation called independence)** → `statistical-inference-for-
  physics.md` "Common probability errors".
- **E (systematics listed without propagation)** → `statistical-inference-for-
  physics.md` "Systematic uncertainty" entry question.
- **F (hyperparameters tuned on the eval set)** → `numerical-and-computational-
  methods.md` "Computational experiment design" circular-validation steps 1-3.
- **G (exclusion limit, procedure unclear)** → `statistical-inference-for-
  physics.md` "Frequentist inference" upper-limits bullet (test statistic,
  CLs/Neyman, observed/expected, nuisance treatment).

If any scenario has no clear owning section, stop and add the missing bullet
to the relevant file before proceeding — do not close the task with a gap.

- [ ] **Step 5: Final commit (only if Step 4 required a fix; otherwise this task produces no commit)**

```bash
git add -A academic-papers/
git commit -m "$(cat <<'EOF'
Close scenario-coverage gap found in final validation pass

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01PT3zUgd2GNmGCmkwjUwmxH
EOF
)"
```

---

## Self-Review (performed before handing off this plan)

**Spec coverage:**
- §3 Mathematical reasoning/proof → Task 2. §4 Statistical inference → Task 1.
  §5 Systematic uncertainty → Task 1's "Systematic uncertainty" section. §6
  Claim calibration → Task 1's "Statistical claim calibration" table. §7
  Probability → Task 1's "Common probability errors" (folded per spec §20
  explicit permission). §8-9 Numerical/MC → Task 3. §10 Symbolic/dimensional →
  Task 4 (extends existing file per spec §10's own instruction to prefer
  that). §11 Computational experiment design → Task 3's dedicated section. §12
  Scientific computing → Task 3's dedicated section with boundary table. §16-18
  Cross-check hierarchy/derivation-vs-verification/assumption tracking → Task
  2's "Separating derivation from verification" (explicitly generalizes to the
  other two files rather than repeating the principle three times). §19
  Evidence strength → Task 2's "Evidence-strength ladder" + Task 5's
  cross-link into `claim-evidence-mapping.md`. §22 Routing → Task 6. §23
  HEP-specific-but-not-overspecialized → satisfied by keeping HEP terms
  (profile likelihood, CLs, look-elsewhere, signal/control/validation regions)
  inside otherwise general sections rather than a HEP-only file. §13/§26
  Non-goals (no computer-science.md, no textbook) → satisfied by the 3-file
  scope and the audit's reuse-first outcome.
- No task spec section is left without an owning task.

**Placeholder scan:** every step above contains complete file content or an
exact old_string/new_string pair — no "TBD," no "similar to Task N," no
prose-only description of a code/content step.

**Type/anchor consistency:** the heading text used in each file's own ToC
(Task 1/2/3, Step 1) matches exactly what Tasks 5 and 6 reference by name; no
task links to a heading that doesn't exist in the file that defines it.
