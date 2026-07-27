"""Exact content, resultant, and cyclotomic audits for M24."""

from __future__ import annotations

from dataclasses import dataclass
from functools import cache
from math import gcd

from .geometric_sum import evaluate_geometric_sum


@dataclass(frozen=True)
class RationalResidueAuditEvaluation:
    """Evaluate the normalized numerator and public stage-overlap bounds."""

    base: int
    modulus: int
    first_factor: int
    second_factor: int
    first_coefficient: int
    second_coefficient: int
    content: int
    primitive_first_coefficient: int
    primitive_second_coefficient: int
    content_gcd: int
    content_status: str
    first_quotient_residue: int
    second_quotient_residue: int
    first_quotient_gcd: int
    second_quotient_gcd: int
    aggregate_residue: int
    aggregate_gcd: int
    primitive_aggregate_residue: int
    primitive_aggregate_gcd: int
    prefix_status: str
    rational_residue: int | None
    rational_gcd: int | None
    primitive_rational_residue: int | None
    primitive_rational_gcd: int | None
    first_overlap_gcd: int
    first_public_bound_gcd: int
    second_overlap_gcd: int
    second_public_bound_gcd: int
    first_resultant_base: int
    first_resultant_exponent: int
    second_resultant_coefficient_base: int
    second_resultant_coefficient_exponent: int
    second_resultant_stage_base: int
    second_resultant_stage_exponent: int


def _validate_factor(value: int, name: str) -> None:
    if isinstance(value, bool) or not isinstance(value, int) or value < 2:
        raise ValueError(f"{name} must be an integer at least two")


def _validate_coefficient(value: int, name: str) -> None:
    if isinstance(value, bool) or not isinstance(value, int) or value == 0:
        raise ValueError(f"{name} must be a nonzero integer")


def _status(value: int, modulus: int) -> str:
    if value == 1:
        return "unit"
    if value < modulus:
        return "proper_factor"
    return "full_collision"


def _trim(coefficients: list[int]) -> tuple[int, ...]:
    while len(coefficients) > 1 and coefficients[-1] == 0:
        coefficients.pop()
    return tuple(coefficients)


def polynomial_multiply(
    left: tuple[int, ...], right: tuple[int, ...]
) -> tuple[int, ...]:
    """Multiply ascending integer coefficient vectors."""
    result = [0] * (len(left) + len(right) - 1)
    for left_index, left_value in enumerate(left):
        for right_index, right_value in enumerate(right):
            result[left_index + right_index] += left_value * right_value
    return _trim(result)


def monic_polynomial_divide(
    dividend: tuple[int, ...], divisor: tuple[int, ...]
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    """Divide by a monic integer polynomial, returning quotient and remainder."""
    if not divisor or divisor[-1] != 1:
        raise ValueError("divisor must be monic")
    remainder = list(dividend)
    quotient = [0] * max(1, len(dividend) - len(divisor) + 1)
    while len(remainder) >= len(divisor) and any(remainder):
        multiplier = remainder[-1]
        offset = len(remainder) - len(divisor)
        quotient[offset] = multiplier
        for index, value in enumerate(divisor):
            remainder[offset + index] -= multiplier * value
        remainder = list(_trim(remainder))
    return _trim(quotient), _trim(remainder)


@cache
def _cyclotomic_coefficients_cached(order: int) -> tuple[int, ...]:
    polynomial = (-1,) + (0,) * (order - 1) + (1,)
    for divisor in range(1, order):
        if order % divisor:
            continue
        polynomial, remainder = monic_polynomial_divide(
            polynomial,
            _cyclotomic_coefficients_cached(divisor),
        )
        if any(remainder):
            raise AssertionError("cyclotomic recursion was not exact")
    return polynomial


def cyclotomic_coefficients(order: int) -> tuple[int, ...]:
    """Return ascending coefficients of the exact cyclotomic polynomial."""
    if isinstance(order, bool) or not isinstance(order, int) or order < 1:
        raise ValueError("order must be a positive integer")
    return _cyclotomic_coefficients_cached(order)


def signed_numerator_coefficients(
    first_factor: int,
    second_factor: int,
    first_coefficient: int,
    second_coefficient: int,
) -> tuple[int, ...]:
    """Return coefficients of ``c1*S_A(X)+c2*S_B(X**A)``."""
    _validate_factor(first_factor, "first_factor")
    _validate_factor(second_factor, "second_factor")
    if first_factor == second_factor:
        raise ValueError("factors must be unequal")
    _validate_coefficient(first_coefficient, "first_coefficient")
    _validate_coefficient(second_coefficient, "second_coefficient")
    degree = first_factor * (second_factor - 1)
    coefficients = [0] * (degree + 1)
    for exponent in range(first_factor):
        coefficients[exponent] += first_coefficient
    for index in range(second_factor):
        coefficients[first_factor * index] += second_coefficient
    return _trim(coefficients)


def cleared_root_of_unity_coefficients(
    first_factor: int,
    second_factor: int,
    first_coefficient: int,
    second_coefficient: int,
) -> tuple[int, ...]:
    """Return ``c1(X^A-1)^2+c2(X-1)(X^(AB)-1)``."""
    _validate_factor(first_factor, "first_factor")
    _validate_factor(second_factor, "second_factor")
    if first_factor == second_factor:
        raise ValueError("factors must be unequal")
    _validate_coefficient(first_coefficient, "first_coefficient")
    _validate_coefficient(second_coefficient, "second_coefficient")
    first_endpoint = (-1,) + (0,) * (first_factor - 1) + (1,)
    full_endpoint = (
        (-1,)
        + (0,) * (first_factor * second_factor - 1)
        + (1,)
    )
    first_term = [
        first_coefficient * value
        for value in polynomial_multiply(first_endpoint, first_endpoint)
    ]
    second_term = [
        second_coefficient * value
        for value in polynomial_multiply((-1, 1), full_endpoint)
    ]
    result = [0] * max(len(first_term), len(second_term))
    for index, value in enumerate(first_term):
        result[index] += value
    for index, value in enumerate(second_term):
        result[index] += value
    return _trim(result)


def cyclotomic_factor_orders(
    first_factor: int,
    second_factor: int,
    first_coefficient: int,
    second_coefficient: int,
    order_max: int,
) -> tuple[int, ...]:
    """Enumerate exact cyclotomic divisors up to an explicit order bound."""
    if (
        isinstance(order_max, bool)
        or not isinstance(order_max, int)
        or order_max < 1
    ):
        raise ValueError("order_max must be a positive integer")
    numerator = signed_numerator_coefficients(
        first_factor,
        second_factor,
        first_coefficient,
        second_coefficient,
    )
    orders: list[int] = []
    for order in range(1, order_max + 1):
        _, remainder = monic_polynomial_divide(
            numerator,
            cyclotomic_coefficients(order),
        )
        if not any(remainder):
            orders.append(order)
    return tuple(orders)


def evaluate_rational_residue_audit(
    base: int,
    modulus: int,
    first_factor: int,
    second_factor: int,
    first_coefficient: int,
    second_coefficient: int,
) -> RationalResidueAuditEvaluation:
    """Evaluate the M24 content and stage-resultant isolation theorem."""
    _validate_factor(first_factor, "first_factor")
    _validate_factor(second_factor, "second_factor")
    if first_factor == second_factor:
        raise ValueError("factors must be unequal")
    for value, name in (
        (first_coefficient, "first_coefficient"),
        (second_coefficient, "second_coefficient"),
    ):
        _validate_coefficient(value, name)

    first = evaluate_geometric_sum(base, modulus, first_factor)
    second = evaluate_geometric_sum(
        first.power_residue,
        modulus,
        second_factor,
    )
    content = gcd(abs(first_coefficient), abs(second_coefficient))
    primitive_first = first_coefficient // content
    primitive_second = second_coefficient // content
    content_gcd = gcd(content, modulus)
    aggregate = (
        first_coefficient * first.sum_residue
        + second_coefficient * second.sum_residue
    ) % modulus
    primitive_aggregate = (
        primitive_first * first.sum_residue
        + primitive_second * second.sum_residue
    ) % modulus
    if aggregate != content * primitive_aggregate % modulus:
        raise AssertionError("coefficient-content normalization failed")

    prefix_status = _status(first.sum_gcd, modulus)
    if prefix_status == "unit":
        inverse = pow(first.sum_residue, -1, modulus)
        rational = (
            first_coefficient
            + second_coefficient * second.sum_residue * inverse
        ) % modulus
        primitive_rational = (
            primitive_first
            + primitive_second * second.sum_residue * inverse
        ) % modulus
        if (
            aggregate != first.sum_residue * rational % modulus
            or primitive_aggregate
            != first.sum_residue * primitive_rational % modulus
        ):
            raise AssertionError("unit-prefix rational reduction failed")
        rational_gcd: int | None = gcd(rational, modulus)
        primitive_rational_gcd: int | None = gcd(
            primitive_rational,
            modulus,
        )
    else:
        rational = None
        rational_gcd = None
        primitive_rational = None
        primitive_rational_gcd = None

    first_overlap = gcd(first.sum_residue, aggregate, modulus)
    first_bound = gcd(second_coefficient * second_factor, modulus)
    second_overlap = gcd(second.sum_residue, aggregate, modulus)
    second_bound = gcd(first_coefficient * second_factor, modulus)
    if first_bound % first_overlap or second_bound % second_overlap:
        raise AssertionError("stage overlap escaped its public resultant bound")

    return RationalResidueAuditEvaluation(
        base=first.base,
        modulus=modulus,
        first_factor=first_factor,
        second_factor=second_factor,
        first_coefficient=first_coefficient,
        second_coefficient=second_coefficient,
        content=content,
        primitive_first_coefficient=primitive_first,
        primitive_second_coefficient=primitive_second,
        content_gcd=content_gcd,
        content_status=_status(content_gcd, modulus),
        first_quotient_residue=first.sum_residue,
        second_quotient_residue=second.sum_residue,
        first_quotient_gcd=first.sum_gcd,
        second_quotient_gcd=second.sum_gcd,
        aggregate_residue=aggregate,
        aggregate_gcd=gcd(aggregate, modulus),
        primitive_aggregate_residue=primitive_aggregate,
        primitive_aggregate_gcd=gcd(primitive_aggregate, modulus),
        prefix_status=prefix_status,
        rational_residue=rational,
        rational_gcd=rational_gcd,
        primitive_rational_residue=primitive_rational,
        primitive_rational_gcd=primitive_rational_gcd,
        first_overlap_gcd=first_overlap,
        first_public_bound_gcd=first_bound,
        second_overlap_gcd=second_overlap,
        second_public_bound_gcd=second_bound,
        first_resultant_base=abs(second_coefficient) * second_factor,
        first_resultant_exponent=first_factor - 1,
        second_resultant_coefficient_base=abs(first_coefficient),
        second_resultant_coefficient_exponent=(
            first_factor * (second_factor - 1)
        ),
        second_resultant_stage_base=second_factor,
        second_resultant_stage_exponent=first_factor - 1,
    )
