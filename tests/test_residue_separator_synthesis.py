"""Tests for the M60--M80 residue and restricted-factor synthesis."""

from __future__ import annotations

import unittest

from python.mosef_reference.residue_separator_synthesis import (
    minimal_divisibility_antichain,
    residue_union_ledger,
    restricted_phi4_separated_pairs,
    restricted_phi4_separator_factor,
)


class ResidueSeparatorSynthesisTests(unittest.TestCase):
    def test_minimal_antichain_preserves_nested_residue_union(self) -> None:
        self.assertEqual(
            minimal_divisibility_antichain((3, 9, 5, 15, 45)),
            (3, 5),
        )

    def test_endpoint_ledgers_are_exact_and_bounded(self) -> None:
        for input_length in range(9, 25):
            ledger = residue_union_ledger(
                input_length,
                input_length // 2,
            )
            self.assertLessEqual(
                ledger.residue_union_size,
                ledger.elementary_union_bound,
            )
            self.assertLessEqual(
                ledger.residue_union_size,
                ledger.interval_size,
            )
            self.assertTrue(
                set(ledger.minimal_divisors).issubset(
                    ledger.admissible_divisors
                )
            )

    def test_restricted_separator_returns_an_actual_factor(self) -> None:
        factor = restricted_phi4_separator_factor(17, 19, tuple(range(2, 20)))
        if factor is not None:
            self.assertIn(factor, (17, 19))
        for input_length in range(9, 15):
            separated, factored = restricted_phi4_separated_pairs(
                input_length,
                tuple(range(2, input_length + 13)),
            )
            self.assertEqual(separated, factored)

    def test_invalid_inputs(self) -> None:
        for call in (
            lambda: residue_union_ledger(8, 4),
            lambda: residue_union_ledger(10, 0),
            lambda: minimal_divisibility_antichain((0, 1)),
            lambda: restricted_phi4_separator_factor(17, 17, (2,)),
        ):
            with self.assertRaises(ValueError):
                call()


if __name__ == "__main__":
    unittest.main()
