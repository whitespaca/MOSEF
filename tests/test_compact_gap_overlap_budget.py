"""Exact tests for the M48 compact-gap overlap budget."""

from __future__ import annotations

import math
import unittest

from python.mosef_reference.compact_gap_overlap_budget import (
    compact_gap_exponent,
    compact_gap_overlap_bit_bound,
    compact_gap_overlap_integer,
    compact_gap_overlap_population_upper_bound,
    compact_gap_overlap_profile,
)


def _compact_cofactor(level: int) -> int:
    exponent = compact_gap_exponent(level)
    numerator = 16 * (pow(2, exponent) + 3)
    cofactor, remainder = divmod(numerator, 35)
    if remainder:
        raise AssertionError("compact cofactor formula was not integral")
    return cofactor


class CompactGapOverlapBudgetTests(unittest.TestCase):
    def test_overlap_integer_small_values_and_bit_bound(self) -> None:
        self.assertEqual(compact_gap_overlap_integer(1), 35)
        self.assertEqual(compact_gap_overlap_integer(2), 32795)
        for gap in range(1, 8):
            with self.subTest(gap=gap):
                self.assertLessEqual(
                    compact_gap_overlap_integer(gap).bit_length(),
                    compact_gap_overlap_bit_bound(gap),
                )

    def test_common_large_prime_divisors_obey_overlap_integer(self) -> None:
        for first in range(2, 7):
            for second in range(first + 1, 8):
                common = math.gcd(
                    _compact_cofactor(first),
                    _compact_cofactor(second),
                )
                overlap = compact_gap_overlap_integer(second - first)
                residual = common
                for prime in (2, 3, 5, 7):
                    while residual % prime == 0:
                        residual //= prime
                with self.subTest(first=first, second=second):
                    self.assertEqual(overlap % residual, 0)

    def test_registered_profile_is_conservative(self) -> None:
        profile = compact_gap_overlap_profile(14, (14, 15, 16))
        self.assertEqual(profile.population_size, 7)
        self.assertEqual(profile.candidate_count, 3)
        self.assertEqual(profile.level_span, 2)
        self.assertLessEqual(
            profile.multi_hit_prime_count,
            profile.overlap_population_upper_bound,
        )
        self.assertEqual(
            profile.injective,
            profile.collision_pair_count == 0,
        )

    def test_pair_specific_bound_is_no_larger_than_span_bound(self) -> None:
        levels = (20, 22, 25, 27)
        exact_union_bound = compact_gap_overlap_population_upper_bound(
            24,
            levels,
        )
        span_bound = (
            math.comb(len(levels), 2)
            * compact_gap_overlap_bit_bound(levels[-1] - levels[0])
            // ((24 - 1) // 2)
        )
        self.assertLessEqual(exact_union_bound, span_bound)

    def test_invalid_inputs(self) -> None:
        invalid_calls = (
            lambda: compact_gap_exponent(True),
            lambda: compact_gap_overlap_integer(0),
            lambda: compact_gap_overlap_bit_bound(False),
            lambda: compact_gap_overlap_population_upper_bound(8, (2, 3)),
            lambda: compact_gap_overlap_population_upper_bound(12, (3, 2)),
            lambda: compact_gap_overlap_profile(12, (2, 2)),
        )
        for call in invalid_calls:
            with self.subTest(call=call), self.assertRaises(ValueError):
                call()


if __name__ == "__main__":
    unittest.main()
