"""Exact residue ledgers and restricted separator factoring for M60--M80."""

from __future__ import annotations

import math
from dataclasses import dataclass

from .compact_cofactor_prime_support import phi4_pair_outcome
from .length_indexed_cofactor_schedule import balanced_prime_population


@dataclass(frozen=True)
class ResidueUnionLedger:
    """Exact divisor and residue-union accounting for one gap."""

    input_length: int
    gap: int
    lower: int
    upper: int
    size_threshold: int
    admissible_divisors: tuple[int, ...]
    minimal_divisors: tuple[int, ...]
    residue_union_size: int
    interval_size: int
    elementary_union_bound: int


def _divisors(value: int) -> tuple[int, ...]:
    small: list[int] = []
    large: list[int] = []
    divisor = 1
    while divisor * divisor <= value:
        if value % divisor == 0:
            small.append(divisor)
            if divisor * divisor != value:
                large.append(value // divisor)
        divisor += 1
    return tuple(small + list(reversed(large)))


def minimal_divisibility_antichain(values: tuple[int, ...]) -> tuple[int, ...]:
    """Delete residue moduli whose classes are nested in a smaller one."""
    if any(
        isinstance(value, bool) or not isinstance(value, int) or value < 1
        for value in values
    ):
        raise ValueError("values must be positive integers")
    ordered = tuple(sorted(set(values)))
    return tuple(
        value
        for value in ordered
        if not any(value % smaller == 0 for smaller in ordered if smaller < value)
    )


def residue_union_ledger(input_length: int, gap: int) -> ResidueUnionLedger:
    """Build the exact M60--M63 necessary residue-class ledger."""
    if (
        isinstance(input_length, bool)
        or not isinstance(input_length, int)
        or input_length < 9
    ):
        raise ValueError("input_length must be an integer at least nine")
    if isinstance(gap, bool) or not isinstance(gap, int) or gap < 1:
        raise ValueError("gap must be a positive integer")
    lower = math.isqrt((1 << (input_length - 1)) - 1) + 1
    upper = math.isqrt((1 << input_length) - 1)
    threshold = 3
    while 33**threshold <= lower:
        threshold += 2
    admissible = tuple(
        divisor
        for divisor in _divisors((1 << gap) - 1)
        if divisor >= threshold
    )
    minimal = minimal_divisibility_antichain(admissible)
    residues = {
        value
        for divisor in minimal
        for value in range(
            lower + ((1 - lower) % (2 * divisor)),
            upper + 1,
            2 * divisor,
        )
    }
    interval_size = upper - lower + 1
    elementary_bound = sum(
        interval_size // (2 * divisor) + 1 for divisor in minimal
    )
    return ResidueUnionLedger(
        input_length=input_length,
        gap=gap,
        lower=lower,
        upper=upper,
        size_threshold=threshold,
        admissible_divisors=admissible,
        minimal_divisors=minimal,
        residue_union_size=len(residues),
        interval_size=interval_size,
        elementary_union_bound=elementary_bound,
    )


def restricted_phi4_separator_factor(
    first_prime: int,
    second_prime: int,
    candidate_levels: tuple[int, ...],
) -> int | None:
    """Return the first proper factor exposed by a public Phi4 level list."""
    if first_prime == second_prime:
        raise ValueError("pair primes must be distinct")
    for level in candidate_levels:
        outcome = phi4_pair_outcome(level, first_prime, second_prime)
        if outcome.factor is not None:
            return outcome.factor
    return None


def restricted_phi4_separated_pairs(
    input_length: int,
    candidate_levels: tuple[int, ...],
) -> tuple[int, int]:
    """Count finite balanced pairs separated and factored by the same list."""
    primes = balanced_prime_population(input_length)
    separated = 0
    factored = 0
    for index, first in enumerate(primes):
        for second in primes[index + 1 :]:
            factor = restricted_phi4_separator_factor(
                first,
                second,
                candidate_levels,
            )
            if factor is not None:
                separated += 1
                factored += int(factor in (first, second))
    return separated, factored
