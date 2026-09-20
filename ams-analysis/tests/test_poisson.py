"""Tests for scripts/poisson_diagnostics.py: known exact values (zero-count bound
-ln(alpha), Garwood intervals for n=0 and n=1), the unphysical classical-limit case,
seeded reproducibility and conservative coverage, and input rejection.
Run from the skill directory with `python3 -m unittest discover -s tests -v`."""
import contextlib
import io
import json
import math
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import poisson_diagnostics as pd  # noqa: E402


class ExactValueTests(unittest.TestCase):
    def test_cdf_matches_closed_forms(self):
        self.assertAlmostEqual(pd.poisson_cdf(0, 2.0), math.exp(-2.0), places=14)
        self.assertAlmostEqual(pd.poisson_cdf(2, 3.0), math.exp(-3.0) * (1 + 3 + 4.5), places=14)
        self.assertEqual(pd.poisson_cdf(5, 0.0), 1.0)

    def test_zero_count_bound_is_minus_ln_alpha(self):
        out = pd.upper_limit(0, 0.0, 0.95)
        self.assertAlmostEqual(out["upper_limit_on_signal"], -math.log(0.05), places=9)
        self.assertAlmostEqual(out["upper_limit_on_signal"], 2.9957, places=3)
        self.assertEqual(out["label"], "[General method]")

    def test_known_upper_limits(self):
        self.assertAlmostEqual(pd.upper_limit(1, 0.0, 0.95)["upper_limit_on_signal"], 4.7439, places=3)
        self.assertAlmostEqual(pd.upper_limit(3, 1.0, 0.95)["upper_limit_on_signal"], 7.7537 - 1.0, places=3)

    def test_garwood_intervals(self):
        zero = pd.central_interval(0, 0.6827)
        self.assertEqual(zero["lower"], 0.0)
        self.assertAlmostEqual(zero["upper"], 1.8410, places=3)
        one = pd.central_interval(1, 0.6827)
        self.assertAlmostEqual(one["lower"], 0.1727, places=3)
        self.assertAlmostEqual(one["upper"], 3.2996, places=3)

    def test_interval_brackets_the_count_for_larger_n(self):
        iv = pd.central_interval(25, 0.95)
        self.assertLess(iv["lower"], 25)
        self.assertGreater(iv["upper"], 25)


class UnphysicalClassicalLimitTests(unittest.TestCase):
    def test_few_events_against_large_background_is_flagged_not_reported(self):
        out = pd.upper_limit(0, 5.0, 0.95)
        self.assertIsNone(out["upper_limit_on_signal"])
        self.assertIn("Feldman-Cousins or CLs", out["warning"])

    def test_no_warning_when_signal_limit_is_positive(self):
        self.assertNotIn("warning", pd.upper_limit(6, 2.0, 0.95))


class CoverageTests(unittest.TestCase):
    def test_same_seed_reproduces_and_different_seed_differs(self):
        a = pd.coverage(2.5, 0.6827, 2000, seed=7)
        b = pd.coverage(2.5, 0.6827, 2000, seed=7)
        c = pd.coverage(2.5, 0.6827, 2000, seed=8)
        self.assertEqual(a["coverage"], b["coverage"])
        self.assertNotEqual(a["coverage"], c["coverage"])
        self.assertEqual((a["seed"], a["toys"], a["cl"]), (7, 2000, 0.6827))

    def test_garwood_is_conservative(self):
        for mu in (0.5, 2.5, 10.0):
            out = pd.coverage(mu, 0.6827, 20000, seed=3)
            self.assertGreaterEqual(out["coverage"] + 4 * out["binomial_error_on_coverage"], 0.6827, mu)

    def test_sampler_mean_and_variance(self):
        import random
        rng = random.Random(11)
        draws = [pd._draw(rng, 4.0) for _ in range(40000)]
        mean = sum(draws) / len(draws)
        var = sum((d - mean) ** 2 for d in draws) / len(draws)
        self.assertAlmostEqual(mean, 4.0, delta=0.06)
        self.assertAlmostEqual(var, 4.0, delta=0.15)


class RejectionTests(unittest.TestCase):
    def test_bad_inputs_rejected(self):
        for call in (lambda: pd.upper_limit(-1, 0.0), lambda: pd.upper_limit(1.5, 0.0), lambda: pd.upper_limit(0, -1.0),
                     lambda: pd.upper_limit(0, 0.0, 1.0), lambda: pd.upper_limit(0, 0.0, 0.0), lambda: pd.central_interval(True),
                     lambda: pd.poisson_cdf(1, 1e6), lambda: pd.coverage(0.0, 0.68, 1000, 1),
                     lambda: pd.coverage(2.0, 0.68, 10, 1), lambda: pd.coverage(2.0, 0.68, 1000, None)):
            with self.assertRaises(pd.DiagnosticsError):
                call()


class CliTests(unittest.TestCase):
    def run_cli(self, *argv):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = pd.main(list(argv))
        return code, json.loads(buf.getvalue())

    def test_upper_limit_cli(self):
        code, out = self.run_cli("upper-limit", "--n", "0", "--b", "0")
        self.assertEqual(code, 0)
        self.assertAlmostEqual(out["upper_limit_on_signal"], 2.9957, places=3)

    def test_rejected_input_exits_2(self):
        code, out = self.run_cli("interval", "--n", "1", "--cl", "1.5")
        self.assertEqual((code, out["status"]), (2, "rejected"))

    def test_coverage_requires_a_seed(self):
        with self.assertRaises(SystemExit) as ctx, contextlib.redirect_stderr(io.StringIO()):
            pd.main(["coverage", "--mu", "2.0"])
        self.assertEqual(ctx.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
