"""Exact tests for the M23 unequal signed reduction."""

from __future__ import annotations

import math
import unittest

from python.mosef_reference.unequal_signed_reduction import (
    evaluate_unequal_signed_reduction,
    unequal_difference_coefficients,
    unequal_difference_cofactor_coefficients,
)


def multiply(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    result = [0] * (len(left) + len(right) - 1)
    for left_index, left_value in enumerate(left):
        for right_index, right_value in enumerate(right):
            result[left_index + right_index] += left_value * right_value
    return tuple(result)


class UnequalSignedReductionTests(unittest.TestCase):
    def test_unit_prefix_rational_branch_can_expose_factor(self) -> None:
        value = evaluate_unequal_signed_reduction(3, 25, 3, 2, -1, 1)
        self.assertEqual(value.first_quotient_residue, 13)
        self.assertEqual(value.second_quotient_residue, 3)
        self.assertEqual(value.aggregate_residue, 15)
        self.assertEqual(value.aggregate_gcd, 5)
        self.assertEqual(value.first_quotient_status, "unit")
        self.assertEqual(value.rational_reduction_residue, 5)
        self.assertEqual(value.rational_reduction_gcd, 5)
        self.assertEqual(value.common_step, 1)
        self.assertEqual(value.common_factor_gcd, 1)
        self.assertEqual(value.difference_cofactor_residue, 5)

    def test_unequal_common_step_can_expose_factor(self) -> None:
        value = evaluate_unequal_signed_reduction(2, 9, 5, 7, -1, 1)
        self.assertEqual(value.common_step, 2)
        self.assertEqual(value.common_factor_residue, 6)
        self.assertEqual(value.common_factor_gcd, 3)
        self.assertEqual(value.difference_residue, 6)
        self.assertEqual(value.difference_gcd, 3)
        self.assertIsNone(value.difference_cofactor_residue)

    def test_proper_and_full_prefix_branches_are_total(self) -> None:
        proper = evaluate_unequal_signed_reduction(2, 15, 2, 3, 1, -1)
        self.assertEqual(proper.first_quotient_status, "proper_factor")
        self.assertEqual(proper.first_quotient_gcd, 3)
        self.assertIsNone(proper.rational_reduction_residue)

        full = evaluate_unequal_signed_reduction(2, 15, 4, 5, 1, 2)
        self.assertEqual(full.first_quotient_status, "full_collision")
        self.assertEqual(full.first_quotient_residue, 0)
        self.assertEqual(full.second_quotient_residue, 5)
        self.assertEqual(full.aggregate_residue, 10)
        self.assertEqual(full.aggregate_gcd, full.public_full_gcd)

    def test_exact_common_step_factorization(self) -> None:
        for first_factor in range(2, 11):
            for second_factor in range(2, 11):
                if first_factor == second_factor:
                    continue
                common_step = math.gcd(first_factor - 1, second_factor - 1)
                expected_factor = (0,) + (1,) * common_step
                cofactor = unequal_difference_cofactor_coefficients(
                    first_factor,
                    second_factor,
                )
                self.assertEqual(
                    multiply(expected_factor, cofactor),
                    unequal_difference_coefficients(first_factor, second_factor),
                )

    def test_smallest_trivial_common_step_has_no_endpoint_factor(self) -> None:
        self.assertEqual(
            unequal_difference_coefficients(2, 3),
            (0, -1, 1, 0, 1),
        )
        self.assertEqual(
            unequal_difference_cofactor_coefficients(2, 3),
            (-1, 1, 0, 1),
        )

    def test_boundary_factors_and_formal_counts(self) -> None:
        x_only = evaluate_unequal_signed_reduction(2, 35, 3, 5, -1, 1)
        self.assertTrue(x_only.has_x_factor)
        self.assertFalse(x_only.has_x_minus_one_factor)
        self.assertEqual(x_only.collected_monomial_count, 6)
        self.assertEqual(x_only.formal_degree, 12)

        one_only = evaluate_unequal_signed_reduction(2, 35, 2, 4, -2, 1)
        self.assertFalse(one_only.has_x_factor)
        self.assertTrue(one_only.has_x_minus_one_factor)
        self.assertEqual(one_only.collected_monomial_count, 5)

    def test_common_stage_divisor_is_public(self) -> None:
        for modulus in range(4, 80):
            for base in range(2, min(modulus, 12)):
                if math.gcd(base, modulus) != 1:
                    continue
                for first_factor in range(2, 7):
                    for second_factor in range(2, 7):
                        if first_factor == second_factor:
                            continue
                        value = evaluate_unequal_signed_reduction(
                            base,
                            modulus,
                            first_factor,
                            second_factor,
                            1,
                            -1,
                        )
                        self.assertEqual(
                            value.multiplier_gcd % value.common_stage_gcd,
                            0,
                        )

    def test_invalid_inputs_raise(self) -> None:
        invalid = (
            (2, 9, 1, 3, -1, 1),
            (2, 9, 3, 1, -1, 1),
            (2, 9, 3, 3, -1, 1),
            (3, 9, 3, 2, -1, 1),
            (2, 9, 3, 2, 0, 1),
            (2, 9, 3, 2, -1, 0),
        )
        for arguments in invalid:
            with self.assertRaises(ValueError):
                evaluate_unequal_signed_reduction(*arguments)


if __name__ == "__main__":
    unittest.main()
