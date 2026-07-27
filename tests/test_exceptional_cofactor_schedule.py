"""Exact tests for the M27 exceptional-cofactor schedule barrier."""

from __future__ import annotations

import unittest

from python.mosef_reference.exceptional_cofactor_schedule import (
    evaluate_exceptional_cofactor_local_profile,
    exceptional_cofactor_overlap,
    exceptional_cofactor_root_residues,
)
from python.mosef_reference.exceptional_cyclotomic import (
    exceptional_cofactor_coefficients,
)


def reduce_quadratic(
    coefficients: tuple[int, ...],
    linear_coefficient: int,
) -> tuple[int, int]:
    """Return the remainder modulo x^2+a*x+1."""
    power_constant, power_linear = 1, 0
    result_constant, result_linear = 0, 0
    for coefficient in coefficients:
        result_constant += coefficient * power_constant
        result_linear += coefficient * power_linear
        power_constant, power_linear = (
            -power_linear,
            power_constant - linear_coefficient * power_linear,
        )
    return result_constant, result_linear


class ExceptionalCofactorScheduleTests(unittest.TestCase):
    def test_exact_cyclotomic_remainders_and_resultants(self) -> None:
        for first_factor, second_factor, family, linear_coefficient in (
            (3, 7, "phi4", 0),
            (7, 11, "phi4", 0),
            (11, 3, "phi4", 0),
            (5, 3, "phi6", -1),
            (11, 9, "phi6", -1),
            (17, 15, "phi6", -1),
        ):
            overlap = exceptional_cofactor_overlap(
                first_factor,
                second_factor,
                family,
            )
            remainder = reduce_quadratic(
                exceptional_cofactor_coefficients(
                    first_factor,
                    second_factor,
                    family,
                ),
                linear_coefficient,
            )
            self.assertEqual(
                remainder,
                (overlap.remainder_constant, overlap.remainder_linear),
            )
            constant, linear = remainder
            expected = (
                constant * constant + linear * linear
                if family == "phi4"
                else constant * constant + constant * linear + linear * linear
            )
            self.assertEqual(
                overlap.cyclotomic_cofactor_resultant,
                expected,
            )
            self.assertGreater(expected, 0)

    def test_local_roots_and_prime_power_valuations(self) -> None:
        roots = exceptional_cofactor_root_residues(5, 3, 7, "phi4")
        self.assertEqual(roots, (1, 2))
        first = evaluate_exceptional_cofactor_local_profile(
            1,
            5,
            2,
            3,
            7,
            "phi4",
        )
        self.assertTrue(first.is_cofactor_root_mod_prime)
        self.assertEqual(first.cofactor_valuation, 1)
        self.assertFalse(first.is_cyclotomic_root_mod_prime)

        repeated = evaluate_exceptional_cofactor_local_profile(
            3,
            5,
            2,
            5,
            3,
            "phi6",
        )
        self.assertTrue(repeated.is_cofactor_root_mod_prime)
        self.assertEqual(repeated.cofactor_valuation, 1)

    def test_overlap_descriptors(self) -> None:
        phi4 = exceptional_cofactor_overlap(3, 7, "phi4")
        self.assertEqual((phi4.remainder_constant, phi4.remainder_linear), (7, 4))
        self.assertEqual(phi4.cyclotomic_cofactor_resultant, 65)
        self.assertEqual(phi4.stage_overlap_support, (7,))
        self.assertEqual(phi4.second_stage_power_of_two_exponent, 0)

        phi6 = exceptional_cofactor_overlap(5, 3, "phi6")
        self.assertEqual((phi6.remainder_constant, phi6.remainder_linear), (-4, 13))
        self.assertEqual(phi6.cyclotomic_cofactor_resultant, 133)
        self.assertEqual(phi6.stage_overlap_support, (2, 3))
        self.assertEqual(phi6.second_stage_power_of_two_exponent, 8)

    def test_invalid_inputs(self) -> None:
        for call in (
            lambda: exceptional_cofactor_overlap(5, 7, "phi4"),
            lambda: exceptional_cofactor_overlap(5, 3, "phi8"),
            lambda: exceptional_cofactor_root_residues(9, 3, 7, "phi4"),
            lambda: evaluate_exceptional_cofactor_local_profile(
                5,
                5,
                1,
                3,
                7,
                "phi4",
            ),
        ):
            with self.subTest(call=call), self.assertRaises(ValueError):
                call()


if __name__ == "__main__":
    unittest.main()
