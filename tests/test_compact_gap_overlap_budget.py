"""Exact tests for the M48 compact-gap overlap budget."""

from __future__ import annotations

import math
import unittest

from python.mosef_reference.compact_gap_overlap_budget import (
    compact_gap_balanced_overlap_order,
    compact_gap_boundary_ledger,
    compact_gap_boundary_overlap_order,
    compact_gap_common_support_gap,
    compact_gap_common_support_integer,
    compact_gap_distinct_gap_ledger,
    compact_gap_exponent,
    compact_gap_high_weight_population_upper_bound,
    compact_gap_high_weight_profile,
    compact_gap_low_weight_signature_capacity,
    compact_gap_maximal_gap_witness,
    compact_gap_overlap_bit_bound,
    compact_gap_overlap_integer,
    compact_gap_overlap_population_upper_bound,
    compact_gap_overlap_prefix_bit_bound,
    compact_gap_overlap_profile,
    compact_gap_realizable_common_gaps,
    compact_gap_variable_order_profile,
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

    def test_common_support_gcd_collapses_many_levels(self) -> None:
        self.assertEqual(compact_gap_common_support_gap((4, 8, 12, 16)), 4)
        self.assertEqual(
            compact_gap_common_support_integer((4, 8, 12, 16)),
            compact_gap_overlap_integer(4),
        )
        for prime, levels in (
            (11, (4, 8, 12, 16)),
            (179, (6, 17, 28)),
            (409, (9, 17, 25)),
        ):
            with self.subTest(prime=prime, levels=levels):
                self.assertTrue(all(_compact_cofactor(level) % prime == 0 for level in levels))
                self.assertEqual(
                    compact_gap_common_support_integer(levels) % prime,
                    0,
                )

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

    def test_high_weight_capacity_and_profile(self) -> None:
        self.assertEqual(
            compact_gap_low_weight_signature_capacity(5, 3),
            1 + 5 + math.comb(5, 2),
        )
        levels = tuple(range(20, 41))
        profile = compact_gap_high_weight_profile(20, levels, 4)
        self.assertLessEqual(
            profile.high_weight_prime_count,
            profile.high_weight_population_upper_bound,
        )
        self.assertEqual(
            profile.injective,
            profile.collision_pair_count == 0,
        )
        self.assertEqual(
            compact_gap_high_weight_population_upper_bound(20, (2, 3), 3),
            0,
        )

    def test_balanced_variable_overlap_order(self) -> None:
        self.assertEqual(compact_gap_balanced_overlap_order(21, 89), 5)
        self.assertEqual(compact_gap_balanced_overlap_order(1, 0), 1)
        for candidate_count, level_span in ((21, 89), (41, 252), (41, 636)):
            with self.subTest(
                candidate_count=candidate_count,
                level_span=level_span,
            ):
                order = compact_gap_balanced_overlap_order(
                    candidate_count,
                    level_span,
                )
                logarithmic_scale = candidate_count.bit_length()
                self.assertGreaterEqual(
                    order * order * logarithmic_scale,
                    level_span,
                )
                if order > 1:
                    self.assertLess(
                        (order - 1) ** 2 * logarithmic_scale,
                        level_span,
                    )

    def test_variable_order_profile_is_conservative(self) -> None:
        levels = tuple(
            20 + (index * 89) // 20
            for index in range(21)
        )
        profile = compact_gap_variable_order_profile(20, levels)
        self.assertEqual(profile.high_weight_threshold, 6)
        self.assertLessEqual(
            profile.high_weight_prime_count,
            profile.high_weight_population_upper_bound,
        )
        self.assertFalse(profile.injective)

    def test_boundary_order_and_exact_ledger(self) -> None:
        order = compact_gap_boundary_overlap_order(1024, 819, 1, 4)
        self.assertEqual(order, 26)
        ledger = compact_gap_boundary_ledger(1024, 819, 3276, order)
        self.assertEqual(ledger.high_weight_threshold, 27)
        self.assertEqual(ledger.maximum_common_gap, 126)
        self.assertGreater(
            ledger.conservative_population_lower_bound,
            0,
        )
        self.assertEqual(
            ledger.theorem_forces_collision,
            ledger.conservative_population_lower_bound
            - ledger.high_weight_population_upper_bound
            > ledger.low_weight_signature_capacity,
        )

    def test_boundary_ledger_switches_to_full_signature_space(self) -> None:
        ledger = compact_gap_boundary_ledger(20, 3, 9, 3)
        self.assertEqual(ledger.high_weight_population_upper_bound, 0)
        self.assertEqual(ledger.low_weight_signature_capacity, 8)
        self.assertEqual(ledger.maximum_common_gap, 0)

    def test_distinct_gap_prefix_and_ledger_remove_subset_overcount(self) -> None:
        self.assertEqual(compact_gap_overlap_prefix_bit_bound(0), 0)
        self.assertEqual(
            compact_gap_overlap_prefix_bit_bound(2),
            compact_gap_overlap_bit_bound(1)
            + compact_gap_overlap_bit_bound(2),
        )
        boundary = compact_gap_boundary_ledger(1024, 819, 3276, 52)
        distinct = compact_gap_distinct_gap_ledger(1024, 819, 3276, 52)
        self.assertEqual(distinct.maximum_common_gap, 63)
        self.assertEqual(distinct.distinct_gap_count, 63)
        self.assertLess(
            distinct.high_weight_population_upper_bound,
            boundary.high_weight_population_upper_bound,
        )

    def test_realizable_gap_bound_is_attained_by_arithmetic_progressions(
        self,
    ) -> None:
        witness = compact_gap_maximal_gap_witness(4, 7, initial_level=3)
        self.assertEqual(witness, (3, 10, 17, 24, 31))
        self.assertEqual(
            compact_gap_realizable_common_gaps(witness, 4),
            (7,),
        )
        self.assertEqual((witness[-1] - witness[0]) // 4, 7)
        self.assertEqual(
            compact_gap_realizable_common_gaps((2, 4, 6, 9, 12), 2),
            (1, 2, 3),
        )

    def test_invalid_inputs(self) -> None:
        invalid_calls = (
            lambda: compact_gap_exponent(True),
            lambda: compact_gap_overlap_integer(0),
            lambda: compact_gap_overlap_bit_bound(False),
            lambda: compact_gap_overlap_population_upper_bound(8, (2, 3)),
            lambda: compact_gap_overlap_population_upper_bound(12, (3, 2)),
            lambda: compact_gap_overlap_profile(12, (2, 2)),
            lambda: compact_gap_common_support_gap((2,)),
            lambda: compact_gap_low_weight_signature_capacity(0, 3),
            lambda: compact_gap_high_weight_population_upper_bound(
                12,
                (2, 3),
                1,
            ),
            lambda: compact_gap_high_weight_profile(12, (2, 3), False),
            lambda: compact_gap_balanced_overlap_order(2, 0),
            lambda: compact_gap_balanced_overlap_order(False, 1),
            lambda: compact_gap_boundary_overlap_order(12, 3, 0, 1),
            lambda: compact_gap_boundary_ledger(12, 4, 2, 1),
            lambda: compact_gap_boundary_ledger(12, 4, 8, 5),
            lambda: compact_gap_overlap_prefix_bit_bound(False),
            lambda: compact_gap_realizable_common_gaps((2, 3), 2),
            lambda: compact_gap_maximal_gap_witness(0, 1),
            lambda: compact_gap_maximal_gap_witness(1, False),
        )
        for call in invalid_calls:
            with self.subTest(call=call), self.assertRaises(ValueError):
                call()


if __name__ == "__main__":
    unittest.main()
