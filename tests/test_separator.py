"""Exact and adversarial tests for the M2 separator semantics."""

from __future__ import annotations

import math
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

from mosef_reference import (  # noqa: E402
    CandidateKind,
    capped_valuation_profile,
    evaluate_separator_candidate,
    multiplicative_order_mod_prime,
    order_support,
    prime_factorization,
    support_is_separator,
    valuation_predicts_factor,
)


class SeparatorDefinitionTests(unittest.TestCase):
    def test_factorization_and_orders(self) -> None:
        self.assertEqual(prime_factorization(360), ((2, 3), (3, 2), (5, 1)))
        self.assertEqual(multiplicative_order_mod_prime(2, 3), 2)
        self.assertEqual(multiplicative_order_mod_prime(2, 5), 4)
        self.assertEqual(order_support(15, 2, 2), (3,))

    def test_square_free_separator_is_exact(self) -> None:
        outcome = evaluate_separator_candidate(15, 2, 2)
        self.assertEqual(outcome.kind, CandidateKind.FACTOR)
        self.assertEqual(outcome.factor, 3)
        self.assertTrue(support_is_separator(15, 2, 2))
        self.assertTrue(valuation_predicts_factor(15, 2, 2))

    def test_repeated_prime_support_is_not_necessary(self) -> None:
        outcome = evaluate_separator_candidate(4, 3, 1)
        self.assertEqual(outcome.kind, CandidateKind.FACTOR)
        self.assertEqual(outcome.factor, 2)
        self.assertFalse(support_is_separator(4, 3, 1))
        self.assertEqual(capped_valuation_profile(4, 3, 1), ((2, 2, 1),))
        self.assertTrue(valuation_predicts_factor(4, 3, 1))

    def test_odd_prime_power_has_same_support_failure(self) -> None:
        outcome = evaluate_separator_candidate(9, 2, 2)
        self.assertEqual(outcome.kind, CandidateKind.FACTOR)
        self.assertEqual(outcome.factor, 3)
        self.assertFalse(support_is_separator(9, 2, 2))
        self.assertEqual(capped_valuation_profile(9, 2, 2), ((3, 2, 1),))

    def test_all_candidate_outcomes(self) -> None:
        cases = (
            ((15, 3, 1), CandidateKind.DIRECT_FACTOR, 3),
            ((15, 0, 1), CandidateKind.INVALID_BASE, None),
            ((15, 2, 1), CandidateKind.MISS, None),
            ((15, 2, 2), CandidateKind.FACTOR, 3),
            ((15, 4, 2), CandidateKind.SIMULTANEOUS_COLLISION, None),
        )
        for arguments, kind, factor in cases:
            with self.subTest(arguments=arguments):
                outcome = evaluate_separator_candidate(*arguments)
                self.assertEqual(outcome.kind, kind)
                self.assertEqual(outcome.factor, factor)

    def test_named_adversarial_boundaries(self) -> None:
        order_one = evaluate_separator_candidate(15, 1, 1)
        self.assertEqual(order_one.kind, CandidateKind.SIMULTANEOUS_COLLISION)

        valuation_only = evaluate_separator_candidate(12, 7, 1)
        self.assertEqual(valuation_only.kind, CandidateKind.FACTOR)
        self.assertEqual(valuation_only.factor, 6)
        self.assertFalse(support_is_separator(12, 7, 1))
        self.assertEqual(
            capped_valuation_profile(12, 7, 1),
            ((2, 2, 1), (3, 1, 1)),
        )

        equal_orders = evaluate_separator_candidate(15, 14, 2)
        self.assertEqual(equal_orders.kind, CandidateKind.SIMULTANEOUS_COLLISION)
        self.assertEqual(order_support(15, 14, 2), (3, 5))

        carmichael_collision = evaluate_separator_candidate(561, 2, 80)
        self.assertEqual(
            carmichael_collision.kind,
            CandidateKind.SIMULTANEOUS_COLLISION,
        )

    def test_invalid_domains_raise(self) -> None:
        invalid_calls = (
            lambda: prime_factorization(1),
            lambda: multiplicative_order_mod_prime(2, 9),
            lambda: multiplicative_order_mod_prime(3, 3),
            lambda: order_support(15, 3, 1),
            lambda: capped_valuation_profile(15, 2, 0),
            lambda: evaluate_separator_candidate(1, 2, 1),
            lambda: evaluate_separator_candidate(15, 2, 0),
        )
        for invalid_call in invalid_calls:
            with self.subTest(invalid_call=invalid_call):
                with self.assertRaises(ValueError):
                    invalid_call()


class SeparatorExhaustiveTests(unittest.TestCase):
    def test_bounded_criteria_against_direct_gcd(self) -> None:
        support_false_negatives: list[tuple[int, int, int]] = []
        for n in range(4, 151):
            factorization = prime_factorization(n)
            if len(factorization) == 1 and factorization[0][1] == 1:
                continue
            square_free = all(exponent == 1 for _, exponent in factorization)
            for g in range(2, 13):
                if math.gcd(g, n) != 1:
                    continue
                for d in range(1, 13):
                    outcome = evaluate_separator_candidate(n, g, d)
                    actual = outcome.kind == CandidateKind.FACTOR
                    support = support_is_separator(n, g, d)
                    valuation = valuation_predicts_factor(n, g, d)
                    self.assertEqual(valuation, actual, (n, g, d))
                    if support:
                        self.assertTrue(actual, (n, g, d))
                    if square_free:
                        self.assertEqual(support, actual, (n, g, d))
                    elif actual and not support:
                        support_false_negatives.append((n, g, d))
        self.assertTrue(support_false_negatives)
        self.assertEqual(min(support_false_negatives), (4, 3, 1))


if __name__ == "__main__":
    unittest.main()
