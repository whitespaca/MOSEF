"""Exact tests for the M15 leaf-materialized product-tree model."""

from __future__ import annotations

import itertools
import math
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

from mosef_reference import (  # noqa: E402
    batch_tree_multiplication_count,
    evaluate_batch_product,
    prime_factorization,
)
from scripts.run_m15_implicit_batch_search import search  # noqa: E402


def valuation(value: int, prime: int) -> int:
    """Return the exact nonnegative prime-adic valuation."""
    if value == 0:
        return 1 << 60
    exponent = 0
    while value % prime == 0:
        value //= prime
        exponent += 1
    return exponent


class ImplicitBatchTests(unittest.TestCase):
    def test_named_union_collision_masks_two_separators(self) -> None:
        evaluation = evaluate_batch_product(2, 21, (2, 3))
        self.assertEqual(evaluation.leaf_residues, (3, 7))
        self.assertEqual(evaluation.leaf_gcds, (3, 7))
        self.assertEqual(evaluation.root_residue, 0)
        self.assertEqual(evaluation.root_gcd, 21)
        self.assertEqual(evaluation.multiplication_count, 1)

    def test_odd_tree_has_exact_multiplication_count(self) -> None:
        evaluation = evaluate_batch_product(2, 35, (1, 2, 3))
        self.assertEqual(evaluation.levels, ((1, 3, 7), (3, 7), (21,)))
        self.assertEqual(evaluation.root_residue, 21)
        self.assertEqual(evaluation.multiplication_count, 2)
        for leaf_count in range(1, 100):
            exponents = tuple(range(1, leaf_count + 1))
            actual = evaluate_batch_product(2, 101, exponents)
            self.assertEqual(
                actual.multiplication_count,
                batch_tree_multiplication_count(leaf_count),
            )

    def test_exact_valuation_formula_and_one_way_success(self) -> None:
        for modulus in range(4, 80):
            factorization = prime_factorization(modulus)
            for base in range(1, min(modulus, 12)):
                if math.gcd(base, modulus) != 1:
                    continue
                for length in range(1, 5):
                    for exponents in itertools.combinations(range(1, 7), length):
                        evaluation = evaluate_batch_product(base, modulus, exponents)
                        predicted = 1
                        for prime, multiplicity in factorization:
                            total = sum(
                                valuation(pow(base, exponent) - 1, prime)
                                for exponent in exponents
                            )
                            predicted *= prime ** min(multiplicity, total)
                        self.assertEqual(evaluation.root_gcd, predicted)
                        if 1 < evaluation.root_gcd < modulus:
                            self.assertTrue(
                                any(1 < divisor < modulus for divisor in evaluation.leaf_gcds)
                            )

    def test_invalid_domains_raise(self) -> None:
        invalid_calls = (
            lambda: evaluate_batch_product(2, 1, (1,)),
            lambda: evaluate_batch_product(True, 5, (1,)),
            lambda: evaluate_batch_product(2, True, (1,)),
            lambda: evaluate_batch_product(5, 35, (1,)),
            lambda: evaluate_batch_product(2, 5, ()),
            lambda: evaluate_batch_product(2, 5, (0,)),
            lambda: evaluate_batch_product(2, 5, (True,)),
            lambda: evaluate_batch_product(2, 5, (2, 1)),
            lambda: evaluate_batch_product(2, 5, (1, 1)),
            lambda: batch_tree_multiplication_count(0),
            lambda: batch_tree_multiplication_count(True),
        )
        for invalid_call in invalid_calls:
            with self.subTest(invalid_call=invalid_call):
                with self.assertRaises(ValueError):
                    invalid_call()

    def test_registered_search_smoke(self) -> None:
        result = search(7, 64, 12, 128)
        self.assertGreater(result["counts"]["subset_checks"], 0)
        self.assertGreater(result["counts"]["masked_separator_batches"], 0)
        self.assertEqual(result["tree"]["maximum_leaf_count"], 128)
        self.assertEqual(len(result["summary_sha256"]), 64)


if __name__ == "__main__":
    unittest.main()
