"""Iterated geometric-quotient chain semantics for M20."""

from __future__ import annotations

from dataclasses import dataclass

from .nested_quotient import NestedQuotientEvaluation, evaluate_nested_quotient


@dataclass(frozen=True)
class IteratedQuotientEvaluation:
    """Evaluate every quotient in a public geometric factor chain."""

    base: int
    modulus: int
    factors: tuple[int, ...]
    prefix_exponents: tuple[int, ...]
    stages: tuple[NestedQuotientEvaluation, ...]
    final_quotient_product_residue: int
    final_prefix_residue: int
    final_prefix_gcd: int
    multiplication_count: int
    addition_count: int


def evaluate_iterated_quotient(
    base: int,
    modulus: int,
    factors: tuple[int, ...] | list[int],
) -> IteratedQuotientEvaluation:
    """Evaluate the chain ``S_(M_i)(g) / S_(M_(i-1))(g)``."""
    factor_tuple = tuple(factors)
    if modulus < 2:
        raise ValueError("modulus must be at least two")
    if not factor_tuple or any(factor < 1 for factor in factor_tuple):
        raise ValueError("factors must be a nonempty sequence of positive integers")

    prefix = 1
    prefixes = [prefix]
    stages: list[NestedQuotientEvaluation] = []
    quotient_product: int | None = None
    multiplication_count = 0
    addition_count = 0
    previous_numerator: int | None = None
    for factor in factor_tuple:
        stage = evaluate_nested_quotient(base, modulus, prefix, factor)
        if previous_numerator is not None:
            if stage.intermediate_residue != previous_numerator:
                raise AssertionError("iterated prefix linkage failed")
        quotient_product = (
            stage.quotient_residue
            if quotient_product is None
            else quotient_product * stage.quotient_residue % modulus
        )
        if quotient_product != stage.rational_numerator_residue:
            raise AssertionError("iterated quotient product identity failed")
        stages.append(stage)
        multiplication_count += stage.multiplication_count
        addition_count += stage.addition_count
        previous_numerator = stage.rational_numerator_residue
        prefix *= factor
        prefixes.append(prefix)

    final_stage = stages[-1]
    assert quotient_product is not None
    return IteratedQuotientEvaluation(
        base=final_stage.base,
        modulus=modulus,
        factors=factor_tuple,
        prefix_exponents=tuple(prefixes),
        stages=tuple(stages),
        final_quotient_product_residue=quotient_product,
        final_prefix_residue=final_stage.rational_numerator_residue,
        final_prefix_gcd=final_stage.rational_numerator_gcd,
        multiplication_count=multiplication_count + max(0, len(stages) - 1),
        addition_count=addition_count,
    )
