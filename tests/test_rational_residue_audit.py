"""Exact tests for the M24 rational-residue audit."""

from __future__ import annotations

import math
import unittest

from python.mosef_reference.rational_residue_audit import (
    cleared_root_of_unity_coefficients,
    cyclotomic_coefficients,
    cyclotomic_factor_orders,
    evaluate_rational_residue_audit,
    polynomial_multiply,
    signed_numerator_coefficients,
)


class RationalResidueAuditTests(unittest.TestCase):
    def test_content_normalization_is_total(self) -> None:
        unit = evaluate_rational_residue_audit(2, 35, 3, 7, 2, 4)
        self.assertEqual(unit.content, 2)
        self.assertEqual(unit.content_status, "unit")
        self.assertEqual(unit.primitive_first_coefficient, 1)
        self.assertEqual(unit.primitive_second_coefficient, 2)
        self.assertEqual(unit.aggregate_gcd, unit.primitive_aggregate_gcd)

        proper = evaluate_rational_residue_audit(2, 55, 3, 7, 5, 10)
        self.assertEqual(proper.content_status, "proper_factor")
        self.assertEqual(proper.content_gcd, 5)

        full = evaluate_rational_residue_audit(2, 5, 3, 7, 5, 10)
        self.assertEqual(full.content_status, "full_collision")
        self.assertEqual(full.aggregate_gcd, 5)

    def test_phi4_is_an_exceptional_primitive_factor(self) -> None:
        self.assertEqual(
            cyclotomic_factor_orders(3, 7, 1, 1, 20),
            (4,),
        )
        value = evaluate_rational_residue_audit(2, 55, 3, 7, 1, 1)
        self.assertEqual(value.first_quotient_residue, 7)
        self.assertEqual(value.second_quotient_residue, 8)
        self.assertEqual(value.first_quotient_gcd, 1)
        self.assertEqual(value.second_quotient_gcd, 1)
        self.assertEqual(value.aggregate_residue, 15)
        self.assertEqual(value.aggregate_gcd, 5)
        self.assertEqual(value.rational_gcd, 5)
        self.assertEqual(value.content_status, "unit")
        self.assertGreater(value.first_public_bound_gcd, 0)
        self.assertEqual(value.first_public_bound_gcd, 1)
        self.assertEqual(value.second_public_bound_gcd, 1)

    def test_public_stage_overlap_bounds_hold(self) -> None:
        for modulus in range(4, 80):
            for base in range(2, min(modulus, 12)):
                if math.gcd(base, modulus) != 1:
                    continue
                for first_factor in range(2, 7):
                    for second_factor in range(2, 7):
                        if first_factor == second_factor:
                            continue
                        for coefficients in ((1, 1), (2, -3), (-4, 2)):
                            value = evaluate_rational_residue_audit(
                                base,
                                modulus,
                                first_factor,
                                second_factor,
                                *coefficients,
                            )
                            self.assertEqual(
                                value.first_public_bound_gcd
                                % value.first_overlap_gcd,
                                0,
                            )
                            self.assertEqual(
                                value.second_public_bound_gcd
                                % value.second_overlap_gcd,
                                0,
                            )

    def test_compact_resultant_descriptors(self) -> None:
        value = evaluate_rational_residue_audit(2, 55, 3, 7, -2, 3)
        self.assertEqual(value.first_resultant_base, 21)
        self.assertEqual(value.first_resultant_exponent, 2)
        self.assertEqual(value.second_resultant_coefficient_base, 2)
        self.assertEqual(value.second_resultant_coefficient_exponent, 18)
        self.assertEqual(value.second_resultant_stage_base, 7)
        self.assertEqual(value.second_resultant_stage_exponent, 2)

    def test_cleared_root_of_unity_identity(self) -> None:
        for first_factor in range(2, 8):
            for second_factor in range(2, 8):
                if first_factor == second_factor:
                    continue
                for first_coefficient, second_coefficient in (
                    (1, 1),
                    (-1, 1),
                    (2, -3),
                ):
                    numerator = signed_numerator_coefficients(
                        first_factor,
                        second_factor,
                        first_coefficient,
                        second_coefficient,
                    )
                    first_endpoint = (
                        (-1,)
                        + (0,) * (first_factor - 1)
                        + (1,)
                    )
                    expected = polynomial_multiply(
                        polynomial_multiply((-1, 1), first_endpoint),
                        numerator,
                    )
                    self.assertEqual(
                        cleared_root_of_unity_coefficients(
                            first_factor,
                            second_factor,
                            first_coefficient,
                            second_coefficient,
                        ),
                        expected,
                    )

    def test_known_cyclotomic_polynomials(self) -> None:
        self.assertEqual(cyclotomic_coefficients(1), (-1, 1))
        self.assertEqual(cyclotomic_coefficients(2), (1, 1))
        self.assertEqual(cyclotomic_coefficients(4), (1, 0, 1))
        self.assertEqual(cyclotomic_coefficients(6), (1, -1, 1))
        self.assertEqual(cyclotomic_coefficients(12), (1, 0, -1, 0, 1))

    def test_invalid_inputs_raise(self) -> None:
        for arguments in (
            (2, 9, 1, 3, 1, 1),
            (2, 9, 3, 1, 1, 1),
            (2, 9, 3, 3, 1, 1),
            (3, 9, 3, 2, 1, 1),
            (2, 9, 3, 2, 0, 1),
            (2, 9, 3, 2, 1, 0),
        ):
            with self.assertRaises(ValueError):
                evaluate_rational_residue_audit(*arguments)
        with self.assertRaises(ValueError):
            cyclotomic_coefficients(0)
        with self.assertRaises(ValueError):
            cyclotomic_coefficients(True)
        with self.assertRaises(ValueError):
            signed_numerator_coefficients(3, 7, True, 1)
        with self.assertRaises(ValueError):
            cyclotomic_factor_orders(3, 7, 1, 1, True)


if __name__ == "__main__":
    unittest.main()
