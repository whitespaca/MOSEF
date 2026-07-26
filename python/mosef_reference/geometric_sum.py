"""Binary geometric-sum evaluation with total denominator semantics for M18."""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd


@dataclass(frozen=True)
class GeometricSumEvaluation:
    """Evaluate one arbitrary-exponent geometric sum without expansion."""

    base: int
    modulus: int
    exponent: int
    exponent_bit_length: int
    power_residue: int
    sum_residue: int
    denominator_residue: int
    denominator_gcd: int
    numerator_residue: int
    numerator_gcd: int
    sum_gcd: int
    exponent_gcd: int
    division_status: str
    division_quotient: int | None
    formal_degree: int
    formal_monomial_count: int
    multiplication_count: int
    addition_count: int


def _validate_inputs(base: int, modulus: int, exponent: int) -> tuple[int, int]:
    if isinstance(base, bool) or not isinstance(base, int):
        raise ValueError("base must be an integer")
    if isinstance(modulus, bool) or not isinstance(modulus, int) or modulus < 2:
        raise ValueError("modulus must be at least two")
    if (
        isinstance(exponent, bool)
        or not isinstance(exponent, int)
        or exponent < 1
    ):
        raise ValueError("exponent must be a positive integer")
    reduced_base = base % modulus
    if gcd(reduced_base, modulus) != 1:
        raise ValueError("base must be a unit modulo the modulus")
    return reduced_base, modulus


def evaluate_geometric_sum(
    base: int,
    modulus: int,
    exponent: int,
) -> GeometricSumEvaluation:
    """Evaluate ``S_exponent(base)`` by left-to-right binary composition."""
    reduced_base, modulus = _validate_inputs(base, modulus, exponent)
    bits = bin(exponent)[2:]
    power = reduced_base
    geometric_sum = 1 % modulus
    multiplication_count = 0
    addition_count = 0

    for bit in bits[1:]:
        doubled_sum = geometric_sum * ((1 + power) % modulus) % modulus
        doubled_power = power * power % modulus
        multiplication_count += 2
        addition_count += 1
        geometric_sum = doubled_sum
        power = doubled_power
        if bit == "1":
            geometric_sum = (geometric_sum + power) % modulus
            power = power * reduced_base % modulus
            multiplication_count += 1
            addition_count += 1

    denominator = (reduced_base - 1) % modulus
    denominator_gcd = gcd(denominator, modulus)
    numerator = (power - 1) % modulus
    if denominator_gcd == 1:
        division_status = "unit"
        division_quotient = numerator * pow(denominator, -1, modulus) % modulus
    elif denominator_gcd < modulus:
        division_status = "proper_factor"
        division_quotient = None
    else:
        division_status = "full_collision"
        division_quotient = None

    return GeometricSumEvaluation(
        base=reduced_base,
        modulus=modulus,
        exponent=exponent,
        exponent_bit_length=exponent.bit_length(),
        power_residue=power,
        sum_residue=geometric_sum,
        denominator_residue=denominator,
        denominator_gcd=denominator_gcd,
        numerator_residue=numerator,
        numerator_gcd=gcd(numerator, modulus),
        sum_gcd=gcd(geometric_sum, modulus),
        exponent_gcd=gcd(exponent, modulus),
        division_status=division_status,
        division_quotient=division_quotient,
        formal_degree=exponent - 1,
        formal_monomial_count=exponent,
        multiplication_count=multiplication_count,
        addition_count=addition_count,
    )


def geometric_sum_coefficients(exponent: int) -> tuple[int, ...]:
    """Materialize coefficients for bounded symbolic-recursion audits."""
    if (
        isinstance(exponent, bool)
        or not isinstance(exponent, int)
        or exponent < 1
    ):
        raise ValueError("exponent must be a positive integer")
    if exponent > 65_536:
        raise ValueError("coefficient materialization is limited to 65,536 terms")
    return (1,) * exponent
