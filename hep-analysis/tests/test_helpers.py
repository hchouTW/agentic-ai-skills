"""Behavioral tests for histogram failures and analytic Poisson reference cases.

Run from the skill directory with python3 -m unittest discover -s tests -v.
Uses synthetic data and standard library only; no experiment files are needed.
"""
import copy
import json
import math
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from audit_histograms import audit
from counting_reference import bayesian_upper, poisson_upper_tail
from tag_and_probe_efficiency import clopper_pearson, efficiency_bin
from pileup_reweight import compute_weights, normalize, profile_mean, reweighted_mean


class HistogramTests(unittest.TestCase):
    def setUp(self):
        self.bundle = json.loads((ROOT / 'assets/histograms.example.json').read_text())
        self.hist = self.bundle['histograms']['synthetic_background']

    def test_good_input_not_mutated(self):
        previous = copy.deepcopy(self.bundle)
        self.assertEqual(audit(self.bundle), ([], []))
        self.assertEqual(previous, self.bundle)

    def test_signed_mc_not_poisson(self):
        self.hist['sumw'][0] = -2
        self.assertFalse(audit(self.bundle)[0])
        self.assertTrue(audit(self.bundle)[1])
        self.bundle['kind'] = 'poisson_expectation'
        self.assertTrue(audit(self.bundle)[0])

    def test_missing_and_mismatched_variation(self):
        del self.hist['variations']['scaleDown']
        self.hist['variations']['scaleUp']['edges'][1] = 40
        self.assertEqual(len(audit(self.bundle)[0]), 2)

    def test_nonfinite_variance_and_dimensions(self):
        for field, value in [('sumw', [float('nan'), 8]), ('sumw2', [-1, 10]), ('sumw2', [1]), ('edges', [0, 0, 100])]:
            with self.subTest(field=field, value=value):
                bundle = copy.deepcopy(self.bundle)
                bundle['histograms']['synthetic_background'][field] = value
                self.assertTrue(audit(bundle)[0])

    def test_malformed_types(self):
        for bundle in (None, [], {}, {'schema_version':1,'kind':'mc','histograms':{'bad':None}}):
            self.assertTrue(audit(bundle)[0])

    def test_bool_not_numeric(self):
        self.hist['sumw'][0] = True
        self.assertTrue(audit(self.bundle)[0])

    def test_identical_variation_warns(self):
        self.hist['variations']['scaleUp'] = {k: self.hist[k][:] for k in ('edges','sumw','sumw2')}
        self.assertFalse(audit(self.bundle)[0])
        self.assertTrue(audit(self.bundle)[1])

    def test_cli_success(self):
        result = subprocess.run([sys.executable, str(ROOT/'scripts/audit_histograms.py'), str(ROOT/'assets/histograms.example.json')], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        self.assertTrue(json.loads(result.stdout)['ok'])


class CountingTests(unittest.TestCase):
    def test_zero_count_analytic(self):
        for b in (0, 3, 100, 500):
            self.assertAlmostEqual(bayesian_upper(0, b), -math.log(.05), places=10)

    def test_one_count_known_bound(self):
        self.assertAlmostEqual(bayesian_upper(1, 0), 4.743864518390578, places=10)

    def test_tail_exact_cases(self):
        self.assertEqual(poisson_upper_tail(0, 0), 1)
        self.assertEqual(poisson_upper_tail(2, 0), 0)
        self.assertAlmostEqual(poisson_upper_tail(1, 2), 1-math.exp(-2), places=14)
        self.assertAlmostEqual(poisson_upper_tail(2, 2), 1-3*math.exp(-2), places=14)
        self.assertAlmostEqual(poisson_upper_tail(10, 1), 1.114254783387207e-7, delta=1e-20)

    def test_monotonic_confidence(self):
        self.assertLess(bayesian_upper(5, 2, .9), bayesian_upper(5, 2, .95))

    def test_invalid_input_rejected(self):
        for n,b in ((-1,0),(1.5,0),(True,0),(1,-1),(1,float('nan')),(501,0)):
            with self.assertRaises(ValueError):
                bayesian_upper(n,b)
        with self.assertRaises(ValueError):
            bayesian_upper(0,0,1)


class TagAndProbeTests(unittest.TestCase):
    def test_known_exact_intervals(self):
        # Textbook exact Clopper-Pearson 95% intervals; independently cross-checked
        # against scipy.stats.beta.ppf during development (scipy is not a runtime
        # dependency of this package, so the expected values are hardcoded here).
        lo, hi = clopper_pearson(0, 10, 0.95)
        self.assertEqual(lo, 0.0)
        self.assertAlmostEqual(hi, 0.30849710781876385, places=10)

        lo, hi = clopper_pearson(10, 10, 0.95)
        self.assertAlmostEqual(lo, 0.6915028921812392, places=10)
        self.assertEqual(hi, 1.0)

        lo, hi = clopper_pearson(5, 20, 0.95)
        self.assertAlmostEqual(lo, 0.08657146910143451, places=8)
        self.assertAlmostEqual(hi, 0.49104587170795455, places=8)

    def test_interval_widens_with_confidence_level(self):
        lo68, hi68 = clopper_pearson(30, 100, 0.68)
        lo95, hi95 = clopper_pearson(30, 100, 0.95)
        lo99, hi99 = clopper_pearson(30, 100, 0.99)
        self.assertLess(lo99, lo95)
        self.assertLess(lo95, lo68)
        self.assertLess(hi68, hi95)
        self.assertLess(hi95, hi99)

    def test_interval_contains_point_estimate(self):
        for k, n in ((0, 10), (5, 20), (92, 100), (1, 1), (0, 1), (50, 100)):
            with self.subTest(k=k, n=n):
                point = k / n
                lo, hi = clopper_pearson(k, n, 0.95)
                self.assertLessEqual(lo, point)
                self.assertLessEqual(point, hi)

    def test_invalid_input_rejected(self):
        for k, n in ((-1, 10), (11, 10), (1.5, 10), (True, 10), (1, -1), (1, 200001)):
            with self.subTest(k=k, n=n):
                with self.assertRaises(ValueError):
                    clopper_pearson(k, n)
        with self.assertRaises(ValueError):
            clopper_pearson(1, 10, level=1.0)

    def test_efficiency_bin_zero_total_is_nan_not_error(self):
        result = efficiency_bin(0, 0)
        self.assertNotEqual(result['efficiency'], result['efficiency'])  # NaN

    def test_cli_matches_library_result(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / 'scripts/tag_and_probe_efficiency.py'),
             '--pass-count', '92', '--total', '100'],
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0)
        payload = json.loads(result.stdout)
        expected_lo, expected_hi = clopper_pearson(92, 100)
        self.assertAlmostEqual(payload['lower'], expected_lo, places=10)
        self.assertAlmostEqual(payload['upper'], expected_hi, places=10)

    def test_cli_rejects_pass_greater_than_total(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / 'scripts/tag_and_probe_efficiency.py'),
             '--pass-count', '11', '--total', '10'],
            capture_output=True, text=True,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('pass_count must be', result.stderr)


class PileupReweightTests(unittest.TestCase):
    def test_weights_reproduce_data_over_mc_ratio(self):
        weights, empty = compute_weights([0.2, 0.3, 0.5], [0.5, 0.3, 0.2])
        self.assertEqual(empty, [])
        for w, d, m in zip(weights, *[normalize(p)[0] for p in ([0.2, 0.3, 0.5], [0.5, 0.3, 0.2])]):
            self.assertAlmostEqual(w, d / m, places=12)

    def test_empty_mc_bin_with_data_is_flagged_not_inf(self):
        weights, empty = compute_weights([0.1, 0.9], [1.0, 0.0])
        self.assertEqual(empty, [1])
        self.assertIsNone(weights[1])
        self.assertIsNotNone(weights[0])

    def test_empty_mc_bin_without_data_is_not_flagged(self):
        # MC has zero probability in a bin, but so does data - nothing to reweight
        # there, so it should not be reported as an error.
        weights, empty = compute_weights([0.5, 0.0, 0.5], [0.4, 0.0, 0.6])
        self.assertEqual(empty, [])
        self.assertIsNone(weights[1])

    def test_reweighted_mean_matches_data_mean_closure(self):
        bin_centers = list(range(10))
        data_profile = [1, 2, 3, 4, 5, 4, 3, 2, 1, 1]
        mc_profile = [5, 4, 3, 2, 1, 1, 1, 1, 1, 1]
        weights, empty = compute_weights(data_profile, mc_profile)
        self.assertEqual(empty, [])
        reweighted = reweighted_mean(weights, mc_profile, bin_centers)
        expected = profile_mean(data_profile, bin_centers)
        self.assertAlmostEqual(reweighted, expected, places=10)

    def test_normalize_rejects_negative_or_all_zero(self):
        with self.assertRaises(ValueError):
            normalize([0.1, -0.2, 0.5])
        with self.assertRaises(ValueError):
            normalize([0.0, 0.0, 0.0])
        with self.assertRaises(ValueError):
            normalize([])

    def test_mismatched_lengths_rejected(self):
        with self.assertRaises(ValueError):
            compute_weights([0.5, 0.5], [1.0])

    def test_cli_closure_on_shipped_example(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / 'scripts/pileup_reweight.py'),
             str(ROOT / 'assets/pileup_profiles.example.json')],
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0)
        payload = json.loads(result.stdout)
        self.assertTrue(payload['ok'])
        self.assertAlmostEqual(payload['mc_mean_after_reweight'], payload['data_mean'], places=6)

    def test_cli_flags_missing_mc_coverage(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as handle:
            json.dump({'bin_centers': [0, 1, 2], 'data_profile': [0.2, 0.3, 0.5], 'mc_profile': [0.6, 0.4, 0.0]}, handle)
            path = handle.name
        try:
            result = subprocess.run(
                [sys.executable, str(ROOT / 'scripts/pileup_reweight.py'), path],
                capture_output=True, text=True,
            )
        finally:
            os.unlink(path)
        self.assertEqual(result.returncode, 1)
        payload = json.loads(result.stdout)
        self.assertFalse(payload['ok'])
        self.assertEqual(payload['empty_mc_bins_with_data'], [2])

    def test_cli_missing_file_fails_cleanly(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / 'scripts/pileup_reweight.py'), '/tmp/does-not-exist-pileup-bundle.json'],
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 1)
        payload = json.loads(result.stdout)
        self.assertFalse(payload['ok'])
        self.assertNotIn('Traceback', result.stderr)


if __name__ == '__main__':
    unittest.main()
