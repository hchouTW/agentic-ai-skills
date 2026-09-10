---
role: Senior Experimental Particle Physicist
skill: hep-analysis
use_case: measuring a tag-and-probe trigger/identification efficiency with sideband background subtraction
---

## Scenario

An analysis needs the identification efficiency of a lepton-selection algorithm,
measured with the tag-and-probe method on a resonance decaying to two leptons
(a well-identified "tag" leg selects the event; the other, unbiased "probe" leg
is checked against the identification cut). Both the "pass" and "fail" probe
categories are dominated by resonance signal but still contain non-resonant
background under the mass peak, and that background populates the two
categories in very different proportions. The analyst has 5,200 probes in the
mass window in the pass category and 1,500 in the fail category, and needs the
identification efficiency and its uncertainty from these two samples.

## Common Weak Approach

```python
def selection_efficiency_weak(n_pass_window: int, n_fail_window: int) -> float:
    """Efficiency from raw window counts, no background subtraction."""
    return n_pass_window / (n_pass_window + n_fail_window)


N_PASS_WINDOW = 5200
N_FAIL_WINDOW = 1500

eff_weak = selection_efficiency_weak(N_PASS_WINDOW, N_FAIL_WINDOW)
print(f"efficiency (weak) = {eff_weak:.4f}")
# efficiency (weak) = 0.7761
```

`selection_efficiency_weak` treats every probe inside the mass window as a
genuine resonance decay, in both the pass and fail categories, and reports
**0.7761** with no uncertainty attached at all. It never asks how much of
either window is non-resonant background - per this skill's own guidance that
"tag-and-probe requires background modeling, pass/fail correlation, selection-
bias checks, signal-shape uncertainty, and closure," none of which happens
here. In this sample the background is far from evenly split: a sideband
study (not run by this approach) would show it makes up about 15% of the pass
window but 60% of the fail window, because non-resonant background probes are
disproportionately likely to fail the identification cut. Counting all of them
as failing signal probes inflates the fail count and drags the reported
efficiency down from its true value - a systematic bias with a sign and a
cause, not noise. Feeding these raw window counts straight into the shipped
binomial estimator (`scripts/tag_and_probe_efficiency.py`'s exact
Clopper-Pearson interval) would not fix this either: that tool is correct only
for a pure pass/total binomial count with no background component, which is
exactly the assumption this scenario violates.

## Expert-Level Best Practice

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class WindowYield:
    """A tag-and-probe mass-window count and its sideband-subtracted signal yield."""
    n_window: float          # raw probe count inside the mass window
    n_background: float      # background estimate under the peak, from sideband fit
    sigma_background: float  # uncertainty on that background estimate

    @property
    def n_signal(self) -> float:
        return self.n_window - self.n_background

    @property
    def var_signal(self) -> float:
        # Poisson variance of the raw window count, plus the (independent)
        # variance of the fitted/extrapolated background estimate.
        return self.n_window + self.sigma_background**2


def tag_and_probe_efficiency(pass_yield: WindowYield, fail_yield: WindowYield) -> dict[str, float]:
    signal_pass = pass_yield.n_signal
    signal_total = pass_yield.n_signal + fail_yield.n_signal
    efficiency = signal_pass / signal_total

    var_pass = pass_yield.var_signal
    var_total = pass_yield.var_signal + fail_yield.var_signal
    # Cov(signal_pass, signal_total) = Cov(A, A+D) = Var(A) + Cov(A,D) = Var(A):
    # pass and fail are complementary, independent probe categories, so
    # Cov(A,D) = 0 and the shared term reduces to Var(A).
    cov_pass_total = var_pass

    # references/04-histograms-efficiencies.md: Var(e) ~= Var(A)/B^2 +
    # A^2*Var(B)/B^4 - 2*A*Cov(A,B)/B^3, for e = A/B with B = A + D.
    var_efficiency = (
        var_pass / signal_total**2
        + signal_pass**2 * var_total / signal_total**4
        - 2 * signal_pass * cov_pass_total / signal_total**3
    )

    return {
        "signal_pass": signal_pass,
        "signal_total": signal_total,
        "efficiency": efficiency,
        "sigma_efficiency": var_efficiency**0.5,
    }


pass_yield = WindowYield(n_window=5200, n_background=800, sigma_background=60)
fail_yield = WindowYield(n_window=1500, n_background=900, sigma_background=70)

result = tag_and_probe_efficiency(pass_yield, fail_yield)
print(f"efficiency (expert) = {result['efficiency']:.4f} +/- {result['sigma_efficiency']:.4f}")
# efficiency (expert) = 0.8800 +/- 0.0143

# Systematic: repeat with an alternative sideband extrapolation model
# (e.g. exponential instead of linear background shape).
alt_pass_yield = WindowYield(n_window=5200, n_background=760, sigma_background=60)
alt_fail_yield = WindowYield(n_window=1500, n_background=950, sigma_background=70)
alt_result = tag_and_probe_efficiency(alt_pass_yield, alt_fail_yield)
background_model_syst = alt_result["efficiency"] - result["efficiency"]
print(f"efficiency (alt. background model) = {alt_result['efficiency']:.4f}")
print(f"background-model systematic = {background_model_syst:+.4f}")
# efficiency (alt. background model) = 0.8898
# background-model systematic = +0.0098
```

The expert version fits (or sideband-subtracts) the background separately in
the pass and fail categories, isolating a signal yield of 4,400 in pass and
600 in fail, before ever forming the ratio - so the 60%-background fail
category no longer inflates the denominator with non-signal probes. That alone
moves the efficiency from 0.7761 to **0.8800**, a shift more than six times the
statistical uncertainty on the corrected number. The uncertainty itself uses
the ratio-of-correlated-yields propagation from
`references/04-histograms-efficiencies.md` rather than treating pass and fail
counts as independent Poisson draws - `signal_total` shares `signal_pass`, and
skipping the covariance term would understate the true uncertainty. Finally,
repeating the whole extraction with an alternative background-shape model
shifts the efficiency by +0.0098, a shift of comparable size to the 0.0143
statistical uncertainty, so it is reported as its own dedicated background-
model systematic rather than folded silently into the central value.

## Key Takeaways

- Background does not populate pass and fail categories equally, so counting
  raw window totals as if they were pure signal introduces a *biased*
  efficiency, not merely a noisier one - here the bias is large enough (0.776
  vs. 0.880) to change conclusions, because non-resonant background is
  disproportionately concentrated in the fail category.
- Extract the signal yield in each category independently (fit or sideband
  subtraction) before forming the efficiency ratio. The weak approach's error
  is architectural: it forms the ratio first and never has a step where
  background could be separated out, whereas the expert version's
  `WindowYield.n_signal` isolates signal before `tag_and_probe_efficiency`
  ever sees a background-contaminated count.
- Propagate the efficiency uncertainty as a ratio of *correlated* quantities,
  not as if pass and fail were independent Poisson counts. `signal_total`
  contains `signal_pass` as a term, so the covariance in
  `Var(e) ~= Var(A)/B^2 + A^2*Var(B)/B^4 - 2*A*Cov(A,B)/B^3` is not optional -
  omitting it would report an efficiency uncertainty that does not match the
  actual estimator.
- Vary the background model itself and report the resulting shift as a
  dedicated systematic, per this skill's own tag-and-probe checklist
  ("background modeling ... signal-shape uncertainty, and closure"). A single
  central value from one background parameterization, with no check of how
  much that choice matters, silently treats a modeling choice as if it were a
  known truth.
