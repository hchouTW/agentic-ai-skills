#!/usr/bin/env python3
"""Small exact-Poisson diagnostics for low-count AMS-style decisions.

Purpose: give the "use Poisson-exact, not Gaussian/Wilks/S-over-sqrt-B" rule an
executable form: exact upper limits and central intervals on a Poisson mean, the
zero-count bound, and a seeded toy coverage check of the interval. This is not a
statistics framework: it does not do profile likelihood, CLs, or unfolding.

What it does: (1) `upper-limit`: classical one-sided upper limit on a signal mean s
for n observed events and a KNOWN background b, found by solving P(N <= n | s + b) =
1 - CL; when the limit is <= 0 (n small versus b) it says the classical construction is
unphysical there and a Feldman-Cousins or CLs construction with toys is needed.
(2) `interval`: Garwood central interval on a Poisson mean (conservative). (3)
`coverage`: fraction of seeded pseudo-experiments whose interval contains the true mean.
Approximations are stated in the output ("[General method]"); seed, toy count and
configuration are always echoed so a run is reproducible.

Usage (from the skill directory):
  python3 scripts/poisson_diagnostics.py upper-limit --n 0 --b 0 --cl 0.95
  python3 scripts/poisson_diagnostics.py interval --n 3 --cl 0.6827
  python3 scripts/poisson_diagnostics.py coverage --mu 2.5 --cl 0.6827 --toys 20000 --seed 1
Exit codes: 0 ok; 2 rejected input. Standard library only.
Importable: poisson_cdf, upper_limit, central_interval, coverage.
"""
from __future__ import annotations

import argparse
import json
import math
import random
import sys

LABEL = "[General method]"
MAX_MEAN = 500.0  # inversion sampling and exp(-mu) stay accurate below this


class DiagnosticsError(ValueError):
    """Raised for invalid counts, backgrounds, confidence levels or means."""


def _count(n) -> int:
    if isinstance(n, bool) or not isinstance(n, int) or n < 0:
        raise DiagnosticsError(f"n must be a non-negative integer, got {n!r}")
    return n


def _cl(cl) -> float:
    if isinstance(cl, bool) or not isinstance(cl, (int, float)) or not 0.0 < cl < 1.0:
        raise DiagnosticsError(f"cl must lie strictly between 0 and 1, got {cl!r}")
    return float(cl)


def _mean(mu, name="mean", allow_zero=True) -> float:
    ok = isinstance(mu, (int, float)) and not isinstance(mu, bool) and math.isfinite(mu)
    if not ok or mu < 0 or (mu == 0 and not allow_zero):
        raise DiagnosticsError(f"{name} must be a finite non-negative number, got {mu!r}")
    if mu > MAX_MEAN:
        raise DiagnosticsError(f"{name} {mu} exceeds {MAX_MEAN}; use a Gaussian-validated method there")
    return float(mu)


def poisson_cdf(n: int, mu: float) -> float:
    """P(N <= n) for a Poisson mean mu, by direct summation."""
    n, mu = _count(n), _mean(mu)
    if mu == 0.0:
        return 1.0
    term = total = math.exp(-mu)
    for k in range(1, n + 1):
        term *= mu / k
        total += term
    return min(total, 1.0)


def _solve(f, lo: float, hi: float) -> float:
    """Root of a decreasing f on [lo, hi] by bisection."""
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if f(mid) > 0:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def upper_limit(n: int, b: float, cl: float = 0.95) -> dict:
    """Classical one-sided upper limit on the signal mean s: P(N <= n | s + b) = 1 - cl."""
    n, b, cl = _count(n), _mean(b, "b"), _cl(cl)
    alpha = 1.0 - cl
    total = _solve(lambda mu: poisson_cdf(n, mu) - alpha, 0.0, MAX_MEAN)  # limit on s + b
    s_ul = total - b
    out = {"label": LABEL, "method": "classical Poisson upper limit, known background", "n_obs": n, "b": b, "cl": cl,
           "upper_limit_on_total_mean": total, "upper_limit_on_signal": s_ul}
    if s_ul <= 0:
        out["upper_limit_on_signal"] = None
        out["warning"] = ("classical limit is <= 0: fewer events than the background expects; the construction is "
                          "unphysical here (a negative or empty limit is not a result). Use Feldman-Cousins or CLs "
                          "with toys and report the expected sensitivity")
    if n == 0 and b == 0:
        out["check_minus_ln_alpha"] = -math.log(alpha)
    return out


def central_interval(n: int, cl: float = 0.6827) -> dict:
    """Garwood central interval on a Poisson mean (conservative: coverage >= cl)."""
    n, cl = _count(n), _cl(cl)
    tail = (1.0 - cl) / 2.0
    lower = 0.0
    if n > 0:  # P(N >= n | mu) increases with mu; find mu with P(N >= n | mu) = tail
        lo, hi = 0.0, MAX_MEAN
        for _ in range(200):
            mid = 0.5 * (lo + hi)
            if 1.0 - poisson_cdf(n - 1, mid) < tail:
                lo = mid
            else:
                hi = mid
        lower = 0.5 * (lo + hi)
    upper = _solve(lambda mu: poisson_cdf(n, mu) - tail, 0.0, MAX_MEAN)
    return {"label": LABEL, "method": "Garwood central interval (conservative)", "n_obs": n, "cl": cl,
            "lower": lower, "upper": upper}


def _draw(rng: random.Random, mu: float) -> int:
    """Poisson variate by inversion of the CDF (exact for mu <= MAX_MEAN)."""
    u, k = rng.random(), 0
    term = total = math.exp(-mu)
    while u > total and k < 10 * int(mu + 10):
        k += 1
        term *= mu / k
        total += term
    return k


def coverage(mu: float, cl: float, toys: int, seed: int) -> dict:
    """Fraction of seeded pseudo-experiments whose Garwood interval contains the true mean mu."""
    mu, cl = _mean(mu, "mu", allow_zero=False), _cl(cl)
    if isinstance(toys, bool) or not isinstance(toys, int) or toys < 100:
        raise DiagnosticsError("toys must be an integer >= 100")
    if isinstance(seed, bool) or not isinstance(seed, int):
        raise DiagnosticsError("seed must be an integer and must be recorded")
    rng, cache, hits = random.Random(seed), {}, 0
    for _ in range(toys):
        n = _draw(rng, mu)
        if n not in cache:
            iv = central_interval(n, cl)
            cache[n] = (iv["lower"], iv["upper"])
        lo, hi = cache[n]
        hits += lo <= mu <= hi
    frac = hits / toys
    return {"label": LABEL, "method": "seeded toy coverage of the Garwood interval", "true_mean": mu, "cl": cl,
            "toys": toys, "seed": seed, "coverage": frac,
            "binomial_error_on_coverage": math.sqrt(max(frac * (1 - frac), 0.0) / toys),
            "note": "coverage at a single true mean; scan mu, coverage oscillates for discrete counts"}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0], formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    u = sub.add_parser("upper-limit", help="classical upper limit on a signal mean")
    u.add_argument("--n", type=int, required=True)
    u.add_argument("--b", type=float, required=True, help="known background mean (0 if none)")
    u.add_argument("--cl", type=float, default=0.95)
    i = sub.add_parser("interval", help="Garwood central interval on a Poisson mean")
    i.add_argument("--n", type=int, required=True)
    i.add_argument("--cl", type=float, default=0.6827)
    c = sub.add_parser("coverage", help="seeded toy coverage of the interval")
    c.add_argument("--mu", type=float, required=True)
    c.add_argument("--cl", type=float, default=0.6827)
    c.add_argument("--toys", type=int, default=20000)
    c.add_argument("--seed", type=int, required=True, help="required: every toy study records its seed")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "upper-limit":
            result = upper_limit(args.n, args.b, args.cl)
        elif args.command == "interval":
            result = central_interval(args.n, args.cl)
        else:
            result = coverage(args.mu, args.cl, args.toys, args.seed)
    except DiagnosticsError as exc:
        print(json.dumps({"label": LABEL, "status": "rejected", "error": str(exc)}, indent=2))
        return 2
    result["status"] = "ok"
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
