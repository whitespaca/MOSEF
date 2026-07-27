"""Exact tests for the M19 cancellation-obscured nested quotient."""

from __future__ import annotations

import math
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

from mosef_reference import evaluate_nested_quotient


class NestedQuotientTests(unittest.TestCase):
    def test_bounded_exact_identity_and_trichotomy(self) -> None:
        for modulus in range(4, 50):
            for base in range(modulus):
                if math.gcd(base, modulus) != 1:
                    continue
                for inner_exponent in range(1, 9):
                    for multiplier in range(1, 9):
                        value = evaluate_nested_quotient(
                            base,
                            modulus,
                            inner_exponent,
                            multiplier,
                        )
                        self.assertEqual(
                            value.rational_numerator_residue,
                            value.intermediate_residue
                            * value.quotient_residue
                            % modulus,
                        )
                        if value.rational_division_status == "unit":
                            self.assertEqual(
                                value.rational_division_quotient,
                                value.quotient_residue,
                            )
                            self.assertEqual(
                                value.rational_numerator_gcd,
                                value.quotient_gcd,
                            )
                        elif value.rational_division_status == "proper_factor":
                            self.assertTrue(1 < value.intermediate_gcd < modulus)
                        else:
                            self.assertEqual(value.intermediate_gcd, modulus)
                            self.assertEqual(
                                value.quotient_residue,
                                multiplier % modulus,
                            )
                            self.assertEqual(
                                value.quotient_gcd,
                                value.multiplier_gcd,
                            )

    def test_unit_intermediate_reduces_to_rational_numerator(self) -> None:
        value = evaluate_nested_quotient(2, 15, 1, 2)
        self.assertEqual(value.rational_division_status, "unit")
        self.assertEqual(value.intermediate_gcd, 1)
        self.assertEqual(value.quotient_gcd, value.rational_numerator_gcd)

    def test_proper_intermediate_can_expose_different_factor(self) -> None:
        value = evaluate_nested_quotient(2, 15, 2, 2)
        self.assertEqual(value.intermediate_gcd, 3)
        self.assertEqual(value.quotient_gcd, 5)
        self.assertEqual(value.rational_numerator_gcd, 15)

    def test_full_intermediate_reduces_to_public_multiplier(self) -> None:
        value = evaluate_nested_quotient(2, 15, 4, 5)
        self.assertEqual(value.intermediate_gcd, 15)
        self.assertEqual(value.inner_power_residue, 1)
        self.assertEqual(value.quotient_gcd, 5)
        self.assertEqual(value.quotient_gcd, value.multiplier_gcd)

    def test_composed_division_has_total_semantics(self) -> None:
        for arguments in ((2, 15, 1, 2), (2, 15, 2, 2), (2, 15, 4, 5)):
            value = evaluate_nested_quotient(*arguments)
            if value.composed_division_status == "unit":
                self.assertEqual(
                    value.composed_division_quotient,
                    value.quotient_residue,
                )
                self.assertEqual(value.endpoint_gcd, value.quotient_gcd)
            elif value.composed_division_status == "proper_factor":
                self.assertTrue(
                    1 < value.composed_denominator_gcd < value.modulus
                )
            else:
                self.assertEqual(value.composed_denominator_gcd, value.modulus)
                self.assertEqual(value.quotient_gcd, value.multiplier_gcd)

    def test_multiplier_one_and_invalid_inputs(self) -> None:
        value = evaluate_nested_quotient(2, 35, 7, 1)
        self.assertEqual(value.quotient_residue, 1)
        self.assertEqual(value.formal_quotient_degree, 0)
        self.assertEqual(value.formal_quotient_monomial_count, 1)
        for arguments in ((5, 15, 2, 2), (2, 15, 0, 2), (2, 15, 2, 0)):
            with self.assertRaises(ValueError):
                evaluate_nested_quotient(*arguments)


if __name__ == "__main__":
    unittest.main()
