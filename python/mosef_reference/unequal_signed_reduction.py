"""Exact unequal depth-two signed reductions for M23."""

from __future__ import annotations

from dataclasses import dataclass
from functools import cache
from math import gcd

from .geometric_sum import evaluate_geometric_sum


@dataclass(frozen=True)
class UnequalSignedReductionEvaluation:
    """Evaluate ``c1*S_A(g) + c2*S_B(g**A)`` and its M23 reductions."""

    base: int
    modulus: int
    first_factor: int
    second_factor: int
    first_coefficient: int
    second_coefficient: int
    first_quotient_residue: int
    second_quotient_residue: int
    first_quotient_gcd: int
    second_quotient_gcd: int
    aggregate_residue: int
    aggregate_gcd: int
    first_quotient_status: str
    rational_reduction_residue: int | None
    rational_reduction_gcd: int | None
    public_full_residue: int
    public_full_gcd: int
    common_stage_gcd: int
    multiplier_gcd: int
    has_x_factor: bool
    has_x_minus_one_factor: bool
    formal_degree: int
    collected_monomial_count: int
    common_step: int
    difference_residue: int
    difference_gcd: int
    common_factor_residue: int
    common_factor_gcd: int
    difference_cofactor_residue: int | None
    difference_cofactor_gcd: int | None
    difference_cofactor_degree: int


def _validate_factor(value: int, name: str) -> None:
    if isinstance(value, bool) or not isinstance(value, int) or value < 2:
        raise ValueError(f"{name} must be an integer at least two")


def _monic_divide(
    dividend: tuple[int, ...], divisor: tuple[int, ...]
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    remainder = list(dividend)
    quotient = [0] * max(1, len(dividend) - len(divisor) + 1)
    while len(remainder) >= len(divisor) and any(remainder):
        leading = remainder[-1]
        offset = len(remainder) - len(divisor)
        quotient[offset] = leading
        for index, coefficient in enumerate(divisor):
            remainder[offset + index] -= leading * coefficient
        while len(remainder) > 1 and remainder[-1] == 0:
            remainder.pop()
    return tuple(quotient), tuple(remainder)


@cache
def unequal_difference_coefficients(
    first_factor: int, second_factor: int
) -> tuple[int, ...]:
    """Return coefficients of ``S_B(X**A) - S_A(X)`` in ascending degree."""
    _validate_factor(first_factor, "first_factor")
    _validate_factor(second_factor, "second_factor")
    if first_factor == second_factor:
        raise ValueError("factors must be unequal")
    degree = first_factor * (second_factor - 1)
    coefficients = [0] * (degree + 1)
    for exponent in range(first_factor):
        coefficients[exponent] -= 1
    for index in range(second_factor):
        coefficients[first_factor * index] += 1
    return tuple(coefficients)


@cache
def unequal_difference_cofactor_coefficients(
    first_factor: int, second_factor: int
) -> tuple[int, ...]:
    """Return the exact cofactor after removing ``X*S_h(X)``."""
    difference = unequal_difference_coefficients(first_factor, second_factor)
    if difference[0] != 0:
        raise AssertionError("unequal difference must have zero constant term")
    common_step = gcd(first_factor - 1, second_factor - 1)
    quotient, remainder = _monic_divide(
        difference[1:],
        (1,) * common_step,
    )
    if any(remainder):
        raise AssertionError("common-step factor division was not exact")
    return quotient


def _evaluate_coefficients(
    coefficients: tuple[int, ...], base: int, modulus: int
) -> int:
    value = 0
    for coefficient in reversed(coefficients):
        value = (value * base + coefficient) % modulus
    return value


def evaluate_unequal_signed_reduction(
    base: int,
    modulus: int,
    first_factor: int,
    second_factor: int,
    first_coefficient: int,
    second_coefficient: int,
) -> UnequalSignedReductionEvaluation:
    """Evaluate the general signed form and normalized unequal difference."""
    _validate_factor(first_factor, "first_factor")
    _validate_factor(second_factor, "second_factor")
    if first_factor == second_factor:
        raise ValueError("factors must be unequal")
    for value, name in (
        (first_coefficient, "first_coefficient"),
        (second_coefficient, "second_coefficient"),
    ):
        if isinstance(value, bool) or not isinstance(value, int) or value == 0:
            raise ValueError(f"{name} must be a nonzero integer")

    first = evaluate_geometric_sum(base, modulus, first_factor)
    second = evaluate_geometric_sum(
        first.power_residue,
        modulus,
        second_factor,
    )
    first_gcd = first.sum_gcd
    second_gcd = second.sum_gcd
    aggregate = (
        first_coefficient * first.sum_residue
        + second_coefficient * second.sum_residue
    ) % modulus
    if first_gcd == 1:
        status = "unit"
        rational = (
            first_coefficient
            + second_coefficient
            * second.sum_residue
            * pow(first.sum_residue, -1, modulus)
        ) % modulus
        if aggregate != first.sum_residue * rational % modulus:
            raise AssertionError("unit-prefix rational reduction failed")
        rational_gcd: int | None = gcd(rational, modulus)
    elif first_gcd < modulus:
        status = "proper_factor"
        rational = None
        rational_gcd = None
    else:
        status = "full_collision"
        rational = None
        rational_gcd = None

    public_full = second_coefficient * second_factor % modulus
    if status == "full_collision":
        if second.sum_residue != second_factor % modulus:
            raise AssertionError("full prefix did not reduce the second stage")
        if aggregate != public_full:
            raise AssertionError("full-prefix public reduction failed")

    common_stage_gcd = gcd(first.sum_residue, second.sum_residue, modulus)
    multiplier_gcd = gcd(second_factor, modulus)
    if multiplier_gcd % common_stage_gcd != 0:
        raise AssertionError("common stage divisor did not divide multiplier")

    common_step = gcd(first_factor - 1, second_factor - 1)
    common_sum = evaluate_geometric_sum(base, modulus, common_step)
    common_factor = first.base * common_sum.sum_residue % modulus
    common_factor_gcd = gcd(common_factor, modulus)
    difference = (second.sum_residue - first.sum_residue) % modulus
    cofactor_coefficients = unequal_difference_cofactor_coefficients(
        first_factor,
        second_factor,
    )
    expanded_cofactor = _evaluate_coefficients(
        cofactor_coefficients,
        first.base,
        modulus,
    )
    if difference != common_factor * expanded_cofactor % modulus:
        raise AssertionError("unequal common-step factorization failed")
    if common_factor_gcd == 1:
        difference_cofactor = (
            difference * pow(common_factor, -1, modulus) % modulus
        )
        if difference_cofactor != expanded_cofactor:
            raise AssertionError("unit common-factor division failed")
        difference_cofactor_gcd: int | None = gcd(
            difference_cofactor, modulus
        )
    else:
        difference_cofactor = None
        difference_cofactor_gcd = None

    return UnequalSignedReductionEvaluation(
        base=first.base,
        modulus=modulus,
        first_factor=first_factor,
        second_factor=second_factor,
        first_coefficient=first_coefficient,
        second_coefficient=second_coefficient,
        first_quotient_residue=first.sum_residue,
        second_quotient_residue=second.sum_residue,
        first_quotient_gcd=first_gcd,
        second_quotient_gcd=second_gcd,
        aggregate_residue=aggregate,
        aggregate_gcd=gcd(aggregate, modulus),
        first_quotient_status=status,
        rational_reduction_residue=rational,
        rational_reduction_gcd=rational_gcd,
        public_full_residue=public_full,
        public_full_gcd=gcd(public_full, modulus),
        common_stage_gcd=common_stage_gcd,
        multiplier_gcd=multiplier_gcd,
        has_x_factor=first_coefficient + second_coefficient == 0,
        has_x_minus_one_factor=(
            first_coefficient * first_factor
            + second_coefficient * second_factor
            == 0
        ),
        formal_degree=first_factor * (second_factor - 1),
        collected_monomial_count=(
            first_factor
            + second_factor
            - 2
            if first_coefficient + second_coefficient == 0
            else first_factor + second_factor - 1
        ),
        common_step=common_step,
        difference_residue=difference,
        difference_gcd=gcd(difference, modulus),
        common_factor_residue=common_factor,
        common_factor_gcd=common_factor_gcd,
        difference_cofactor_residue=difference_cofactor,
        difference_cofactor_gcd=difference_cofactor_gcd,
        difference_cofactor_degree=(
            first_factor * (second_factor - 1) - common_step - 1
        ),
    )
