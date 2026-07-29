"""Overlap accounting for shifted compact Phi4 gap selectors."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from itertools import combinations

from .compact_support_signatures import (
    phi4_compact_signature,
    signature_pair_accounting,
)
from .length_indexed_cofactor_schedule import balanced_prime_population


@dataclass(frozen=True)
class CompactGapOverlapProfile:
    """Exact finite signature and overlap accounting for one public level list."""

    input_length: int
    candidate_levels: tuple[int, ...]
    population_size: int
    candidate_count: int
    level_span: int
    compact_evaluation_level_sum: int
    distinct_signature_count: int
    zero_signature_count: int
    multi_hit_prime_count: int
    low_weight_prime_count: int
    pair_count: int
    separated_pair_count: int
    collision_pair_count: int
    overlap_population_upper_bound: int
    low_weight_signature_capacity: int
    theorem_forces_collision: bool
    injective: bool
    maximum_bucket_size: int


def _validate_level(level: int) -> None:
    if isinstance(level, bool) or not isinstance(level, int) or level < 2:
        raise ValueError("level must be an integer at least two")


def _validate_levels(candidate_levels: tuple[int, ...]) -> None:
    if not candidate_levels:
        raise ValueError("candidate_levels must be nonempty")
    for level in candidate_levels:
        _validate_level(level)
    if tuple(sorted(set(candidate_levels))) != candidate_levels:
        raise ValueError(
            "candidate_levels must be strictly increasing and distinct"
        )


def compact_gap_exponent(level: int) -> int:
    """Return the M29 exponent ``E_t = 3*2**t + 5``."""
    _validate_level(level)
    return 3 * (1 << level) + 5


def compact_gap_overlap_integer(level_gap: int) -> int:
    """Return the exact M48 pair-overlap integer for one positive level gap."""
    if (
        isinstance(level_gap, bool)
        or not isinstance(level_gap, int)
        or level_gap < 1
    ):
        raise ValueError("level_gap must be a positive integer")
    odd_exponent = (1 << level_gap) - 1
    return int(pow(3, odd_exponent) + pow(32, odd_exponent))


def compact_gap_overlap_bit_bound(level_gap: int) -> int:
    """Bound the bit length of the exact pair-overlap integer."""
    if (
        isinstance(level_gap, bool)
        or not isinstance(level_gap, int)
        or level_gap < 1
    ):
        raise ValueError("level_gap must be a positive integer")
    return 5 * ((1 << level_gap) - 1) + 1


def compact_gap_overlap_population_upper_bound(
    input_length: int,
    candidate_levels: tuple[int, ...],
) -> int:
    """Union-bound balanced primes that can hit at least two candidates."""
    if (
        isinstance(input_length, bool)
        or not isinstance(input_length, int)
        or input_length < 9
    ):
        raise ValueError("input_length must be an integer at least nine")
    _validate_levels(candidate_levels)
    population_prime_bits = (input_length - 1) // 2
    return sum(
        compact_gap_overlap_bit_bound(second - first)
        // population_prime_bits
        for first, second in combinations(candidate_levels, 2)
    )


def compact_gap_overlap_profile(
    input_length: int,
    candidate_levels: tuple[int, ...],
) -> CompactGapOverlapProfile:
    """Compute exact signatures and the M48 low-weight collision certificate."""
    if (
        isinstance(input_length, bool)
        or not isinstance(input_length, int)
        or input_length < 9
    ):
        raise ValueError("input_length must be an integer at least nine")
    _validate_levels(candidate_levels)
    primes = balanced_prime_population(input_length)
    if len(primes) < 2:
        raise ValueError("balanced population must contain at least two primes")
    signatures = tuple(
        phi4_compact_signature(candidate_levels, prime) for prime in primes
    )
    accounting = signature_pair_accounting(
        signatures,
        len(candidate_levels),
    )
    counts = Counter(signatures)
    multi_hit_count = sum(signature.bit_count() >= 2 for signature in signatures)
    low_weight_count = len(signatures) - multi_hit_count
    overlap_bound = compact_gap_overlap_population_upper_bound(
        input_length,
        candidate_levels,
    )
    if multi_hit_count > overlap_bound:
        raise AssertionError("M48 pair-overlap population bound failed")
    low_weight_capacity = len(candidate_levels) + 1
    return CompactGapOverlapProfile(
        input_length=input_length,
        candidate_levels=candidate_levels,
        population_size=len(primes),
        candidate_count=len(candidate_levels),
        level_span=candidate_levels[-1] - candidate_levels[0],
        compact_evaluation_level_sum=sum(candidate_levels),
        distinct_signature_count=len(counts),
        zero_signature_count=counts.get(0, 0),
        multi_hit_prime_count=multi_hit_count,
        low_weight_prime_count=low_weight_count,
        pair_count=accounting.pair_count,
        separated_pair_count=accounting.separated_pair_count,
        collision_pair_count=accounting.collision_pair_count,
        overlap_population_upper_bound=overlap_bound,
        low_weight_signature_capacity=low_weight_capacity,
        theorem_forces_collision=(
            len(primes) - overlap_bound > low_weight_capacity
        ),
        injective=accounting.injective,
        maximum_bucket_size=max(counts.values()),
    )
