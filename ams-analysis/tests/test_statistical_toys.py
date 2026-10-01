"""Tests for scripts/statistical_toys.py: seeded reproducibility, known limits of each
diagnostic (exact Poisson tail at the boundary, finite-template spread -> 1 for a huge MC
sample, identity-response unfolding, ratio cancellation at rho = 1), input rejection and the
CLI contract. Run from the skill directory with `python3 -m unittest discover -s tests -v`."""
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
import statistical_toys as st  # noqa: E402

SIG, BKG = "0.1,0.3,0.4,0.2", "0.4,0.3,0.2,0.1"
RESPONSE = {"response": [[0.6, 0.2, 0.0], [0.2, 0.5, 0.2], [0.0, 0.2, 0.6]], "truth": [1000, 600, 200], "max_iterations": 6}


class DrawTests(unittest.TestCase):
    def test_poisson_draw_moments_for_large_mean(self):
        import random
        rng = random.Random(5)
        v = [st.poisson_draw(rng, 120.0) for _ in range(4000)]
        mean = sum(v) / len(v)
        var = sum((x - mean) ** 2 for x in v) / len(v)
        self.assertAlmostEqual(mean, 120.0, delta=1.0)
        self.assertAlmostEqual(var, 120.0, delta=9.0)


class BoundaryTests(unittest.TestCase):
    def test_toys_match_exact_tail_and_naive_wilks_doubles_it(self):
        out = st.boundary(12, 8.0, 20000, 1)
        self.assertAlmostEqual(out["p_value_toys"], out["p_value_exact_poisson"], delta=0.012)
        self.assertAlmostEqual(out["p_value_naive_wilks_chi2_1dof"], 2 * out["p_value_half_chi2_asymptotic"], places=12)
        self.assertAlmostEqual(out["fraction_toys_with_q0_zero"], 0.5925, delta=0.012)  # P(N <= 8 | 8)

    def test_underfluctuation_has_q0_zero_and_unit_p(self):
        out = st.boundary(3, 8.0, 500, 2)
        self.assertEqual(out["q0_observed"], 0.0)
        self.assertEqual(out["p_value_toys"], 1.0)
        self.assertEqual(out["p_value_half_chi2_asymptotic"], 0.5)

    def test_seed_reproducible(self):
        self.assertEqual(st.boundary(10, 8.0, 1000, 7), st.boundary(10, 8.0, 1000, 7))


class TemplateStatTests(unittest.TestCase):
    def test_huge_mc_sample_recovers_true_template_spread(self):
        out = st.template_stat(SIG, BKG, 400, 0.2, 5e4, 5e4, 600, 3)
        self.assertAlmostEqual(out["spread_ratio_finite_over_true"], 1.0, delta=0.06)

    def test_small_mc_sample_inflates_the_spread(self):
        out = st.template_stat(SIG, BKG, 400, 0.2, 100, 100, 600, 3)
        self.assertGreater(out["spread_ratio_finite_over_true"], 1.2)

    def test_seed_reproducible_and_rejections(self):
        a = st.template_stat(SIG, BKG, 100, 0.5, 50, 50, 200, 9)
        self.assertEqual(a, st.template_stat(SIG, BKG, 100, 0.5, 50, 50, 200, 9))
        for call in (lambda: st.template_stat("1", BKG, 100, 0.5, 50, 50, 200, 1),
                     lambda: st.template_stat("0.1,0.2", "0.1,0.2,0.3", 100, 0.5, 50, 50, 200, 1),
                     lambda: st.template_stat(SIG, BKG, 100, 1.5, 50, 50, 200, 1),
                     lambda: st.template_stat(SIG, BKG, 100, 0.5, 50, 50, 200, None),
                     lambda: st.template_stat(SIG, "0,0,0,0", 100, 0.5, 50, 50, 200, 1)):
            with self.assertRaises(st.ToyError):
                call()


class TemplateBBTests(unittest.TestCase):
    def test_bb_lite_restores_error_calibration_that_the_naive_fit_loses(self):
        out = st.template_bb(SIG, BKG, 400, 0.4, 100, 100, 500, 1)["variants"]
        self.assertAlmostEqual(out["true_templates"]["pull_width"], 1.0, delta=0.15)
        self.assertGreater(out["naive_finite_templates"]["pull_width"], 1.3)
        self.assertLess(out["naive_finite_templates"]["coverage_of_delta_lnL_interval"], 0.6)
        self.assertAlmostEqual(out["barlow_beeston_lite"]["pull_width"], 1.0, delta=0.2)
        self.assertGreater(out["barlow_beeston_lite"]["coverage_of_delta_lnL_interval"],
                           out["naive_finite_templates"]["coverage_of_delta_lnL_interval"])

    def test_huge_mc_makes_the_variants_agree_and_seed_reproduces(self):
        out = st.template_bb(SIG, BKG, 400, 0.4, 2e4, 2e4, 200, 2)
        sp = [v["spread"] for v in out["variants"].values()]
        self.assertLess(max(sp) / min(sp), 1.1)
        self.assertEqual(out, st.template_bb(SIG, BKG, 400, 0.4, 2e4, 2e4, 200, 2))

    def test_rejections(self):
        for call in (lambda: st.template_bb("1", BKG, 100, 0.5, 50, 50, 200, 1),
                     lambda: st.template_bb(SIG, BKG, 100, -0.5, 50, 50, 200, 1),
                     lambda: st.template_bb(SIG, BKG, 100, 0.5, 50, 50, 200, None)):
            with self.assertRaises(st.ToyError):
                call()


class RatioCovTests(unittest.TestCase):
    DOC = {"numerator": [900, 700, 500, 300], "denominator": [3000, 2500, 2000, 1500]}

    def doc(self, kind, **kw):
        sysd = {"name": "x", "sigma_num": 0.03, "sigma_den": 0.0, "num_den_rho": 0.0, "bin_correlation": dict(kind=kind, **kw)}
        return dict(self.DOC, systematics=[sysd])

    def test_shared_systematic_is_underestimated_if_bins_are_assumed_independent(self):
        full = st.ratio_cov(self.doc("full"), 4000, 1)["weighted_mean_fractional_spread"]
        none = st.ratio_cov(self.doc("none"), 4000, 1)["weighted_mean_fractional_spread"]
        self.assertAlmostEqual(full["systematic_only"], 0.03, delta=0.002)
        self.assertGreater(full["underestimate_factor_if_independent"], 1.8)
        self.assertAlmostEqual(none["underestimate_factor_if_independent"], 1.0, delta=0.1)

    def test_exponential_correlation_is_between_and_decays(self):
        out = st.ratio_cov(self.doc("exponential", length=1.5), 4000, 1)
        c = out["systematic_correlation_between_bins"][0]
        self.assertGreater(c[1], c[3])
        self.assertAlmostEqual(c[1], math.exp(-1 / 1.5), delta=0.06)

    def test_cancellation_and_reproducibility(self):
        d = self.doc("full")
        d["systematics"][0].update(sigma_den=0.03, num_den_rho=1.0)
        self.assertLess(st.ratio_cov(d, 500, 1)["weighted_mean_fractional_spread"]["systematic_only"], 1e-9)
        self.assertEqual(st.ratio_cov(self.doc("none"), 300, 7), st.ratio_cov(self.doc("none"), 300, 7))

    def test_rejections(self):
        bad = [[1], {"numerator": [1.0], "denominator": [1.0]}, {"numerator": [1, 2], "denominator": [1]},
               dict(self.DOC, systematics=[{"sigma_num": 0.1}]),
               dict(self.DOC, systematics=[{"name": "x", "bin_correlation": {"kind": "weird"}}]),
               dict(self.DOC, systematics=[{"name": "x", "sigma_num": 2.0}]),
               dict(self.DOC, systematics=[{"name": "x", "sigma_num": [0.1, 0.1]}]),
               dict(self.DOC, systematics=[{"name": "x", "bin_correlation": {"kind": "exponential"}}])]
        for d in bad:
            with self.assertRaises(st.ToyError):
                st.ratio_cov(d, 200, 1)


class UnfoldScanTests(unittest.TestCase):
    def test_identity_response_is_unbiased_at_one_iteration(self):
        doc = {"response": [[1, 0], [0, 1]], "truth": [500, 300], "max_iterations": 3}
        out = st.unfold_scan(doc, 300, 1)
        self.assertLess(out["scan"][0]["rms_relative_bias"], 0.02)

    def test_bias_falls_and_spread_grows_with_iterations(self):
        out = st.unfold_scan(RESPONSE, 300, 1)["scan"]
        self.assertGreater(out[0]["rms_relative_bias"], out[-1]["rms_relative_bias"])
        self.assertLess(out[0]["rms_relative_spread"], out[-1]["rms_relative_spread"])

    def test_transposed_orientation_gives_the_same_scan(self):
        t = dict(RESPONSE, response=[list(c) for c in zip(*RESPONSE["response"])], orientation="rows_truth_cols_reco")
        self.assertEqual(st.unfold_scan(t, 100, 4)["scan"], st.unfold_scan(RESPONSE, 100, 4)["scan"])

    def test_rejections(self):
        for bad in (dict(RESPONSE, response=[[0.6, 0.2], [0.2]]), dict(RESPONSE, truth=[1, 2]),
                    dict(RESPONSE, response=[[0.9, 0.2, 0.0], [0.9, 0.5, 0.2], [0.0, 0.2, 0.6]]),
                    dict(RESPONSE, max_iterations=0), dict(RESPONSE, orientation="sideways"),
                    dict(RESPONSE, response=[[0.0, 0.2, 0.0], [0.0, 0.5, 0.2], [0.0, 0.2, 0.6]]), [1, 2]):
            with self.assertRaises(st.ToyError):
                st.unfold_scan(bad, 100, 1)


class RatioTests(unittest.TestCase):
    def test_full_correlation_cancels_and_independence_adds(self):
        cancel = st.ratio_toys(4000, 9000, ["eff:0.05:0.05:1"], 6000, 1)
        indep = st.ratio_toys(4000, 9000, ["eff:0.05:0.05:0"], 6000, 1)
        self.assertLess(cancel["fractional_spread_systematic_only"], 1e-9)
        self.assertAlmostEqual(indep["fractional_spread_systematic_only"], 0.05 * math.sqrt(2), delta=0.004)
        self.assertAlmostEqual(cancel["fractional_spread_statistical_only"], math.sqrt(1 / 4000 + 1 / 9000), delta=0.002)

    def test_partial_correlation_analytic_value_and_reproducible(self):
        out = st.ratio_toys(400, 900, ["a:0.03:0.04:0.5"], 200, 3)
        self.assertAlmostEqual(out["systematics"][0]["fractional_effect_on_ratio_analytic"],
                               math.sqrt(0.03 ** 2 + 0.04 ** 2 - 2 * 0.5 * 0.03 * 0.04), places=12)
        self.assertEqual(out, st.ratio_toys(400, 900, ["a:0.03:0.04:0.5"], 200, 3))

    def test_rejections(self):
        for call in (lambda: st.ratio_toys(10, 0, [], 200, 1), lambda: st.ratio_toys(10, 20, ["a:0.1:0.1:1.5"], 200, 1),
                     lambda: st.ratio_toys(10, 20, ["a:0.1:0.1"], 200, 1), lambda: st.ratio_toys(10, 20, ["a:2:0.1:0"], 200, 1),
                     lambda: st.ratio_toys(10, 20, [], 10, 1), lambda: st.ratio_toys(10, 20, [], 200, True)):
            with self.assertRaises(st.ToyError):
                call()


class CliTests(unittest.TestCase):
    def run_cli(self, *argv):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = st.main(list(argv))
        return code, json.loads(buf.getvalue())

    def test_each_subcommand_ok_and_echoes_seed(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "u.json"
            path.write_text(json.dumps(RESPONSE))
            rpath = Path(tmp) / "r.json"
            rpath.write_text(json.dumps(RatioCovTests.DOC))
            for argv in (["boundary", "--n", "5", "--b", "3", "--toys", "200", "--seed", "4"],
                         ["template-stat", "--sig", SIG, "--bkg", BKG, "--n-data", "100", "--f", "0.3", "--mc-sig", "100",
                          "--mc-bkg", "100", "--toys", "100", "--seed", "4"],
                         ["unfold-scan", "--input", str(path), "--toys", "50", "--seed", "4"],
                         ["template-bb", "--sig", SIG, "--bkg", BKG, "--n-data", "100", "--f", "0.3", "--mc-sig", "100",
                          "--mc-bkg", "100", "--toys", "100", "--seed", "4"],
                         ["ratio-cov", "--input", str(rpath), "--toys", "100", "--seed", "4"],
                         ["ratio-toys", "--n1", "50", "--n2", "80", "--sys", "x:0.02:0.02:1", "--toys", "200", "--seed", "4"]):
                code, out = self.run_cli(*argv)
                self.assertEqual((code, out["status"], out["seed"]), (0, "ok", 4), argv[0])
                self.assertEqual(out["label"], "[General method]")

    def test_seed_required_and_bad_input_exits_2(self):
        with self.assertRaises(SystemExit), contextlib.redirect_stderr(io.StringIO()):
            st.main(["boundary", "--n", "5", "--b", "3"])
        code, out = self.run_cli("boundary", "--n", "5", "--b", "0", "--seed", "1")
        self.assertEqual((code, out["status"]), (2, "rejected"))
        code, out = self.run_cli("unfold-scan", "--input", "/nonexistent/x.json", "--seed", "1")
        self.assertEqual((code, out["status"]), (2, "rejected"))


if __name__ == "__main__":
    unittest.main()
