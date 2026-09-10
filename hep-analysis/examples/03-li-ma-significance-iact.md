---
role: Astroparticle Physicist / IACT Analyst
skill: hep-analysis
use_case: computing the detection significance of a candidate gamma-ray source from on-source/off-source counts in an imaging atmospheric Cherenkov telescope (IACT) analysis
---

## Scenario

A wobble-mode IACT observation of a candidate gamma-ray source counts 10
events in the ON region (the source direction) and 20 events in 5 combined OFF
regions (background-control regions with equal acceptance but no expected
signal), giving a background normalization `alpha = 1/5 = 0.2`. The candidate
position was one of 25 statistically independent positions searched in a
blind scan of the surrounding field of view. The analyst needs the detection
significance of this excess, and whether it survives correcting for the scan.

## Common Weak Approach

```python
import math

N_ON = 10
N_OFF = 20
ALPHA = 0.2


def naive_gaussian_significance(n_on: float, n_off: float, alpha: float) -> float:
    """(N_on - alpha*N_off) / sqrt(N_on + alpha^2*N_off) -- a Gaussian
    approximation, not the field-standard likelihood-ratio statistic."""
    excess = n_on - alpha * n_off
    variance = n_on + alpha**2 * n_off
    return excess / math.sqrt(variance)


significance = naive_gaussian_significance(N_ON, N_OFF, ALPHA)
print(f"significance (naive Gaussian) = {significance:.3f} sigma")
# significance (naive Gaussian) = 1.826 sigma
print("reported as a single-trial result; scan not corrected for.")
```

`naive_gaussian_significance` treats the excess as Gaussian-distributed and
reports **1.826 sigma** as if it were the final answer, with no correction for
the 25 independent positions actually searched. Both choices are flagged by
this skill's own guidance in `references/39-astroparticle-statistics.md`: the
Gaussian formula "require[s] large counts" to be valid and is not "the field
standard" precisely because `N_on = 10` and `N_off = 20` are low counts, not
the asymptotic regime it assumes; and quoting a single candidate position's
significance from a blind scan without a trials correction reports "only the
one presented" instead of accounting for "all of them," which the reference
explicitly calls out as the discipline required.

## Expert-Level Best Practice

```python
import math
from statistics import NormalDist

N_ON = 10
N_OFF = 20
ALPHA = 0.2
N_INDEPENDENT_TRIALS = 25  # independent positions searched in the blind scan

_NORMAL = NormalDist()


def _log_term(count: float, factor: float, ratio: float) -> float:
    """count * ln(factor * ratio), defined as 0 when count == 0 (0*ln(0) := 0)."""
    if count == 0:
        return 0.0
    return count * math.log(factor * ratio)


def li_ma_significance(n_on: float, n_off: float, alpha: float) -> float:
    """Li & Ma (1983) likelihood-ratio significance for ON/OFF counting.
    See references/39-astroparticle-statistics.md and scripts/li_ma_significance.py."""
    total = n_on + n_off
    on_term = _log_term(n_on, (1.0 + alpha) / alpha, n_on / total)
    off_term = _log_term(n_off, 1.0 + alpha, n_off / total)
    radicand = max(2.0 * (on_term + off_term), 0.0)
    sign = 1.0 if n_on >= alpha * n_off else -1.0
    return sign * math.sqrt(radicand)


def trials_corrected_significance(local_significance: float, n_trials: int) -> float:
    """Convert a local significance into a global significance via a
    Sidak-style correction for n_trials independent, uncorrelated trials."""
    p_local = 1.0 - _NORMAL.cdf(local_significance)
    p_global = 1.0 - (1.0 - p_local) ** n_trials
    return _NORMAL.inv_cdf(1.0 - p_global)


local_sig = li_ma_significance(N_ON, N_OFF, ALPHA)
global_sig = trials_corrected_significance(local_sig, N_INDEPENDENT_TRIALS)

print(f"significance (Li & Ma, local)  = {local_sig:.3f} sigma")
print(f"significance (Li & Ma, global) = {global_sig:.3f} sigma, "
      f"after correcting for {N_INDEPENDENT_TRIALS} independent trial positions")
# significance (Li & Ma, local)  = 2.222 sigma
# significance (Li & Ma, global) = 0.578 sigma, after correcting for 25 independent trial positions
```

The Li & Ma formula already differs materially from the naive Gaussian
estimate at these low counts: 2.222 sigma against 1.826 sigma for the exact
same `N_on`, `N_off`, and `alpha` - a discrepancy the Gaussian approximation
cannot be trusted to bound in either direction at this count, which is exactly
why `references/39-astroparticle-statistics.md` calls the likelihood-ratio
statistic, not the Gaussian formula, the field standard. But the more decisive
correction is the second one: this candidate was one of 25 independent
positions searched, and applying the trials correction from
`trials_corrected_significance` collapses the local 2.222 sigma into a global
**0.578 sigma** - nowhere near a detection. Reporting the local 2.222 sigma
number alone, as a single-trial result, would have been a false-positive claim
built entirely from not accounting for how many other positions were also
searched and could equally well have produced an upward fluctuation.

## Key Takeaways

- Use the Li & Ma (1983) likelihood-ratio significance, not the Gaussian
  `(N_on - alpha*N_off)/sqrt(N_on + alpha^2*N_off)` approximation, for ON/OFF
  counting at low counts - the two formulas are not interchangeable
  approximations of the same quantity; the Gaussian form is derived assuming
  large counts that do not hold here, so it has no guaranteed relationship to
  the correct likelihood-ratio answer in either direction.
- A significance computed for one candidate position out of many searched is a
  *local* significance, not the quantity that answers "is this a real
  detection" - the number that answers that question is the *global*
  significance, corrected for every independent trial actually performed, not
  only the one being reported.
- The trials correction can change the conclusion entirely, not just the third
  decimal place: a "2.2 sigma" local excess became "0.6 sigma" globally once
  25 independent search positions were accounted for, the difference between a
  claim worth investigating further and one indistinguishable from a
  background fluctuation.
- State the counting method, the exact `N_on`/`N_off`/`alpha` used, and the
  number of independent trials and how it was estimated, as this skill's own
  deliverables checklist requires - a significance number reported without
  those three pieces of provenance cannot be checked or reproduced by a
  reader.
