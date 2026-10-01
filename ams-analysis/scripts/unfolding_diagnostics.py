#!/usr/bin/env python3
"""Seeded unfolding diagnostics for small response matrices (approximations).

Purpose: give the "regularization is a bias-variance choice, validate it" rules an executable
form: regularized (Tikhonov, truncated-SVD) scans, closure and pull tests, a forward-folding
versus unfold-then-fit comparison, and the effect of finite Monte Carlo statistics in the
response matrix. This is not an unfolding package: matrices are small (at most 60 bins), the
data are independent Poisson counts, the response is a probability matrix with inefficiency
outside it (the convention of scripts/validate_response.py), and no systematic is modeled.
Output is labeled [General method]; nothing here is AMS performance. Seed, toy count and
configuration are echoed.

Methods (--method, --param): `dagostini` (iterations; nonlinear, so spread comes from toys),
`tikhonov` (second-difference penalty; strength relative to the mean diagonal of R^T W^2 R)
and `tsvd` (number of retained singular values of the Poisson-weighted response). The linear
methods have analytic bias and covariance (bias = A mu - truth, cov = A diag(mu) A^T).

Subcommands:
  regularized-scan  bias, spread and adjacent-bin correlation per regularization setting.
  closure           noise-free closure (model dependence) and seeded pulls for one setting.
  fold-compare      power-law spectrum fit by forward folding versus unfold-then-fit.
  response-stat     spread from data statistics, from finite response (MC) statistics, both.

Input JSON (shared): {"response": [[...]], "orientation": "rows_reco_cols_truth" (default) |
"rows_truth_cols_reco", "truth": [expected truth counts], "prior": [...] (optional start shape for
dagostini)}; closure also "test_truth": [...]; fold-compare also "truth_edges": [n_truth + 1
increasing positive edges] and "model": {"gamma": 2.7}  (the truth is then the power law with
the total of "truth"); response-stat also "mc_events_per_truth_bin": [...].

Usage (from the skill directory):
  python3 scripts/unfolding_diagnostics.py regularized-scan --input u.json --method tikhonov --seed 1
  python3 scripts/unfolding_diagnostics.py closure --input u.json --method tsvd --param 3 --toys 500 --seed 1
  python3 scripts/unfolding_diagnostics.py fold-compare --input u.json --method tikhonov --param 0.01 --toys 300 --seed 1
  python3 scripts/unfolding_diagnostics.py response-stat --input u.json --method dagostini --param 4 --toys 300 --seed 1
Exit codes: 0 ok; 2 rejected input. Standard library only.
Importable: regularized_scan, closure, fold_compare, response_stat, linear_matrix.
"""
from __future__ import annotations

import argparse
import json
import math
import random
import sys
from pathlib import Path

from statistical_toys import (ToyError, _load_response, _num, _scan_then_golden, _seed, _std, _toys, _unfold,
                              poisson_draw)

LABEL = "[General method]"
METHODS = ("dagostini", "tikhonov", "tsvd")


# ------------------------------------------------------------------ small linear algebra
def _matmul(a, b):
    bt = list(zip(*b))
    return [[sum(x * y for x, y in zip(row, col)) for col in bt] for row in a]


def _transpose(a):
    return [list(r) for r in zip(*a)]


def _solve(a, b):
    """Solve a X = b (square a, matrix b) by Gaussian elimination with partial pivoting."""
    n = len(a)
    m = [list(a[i]) + list(b[i]) for i in range(n)]
    for c in range(n):
        piv = max(range(c, n), key=lambda r: abs(m[r][c]))
        if abs(m[piv][c]) < 1e-300:
            raise ToyError("singular matrix in the regularized solve; use a larger strength or fewer singular values")
        m[c], m[piv] = m[piv], m[c]
        pv = m[c][c]
        m[c] = [v / pv for v in m[c]]
        for r in range(n):
            if r != c and m[r][c] != 0.0:
                f = m[r][c]
                m[r] = [x - f * y for x, y in zip(m[r], m[c])]
    return [row[n:] for row in m]


def _jacobi(a, sweeps: int = 80):
    """Eigen-decomposition of a symmetric matrix by cyclic Jacobi rotations: (eigenvalues, eigenvector columns)."""
    n = len(a)
    a = [list(r) for r in a]
    v = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for _ in range(sweeps):
        off = sum(a[i][j] ** 2 for i in range(n) for j in range(i + 1, n))
        if off < 1e-24 * max(sum(a[i][i] ** 2 for i in range(n)), 1e-300):
            break
        for p in range(n - 1):
            for q in range(p + 1, n):
                if abs(a[p][q]) < 1e-300:
                    continue
                theta = (a[q][q] - a[p][p]) / (2.0 * a[p][q])
                t = (1.0 if theta >= 0 else -1.0) / (abs(theta) + math.sqrt(theta * theta + 1.0))
                c = 1.0 / math.sqrt(t * t + 1.0)
                s = t * c
                for k in range(n):
                    akp, akq = a[k][p], a[k][q]
                    a[k][p], a[k][q] = c * akp - s * akq, s * akp + c * akq
                for k in range(n):
                    apk, aqk = a[p][k], a[q][k]
                    a[p][k], a[q][k] = c * apk - s * aqk, s * apk + c * aqk
                for k in range(n):
                    vkp, vkq = v[k][p], v[k][q]
                    v[k][p], v[k][q] = c * vkp - s * vkq, s * vkp + c * vkq
    return [a[i][i] for i in range(n)], v


# -------------------------------------------------------------------------------- methods
def _check_method(method, param, n_truth):
    if method not in METHODS:
        raise ToyError(f"method must be one of {METHODS}")
    p = _num(param, "param", 0.0)
    if method == "dagostini":
        if p != int(p) or not 1 <= p <= 200:
            raise ToyError("dagostini param is an iteration count in [1, 200]")
    elif method == "tsvd":
        if p != int(p) or not 1 <= p <= n_truth:
            raise ToyError(f"tsvd param is a number of singular values in [1, {n_truth}]")
    elif p <= 0:
        raise ToyError("tikhonov param (relative strength) must be > 0")
    return int(p) if method != "tikhonov" else p


def linear_matrix(method: str, param, r, mu_w) -> list[list[float]]:
    """Unfolding matrix A (n_truth x n_reco) of a linear method; weights W^2 = 1 / max(mu_w, 1)."""
    n_reco, n_truth = len(r), len(r[0])
    w = [1.0 / math.sqrt(max(m, 1.0)) for m in mu_w]
    b = [[w[i] * r[i][j] for j in range(n_truth)] for i in range(n_reco)]  # W R
    bt = _transpose(b)
    btb = _matmul(bt, b)
    wt = [[w[i] if k == i else 0.0 for k in range(n_reco)] for i in range(n_reco)]
    if method == "tikhonov":
        scale = param * sum(btb[j][j] for j in range(n_truth)) / n_truth
        if n_truth >= 3:
            rows = [[(1.0 if j == i else -2.0 if j == i + 1 else 1.0 if j == i + 2 else 0.0) for j in range(n_truth)]
                    for i in range(n_truth - 2)]
            ltl = _matmul(_transpose(rows), rows)
        else:
            ltl = [[1.0 if i == j else 0.0 for j in range(n_truth)] for i in range(n_truth)]
        m = [[btb[i][j] + scale * ltl[i][j] for j in range(n_truth)] for i in range(n_truth)]
        return _matmul(_solve(m, bt), wt)
    vals, vecs = _jacobi(btb)
    order = sorted(range(n_truth), key=lambda i: -vals[i])
    a = [[0.0] * n_reco for _ in range(n_truth)]
    kept = 0
    for idx in order[:param]:
        if vals[idx] <= 1e-12 * vals[order[0]]:
            continue
        sigma = math.sqrt(vals[idx])
        vk = [vecs[j][idx] for j in range(n_truth)]
        uk = [sum(b[i][j] * vk[j] for j in range(n_truth)) / sigma for i in range(n_reco)]
        for j in range(n_truth):
            for i in range(n_reco):
                a[j][i] += vk[j] * uk[i] / sigma
        kept += 1
    if kept == 0:
        raise ToyError("no usable singular values")
    return _matmul(a, wt)


def _estimator(method, param, r, mu_w, prior):
    """counts -> unfolded truth estimate."""
    n_reco, n_truth = len(r), len(r[0])
    if method == "dagostini":
        eff = [sum(r[i][j] for i in range(n_reco)) for j in range(n_truth)]
        base = prior if prior is not None else [1.0] * n_truth
        norm = sum(sum(r[i][j] * base[j] for j in range(n_truth)) for i in range(n_reco))

        def run(counts):
            scale = sum(counts) / norm if norm > 0 else 1.0
            return _unfold(counts, r, eff, [v * scale for v in base], param)[-1]
        return run, None
    a = linear_matrix(method, param, r, mu_w)
    return (lambda counts: [sum(a[j][i] * counts[i] for i in range(n_reco)) for j in range(n_truth)]), a


def _mu(r, t):
    return [sum(row[j] * t[j] for j in range(len(t))) for row in r]


def _cov(a, mu):
    n_t, n_r = len(a), len(a[0])
    return [[sum(a[j][i] * a[k][i] * mu[i] for i in range(n_r)) for k in range(n_t)] for j in range(n_t)]


def _rms(v):
    return math.sqrt(sum(x * x for x in v) / len(v)) if v else 0.0


def _unpack(doc, method, param):
    r, truth, prior, _ = _load_response(dict(doc, max_iterations=doc.get("max_iterations", 1)))
    return r, truth, prior, _check_method(method, param, len(r[0]))


# ------------------------------------------------------------------ regularized-scan
def regularized_scan(doc: dict, method: str, values, toys: int, seed: int) -> dict:
    if method not in ("tikhonov", "tsvd"):
        raise ToyError("regularized-scan supports tikhonov and tsvd (use unfold-scan in statistical_toys.py for dagostini)")
    r, truth, prior, _ = _unpack(doc, method, 1.0 if method == "tikhonov" else 1)
    n_truth = len(truth)
    if values is None:
        values = [1e-4, 1e-3, 1e-2, 1e-1, 1.0, 10.0] if method == "tikhonov" else list(range(1, n_truth + 1))
    if not isinstance(values, list) or not 1 <= len(values) <= 60:
        raise ToyError("values must be a list of 1 to 60 settings")
    toys, seed = _toys(toys, 20), _seed(seed)
    mu = _mu(r, truth)
    used = [j for j in range(n_truth) if truth[j] > 0]
    rows = []
    for v in values:
        p = _check_method(method, v, n_truth)
        a = linear_matrix(method, p, r, mu)
        est = [sum(a[j][i] * mu[i] for i in range(len(mu))) for j in range(n_truth)]
        cov = _cov(a, mu)
        bias = [(est[j] - truth[j]) / truth[j] for j in used]
        spread = [math.sqrt(max(cov[j][j], 0.0)) / truth[j] for j in used]
        adj = [cov[j][j + 1] / math.sqrt(cov[j][j] * cov[j + 1][j + 1]) for j in range(n_truth - 1)
               if cov[j][j] > 0 and cov[j + 1][j + 1] > 0]
        rng = random.Random(seed)
        neg = 0
        for _ in range(toys):
            n = [poisson_draw(rng, m) for m in mu]
            neg += any(sum(a[j][i] * n[i] for i in range(len(n))) < 0 for j in range(n_truth))
        rows.append({"setting": p, "rms_relative_bias": _rms(bias), "rms_relative_spread": _rms(spread),
                     "rms_relative_total": math.sqrt(_rms(bias) ** 2 + _rms(spread) ** 2),
                     "min_adjacent_correlation": min(adj) if adj else None,
                     "fraction_toys_with_a_negative_bin": neg / toys})
    best = min(rows, key=lambda x: x["rms_relative_total"])
    return {"label": LABEL, "method": f"{method} regularized unfolding scan (analytic bias and covariance)",
            "bins_truth": n_truth, "bins_reco": len(r), "toys": toys, "seed": seed, "scan": rows,
            "minimum_total_at_setting": best["setting"],
            "note": ("bias is against the truth you supplied, which also sets the weights, so the scan is circular: "
                     "repeat with a different truth (closure) before choosing a strength; a strong negative adjacent "
                     "correlation is the signature of too weak a regularization; linear solutions can be negative "
                     "in a bin; the covariance is the Poisson propagation only (no response statistics, no "
                     "systematics), and the regularization strength is relative to the mean diagonal of R^T W^2 R")}


# -------------------------------------------------------------------------------- closure
def closure(doc: dict, method: str, param, toys: int, seed: int) -> dict:
    r, truth, prior, p = _unpack(doc, method, param)
    test = doc.get("test_truth", truth)
    if not isinstance(test, list) or len(test) != len(truth):
        raise ToyError(f"test_truth must list {len(truth)} expected counts")
    test = [_num(v, "test_truth", 0.0, 1e5) for v in test]
    toys, seed = _toys(toys, 50), _seed(seed)
    n_truth = len(truth)
    mu_model, mu_test = _mu(r, truth), _mu(r, test)
    est, a = _estimator(method, p, r, mu_model, prior)
    closure_x = est([float(m) for m in mu_test])
    rng = random.Random(seed)
    draws = [est([poisson_draw(rng, m) for m in mu_test]) for _ in range(toys)]
    used = [j for j in range(n_truth) if test[j] > 0]
    if a is not None:
        cov = _cov(a, mu_test)
        sigma = [math.sqrt(max(cov[j][j], 0.0)) for j in range(n_truth)]
        sigma_kind = "analytic Poisson propagation"
    else:
        sigma = [_std([d[j] for d in draws]) for j in range(n_truth)]
        sigma_kind = "spread of the toys (so the pull width is 1 by construction; read the mean pull)"
    bias = [closure_x[j] - test[j] for j in range(n_truth)]
    means = [sum(d[j] for d in draws) / toys for j in range(n_truth)]
    pull_mean = [(means[j] - test[j]) / sigma[j] if sigma[j] > 0 else 0.0 for j in used]
    pull_width = [_std([(d[j] - test[j]) / sigma[j] for d in draws]) for j in used if sigma[j] > 0]
    chi2 = sum((bias[j] / sigma[j]) ** 2 for j in used if sigma[j] > 0)
    return {"label": LABEL, "method": f"{method} closure and pull test (param {p})", "bins_truth": n_truth, "toys": toys,
            "seed": seed, "test_truth_differs_from_model": test != truth, "sigma_source": sigma_kind,
            "closure_relative_bias_per_bin": [bias[j] / test[j] for j in used],
            "closure_rms_relative_bias": _rms([bias[j] / test[j] for j in used]),
            "closure_bias_significance_chi2_over_bins": chi2 / len(used),
            "statistical_sigma_per_bin": [sigma[j] for j in used],
            "mean_pull_per_bin": pull_mean, "max_abs_mean_pull": max(abs(x) for x in pull_mean),
            "mean_pull_standard_error": 1.0 / math.sqrt(toys),
            "mean_pull_width": sum(pull_width) / len(pull_width) if pull_width else None,
            "note": ("the noise-free closure unfolds the expected measurement of test_truth with the response, prior and "
                     "weights of the model truth: a nonzero bias is model dependence, to be compared with the "
                     "statistical sigma (chi2 over bins near 0 means it is negligible, well above 1 means it is a "
                     "systematic to assign); the mean pull is the toy mean minus truth in units of the statistical "
                     "sigma, with standard error 1/sqrt(toys), so a mean pull beyond about 3 standard errors flags a bias, "
                     "and a bias of a few tenths of a sigma is a systematic to assign; a pull width above 1 means the quoted errors are too "
                     "small; the response is assumed exactly known and the efficiency exactly applied")}


# --------------------------------------------------------------------------- fold-compare
def _pl_weights(edges, gamma):
    def integral(lo, hi):
        return math.log(hi / lo) if abs(gamma - 1.0) < 1e-9 else (hi ** (1 - gamma) - lo ** (1 - gamma)) / (1 - gamma)
    w = [integral(edges[j], edges[j + 1]) for j in range(len(edges) - 1)]
    tot = sum(w)
    return [x / tot for x in w]


def fold_compare(doc: dict, method: str, param, toys: int, seed: int) -> dict:
    if method == "dagostini":
        raise ToyError("fold-compare supports tikhonov and tsvd (the covariance of the unfolded result must be known)")
    r, truth, prior, p = _unpack(doc, method, param)
    edges = doc.get("truth_edges")
    model = doc.get("model")
    if not isinstance(edges, list) or len(edges) != len(truth) + 1:
        raise ToyError(f"truth_edges must list {len(truth) + 1} edges")
    edges = [_num(e, "edge", 0.0, 1e9, strict_low=True) for e in edges]
    if any(edges[k + 1] <= edges[k] for k in range(len(edges) - 1)):
        raise ToyError("truth_edges must be increasing")
    if not isinstance(model, dict):
        raise ToyError('model must be {"gamma": value}')
    g_true = _num(model.get("gamma"), "model.gamma", -5.0, 12.0)
    toys, seed = _toys(toys, 20), _seed(seed)
    total = sum(truth)
    n_t = len(truth)
    t_true = [total * w for w in _pl_weights(edges, g_true)]
    mu = _mu(r, t_true)
    a = linear_matrix(method, p, r, mu)
    rng = random.Random(seed)
    fold_fit, unf_fit = [], []
    g_lo, g_hi = g_true - 3.0, g_true + 3.0
    for _ in range(toys):
        n = [poisson_draw(rng, m) for m in mu]
        if sum(n) == 0:
            continue
        cache = {}

        def u_of(g):
            if g not in cache:
                w = _pl_weights(edges, g)
                cache[g] = [sum(r[i][j] * w[j] for j in range(n_t)) for i in range(len(r))]
            return cache[g]

        def nll(g):
            u = u_of(g)
            if any(x <= 0 for x, c in zip(u, n) if c > 0):
                return 1e300
            return -(sum(c * math.log(x) for x, c in zip(u, n) if c > 0) - sum(n) * math.log(sum(u)))
        fold_fit.append(_scan_then_golden(nll, g_lo, g_hi))
        x = [sum(a[j][i] * n[i] for i in range(len(n))) for j in range(n_t)]
        cov = _cov(a, [max(c, 1) for c in n])
        ridge = 1e-9 * sum(cov[j][j] for j in range(n_t)) / n_t
        cinv = _solve([[cov[j][k] + (ridge if j == k else 0.0) for k in range(n_t)] for j in range(n_t)],
                      [[1.0 if j == k else 0.0 for k in range(n_t)] for j in range(n_t)])

        def chi2(g):
            w = _pl_weights(edges, g)
            cw = [sum(cinv[j][k] * w[k] for k in range(n_t)) for j in range(n_t)]
            num, den = sum(x[j] * cw[j] for j in range(n_t)), sum(w[j] * cw[j] for j in range(n_t))
            norm = num / den if den > 0 else 0.0
            res = [x[j] - norm * w[j] for j in range(n_t)]
            return sum(res[j] * sum(cinv[j][k] * res[k] for k in range(n_t)) for j in range(n_t))
        unf_fit.append(_scan_then_golden(chi2, g_lo, g_hi))
    if len(fold_fit) < 10:
        raise ToyError("too few usable toys; increase the counts")
    mean = lambda v: sum(v) / len(v)
    sf, su = _std(fold_fit), _std(unf_fit)
    return {"label": LABEL, "method": f"power-law index: forward folding versus {method} unfolding then chi2 fit (param {p})",
            "true_gamma": g_true, "toys_used": len(fold_fit), "seed": seed,
            "forward_fold_bias": mean(fold_fit) - g_true, "forward_fold_spread": sf,
            "unfold_then_fit_bias": mean(unf_fit) - g_true, "unfold_then_fit_spread": su,
            "spread_ratio_unfold_over_fold": su / sf if sf > 0 else None,
            "note": ("the forward fit maximizes the Poisson likelihood of the measured counts (normalization profiled) and "
                     "is the reference here; the unfold-then-fit result uses the unfolded vector and its Poisson "
                     "covariance (estimated from the observed counts) in a generalized chi2 fit; a bias or a spread "
                     "ratio above 1 for the unfolded route is the cost of regularization and of the covariance "
                     "estimate; the model is a pure power law whose true form is assumed known, so this isolates the "
                     "statistical and regularization cost and says nothing about model misspecification")}


# --------------------------------------------------------------------------- response-stat
def response_stat(doc: dict, method: str, param, toys: int, seed: int) -> dict:
    r, truth, prior, p = _unpack(doc, method, param)
    n_truth, n_reco = len(truth), len(r)
    if method == "tsvd" and n_truth > 20:
        raise ToyError("response-stat with tsvd is limited to 20 truth bins (a decomposition per toy)")
    gen = doc.get("mc_events_per_truth_bin")
    if not isinstance(gen, list) or len(gen) != n_truth:
        raise ToyError(f"mc_events_per_truth_bin must list {n_truth} generated-event counts")
    gen = [_num(g, "mc_events", 1.0, 1e5) for g in gen]
    toys, seed = _toys(toys, 20), _seed(seed)
    mu = _mu(r, truth)
    est0, _ = _estimator(method, p, r, mu, prior)
    rng = random.Random(seed)
    data_only, resp_only, both = [], [], []
    for _ in range(toys):
        r2 = [[0.0] * n_truth for _ in range(n_reco)]
        for j in range(n_truth):
            for i in range(n_reco):
                r2[i][j] = poisson_draw(rng, gen[j] * r[i][j]) / gen[j]
        if any(sum(r2[i][j] for i in range(n_reco)) <= 0 for j in range(n_truth) if truth[j] > 0):
            continue
        est2, _ = _estimator(method, p, r2, mu, prior)
        n = [poisson_draw(rng, m) for m in mu]
        data_only.append(est0(n))
        resp_only.append(est2([float(m) for m in mu]))
        both.append(est2(n))
    if len(both) < 10:
        raise ToyError("too few usable toys; increase mc_events_per_truth_bin")
    used = [j for j in range(n_truth) if truth[j] > 0]

    def rel(vs):
        return _rms([_std([v[j] for v in vs]) / truth[j] for j in used])
    d, rs, b = rel(data_only), rel(resp_only), rel(both)
    return {"label": LABEL, "method": f"finite response statistics in {method} unfolding (param {p}), seeded toys",
            "toys_used": len(both), "seed": seed, "rms_relative_spread_data_only": d,
            "rms_relative_spread_response_only": rs, "rms_relative_spread_both": b,
            "quadrature_of_data_and_response": math.sqrt(d * d + rs * rs),
            "response_share_of_total_variance": rs * rs / (b * b) if b > 0 else None,
            "note": ("the response matrix is redrawn with Poisson counts per cell from the stated generated-event counts "
                     "(an approximation to multinomial migration with a lost-event class), the unfolding then uses the "
                     "redrawn matrix as if it were exact; data-only and response-only spreads add in quadrature only "
                     "approximately because the two sources interact in the unfolding; a response share above a few "
                     "percent of the variance is the trigger to put response statistics in the uncertainty "
                     "(for example by repeating the unfolding with a bootstrap of the MC) or to enlarge the MC")}


# ------------------------------------------------------------------------------ CLI
def _read(path):
    try:
        return json.loads(Path(path).read_text())
    except (OSError, json.JSONDecodeError) as exc:
        raise ToyError(f"cannot read {path}: {exc}") from None


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0], formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    def common(p, toys, method_default=None, param=True):
        p.add_argument("--input", required=True, help="JSON file (see the module docstring)")
        p.add_argument("--method", choices=METHODS, default=method_default, required=method_default is None)
        if param:
            p.add_argument("--param", type=float, required=True, help="iterations, strength or singular values")
        p.add_argument("--toys", type=int, default=toys)
        p.add_argument("--seed", type=int, required=True, help="required: every toy study records its seed")

    s = sub.add_parser("regularized-scan", help="bias/spread scan over regularization settings")
    common(s, 200, param=False)
    s.add_argument("--values", help="comma-separated settings (default: a built-in list)")
    common_c = sub.add_parser("closure", help="closure and pull test")
    common(common_c, 500)
    f = sub.add_parser("fold-compare", help="forward folding versus unfold-then-fit")
    common(f, 300)
    r = sub.add_parser("response-stat", help="effect of finite response statistics")
    common(r, 300)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        doc = _read(args.input)
        if args.command == "regularized-scan":
            try:
                values = [float(v) for v in args.values.split(",")] if args.values else None
            except ValueError:
                raise ToyError("--values must be comma-separated numbers") from None
            result = regularized_scan(doc, args.method, values, args.toys, args.seed)
        elif args.command == "closure":
            result = closure(doc, args.method, args.param, args.toys, args.seed)
        elif args.command == "fold-compare":
            result = fold_compare(doc, args.method, args.param, args.toys, args.seed)
        else:
            result = response_stat(doc, args.method, args.param, args.toys, args.seed)
    except ToyError as exc:
        print(json.dumps({"label": LABEL, "status": "rejected", "error": str(exc)}, indent=2))
        return 2
    result["status"] = "ok"
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
