"""Compact evaluation of the symmetric signed quotient difference for M22."""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd

from .geometric_sum import evaluate_geometric_sum


@dataclass(frozen=True)
class SymmetricQuotientDifferenceEvaluation:
    """Evaluate ``S_A(g**A) - S_A(g)`` and its exact polynomial factors."""

    base: int
    modulus: int
    exponent: int
    first_quotient_residue: int
    second_quotient_residue: int
    difference_residue: int
    difference_gcd: int
    endpoint_residue: int
    endpoint_gcd: int
    endpoint_status: str
    cofactor_residue: int
    cofactor_gcd: int
    division_cofactor: int | None
    cofactor_monomial_count: int
    cofactor_degree: int
    matrix_multiplication_count: int


Matrix3 = tuple[
    tuple[int, int, int],
    tuple[int, int, int],
    tuple[int, int, int],
]


def _matrix_multiply(left: Matrix3, right: Matrix3, modulus: int) -> Matrix3:
    return tuple(
        tuple(
            sum(left[row][inner] * right[inner][column] for inner in range(3))
            % modulus
            for column in range(3)
        )
        for row in range(3)
    )  # type: ignore[return-value]


def _matrix_power(
    matrix: Matrix3, exponent: int, modulus: int
) -> tuple[Matrix3, int]:
    result: Matrix3 = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
    power = matrix
    remaining = exponent
    multiplication_count = 0
    while remaining:
        if remaining & 1:
            result = _matrix_multiply(result, power, modulus)
            multiplication_count += 1
        remaining >>= 1
        if remaining:
            power = _matrix_multiply(power, power, modulus)
            multiplication_count += 1
    return result, multiplication_count


def _compact_cofactor(
    base: int, modulus: int, exponent: int
) -> tuple[int, int]:
    n = exponent - 1
    y = pow(base, n, modulus)
    xy = base * y % modulus
    transition: Matrix3 = (
        (base, 1, 0),
        (0, xy, 0),
        (base, 1, 1),
    )
    powered, matrix_count = _matrix_power(transition, n - 1, modulus)
    initial = (1 % modulus, xy, 1 % modulus)
    state = tuple(
        sum(powered[row][column] * initial[column] for column in range(3))
        % modulus
        for row in range(3)
    )
    return state[2], matrix_count


def symmetric_cofactor_terms(exponent: int) -> tuple[int, ...]:
    """Return the exact monomial exponents of the formal cofactor ``H_A``."""
    if (
        isinstance(exponent, bool)
        or not isinstance(exponent, int)
        or exponent < 2
    ):
        raise ValueError("exponent must be an integer at least two")
    n = exponent - 1
    return tuple(
        (j - 1) + n * k
        for j in range(1, exponent)
        for k in range(j)
    )


def evaluate_symmetric_quotient_difference(
    base: int,
    modulus: int,
    exponent: int,
) -> SymmetricQuotientDifferenceEvaluation:
    """Evaluate the M22 symmetric difference and its compact cofactor."""
    if (
        isinstance(exponent, bool)
        or not isinstance(exponent, int)
        or exponent < 2
    ):
        raise ValueError("exponent must be an integer at least two")
    first = evaluate_geometric_sum(base, modulus, exponent)
    second = evaluate_geometric_sum(
        first.power_residue,
        modulus,
        exponent,
    )
    reduced_base = first.base
    difference = (second.sum_residue - first.sum_residue) % modulus
    endpoint = (pow(reduced_base, exponent - 1, modulus) - 1) % modulus
    endpoint_gcd = gcd(endpoint, modulus)
    if endpoint_gcd == 1:
        endpoint_status = "unit"
    elif endpoint_gcd < modulus:
        endpoint_status = "proper_factor"
    else:
        endpoint_status = "full_collision"
    cofactor, matrix_count = _compact_cofactor(
        reduced_base,
        modulus,
        exponent,
    )
    if difference != reduced_base * endpoint * cofactor % modulus:
        raise AssertionError("symmetric quotient-difference identity failed")
    division_cofactor = (
        difference * pow(reduced_base * endpoint % modulus, -1, modulus)
        % modulus
        if endpoint_gcd == 1
        else None
    )
    if division_cofactor is not None and division_cofactor != cofactor:
        raise AssertionError("unit endpoint division disagreed with cofactor")
    return SymmetricQuotientDifferenceEvaluation(
        base=reduced_base,
        modulus=modulus,
        exponent=exponent,
        first_quotient_residue=first.sum_residue,
        second_quotient_residue=second.sum_residue,
        difference_residue=difference,
        difference_gcd=gcd(difference, modulus),
        endpoint_residue=endpoint,
        endpoint_gcd=endpoint_gcd,
        endpoint_status=endpoint_status,
        cofactor_residue=cofactor,
        cofactor_gcd=gcd(cofactor, modulus),
        division_cofactor=division_cofactor,
        cofactor_monomial_count=exponent * (exponent - 1) // 2,
        cofactor_degree=exponent * (exponent - 2),
        matrix_multiplication_count=matrix_count,
    )
