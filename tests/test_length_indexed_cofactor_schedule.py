"""Exact tests for the M28 length-indexed materialized-support barrier."""

from __future__ import annotations

import unittest
from math import gcd

from python.mosef_reference.exceptional_cyclotomic import (
    compact_exceptional_cofactor_residue,
)
from python.mosef_reference.length_indexed_cofactor_schedule import (
    balanced_prime_population,
    length_indexed_support_profile,
    phi4_compact_gap_profile,
)


def exact_phi4_gap_cofactor(level: int) -> int:
    """Materialize the bounded M28 gap witness for independent checking."""
    second_factor = (1 << level) + 3
    first_stage = 7
    second_stage = (8**second_factor - 1) // 7
    aggregate = first_stage + second_stage
    if aggregate % 5 != 0:
        raise AssertionError("exceptional phi4 identity was not integral")
    return aggregate // 5


class LengthIndexedCofactorScheduleTests(unittest.TestCase):
    def test_balanced_populations_have_the_declared_pair_length(self) -> None:
        self.assertEqual(balanced_prime_population(10), (23, 29, 31))
        self.assertEqual(balanced_prime_population(12), (47, 53, 59, 61))
        for input_length in range(9, 18):
            population = balanced_prime_population(input_length)
            for index, first_prime in enumerate(population):
                for second_prime in population[index + 1 :]:
                    self.assertEqual(
                        (first_prime * second_prime).bit_length(),
                        input_length,
                    )

    def test_support_profile_counts_forced_misses(self) -> None:
        profile = length_indexed_support_profile(
            12,
            (47, 53, 59, 61),
            (47 * 53, -5),
        )
        self.assertEqual(profile.hit_primes, (47, 53))
        self.assertEqual(profile.missed_primes, (59, 61))
        self.assertEqual(profile.hit_prime_count, 2)
        self.assertEqual(profile.forced_miss_pair_count, 1)
        self.assertEqual(profile.pair_count, 6)
        self.assertEqual(profile.maximum_coverable_pair_count, 5)
        self.assertLessEqual(profile.hit_prime_count, profile.support_cap)
        for value in (47 * 53, -5):
            self.assertEqual(gcd(value, 59 * 61), 1)

    def test_universal_support_requires_all_but_one_prime(self) -> None:
        primes = (67, 71, 73, 79, 83, 89)
        profile = length_indexed_support_profile(
            13,
            primes,
            (67 * 71, 73 * 79, 83),
        )
        self.assertEqual(profile.hit_prime_count, 5)
        self.assertEqual(profile.forced_miss_pair_count, 0)
        self.assertGreaterEqual(
            profile.materialized_bit_budget,
            profile.necessary_universal_bit_budget,
        )

    def test_phi4_gap_certificate_matches_exact_bounded_lifts(self) -> None:
        for level in range(2, 11):
            profile = phi4_compact_gap_profile(level)
            cofactor = exact_phi4_gap_cofactor(level)
            self.assertEqual(profile.second_factor, (1 << level) + 3)
            self.assertEqual(
                cofactor % 101,
                compact_exceptional_cofactor_residue(
                    2,
                    101,
                    3,
                    profile.second_factor,
                    "phi4",
                ),
            )
            self.assertGreaterEqual(
                cofactor.bit_length(),
                profile.cofactor_bit_length_lower_bound,
            )
            self.assertEqual(
                profile.cofactor_degree,
                3 * (profile.second_factor - 1) - 2,
            )

    def test_invalid_inputs(self) -> None:
        for call in (
            lambda: balanced_prime_population(3),
            lambda: length_indexed_support_profile(10, (23,), (23,)),
            lambda: length_indexed_support_profile(10, (23, 23), (23,)),
            lambda: length_indexed_support_profile(10, (23, 29), (0,)),
            lambda: length_indexed_support_profile(11, (23, 29), (23,)),
            lambda: phi4_compact_gap_profile(1),
        ):
            with self.subTest(call=call), self.assertRaises(ValueError):
                call()


if __name__ == "__main__":
    unittest.main()
