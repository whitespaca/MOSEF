"""Exact tests for the M11 boundary divisor budget and primorial schedule."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

from mosef_reference import (
    boundary_divisor_budget,
    divisor_count,
    exponent_bit_length,
    first_primes,
    global_hit_primes,
    is_prime,
    primorial_divisors,
    primorial_schedule,
)

from scripts.run_m11_boundary_schedule_search import search


class BoundaryDivisorBudgetTests(unittest.TestCase):
    def test_exact_small_parameters(self) -> None:
        length_one = boundary_divisor_budget(1)
        self.assertEqual(length_one.logarithm_scale, 1)
        self.assertEqual(length_one.iterated_logarithm_scale, 1)
        self.assertEqual(length_one.split_threshold, 1)
        self.assertEqual(length_one.large_multiplicity_bound, 0)
        self.assertEqual(length_one.one_length_bound, 2)
        self.assertEqual(length_one.monotone_bound, 2)

        length_three = boundary_divisor_budget(3)
        self.assertEqual(length_three.logarithm_scale, 2)
        self.assertEqual(length_three.iterated_logarithm_scale, 2)
        self.assertEqual(length_three.split_threshold, 1)
        self.assertEqual(length_three.large_multiplicity_bound, 2)
        self.assertEqual(length_three.one_length_bound, 16)

        length_4096 = boundary_divisor_budget(4096)
        self.assertEqual(length_4096.split_threshold, 6)
        self.assertEqual(length_4096.large_multiplicity_bound, 1459)
        self.assertEqual(length_4096.one_length_bound.bit_length(), 1532)

    def test_budget_bounds_every_small_divisor_count(self) -> None:
        previous_envelope = 0
        for value in range(1, 65_536):
            budget = boundary_divisor_budget(exponent_bit_length(value))
            self.assertLessEqual(divisor_count(value), budget.one_length_bound)
            self.assertLessEqual(budget.one_length_bound, budget.monotone_bound)
            self.assertGreaterEqual(budget.monotone_bound, previous_envelope)
            previous_envelope = budget.monotone_bound

    def test_primorial_constructor_and_node_accounting(self) -> None:
        schedule = primorial_schedule(6)
        self.assertEqual(schedule.primes, (2, 3, 5, 7, 11, 13))
        self.assertEqual(schedule.exponent, 30_030)
        self.assertEqual(schedule.bit_length, 15)
        self.assertEqual(schedule.divisor_count, 64)
        self.assertEqual(schedule.binary_multiplication_nodes, 22)
        self.assertLessEqual(
            schedule.binary_multiplication_nodes,
            2 * schedule.bit_length - 2,
        )

    def test_primorial_divisors_are_exact(self) -> None:
        expected = (1, 2, 3, 5, 6, 7, 10, 14, 15, 21, 30, 35, 42, 70, 105, 210)
        self.assertEqual(primorial_divisors(4), expected)
        for count in range(1, 8):
            schedule = primorial_schedule(count)
            divisors = primorial_divisors(count)
            self.assertEqual(len(divisors), schedule.divisor_count)
            self.assertEqual(len(set(divisors)), schedule.divisor_count)
            self.assertTrue(all(schedule.exponent % divisor == 0 for divisor in divisors))

    def test_squarefree_even_primorial_channels_are_disjoint(self) -> None:
        for count in range(1, 8):
            schedule = primorial_schedule(count)
            divisors = primorial_divisors(count)
            minus_hits = {
                divisor + 1
                for divisor in divisors
                if divisor + 1 >= 3 and is_prime(divisor + 1)
            }
            plus_hits = {
                divisor - 1
                for divisor in divisors
                if divisor - 1 >= 3 and is_prime(divisor - 1)
            }
            self.assertFalse(minus_hits & plus_hits)
            self.assertEqual(
                global_hit_primes((schedule.exponent,)),
                tuple(sorted(minus_hits | plus_hits)),
            )

    def test_invalid_domains_raise(self) -> None:
        invalid_calls = (
            lambda: boundary_divisor_budget(0),
            lambda: boundary_divisor_budget(False),
            lambda: first_primes(0),
            lambda: first_primes(True),
            lambda: primorial_schedule(0),
            lambda: primorial_divisors(False),
        )
        for invalid_call in invalid_calls:
            with self.subTest(invalid_call=invalid_call), self.assertRaises(ValueError):
                invalid_call()

    def test_registered_search_small_box(self) -> None:
        summary = search(1024, 6)
        self.assertEqual(summary["divisor_budget_checks"], 1023)
        self.assertEqual(summary["rosser_schoenfeld_checks"], 1)
        self.assertEqual(summary["primorial_records"][-1]["hit_count"], 36)
        self.assertTrue(all(summary["checked"].values()))


if __name__ == "__main__":
    unittest.main()
