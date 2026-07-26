"""Exact tests for the M22 symmetric quotient-difference factorization."""

from __future__ import annotations

import math
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

from mosef_reference import (  # noqa: E402
    evaluate_symmetric_quotient_difference,
    symmetric_cofactor_terms,
)


def direct_geometric_sum(base: int, exponent: int) -> int:
    return sum(base**index for index in range(exponent))


class SymmetricQuotientDifferenceTests(unittest.TestCase):
    def test_m21_witness_reduces_to_proper_endpoint(self) -> None:
        value = evaluate_symmetric_quotient_difference(2, 9, 5)
        self.assertEqual(value.first_quotient_residue, 4)
        self.assertEqual(value.second_quotient_residue, 7)
        self.assertEqual(value.difference_residue, 3)
        self.assertEqual(value.difference_gcd, 3)
        self.assertEqual(value.endpoint_residue, 6)
        self.assertEqual(value.endpoint_gcd, 3)
        self.assertEqual(value.endpoint_status, "proper_factor")

    def test_formal_factorization_is_exact(self) -> None:
        for exponent in range(2, 12):
            terms = symmetric_cofactor_terms(exponent)
            self.assertEqual(len(terms), exponent * (exponent - 1) // 2)
            self.assertEqual(len(terms), len(set(terms)))
            self.assertEqual(max(terms), exponent * (exponent - 2))
            for base in range(-3, 5):
                first = direct_geometric_sum(base, exponent)
                second = direct_geometric_sum(base**exponent, exponent)
                cofactor = sum(base**term for term in terms)
                self.assertEqual(
                    second - first,
                    base * (base ** (exponent - 1) - 1) * cofactor,
                )

    def test_compact_cofactor_matches_expansion(self) -> None:
        for modulus in range(4, 80):
            for base in range(modulus):
                if math.gcd(base, modulus) != 1:
                    continue
                for exponent in range(2, 18):
                    value = evaluate_symmetric_quotient_difference(
                        base,
                        modulus,
                        exponent,
                    )
                    direct = sum(
                        pow(base, term, modulus)
                        for term in symmetric_cofactor_terms(exponent)
                    ) % modulus
                    self.assertEqual(value.cofactor_residue, direct)

    def test_total_endpoint_trichotomy(self) -> None:
        counts = {"unit": 0, "proper_factor": 0, "full_collision": 0}
        for modulus in range(4, 80):
            for base in range(modulus):
                if math.gcd(base, modulus) != 1:
                    continue
                for exponent in range(2, 14):
                    value = evaluate_symmetric_quotient_difference(
                        base,
                        modulus,
                        exponent,
                    )
                    counts[value.endpoint_status] += 1
                    if value.endpoint_status == "unit":
                        self.assertEqual(
                            value.difference_gcd,
                            value.cofactor_gcd,
                        )
                    elif value.endpoint_status == "full_collision":
                        self.assertEqual(value.difference_gcd, modulus)
        self.assertTrue(all(counts.values()))

    def test_matrix_cost_is_logarithmic(self) -> None:
        for exponent in (2, 3, 5, 17, 257, 65_537):
            value = evaluate_symmetric_quotient_difference(
                2,
                1_000_003,
                exponent,
            )
            self.assertLessEqual(
                value.matrix_multiplication_count,
                2 * max(0, (exponent - 2).bit_length()),
            )

    def test_invalid_inputs_raise(self) -> None:
        for arguments in (
            (2, 9, 1),
            (2, 1, 5),
            (3, 9, 5),
            (True, 9, 5),
        ):
            with self.assertRaises(ValueError):
                evaluate_symmetric_quotient_difference(*arguments)
        with self.assertRaises(ValueError):
            symmetric_cofactor_terms(1)


if __name__ == "__main__":
    unittest.main()
