"""Exact tests for the M30 compact support-signature theorem."""

from __future__ import annotations

import unittest
from itertools import combinations

from python.mosef_reference.compact_cofactor_prime_support import (
    phi4_prime_divisibility_profile,
)
from python.mosef_reference.compact_support_signatures import (
    materialized_support_signature,
    minimum_candidate_count,
    minimum_signature_collision_count,
    phi4_compact_signature,
    phi4_prefix_signature_profile,
    signature_pair_accounting,
)


class CompactSupportSignatureTests(unittest.TestCase):
    def test_pair_accounting_is_exact(self) -> None:
        signatures = (0, 1, 1, 3)
        profile = signature_pair_accounting(signatures, 2)
        direct_separated = sum(
            first != second for first, second in combinations(signatures, 2)
        )
        self.assertEqual(profile.separated_pair_count, direct_separated)
        self.assertEqual(profile.collision_pair_count, 1)
        self.assertEqual(profile.pair_count, 6)
        self.assertFalse(profile.injective)

    def test_injectivity_is_universal_pair_separation(self) -> None:
        injective = signature_pair_accounting((0, 1, 2, 3), 2)
        self.assertTrue(injective.injective)
        self.assertEqual(injective.separated_pair_count, injective.pair_count)
        collision = signature_pair_accounting((0, 1, 2, 2), 2)
        self.assertFalse(collision.injective)
        self.assertLess(collision.separated_pair_count, collision.pair_count)

    def test_information_and_coverage_lower_bounds(self) -> None:
        expected = (
            (2, 1, 2),
            (3, 2, 2),
            (4, 2, 3),
            (7, 3, 3),
            (8, 3, 4),
        )
        for population_size, ordinary, covered in expected:
            with self.subTest(population_size=population_size):
                self.assertEqual(
                    minimum_candidate_count(population_size),
                    ordinary,
                )
                self.assertEqual(
                    minimum_candidate_count(
                        population_size,
                        require_nonzero=True,
                    ),
                    covered,
                )

    def test_balanced_bucket_collision_lower_bound(self) -> None:
        self.assertEqual(minimum_signature_collision_count(5, 1), 4)
        self.assertEqual(minimum_signature_collision_count(6, 2), 2)
        self.assertEqual(minimum_signature_collision_count(5, 2), 1)
        self.assertEqual(minimum_signature_collision_count(4, 2), 0)
        self.assertEqual(
            minimum_signature_collision_count(
                4,
                2,
                require_nonzero=True,
            ),
            1,
        )

    def test_coverage_and_candidate_count_do_not_imply_separation(self) -> None:
        candidates = (15, 7)
        primes = (3, 5, 7)
        signatures = tuple(
            materialized_support_signature(candidates, prime)
            for prime in primes
        )
        self.assertEqual(signatures, (1, 1, 2))
        profile = signature_pair_accounting(signatures, 2)
        self.assertTrue(profile.covers_every_population_member)
        self.assertEqual(
            profile.candidate_count,
            profile.coverage_candidate_lower_bound,
        )
        self.assertFalse(profile.injective)
        self.assertEqual(profile.collision_pair_count, 1)

    def test_phi4_signatures_agree_with_each_coordinate(self) -> None:
        levels = tuple(range(2, 15))
        for prime in (2, 3, 5, 7, 11, 107, 109, 409, 1229):
            signature = phi4_compact_signature(levels, prime)
            for index, level in enumerate(levels):
                expected = phi4_prime_divisibility_profile(level, prime).divides
                self.assertEqual(bool(signature & (1 << index)), expected)

    def test_registered_prefix_obstructions(self) -> None:
        level_nine = phi4_prefix_signature_profile(9)
        self.assertEqual(level_nine.population_size, 2)
        self.assertEqual(level_nine.zero_signature_count, 2)
        self.assertEqual(level_nine.collision_pair_count, 1)
        self.assertFalse(level_nine.injective)

        level_fourteen = phi4_prefix_signature_profile(14)
        self.assertEqual(level_fourteen.population_size, 7)
        self.assertEqual(level_fourteen.zero_signature_count, 6)
        self.assertEqual(level_fourteen.covered_prime_count, 1)
        self.assertEqual(level_fourteen.collision_pair_count, 15)

    def test_invalid_inputs(self) -> None:
        for call in (
            lambda: minimum_candidate_count(1),
            lambda: minimum_signature_collision_count(2, -1),
            lambda: minimum_signature_collision_count(
                2,
                0,
                require_nonzero=True,
            ),
            lambda: signature_pair_accounting((0,), 1),
            lambda: signature_pair_accounting((0, 2), 1),
            lambda: materialized_support_signature((), 3),
            lambda: materialized_support_signature((0,), 3),
            lambda: phi4_compact_signature((), 3),
            lambda: phi4_compact_signature((1,), 3),
            lambda: phi4_compact_signature((2,), 9),
            lambda: phi4_prefix_signature_profile(3),
        ):
            with self.subTest(call=call), self.assertRaises(ValueError):
                call()


if __name__ == "__main__":
    unittest.main()
