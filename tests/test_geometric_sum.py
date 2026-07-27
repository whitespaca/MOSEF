"""Exact tests for the M18 arbitrary-exponent binary geometric-sum circuit."""

from __future__ import annotations

import math
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

from mosef_reference import (
    evaluate_geometric_sum,
    geometric_sum_coefficients,
)


def add_polynomials(
    left: tuple[int, ...],
    right: tuple[int, ...],
) -> tuple[int, ...]:
    """Add two small coefficient vectors."""
    result = [0] * max(len(left), len(right))
    for index, value in enumerate(left):
        result[index] += value
    for index, value in enumerate(right):
        result[index] += value
    return tuple(result)


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


def shift_polynomial(values: tuple[int, ...], amount: int) -> tuple[int, ...]:
    return (0,) * amount + values


def binary_geometric_coefficients(exponent: int) -> tuple[int, ...]:
    """Construct S_M from the exact even/odd binary identities."""
    if exponent == 1:
        return (1,)
    half = exponent // 2
    lower = binary_geometric_coefficients(half)
    doubled = multiply_polynomials(
        lower,
        (1,) + (0,) * (half - 1) + (1,),
    )
    if exponent % 2 == 0:
        return doubled
    return add_polynomials(doubled, shift_polynomial((1,), 2 * half))


class GeometricSumTests(unittest.TestCase):
    def test_symbolic_binary_identities(self) -> None:
        for exponent in range(1, 65):
            self.assertEqual(
                binary_geometric_coefficients(exponent),
                geometric_sum_coefficients(exponent),
            )

    def test_binary_evaluator_matches_direct_sum(self) -> None:
        for modulus in range(4, 50):
            for base in range(modulus):
                if math.gcd(base, modulus) != 1:
                    continue
                for exponent in range(1, 33):
                    evaluation = evaluate_geometric_sum(base, modulus, exponent)
                    direct = sum(pow(base, index, modulus) for index in range(exponent))
                    self.assertEqual(evaluation.sum_residue, direct % modulus)
                    self.assertEqual(
                        evaluation.power_residue,
                        pow(base, exponent, modulus),
                    )
                    self.assertEqual(
                        evaluation.numerator_residue,
                        evaluation.denominator_residue
                        * evaluation.sum_residue
                        % modulus,
                    )

    def test_unit_denominator_reduces_to_endpoint_gcd(self) -> None:
        evaluation = evaluate_geometric_sum(2, 15, 2)
        self.assertEqual(evaluation.division_status, "unit")
        self.assertEqual(evaluation.division_quotient, evaluation.sum_residue)
        self.assertEqual(evaluation.sum_gcd, 3)
        self.assertEqual(evaluation.sum_gcd, evaluation.numerator_gcd)

    def test_proper_denominator_is_already_a_factor(self) -> None:
        evaluation = evaluate_geometric_sum(4, 15, 2)
        self.assertEqual(evaluation.division_status, "proper_factor")
        self.assertEqual(evaluation.denominator_gcd, 3)
        self.assertEqual(evaluation.sum_gcd, 5)
        self.assertEqual(evaluation.numerator_gcd, 15)
        self.assertIsNone(evaluation.division_quotient)

    def test_full_denominator_reduces_to_public_exponent_gcd(self) -> None:
        for modulus in range(4, 80):
            for exponent in range(1, 40):
                evaluation = evaluate_geometric_sum(1, modulus, exponent)
                self.assertEqual(evaluation.division_status, "full_collision")
                self.assertEqual(evaluation.sum_residue, exponent % modulus)
                self.assertEqual(evaluation.sum_gcd, math.gcd(exponent, modulus))
                self.assertEqual(evaluation.sum_gcd, evaluation.exponent_gcd)

    def test_repeated_prime_power_factor_values_are_preserved(self) -> None:
        evaluation = evaluate_geometric_sum(1, 8, 4)
        self.assertEqual(evaluation.sum_residue, 4)
        self.assertEqual(evaluation.sum_gcd, 4)
        self.assertEqual(evaluation.exponent_gcd, 4)

    def test_exponent_one_and_operation_counts(self) -> None:
        for exponent in range(1, 256):
            evaluation = evaluate_geometric_sum(2, 257, exponent)
            trailing_bits = bin(exponent)[3:]
            expected_multiplications = 2 * len(trailing_bits) + trailing_bits.count("1")
            expected_additions = len(trailing_bits) + trailing_bits.count("1")
            self.assertEqual(
                evaluation.multiplication_count,
                expected_multiplications,
            )
            self.assertEqual(evaluation.addition_count, expected_additions)
            self.assertEqual(evaluation.formal_degree, exponent - 1)
            self.assertEqual(evaluation.formal_monomial_count, exponent)
        base_case = evaluate_geometric_sum(2, 257, 1)
        self.assertEqual(base_case.power_residue, 2)
        self.assertEqual(base_case.sum_residue, 1)
        self.assertEqual(base_case.multiplication_count, 0)
        self.assertEqual(base_case.addition_count, 0)

    def test_invalid_inputs_are_rejected(self) -> None:
        for arguments in (
            (2, 1, 3),
            (2, 15, 0),
            (5, 15, 3),
            (True, 15, 3),
            (2, 15, True),
        ):
            with self.assertRaises(ValueError):
                evaluate_geometric_sum(*arguments)
        with self.assertRaises(ValueError):
            geometric_sum_coefficients(0)
        with self.assertRaises(ValueError):
            geometric_sum_coefficients(65_537)


if __name__ == "__main__":
    unittest.main()
