"""Exact and adversarial tests for the M7 nonsplit Lucas theorem."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

from mosef_reference import (  # noqa: E402
    LucasAsymmetryWitness,
    candidate_succeeds,
    direct_lucas_root_count,
    direct_witness_event_count,
    evaluate_lucas_candidate,
    is_lucas_asymmetry_witness,
    is_prime,
    lucas_root_count,
    lucas_split_success_count,
    nondegenerate_lucas_collision_count,
    nonsplit_parameter_count,
    witness_event_count,
    witness_event_holds,
)


class LucasRootCountTests(unittest.TestCase):
    def test_formula_matches_direct_enumeration(self) -> None:
        checks = 0
        for prime in range(3, 98, 2):
            if not is_prime(prime):
                continue
            for exponent in range(1, 65):
                self.assertEqual(
                    lucas_root_count(prime, exponent),
                    direct_lucas_root_count(prime, exponent),
                    (prime, exponent),
                )
                checks += 1
        self.assertGreater(checks, 1_000)

    def test_nonsplit_parameter_count(self) -> None:
        for prime in range(3, 150, 2):
            if is_prime(prime):
                self.assertEqual(
                    nonsplit_parameter_count(prime),
                    (prime - 1) // 2,
                    prime,
                )

    def test_degenerate_root_subtraction(self) -> None:
        self.assertEqual(nondegenerate_lucas_collision_count(7, 1), 0)
        self.assertEqual(nondegenerate_lucas_collision_count(7, 2), 0)
        self.assertEqual(nondegenerate_lucas_collision_count(7, 6), 2)

    def test_invalid_domains_raise(self) -> None:
        calls = (
            lambda: lucas_root_count(2, 1),
            lambda: lucas_root_count(9, 1),
            lambda: lucas_root_count(7, 0),
            lambda: nonsplit_parameter_count(15),
            lambda: is_lucas_asymmetry_witness(3, 3, 4),
            lambda: is_lucas_asymmetry_witness(3, 5, 0),
        )
        for call in calls:
            with self.subTest(call=call):
                with self.assertRaises(ValueError):
                    call()


class LucasAsymmetryWitnessTests(unittest.TestCase):
    def test_formula_event_and_one_twelfth_bound(self) -> None:
        checks = 0
        primes = [value for value in range(3, 44, 2) if is_prime(value)]
        for p in primes:
            for q in primes:
                if p == q:
                    continue
                for exponent in range(1, 81):
                    if not is_lucas_asymmetry_witness(p, q, exponent):
                        continue
                    witness = LucasAsymmetryWitness(p, q, exponent)
                    formula = witness_event_count(witness)
                    direct = direct_witness_event_count(witness)
                    self.assertEqual(formula, direct, witness)
                    self.assertGreaterEqual(12 * formula, p * q, witness)
                    self.assertGreaterEqual(
                        lucas_split_success_count(p * q, exponent),
                        formula,
                        witness,
                    )
                    checks += 1
        self.assertGreater(checks, 500)

    def test_every_counted_parameter_succeeds_on_adversarial_moduli(self) -> None:
        cases = (
            (15, LucasAsymmetryWitness(3, 5, 4)),
            (35, LucasAsymmetryWitness(5, 7, 6)),
            (45, LucasAsymmetryWitness(3, 5, 4)),
            (75, LucasAsymmetryWitness(3, 5, 4)),
            (105, LucasAsymmetryWitness(3, 5, 4)),
            (30, LucasAsymmetryWitness(3, 5, 4)),
        )
        checks = 0
        for modulus, witness in cases:
            for parameter in range(modulus):
                if not witness_event_holds(modulus, witness, parameter):
                    continue
                self.assertTrue(
                    candidate_succeeds(
                        evaluate_lucas_candidate(
                            modulus,
                            parameter,
                            witness.exponent,
                        )
                    ),
                    (modulus, witness, parameter),
                )
                checks += 1
        self.assertGreater(checks, 20)

    def test_nonwitness_is_rejected(self) -> None:
        invalid = LucasAsymmetryWitness(3, 5, 12)
        with self.assertRaises(ValueError):
            witness_event_count(invalid)
        with self.assertRaises(ValueError):
            witness_event_holds(15, invalid, 0)


if __name__ == "__main__":
    unittest.main()
