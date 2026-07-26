"""Exact and adversarial tests for the M5 two-channel analysis."""

from __future__ import annotations

import math
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

from mosef_reference import (  # noqa: E402
    CandidateKind,
    LucasCandidateKind,
    analyze_conjugate_pair,
    candidate_succeeds,
    conjugate_parameter,
    evaluate_lucas_candidate,
    evaluate_separator_candidate,
)


def is_squarefree(value: int) -> bool:
    """Return whether no prime square divides ``value``."""
    for prime in range(2, math.isqrt(value) + 1):
        if value % (prime * prime) == 0:
            return False
    return True


class LucasCandidateTests(unittest.TestCase):
    def test_every_exact_branch(self) -> None:
        cases = (
            ((15, 5, 3), LucasCandidateKind.DISCRIMINANT_FACTOR, 3, None),
            ((15, 13, 1), LucasCandidateKind.DEGENERATE_MISS, None, 13),
            ((15, 8, 1), LucasCandidateKind.DEGENERATE_FACTOR, 3, 8),
            ((15, 2, 3), LucasCandidateKind.DEGENERATE_COLLISION, None, 2),
            ((15, 6, 1), LucasCandidateKind.MISS, None, 6),
            ((35, 20, 3), LucasCandidateKind.FACTOR, 7, 30),
            ((6, 3, 12), LucasCandidateKind.SIMULTANEOUS_COLLISION, None, 2),
        )
        for arguments, kind, factor, residue in cases:
            with self.subTest(arguments=arguments):
                outcome = evaluate_lucas_candidate(*arguments)
                self.assertEqual(outcome.kind, kind)
                self.assertEqual(outcome.factor, factor)
                self.assertEqual(outcome.residue, residue)

    def test_independently_selected_parameter_can_complement_a_miss(self) -> None:
        multiplicative = evaluate_separator_candidate(15, 2, 3)
        lucas = evaluate_lucas_candidate(15, 9, 3)
        self.assertEqual(multiplicative.kind, CandidateKind.MISS)
        self.assertEqual(lucas.kind, LucasCandidateKind.FACTOR)
        self.assertEqual(lucas.factor, 5)

    def test_invalid_domains_raise(self) -> None:
        calls = (
            lambda: evaluate_lucas_candidate(1, 2, 3),
            lambda: evaluate_lucas_candidate(15, 2, 0),
            lambda: conjugate_parameter(1, 2),
            lambda: conjugate_parameter(15, 3),
            lambda: analyze_conjugate_pair(1, 2, 3),
            lambda: analyze_conjugate_pair(15, 3, 3),
            lambda: analyze_conjugate_pair(15, 2, 0),
        )
        for call in calls:
            with self.subTest(call=call):
                with self.assertRaises(ValueError):
                    call()


class ConjugatePairTests(unittest.TestCase):
    def test_registered_factor_and_valuation_collision(self) -> None:
        factor = analyze_conjugate_pair(35, 2, 3)
        self.assertEqual(factor.parameter, 20)
        self.assertEqual(factor.multiplicative_gcd, 7)
        self.assertEqual(factor.lucas_gcd, 7)
        self.assertEqual(factor.discriminant_gcd, 1)
        self.assertTrue(factor.discriminant_identity)
        self.assertTrue(factor.lucas_identity)

        collision = analyze_conjugate_pair(49, 2, 3)
        self.assertEqual(collision.parameter, 27)
        self.assertEqual(collision.multiplicative_gcd, 7)
        self.assertEqual(collision.lucas_gcd, 49)
        self.assertEqual(
            collision.lucas.kind,
            LucasCandidateKind.SIMULTANEOUS_COLLISION,
        )

    def test_identities_hold_exhaustively(self) -> None:
        checks = 0
        for n in range(2, 201):
            for base in range(1, n):
                if math.gcd(base, n) != 1:
                    continue
                for exponent in range(1, 13):
                    analysis = analyze_conjugate_pair(n, base, exponent)
                    self.assertTrue(
                        analysis.discriminant_identity,
                        (n, base, exponent),
                    )
                    self.assertTrue(analysis.lucas_identity, (n, base, exponent))
                    checks += 1
        self.assertGreater(checks, 100_000)

    def test_squarefree_moduli_have_identical_raw_gcds(self) -> None:
        checks = 0
        for n in range(2, 201):
            if not is_squarefree(n):
                continue
            for base in range(1, n):
                if math.gcd(base, n) != 1:
                    continue
                for exponent in range(1, 13):
                    analysis = analyze_conjugate_pair(n, base, exponent)
                    self.assertEqual(
                        analysis.lucas_gcd,
                        analysis.multiplicative_gcd,
                        (n, base, exponent),
                    )
                    checks += 1
        self.assertGreater(checks, 50_000)

    def test_family_with_exponent_two_gets_no_derived_lucas_only_success(self) -> None:
        failures = 0
        for n in range(4, 201):
            if all(n % divisor for divisor in range(2, math.isqrt(n) + 1)):
                continue
            for base in range(1, n):
                if math.gcd(base, n) != 1:
                    continue
                multiplicative_success = False
                lucas_success = False
                for exponent in range(1, 13):
                    analysis = analyze_conjugate_pair(n, base, exponent)
                    multiplicative_success |= candidate_succeeds(
                        analysis.multiplicative
                    )
                    lucas_success |= candidate_succeeds(analysis.lucas)
                if lucas_success and not multiplicative_success:
                    failures += 1
        self.assertEqual(failures, 0)


if __name__ == "__main__":
    unittest.main()
