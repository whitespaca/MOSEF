"""Exact tests for the M14 addition-subtraction representation."""

from __future__ import annotations

import itertools
import math
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

from mosef_reference import (  # noqa: E402
    absolute_exponent_support,
    evaluate_addition_subtraction_program,
    signed_exponent_lower_bound,
)
from scripts.run_m14_addition_subtraction_search import search  # noqa: E402


class AdditionSubtractionExponentTests(unittest.TestCase):
    def test_signed_semantics_cancellation_and_inversion_count(self) -> None:
        steps = (
            (0, 0, 1),
            (1, 0, -1),
            (0, 1, -1),
            (3, 3, 1),
            (2, 2, -1),
        )
        evaluation = evaluate_addition_subtraction_program(5, 77, steps)
        self.assertEqual(evaluation.exponents, (1, 2, 1, -1, -2, 0))
        self.assertEqual(
            evaluation.residues,
            tuple(pow(5, exponent, 77) for exponent in evaluation.exponents),
        )
        self.assertEqual(evaluation.inversion_count, 3)
        self.assertEqual(evaluation.residues[-1], 1)

    def test_every_small_program_obeys_signed_node_bound(self) -> None:
        programs: list[tuple[tuple[int, int, int], ...]] = [()]
        for depth in range(1, 6):
            extended = []
            additions = (
                (left, right, 1)
                for left, right in itertools.combinations_with_replacement(
                    range(depth),
                    2,
                )
            )
            subtractions = (
                (left, right, -1)
                for left in range(depth)
                for right in range(depth)
                if left != right
            )
            options = tuple(additions) + tuple(subtractions)
            for program in programs:
                for step in options:
                    candidate = (*program, step)
                    evaluation = evaluate_addition_subtraction_program(
                        5,
                        77,
                        candidate,
                    )
                    self.assertLessEqual(
                        abs(evaluation.exponents[-1]),
                        1 << depth,
                    )
                    self.assertEqual(
                        evaluation.residues[-1],
                        pow(5, evaluation.exponents[-1], 77),
                    )
                    extended.append(candidate)
            programs = extended

    def test_positive_and_negative_candidates_have_same_gcd(self) -> None:
        for modulus in range(4, 100):
            for base in range(1, 20):
                if math.gcd(base, modulus) != 1:
                    continue
                for exponent in range(1, 20):
                    positive = math.gcd(
                        pow(base, exponent, modulus) - 1,
                        modulus,
                    )
                    negative = math.gcd(
                        pow(base, -exponent, modulus) - 1,
                        modulus,
                    )
                    self.assertEqual(positive, negative)

    def test_absolute_support_discards_sign_zero_and_duplicates(self) -> None:
        self.assertEqual(
            absolute_exponent_support((1, -2, 0, 2, -5, 1)),
            (1, 2, 5),
        )

    def test_signed_growth_lower_bound(self) -> None:
        for exponent in (-257, -256, -3, -1, 1, 2, 255, 256, 257):
            required = signed_exponent_lower_bound(exponent)
            self.assertGreaterEqual(1 << required, abs(exponent))
            if required:
                self.assertLess(1 << (required - 1), abs(exponent))

    def test_invalid_domains_raise(self) -> None:
        invalid_calls = (
            lambda: evaluate_addition_subtraction_program(2, 1, ()),
            lambda: evaluate_addition_subtraction_program(True, 5, ()),
            lambda: evaluate_addition_subtraction_program(2, 6, ()),
            lambda: evaluate_addition_subtraction_program(2, 5, ((0, 1, 1),)),
            lambda: evaluate_addition_subtraction_program(2, 5, ((0, 0, 0),)),
            lambda: evaluate_addition_subtraction_program(2, 5, ((0, 0, True),)),
            lambda: evaluate_addition_subtraction_program(2, 5, ([0, 0, 1],)),
            lambda: absolute_exponent_support((1, True)),
            lambda: signed_exponent_lower_bound(0),
        )
        for invalid_call in invalid_calls:
            with self.subTest(invalid_call=invalid_call):
                with self.assertRaises(ValueError):
                    invalid_call()

    def test_registered_search_smoke(self) -> None:
        result = search(4, 3, 64, 12, 16)
        self.assertEqual(result["programs_by_depth"], [1, 1, 5, 60, 1320])
        self.assertEqual(
            result["maximum_absolute_exponent"],
            [1, 2, 4, 8, 16],
        )
        self.assertEqual(len(result["summary_sha256"]), 64)


if __name__ == "__main__":
    unittest.main()
