"""Regression tests for the M81 standard-bit-length migration."""

from __future__ import annotations

import unittest

from python.mosef_reference.bitlength_audit import (
    balanced_prime_interval,
    balanced_prime_population,
    compare_lengths,
    is_power_of_two,
    legacy_ceiling_log_length,
    standard_bit_length,
)
from python.mosef_reference.semismooth import factor_semismooth_promised


class BitLengthAuditTests(unittest.TestCase):
    def test_standard_values_include_exact_powers_of_two(self) -> None:
        expected = {
            1: (1, 0),
            2: (2, 1),
            3: (2, 2),
            4: (3, 2),
            7: (3, 3),
            8: (4, 3),
            9: (4, 4),
        }
        for value, lengths in expected.items():
            self.assertEqual(
                (standard_bit_length(value), legacy_ceiling_log_length(value)),
                lengths,
            )

    def test_discrepancy_is_exactly_the_power_of_two_indicator(self) -> None:
        for value in range(1, 1 << 16):
            comparison = compare_lengths(value)
            self.assertEqual(comparison.discrepancy, int(is_power_of_two(value)))
            self.assertEqual(comparison.is_power_of_two, is_power_of_two(value))

    def test_balanced_odd_products_keep_both_length_indices(self) -> None:
        for input_length in range(9, 21):
            lower, upper = balanced_prime_interval(input_length)
            primes = balanced_prime_population(input_length)
            self.assertGreaterEqual(primes[0], lower)
            self.assertLessEqual(primes[-1], upper)
            for first, second in (
                (primes[0], primes[0]),
                (primes[0], primes[-1]),
                (primes[-1], primes[-1]),
            ):
                product = first * second
                self.assertEqual(standard_bit_length(product), input_length)
                self.assertEqual(
                    legacy_ceiling_log_length(product),
                    input_length,
                )
                self.assertFalse(is_power_of_two(product))

    def test_perfect_power_recursion_uses_the_correct_input_domain(self) -> None:
        self.assertEqual(
            factor_semismooth_promised(1 << 12, 2, 2, 1),
            (2,) * 12,
        )
        self.assertEqual(
            factor_semismooth_promised(3**8, 2, 2, 1),
            (3,) * 8,
        )
        self.assertEqual(standard_bit_length(1 << 12), 13)
        self.assertEqual(legacy_ceiling_log_length(1 << 12), 12)
        self.assertEqual(
            standard_bit_length(3**8),
            legacy_ceiling_log_length(3**8),
        )

    def test_invalid_inputs_are_rejected(self) -> None:
        for call in (
            lambda: standard_bit_length(0),
            lambda: legacy_ceiling_log_length(-1),
            lambda: is_power_of_two(True),
            lambda: balanced_prime_interval(3),
        ):
            with self.assertRaises(ValueError):
                call()


if __name__ == "__main__":
    unittest.main()
