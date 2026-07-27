"""Exact and adversarial tests for the M3 semismooth promise theorem."""

from __future__ import annotations

import math
import random
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

from mosef_reference import (
    factor_semismooth_oracle,
    factor_semismooth_promised,
    find_semismooth_asymmetry_witness,
    find_semismooth_witness,
    is_hereditarily_semismooth_asymmetric,
    is_hereditarily_semismooth_separable,
    semismooth_asymmetry_witnesses,
    stage_one_exponent,
    successful_residue_count,
    try_randomized_semismooth_factor,
    try_semismooth_factor,
)


class SemismoothDefinitionTests(unittest.TestCase):
    def test_stage_one_exponents(self) -> None:
        self.assertEqual(stage_one_exponent(1), 1)
        self.assertEqual(stage_one_exponent(5), 60)
        self.assertEqual(stage_one_exponent(8), 840)

    def test_basic_promised_separator(self) -> None:
        witness = find_semismooth_witness(15, 2, 2, 1)
        self.assertIsNotNone(witness)
        assert witness is not None
        self.assertEqual((witness.p, witness.q), (3, 5))
        result = try_semismooth_factor(15, 2, 2, 1)
        self.assertIsNotNone(result)
        assert result is not None
        self.assertEqual(result.factor, 3)

    def test_q_minus_one_nondivisibility_is_not_enough(self) -> None:
        exponent = stage_one_exponent(8)
        self.assertEqual(exponent, 840)
        self.assertEqual(exponent % (3 - 1), 0)
        self.assertNotEqual(exponent % (17 - 1), 0)
        self.assertEqual(pow(2, exponent, 17), 1)
        self.assertEqual(math.gcd(pow(2, exponent, 51) - 1, 51), 51)
        self.assertIsNone(try_semismooth_factor(51, 2, 8, 1))
        witness = find_semismooth_asymmetry_witness(51, 8, 1)
        self.assertIsNotNone(witness)
        assert witness is not None
        self.assertEqual((witness.p, witness.q, witness.exponent), (3, 17, 840))
        self.assertGreaterEqual(successful_residue_count(51, 840), 17)

    def test_exact_success_bound_for_witnesses(self) -> None:
        checked = 0
        for n in range(6, 301):
            for witness in semismooth_asymmetry_witnesses(n, 8, 3):
                checked += 1
                self.assertGreaterEqual(
                    12 * successful_residue_count(n, witness.exponent),
                    5 * n,
                    (n, witness),
                )
        self.assertGreater(checked, 0)

    def test_seeded_randomized_split_is_reproducible(self) -> None:
        first = try_randomized_semismooth_factor(
            51,
            8,
            1,
            random.Random(20260725),
            8,
        )
        second = try_randomized_semismooth_factor(
            51,
            8,
            1,
            random.Random(20260725),
            8,
        )
        self.assertEqual(first, second)
        self.assertIsNotNone(first)

    def test_direct_factor_and_unresolved_paths(self) -> None:
        direct = try_semismooth_factor(21, 3, 3, 1)
        self.assertIsNotNone(direct)
        assert direct is not None
        self.assertEqual(direct.factor, 3)
        self.assertIsNone(try_semismooth_factor(21, 2, 3, 1))

    def test_invalid_domains_raise(self) -> None:
        calls = (
            lambda: stage_one_exponent(0),
            lambda: try_semismooth_factor(1, 2, 2, 1),
            lambda: try_semismooth_factor(15, 1, 2, 1),
            lambda: find_semismooth_witness(15, 2, 0, 1),
            lambda: find_semismooth_asymmetry_witness(15, 0, 1),
            lambda: factor_semismooth_promised(0, 2, 2, 1),
            lambda: successful_residue_count(1, 1),
        )
        for call in calls:
            with self.subTest(call=call), self.assertRaises(ValueError):
                call()


class SemismoothExhaustiveTests(unittest.TestCase):
    def test_promised_inputs_factor_completely(self) -> None:
        promised = 0
        for n in range(4, 301):
            if not is_hereditarily_semismooth_separable(n, 5, 8, 3):
                continue
            promised += 1
            factors = factor_semismooth_promised(n, 5, 8, 3)
            self.assertIsNotNone(factors, n)
            assert factors is not None
            self.assertEqual(math.prod(factors), n)
        self.assertGreater(promised, 0)

    def test_asymmetric_promised_inputs_factor_with_exhaustive_oracle(self) -> None:
        promised = 0
        for n in range(4, 301):
            if not is_hereditarily_semismooth_asymmetric(n, 8, 3):
                continue
            promised += 1
            factors = factor_semismooth_oracle(n, 8, 3)
            self.assertIsNotNone(factors, n)
            assert factors is not None
            self.assertEqual(math.prod(factors), n)
        self.assertGreater(promised, 0)


if __name__ == "__main__":
    unittest.main()
