"""Behavioral tests for the deep-learning diagnostic scripts.

Run from the skill directory with python3 -m unittest discover -s tests -v.
Standard library only. These tests do not require PyTorch to be installed: the
diagnostic scripts (other than check_pytorch_env.py) are expected to degrade
gracefully - `--help` always works, and any real invocation without PyTorch exits
cleanly with a one-line message instead of a raw traceback. When PyTorch *is*
installed, the graceful-degradation checks are skipped rather than actually
exercising GPU/CPU training code.
"""
from __future__ import annotations

import importlib
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

try:
    import torch as _torch_probe  # noqa: F401

    TORCH_AVAILABLE = True
except ModuleNotFoundError:
    TORCH_AVAILABLE = False

# (module name, extra CLI args needed to get past argparse before the torch check)
GUARDED_SCRIPTS = [
    ("benchmark_model", []),
    ("check_dataset_contract", []),
    ("find_nan_batches", []),
    ("inspect_checkpoint", ["nonexistent-checkpoint.pt"]),
    ("profile_dataloader", []),
]


class HelpAlwaysWorksTests(unittest.TestCase):
    """--help must succeed whether or not PyTorch is installed."""

    def test_help_exits_zero_and_shows_usage(self):
        for name, _ in GUARDED_SCRIPTS:
            with self.subTest(script=name):
                result = subprocess.run(
                    [sys.executable, str(SCRIPTS / f"{name}.py"), "--help"],
                    capture_output=True,
                    text=True,
                )
                self.assertEqual(result.returncode, 0)
                self.assertIn("usage:", result.stdout)


class ImportGuardStateTests(unittest.TestCase):
    """The guarded `import torch` sets consistent module-level state either way."""

    def test_torch_name_reflects_availability(self):
        for name, _ in GUARDED_SCRIPTS:
            with self.subTest(script=name):
                module = importlib.import_module(name)
                if TORCH_AVAILABLE:
                    self.assertIsNotNone(module.torch)
                    self.assertIsNone(module._TORCH_IMPORT_ERROR)
                else:
                    self.assertIsNone(module.torch)
                    self.assertIsInstance(module._TORCH_IMPORT_ERROR, ModuleNotFoundError)


@unittest.skipIf(TORCH_AVAILABLE, "only meaningful when PyTorch is not installed")
class CleanDegradationWithoutTorchTests(unittest.TestCase):
    """Without PyTorch, a real (non---help) invocation must fail cleanly, not crash."""

    def test_exits_with_clear_message_not_traceback(self):
        for name, extra_args in GUARDED_SCRIPTS:
            with self.subTest(script=name):
                result = subprocess.run(
                    [sys.executable, str(SCRIPTS / f"{name}.py"), *extra_args],
                    capture_output=True,
                    text=True,
                )
                self.assertEqual(result.returncode, 1)
                self.assertIn("PyTorch is required", result.stdout + result.stderr)
                self.assertNotIn("Traceback", result.stderr)

    def test_check_pytorch_env_reports_missing_torch_cleanly(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPTS / "check_pytorch_env.py")],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("ERROR: Could not import torch", result.stdout)
        self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
