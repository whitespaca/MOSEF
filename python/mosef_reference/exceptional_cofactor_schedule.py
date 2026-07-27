"""Local profiles and public overlap descriptors for M27 schedules."""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd

from .baseline import is_prime
from .exceptional_cyclotomic import (
    compact_exceptional_cofactor_residue,
    exceptional_cyclotomic_coefficients,
)


@dataclass(frozen=True)
class ExceptionalCofactorOverlap:
    """Compact exact resultant data for one exceptional family."""

    family: str
    order: int
    first_factor: int
    second_factor: int
    cofactor_degree: int
    remainder_constant: int
    remainder_linear: int
    cyclotomic_cofactor_resultant: int
    first_stage_resultant_base: int
    first_stage_resultant_exponent: int
    second_stage_power_of_two_exponent: int
    second_stage_resultant_base: int
    second_stage_resultant_exponent: int
    stage_overlap_support: tuple[int, ...]


@dataclass(frozen=True)
class ExceptionalCofactorLocalProfile:
    """Capped local valuations at one public base and prime power."""

    family: str
    order: int
    base: int
    prime: int
    exponent: int
    modulus: int
    cyclotomic_residue: int
    cyclotomic_valuation: int
    cofactor_residue: int
    cofactor_valuation: int
    is_cofactor_root_mod_prime: bool
    is_cyclotomic_root_mod_prime: bool


def _family_remainder(
    first_factor: int, second_factor: int, family: str
) -> tuple[int, int, int]:
    exceptional_cyclotomic_coefficients(
        first_factor,
        second_factor,
        family,
    )
    if family == "phi4":
        constant = (first_factor * (second_factor + 2) + 1) // 4
        linear = (first_factor * (second_factor - 2) + 1) // 4
        return 4, constant, linear
    residual = first_factor * (second_factor - 2) + 1
    constant = -(2 * residual // 3)
    linear = (first_factor * (second_factor + 4) + 4) // 3
    return 6, constant, linear


def exceptional_cofactor_overlap(
    first_factor: int,
    second_factor: int,
    family: str,
) -> ExceptionalCofactorOverlap:
    """Return exact compact resultants without expanding either stage."""
    order, constant, linear = _family_remainder(
        first_factor,
        second_factor,
        family,
    )
    support: tuple[int, ...]
    if family == "phi4":
        resultant = constant * constant + linear * linear
        power_of_two_exponent = 0
        support = (second_factor,)
    else:
        resultant = (
            constant * constant
            + constant * linear
            + linear * linear
        )
        power_of_two_exponent = first_factor * (second_factor - 1) - 2
        support = (2, second_factor)
    return ExceptionalCofactorOverlap(
        family=family,
        order=order,
        first_factor=first_factor,
        second_factor=second_factor,
        cofactor_degree=first_factor * (second_factor - 1) - 2,
        remainder_constant=constant,
        remainder_linear=linear,
        cyclotomic_cofactor_resultant=resultant,
        first_stage_resultant_base=second_factor,
        first_stage_resultant_exponent=first_factor - 1,
        second_stage_power_of_two_exponent=power_of_two_exponent,
        second_stage_resultant_base=second_factor,
        second_stage_resultant_exponent=first_factor - 1,
        stage_overlap_support=support,
    )


def _capped_valuation(residue: int, prime: int, exponent: int) -> int:
    if residue == 0:
        return exponent
    valuation = 0
    while valuation < exponent and residue % prime == 0:
        residue //= prime
        valuation += 1
    return valuation


def evaluate_exceptional_cofactor_local_profile(
    base: int,
    prime: int,
    exponent: int,
    first_factor: int,
    second_factor: int,
    family: str,
) -> ExceptionalCofactorLocalProfile:
    """Evaluate exact capped valuations at one prime power."""
    if isinstance(prime, bool) or not isinstance(prime, int) or not is_prime(prime):
        raise ValueError("prime must be prime")
    if isinstance(exponent, bool) or not isinstance(exponent, int) or exponent < 1:
        raise ValueError("exponent must be a positive integer")
    if isinstance(base, bool) or not isinstance(base, int):
        raise ValueError("base must be an integer")
    modulus = prime**exponent
    normalized_base = base % modulus
    if gcd(normalized_base, prime) != 1:
        raise ValueError("base must be a unit modulo the prime")
    overlap = exceptional_cofactor_overlap(
        first_factor,
        second_factor,
        family,
    )
    cofactor_residue = compact_exceptional_cofactor_residue(
        normalized_base,
        modulus,
        first_factor,
        second_factor,
        family,
    )
    if family == "phi4":
        cyclotomic_residue = (
            normalized_base * normalized_base + 1
        ) % modulus
    else:
        cyclotomic_residue = (
            normalized_base * normalized_base - normalized_base + 1
        ) % modulus
    return ExceptionalCofactorLocalProfile(
        family=family,
        order=overlap.order,
        base=normalized_base,
        prime=prime,
        exponent=exponent,
        modulus=modulus,
        cyclotomic_residue=cyclotomic_residue,
        cyclotomic_valuation=_capped_valuation(
            cyclotomic_residue,
            prime,
            exponent,
        ),
        cofactor_residue=cofactor_residue,
        cofactor_valuation=_capped_valuation(
            cofactor_residue,
            prime,
            exponent,
        ),
        is_cofactor_root_mod_prime=(
            compact_exceptional_cofactor_residue(
                normalized_base,
                prime,
                first_factor,
                second_factor,
                family,
            )
            == 0
        ),
        is_cyclotomic_root_mod_prime=(cyclotomic_residue % prime == 0),
    )


def exceptional_cofactor_root_residues(
    prime: int,
    first_factor: int,
    second_factor: int,
    family: str,
) -> tuple[int, ...]:
    """Enumerate unit roots explicitly, charging all ``prime - 1`` trials."""
    if isinstance(prime, bool) or not isinstance(prime, int) or not is_prime(prime):
        raise ValueError("prime must be prime")
    exceptional_cofactor_overlap(first_factor, second_factor, family)
    return tuple(
        residue
        for residue in range(1, prime)
        if compact_exceptional_cofactor_residue(
            residue,
            prime,
            first_factor,
            second_factor,
            family,
        )
        == 0
    )
