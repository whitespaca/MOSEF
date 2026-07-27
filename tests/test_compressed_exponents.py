"""Exact tests for the M10 multiplication straight-line compression model."""

from __future__ import annotations

import itertools
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

from mosef_reference import (
    evaluate_multiplication_program,
    generic_multiplication_lower_bound,
    repeated_squaring_program,
    tower_descriptor_exponent,
)


class CompressedExponentTests(unittest.TestCase):
    def test_repeated_squaring_attains_growth_bound(self) -> None:
        for multiplication_count in range(13):
            evaluation = evaluate_multiplication_program(
                7,
                91,
                repeated_squaring_program(multiplication_count),
            )
            self.assertEqual(evaluation.exponents[-1], 1 << multiplication_count)
            self.assertEqual(
                evaluation.residues[-1],
                pow(7, 1 << multiplication_count, 91),
            )
            self.assertEqual(
                evaluation.multiplication_count,
                multiplication_count,
            )

    def test_every_small_program_obeys_nodewise_bound(self) -> None:
        programs: list[tuple[tuple[int, int], ...]] = [()]
        for depth in range(1, 6):
            extended = []
            for program in programs:
                for left, right in itertools.combinations_with_replacement(
                    range(depth),
                    2,
                ):
                    candidate = (*program, (left, right))
                    evaluation = evaluate_multiplication_program(5, 77, candidate)
                    self.assertLessEqual(evaluation.exponents[-1], 1 << depth)
                    self.assertEqual(
                        evaluation.residues[-1],
                        pow(5, evaluation.exponents[-1], 77),
                    )
                    extended.append(candidate)
            programs = extended

    def test_shared_addition_chain_semantics(self) -> None:
        steps = ((0, 0), (1, 0), (2, 2), (3, 1))
        evaluation = evaluate_multiplication_program(11, 143, steps)
        self.assertEqual(evaluation.exponents, (1, 2, 3, 6, 8))
        self.assertEqual(
            evaluation.residues,
            tuple(pow(11, exponent, 143) for exponent in (1, 2, 3, 6, 8)),
        )

    def test_tower_descriptor_has_exponential_generic_cost(self) -> None:
        for level in range(13):
            exponent = tower_descriptor_exponent(level)
            required = 1 << level
            self.assertEqual(generic_multiplication_lower_bound(exponent), required)
            evaluation = evaluate_multiplication_program(
                3,
                101,
                repeated_squaring_program(required),
            )
            self.assertEqual(evaluation.exponents[-1], exponent)

    def test_invalid_domains_raise(self) -> None:
        invalid_calls = (
            lambda: evaluate_multiplication_program(2, 1, ()),
            lambda: evaluate_multiplication_program(True, 5, ()),
            lambda: evaluate_multiplication_program(2, 5, ((0, 1),)),
            lambda: evaluate_multiplication_program(2, 5, ((-1, 0),)),
            lambda: evaluate_multiplication_program(2, 5, ([0, 0],)),
            lambda: repeated_squaring_program(-1),
            lambda: generic_multiplication_lower_bound(0),
            lambda: tower_descriptor_exponent(-1),
        )
        for invalid_call in invalid_calls:
            with self.subTest(invalid_call=invalid_call), self.assertRaises(ValueError):
                invalid_call()


if __name__ == "__main__":
    unittest.main()
