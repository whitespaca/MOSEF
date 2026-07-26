"""Signed linear combinations of explicit iterated quotient stages for M21."""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd

from .iterated_quotient import (
    IteratedQuotientEvaluation,
    evaluate_iterated_quotient,
)


@dataclass(frozen=True)
class QuotientLinearCombinationEvaluation:
    """Compact residue semantics for one public signed stage combination."""

    base: int
    modulus: int
    factors: tuple[int, ...]
    coefficients: tuple[int, ...]
    chain: IteratedQuotientEvaluation
    coefficient_residues: tuple[int, ...]
    coefficient_gcds: tuple[int, ...]
    weighted_stage_residues: tuple[int, ...]
    weighted_stage_gcds: tuple[int, ...]
    aggregate_residue: int
    aggregate_gcd: int
    formal_degree_bound: int
    uncollected_term_count: int
    multiplication_count: int
    addition_count: int


def expand_quotient_linear_combination(
    factors: tuple[int, ...] | list[int],
    coefficients: tuple[int, ...] | list[int],
) -> tuple[tuple[int, int], ...]:
    """Return the collected sparse integer polynomial for the requested output."""
    factor_tuple = tuple(factors)
    coefficient_tuple = tuple(coefficients)
    if (
        not factor_tuple
        or len(factor_tuple) != len(coefficient_tuple)
        or any(factor < 1 for factor in factor_tuple)
    ):
        raise ValueError("factors and coefficients must be aligned and nonempty")

    prefix = 1
    collected: dict[int, int] = {}
    for factor, coefficient in zip(factor_tuple, coefficient_tuple, strict=True):
        for term in range(factor):
            exponent = term * prefix
            collected[exponent] = collected.get(exponent, 0) + coefficient
        prefix *= factor
    return tuple(
        (exponent, coefficient)
        for exponent, coefficient in sorted(collected.items())
        if coefficient != 0
    )


def evaluate_quotient_linear_combination(
    base: int,
    modulus: int,
    factors: tuple[int, ...] | list[int],
    coefficients: tuple[int, ...] | list[int],
) -> QuotientLinearCombinationEvaluation:
    """Evaluate ``sum(c_i * S_(A_i)(g**M_(i-1)))`` modulo ``modulus``."""
    factor_tuple = tuple(factors)
    coefficient_tuple = tuple(coefficients)
    if len(factor_tuple) != len(coefficient_tuple):
        raise ValueError("factors and coefficients must have equal length")
    chain = evaluate_iterated_quotient(base, modulus, factor_tuple)

    coefficient_residues = tuple(
        coefficient % modulus for coefficient in coefficient_tuple
    )
    coefficient_gcds = tuple(
        gcd(coefficient, modulus) for coefficient in coefficient_tuple
    )
    weighted = tuple(
        coefficient_residue * stage.quotient_residue % modulus
        for coefficient_residue, stage in zip(
            coefficient_residues, chain.stages, strict=True
        )
    )
    weighted_gcds = tuple(gcd(value, modulus) for value in weighted)
    aggregate = sum(weighted) % modulus
    degree_bound = max(
        right - left
        for left, right in zip(
            chain.prefix_exponents[:-1],
            chain.prefix_exponents[1:],
            strict=True,
        )
    )
    return QuotientLinearCombinationEvaluation(
        base=chain.base,
        modulus=modulus,
        factors=factor_tuple,
        coefficients=coefficient_tuple,
        chain=chain,
        coefficient_residues=coefficient_residues,
        coefficient_gcds=coefficient_gcds,
        weighted_stage_residues=weighted,
        weighted_stage_gcds=weighted_gcds,
        aggregate_residue=aggregate,
        aggregate_gcd=gcd(aggregate, modulus),
        formal_degree_bound=degree_bound,
        uncollected_term_count=sum(factor_tuple),
        multiplication_count=chain.multiplication_count + len(factor_tuple),
        addition_count=chain.addition_count + max(0, len(factor_tuple) - 1),
    )
