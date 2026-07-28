"""Exact tests for the M31 diversified exceptional selector."""

from __future__ import annotations

import unittest

from python.mosef_reference.diversified_compact_signatures import (
    ExceptionalSelectorDescriptor,
    diversified_exceptional_selector,
    diversified_selector_profile,
    greedy_separating_column_indices,
    primitive_exit_mask,
)


class DiversifiedCompactSignatureTests(unittest.TestCase):
    def test_public_selector_is_deterministic_and_valid(self) -> None:
        descriptors = diversified_exceptional_selector(12)
        self.assertEqual(len(descriptors), 110)
        self.assertEqual(descriptors, diversified_exceptional_selector(12))
        self.assertEqual(
            descriptors[0],
            ExceptionalSelectorDescriptor("phi4", 3, 7, 2),
        )
        self.assertTrue(
            all(
                2 <= descriptor.first_factor <= 12
                and 2 <= descriptor.second_factor <= 12
                and 2 <= descriptor.base <= 12
                for descriptor in descriptors
            )
        )

    def test_widened_public_selector_is_nested_and_factor_independent(self) -> None:
        baseline = diversified_exceptional_selector(16)
        widened = diversified_exceptional_selector(16, 17)
        self.assertTrue(set(baseline).issubset(widened))
        self.assertGreater(len(widened), len(baseline))
        self.assertTrue(
            all(
                2 <= descriptor.first_factor <= 17
                and 2 <= descriptor.second_factor <= 17
                and 2 <= descriptor.base <= 17
                for descriptor in widened
            )
        )

    def test_primitive_exit_mask_has_stable_bit_order(self) -> None:
        descriptor = ExceptionalSelectorDescriptor("phi4", 3, 7, 2)
        self.assertEqual(primitive_exit_mask(descriptor, 107), 1 << 7)
        self.assertEqual(primitive_exit_mask(descriptor, 109), 0)
        self.assertEqual(
            primitive_exit_mask(
                ExceptionalSelectorDescriptor("phi4", 3, 7, 7),
                19,
            ),
            1 << 1,
        )
        self.assertEqual(
            primitive_exit_mask(
                ExceptionalSelectorDescriptor("phi4", 3, 7, 19),
                19,
            ),
            1,
        )

    def test_registered_finite_construction_boundary(self) -> None:
        level_nine = diversified_selector_profile(9)
        self.assertTrue(level_nine.injective)
        self.assertEqual(level_nine.collision_pair_count, 0)
        self.assertEqual(level_nine.minimum_separating_column_indices, (0,))

        level_fifteen = diversified_selector_profile(15)
        self.assertTrue(level_fifteen.injective)
        self.assertEqual(level_fifteen.population_primes[-1], 181)
        self.assertEqual(len(level_fifteen.normalized_columns), 12)
        self.assertEqual(
            len(level_fifteen.minimum_separating_column_indices or ()),
            10,
        )

        level_sixteen = diversified_selector_profile(16)
        self.assertFalse(level_sixteen.injective)
        self.assertEqual(level_sixteen.collision_pair_count, 3)
        self.assertEqual(level_sixteen.collision_buckets, ((191, 227, 233),))

    def test_normalization_removes_constants_and_duplicates(self) -> None:
        profile = diversified_selector_profile(14)
        self.assertEqual(profile.raw_coordinate_count, 1040)
        self.assertEqual(profile.constant_coordinate_count, 1014)
        self.assertEqual(profile.duplicate_coordinate_count, 19)
        self.assertEqual(len(profile.normalized_columns), 7)
        self.assertEqual(
            profile.constant_coordinate_count
            + profile.duplicate_coordinate_count
            + len(profile.normalized_columns),
            profile.raw_coordinate_count,
        )
        self.assertEqual(
            profile.separated_pair_count + profile.collision_pair_count,
            profile.pair_count,
        )

    def test_cofactor_novelty_is_pair_marginal_not_raw_hit_count(self) -> None:
        profile = diversified_selector_profile(16)
        self.assertEqual(profile.cofactor_novel_column_count, 3)
        self.assertEqual(profile.cofactor_novel_pair_count, 12)
        self.assertLessEqual(
            profile.cofactor_novel_pair_count,
            profile.separated_pair_count,
        )

    def test_greedy_certificate_handles_widened_cap(self) -> None:
        profile = diversified_selector_profile(
            16,
            19,
            compute_minimum_certificate=False,
        )
        indices = greedy_separating_column_indices(profile)
        self.assertIsNotNone(indices)
        signatures = tuple(
            sum(
                1 << output_index
                for output_index, column_index in enumerate(indices or ())
                if profile.normalized_columns[column_index].support_mask
                & (1 << prime_index)
            )
            for prime_index in range(len(profile.population_primes))
        )
        self.assertEqual(len(set(signatures)), len(signatures))
        self.assertIsNone(
            greedy_separating_column_indices(
                diversified_selector_profile(
                    16,
                    compute_minimum_certificate=False,
                )
            )
        )

    def test_m33_linear_caps_recur_and_cap_33_repairs(self) -> None:
        failed = diversified_selector_profile(
            21,
            32,
            compute_minimum_certificate=False,
        )
        repaired = diversified_selector_profile(
            21,
            33,
            compute_minimum_certificate=False,
        )
        self.assertEqual(
            failed.collision_buckets,
            ((1031, 1231, 1319, 1433),),
        )
        self.assertEqual(failed.collision_pair_count, 6)
        self.assertTrue(repaired.injective)
        self.assertEqual(repaired.collision_pair_count, 0)

    def test_m34_repaired_caps_recur_and_cap_39_repairs(self) -> None:
        failed = diversified_selector_profile(
            22,
            34,
            compute_minimum_certificate=False,
        )
        repaired = diversified_selector_profile(
            22,
            39,
            compute_minimum_certificate=False,
        )
        self.assertEqual(
            failed.collision_buckets,
            (
                (1481, 1511, 1571, 1663, 1721, 1747, 1867, 1931, 2029),
                (1907, 1999),
            ),
        )
        self.assertEqual(failed.collision_pair_count, 37)
        self.assertTrue(repaired.injective)
        self.assertEqual(repaired.collision_pair_count, 0)

    def test_m35_repaired_caps_recur_and_cap_47_repairs(self) -> None:
        failed = diversified_selector_profile(
            23,
            40,
            compute_minimum_certificate=False,
        )
        repaired = diversified_selector_profile(
            23,
            47,
            compute_minimum_certificate=False,
        )
        self.assertEqual(
            failed.collision_buckets,
            ((2411, 2477, 2741, 2777, 2837),),
        )
        self.assertEqual(failed.collision_pair_count, 10)
        self.assertTrue(repaired.injective)
        self.assertEqual(repaired.collision_pair_count, 0)

    def test_invalid_inputs(self) -> None:
        for call in (
            lambda: diversified_exceptional_selector(8),
            lambda: diversified_exceptional_selector(16, 15),
            lambda: diversified_exceptional_selector(16, True),
            lambda: diversified_selector_profile(True),
            lambda: diversified_selector_profile(
                16,
                compute_minimum_certificate=1,  # type: ignore[arg-type]
            ),
            lambda: primitive_exit_mask(
                ExceptionalSelectorDescriptor("phi4", 3, 7, 2),
                9,
            ),
            lambda: primitive_exit_mask(  # type: ignore[arg-type]
                ("phi4", 3, 7, 2),
                107,
            ),
            lambda: greedy_separating_column_indices(  # type: ignore[arg-type]
                ("not", "a", "profile")
            ),
        ):
            with self.subTest(call=call), self.assertRaises(ValueError):
                call()


if __name__ == "__main__":
    unittest.main()
