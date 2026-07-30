"""Bounded total wrappers for the two hereditary promise algorithms.

This module is an exact small-input semantic reference.  Its trial-division
primality oracle is not the polynomial-time primality implementation assumed
by the paper theorem.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum
from fractions import Fraction

from .baseline import is_prime, perfect_power
from .multigroup import candidate_succeeds, evaluate_lucas_candidate
from .semismooth import (
    ResidueSampler,
    stage_one_exponent,
    try_randomized_semismooth_factor,
)

BoundSchedule = Callable[[int], int]


class PromiseChannel(str, Enum):
    """The two randomized promise channels."""

    SEMISMOOTH_P_MINUS_ONE = "semismooth_p_minus_one"
    NONSPLIT_LUCAS_P_PLUS_ONE = "nonsplit_lucas_p_plus_one"


class BoundedFactorizationStatus(str, Enum):
    """Exhaustive public outcomes of a bounded total wrapper."""

    FACTORED = "factored"
    UNRESOLVED = "unresolved"


@dataclass(frozen=True)
class BoundedFactorizationResult:
    """A complete exact factorization or an explicit unresolved node."""

    status: BoundedFactorizationStatus
    factors: tuple[int, ...]
    unresolved: int | None


def _positive_schedule_value(schedule: BoundSchedule, bit_length: int) -> int:
    value = schedule(bit_length)
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise ValueError("schedule values must be positive integers")
    return value


def _validate_budget(n: int, cycles_per_node: int) -> None:
    if n < 1:
        raise ValueError("n must be positive")
    if (
        isinstance(cycles_per_node, bool)
        or not isinstance(cycles_per_node, int)
        or cycles_per_node < 1
    ):
        raise ValueError("cycles_per_node must be a positive integer")


def local_unresolved_probability_bound(
    channel: PromiseChannel,
    cycles_per_node: int,
) -> Fraction:
    """Return the exact proved on-promise tail after a local cycle budget."""
    _validate_budget(1, cycles_per_node)
    if channel == PromiseChannel.SEMISMOOTH_P_MINUS_ONE:
        return Fraction(7, 12) ** cycles_per_node
    if channel == PromiseChannel.NONSPLIT_LUCAS_P_PLUS_ONE:
        return Fraction(11, 12) ** cycles_per_node
    raise ValueError("unknown promise channel")


def complete_unresolved_probability_bound(
    channel: PromiseChannel,
    cycles_per_node: int,
    input_bit_length: int,
) -> Fraction:
    """Return the conservative hereditary-recursion union bound.

    Maximal-perfect-power preprocessing and binary splitting use fewer than
    ``4 * input_bit_length`` invocations.  The bound is meaningful only on the
    corresponding hereditary promise.
    """
    if (
        isinstance(input_bit_length, bool)
        or not isinstance(input_bit_length, int)
        or input_bit_length < 1
    ):
        raise ValueError("input_bit_length must be a positive integer")
    local = local_unresolved_probability_bound(channel, cycles_per_node)
    return min(Fraction(1), 4 * input_bit_length * local)


def _factor_bounded(
    n: int,
    split: Callable[[int], int | None],
) -> BoundedFactorizationResult:
    if n == 1:
        return BoundedFactorizationResult(
            BoundedFactorizationStatus.FACTORED,
            (),
            None,
        )
    if is_prime(n):
        return BoundedFactorizationResult(
            BoundedFactorizationStatus.FACTORED,
            (n,),
            None,
        )

    power = perfect_power(n)
    if power is not None:
        base, exponent = power
        base_result = _factor_bounded(base, split)
        if base_result.status == BoundedFactorizationStatus.UNRESOLVED:
            return base_result
        return BoundedFactorizationResult(
            BoundedFactorizationStatus.FACTORED,
            tuple(sorted(base_result.factors * exponent)),
            None,
        )

    if n % 2 == 0:
        right = _factor_bounded(n // 2, split)
        if right.status == BoundedFactorizationStatus.UNRESOLVED:
            return right
        return BoundedFactorizationResult(
            BoundedFactorizationStatus.FACTORED,
            tuple(sorted((2,) + right.factors)),
            None,
        )

    factor = split(n)
    if factor is None:
        return BoundedFactorizationResult(
            BoundedFactorizationStatus.UNRESOLVED,
            (),
            n,
        )
    if factor <= 1 or factor >= n or n % factor != 0:
        raise AssertionError("splitter returned an invalid factor")

    left = _factor_bounded(factor, split)
    if left.status == BoundedFactorizationStatus.UNRESOLVED:
        return left
    right = _factor_bounded(n // factor, split)
    if right.status == BoundedFactorizationStatus.UNRESOLVED:
        return right
    return BoundedFactorizationResult(
        BoundedFactorizationStatus.FACTORED,
        tuple(sorted(left.factors + right.factors)),
        None,
    )


def factor_semismooth_bounded(
    n: int,
    smooth_bound: BoundSchedule,
    cofactor_bound: BoundSchedule,
    cycles_per_node: int,
    rng: ResidueSampler,
) -> BoundedFactorizationResult:
    """Run the bounded hereditary ``p-1`` wrapper on any positive input."""
    _validate_budget(n, cycles_per_node)

    def split(current: int) -> int | None:
        bit_length = current.bit_length()
        bound = _positive_schedule_value(smooth_bound, bit_length)
        cofactor = _positive_schedule_value(cofactor_bound, bit_length)
        result = try_randomized_semismooth_factor(
            current,
            bound,
            cofactor,
            rng,
            cycles_per_node,
        )
        return None if result is None else result.factor

    return _factor_bounded(n, split)


def _try_randomized_nonsplit_factor(
    n: int,
    smooth_bound: int,
    cofactor_bound: int,
    cycles_per_node: int,
    rng: ResidueSampler,
) -> int | None:
    if n < 3 or n % 2 == 0:
        raise ValueError("n must be an odd integer at least 3")
    stage_exponent = stage_one_exponent(smooth_bound)
    for _ in range(cycles_per_node):
        for multiplier in range(1, cofactor_bound + 1):
            exponent = multiplier * stage_exponent
            parameter = rng.randrange(n)
            outcome = evaluate_lucas_candidate(n, parameter, exponent)
            if not candidate_succeeds(outcome):
                continue
            if outcome.factor is None:
                raise AssertionError("successful Lucas outcome lacks a factor")
            if not 1 < outcome.factor < n or n % outcome.factor != 0:
                raise AssertionError("Lucas candidate returned an invalid factor")
            return outcome.factor
    return None


def factor_nonsplit_lucas_bounded(
    n: int,
    smooth_bound: BoundSchedule,
    cofactor_bound: BoundSchedule,
    cycles_per_node: int,
    rng: ResidueSampler,
) -> BoundedFactorizationResult:
    """Run the bounded hereditary nonsplit ``p+1`` wrapper on any input."""
    _validate_budget(n, cycles_per_node)

    def split(current: int) -> int | None:
        bit_length = current.bit_length()
        bound = _positive_schedule_value(smooth_bound, bit_length)
        cofactor = _positive_schedule_value(cofactor_bound, bit_length)
        return _try_randomized_nonsplit_factor(
            current,
            bound,
            cofactor,
            cycles_per_node,
            rng,
        )

    return _factor_bounded(n, split)
