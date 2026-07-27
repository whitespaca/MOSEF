"""Exact tests for the M13 arbitrary-exponent factor-scale bound."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

from mosef_reference import (
    factor_scale_divisor_bound,
    factor_scale_threshold,
    is_prime,
    positive_divisors,
)

from scripts.run_m13_general_factor_scale_search import search


class GeneralFactorScaleTests(unittest.TestCase):
    def test_threshold_is_exact_and_valid(self) -> None:
        self.assertEqual(factor_scale_threshold(1), 2)
        self.assertEqual(factor_scale_threshold(64), 2)
        self.assertEqual(factor_scale_threshold(1023), 10)
        self.assertEqual(factor_scale_threshold(1024), 8)
        for input_bits in range(1, 5000):
            threshold = factor_scale_threshold(input_bits)
            self.assertGreaterEqual(threshold, 2)
            self.assertLessEqual(threshold, input_bits + 1)

    def test_hand_computed_squareful_bound(self) -> None:
        bound = factor_scale_divisor_bound(2**4 * 3**2 * 11**3, 127, 3)
        self.assertEqual(bound.small_choice_count, 15)
        self.assertEqual(bound.large_multiplicity, 3)
        self.assertEqual(bound.large_selection_limit, 3)
        self.assertEqual(bound.large_choice_bound, 8)
        self.assertEqual(bound.divisor_candidate_bound, 120)

    def test_all_small_exponents_obey_bound(self) -> None:
        for exponent in range(2, 4097):
            divisors = positive_divisors(exponent)
            for target_max in (7, 31, 127, 511):
                for threshold in (2, 3, 5, 11):
                    bound = factor_scale_divisor_bound(
                        exponent, target_max, threshold
                    )
                    relevant = sum(
                        divisor <= target_max + 1 for divisor in divisors
                    )
                    self.assertLessEqual(
                        relevant, bound.divisor_candidate_bound
                    )

    def test_prime_candidates_obey_twice_divisor_bound(self) -> None:
        families = (
            2**20,
            2**8 * 3**6 * 5**3,
            17 * 19 * 23 * 29,
            2 * 7**5 * 31**2,
        )
        for exponent in families:
            for target_max in (127, 1023, 4095):
                bound = factor_scale_divisor_bound(exponent, target_max, 5)
                hits = {
                    candidate
                    for divisor in positive_divisors(exponent)
                    if divisor <= target_max + 1
                    for candidate in (divisor - 1, divisor + 1)
                    if 3 <= candidate <= target_max
                    and candidate % 2 == 1
                    and is_prime(candidate)
                }
                self.assertLessEqual(len(hits), bound.prime_candidate_bound)

    def test_invalid_domains(self) -> None:
        for value in (True, 1, 0, -1):
            with self.assertRaises(ValueError):
                factor_scale_divisor_bound(value, 7, 2)
        for value in (True, 2, 0, -1):
            with self.assertRaises(ValueError):
                factor_scale_divisor_bound(6, value, 2)
        for value in (True, 1, 0, -1):
            with self.assertRaises(ValueError):
                factor_scale_divisor_bound(6, 7, value)
        for value in (True, 0, -1):
            with self.assertRaises(ValueError):
                factor_scale_threshold(value)

    def test_registered_search_smoke(self) -> None:
        result = search(4096, 8)
        self.assertGreater(result["counts"]["bound_checks"], 10_000)
        self.assertEqual(len(result["summary_sha256"]), 64)


if __name__ == "__main__":
    unittest.main()
