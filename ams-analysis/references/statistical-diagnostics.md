# Statistical Diagnostics: Poisson Limits, Profile Likelihood, Template and Unfolding Toys

## When to read this file

Read only when a low-count or validation answer needs numbers that a rule alone cannot give: an exact Poisson upper limit or interval, the zero-count bound, a Feldman-Cousins or CLs limit, a profile-likelihood limit or significance (single or multi-bin), a seeded coverage check, a boundary (s >= 0) significance check, a finite-template-statistics check (with a Barlow-Beeston-lite fit), a regularization scan, a closure or pull test, a forward-folding versus unfolding comparison, a response-statistics check, or a correlated-ratio check. The decisions themselves (when Gaussian, Wilks or S/sqrt(B) fail, boundary and non-regular problems, limits versus discovery) are in [inference-and-unfolding](inference-and-unfolding.md#rare-and-low-count-inference); do not load this file for those.

## Contents

1. [What the scripts do](#what-the-scripts-do)
2. [Decision rules](#decision-rules)
3. [Not implemented](#not-implemented)
4. [Failure modes](#failure-modes)
5. [Required source classes](#required-source-classes)
6. [Questions to ask the user](#questions-to-ask-the-user)

## What the scripts do

All four scripts are standard library only, label output [General method], and exit 0 (ok) or 2 (rejected input). Toy-based subcommands require `--seed` and echo it with the toy count.

`scripts/poisson_diagnostics.py` provides five subcommands (exact Poisson constructions, no toys except `coverage`):

- `upper-limit --n N --b B --cl CL`: the classical one-sided upper limit on a signal mean for `N` observed events and a **known** background `B`, from `P(N' <= N | s + B) = 1 - CL`. For `N = 0`, `B = 0` it returns `-ln(1 - CL)` (about 3.00 at 95%).
- `interval --n N --cl CL`: the Garwood central interval on a Poisson mean, which is conservative (coverage at least `CL`).
- `fc-interval --n N --b B --cl CL [--step X]`: the Feldman-Cousins unified interval on a signal mean `s >= 0` for `N` observed events and a **known** background `B` (S31), by a deterministic grid scan (no toys; the grid step, default 0.005, bounds its accuracy, and the result is slightly conservative for discrete counts). It reproduces the published table values (for example `N = 0`, `B = 0`, 90%: upper 2.44; `N = 0`, `B = 2`: 1.08). Unlike the classical limit it is never empty or negative: a lower bound of 0 is the expected behavior at small `N`.
- `cls-limit --n N --b B --cl CL [--sigma-b S]`: the CLs upper limit on a signal mean for a counting experiment (`CLs = CLs+b / CLb`, S36): the observed limit plus the median and 1- and 2-sigma expected limits under background only, the expected sensitivity the classical limit lacks. `--sigma-b` marginalizes the background over a truncated normal prior by deterministic quantile nodes (Cousins-Highland): an approximation, so vary `sigma_b` and check the result moves little. CLs over-covers by design and is not a frequentist interval.
- `fc-interval ... --sigma-b S`: the same Feldman-Cousins scan with the background marginalized in the same way (default grid step 0.02 and about 2 s; it converges to the known-background interval as `S` goes to 0 and widens with `S`). This is not a profile-likelihood treatment of the nuisance and its coverage at the true background is not guaranteed.
- `coverage --mu MU --cl CL --toys T --seed S`: the fraction of seeded pseudo-experiments whose Garwood interval contains the true mean. The seed is required and echoed with the toy count and confidence level.

`scripts/statistical_toys.py` provides four seeded toy diagnostics, each answering one narrow question under stated simplifications:

- `boundary --n N --b B`: the discovery statistic `q0` at the `s >= 0` boundary with a known background: the exact Poisson p-value, the seeded-toy p-value, the half-chi2 asymptotic form, naive Wilks (chi2, 1 dof, which doubles the p-value) and the fraction of toys at `q0 = 0` (about one half at large `B`). For the decision rule against Wilks near a boundary; an uncertain background is not covered.
- `template-bb --sig ... --bkg ... --n-data N --f F --mc-sig M --mc-bkg M`: the same toys with three fits compared: true templates, naive finite templates and a Barlow-Beeston-lite (Conway) per-bin nuisance. Reports bias, spread, pull width and coverage of the delta-lnL = 0.5 interval for each. A naive pull width above 1 with low coverage, restored towards 1 by the nuisance, is the evidence that template statistics must enter the likelihood. It is the per-bin total-count approximation, not the full per-template Barlow-Beeston fit.
- `ratio-cov --input FILE`: per-bin ratios (for example across rigidity) with each systematic given a per-bin fractional sigma for numerator and denominator, a numerator-denominator correlation `rho`, and a bin-to-bin correlation (`full`, `none` or `exponential` with a length in bins); reports the per-bin systematic spread, the bin-to-bin correlation matrix, and the weighted-mean spread against the independent-bins assumption (the underestimate factor).
- `template-stat --sig ... --bkg ... --n-data N --f F --mc-sig M --mc-bkg M`: a one-parameter template-fraction fit run with the true templates and with templates built from a finite Monte Carlo sample; reports the bias and the spread ratio (finite over true) and the fraction of fits at the boundary. It measures the cost of ignoring MC statistics; it is not a Barlow-Beeston fit.
- `unfold-scan --input FILE`: iterative (D'Agostini) unfolding of seeded toys of a supplied response matrix and truth (same orientation and efficiency convention as `validate_response.py`); reports the rms relative bias, spread and their sum per iteration. The bias is against the truth you supply, so the scan is circular: repeat with a different truth and prior before choosing an iteration count, and treat the stopping rule as a separate documented choice.
- `ratio-toys --n1 N --n2 N --sys name:sigma_num:sigma_den:rho`: the ratio of two Poisson counts with multiplicative systematic nuisances of declared numerator-denominator correlation; reports the statistical, systematic and total spread against the analytic residual, the "cancels" and the "independent" assumptions, plus the low-denominator bias. The correlation is your input; the script cannot determine it.

`scripts/likelihood_limits.py` provides profile-likelihood constructions for counting experiments (one signal strength `mu >= 0`, Gaussian-constrained background):

- `profile-limit --n N --b B --sigma-b S`: the asymptotic upper limit (`q-tilde = z^2`) and a seeded-toy-calibrated limit (common random numbers; for `S = 0` it is compared with the exact classical limit). The asymptotic limit undershoots at small counts; the toy limit is the reference and is toy-noise limited.
- `profile-significance --n N --b B --sigma-b S`: `q0` with the nuisance profiled, with the toy, half-chi2 asymptotic, naive Wilks and (for `S = 0`) exact Poisson p-values.
- `multibin-limit --input FILE`: bins sharing one `mu` with no, independent per-bin (Gaussian) or one common multiplicative background nuisance; the asymptotic observed limit, the Asimov median expected limit (no 1/2-sigma bands), and a seeded-toy p-value at the asymptotic limit as the calibration check (it should be near `1 - cl`). Shapes and other nuisances are not modeled.

`scripts/unfolding_diagnostics.py` works on a small response matrix (same orientation and efficiency convention as `validate_response.py`) with `--method` `dagostini` (iterations), `tikhonov` (curvature penalty, strength relative to the mean diagonal of `R^T W^2 R`) or `tsvd` (retained singular values of the Poisson-weighted response):

- `regularized-scan`: analytic bias and covariance of the linear methods per setting, the minimum adjacent-bin correlation (strongly negative means too weak a regularization), and the fraction of toys with a negative bin.
- `closure`: the noise-free closure of a different `test_truth` (the model dependence of the response weights and prior) with its bias significance against the statistical sigma, and seeded pulls (mean pull with its standard error, pull width).
- `fold-compare`: a power-law index from a forward-folded Poisson likelihood against an unfold-then-chi2 fit with the unfolded covariance; reports each bias and spread. It isolates statistical and regularization cost with the true spectral form assumed known.
- `response-stat`: the response redrawn from finite generated-event counts; reports the spread from data, from the response, from both, and the response share of the variance.

## Decision rules

- **[General method]** With `N` small against `B` the classical limit can be zero or negative; the script then reports no limit and says so. That is not a result: use `fc-interval` (a unified interval) or `cls-limit` (a limit with its expected band; S31, S36) and report the expected sensitivity with any limit. A Feldman-Cousins interval is a frequentist interval, not a CLs limit: do not label one as the other, and do not quote a CLs limit as having nominal coverage.
- **[General method]** With an uncertain background, prefer `profile-limit`, `profile-significance` or `multibin-limit` to a marginalized `--sigma-b` result, and compare the two: a difference is itself a systematic on the method. Check that the toy p-value at the asymptotic limit in `multibin-limit` is near `1 - cl`; if not, use the toy-calibrated construction. Do not call a profile limit a CLs limit (no CLs protection) and always report the expected sensitivity next to an observed limit.
- **[General method]** Run `regularized-scan` and `closure` before fixing a regularization strength: choose it with a stated criterion (for example the strength at which the closure bias on a different truth falls below a stated fraction of the statistical sigma and no adjacent correlation is below a stated value), not from the scan's own minimum, which is circular. A pull width above 1 or a mean pull beyond about 3 standard errors is a trigger to add an uncertainty or change the method; those thresholds are [Proposal], not AMS values. Run `fold-compare` when a parameter is fitted from an unfolded spectrum, and `response-stat` when the response comes from a finite MC sample.
- **[General method]** Near a physical boundary or with a weakly constrained parameter, run `boundary` before quoting a Wilks or asymptotic significance: if the toy and exact p-values differ from the asymptotic one, say so and use the toy or exact value (S30 for when asymptotics hold).
- **[General method]** If `template-bb` shows the naive pull width and coverage off, put the template statistics in the likelihood (Barlow-Beeston or Conway) rather than inflating the error by hand. Run `template-stat` when a template comes from a finite Monte Carlo sample or a data control sample; a spread ratio above about 1.1, or a bias above a stated fraction of the statistical error, is the trigger to put template statistics in the likelihood or enlarge the sample (that threshold is [Proposal], not an AMS value).
- **[General method]** Run `ratio-toys` before claiming that a ratio or fraction cancels a systematic; classify each effect as correlated, partial or independent with a stated `rho`, and keep the residual (invariant 5 of `SKILL.md`).
- **[General method]** For `N = 0` the classical limit on the signal is `-ln(1 - CL) - B`: it shrinks as the expected background `B` grows and is not positive once `B` reaches `-ln(1 - CL)`. It is `B`-independent only for a flat-prior Bayesian limit, which answers a different question. Never call the classical zero-count limit "independent of the background".
- **[General method]** A background is treated as exactly known. An uncertain background, nuisance parameters, or a template fit need a profile-likelihood or toy construction, not this script.
- **[General method]** Coverage of a discrete distribution oscillates with the true mean; a single-mean coverage number is a diagnostic, not a proof. Scan the mean before claiming coverage.
- **[Proposal]** Record the seed, toy count, confidence level and the script version next to any result that quotes a toy-based number.
- A limit on counts becomes a flux or ratio limit only through the exposure (`Phi_UL = N_UL / (E * DeltaX)`, with the exposure uncertainty propagated as a nuisance); see [inference-and-unfolding](inference-and-unfolding.md#rare-and-low-count-inference).

## Not implemented

A profile-likelihood treatment inside the Feldman-Cousins or CLs construction (CLs here has only the Poisson, optionally marginalized, form), shape and multiple nuisances in the limits, the full per-template Barlow-Beeston fit and multi-parameter template fits, regularization chosen by cross-validation or an L-curve, unfolding with the response-matrix covariance propagated analytically, forward folding with a free-form (non-parametric) truth, and ratio toys with a measured (not declared) covariance. These stay out because each would be a framework, not a diagnostic.

## Failure modes

- Quoting the classical limit when it is zero or negative.
- Reading a Feldman-Cousins lower bound of 0 as a failure, or as evidence for zero signal.
- Quoting an asymptotic limit or significance at small counts without the toy calibration; reporting a profile limit as CLs; treating a pull width near 1 on one truth as validation of the unfolding on another.
- Choosing a regularization strength or iteration count from a scan that used the same truth as its weights or prior; ignoring a strongly negative adjacent-bin correlation; letting a fitted index depend on the regularization without running `fold-compare`.
- Ignoring finite MC statistics in a response or template; assuming bins are independent when they share a systematic.
- Quoting a CLs limit without its expected band, or as a frequentist interval; reporting a marginalized-background result without varying `sigma_b`.
- Quoting a boundary significance from naive Wilks; choosing an unfolding iteration count from a scan that used the same truth as its prior; assuming a ratio cancels a systematic without a stated correlation.
- Using an exact interval for a count whose background is uncertain, as if the background were known.
- Reading one coverage number as proof of coverage; omitting the seed.
- Applying these limits to a mean above the script's range (500) without a validated approximation.

## Required source classes

Tier 4 methodology: Feldman and Cousins (S31), Junk (S36) for CLs, and Cowan et al. (S30) for profile-likelihood asymptotics and Asimov datasets and when they are valid. The formulas and toy models are textbook relations (iterative unfolding is D'Agostini's method, not an AMS-specific procedure unless a ledger claim says so, as for S06 and S08); no AMS numbers are involved.

## Questions to ask the user

How many events were observed, and is the background known or estimated with an uncertainty? Which confidence level and which construction (classical, Feldman-Cousins, CLs)? Is this a count limit or a flux or ratio limit, and what is the exposure and its uncertainty?
