# Statistical Diagnostics: Exact Poisson Limits, Intervals, Seeded Coverage

## When to read this file

Read only when a low-count answer needs numbers that a rule alone cannot give: an exact Poisson upper limit or interval, the zero-count bound, or a seeded coverage check of an interval. The decisions themselves (when Gaussian, Wilks or S/sqrt(B) fail, boundary and non-regular problems, limits versus discovery) are in [inference-and-unfolding](inference-and-unfolding.md#rare-and-low-count-inference); do not load this file for those.

## Contents

1. [What the script does](#what-the-script-does)
2. [Decision rules](#decision-rules)
3. [Not implemented](#not-implemented)
4. [Failure modes](#failure-modes)
5. [Required source classes](#required-source-classes)
6. [Questions to ask the user](#questions-to-ask-the-user)

## What the script does

`scripts/poisson_diagnostics.py` (standard library; output labeled [General method]) provides three subcommands:

- `upper-limit --n N --b B --cl CL`: the classical one-sided upper limit on a signal mean for `N` observed events and a **known** background `B`, from `P(N' <= N | s + B) = 1 - CL`. For `N = 0`, `B = 0` it returns `-ln(1 - CL)` (about 3.00 at 95%).
- `interval --n N --cl CL`: the Garwood central interval on a Poisson mean, which is conservative (coverage at least `CL`).
- `coverage --mu MU --cl CL --toys T --seed S`: the fraction of seeded pseudo-experiments whose Garwood interval contains the true mean. The seed is required and echoed with the toy count and confidence level.

## Decision rules

- **[General method]** With `N` small against `B` the classical limit can be zero or negative; the script then reports no limit and says so. That is not a result: use a Feldman-Cousins or CLs construction with toys (S31, S36) and report the expected sensitivity, which this script does not compute.
- **[General method]** For `N = 0` the classical limit on the signal is `-ln(1 - CL) - B`: it shrinks as the expected background `B` grows and is not positive once `B` reaches `-ln(1 - CL)`. It is `B`-independent only for a flat-prior Bayesian limit, which answers a different question. Never call the classical zero-count limit "independent of the background".
- **[General method]** A background is treated as exactly known. An uncertain background, nuisance parameters, or a template fit need a profile-likelihood or toy construction, not this script.
- **[General method]** Coverage of a discrete distribution oscillates with the true mean; a single-mean coverage number is a diagnostic, not a proof. Scan the mean before claiming coverage.
- **[Proposal]** Record the seed, toy count, confidence level and the script version next to any result that quotes a toy-based number.
- A limit on counts becomes a flux or ratio limit only through the exposure (`Phi_UL = N_UL / (E * DeltaX)`, with the exposure uncertainty propagated as a nuisance); see [inference-and-unfolding](inference-and-unfolding.md#rare-and-low-count-inference).

## Not implemented

Profile-likelihood behavior at physical boundaries, Feldman-Cousins and CLs constructions, finite-template-statistics effects, unfolding closure, pull, prior and regularization scans, forward-folding versus unfolding comparisons, and correlated ratio or fraction toys. These were considered and deliberately left out: no routed decision needs them yet, and each would be a framework, not a diagnostic.

## Failure modes

- Quoting the classical limit when it is zero or negative.
- Using an exact interval for a count whose background is uncertain, as if the background were known.
- Reading one coverage number as proof of coverage; omitting the seed.
- Applying these limits to a mean above the script's range (500) without a validated approximation.

## Required source classes

Tier 4 methodology: Feldman and Cousins (S31), Junk (S36) for CLs, and Cowan et al. (S30) for when asymptotic formulae are valid. The script's formulas are textbook Poisson relations; no AMS numbers are involved.

## Questions to ask the user

How many events were observed, and is the background known or estimated with an uncertainty? Which confidence level and which construction (classical, Feldman-Cousins, CLs)? Is this a count limit or a flux or ratio limit, and what is the exposure and its uncertainty?
