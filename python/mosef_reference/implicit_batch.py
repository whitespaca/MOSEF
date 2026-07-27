"""Exact leaf-materialized product-tree semantics for M15."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from math import gcd


@dataclass(frozen=True)
class BatchProductEvaluation:
    """Leaves, tree levels, GCDs, and charged multiplication count."""

    exponents: tuple[int, ...]
    leaf_residues: tuple[int, ...]
    levels: tuple[tuple[int, ...], ...]
    leaf_gcds: tuple[int, ...]
    root_residue: int
    root_gcd: int
    multiplication_count: int

    @property
    def leaf_count(self) -> int:
        """Return the number of charged modular-power leaves."""
        return len(self.exponents)


def _normalized_exponents(exponents: Iterable[int]) -> tuple[int, ...]:
    """Validate and freeze one canonical finite exponent set."""
    normalized = tuple(exponents)
    if not normalized:
        raise ValueError("the exponent set must be nonempty")
    if any(
        isinstance(exponent, bool)
        or not isinstance(exponent, int)
        or exponent <= 0
        for exponent in normalized
    ):
        raise ValueError("exponents must be positive integers")
    if tuple(sorted(set(normalized))) != normalized:
        raise ValueError("exponents must be strictly increasing")
    return normalized


def evaluate_batch_product(
    base: int,
    modulus: int,
    exponents: Iterable[int],
) -> BatchProductEvaluation:
    """Evaluate a charged product tree for ``prod(g**d - 1) mod N``."""
    if isinstance(base, bool) or not isinstance(base, int):
        raise ValueError("base must be an integer")
    if isinstance(modulus, bool) or not isinstance(modulus, int) or modulus < 2:
        raise ValueError("modulus must be at least two")
    reduced_base = base % modulus
    if gcd(reduced_base, modulus) != 1:
        raise ValueError("base must be a unit modulo the modulus")
    normalized = _normalized_exponents(exponents)
    leaves = tuple(
        (pow(reduced_base, exponent, modulus) - 1) % modulus
        for exponent in normalized
    )
    levels = [leaves]
    multiplication_count = 0
    current = leaves
    while len(current) > 1:
        following: list[int] = []
        for index in range(0, len(current), 2):
            if index + 1 == len(current):
                following.append(current[index])
            else:
                following.append(
                    current[index] * current[index + 1] % modulus
                )
                multiplication_count += 1
        current = tuple(following)
        levels.append(current)
    return BatchProductEvaluation(
        exponents=normalized,
        leaf_residues=leaves,
        levels=tuple(levels),
        leaf_gcds=tuple(gcd(residue, modulus) for residue in leaves),
        root_residue=current[0],
        root_gcd=gcd(current[0], modulus),
        multiplication_count=multiplication_count,
    )


def batch_tree_multiplication_count(leaf_count: int) -> int:
    """Return the exact binary product-tree multiplication count."""
    if (
        isinstance(leaf_count, bool)
        or not isinstance(leaf_count, int)
        or leaf_count < 1
    ):
        raise ValueError("leaf_count must be positive")
    return leaf_count - 1
