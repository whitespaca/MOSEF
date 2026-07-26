"""Cancellation-obscured nested geometric quotient semantics for M19."""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd

from .geometric_sum import evaluate_geometric_sum


@dataclass(frozen=True)
class NestedQuotientEvaluation:
    """Evaluate S_(A B)(g) / S_A(g) and S_B(g^A) through both paths."""

    base: int
    modulus: int
    inner_exponent: int
    multiplier: int
    product_exponent: int
    inner_power_residue: int
    intermediate_residue: int
    intermediate_gcd: int
    quotient_residue: int
    quotient_gcd: int
    rational_numerator_residue: int
    rational_numerator_gcd: int
    composed_denominator_residue: int
    composed_denominator_gcd: int
    endpoint_residue: int
    endpoint_gcd: int
    multiplier_gcd: int
    rational_division_status: str
    rational_division_quotient: int | None
    composed_division_status: str
    composed_division_quotient: int | None
    multiplication_count: int
    addition_count: int
    formal_quotient_degree: int
    formal_quotient_monomial_count: int


def _division(
    numerator: int,
    denominator: int,
    modulus: int,
) -> tuple[str, int | None]:
    divisor = gcd(denominator, modulus)
    if divisor == 1:
        return "unit", numerator * pow(denominator, -1, modulus) % modulus
    if divisor < modulus:
        return "proper_factor", None
    return "full_collision", None


def evaluate_nested_quotient(
    base: int,
    modulus: int,
    inner_exponent: int,
    multiplier: int,
) -> NestedQuotientEvaluation:
    """Evaluate the exact identity ``S_(A B)(g)=S_A(g) S_B(g^A)``."""
    inner = evaluate_geometric_sum(base, modulus, inner_exponent)
    outer = evaluate_geometric_sum(inner.power_residue, modulus, multiplier)
    product_exponent = inner_exponent * multiplier
    combined = evaluate_geometric_sum(base, modulus, product_exponent)

    intermediate = inner.sum_residue
    quotient = outer.sum_residue
    rational_numerator = combined.sum_residue
    composed_denominator = (inner.power_residue - 1) % modulus
    endpoint = (outer.power_residue - 1) % modulus
    rational_status, rational_division = _division(
        rational_numerator,
        intermediate,
        modulus,
    )
    composed_status, composed_division = _division(
        endpoint,
        composed_denominator,
        modulus,
    )
    if rational_numerator != intermediate * quotient % modulus:
        raise AssertionError("nested geometric-sum residue identity failed")
    if combined.power_residue != outer.power_residue:
        raise AssertionError("nested endpoint composition failed")

    return NestedQuotientEvaluation(
        base=inner.base,
        modulus=modulus,
        inner_exponent=inner_exponent,
        multiplier=multiplier,
        product_exponent=product_exponent,
        inner_power_residue=inner.power_residue,
        intermediate_residue=intermediate,
        intermediate_gcd=gcd(intermediate, modulus),
        quotient_residue=quotient,
        quotient_gcd=gcd(quotient, modulus),
        rational_numerator_residue=rational_numerator,
        rational_numerator_gcd=gcd(rational_numerator, modulus),
        composed_denominator_residue=composed_denominator,
        composed_denominator_gcd=gcd(composed_denominator, modulus),
        endpoint_residue=endpoint,
        endpoint_gcd=gcd(endpoint, modulus),
        multiplier_gcd=gcd(multiplier, modulus),
        rational_division_status=rational_status,
        rational_division_quotient=rational_division,
        composed_division_status=composed_status,
        composed_division_quotient=composed_division,
        multiplication_count=(
            inner.multiplication_count
            + outer.multiplication_count
            + combined.multiplication_count
        ),
        addition_count=(
            inner.addition_count
            + outer.addition_count
            + combined.addition_count
        ),
        formal_quotient_degree=inner_exponent * (multiplier - 1),
        formal_quotient_monomial_count=multiplier,
    )
