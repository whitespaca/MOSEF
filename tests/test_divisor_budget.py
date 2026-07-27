"""Exact tests for the M9 exponent-encoding divisor-budget barrier."""

from __future__ import annotations

import itertools
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

from mosef_reference import (
    bit_length_divisor_budget,
    combined_asymmetry,
    combined_signature,
    divisor_count,
    exponent_bit_length,
    global_hit_primes,
    is_prime,
    positive_divisors,
)


class ExponentEncodingDivisorBudgetTests(unittest.TestCase):
    def test_bit_length_and_exact_budget_parameters(self) -> None:
        self.assertEqual(exponent_bit_length(1), 1)
        self.assertEqual(exponent_bit_length(7), 3)
        self.assertEqual(exponent_bit_length(8), 4)
        self.assertEqual(
            bit_length_divisor_budget(1),
            bit_length_divisor_budget(1).__class__(
                bit_length=1,
                split_threshold=1,
                large_multiplicity_bound=0,
                one_length_bound=2,
                monotone_bound=2,
            ),
        )
        length_three = bit_length_divisor_budget(3)
        self.assertEqual(length_three.split_threshold, 1)
        self.assertEqual(length_three.large_multiplicity_bound, 2)
        self.assertEqual(length_three.one_length_bound, 16)

    def test_exact_divisor_budget_exhaustively(self) -> None:
        previous_envelope = 0
        for value in range(1, 10_001):
            budget = bit_length_divisor_budget(exponent_bit_length(value))
            self.assertLessEqual(divisor_count(value), budget.one_length_bound, value)
            self.assertLessEqual(budget.one_length_bound, budget.monotone_bound)
            self.assertGreaterEqual(budget.monotone_bound, previous_envelope)
            previous_envelope = budget.monotone_bound

    def test_positive_divisors(self) -> None:
        self.assertEqual(positive_divisors(1), (1,))
        self.assertEqual(positive_divisors(36), (1, 2, 3, 4, 6, 9, 12, 18, 36))
        self.assertEqual(len(positive_divisors(840)), divisor_count(840))

    def test_global_hit_oracle_matches_direct_scan(self) -> None:
        for exponent in range(1, 501):
            expected = tuple(
                prime
                for prime in range(3, exponent + 2, 2)
                if is_prime(prime)
                and any(bit for bits in combined_signature(prime, (exponent,)) for bit in bits)
            )
            self.assertEqual(global_hit_primes((exponent,)), expected, exponent)
            self.assertLessEqual(len(expected), 2 * divisor_count(exponent))

    def test_global_family_hit_set_is_exact_union(self) -> None:
        family = (12, 18, 60)
        expected = tuple(
            sorted(
                set().union(
                    *(set(global_hit_primes((exponent,))) for exponent in family)
                )
            )
        )
        self.assertEqual(global_hit_primes(family), expected)
        self.assertLessEqual(
            len(expected),
            2 * sum(divisor_count(exponent) for exponent in family),
        )

    def test_smallest_large_value_zero_pair(self) -> None:
        primes = tuple(value for value in range(3, 20, 2) if is_prime(value))
        first: tuple[int, int, int] | None = None
        for exponent in range(1, 20):
            for left, right in itertools.combinations(primes, 2):
                if exponent <= right + 1:
                    continue
                left_signature = combined_signature(left, (exponent,))
                right_signature = combined_signature(right, (exponent,))
                if (
                    not any(bit for bits in left_signature for bit in bits)
                    and not any(bit for bits in right_signature for bit in bits)
                ):
                    first = (exponent, left, right)
                    break
            if first is not None:
                break
        self.assertEqual(first, (7, 3, 5))
        self.assertFalse(combined_asymmetry(3, 5, (7,)))
        self.assertGreater(7, 5 + 1)

    def test_large_value_can_hit_without_guaranteeing_coverage(self) -> None:
        self.assertEqual(global_hit_primes((7,)), ())
        self.assertEqual(global_hit_primes((12,)), (3, 5, 7, 11, 13))

    def test_invalid_domains_raise(self) -> None:
        invalid_calls = (
            lambda: exponent_bit_length(0),
            lambda: exponent_bit_length(True),
            lambda: bit_length_divisor_budget(0),
            lambda: bit_length_divisor_budget(False),
            lambda: positive_divisors(0),
            lambda: global_hit_primes(()),
            lambda: global_hit_primes((False,)),
        )
        for invalid_call in invalid_calls:
            with self.subTest(invalid_call=invalid_call), self.assertRaises(ValueError):
                invalid_call()


if __name__ == "__main__":
    unittest.main()
