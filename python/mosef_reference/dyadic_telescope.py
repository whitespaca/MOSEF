"""Exact dyadic telescoping and total modular-division semantics for M17."""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd


@dataclass(frozen=True)
class DyadicTelescopeEvaluation:
    """Evaluate one dyadic geometric quotient without formal expansion."""

    base: int
    modulus: int
    levels: int
    power_residues: tuple[int, ...]
    factor_residues: tuple[int, ...]
    factor_gcds: tuple[int, ...]
    denominator_residue: int
    denominator_gcd: int
    numerator_residue: int
    numerator_gcd: int
    quotient_residue: int
    quotient_gcd: int
    division_status: str
    division_quotient: int | None
    formal_degree: int
    formal_monomial_count: int
    squaring_count: int
    product_multiplication_count: int


def _validate_inputs(base: int, modulus: int, levels: int) -> tuple[int, int]:
    """Return the reduced base after validating the dyadic circuit domain."""
    if isinstance(base, bool) or not isinstance(base, int):
        raise ValueError("base must be an integer")
    if isinstance(modulus, bool) or not isinstance(modulus, int) or modulus < 2:
        raise ValueError("modulus must be at least two")
    if isinstance(levels, bool) or not isinstance(levels, int) or levels < 0:
        raise ValueError("levels must be a nonnegative integer")
    reduced_base = base % modulus
    if gcd(reduced_base, modulus) != 1:
        raise ValueError("base must be a unit modulo the modulus")
    return reduced_base, modulus


def evaluate_dyadic_telescope(
    base: int,
    modulus: int,
    levels: int,
) -> DyadicTelescopeEvaluation:
    """Evaluate ``(g**(2**levels)-1)/(g-1)`` with total division status."""
    reduced_base, modulus = _validate_inputs(base, modulus, levels)

    powers = [reduced_base]
    for _ in range(levels):
        powers.append(powers[-1] * powers[-1] % modulus)

    factors = tuple((powers[index] + 1) % modulus for index in range(levels))
    quotient = 1 % modulus
    if factors:
        quotient = factors[0]
        for factor in factors[1:]:
            quotient = quotient * factor % modulus

    denominator = (reduced_base - 1) % modulus
    denominator_gcd = gcd(denominator, modulus)
    numerator = (powers[-1] - 1) % modulus
    if denominator_gcd == 1:
        division_status = "unit"
        division_quotient = numerator * pow(denominator, -1, modulus) % modulus
    elif denominator_gcd < modulus:
        division_status = "proper_factor"
        division_quotient = None
    else:
        division_status = "full_collision"
        division_quotient = None

    return DyadicTelescopeEvaluation(
        base=reduced_base,
        modulus=modulus,
        levels=levels,
        power_residues=tuple(powers),
        factor_residues=factors,
        factor_gcds=tuple(gcd(factor, modulus) for factor in factors),
        denominator_residue=denominator,
        denominator_gcd=denominator_gcd,
        numerator_residue=numerator,
        numerator_gcd=gcd(numerator, modulus),
        quotient_residue=quotient,
        quotient_gcd=gcd(quotient, modulus),
        division_status=division_status,
        division_quotient=division_quotient,
        formal_degree=(1 << levels) - 1,
        formal_monomial_count=1 << levels,
        squaring_count=levels,
        product_multiplication_count=max(0, levels - 1),
    )


def dyadic_geometric_coefficients(levels: int) -> tuple[int, ...]:
    """Materialize the exact geometric quotient coefficients for small audits."""
    if isinstance(levels, bool) or not isinstance(levels, int) or levels < 0:
        raise ValueError("levels must be a nonnegative integer")
    if levels > 20:
        raise ValueError("coefficient materialization is limited to level 20")
    return (1,) * (1 << levels)
