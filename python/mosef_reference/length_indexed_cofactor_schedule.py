"""Materialized-support accounting for M28 length-indexed schedules."""

from __future__ import annotations

from dataclasses import dataclass
from math import isqrt

from .baseline import is_prime


@dataclass(frozen=True)
class LengthIndexedSupportProfile:
    """Exact support and pair-coverage accounting for one input length."""

    input_length: int
    population_size: int
    min_prime_log2_floor: int
    charged_value_count: int
    materialized_bit_budget: int
    hit_primes: tuple[int, ...]
    missed_primes: tuple[int, ...]
    hit_prime_count: int
    forced_miss_pair_count: int
    pair_count: int
    maximum_coverable_pair_count: int
    support_cap: int
    necessary_universal_bit_budget: int


@dataclass(frozen=True)
class Phi4CompactGapProfile:
    """A compact in-family descriptor with an exponential exact-lift bound."""

    level: int
    family: str
    order: int
    first_factor: int
    second_factor: int
    base: int
    public_integer_bit_budget: int
    compact_count_bit_budget: int
    cofactor_degree: int
    cofactor_bit_length_lower_bound: int


def balanced_prime_population(input_length: int) -> tuple[int, ...]:
    """Return primes whose pairwise products all have ``input_length`` bits."""
    if (
        isinstance(input_length, bool)
        or not isinstance(input_length, int)
        or input_length < 4
    ):
        raise ValueError("input_length must be an integer at least four")
    lower_square = 1 << (input_length - 1)
    upper_square = 1 << input_length
    lower = isqrt(lower_square - 1) + 1
    upper = isqrt(upper_square - 1)
    return tuple(prime for prime in range(lower, upper + 1) if is_prime(prime))


def length_indexed_support_profile(
    input_length: int,
    primes: tuple[int, ...],
    charged_values: tuple[int, ...],
) -> LengthIndexedSupportProfile:
    """Account for all pairs that a nonzero materialized value list can touch."""
    if (
        isinstance(input_length, bool)
        or not isinstance(input_length, int)
        or input_length < 4
    ):
        raise ValueError("input_length must be an integer at least four")
    if len(primes) < 2 or len(set(primes)) != len(primes):
        raise ValueError("primes must contain at least two distinct values")
    if any(
        isinstance(prime, bool)
        or not isinstance(prime, int)
        or not is_prime(prime)
        for prime in primes
    ):
        raise ValueError("every population value must be prime")
    for index, first_prime in enumerate(primes):
        for second_prime in primes[index + 1 :]:
            if (first_prime * second_prime).bit_length() != input_length:
                raise ValueError("every prime pair must produce the declared input length")
    if any(
        isinstance(value, bool) or not isinstance(value, int) or value == 0
        for value in charged_values
    ):
        raise ValueError("charged values must be nonzero integers")

    materialized_bit_budget = sum(abs(value).bit_length() for value in charged_values)
    hit_primes = tuple(
        prime
        for prime in primes
        if any(value % prime == 0 for value in charged_values)
    )
    hit_set = set(hit_primes)
    missed_primes = tuple(prime for prime in primes if prime not in hit_set)
    population_size = len(primes)
    hit_prime_count = len(hit_primes)
    missed_count = len(missed_primes)
    pair_count = population_size * (population_size - 1) // 2
    forced_miss_pair_count = missed_count * (missed_count - 1) // 2
    min_prime_log2_floor = min(prime.bit_length() - 1 for prime in primes)
    support_cap = min(
        population_size,
        materialized_bit_budget // min_prime_log2_floor,
    )
    return LengthIndexedSupportProfile(
        input_length=input_length,
        population_size=population_size,
        min_prime_log2_floor=min_prime_log2_floor,
        charged_value_count=len(charged_values),
        materialized_bit_budget=materialized_bit_budget,
        hit_primes=hit_primes,
        missed_primes=missed_primes,
        hit_prime_count=hit_prime_count,
        forced_miss_pair_count=forced_miss_pair_count,
        pair_count=pair_count,
        maximum_coverable_pair_count=pair_count - forced_miss_pair_count,
        support_cap=support_cap,
        necessary_universal_bit_budget=(
            min_prime_log2_floor * (population_size - 1)
        ),
    )


def phi4_compact_gap_profile(level: int) -> Phi4CompactGapProfile:
    """Return the M28 ``A=3, B=2^level+3, g=2`` size-gap certificate."""
    if isinstance(level, bool) or not isinstance(level, int) or level < 2:
        raise ValueError("level must be an integer at least two")
    first_factor = 3
    second_factor = (1 << level) + 3
    base = 2
    order = 4
    cofactor_degree = first_factor * (second_factor - 1) - 2
    return Phi4CompactGapProfile(
        level=level,
        family="phi4",
        order=order,
        first_factor=first_factor,
        second_factor=second_factor,
        base=base,
        public_integer_bit_budget=(
            first_factor.bit_length()
            + second_factor.bit_length()
            + base.bit_length()
        ),
        compact_count_bit_budget=(
            first_factor.bit_length() + second_factor.bit_length()
        ),
        cofactor_degree=cofactor_degree,
        cofactor_bit_length_lower_bound=3 * second_factor - 5,
    )
