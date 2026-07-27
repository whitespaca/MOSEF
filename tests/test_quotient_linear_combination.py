"""Exact tests for M21 signed combinations of quotient stages."""

from __future__ import annotations

import math
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

from mosef_reference import (
    evaluate_quotient_linear_combination,
    expand_quotient_linear_combination,
)


class QuotientLinearCombinationTests(unittest.TestCase):
    def test_prime_power_witness_has_only_unit_components(self) -> None:
        value = evaluate_quotient_linear_combination(2, 9, (5, 5), (-1, 1))
        self.assertEqual(
            tuple(stage.quotient_residue for stage in value.chain.stages),
            (4, 7),
        )
        self.assertEqual(value.coefficient_gcds, (1, 1))
        self.assertEqual(value.weighted_stage_gcds, (1, 1))
        for stage in value.chain.stages:
            self.assertEqual(stage.intermediate_gcd, 1)
            self.assertEqual(stage.quotient_gcd, 1)
            self.assertEqual(stage.rational_numerator_gcd, 1)
            self.assertEqual(stage.composed_denominator_gcd, 1)
            self.assertEqual(stage.endpoint_gcd, 1)
            self.assertEqual(stage.multiplier_gcd, 1)
        self.assertEqual(value.aggregate_residue, 3)
        self.assertEqual(value.aggregate_gcd, 3)

    def test_witness_sparse_polynomial_is_exact(self) -> None:
        self.assertEqual(
            expand_quotient_linear_combination((5, 5), (-1, 1)),
            (
                (1, -1),
                (2, -1),
                (3, -1),
                (4, -1),
                (5, 1),
                (10, 1),
                (15, 1),
                (20, 1),
            ),
        )

    def test_sparse_expansion_matches_compact_evaluation(self) -> None:
        cases = (
            ((2, 3), (1, -1)),
            ((1, 4, 2), (2, -1, 1)),
            ((3, 1, 3), (-2, 1, 2)),
        )
        for modulus in range(4, 40):
            for base in range(modulus):
                if math.gcd(base, modulus) != 1:
                    continue
                for factors, coefficients in cases:
                    value = evaluate_quotient_linear_combination(
                        base, modulus, factors, coefficients
                    )
                    direct = sum(
                        coefficient * pow(base, exponent, modulus)
                        for exponent, coefficient in expand_quotient_linear_combination(
                            factors, coefficients
                        )
                    ) % modulus
                    self.assertEqual(value.aggregate_residue, direct)

    def test_exact_cancellation_has_full_aggregate(self) -> None:
        value = evaluate_quotient_linear_combination(2, 15, (1, 1), (1, -1))
        self.assertEqual(value.weighted_stage_gcds, (1, 1))
        self.assertEqual(value.aggregate_residue, 0)
        self.assertEqual(value.aggregate_gcd, 15)
        self.assertEqual(expand_quotient_linear_combination((1, 1), (1, -1)), ())

    def test_operation_counts_and_metadata(self) -> None:
        value = evaluate_quotient_linear_combination(
            2, 257, (3, 5, 7), (2, -3, 1)
        )
        self.assertEqual(
            value.multiplication_count,
            value.chain.multiplication_count + 3,
        )
        self.assertEqual(
            value.addition_count,
            value.chain.addition_count + 2,
        )
        self.assertEqual(value.formal_degree_bound, 90)
        self.assertEqual(value.uncollected_term_count, 15)

    def test_invalid_inputs_raise(self) -> None:
        for arguments in (
            (2, 15, (), ()),
            (2, 15, (2,), ()),
            (2, 15, (2, 0), (1, 1)),
            (5, 15, (2,), (1,)),
            (2, 1, (2,), (1,)),
        ):
            with self.assertRaises(ValueError):
                evaluate_quotient_linear_combination(*arguments)
        with self.assertRaises(ValueError):
            expand_quotient_linear_combination((2,), (1, 2))


if __name__ == "__main__":
    unittest.main()
