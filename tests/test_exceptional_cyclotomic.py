"""Exact tests for the M26 exceptional cyclotomic extraction grammar."""

from __future__ import annotations

import unittest

from python.mosef_reference.exceptional_cyclotomic import (
    compact_exceptional_cofactor_residue,
    evaluate_exceptional_cyclotomic,
    exceptional_cofactor_coefficients,
    exceptional_cyclotomic_coefficients,
)
from python.mosef_reference.rational_residue_audit import (
    polynomial_multiply,
    signed_numerator_coefficients,
)


class ExceptionalCyclotomicTests(unittest.TestCase):
    def test_exact_dense_divisions(self) -> None:
        cases = (
            (3, 7, "phi4", 1),
            (7, 3, "phi4", 1),
            (11, 15, "phi4", 1),
            (5, 3, "phi6", 2),
            (11, 9, "phi6", 2),
        )
        for first_factor, second_factor, family, first_coefficient in cases:
            cyclotomic = exceptional_cyclotomic_coefficients(
                first_factor, second_factor, family
            )
            cofactor = exceptional_cofactor_coefficients(
                first_factor, second_factor, family
            )
            numerator = signed_numerator_coefficients(
                first_factor,
                second_factor,
                first_coefficient,
                1,
            )
            self.assertEqual(
                polynomial_multiply(cyclotomic, cofactor),
                numerator,
            )
            self.assertEqual(
                len(cofactor),
                first_factor * (second_factor - 1) - 1,
            )
            for modulus in range(2, 48):
                for base in range(modulus):
                    dense = 0
                    for coefficient in reversed(cofactor):
                        dense = (dense * base + coefficient) % modulus
                    self.assertEqual(
                        compact_exceptional_cofactor_residue(
                            base,
                            modulus,
                            first_factor,
                            second_factor,
                            family,
                        ),
                        dense,
                    )

    def test_direct_cyclotomic_and_full_collision_branches(self) -> None:
        proper = evaluate_exceptional_cyclotomic(2, 55, 3, 7, "phi4")
        self.assertEqual(proper.cyclotomic_status, "proper_factor")
        self.assertEqual(proper.extraction_source, "cyclotomic")
        self.assertEqual(proper.extraction_gcd, 5)
        self.assertIsNotNone(proper.cofactor_residue)

        full = evaluate_exceptional_cyclotomic(2, 5, 3, 7, "phi4")
        self.assertEqual(full.cyclotomic_status, "full_collision")
        self.assertEqual(full.aggregate_status, "full_collision")
        self.assertEqual(full.extraction_source, "full_collision")

    def test_unit_phi4_cofactor_extracts_square_free_and_repeated(self) -> None:
        for arguments, expected in (
            ((11, 15, 3, 7, "phi4"), 5),
            ((4, 9, 11, 7, "phi4"), 3),
        ):
            value = evaluate_exceptional_cyclotomic(*arguments)
            self.assertEqual(value.cyclotomic_status, "unit")
            self.assertEqual(value.extraction_source, "cofactor")
            self.assertEqual(value.extraction_gcd, expected)
            self.assertEqual(value.aggregate_gcd, expected)
            self.assertEqual(value.first_quotient_gcd, 1)
            self.assertEqual(value.second_quotient_gcd, 1)
            self.assertEqual(value.first_public_bound_gcd, 1)
            self.assertEqual(value.second_public_bound_gcd, 1)

    def test_unit_phi6_cofactor_extracts_square_free_and_repeated(self) -> None:
        for arguments, expected in (
            ((8, 35, 5, 3, "phi6"), 5),
            ((3, 25, 5, 3, "phi6"), 5),
        ):
            value = evaluate_exceptional_cyclotomic(*arguments)
            self.assertEqual(value.cyclotomic_status, "unit")
            self.assertEqual(value.extraction_source, "cofactor")
            self.assertEqual(value.extraction_gcd, expected)
            self.assertEqual(value.aggregate_gcd, expected)

    def test_invalid_domains_raise(self) -> None:
        for arguments in (
            (2, 15, 5, 7, "phi4"),
            (2, 15, 3, 5, "phi4"),
            (2, 35, 7, 3, "phi6"),
            (2, 35, 5, 5, "phi6"),
            (5, 15, 3, 7, "phi4"),
            (2, 15, 3, 7, "phi8"),
        ):
            with self.assertRaises(ValueError):
                evaluate_exceptional_cyclotomic(*arguments)


if __name__ == "__main__":
    unittest.main()
