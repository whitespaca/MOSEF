"""Canonical-vector and edge-case tests for the Python semantic oracle."""

from __future__ import annotations

import json
import math
import random
import sys
import unittest
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

from mosef_reference import (
    batch_gcd,
    is_prime,
    lucas_v,
    mod_pow,
    perfect_power,
    pollard_p_minus_one,
    pollard_p_plus_one,
    pollard_rho,
    trial_division,
)


def load_vectors() -> dict[str, Any]:
    with (ROOT / "schemas" / "baseline-vectors-v1.json").open(encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise TypeError("baseline vectors must be a JSON object")
    return value


VECTORS = load_vectors()


def optional_integer(value: str | None) -> int | None:
    return None if value is None else int(value)


class BaselineVectorTests(unittest.TestCase):
    def test_modular_power_vectors(self) -> None:
        for vector in VECTORS["mod_pow"]:
            with self.subTest(vector=vector):
                self.assertEqual(
                    mod_pow(int(vector["base"]), int(vector["exponent"]), int(vector["modulus"])),
                    int(vector["result"]),
                )

    def test_primality_vectors(self) -> None:
        for vector in VECTORS["primality"]:
            with self.subTest(vector=vector):
                self.assertEqual(is_prime(int(vector["n"])), vector["result"])

    def test_trial_division_vectors(self) -> None:
        for vector in VECTORS["trial_division"]:
            with self.subTest(vector=vector):
                self.assertEqual(trial_division(int(vector["n"])), optional_integer(vector["factor"]))

    def test_perfect_power_vectors(self) -> None:
        for vector in VECTORS["perfect_power"]:
            expected = (
                None
                if vector["base"] is None
                else (int(vector["base"]), int(vector["exponent"]))
            )
            with self.subTest(vector=vector):
                self.assertEqual(perfect_power(int(vector["n"])), expected)

    def test_pollard_rho_vectors(self) -> None:
        for vector in VECTORS["pollard_rho"]:
            with self.subTest(vector=vector):
                self.assertEqual(
                    pollard_rho(
                        int(vector["n"]),
                        int(vector["seed"]),
                        int(vector["max_steps"]),
                    ),
                    optional_integer(vector["factor"]),
                )

    def test_pollard_p_minus_one_vectors(self) -> None:
        for vector in VECTORS["pollard_p_minus_one"]:
            with self.subTest(vector=vector):
                self.assertEqual(
                    pollard_p_minus_one(
                        int(vector["n"]),
                        int(vector["bound"]),
                        int(vector["base"]),
                    ),
                    optional_integer(vector["factor"]),
                )

    def test_pollard_p_plus_one_vectors(self) -> None:
        for vector in VECTORS["pollard_p_plus_one"]:
            with self.subTest(vector=vector):
                self.assertEqual(
                    pollard_p_plus_one(
                        int(vector["n"]),
                        int(vector["bound"]),
                        int(vector["parameter"]),
                    ),
                    optional_integer(vector["factor"]),
                )

    def test_batch_gcd_vectors(self) -> None:
        for vector in VECTORS["batch_gcd"]:
            with self.subTest(vector=vector):
                self.assertEqual(
                    batch_gcd([int(value) for value in vector["values"]], int(vector["modulus"])),
                    [int(value) for value in vector["results"]],
                )


class BaselineEdgeCaseTests(unittest.TestCase):
    def test_invalid_modular_inputs_raise(self) -> None:
        with self.assertRaises(ValueError):
            mod_pow(2, -1, 5)
        with self.assertRaises(ValueError):
            mod_pow(2, 3, 0)
        with self.assertRaises(ValueError):
            batch_gcd([1], 0)

    def test_lucas_matrix_matches_recurrence(self) -> None:
        parameter = 4
        modulus = 667
        recurrence = [2, parameter]
        for _ in range(2, 20):
            recurrence.append((parameter * recurrence[-1] - recurrence[-2]) % modulus)
        self.assertEqual(
            [lucas_v(index, parameter, modulus) for index in range(20)],
            [value % modulus for value in recurrence],
        )

    def test_reported_factors_are_nontrivial_divisors(self) -> None:
        cases = (
            (8051, pollard_rho(8051, 0, 10_000)),
            (10807, pollard_p_minus_one(10807, 25, 2)),
            (667, pollard_p_plus_one(667, 5, 4)),
        )
        for n, factor in cases:
            with self.subTest(n=n, factor=factor):
                self.assertIsNotNone(factor)
                assert factor is not None
                self.assertGreater(factor, 1)
                self.assertLess(factor, n)
                self.assertEqual(n % factor, 0)


class BaselineDeterministicPropertyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.random = random.Random(0x4D4F534546)

    def test_modular_power_matches_builtin(self) -> None:
        for _ in range(200):
            base = self.random.randrange(0, 1 << 64)
            exponent = self.random.randrange(0, 1_000)
            modulus = self.random.randrange(1, 1 << 64)
            self.assertEqual(mod_pow(base, exponent, modulus), pow(base, exponent, modulus))

    def test_batch_gcd_matches_scalar_oracle(self) -> None:
        for _ in range(100):
            modulus = self.random.randrange(1, 1 << 32)
            values = [self.random.randrange(0, 1 << 64) for _ in range(16)]
            self.assertEqual(batch_gcd(values, modulus), [math.gcd(value, modulus) for value in values])

    def test_generated_perfect_powers_reconstruct(self) -> None:
        for _ in range(100):
            base = self.random.randrange(2, 100)
            exponent = self.random.randrange(2, 12)
            n = base**exponent
            result = perfect_power(n)
            self.assertIsNotNone(result)
            assert result is not None
            self.assertEqual(result[0] ** result[1], n)
            self.assertGreaterEqual(result[1], exponent)

    def test_trial_factor_is_least_divisor(self) -> None:
        for n in range(2, 5_000):
            factor = trial_division(n)
            candidates = [candidate for candidate in range(2, n) if n % candidate == 0]
            expected = candidates[0] if candidates else None
            self.assertEqual(factor, expected)


if __name__ == "__main__":
    unittest.main()
