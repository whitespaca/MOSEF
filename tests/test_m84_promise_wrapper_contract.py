"""Mutation tests for the independent M84 contract checker."""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path
from types import ModuleType

ROOT = Path(__file__).resolve().parents[1]


def load_checker() -> ModuleType:
    path = ROOT / "scripts" / "check_m84_promise_wrappers.py"
    spec = importlib.util.spec_from_file_location("check_m84_wrappers", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load M84 checker")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


CHECKER = load_checker()


class M84ContractTests(unittest.TestCase):
    def test_registered_contract_passes(self) -> None:
        self.assertEqual(CHECKER.validate(), [])

    def test_factor_aware_oracle_leak_is_rejected(self) -> None:
        text = CHECKER.IMPLEMENTATION.read_text(encoding="utf-8")
        errors = CHECKER.validate_implementation(text + "\nprime_factorization\n")
        self.assertIn(
            "factor-aware oracle leaked into wrapper: prime_factorization",
            errors,
        )

    def test_missing_unresolved_state_is_rejected(self) -> None:
        text = CHECKER.IMPLEMENTATION.read_text(encoding="utf-8")
        altered = text.replace('UNRESOLVED = "unresolved"', "", 1)
        errors = CHECKER.validate_implementation(altered)
        self.assertIn(
            'implementation contract token missing: UNRESOLVED = "unresolved"',
            errors,
        )

    def test_missing_global_recursion_bound_is_rejected(self) -> None:
        text = CHECKER.PROOF.read_text(encoding="utf-8")
        altered = text.replace("fewer than \\(4m\\) total invocations", "", 1)
        errors = CHECKER.validate_proof(altered)
        self.assertIn(
            "proof contract token missing: fewer than \\(4m\\) total invocations",
            errors,
        )

    def test_missing_korean_probability_bound_is_rejected(self) -> None:
        path = ROOT / "paper" / "focused" / "promise-factorization-ko.tex"
        text = path.read_text(encoding="utf-8")
        altered = text.replace("\\frac{11}{12}", "\\frac{10}{12}")
        errors = CHECKER.validate_paper(path, altered)
        self.assertTrue(any("\\frac{11}{12}" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
