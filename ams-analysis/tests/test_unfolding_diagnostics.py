"""Tests for scripts/unfolding_diagnostics.py: linear-algebra helpers, the identities of the linear
unfolding matrices (A R = I at full rank, a projector under truncation), the bias-variance trend of the
regularized scan, closure and pull behavior, forward-fold versus unfold-then-fit, finite response
statistics, reproducibility, rejection and the CLI contract.
Run from the skill directory with `python3 -m unittest discover -s tests -v`."""
import contextlib
import io
import json
import math
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import unfolding_diagnostics as ud  # noqa: E402

N, SIGMA, EDGES = 4, 0.5, [1.0, 2.0, 4.0, 8.0, 16.0]


def make_doc(total=20000.0, gamma=2.7, gen=5000, test_tilt=0.0):
    r = [[0.0] * N for _ in range(N)]
    for j in range(N):
        z = sum(math.exp(-0.5 * ((k - j) / SIGMA) ** 2) for k in range(N))
        for i in range(N):
            r[i][j] = 0.8 * math.exp(-0.5 * ((i - j) / SIGMA) ** 2) / z
    w = [(EDGES[k] ** (1 - gamma) - EDGES[k + 1] ** (1 - gamma)) / (gamma - 1) for k in range(N)]
    truth = [total * x / sum(w) for x in w]
    return {"response": r, "truth": truth, "truth_edges": EDGES, "model": {"gamma": gamma},
            "mc_events_per_truth_bin": [gen] * N,
            "test_truth": [x * (1 + test_tilt * (k - 1.5) / 1.5) for k, x in enumerate(truth)]}


def identity_error(a, r):
    ar = ud._matmul(a, r)
    return max(abs(ar[i][j] - (1.0 if i == j else 0.0)) for i in range(N) for j in range(N))


class LinearAlgebraTests(unittest.TestCase):
    def test_solve_and_jacobi(self):
        a = [[4.0, 1.0, 0.0], [1.0, 3.0, 1.0], [0.0, 1.0, 2.0]]
        x = ud._solve(a, [[1.0], [2.0], [3.0]])
        back = ud._matmul(a, x)
        for got, want in zip(back, (1.0, 2.0, 3.0)):
            self.assertAlmostEqual(got[0], want, places=10)
        vals, vecs = ud._jacobi(a)
        for k in range(3):
            v = [vecs[i][k] for i in range(3)]
            av = [sum(a[i][j] * v[j] for j in range(3)) for i in range(3)]
            for i in range(3):
                self.assertAlmostEqual(av[i], vals[k] * v[i], places=8)

    def test_singular_solve_rejected(self):
        with self.assertRaises(ud.ToyError):
            ud._solve([[1.0, 2.0], [2.0, 4.0]], [[1.0], [1.0]])


class LinearMatrixTests(unittest.TestCase):
    def setUp(self):
        d = make_doc()
        self.r, self.mu = d["response"], ud._mu(d["response"], d["truth"])

    def test_full_rank_inverts_the_response(self):
        self.assertLess(identity_error(ud.linear_matrix("tsvd", N, self.r, self.mu), self.r), 1e-8)
        self.assertLess(identity_error(ud.linear_matrix("tikhonov", 1e-10, self.r, self.mu), self.r), 1e-4)

    def test_truncation_gives_a_projector(self):
        a = ud.linear_matrix("tsvd", 2, self.r, self.mu)
        p = ud._matmul(a, self.r)
        pp = ud._matmul(p, p)
        for i in range(N):
            for j in range(N):
                self.assertAlmostEqual(pp[i][j], p[i][j], places=8)
        self.assertGreater(identity_error(a, self.r), 0.05)


class ScanTests(unittest.TestCase):
    def test_tikhonov_trades_variance_for_bias(self):
        rows = ud.regularized_scan(make_doc(), "tikhonov", [1e-6, 1e-3, 1e-1], 50, 1)["scan"]
        self.assertLess(rows[0]["rms_relative_bias"], rows[2]["rms_relative_bias"])
        self.assertGreater(rows[0]["rms_relative_spread"], rows[2]["rms_relative_spread"])

    def test_tsvd_full_rank_is_unbiased_and_truncation_biases(self):
        rows = ud.regularized_scan(make_doc(), "tsvd", None, 50, 1)["scan"]
        self.assertLess(rows[-1]["rms_relative_bias"], 1e-6)
        self.assertGreater(rows[0]["rms_relative_bias"], 0.05)
        self.assertEqual(len(rows), N)

    def test_seed_reproducible_and_rejections(self):
        a = ud.regularized_scan(make_doc(), "tikhonov", [0.01], 30, 3)
        self.assertEqual(a, ud.regularized_scan(make_doc(), "tikhonov", [0.01], 30, 3))
        for call in (lambda: ud.regularized_scan(make_doc(), "dagostini", [1], 30, 1),
                     lambda: ud.regularized_scan(make_doc(), "tsvd", [0], 30, 1),
                     lambda: ud.regularized_scan(make_doc(), "tikhonov", [-1.0], 30, 1),
                     lambda: ud.regularized_scan(make_doc(), "tikhonov", [0.1], 30, None),
                     lambda: ud.regularized_scan({"response": [[1.0]]}, "tikhonov", [0.1], 30, 1)):
            with self.assertRaises(ud.ToyError):
                call()


class ClosureTests(unittest.TestCase):
    def test_full_rank_noise_free_closure_is_exact_and_pulls_are_unbiased(self):
        out = ud.closure(make_doc(), "tsvd", N, 600, 1)
        self.assertLess(out["closure_rms_relative_bias"], 1e-8)
        self.assertLess(out["max_abs_mean_pull"], 4.0 * out["mean_pull_standard_error"])
        self.assertAlmostEqual(out["mean_pull_width"], 1.0, delta=0.12)

    def test_model_dependence_shows_up_with_a_different_test_truth(self):
        same = ud.closure(make_doc(), "tikhonov", 0.05, 100, 1)
        diff = ud.closure(make_doc(test_tilt=0.5), "tikhonov", 0.05, 100, 1)
        self.assertFalse(same["test_truth_differs_from_model"])
        self.assertTrue(diff["test_truth_differs_from_model"])
        self.assertNotEqual(same["closure_relative_bias_per_bin"], diff["closure_relative_bias_per_bin"])

    def test_dagostini_closure_bias_falls_with_iterations(self):
        few = ud.closure(make_doc(test_tilt=0.5), "dagostini", 2, 50, 1)["closure_rms_relative_bias"]
        many = ud.closure(make_doc(test_tilt=0.5), "dagostini", 60, 50, 1)["closure_rms_relative_bias"]
        self.assertGreater(few, 3 * many)

    def test_dagostini_sigma_comes_from_toys(self):
        out = ud.closure(make_doc(), "dagostini", 3, 100, 1)
        self.assertIn("toys", out["sigma_source"])

    def test_rejections(self):
        for call in (lambda: ud.closure(dict(make_doc(), test_truth=[1.0]), "tsvd", 2, 100, 1),
                     lambda: ud.closure(make_doc(), "tsvd", 9, 100, 1), lambda: ud.closure(make_doc(), "dagostini", 0, 100, 1),
                     lambda: ud.closure(make_doc(), "bogus", 1, 100, 1)):
            with self.assertRaises(ud.ToyError):
                call()


class FoldCompareTests(unittest.TestCase):
    def test_both_routes_recover_the_index_and_forward_fold_is_unbiased(self):
        out = ud.fold_compare(make_doc(), "tikhonov", 1e-3, 80, 1)
        self.assertLess(abs(out["forward_fold_bias"]), 3 * out["forward_fold_spread"] / math.sqrt(out["toys_used"]) + 1e-3)
        self.assertLess(abs(out["unfold_then_fit_bias"]), 0.2)
        self.assertGreater(out["spread_ratio_unfold_over_fold"], 0.5)

    def test_rejections(self):
        for call in (lambda: ud.fold_compare(make_doc(), "dagostini", 3, 50, 1),
                     lambda: ud.fold_compare(dict(make_doc(), truth_edges=[1, 2]), "tsvd", 3, 50, 1),
                     lambda: ud.fold_compare(dict(make_doc(), truth_edges=[1, 3, 2, 4, 5]), "tsvd", 3, 50, 1),
                     lambda: ud.fold_compare(dict(make_doc(), model=None), "tsvd", 3, 50, 1)):
            with self.assertRaises(ud.ToyError):
                call()


class ResponseStatTests(unittest.TestCase):
    def test_response_share_falls_with_more_mc(self):
        small = ud.response_stat(make_doc(gen=300), "tikhonov", 1e-3, 100, 1)
        large = ud.response_stat(make_doc(gen=20000), "tikhonov", 1e-3, 100, 1)
        self.assertGreater(small["response_share_of_total_variance"], 3 * large["response_share_of_total_variance"])
        self.assertLess(large["response_share_of_total_variance"], 0.08)

    def test_dagostini_supported_and_rejections(self):
        out = ud.response_stat(make_doc(gen=1000), "dagostini", 3, 60, 1)
        self.assertGreater(out["rms_relative_spread_both"], 0.0)
        for call in (lambda: ud.response_stat(dict(make_doc(), mc_events_per_truth_bin=[1, 2]), "tikhonov", 0.1, 60, 1),
                     lambda: ud.response_stat(dict(make_doc(), mc_events_per_truth_bin=[0] * N), "tikhonov", 0.1, 60, 1)):
            with self.assertRaises(ud.ToyError):
                call()


class CliTests(unittest.TestCase):
    def run_cli(self, *argv):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = ud.main(list(argv))
        return code, json.loads(buf.getvalue())

    def test_each_subcommand_ok_and_bad_input_exits_2(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "u.json"
            path.write_text(json.dumps(make_doc()))
            for argv in (["regularized-scan", "--input", str(path), "--method", "tikhonov", "--values", "0.01,0.1", "--toys", "30", "--seed", "4"],
                         ["closure", "--input", str(path), "--method", "tsvd", "--param", "3", "--toys", "60", "--seed", "4"],
                         ["fold-compare", "--input", str(path), "--method", "tikhonov", "--param", "0.01", "--toys", "30", "--seed", "4"],
                         ["response-stat", "--input", str(path), "--method", "dagostini", "--param", "3", "--toys", "30", "--seed", "4"]):
                code, out = self.run_cli(*argv)
                self.assertEqual((code, out["status"], out["seed"], out["label"]), (0, "ok", 4, "[General method]"), argv[0])
            code, out = self.run_cli("closure", "--input", str(path), "--method", "tsvd", "--param", "9", "--seed", "1")
            self.assertEqual((code, out["status"]), (2, "rejected"))
        code, out = self.run_cli("closure", "--input", "/nonexistent.json", "--method", "tsvd", "--param", "2", "--seed", "1")
        self.assertEqual(code, 2)
        with self.assertRaises(SystemExit), contextlib.redirect_stderr(io.StringIO()):
            ud.main(["closure", "--input", "x.json", "--method", "tsvd", "--param", "2"])


if __name__ == "__main__":
    unittest.main()
