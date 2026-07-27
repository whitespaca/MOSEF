"""Exact quotient and extraction semantics for the M26 exceptional families."""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd

from .rational_residue_audit import (
    evaluate_rational_residue_audit,
    monic_polynomial_divide,
    polynomial_multiply,
    signed_numerator_coefficients,
)


@dataclass(frozen=True)
class ExceptionalCyclotomicEvaluation:
    """Evaluate one recognized Phi4 or Phi6 exceptional numerator."""

    base: int
    modulus: int
    family: str
    order: int
    first_factor: int
    second_factor: int
    first_coefficient: int
    second_coefficient: int
    cyclotomic_residue: int
    cyclotomic_gcd: int
    cyclotomic_status: str
    aggregate_residue: int
    aggregate_gcd: int
    aggregate_status: str
    cofactor_residue: int | None
    cofactor_gcd: int | None
    cofactor_status: str | None
    extraction_source: str
    extraction_gcd: int | None
    first_quotient_gcd: int
    second_quotient_gcd: int
    first_public_bound_gcd: int
    second_public_bound_gcd: int
    dense_cofactor_degree: int
    dense_cofactor_coefficient_count: int


def _status(value: int, modulus: int) -> str:
    if value == 1:
        return "unit"
    if value < modulus:
        return "proper_factor"
    return "full_collision"


def _family_data(
    first_factor: int, second_factor: int, family: str
) -> tuple[int, int, tuple[int, ...]]:
    if (
        isinstance(first_factor, bool)
        or not isinstance(first_factor, int)
        or first_factor < 2
        or isinstance(second_factor, bool)
        or not isinstance(second_factor, int)
        or second_factor < 2
        or first_factor == second_factor
    ):
        raise ValueError("factors must be unequal integers at least two")
    if family == "phi4":
        if first_factor % 4 != 3 or second_factor % 4 != 3:
            raise ValueError("phi4 requires A and B congruent to 3 modulo 4")
        return 4, 1, (1, 0, 1)
    if family == "phi6":
        if first_factor % 6 != 5 or second_factor % 6 != 3:
            raise ValueError("phi6 requires A=5 and B=3 modulo 6")
        return 6, 2, (1, -1, 1)
    raise ValueError("family must be 'phi4' or 'phi6'")


def exceptional_cyclotomic_coefficients(
    first_factor: int, second_factor: int, family: str
) -> tuple[int, ...]:
    """Return the fixed monic cyclotomic factor in ascending order."""
    return _family_data(first_factor, second_factor, family)[2]


def exceptional_cofactor_coefficients(
    first_factor: int, second_factor: int, family: str
) -> tuple[int, ...]:
    """Return the exact dense quotient after removing Phi4 or Phi6."""
    _, first_coefficient, cyclotomic = _family_data(
        first_factor, second_factor, family
    )
    numerator = signed_numerator_coefficients(
        first_factor,
        second_factor,
        first_coefficient,
        1,
    )
    quotient, remainder = monic_polynomial_divide(
        numerator,
        cyclotomic,
    )
    if any(remainder) or polynomial_multiply(cyclotomic, quotient) != numerator:
        raise AssertionError("exceptional cyclotomic division was not exact")
    return quotient


def _geometric_residue(base: int, modulus: int, count: int) -> int:
    def pair(exponent: int) -> tuple[int, int]:
        if exponent == 0:
            return 1 % modulus, 0
        half_power, half_sum = pair(exponent // 2)
        power = half_power * half_power % modulus
        total = half_sum * (1 + half_power) % modulus
        if exponent % 2:
            total = (total + power) % modulus
            power = power * base % modulus
        return power, total

    return pair(count)[1]


def _polynomial_residue(
    coefficients: tuple[int, ...], base: int, modulus: int
) -> int:
    result = 0
    for coefficient in reversed(coefficients):
        result = (result * base + coefficient) % modulus
    return result


def _periodic_residue(
    pattern: tuple[int, ...], length: int, base: int, modulus: int
) -> int:
    blocks, tail = divmod(length, len(pattern))
    block = _polynomial_residue(pattern, base, modulus)
    block_sum = _geometric_residue(
        pow(base, len(pattern), modulus),
        modulus,
        blocks,
    )
    tail_value = _polynomial_residue(pattern[:tail] or (0,), base, modulus)
    return (
        block * block_sum
        + pow(base, blocks * len(pattern), modulus) * tail_value
    ) % modulus


def _compact_phi4_cofactor_residue(
    base: int, modulus: int, first_factor: int, second_factor: int
) -> int:
    first_blocks = (first_factor - 3) // 4
    second_blocks = (second_factor - 3) // 4
    first_fourth = pow(base, 4, modulus)
    first_u = (
        (1 + base)
        * _geometric_residue(first_fourth, modulus, first_blocks)
        + pow(base, 4 * first_blocks, modulus)
    ) % modulus
    nested_base = pow(base, first_factor, modulus)
    nested_u = (
        (1 + nested_base)
        * _geometric_residue(
            pow(nested_base, 4, modulus),
            modulus,
            second_blocks,
        )
        + pow(nested_base, 4 * second_blocks, modulus)
    ) % modulus
    alternating_square = (-base * base) % modulus
    substituted_factor = _geometric_residue(
        alternating_square,
        modulus,
        first_factor,
    )
    first_residual_exponent = first_factor - 2
    second_residual_exponent = first_factor * (second_factor - 2)
    residual_count = (
        second_residual_exponent - first_residual_exponent
    ) // 2
    residual = (
        pow(base, first_residual_exponent, modulus)
        * _geometric_residue(
            alternating_square,
            modulus,
            residual_count,
        )
    ) % modulus
    return (first_u + substituted_factor * nested_u + residual) % modulus


def _compact_phi6_substitution_factor(
    base: int, modulus: int, first_factor: int
) -> int:
    first_segment = _periodic_residue(
        (1, 1, 0, -1, -1, 0),
        first_factor,
        base,
        modulus,
    )
    second_segment = _periodic_residue(
        (-1, 0, 1, 1, 0, -1),
        first_factor - 1,
        base,
        modulus,
    )
    return (
        first_segment
        + pow(base, first_factor, modulus) * second_segment
    ) % modulus


def _compact_phi6_cofactor_residue(
    base: int, modulus: int, first_factor: int, second_factor: int
) -> int:
    first_blocks = (first_factor - 5) // 6
    second_blocks = (second_factor - 3) // 6

    def h(value: int) -> int:
        return (
            pow(value, 3, modulus)
            + 2 * pow(value, 2, modulus)
            + 2 * value
            + 1
        ) % modulus

    first_u = (
        h(base)
        * _geometric_residue(
            pow(base, 6, modulus),
            modulus,
            first_blocks + 1,
        )
    ) % modulus
    nested_base = pow(base, first_factor, modulus)
    nested_u = (
        h(nested_base)
        * _geometric_residue(
            pow(nested_base, 6, modulus),
            modulus,
            second_blocks,
        )
        + pow(nested_base, 6 * second_blocks, modulus)
    ) % modulus
    substituted_factor = _compact_phi6_substitution_factor(
        base,
        modulus,
        first_factor,
    )
    fixed_quotient = (
        pow(base, 4, modulus)
        + pow(base, 3, modulus)
        - base
        - 1
    ) % modulus
    residual = (
        2
        * pow(base, first_factor, modulus)
        * fixed_quotient
        * _geometric_residue(
            pow(base, 6, modulus),
            modulus,
            first_factor * second_blocks,
        )
    ) % modulus
    return (
        2 * first_u + substituted_factor * nested_u + residual
    ) % modulus


def compact_exceptional_cofactor_residue(
    base: int,
    modulus: int,
    first_factor: int,
    second_factor: int,
    family: str,
) -> int:
    """Evaluate the exact quotient without dense expansion or modular division."""
    if (
        isinstance(modulus, bool)
        or not isinstance(modulus, int)
        or modulus < 2
    ):
        raise ValueError("modulus must be an integer at least two")
    if isinstance(base, bool) or not isinstance(base, int):
        raise ValueError("base must be an integer")
    _family_data(first_factor, second_factor, family)
    base %= modulus
    if family == "phi4":
        return _compact_phi4_cofactor_residue(
            base, modulus, first_factor, second_factor
        )
    return _compact_phi6_cofactor_residue(
        base, modulus, first_factor, second_factor
    )


def evaluate_exceptional_cyclotomic(
    base: int,
    modulus: int,
    first_factor: int,
    second_factor: int,
    family: str,
) -> ExceptionalCyclotomicEvaluation:
    """Apply the total direct-factor/unit-cofactor/full-collision trichotomy."""
    if (
        isinstance(modulus, bool)
        or not isinstance(modulus, int)
        or modulus < 2
    ):
        raise ValueError("modulus must be an integer at least two")
    if isinstance(base, bool) or not isinstance(base, int):
        raise ValueError("base must be an integer")
    normalized_base = base % modulus
    if gcd(normalized_base, modulus) != 1:
        raise ValueError("base must be a unit modulo the modulus")
    order, first_coefficient, cyclotomic = _family_data(
        first_factor, second_factor, family
    )
    audit = evaluate_rational_residue_audit(
        normalized_base,
        modulus,
        first_factor,
        second_factor,
        first_coefficient,
        1,
    )
    if family == "phi4":
        cyclotomic_residue = (
            normalized_base * normalized_base + 1
        ) % modulus
    else:
        cyclotomic_residue = (
            normalized_base * normalized_base - normalized_base + 1
        ) % modulus
    cyclotomic_gcd = gcd(cyclotomic_residue, modulus)
    cyclotomic_status = _status(cyclotomic_gcd, modulus)
    aggregate_status = _status(audit.aggregate_gcd, modulus)

    cofactor_residue = compact_exceptional_cofactor_residue(
        normalized_base,
        modulus,
        first_factor,
        second_factor,
        family,
    )
    cofactor_gcd = gcd(cofactor_residue, modulus)
    cofactor_status = _status(cofactor_gcd, modulus)
    if (
        cyclotomic_residue * cofactor_residue % modulus
        != audit.aggregate_residue
    ):
        raise AssertionError("compact cofactor identity failed")
    extraction_source = "none"
    extraction_gcd: int | None = None
    if cyclotomic_status == "proper_factor":
        extraction_source = "cyclotomic"
        extraction_gcd = cyclotomic_gcd
    elif cofactor_status == "proper_factor":
        extraction_source = "cofactor"
        extraction_gcd = cofactor_gcd
    elif cyclotomic_status == "unit":
        if cofactor_gcd != audit.aggregate_gcd:
            raise AssertionError("unit cyclotomic cancellation changed the GCD")
    else:
        if audit.aggregate_gcd != modulus:
            raise AssertionError("full cyclotomic collision did not force F=0")
        extraction_source = "full_collision"

    dense_cofactor_degree = first_factor * (second_factor - 1) - 2
    return ExceptionalCyclotomicEvaluation(
        base=normalized_base,
        modulus=modulus,
        family=family,
        order=order,
        first_factor=first_factor,
        second_factor=second_factor,
        first_coefficient=first_coefficient,
        second_coefficient=1,
        cyclotomic_residue=cyclotomic_residue,
        cyclotomic_gcd=cyclotomic_gcd,
        cyclotomic_status=cyclotomic_status,
        aggregate_residue=audit.aggregate_residue,
        aggregate_gcd=audit.aggregate_gcd,
        aggregate_status=aggregate_status,
        cofactor_residue=cofactor_residue,
        cofactor_gcd=cofactor_gcd,
        cofactor_status=cofactor_status,
        extraction_source=extraction_source,
        extraction_gcd=extraction_gcd,
        first_quotient_gcd=audit.first_quotient_gcd,
        second_quotient_gcd=audit.second_quotient_gcd,
        first_public_bound_gcd=audit.first_public_bound_gcd,
        second_public_bound_gcd=audit.second_public_bound_gcd,
        dense_cofactor_degree=dense_cofactor_degree,
        dense_cofactor_coefficient_count=dense_cofactor_degree + 1,
    )
