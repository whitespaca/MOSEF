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
from python.mosef_reference.exceptional_cofactor_schedule import (
    exceptional_cofactor_overlap,
)
from python.mosef_reference.exceptional_cyclotomic import (
    evaluate_exceptional_cyclotomic,
)


class DiversifiedCompactSignatureTests(unittest.TestCase):
    def test_direct_primitive_masks_match_full_audit_objects(self) -> None:
        primes = (2, 3, 5, 7, 11, 13, 17, 19, 107, 109, 211)
        for descriptor in diversified_exceptional_selector(20):
            overlap = exceptional_cofactor_overlap(
                descriptor.first_factor,
                descriptor.second_factor,
                descriptor.family,
            )
            for prime in primes:
                if descriptor.base % prime == 0:
                    expected = 1
                else:
                    evaluation = evaluate_exceptional_cyclotomic(
                        descriptor.base,
                        prime,
                        descriptor.first_factor,
                        descriptor.second_factor,
                        descriptor.family,
                    )
                    support = (
                        False,
                        evaluation.first_quotient_gcd == prime,
                        evaluation.second_quotient_gcd == prime,
                        evaluation.first_public_bound_gcd == prime,
                        evaluation.second_public_bound_gcd == prime,
                        evaluation.cyclotomic_gcd == prime,
                        (
                            overlap.cyclotomic_cofactor_resultant
                            % prime
                            == 0
                        ),
                        evaluation.cofactor_gcd == prime,
                    )
                    expected = sum(
                        1 << index
                        for index, hit in enumerate(support)
                        if hit
                    )
                self.assertEqual(
                    primitive_exit_mask(descriptor, prime),
                    expected,
                    (descriptor, prime),
                )

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

    def test_m36_distinct_caps_fail_and_cap_51_repairs(self) -> None:
        additive = diversified_selector_profile(
            24,
            48,
            compute_minimum_certificate=False,
        )
        multiplicative = diversified_selector_profile(
            24,
            49,
            compute_minimum_certificate=False,
        )
        repaired = diversified_selector_profile(
            24,
            51,
            compute_minimum_certificate=False,
        )
        self.assertEqual(
            additive.collision_buckets,
            ((3049, 3643, 3769, 3863, 4057),),
        )
        self.assertEqual(
            multiplicative.collision_buckets,
            ((3049, 3643, 3863, 4057),),
        )
        self.assertTrue(repaired.injective)
        self.assertEqual(repaired.collision_pair_count, 0)

    def test_m37_repaired_caps_fail_and_cap_65_repairs(self) -> None:
        additive = diversified_selector_profile(
            25,
            52,
            compute_minimum_certificate=False,
        )
        multiplicative = diversified_selector_profile(
            25,
            53,
            compute_minimum_certificate=False,
        )
        repaired = diversified_selector_profile(
            25,
            65,
            compute_minimum_certificate=False,
        )
        self.assertEqual(
            additive.collision_buckets,
            (
                (
                    4133,
                    4297,
                    4337,
                    4423,
                    4663,
                    5011,
                    5179,
                    5233,
                    5297,
                ),
            ),
        )
        self.assertEqual(
            multiplicative.collision_buckets,
            ((4297, 4337, 4423, 4663, 5011, 5179, 5233, 5297),),
        )
        self.assertTrue(repaired.injective)
        self.assertEqual(repaired.collision_pair_count, 0)

    def test_m38_repaired_caps_fail_and_two_new_columns_repair(self) -> None:
        additive = diversified_selector_profile(
            26,
            66,
            compute_minimum_certificate=False,
        )
        multiplicative = diversified_selector_profile(
            26,
            67,
            compute_minimum_certificate=False,
        )
        self.assertEqual(
            additive.collision_buckets,
            ((6229, 6703, 6793, 6947, 7187, 7229, 7649),),
        )
        self.assertEqual(
            multiplicative.collision_buckets,
            ((7187, 7229, 7649),),
        )

        primes = (7187, 7229, 7649)
        first = ExceptionalSelectorDescriptor("phi4", 7, 71, 65)
        second = ExceptionalSelectorDescriptor("phi4", 19, 71, 50)
        first_pattern = tuple(
            int(bool(primitive_exit_mask(first, prime) & (1 << 7)))
            for prime in primes
        )
        second_pattern = tuple(
            int(bool(primitive_exit_mask(second, prime) & (1 << 7)))
            for prime in primes
        )
        self.assertEqual(first_pattern, (0, 0, 1))
        self.assertEqual(second_pattern, (0, 1, 0))
        self.assertEqual(
            len(
                {
                    first_bit | (second_bit << 1)
                    for first_bit, second_bit in zip(
                        first_pattern,
                        second_pattern,
                        strict=True,
                    )
                }
            ),
            3,
        )

    def test_m39_cap_72_fails_and_five_new_columns_repair(self) -> None:
        additive = diversified_selector_profile(
            27,
            72,
            compute_minimum_certificate=False,
        )
        primes = (9463, 9791, 10607, 10939, 11087, 11213)
        self.assertEqual(additive.collision_buckets, (primes,))

        sources = (
            (ExceptionalSelectorDescriptor("phi4", 11, 15, 73), 2),
            (ExceptionalSelectorDescriptor("phi4", 15, 87, 83), 7),
            (ExceptionalSelectorDescriptor("phi4", 63, 75, 24), 7),
            (ExceptionalSelectorDescriptor("phi6", 35, 75, 46), 7),
            (ExceptionalSelectorDescriptor("phi6", 53, 81, 78), 7),
        )
        patterns = tuple(
            tuple(
                int(
                    bool(
                        primitive_exit_mask(descriptor, prime)
                        & (1 << kind_index)
                    )
                )
                for prime in primes
            )
            for descriptor, kind_index in sources
        )
        self.assertEqual(
            patterns,
            (
                (0, 1, 0, 0, 0, 0),
                (0, 0, 0, 1, 0, 0),
                (1, 0, 0, 0, 0, 0),
                (0, 0, 0, 0, 1, 0),
                (0, 0, 0, 0, 0, 1),
            ),
        )
        signatures = tuple(
            sum(
                pattern[prime_index] << source_index
                for source_index, pattern in enumerate(patterns)
            )
            for prime_index in range(len(primes))
        )
        self.assertEqual(signatures, (4, 1, 0, 2, 8, 16))

    def test_m40_caps_88_and_90_fail_and_five_new_columns_repair(self) -> None:
        additive = diversified_selector_profile(
            28,
            88,
            compute_minimum_certificate=False,
        )
        primes = (11867, 12791, 13633, 13967, 14051, 15559)
        self.assertEqual(additive.collision_buckets, (primes,))
        cap_88_keys = {
            descriptor.key
            for descriptor in diversified_exceptional_selector(28, 88)
        }
        for descriptor in diversified_exceptional_selector(28, 90):
            if descriptor.key in cap_88_keys:
                continue
            self.assertEqual(
                len(
                    {
                        primitive_exit_mask(descriptor, prime)
                        for prime in primes
                    }
                ),
                1,
                descriptor.key,
            )

        sources = (
            (ExceptionalSelectorDescriptor("phi4", 95, 35, 7), 7),
            (ExceptionalSelectorDescriptor("phi6", 59, 75, 92), 7),
            (ExceptionalSelectorDescriptor("phi4", 55, 27, 97), 7),
            (ExceptionalSelectorDescriptor("phi4", 31, 43, 91), 7),
            (ExceptionalSelectorDescriptor("phi4", 15, 99, 104), 7),
        )
        patterns = tuple(
            tuple(
                int(
                    bool(
                        primitive_exit_mask(descriptor, prime)
                        & (1 << kind_index)
                    )
                )
                for prime in primes
            )
            for descriptor, kind_index in sources
        )
        self.assertEqual(
            patterns,
            (
                (0, 0, 0, 0, 0, 1),
                (0, 0, 0, 0, 1, 0),
                (0, 0, 0, 1, 0, 0),
                (0, 0, 1, 0, 0, 0),
                (0, 1, 0, 0, 0, 0),
            ),
        )
        signatures = tuple(
            sum(
                pattern[prime_index] << source_index
                for source_index, pattern in enumerate(patterns)
            )
            for prime_index in range(len(primes))
        )
        self.assertEqual(signatures, (0, 16, 8, 4, 2, 1))

    def test_m41_cap_103_has_one_new_final_pair_coordinate(self) -> None:
        primes = (18979, 21031)
        cap_102 = diversified_exceptional_selector(29, 102)
        cap_103 = diversified_exceptional_selector(29, 103)
        self.assertEqual(len(cap_102), 89789)
        self.assertEqual(len(cap_103), 95778)
        self.assertEqual(
            len(diversified_exceptional_selector(29, 105)),
            99424,
        )
        self.assertEqual(
            len(diversified_exceptional_selector(29, 108)),
            109782,
        )
        for descriptor in cap_102:
            self.assertEqual(
                primitive_exit_mask(descriptor, primes[0]),
                primitive_exit_mask(descriptor, primes[1]),
                descriptor.key,
            )

        old_keys = {descriptor.key for descriptor in cap_102}
        distinguishing: list[tuple[str, int, tuple[int, int]]] = []
        for descriptor in cap_103:
            if descriptor.key in old_keys:
                continue
            masks = tuple(
                primitive_exit_mask(descriptor, prime) for prime in primes
            )
            for kind_index in range(8):
                pattern = tuple(
                    int(bool(mask & (1 << kind_index))) for mask in masks
                )
                if pattern[0] != pattern[1]:
                    distinguishing.append(
                        (descriptor.key, kind_index, pattern)
                    )
        self.assertEqual(
            distinguishing,
            [("phi4:87:95:103", 7, (0, 1))],
        )

    def test_m42_cap_123_has_two_new_final_triple_coordinates(self) -> None:
        primes = (28591, 29209, 29387)
        cap_122 = diversified_exceptional_selector(30, 122)
        cap_123 = diversified_exceptional_selector(30, 123)
        self.assertEqual(len(cap_122), 153670)
        self.assertEqual(len(cap_123), 164700)
        self.assertEqual(
            len(diversified_exceptional_selector(30, 106)),
            100380,
        )
        self.assertEqual(
            len(diversified_exceptional_selector(30, 112)),
            121878,
        )
        for descriptor in cap_122:
            masks = tuple(
                primitive_exit_mask(descriptor, prime) for prime in primes
            )
            self.assertEqual(len(set(masks)), 1, descriptor.key)

        old_keys = {descriptor.key for descriptor in cap_122}
        distinguishing: list[
            tuple[str, int, tuple[int, int, int]]
        ] = []
        for descriptor in cap_123:
            if descriptor.key in old_keys:
                continue
            masks = tuple(
                primitive_exit_mask(descriptor, prime) for prime in primes
            )
            for kind_index in range(8):
                pattern = tuple(
                    int(bool(mask & (1 << kind_index))) for mask in masks
                )
                if len(set(pattern)) > 1:
                    distinguishing.append(
                        (descriptor.key, kind_index, pattern)
                    )
        self.assertEqual(
            distinguishing,
            [
                ("phi4:79:123:54", 7, (1, 0, 0)),
                ("phi4:123:59:87", 7, (0, 0, 1)),
            ],
        )

    def test_m43_cap_144_has_one_new_final_pair_coordinate(self) -> None:
        primes = (37483, 44963)
        cap_143 = diversified_exceptional_selector(31, 143)
        cap_144 = diversified_exceptional_selector(31, 144)
        self.assertEqual(len(cap_143), 260712)
        self.assertEqual(len(cap_144), 262548)
        self.assertEqual(
            len(diversified_exceptional_selector(31, 124)),
            166050,
        )
        self.assertEqual(
            len(diversified_exceptional_selector(31, 127)),
            180558,
        )
        for descriptor in cap_143:
            masks = tuple(
                primitive_exit_mask(descriptor, prime) for prime in primes
            )
            self.assertEqual(len(set(masks)), 1, descriptor.key)

        old_keys = {descriptor.key for descriptor in cap_143}
        distinguishing: list[tuple[str, int, tuple[int, int]]] = []
        for descriptor in cap_144:
            if descriptor.key in old_keys:
                continue
            masks = tuple(
                primitive_exit_mask(descriptor, prime) for prime in primes
            )
            for kind_index in range(8):
                pattern = tuple(
                    int(bool(mask & (1 << kind_index))) for mask in masks
                )
                if len(set(pattern)) > 1:
                    distinguishing.append(
                        (descriptor.key, kind_index, pattern)
                    )
        self.assertEqual(
            distinguishing,
            [("phi6:11:105:144", 7, (1, 0))],
        )

    def test_m44_cap_167_has_one_new_final_pair_coordinate(self) -> None:
        primes = (59699, 63463)
        cap_166 = diversified_exceptional_selector(32, 166)
        cap_167 = diversified_exceptional_selector(32, 167)
        self.assertEqual(len(cap_166), 395340)
        self.assertEqual(len(cap_167), 415996)
        self.assertEqual(
            len(diversified_exceptional_selector(32, 145)),
            264384,
        )
        self.assertEqual(
            len(diversified_exceptional_selector(32, 148)),
            284004,
        )
        for descriptor in cap_166:
            masks = tuple(
                primitive_exit_mask(descriptor, prime) for prime in primes
            )
            self.assertEqual(len(set(masks)), 1, descriptor.key)

        old_keys = {descriptor.key for descriptor in cap_166}
        distinguishing: list[tuple[str, int, tuple[int, int]]] = []
        for descriptor in cap_167:
            if descriptor.key in old_keys:
                continue
            masks = tuple(
                primitive_exit_mask(descriptor, prime) for prime in primes
            )
            for kind_index in range(8):
                pattern = tuple(
                    int(bool(mask & (1 << kind_index))) for mask in masks
                )
                if len(set(pattern)) > 1:
                    distinguishing.append(
                        (descriptor.key, kind_index, pattern)
                    )
        self.assertEqual(
            distinguishing,
            [("phi4:167:119:93", 7, (1, 0))],
        )

    def test_m45_cap_195_has_one_new_final_pair_coordinate(self) -> None:
        primes = (80309, 92671)
        cap_194 = diversified_exceptional_selector(33, 194)
        cap_195 = diversified_exceptional_selector(33, 195)
        self.assertEqual(len(cap_194), 633040)
        self.assertEqual(len(cap_195), 661152)
        self.assertEqual(
            len(diversified_exceptional_selector(33, 168)),
            418502,
        )
        self.assertEqual(
            len(diversified_exceptional_selector(33, 172)),
            447678,
        )
        for descriptor in cap_194:
            masks = tuple(
                primitive_exit_mask(descriptor, prime) for prime in primes
            )
            self.assertEqual(len(set(masks)), 1, descriptor.key)

        old_keys = {descriptor.key for descriptor in cap_194}
        distinguishing: list[tuple[str, int, tuple[int, int]]] = []
        for descriptor in cap_195:
            if descriptor.key in old_keys:
                continue
            masks = tuple(
                primitive_exit_mask(descriptor, prime) for prime in primes
            )
            for kind_index in range(8):
                pattern = tuple(
                    int(bool(mask & (1 << kind_index))) for mask in masks
                )
                if len(set(pattern)) > 1:
                    distinguishing.append(
                        (descriptor.key, kind_index, pattern)
                    )
        self.assertEqual(
            distinguishing,
            [("phi4:195:91:20", 7, (1, 0))],
        )

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
