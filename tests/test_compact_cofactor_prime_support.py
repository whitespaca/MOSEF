"""Exact tests for the M29 compact cofactor prime-support barrier."""

from __future__ import annotations

import unittest
from math import gcd

from python.mosef_reference.compact_cofactor_prime_support import (
    phi4_balanced_support_profile,
    phi4_pair_outcome,
    phi4_prime_divisibility_profile,
)


def exact_phi4_cofactor(level: int) -> int:
    """Materialize only the small test levels."""
    second_factor = (1 << level) + 3
    return (8**second_factor + 48) // 35


class CompactCofactorPrimeSupportTests(unittest.TestCase):
    def test_exact_closed_form_and_consecutive_gcd(self) -> None:
        for level in range(2, 10):
            cofactor = exact_phi4_cofactor(level)
            exponent = 3 * (1 << level) + 5
            self.assertEqual(cofactor, 16 * ((1 << exponent) + 3) // 35)
            self.assertEqual(gcd(cofactor, exact_phi4_cofactor(level + 1)), 16)

    def test_small_prime_quotient_exceptions_are_exact(self) -> None:
        for level in range(2, 18):
            profiles = {
                prime: phi4_prime_divisibility_profile(level, prime)
                for prime in (2, 3, 5, 7)
            }
            self.assertTrue(profiles[2].divides)
            self.assertFalse(profiles[3].divides)
            self.assertEqual(profiles[5].divides, level % 4 == 2)
            self.assertEqual(profiles[7].divides, level % 3 == 2)

    def test_generic_congruence_finds_hits_and_misses(self) -> None:
        for level, prime, expected in (
            (2, 107, True),
            (4, 11, True),
            (9, 409, True),
            (12, 11, True),
            (2, 109, False),
            (9, 401, False),
        ):
            with self.subTest(level=level, prime=prime):
                profile = phi4_prime_divisibility_profile(level, prime)
                self.assertEqual(profile.divides, expected)
                self.assertEqual(
                    profile.divides,
                    profile.cofactor_residue == 0,
                )
                self.assertEqual(
                    profile.divides,
                    profile.criterion_residue == 0,
                )

    def test_pair_outcomes_are_the_signature_cut(self) -> None:
        proper = phi4_pair_outcome(2, 107, 109)
        self.assertEqual(proper.status, "proper_factor")
        self.assertEqual(proper.factor, 107)
        collision = phi4_pair_outcome(2, 5, 107)
        self.assertEqual(collision.status, "full_collision")
        self.assertIsNone(collision.factor)
        unit = phi4_pair_outcome(2, 109, 113)
        self.assertEqual(unit.status, "unit")
        self.assertIsNone(unit.factor)

    def test_balanced_population_accounting(self) -> None:
        for input_length in range(9, 21):
            profile = phi4_balanced_support_profile(input_length)
            self.assertEqual(
                profile.pair_count,
                profile.proper_pair_count
                + profile.full_collision_pair_count
                + profile.unit_pair_count,
            )
            self.assertLessEqual(
                profile.proper_pair_count,
                profile.maximum_proper_pair_count,
            )
            if profile.population_size >= 3:
                self.assertFalse(profile.universal_pair_coverage_possible)

    def test_invalid_inputs(self) -> None:
        for call in (
            lambda: phi4_prime_divisibility_profile(1, 11),
            lambda: phi4_prime_divisibility_profile(2, 9),
            lambda: phi4_pair_outcome(2, 107, 107),
            lambda: phi4_balanced_support_profile(3),
        ):
            with self.subTest(call=call), self.assertRaises(ValueError):
                call()


if __name__ == "__main__":
    unittest.main()
