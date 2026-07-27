"""Exact tests for the M25 Galois-orbit classification."""

from __future__ import annotations

import unittest
from fractions import Fraction

from python.mosef_reference.rational_root_orbit import (
    classify_rational_root_orbit,
    exact_cyclotomic_root_ratio,
    rational_root_order_descriptor,
)


class RationalRootOrbitTests(unittest.TestCase):
    def test_three_rational_families(self) -> None:
        common = classify_rational_root_orbit(4, 7, 3)
        self.assertEqual(common.category, "common_step")
        self.assertEqual(common.rational_ratio, -1)
        self.assertEqual(
            (
                common.primitive_first_coefficient,
                common.primitive_second_coefficient,
            ),
            (-1, 1),
        )

        phi4 = classify_rational_root_orbit(3, 7, 4)
        self.assertEqual(phi4.category, "phi4")
        self.assertEqual(phi4.rational_ratio, 1)
        self.assertEqual(exact_cyclotomic_root_ratio(3, 7, 4), Fraction(1))

        phi6 = classify_rational_root_orbit(5, 3, 6)
        self.assertEqual(phi6.category, "phi6")
        self.assertEqual(phi6.rational_ratio, 2)
        self.assertEqual(exact_cyclotomic_root_ratio(5, 3, 6), Fraction(2))

    def test_phase_divisibility_is_not_sufficient(self) -> None:
        obstruction = classify_rational_root_orbit(2, 4, 5)
        self.assertTrue(obstruction.outside_stage_zeros)
        self.assertTrue(obstruction.phase_divisible)
        self.assertEqual(obstruction.category, "irrational")
        self.assertIsNone(exact_cyclotomic_root_ratio(2, 4, 5))

    def test_stage_zeros_are_outside_the_ratio_domain(self) -> None:
        self.assertEqual(
            classify_rational_root_orbit(4, 3, 2).category,
            "stage_zero",
        )
        self.assertEqual(
            classify_rational_root_orbit(2, 3, 3).category,
            "stage_zero",
        )
        self.assertIsNone(exact_cyclotomic_root_ratio(2, 3, 3))

    def test_compact_descriptor(self) -> None:
        descriptor = rational_root_order_descriptor(11, 15)
        self.assertEqual(descriptor.common_step, 2)
        self.assertTrue(descriptor.phi4_enabled)
        self.assertTrue(descriptor.phi6_enabled)

    def test_exact_enumeration_matches_classification(self) -> None:
        for first_factor in range(2, 13):
            for second_factor in range(2, 13):
                if first_factor == second_factor:
                    continue
                for order in range(2, 65):
                    predicted = classify_rational_root_orbit(
                        first_factor,
                        second_factor,
                        order,
                    )
                    exact = exact_cyclotomic_root_ratio(
                        first_factor,
                        second_factor,
                        order,
                    )
                    expected = (
                        None
                        if predicted.rational_ratio is None
                        else Fraction(predicted.rational_ratio)
                    )
                    self.assertEqual(exact, expected)

    def test_invalid_inputs_raise(self) -> None:
        for arguments in (
            (1, 3, 4),
            (3, 1, 4),
            (3, 3, 4),
            (3, 7, 1),
            (True, 7, 4),
        ):
            with self.assertRaises(ValueError):
                classify_rational_root_orbit(*arguments)


if __name__ == "__main__":
    unittest.main()
