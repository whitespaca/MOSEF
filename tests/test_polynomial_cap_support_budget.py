"""Exact tests for the M47 polynomial-cap support budget."""

from __future__ import annotations

import unittest

from python.mosef_reference import (
    ExceptionalSelectorDescriptor,
    descriptor_bit_budget_upper_bound,
    descriptor_output_budget,
    exact_primitive_exit_integers,
    selector_descriptor_count_upper_bound,
    selector_output_bit_budget_upper_bound,
)


class PolynomialCapSupportBudgetTests(unittest.TestCase):
    def test_exact_phi4_and_phi6_primitive_values(self) -> None:
        cases = (
            (
                ExceptionalSelectorDescriptor("phi4", 3, 7, 2),
                (2, 7, 299593, 7, 7, 5, 65, 59920),
            ),
            (
                ExceptionalSelectorDescriptor("phi6", 5, 3, 2),
                (2, 31, 1057, 3, 6, 3, 133, 373),
            ),
        )
        for descriptor, expected in cases:
            with self.subTest(descriptor=descriptor.key):
                self.assertEqual(
                    exact_primitive_exit_integers(descriptor),
                    expected,
                )

    def test_every_sample_value_is_positive_and_bounded(self) -> None:
        cases = (
            ExceptionalSelectorDescriptor("phi4", 7, 11, 9),
            ExceptionalSelectorDescriptor("phi6", 11, 9, 12),
            ExceptionalSelectorDescriptor("phi4", 19, 15, 20),
        )
        for descriptor in cases:
            cap = max(
                descriptor.first_factor,
                descriptor.second_factor,
                descriptor.base,
            )
            with self.subTest(descriptor=descriptor.key):
                record = descriptor_output_budget(descriptor, cap)
                self.assertTrue(all(value > 0 for value in record.values))
                self.assertLessEqual(
                    record.bit_budget,
                    descriptor_bit_budget_upper_bound(cap),
                )

    def test_selector_bound_uses_all_descriptor_slots(self) -> None:
        for cap in (2, 9, 20, 201):
            with self.subTest(cap=cap):
                self.assertEqual(
                    selector_output_bit_budget_upper_bound(cap),
                    selector_descriptor_count_upper_bound(cap)
                    * descriptor_bit_budget_upper_bound(cap),
                )

    def test_invalid_inputs(self) -> None:
        descriptor = ExceptionalSelectorDescriptor("phi4", 3, 7, 2)
        for call in (
            lambda: exact_primitive_exit_integers(object()),  # type: ignore[arg-type]
            lambda: descriptor_bit_budget_upper_bound(True),
            lambda: descriptor_bit_budget_upper_bound(1),
            lambda: selector_descriptor_count_upper_bound(False),
            lambda: selector_output_bit_budget_upper_bound(1),
            lambda: descriptor_output_budget(descriptor, 6),
        ):
            with self.subTest(call=call), self.assertRaises(ValueError):
                call()


if __name__ == "__main__":
    unittest.main()
