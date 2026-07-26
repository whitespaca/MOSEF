"""Exact tests for the M12 factor-scale primorial bound."""

from __future__ import annotations

from itertools import combinations
from math import comb
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

from mosef_reference import (  # noqa: E402
    combined_asymmetry,
    combined_signature,
    first_primes,
    is_prime,
    primorial_divisors,
    primorial_factor_scale_bound,
)
from scripts.run_m12_primorial_scale_search import search  # noqa: E402


class PrimorialScaleTests(unittest.TestCase):
    def test_exact_support_thresholds(self) -> None:
        self.assertEqual(primorial_factor_scale_bound(8, 3).support_limit, 1)
        self.assertEqual(primorial_factor_scale_bound(8, 5).support_limit, 2)
        self.assertEqual(primorial_factor_scale_bound(8, 23).support_limit, 3)
        self.assertEqual(primorial_factor_scale_bound(8, 119).support_limit, 4)

    def test_binomial_formula(self) -> None:
        bound = primorial_factor_scale_bound(10, 127)
        self.assertEqual(bound.support_limit, 4)
        expected = sum(comb(10, index) for index in range(5))
        self.assertEqual(bound.divisor_candidate_bound, expected)
        self.assertEqual(bound.prime_candidate_bound, 2 * expected)

    def test_all_small_divisors_obey_support_and_count_bound(self) -> None:
        for count in range(1, 11):
            divisors = primorial_divisors(count)
            schedule_primes = first_primes(count)
            for target_max in (3, 7, 31, 127, 1023, 4095):
                bound = primorial_factor_scale_bound(count, target_max)
                relevant = [
                    divisor for divisor in divisors if divisor <= target_max + 1
                ]
                self.assertLessEqual(
                    len(relevant), bound.divisor_candidate_bound
                )
                for divisor in relevant:
                    support = sum(divisor % prime == 0 for prime in schedule_primes)
                    self.assertLessEqual(support, bound.support_limit)

    def test_actual_prime_hits_obey_candidate_bound(self) -> None:
        for count in range(1, 11):
            for target_max in (31, 127, 1023):
                bound = primorial_factor_scale_bound(count, target_max)
                hits = {
                    candidate
                    for divisor in primorial_divisors(count)
                    if divisor <= target_max + 1
                    for candidate in (divisor - 1, divisor + 1)
                    if 3 <= candidate <= target_max
                    and candidate % 2 == 1
                    and is_prime(candidate)
                }
                self.assertLessEqual(len(hits), bound.prime_candidate_bound)

    def test_three_signature_pair_formula(self) -> None:
        for count in range(1, 8):
            exponent = 1
            for prime in first_primes(count):
                exponent *= prime
            population = [
                value for value in range(3, 100, 2) if is_prime(value)
            ]
            signatures = {
                prime: combined_signature(prime, [exponent])[0]
                for prime in population
            }
            minus = sum(signature == (True, False) for signature in signatures.values())
            plus = sum(signature == (False, True) for signature in signatures.values())
            zero = sum(signature == (False, False) for signature in signatures.values())
            self.assertFalse(any(signature == (True, True) for signature in signatures.values()))
            formula = minus * plus + zero * (minus + plus)
            direct = sum(
                combined_asymmetry(left, right, [exponent])
                for left, right in combinations(population, 2)
            )
            self.assertEqual(formula, direct)

    def test_invalid_domains(self) -> None:
        for value in (True, 0, -1):
            with self.assertRaises(ValueError):
                primorial_factor_scale_bound(value, 7)
        for value in (True, 2, 0, -1):
            with self.assertRaises(ValueError):
                primorial_factor_scale_bound(3, value)

    def test_registered_search_smoke(self) -> None:
        result = search(8, 10)
        self.assertEqual(result["counts"]["pair_formula_checks"], 6)
        self.assertEqual(len(result["summary_sha256"]), 64)


if __name__ == "__main__":
    unittest.main()
