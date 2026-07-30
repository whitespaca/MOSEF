"""Exact branch and probability tests for the M84 total wrappers."""

from __future__ import annotations

import math
import random
import sys
import unittest
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

from mosef_reference import (
    BoundedFactorizationStatus,
    PromiseChannel,
    complete_unresolved_probability_bound,
    factor_nonsplit_lucas_bounded,
    factor_semismooth_bounded,
    is_prime,
    local_unresolved_probability_bound,
    promise_wrappers,
)


def constant(value: int):
    """Return a schedule with one public value at every bit length."""

    def schedule(_bit_length: int) -> int:
        return value

    return schedule


class ConstantSampler:
    """Deterministic boundary sampler for forced misses and collisions."""

    def __init__(self, value: int) -> None:
        self.value = value

    def randrange(self, stop: int) -> int:
        return self.value % stop


class SequenceSampler:
    """Return a declared sequence of residues for recursive branch tests."""

    def __init__(self, values: list[int]) -> None:
        self.values = iter(values)

    def randrange(self, stop: int) -> int:
        return next(self.values) % stop


class ProbabilityBoundTests(unittest.TestCase):
    def test_exact_local_tails(self) -> None:
        self.assertEqual(
            local_unresolved_probability_bound(
                PromiseChannel.SEMISMOOTH_P_MINUS_ONE,
                3,
            ),
            Fraction(343, 1728),
        )
        self.assertEqual(
            local_unresolved_probability_bound(
                PromiseChannel.NONSPLIT_LUCAS_P_PLUS_ONE,
                2,
            ),
            Fraction(121, 144),
        )

    def test_complete_union_bound_is_exactly_charged_and_capped(self) -> None:
        local = Fraction(7, 12) ** 20
        self.assertEqual(
            complete_unresolved_probability_bound(
                PromiseChannel.SEMISMOOTH_P_MINUS_ONE,
                20,
                10,
            ),
            40 * local,
        )
        self.assertEqual(
            complete_unresolved_probability_bound(
                PromiseChannel.NONSPLIT_LUCAS_P_PLUS_ONE,
                1,
                10,
            ),
            1,
        )

    def test_invalid_bound_domains_raise(self) -> None:
        with self.assertRaises(ValueError):
            local_unresolved_probability_bound(
                PromiseChannel.SEMISMOOTH_P_MINUS_ONE,
                0,
            )
        with self.assertRaises(ValueError):
            complete_unresolved_probability_bound(
                PromiseChannel.NONSPLIT_LUCAS_P_PLUS_ONE,
                1,
                0,
            )


class TotalWrapperTests(unittest.TestCase):
    def test_semismooth_success_and_forced_unresolved(self) -> None:
        success = factor_semismooth_bounded(
            51,
            constant(8),
            constant(1),
            8,
            random.Random(20260725),
        )
        self.assertEqual(success.status, BoundedFactorizationStatus.FACTORED)
        self.assertEqual(math.prod(success.factors), 51)
        self.assertIsNone(success.unresolved)

        unresolved = factor_semismooth_bounded(
            77,
            constant(1),
            constant(1),
            3,
            ConstantSampler(1),
        )
        self.assertEqual(
            unresolved.status,
            BoundedFactorizationStatus.UNRESOLVED,
        )
        self.assertEqual(unresolved.factors, ())
        self.assertEqual(unresolved.unresolved, 77)

    def test_nonsplit_success_and_forced_unresolved(self) -> None:
        success = factor_nonsplit_lucas_bounded(
            15,
            constant(2),
            constant(2),
            8,
            random.Random(20260731),
        )
        self.assertEqual(success.status, BoundedFactorizationStatus.FACTORED)
        self.assertEqual(math.prod(success.factors), 15)
        self.assertIsNone(success.unresolved)

        unresolved = factor_nonsplit_lucas_bounded(
            77,
            constant(1),
            constant(1),
            3,
            ConstantSampler(0),
        )
        self.assertEqual(
            unresolved.status,
            BoundedFactorizationStatus.UNRESOLVED,
        )
        self.assertEqual(unresolved.factors, ())
        self.assertEqual(unresolved.unresolved, 77)

    def test_preprocessing_is_total_on_units_primes_powers_and_even_inputs(self) -> None:
        cases = (
            (1, ()),
            (13, (13,)),
            (3**4, (3, 3, 3, 3)),
            (2**6, (2, 2, 2, 2, 2, 2)),
            (18, (2, 3, 3)),
        )
        wrappers = (factor_semismooth_bounded, factor_nonsplit_lucas_bounded)
        for wrapper in wrappers:
            for n, expected in cases:
                with self.subTest(wrapper=wrapper.__name__, n=n):
                    result = wrapper(
                        n,
                        constant(1),
                        constant(1),
                        1,
                        ConstantSampler(1),
                    )
                    self.assertEqual(
                        result.status,
                        BoundedFactorizationStatus.FACTORED,
                    )
                    self.assertEqual(result.factors, expected)
                    self.assertIsNone(result.unresolved)

    def test_every_reported_factorization_is_prime_and_exact(self) -> None:
        wrappers = (factor_semismooth_bounded, factor_nonsplit_lucas_bounded)
        for wrapper in wrappers:
            for n in range(1, 151):
                result = wrapper(
                    n,
                    constant(3),
                    constant(2),
                    2,
                    random.Random(10_000 + n),
                )
                with self.subTest(wrapper=wrapper.__name__, n=n):
                    if result.status == BoundedFactorizationStatus.FACTORED:
                        self.assertEqual(math.prod(result.factors), n)
                        self.assertTrue(all(is_prime(p) for p in result.factors))
                        self.assertIsNone(result.unresolved)
                    else:
                        self.assertEqual(result.factors, ())
                        self.assertIsNotNone(result.unresolved)
                        assert result.unresolved is not None
                        self.assertEqual(n % result.unresolved, 0)

    def test_partial_factors_are_discarded_when_later_child_is_unresolved(
        self,
    ) -> None:
        result = factor_semismooth_bounded(
            15 * 77,
            constant(1),
            constant(1),
            1,
            SequenceSampler([15, 3, 1]),
        )
        self.assertEqual(result.status, BoundedFactorizationStatus.UNRESOLVED)
        self.assertEqual(result.factors, ())
        self.assertEqual(result.unresolved, 77)

    def test_invalid_splitter_factor_is_rejected_before_recursion(self) -> None:
        with self.assertRaisesRegex(
            AssertionError,
            "splitter returned an invalid factor",
        ):
            promise_wrappers._factor_bounded(15, lambda _current: 4)

    def test_invalid_input_budget_and_schedule_raise(self) -> None:
        wrappers = (factor_semismooth_bounded, factor_nonsplit_lucas_bounded)
        for wrapper in wrappers:
            with self.subTest(
                wrapper=wrapper.__name__, case="input"
            ), self.assertRaises(ValueError):
                wrapper(
                    0,
                    constant(1),
                    constant(1),
                    1,
                    ConstantSampler(0),
                )
            with self.subTest(
                wrapper=wrapper.__name__, case="budget"
            ), self.assertRaises(ValueError):
                wrapper(
                    15,
                    constant(1),
                    constant(1),
                    0,
                    ConstantSampler(0),
                )
            with self.subTest(
                wrapper=wrapper.__name__, case="schedule"
            ), self.assertRaises(ValueError):
                wrapper(
                    15,
                    constant(0),
                    constant(1),
                    1,
                    ConstantSampler(0),
                )


if __name__ == "__main__":
    unittest.main()
