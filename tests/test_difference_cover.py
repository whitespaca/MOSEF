"""Exact and exhaustive tests for the M4 divisor-cover barrier."""

from __future__ import annotations

import itertools
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

from mosef_reference import (
    CandidateKind,
    analyze_cover,
    evaluate_separator_candidate,
    has_distinct_order_separator_property,
    has_n_divisor_property,
    multiplicative_order_mod_prime,
    positive_differences,
    signature_count_lower_bound,
    square_difference_cover,
)


class DifferenceCoverTests(unittest.TestCase):
    def test_minimal_divisor_cover_is_not_a_separator(self) -> None:
        self.assertEqual(positive_differences((3,), (1,)), (2,))
        analysis = analyze_cover((2,), (1, 2))
        self.assertTrue(analysis.divisor_cover)
        self.assertFalse(analysis.separates_profile)
        self.assertFalse(analysis.distinct_signatures)

    def test_counterexample_is_realized_by_multiplicative_orders(self) -> None:
        self.assertEqual(multiplicative_order_mod_prime(5, 2), 1)
        self.assertEqual(multiplicative_order_mod_prime(5, 3), 2)
        self.assertEqual(
            evaluate_separator_candidate(6, 5, 2).kind,
            CandidateKind.SIMULTANEOUS_COLLISION,
        )
        self.assertEqual(multiplicative_order_mod_prime(4, 3), 1)
        self.assertEqual(multiplicative_order_mod_prime(4, 5), 2)
        self.assertEqual(
            evaluate_separator_candidate(15, 4, 2).kind,
            CandidateKind.SIMULTANEOUS_COLLISION,
        )

    def test_signature_characterization_exhaustively(self) -> None:
        universe = range(1, 9)
        for size in range(1, 5):
            for candidates in itertools.combinations(universe, size):
                for orders in itertools.product(range(1, 7), repeat=3):
                    analysis = analyze_cover(candidates, orders)
                    self.assertEqual(
                        analysis.separates_profile,
                        len(set(analysis.signatures)) > 1,
                        (candidates, orders),
                    )

    def test_square_construction_covers_and_separates(self) -> None:
        for bound in range(1, 101):
            left, right, candidates = square_difference_cover(bound)
            width = len(left)
            self.assertEqual(len(right), width)
            self.assertEqual(candidates, tuple(range(1, width * width + 1)))
            self.assertTrue(has_n_divisor_property(candidates, bound))
            self.assertTrue(
                has_distinct_order_separator_property(candidates, bound)
            )

    def test_signature_count_lower_bound(self) -> None:
        expected = {1: 1, 2: 2, 3: 2, 4: 3, 7: 3, 8: 4, 15: 4, 16: 5}
        for bound, value in expected.items():
            self.assertEqual(signature_count_lower_bound(bound), value)

    def test_separator_property_does_not_require_divisor_coverage(self) -> None:
        candidates = (1,)
        self.assertFalse(has_n_divisor_property(candidates, 2))
        self.assertTrue(has_distinct_order_separator_property(candidates, 2))
        self.assertTrue(analyze_cover(candidates, (1, 2)).separates_profile)

    def test_invalid_domains_raise(self) -> None:
        invalid_calls = (
            lambda: positive_differences((), (1,)),
            lambda: positive_differences((0,), (1,)),
            lambda: analyze_cover((), (1, 2)),
            lambda: analyze_cover((1,), (1,)),
            lambda: has_n_divisor_property((1,), 0),
            lambda: has_distinct_order_separator_property((1,), 0),
            lambda: square_difference_cover(0),
            lambda: signature_count_lower_bound(0),
        )
        for invalid_call in invalid_calls:
            with self.subTest(invalid_call=invalid_call), self.assertRaises(ValueError):
                invalid_call()


if __name__ == "__main__":
    unittest.main()
