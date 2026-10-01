"""Tests for scripts/likelihood_limits.py: the toy-calibrated limit and p-value against the exact
Poisson results at sigma_b = 0, agreement between the single-bin analytic profile and the numeric
multi-bin profile, monotonic dependence on the background uncertainty, calibration of the
asymptotic limit, reproducibility, input rejection and the CLI contract.
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
import likelihood_limits as ll  # noqa: E402


def doc(kind="none", sigma=None, bins=None):
    d = {"bins": bins or [{"n": 5, "b": 2.0, "s": 1.0}], "cl": 0.95}
    d["background_uncertainty"] = {"kind": kind} if sigma is None else {"kind": kind, "sigma": sigma}
    return d


class SingleBinTests(unittest.TestCase):
    def test_toy_limit_matches_exact_classical_and_asymptotic_undershoots(self):
        out = ll.profile_limit(5, 2.0, 0.0, 0.95, 3000, 1)
        self.assertAlmostEqual(out["toy_calibrated_upper_limit"], out["exact_classical_upper_limit"], delta=0.6)
        self.assertLess(out["asymptotic_upper_limit"], out["exact_classical_upper_limit"])

    def test_limit_grows_with_background_uncertainty(self):
        a = ll.profile_limit(5, 3.0, 0.0, 0.95, 200, 1)["asymptotic_upper_limit"]
        b = ll.profile_limit(5, 3.0, 1.0, 0.95, 200, 1)["asymptotic_upper_limit"]
        c = ll.profile_limit(5, 3.0, 2.0, 0.95, 200, 1)["asymptotic_upper_limit"]
        self.assertLess(a, b)
        self.assertLess(b, c)

    def test_significance_toys_match_exact_tail_and_wilks_doubles(self):
        out = ll.profile_significance(15, 8.0, 0.0, 20000, 1)
        self.assertGreater(out["q0_observed"], 4.0)
        self.assertAlmostEqual(out["p_value_toys"], out["p_value_exact_poisson"], delta=0.005)
        self.assertAlmostEqual(out["p_value_naive_wilks_chi2_1dof"], 2 * out["p_value_half_chi2_asymptotic"], places=12)

    def test_significance_with_nuisance_is_weaker_and_agrees_with_asymptotic(self):
        known = ll.profile_significance(15, 8.0, 0.0, 2000, 1)["q0_observed"]
        out = ll.profile_significance(15, 8.0, 2.0, 20000, 1)
        self.assertLess(out["q0_observed"], known)
        self.assertAlmostEqual(out["p_value_toys"], out["p_value_half_chi2_asymptotic"], delta=0.012)

    def test_underfluctuation_gives_q0_zero(self):
        out = ll.profile_significance(4, 8.0, 1.0, 500, 2)
        self.assertEqual((out["q0_observed"], out["p_value_toys"]), (0.0, 1.0))

    def test_seed_reproducible(self):
        self.assertEqual(ll.profile_limit(4, 2.0, 1.0, 0.95, 300, 5), ll.profile_limit(4, 2.0, 1.0, 0.95, 300, 5))

    def test_rejections(self):
        for call in (lambda: ll.profile_limit(-1, 1.0, 0.0, 0.95, 200, 1), lambda: ll.profile_limit(1, -1.0, 0.0, 0.95, 200, 1),
                     lambda: ll.profile_limit(1, 1.0, -1.0, 0.95, 200, 1), lambda: ll.profile_limit(1, 1.0, 0.0, 1.0, 200, 1),
                     lambda: ll.profile_limit(1, 1.0, 0.0, 0.95, 10, 1), lambda: ll.profile_limit(1, 1.0, 0.0, 0.95, 200, None),
                     lambda: ll.profile_significance(3, 0.0, 0.0, 200, 1)):
            with self.assertRaises(ll.LikelihoodError):
                call()


class MultiBinTests(unittest.TestCase):
    def test_one_bin_matches_the_analytic_profile(self):
        single0 = ll.profile_limit(5, 2.0, 0.0, 0.95, 100, 1)["asymptotic_upper_limit"]
        self.assertAlmostEqual(ll.multibin_limit(doc("none"), 0.95, 0, 1)["asymptotic_observed_upper_limit"], single0, delta=2e-3)
        single1 = ll.profile_limit(5, 3.0, 1.0, 0.95, 100, 1)["asymptotic_upper_limit"]
        bins = [{"n": 5, "b": 3.0, "s": 1.0}]
        ind = ll.multibin_limit(doc("independent", [1.0], bins), 0.95, 0, 1)["asymptotic_observed_upper_limit"]
        com = ll.multibin_limit(doc("common_scale", 1.0 / 3.0, bins), 0.95, 0, 1)["asymptotic_observed_upper_limit"]
        self.assertAlmostEqual(ind, single1, delta=2e-3)
        self.assertAlmostEqual(com, single1, delta=5e-3)

    def test_nuisance_loosens_the_limit_and_expected_is_below_observed_for_an_excess(self):
        bins = [{"n": 8, "b": 6.0, "s": 1.0}, {"n": 12, "b": 10.0, "s": 2.0}, {"n": 20, "b": 18.0, "s": 1.0}]
        none = ll.multibin_limit(doc("none", None, bins), 0.95, 0, 1)
        common = ll.multibin_limit(doc("common_scale", 0.2, bins), 0.95, 0, 1)
        self.assertLess(none["asymptotic_observed_upper_limit"], common["asymptotic_observed_upper_limit"])
        self.assertLess(none["asymptotic_asimov_median_expected_limit"], none["asymptotic_observed_upper_limit"])
        self.assertGreater(none["best_fit_mu"], 0.0)

    def test_toy_p_value_at_the_asymptotic_limit_is_near_the_target(self):
        bins = [{"n": 8, "b": 6.0, "s": 1.0}, {"n": 12, "b": 10.0, "s": 2.0}, {"n": 20, "b": 18.0, "s": 1.0}]
        out = ll.multibin_limit(doc("independent", [1.5, 2.0, 3.0], bins), 0.95, 300, 1)
        self.assertAlmostEqual(out["toy_p_value_at_asymptotic_limit"], 0.05, delta=0.05)

    def test_rejections(self):
        bad = [[1, 2], {"bins": []}, {"bins": [{"n": 1, "b": 1.0, "s": 0.0}]}, {"bins": [{"n": -1, "b": 1.0, "s": 1.0}]},
               {"bins": [{"n": 1, "b": 1.0, "s": 1.0}], "background_uncertainty": {"kind": "weird"}},
               {"bins": [{"n": 1, "b": 1.0, "s": 1.0}], "background_uncertainty": {"kind": "independent", "sigma": [1, 2]}},
               {"bins": [{"n": 1, "b": 1.0, "s": 1.0}], "background_uncertainty": {"kind": "common_scale", "sigma": 0}},
               {"bins": [{"n": 1000, "b": 1.0, "s": 1.0}]}]
        for d in bad:
            with self.assertRaises(ll.LikelihoodError):
                ll.multibin_limit(d, 0.95, 0, 1)


class CliTests(unittest.TestCase):
    def run_cli(self, *argv):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = ll.main(list(argv))
        return code, json.loads(buf.getvalue())

    def test_subcommands_ok_and_seed_echoed(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "m.json"
            path.write_text(json.dumps(doc("none")))
            for argv in (["profile-limit", "--n", "3", "--b", "2", "--toys", "200", "--seed", "4"],
                         ["profile-significance", "--n", "9", "--b", "4", "--toys", "200", "--seed", "4"],
                         ["multibin-limit", "--input", str(path), "--toys", "100", "--seed", "4"]):
                code, out = self.run_cli(*argv)
                self.assertEqual((code, out["status"], out["seed"], out["label"]), (0, "ok", 4, "[General method]"), argv[0])

    def test_bad_input_exits_2_and_seed_required(self):
        code, out = self.run_cli("profile-limit", "--n", "-1", "--b", "2", "--seed", "1")
        self.assertEqual((code, out["status"]), (2, "rejected"))
        code, out = self.run_cli("multibin-limit", "--input", "/nonexistent.json", "--seed", "1")
        self.assertEqual(code, 2)
        with self.assertRaises(SystemExit), contextlib.redirect_stderr(io.StringIO()):
            ll.main(["profile-limit", "--n", "1", "--b", "1"])


if __name__ == "__main__":
    unittest.main()
