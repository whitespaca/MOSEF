"""Exact tests for the M20 iterated geometric-quotient chain."""

from __future__ import annotations

import math
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

from mosef_reference import evaluate_iterated_quotient  # noqa: E402


class IteratedQuotientTests(unittest.TestCase):
    def test_bounded_chain_identities_and_stage_trichotomies(self) -> None:
        chains = ((1,), (2,), (2, 2), (2, 3, 2), (1, 3, 1, 2))
        for modulus in range(4, 45):
            for base in range(modulus):
                if math.gcd(base, modulus) != 1:
                    continue
                for factors in chains:
                    value = evaluate_iterated_quotient(base, modulus, factors)
                    self.assertEqual(
                        value.final_prefix_residue,
                        value.final_quotient_product_residue,
                    )
                    for index, stage in enumerate(value.stages):
                        self.assertEqual(
                            stage.rational_numerator_residue,
                            stage.intermediate_residue
                            * stage.quotient_residue
                            % modulus,
                        )
                        if index:
                            self.assertEqual(
                                stage.intermediate_residue,
                                value.stages[
                                    index - 1
                                ].rational_numerator_residue,
                            )
                        if stage.rational_division_status == "unit":
                            self.assertEqual(
                                stage.rational_numerator_gcd,
                                stage.quotient_gcd,
                            )
                        elif stage.rational_division_status == "proper_factor":
                            self.assertTrue(1 < stage.intermediate_gcd < modulus)
                        else:
                            self.assertEqual(stage.intermediate_gcd, modulus)
                            self.assertEqual(
                                stage.quotient_gcd,
                                stage.multiplier_gcd,
                            )

    def test_prefix_exponents_and_factor_one(self) -> None:
        value = evaluate_iterated_quotient(2, 35, (1, 2, 1, 3))
        self.assertEqual(value.prefix_exponents, (1, 1, 2, 2, 6))
        self.assertEqual(value.stages[0].quotient_residue, 1)
        self.assertEqual(value.stages[2].quotient_residue, 1)
        self.assertEqual(value.final_prefix_residue, value.stages[-1].rational_numerator_residue)

    def test_proper_prefix_can_expose_different_stage_factor(self) -> None:
        value = evaluate_iterated_quotient(2, 15, (2, 2, 3))
        stage = value.stages[1]
        self.assertEqual(stage.intermediate_gcd, 3)
        self.assertEqual(stage.quotient_gcd, 5)
        self.assertEqual(stage.rational_numerator_gcd, 15)

    def test_full_prefix_reduces_to_public_multiplier(self) -> None:
        value = evaluate_iterated_quotient(2, 15, (4, 5, 2))
        stage = value.stages[1]
        self.assertEqual(stage.intermediate_gcd, 15)
        self.assertEqual(stage.inner_power_residue, 1)
        self.assertEqual(stage.quotient_gcd, stage.multiplier_gcd)
        self.assertEqual(stage.quotient_gcd, 5)

    def test_proper_final_product_has_proper_stage(self) -> None:
        for modulus in range(4, 65):
            for base in range(modulus):
                if math.gcd(base, modulus) != 1:
                    continue
                value = evaluate_iterated_quotient(base, modulus, (2, 3, 2))
                if 1 < value.final_prefix_gcd < modulus:
                    self.assertTrue(
                        any(
                            1 < stage.quotient_gcd < modulus
                            for stage in value.stages
                        )
                    )

    def test_operation_count_and_invalid_inputs(self) -> None:
        value = evaluate_iterated_quotient(2, 257, (3, 5, 7))
        self.assertEqual(
            value.multiplication_count,
            sum(stage.multiplication_count for stage in value.stages) + 2,
        )
        self.assertEqual(
            value.addition_count,
            sum(stage.addition_count for stage in value.stages),
        )
        for arguments in (
            (2, 15, ()),
            (2, 15, (2, 0)),
            (2, 15, (2, -1)),
            (5, 15, (2,)),
            (2, 1, (2,)),
        ):
            with self.assertRaises(ValueError):
                evaluate_iterated_quotient(*arguments)


if __name__ == "__main__":
    unittest.main()
