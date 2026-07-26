"""Exact tests for the M17 dyadic rational/compositional circuit."""

from __future__ import annotations

import math
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

from mosef_reference import (  # noqa: E402
    dyadic_geometric_coefficients,
    evaluate_dyadic_telescope,
)
from scripts.run_m17_dyadic_telescope_search import search  # noqa: E402


def multiply_polynomials(
    left: tuple[int, ...],
    right: tuple[int, ...],
) -> tuple[int, ...]:
    """Multiply two small integer coefficient vectors."""
    result = [0] * (len(left) + len(right) - 1)
    for left_index, left_value in enumerate(left):
        for right_index, right_value in enumerate(right):
            result[left_index + right_index] += left_value * right_value
    return tuple(result)


class DyadicTelescopeTests(unittest.TestCase):
    def test_symbolic_identity_has_exponentially_many_monomials(self) -> None:
        for levels in range(9):
            product = (1,)
            for index in range(levels):
                factor = [0] * ((1 << index) + 1)
                factor[0] = 1
                factor[-1] = 1
                product = multiply_polynomials(product, tuple(factor))
            self.assertEqual(product, dyadic_geometric_coefficients(levels))

    def test_unit_denominator_division_matches_product_path(self) -> None:
        evaluation = evaluate_dyadic_telescope(2, 35, 3)
        self.assertEqual(evaluation.division_status, "unit")
        self.assertEqual(
            evaluation.division_quotient,
            evaluation.quotient_residue,
        )
        self.assertEqual(
            evaluation.numerator_residue,
            evaluation.denominator_residue
            * evaluation.quotient_residue
            % evaluation.modulus,
        )
        self.assertEqual(evaluation.formal_degree, 7)
        self.assertEqual(evaluation.formal_monomial_count, 8)

    def test_proper_denominator_is_an_extracted_factor(self) -> None:
        evaluation = evaluate_dyadic_telescope(4, 15, 1)
        self.assertEqual(evaluation.division_status, "proper_factor")
        self.assertEqual(evaluation.denominator_gcd, 3)
        self.assertIsNone(evaluation.division_quotient)
        self.assertEqual(evaluation.factor_gcds, (5,))
        self.assertEqual(evaluation.numerator_gcd, 15)

    def test_full_denominator_still_has_total_product_semantics(self) -> None:
        evaluation = evaluate_dyadic_telescope(1, 6, 3)
        self.assertEqual(evaluation.division_status, "full_collision")
        self.assertIsNone(evaluation.division_quotient)
        self.assertEqual(evaluation.denominator_gcd, 6)
        self.assertEqual(evaluation.quotient_residue, 2)
        self.assertEqual(evaluation.quotient_gcd, 2)
        self.assertTrue(any(1 < value < 6 for value in evaluation.factor_gcds))

    def test_proper_aggregate_success_has_a_proper_explicit_component(self) -> None:
        for modulus in range(4, 100):
            for base in range(modulus):
                if math.gcd(base, modulus) != 1:
                    continue
                for levels in range(8):
                    evaluation = evaluate_dyadic_telescope(base, modulus, levels)
                    proper_components = (
                        1 < evaluation.denominator_gcd < modulus
                        or any(
                            1 < divisor < modulus
                            for divisor in evaluation.factor_gcds
                        )
                    )
                    if 1 < evaluation.quotient_gcd < modulus:
                        self.assertTrue(
                            any(
                                1 < divisor < modulus
                                for divisor in evaluation.factor_gcds
                            )
                        )
                    if 1 < evaluation.numerator_gcd < modulus:
                        self.assertTrue(proper_components)

    def test_aggregate_can_change_the_proper_factor_value(self) -> None:
        evaluation = evaluate_dyadic_telescope(1, 8, 2)
        self.assertEqual(evaluation.factor_gcds, (2, 2))
        self.assertEqual(evaluation.quotient_gcd, 4)

    def test_operation_counts_are_linear_in_levels(self) -> None:
        for levels in range(20):
            evaluation = evaluate_dyadic_telescope(2, 101, levels)
            self.assertEqual(evaluation.squaring_count, levels)
            self.assertEqual(
                evaluation.product_multiplication_count,
                max(0, levels - 1),
            )
            self.assertEqual(len(evaluation.factor_residues), levels)

    def test_invalid_domains_raise(self) -> None:
        invalid_calls = (
            lambda: evaluate_dyadic_telescope(True, 5, 1),
            lambda: evaluate_dyadic_telescope(2, 1, 1),
            lambda: evaluate_dyadic_telescope(5, 35, 1),
            lambda: evaluate_dyadic_telescope(2, 5, -1),
            lambda: evaluate_dyadic_telescope(2, 5, True),
            lambda: dyadic_geometric_coefficients(-1),
            lambda: dyadic_geometric_coefficients(True),
            lambda: dyadic_geometric_coefficients(21),
        )
        for invalid_call in invalid_calls:
            with self.subTest(invalid_call=invalid_call):
                with self.assertRaises(ValueError):
                    invalid_call()

    def test_registered_search_smoke(self) -> None:
        result = search(6, 64, 12)
        self.assertGreater(result["symbolic"]["coefficient_checks"], 0)
        self.assertGreater(result["modular"]["circuit_checks"], 0)
        self.assertGreater(result["modular"]["proper_denominator_exits"], 0)
        self.assertEqual(result["modular"]["unexplained_proper_successes"], 0)
        self.assertEqual(len(result["summary_sha256"]), 64)


if __name__ == "__main__":
    unittest.main()
