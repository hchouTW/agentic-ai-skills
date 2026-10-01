#!/usr/bin/env python3
"""Profile-likelihood limits and significance for counting experiments (approximations).

Purpose: give the "treat the background as a nuisance, do not assume Wilks near a boundary"
rule an executable form for small counting problems. This is not a statistics framework:
it covers a single-bin or multi-bin counting model with one signal strength mu >= 0, a
Gaussian-constrained background, the one-sided boundary statistic q-tilde, an asymptotic
result and a seeded toy calibration. Output is labeled [General method]; nothing here is
AMS performance. Seed, toy count and configuration are echoed.

Subcommands:
  profile-limit         single bin: n events, background b +- sigma_b (Gaussian constraint).
                        Asymptotic upper limit (q-tilde = z^2) and a toy-calibrated limit
                        (seeded, common random numbers across the scan); for sigma_b = 0 the toy
                        limit is compared with the exact classical limit.
  profile-significance  single bin: q0 with the nuisance profiled; asymptotic half-chi2 p-value,
                        seeded-toy p-value, naive Wilks (chi2, 1 dof) and, for sigma_b = 0, the
                        exact Poisson tail.
  multibin-limit        several bins sharing one mu, from a JSON file: asymptotic observed
                        limit, Asimov median expected limit, and a seeded-toy p-value at the
                        asymptotic limit (the calibration check). Background nuisance: none,
                        independent per bin (Gaussian), or one common multiplicative scale.

multibin-limit input: {"bins": [{"n": 5, "b": 3.2, "s": 1.0}, ...], "cl": 0.95,
  "background_uncertainty": {"kind": "none" | "independent" | "common_scale", "sigma": [per-bin
  absolute sigma_b] (independent) | fractional scalar (common_scale)}}; "s" is the signal
  expected in the bin per unit mu.

Usage (from the skill directory):
  python3 scripts/likelihood_limits.py profile-limit --n 5 --b 3 --sigma-b 1 --cl 0.95 --toys 4000 --seed 1
  python3 scripts/likelihood_limits.py profile-significance --n 15 --b 8 --sigma-b 2 --toys 20000 --seed 1
  python3 scripts/likelihood_limits.py multibin-limit --input bins.json --toys 500 --seed 1
Exit codes: 0 ok; 2 rejected input. Standard library only.
Importable: profile_limit, profile_significance, multibin_limit.
"""
from __future__ import annotations

import argparse
import json
import math
import random
import sys
from pathlib import Path
from statistics import NormalDist

LABEL = "[General method]"
MAX_MEAN = 500.0
NEG = -1e300


class LikelihoodError(ValueError):
    """Raised for invalid counts, backgrounds, seeds, toy numbers or model files."""


def _num(x, name, low=None, high=None, strict_low=False) -> float:
    ok = isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x)
    if not ok:
        raise LikelihoodError(f"{name} must be a finite number, got {x!r}")
    if low is not None and (x < low or (strict_low and x == low)):
        raise LikelihoodError(f"{name} must be {'>' if strict_low else '>='} {low}, got {x!r}")
    if high is not None and x > high:
        raise LikelihoodError(f"{name} must be <= {high}, got {x!r}")
    return float(x)


def _seed_toys(toys, seed, allow_zero=False) -> tuple[int, int]:
    if isinstance(seed, bool) or not isinstance(seed, int):
        raise LikelihoodError("seed must be an integer and must be recorded")
    if isinstance(toys, bool) or not isinstance(toys, int) or not ((allow_zero and toys == 0) or 100 <= toys <= 100000):
        raise LikelihoodError("toys must be an integer in [100, 100000]" + (" or 0" if allow_zero else ""))
    return toys, seed


def _ppf(u: float, mu: float) -> int:
    """Poisson quantile by cumulative summation (mu <= MAX_MEAN)."""
    if mu <= 0.0:
        return 0
    term = cum = math.exp(-mu)
    k = 0
    while u > cum and k < 20 * int(mu + 20):
        k += 1
        term *= mu / k
        cum += term
    return k


def _lnl(n: float, mu: float) -> float:
    if mu <= 0.0:
        return 0.0 if n == 0 else NEG
    return (n * math.log(mu) if n > 0 else 0.0) - mu


# ------------------------------------------------------------------- single bin
def _b_hat(n: float, s: float, b0: float, sig: float) -> float:
    """Profiled background for Poisson(n | s + b) x Normal(b0 | b, sig)."""
    if sig == 0.0:
        return b0
    a = sig * sig + s - b0
    c = s * (sig * sig - b0) - n * sig * sig
    return max((-a + math.sqrt(max(a * a - 4.0 * c, 0.0))) / 2.0, 0.0)


def _ll1(n: float, s: float, b: float, b0: float, sig: float) -> float:
    return _lnl(n, s + b) - ((b - b0) ** 2 / (2.0 * sig * sig) if sig > 0 else 0.0)


def _q1(n: float, b0: float, sig: float, s: float) -> float:
    """One-sided boundary statistic q-tilde_s (0 when the best-fit signal exceeds s)."""
    s_hat = n - b0 if n >= b0 else 0.0
    if s_hat > s:
        return 0.0
    ll_max = _ll1(n, s_hat, _b_hat(n, s_hat, b0, sig), b0, sig)
    return max(0.0, 2.0 * (ll_max - _ll1(n, s, _b_hat(n, s, b0, sig), b0, sig)))


def _q0(n: float, b0: float, sig: float) -> float:
    """Discovery statistic q0 (0 when the best-fit signal is not positive)."""
    s_hat = n - b0
    if s_hat <= 0.0:
        return 0.0
    ll_max = _ll1(n, s_hat, b0, b0, sig)
    return max(0.0, 2.0 * (ll_max - _ll1(n, 0.0, _b_hat(n, 0.0, b0, sig), b0, sig)))


def _inputs1(n, b, sigma_b):
    if isinstance(n, bool) or not isinstance(n, int) or n < 0:
        raise LikelihoodError(f"n must be a non-negative integer, got {n!r}")
    return n, _num(b, "b", 0.0, 200.0), _num(sigma_b, "sigma_b", 0.0, 100.0)


def _bisect(f, lo: float, hi: float, iters: int = 80) -> float:
    """Root of an increasing f on [lo, hi]."""
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        lo, hi = (mid, hi) if f(mid) < 0 else (lo, mid)
    return 0.5 * (lo + hi)


def _toy_p1(n_obs, b0, sig, s, uniforms, gauss) -> float:
    q_obs = _q1(n_obs, b0, sig, s)
    bh = _b_hat(n_obs, s, b0, sig)
    hits = 0
    for u, z in zip(uniforms, gauss):
        nn = _ppf(u, s + bh)
        bb = max(bh + sig * z, 0.0) if sig > 0 else bh
        hits += _q1(nn, bb, sig, s) >= q_obs - 1e-12
    return hits / len(uniforms)


def profile_limit(n: int, b: float, sigma_b: float, cl: float, toys: int, seed: int) -> dict:
    n, b, sig = _inputs1(n, b, sigma_b)
    cl = _num(cl, "cl", 0.0, 1.0, strict_low=True)
    if cl >= 1.0:
        raise LikelihoodError("cl must lie strictly between 0 and 1")
    toys, seed = _seed_toys(toys, seed)
    z = NormalDist().inv_cdf(cl)
    s_hat = max(n - b, 0.0)
    hi = s_hat + 20.0 * (math.sqrt(n + 1.0) + sig) + 20.0
    if hi + b + 6.0 * sig > MAX_MEAN:
        raise LikelihoodError("inputs reach a mean above the script's range (500)")
    s_asym = _bisect(lambda s: _q1(n, b, sig, s) - z * z, s_hat, hi)
    rng = random.Random(seed)
    uniforms = [rng.random() for _ in range(toys)]
    gauss = [rng.gauss(0.0, 1.0) for _ in range(toys)]
    alpha = 1.0 - cl
    s_toy = _bisect(lambda s: alpha - _toy_p1(n, b, sig, s, uniforms, gauss), s_hat, hi, 30)
    out = {"label": LABEL, "method": "profile-likelihood upper limit on s, single bin, Gaussian-constrained background",
           "n_obs": n, "b": b, "sigma_b": sig, "cl": cl, "toys": toys, "seed": seed,
           "asymptotic_upper_limit": s_asym, "toy_calibrated_upper_limit": s_toy,
           "asymptotic_over_toy": s_asym / s_toy if s_toy > 0 else None}
    if sig == 0.0:
        from poisson_diagnostics import upper_limit
        exact = upper_limit(n, b, cl)["upper_limit_on_signal"]
        out["exact_classical_upper_limit"] = exact
    out["note"] = ("the asymptotic limit uses q-tilde = z^2 (z = Phi^-1(cl)) and is poor at small counts; the toy limit "
                   "calibrates q-tilde with seeded toys generated at the conditional (profiled) background and a "
                   "Gaussian auxiliary measurement, uses common random numbers across the scan (a step-wise, "
                   "toy-noise-limited estimate), and is a profile construction without CLs protection: a downward "
                   "fluctuation can give a limit that excludes signals the experiment cannot test, so also "
                   "report the expected sensitivity (cls-limit in poisson_diagnostics.py for a counting experiment)")
    return out


def profile_significance(n: int, b: float, sigma_b: float, toys: int, seed: int) -> dict:
    n, b, sig = _inputs1(n, b, sigma_b)
    if b <= 0.0:
        raise LikelihoodError("b must be > 0 for the discovery statistic")
    toys, seed = _seed_toys(toys, seed)
    q_obs = _q0(n, b, sig)
    bh = _b_hat(n, 0.0, b, sig)
    rng = random.Random(seed)
    hits = zero = 0
    for _ in range(toys):
        nn = _ppf(rng.random(), bh)
        bb = max(bh + sig * rng.gauss(0.0, 1.0), 0.0) if sig > 0 else bh
        q = _q0(nn, bb, sig)
        hits += q >= q_obs - 1e-12
        zero += q == 0.0
    z = math.sqrt(q_obs)
    out = {"label": LABEL, "method": "profile-likelihood q0 with a Gaussian-constrained background, seeded toys",
           "n_obs": n, "b": b, "sigma_b": sig, "toys": toys, "seed": seed, "q0_observed": q_obs,
           "p_value_toys": hits / toys, "binomial_error_on_p_toys": math.sqrt(max(hits / toys * (1 - hits / toys), 0) / toys),
           "p_value_half_chi2_asymptotic": 0.5 * math.erfc(z / math.sqrt(2.0)) if q_obs > 0 else 0.5,
           "p_value_naive_wilks_chi2_1dof": math.erfc(z / math.sqrt(2.0)) if q_obs > 0 else 1.0,
           "fraction_toys_with_q0_zero": zero / toys}
    if sig == 0.0:
        term = cum = math.exp(-b)
        for k in range(1, n):
            term *= b / k
            cum += term
        out["p_value_exact_poisson"] = 1.0 if n == 0 else 1.0 - cum
    out["note"] = ("toys are generated at s = 0 with the profiled background and a Gaussian auxiliary measurement; the "
                   "p-value is local, with no trial factor; a significance quoted from naive Wilks is wrong near the "
                   "boundary; the Gaussian constraint treats the background uncertainty as symmetric and unbounded, "
                   "which is a poor model for a large sigma_b/b (use a gamma or log-normal constraint then)")
    return out


# --------------------------------------------------------------------- multibin
class _Model:
    def __init__(self, bins, kind, sigma):
        self.n_bins = len(bins)
        self.s = [x["s"] for x in bins]
        self.b = [x["b"] for x in bins]
        self.kind, self.sigma = kind, sigma

    def aux_obs(self):
        return list(self.b) if self.kind == "independent" else ([1.0] if self.kind == "common_scale" else [])

    def _prof_nu(self, ns, aux, mu):
        """Profiled lnL at fixed mu, and the profiled nuisance values."""
        if self.kind == "none":
            return sum(_lnl(n, mu * s + b) for n, s, b in zip(ns, self.s, self.b)), []
        if self.kind == "independent":
            tot, hats = 0.0, []
            for n, s, b0, sg in zip(ns, self.s, aux, self.sigma):
                bh = _b_hat(n, mu * s, b0, sg)
                hats.append(bh)
                tot += _ll1(n, mu * s, bh, b0, sg)
            return tot, hats
        sg, th0 = self.sigma, aux[0]

        def deriv(t):
            return sum((n * b / (mu * s + t * b) - b) if (mu * s + t * b) > 0 else (-b if n == 0 else 1e12)
                       for n, s, b in zip(ns, self.s, self.b)) - (t - th0) / (sg * sg)

        lo, hi = 0.0, th0 + 12.0 * sg + 5.0
        if deriv(lo) <= 0:
            t = 0.0
        else:
            for _ in range(80):
                mid = 0.5 * (lo + hi)
                lo, hi = (mid, hi) if deriv(mid) > 0 else (lo, mid)
            t = 0.5 * (lo + hi)
        tot = sum(_lnl(n, mu * s + t * b) for n, s, b in zip(ns, self.s, self.b)) - (t - th0) ** 2 / (2 * sg * sg)
        return tot, [t]

    def fit(self, ns, aux):
        """Global maximum over mu >= 0 (golden section of the profiled lnL)."""
        mu_max = (sum(ns) + 10.0 * math.sqrt(sum(ns) + 1.0) + 20.0) / max(sum(self.s), 1e-12) * 5.0
        lo, hi, g = 0.0, mu_max, (math.sqrt(5) - 1) / 2
        x1, x2 = hi - g * (hi - lo), lo + g * (hi - lo)
        f1, f2 = self._prof_nu(ns, aux, x1)[0], self._prof_nu(ns, aux, x2)[0]
        for _ in range(70):
            if f1 < f2:
                lo, x1, f1 = x1, x2, f2
                x2 = lo + g * (hi - lo)
                f2 = self._prof_nu(ns, aux, x2)[0]
            else:
                hi, x2, f2 = x2, x1, f1
                x1 = hi - g * (hi - lo)
                f1 = self._prof_nu(ns, aux, x1)[0]
        mu_hat = 0.5 * (lo + hi)
        f0 = self._prof_nu(ns, aux, 0.0)[0]
        fm = self._prof_nu(ns, aux, mu_hat)[0]
        return (0.0, f0) if f0 >= fm else (mu_hat, fm)

    def q(self, ns, aux, mu, fit=None):
        mu_hat, ll_max = fit if fit else self.fit(ns, aux)
        if mu_hat > mu:
            return 0.0
        return max(0.0, 2.0 * (ll_max - self._prof_nu(ns, aux, mu)[0]))


def _load_model(doc):
    if not isinstance(doc, dict):
        raise LikelihoodError("input must be a JSON object")
    raw = doc.get("bins")
    if not isinstance(raw, list) or not 1 <= len(raw) <= 50:
        raise LikelihoodError("bins must be a list of 1 to 50 bins")
    bins = []
    for i, x in enumerate(raw):
        if not isinstance(x, dict):
            raise LikelihoodError(f"bin {i} must be an object with n, b, s")
        n = x.get("n")
        if isinstance(n, bool) or not isinstance(n, (int, float)) or n < 0 or n != int(n):
            raise LikelihoodError(f"bin {i}: n must be a non-negative integer")
        bins.append({"n": int(n), "b": _num(x.get("b"), f"bin {i} b", 0.0, 200.0), "s": _num(x.get("s"), f"bin {i} s", 0.0, 1e6)})
    if sum(x["s"] for x in bins) <= 0:
        raise LikelihoodError("at least one bin needs a positive signal expectation s")
    if sum(x["n"] for x in bins) > 400:
        raise LikelihoodError("total counts above 400 are outside this script's range")
    unc = doc.get("background_uncertainty", {"kind": "none"})
    kind = unc.get("kind") if isinstance(unc, dict) else None
    if kind not in ("none", "independent", "common_scale"):
        raise LikelihoodError("background_uncertainty.kind must be none, independent or common_scale")
    sigma = None
    if kind == "independent":
        sg = unc.get("sigma")
        if not isinstance(sg, list) or len(sg) != len(bins):
            raise LikelihoodError("independent needs one sigma per bin")
        sigma = [_num(v, "sigma", 0.0, 100.0) for v in sg]
    elif kind == "common_scale":
        sigma = _num(unc.get("sigma"), "sigma", 0.0, 2.0, strict_low=True)
    return bins, kind, sigma


def _limit_model(model, ns, aux, z):
    mu_hat, _ = fit = model.fit(ns, aux)
    hi = mu_hat + 30.0 * (math.sqrt(sum(ns) + 1.0) + 1.0) / max(sum(model.s), 1e-12) + 20.0 / max(sum(model.s), 1e-12)
    return _bisect(lambda m: model.q(ns, aux, m, fit) - z * z, mu_hat, hi, 70)


def multibin_limit(doc: dict, cl: float, toys: int, seed: int) -> dict:
    bins, kind, sigma = _load_model(doc)
    cl = _num(doc.get("cl", cl), "cl", 0.0, 1.0, strict_low=True)
    if cl >= 1.0:
        raise LikelihoodError("cl must lie strictly between 0 and 1")
    toys, seed = _seed_toys(toys, seed, allow_zero=True)
    model = _Model(bins, kind, sigma)
    ns = [x["n"] for x in bins]
    aux = model.aux_obs()
    z = NormalDist().inv_cdf(cl)
    obs = _limit_model(model, ns, aux, z)
    asimov = _limit_model(model, [x["b"] for x in bins], aux, z)
    mu_hat, _ = model.fit(ns, aux)
    out = {"label": LABEL, "method": "multi-bin profile-likelihood upper limit on mu, shared signal strength",
           "bins": len(bins), "background_uncertainty": kind, "cl": cl, "seed": seed, "toys": toys,
           "best_fit_mu": mu_hat, "asymptotic_observed_upper_limit": obs,
           "asymptotic_asimov_median_expected_limit": asimov}
    if toys:
        q_obs = model.q(ns, aux, obs)
        _, cond = model._prof_nu(ns, aux, obs)
        rng = random.Random(seed)
        hits = 0
        for _ in range(toys):
            if kind == "none":
                means = [obs * s + b for s, b in zip(model.s, model.b)]
                a = []
            elif kind == "independent":
                means = [obs * s + c for s, c in zip(model.s, cond)]
                a = [max(c + sg * rng.gauss(0, 1), 0.0) for c, sg in zip(cond, sigma)]
            else:
                means = [obs * s + cond[0] * b for s, b in zip(model.s, model.b)]
                a = [max(cond[0] + sigma * rng.gauss(0, 1), 0.0)]
            nn = [_ppf(rng.random(), m) for m in means]
            hits += model.q(nn, a, obs) >= q_obs - 1e-12
        p = hits / toys
        out["toy_p_value_at_asymptotic_limit"] = p
        out["binomial_error_on_p"] = math.sqrt(max(p * (1 - p), 0.0) / toys)
        out["target_p_value"] = 1.0 - cl
    out["note"] = ("asymptotic results rely on q-tilde ~ half-chi2; the toy p-value at the asymptotic limit is the "
                   "calibration check (it should be near 1 - cl; a p-value far from it means the asymptotic limit "
                   "is mis-calibrated here); the Asimov median is the expected limit under background only, with no "
                   "1/2-sigma bands; the Gaussian nuisances are symmetric, a common-scale nuisance multiplies the "
                   "nominal backgrounds, bins are independent Poisson, and shape uncertainties are not modeled")
    return out


# -------------------------------------------------------------------------- CLI
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0], formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    def common(p, toys):
        p.add_argument("--toys", type=int, default=toys)
        p.add_argument("--seed", type=int, required=True, help="required: every toy study records its seed")

    a = sub.add_parser("profile-limit", help="single-bin profile-likelihood upper limit")
    a.add_argument("--n", type=int, required=True)
    a.add_argument("--b", type=float, required=True)
    a.add_argument("--sigma-b", type=float, default=0.0)
    a.add_argument("--cl", type=float, default=0.95)
    common(a, 4000)
    c = sub.add_parser("profile-significance", help="single-bin profile-likelihood q0")
    c.add_argument("--n", type=int, required=True)
    c.add_argument("--b", type=float, required=True)
    c.add_argument("--sigma-b", type=float, default=0.0)
    common(c, 20000)
    m = sub.add_parser("multibin-limit", help="multi-bin profile-likelihood upper limit")
    m.add_argument("--input", required=True)
    m.add_argument("--cl", type=float, default=0.95, help="used when the file has no cl")
    common(m, 500)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "profile-limit":
            result = profile_limit(args.n, args.b, args.sigma_b, args.cl, args.toys, args.seed)
        elif args.command == "profile-significance":
            result = profile_significance(args.n, args.b, args.sigma_b, args.toys, args.seed)
        else:
            try:
                doc = json.loads(Path(args.input).read_text())
            except (OSError, json.JSONDecodeError) as exc:
                raise LikelihoodError(f"cannot read {args.input}: {exc}") from None
            result = multibin_limit(doc, args.cl, args.toys, args.seed)
    except LikelihoodError as exc:
        print(json.dumps({"label": LABEL, "status": "rejected", "error": str(exc)}, indent=2))
        return 2
    result["status"] = "ok"
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
