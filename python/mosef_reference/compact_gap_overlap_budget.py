"""Overlap accounting for shifted compact Phi4 gap selectors."""

from __future__ import annotations

import math
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


@dataclass(frozen=True)
class CompactGapHighWeightProfile:
    """Finite high-weight signature accounting for one wide-span level list."""

    input_length: int
    candidate_levels: tuple[int, ...]
    high_weight_threshold: int
    population_size: int
    candidate_count: int
    level_span: int
    compact_evaluation_level_sum: int
    distinct_signature_count: int
    zero_signature_count: int
    high_weight_prime_count: int
    maximum_signature_weight: int
    pair_count: int
    separated_pair_count: int
    collision_pair_count: int
    high_weight_population_upper_bound: int
    low_weight_signature_capacity: int
    theorem_forces_collision: bool
    injective: bool
    maximum_bucket_size: int


@dataclass(frozen=True)
class CompactGapBoundaryLedger:
    """Exact M52 entropy ledger using only public list geometry."""

    input_length: int
    candidate_count: int
    level_span: int
    overlap_order: int
    high_weight_threshold: int
    maximum_common_gap: int
    high_weight_population_upper_bound: int
    low_weight_signature_capacity: int
    conservative_population_lower_bound: int
    theorem_forces_collision: bool


@dataclass(frozen=True)
class CompactGapDistinctGapLedger:
    """Exact M53 ledger charging each possible GCD gap only once."""

    input_length: int
    candidate_count: int
    level_span: int
    overlap_order: int
    high_weight_threshold: int
    maximum_common_gap: int
    distinct_gap_count: int
    high_weight_population_upper_bound: int
    low_weight_signature_capacity: int
    conservative_population_lower_bound: int
    theorem_forces_collision: bool


@dataclass(frozen=True)
class CompactGapEndpointLedger:
    """Exact M57 endpoint witness and two-ledger obstruction profile."""

    scale_exponent: int
    input_length: int
    candidate_count: int
    level_span: int
    logarithmic_scale: int
    overlap_order: int
    switch_order: int
    maximum_common_gap: int
    lcm_bit_length_lower_bound: int
    high_weight_charge_lower_bound: int
    low_weight_signature_capacity: int
    conservative_population_lower_bound: int
    high_ledger_consumes_population: bool
    low_ledger_consumes_population: bool
    certificate_blocked: bool


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


def compact_gap_overlap_gcd(
    first_gap: int,
    second_gap: int,
) -> int:
    """Return the exact GCD of two M48 overlap integers."""
    if (
        isinstance(first_gap, bool)
        or not isinstance(first_gap, int)
        or first_gap < 1
        or isinstance(second_gap, bool)
        or not isinstance(second_gap, int)
        or second_gap < 1
    ):
        raise ValueError("both gaps must be positive integers")
    return math.gcd(
        compact_gap_overlap_integer(first_gap),
        compact_gap_overlap_integer(second_gap),
    )


def compact_gap_overlap_lcm_prefix(maximum_gap: int) -> int:
    """Return the exact LCM of ``R_1`` through ``R_maximum_gap``."""
    if (
        isinstance(maximum_gap, bool)
        or not isinstance(maximum_gap, int)
        or maximum_gap < 1
    ):
        raise ValueError("maximum_gap must be a positive integer")
    result = 1
    for gap in range(1, maximum_gap + 1):
        value = compact_gap_overlap_integer(gap)
        result = result // math.gcd(result, value) * value
    return result


def compact_gap_overlap_bit_bound(level_gap: int) -> int:
    """Bound the bit length of the exact pair-overlap integer."""
    if (
        isinstance(level_gap, bool)
        or not isinstance(level_gap, int)
        or level_gap < 1
    ):
        raise ValueError("level_gap must be a positive integer")
    return 5 * ((1 << level_gap) - 1) + 1


def compact_gap_overlap_prefix_bit_bound(maximum_gap: int) -> int:
    """Sum the M48 overlap bit bounds for gaps one through ``maximum_gap``."""
    if (
        isinstance(maximum_gap, bool)
        or not isinstance(maximum_gap, int)
        or maximum_gap < 0
    ):
        raise ValueError("maximum_gap must be a nonnegative integer")
    if maximum_gap == 0:
        return 0
    return 5 * ((1 << (maximum_gap + 1)) - 2) - 4 * maximum_gap


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


def compact_gap_common_support_gap(
    candidate_levels: tuple[int, ...],
) -> int:
    """Return the GCD of offsets in one common-support level subset."""
    _validate_levels(candidate_levels)
    if len(candidate_levels) < 2:
        raise ValueError("at least two candidate levels are required")
    first = candidate_levels[0]
    return math.gcd(*(level - first for level in candidate_levels[1:]))


def compact_gap_realizable_common_gaps(
    candidate_levels: tuple[int, ...],
    overlap_order: int,
) -> tuple[int, ...]:
    """Enumerate GCD gaps realized by ``overlap_order + 1`` selected levels."""
    _validate_levels(candidate_levels)
    if (
        isinstance(overlap_order, bool)
        or not isinstance(overlap_order, int)
        or overlap_order < 1
        or overlap_order >= len(candidate_levels)
    ):
        raise ValueError(
            "overlap_order must be between one and candidate_count - 1"
        )
    gaps = {
        math.gcd(*(level - subset[0] for level in subset[1:]))
        for subset in combinations(candidate_levels, overlap_order + 1)
    }
    return tuple(sorted(gaps))


def compact_gap_maximal_gap_witness(
    overlap_order: int,
    common_gap: int,
    *,
    initial_level: int = 2,
) -> tuple[int, ...]:
    """Construct an arithmetic progression attaining span/order ``common_gap``."""
    if (
        isinstance(overlap_order, bool)
        or not isinstance(overlap_order, int)
        or overlap_order < 1
    ):
        raise ValueError("overlap_order must be a positive integer")
    if (
        isinstance(common_gap, bool)
        or not isinstance(common_gap, int)
        or common_gap < 1
    ):
        raise ValueError("common_gap must be a positive integer")
    _validate_level(initial_level)
    return tuple(
        initial_level + index * common_gap
        for index in range(overlap_order + 1)
    )


def compact_gap_dense_interval_realizable_gaps(
    level_span: int,
    overlap_order: int,
) -> tuple[int, ...]:
    """Return the exact realizable GCD-gap prefix for a dense level interval."""
    if (
        isinstance(level_span, bool)
        or not isinstance(level_span, int)
        or level_span < 1
    ):
        raise ValueError("level_span must be a positive integer")
    if (
        isinstance(overlap_order, bool)
        or not isinstance(overlap_order, int)
        or overlap_order < 1
        or overlap_order > level_span
    ):
        raise ValueError(
            "overlap_order must be between one and level_span"
        )
    return tuple(range(1, level_span // overlap_order + 1))


def compact_gap_common_support_integer(
    candidate_levels: tuple[int, ...],
) -> int:
    """Return the overlap integer forced by a common-support level subset."""
    return compact_gap_overlap_integer(
        compact_gap_common_support_gap(candidate_levels)
    )


def compact_gap_low_weight_signature_capacity(
    candidate_count: int,
    high_weight_threshold: int,
) -> int:
    """Count signatures whose weight is below ``high_weight_threshold``."""
    if (
        isinstance(candidate_count, bool)
        or not isinstance(candidate_count, int)
        or candidate_count < 1
    ):
        raise ValueError("candidate_count must be a positive integer")
    if (
        isinstance(high_weight_threshold, bool)
        or not isinstance(high_weight_threshold, int)
        or high_weight_threshold < 2
    ):
        raise ValueError("high_weight_threshold must be at least two")
    return sum(
        math.comb(candidate_count, weight)
        for weight in range(min(high_weight_threshold, candidate_count + 1))
    )


def compact_gap_balanced_overlap_order(
    candidate_count: int,
    level_span: int,
) -> int:
    """Choose the M51 variable overlap order from the public list geometry.

    The returned ``h`` is the smallest integer, capped by the candidate
    count, with ``h**2 * ceil(log2(candidate_count + 1)) >= level_span``.
    """
    if (
        isinstance(candidate_count, bool)
        or not isinstance(candidate_count, int)
        or candidate_count < 1
    ):
        raise ValueError("candidate_count must be a positive integer")
    if (
        isinstance(level_span, bool)
        or not isinstance(level_span, int)
        or level_span < candidate_count - 1
    ):
        raise ValueError(
            "level_span must fit a strictly increasing integer level list"
        )
    logarithmic_scale = candidate_count.bit_length()
    quotient = (level_span + logarithmic_scale - 1) // logarithmic_scale
    overlap_order = math.isqrt(quotient)
    if overlap_order * overlap_order < quotient:
        overlap_order += 1
    return min(candidate_count, max(1, overlap_order))


def compact_gap_boundary_overlap_order(
    input_length: int,
    candidate_count: int,
    multiplier_numerator: int,
    multiplier_denominator: int,
) -> int:
    """Return ``ceil(x*m/ell)`` capped by ``r`` for rational ``x``."""
    for name, value in (
        ("input_length", input_length),
        ("candidate_count", candidate_count),
        ("multiplier_numerator", multiplier_numerator),
        ("multiplier_denominator", multiplier_denominator),
    ):
        if isinstance(value, bool) or not isinstance(value, int) or value < 1:
            raise ValueError(f"{name} must be a positive integer")
    logarithmic_scale = candidate_count.bit_length()
    numerator = multiplier_numerator * input_length
    denominator = multiplier_denominator * logarithmic_scale
    order = (numerator + denominator - 1) // denominator
    return min(candidate_count, max(1, order))


def compact_gap_boundary_ledger(
    input_length: int,
    candidate_count: int,
    level_span: int,
    overlap_order: int,
) -> CompactGapBoundaryLedger:
    """Compute the exact M52 high/low ledger without enumerating levels."""
    if (
        isinstance(input_length, bool)
        or not isinstance(input_length, int)
        or input_length < 10
    ):
        raise ValueError("input_length must be an integer at least ten")
    if (
        isinstance(candidate_count, bool)
        or not isinstance(candidate_count, int)
        or candidate_count < 1
    ):
        raise ValueError("candidate_count must be a positive integer")
    if (
        isinstance(level_span, bool)
        or not isinstance(level_span, int)
        or level_span < candidate_count - 1
    ):
        raise ValueError(
            "level_span must fit a strictly increasing integer level list"
        )
    if (
        isinstance(overlap_order, bool)
        or not isinstance(overlap_order, int)
        or overlap_order < 1
        or overlap_order > candidate_count
    ):
        raise ValueError(
            "overlap_order must be between one and candidate_count"
        )

    high_weight_threshold = overlap_order + 1
    low_weight_capacity = compact_gap_low_weight_signature_capacity(
        candidate_count,
        high_weight_threshold,
    )
    if overlap_order == candidate_count:
        maximum_common_gap = 0
        high_weight_bound = 0
    else:
        maximum_common_gap = level_span // overlap_order
        population_prime_bits = (input_length - 1) // 2
        high_weight_bound = (
            math.comb(candidate_count, high_weight_threshold)
            * compact_gap_overlap_bit_bound(maximum_common_gap)
            // population_prime_bits
        )
    population_lower_bound = (
        (1 << (input_length // 2)) // (81 * input_length)
    )
    return CompactGapBoundaryLedger(
        input_length=input_length,
        candidate_count=candidate_count,
        level_span=level_span,
        overlap_order=overlap_order,
        high_weight_threshold=high_weight_threshold,
        maximum_common_gap=maximum_common_gap,
        high_weight_population_upper_bound=high_weight_bound,
        low_weight_signature_capacity=low_weight_capacity,
        conservative_population_lower_bound=population_lower_bound,
        theorem_forces_collision=(
            population_lower_bound - high_weight_bound > low_weight_capacity
        ),
    )


def compact_gap_distinct_gap_ledger(
    input_length: int,
    candidate_count: int,
    level_span: int,
    overlap_order: int,
) -> CompactGapDistinctGapLedger:
    """Replace M52 subset charging by the exact M53 distinct-gap union."""
    boundary = compact_gap_boundary_ledger(
        input_length,
        candidate_count,
        level_span,
        overlap_order,
    )
    if overlap_order == candidate_count:
        maximum_common_gap = 0
        high_weight_bound = 0
    else:
        maximum_common_gap = level_span // overlap_order
        population_prime_bits = (input_length - 1) // 2
        high_weight_bound = (
            compact_gap_overlap_prefix_bit_bound(maximum_common_gap)
            // population_prime_bits
        )
    return CompactGapDistinctGapLedger(
        input_length=input_length,
        candidate_count=candidate_count,
        level_span=level_span,
        overlap_order=overlap_order,
        high_weight_threshold=overlap_order + 1,
        maximum_common_gap=maximum_common_gap,
        distinct_gap_count=maximum_common_gap,
        high_weight_population_upper_bound=high_weight_bound,
        low_weight_signature_capacity=(
            boundary.low_weight_signature_capacity
        ),
        conservative_population_lower_bound=(
            boundary.conservative_population_lower_bound
        ),
        theorem_forces_collision=(
            boundary.conservative_population_lower_bound
            - high_weight_bound
            > boundary.low_weight_signature_capacity
        ),
    )


def compact_gap_endpoint_dense_ledger(
    scale_exponent: int,
    overlap_order: int,
) -> CompactGapEndpointLedger:
    """Evaluate the exact M57 endpoint-dense witness at one threshold."""
    if (
        isinstance(scale_exponent, bool)
        or not isinstance(scale_exponent, int)
        or scale_exponent < 6
    ):
        raise ValueError("scale_exponent must be an integer at least six")

    level_span = (1 << scale_exponent) - 2
    candidate_count = level_span + 1
    if (
        isinstance(overlap_order, bool)
        or not isinstance(overlap_order, int)
        or overlap_order < 1
        or overlap_order > candidate_count
    ):
        raise ValueError(
            "overlap_order must be between one and candidate_count"
        )

    radicand = 2 * scale_exponent * level_span
    input_length = math.isqrt(radicand)
    if input_length * input_length < radicand:
        input_length += 1
    switch_order = (2 * level_span) // input_length
    maximum_common_gap = (
        0
        if overlap_order == candidate_count
        else level_span // overlap_order
    )
    lcm_bit_length_lower_bound = (
        0
        if maximum_common_gap == 0
        else 5 * ((1 << maximum_common_gap) - 1) + 1
    )
    balanced_prime_bits = (input_length - 1) // 2
    high_weight_charge_lower_bound = (
        lcm_bit_length_lower_bound // balanced_prime_bits
    )
    low_weight_signature_capacity = (
        compact_gap_low_weight_signature_capacity(
            candidate_count,
            overlap_order + 1,
        )
    )
    conservative_population_lower_bound = (
        (1 << (input_length // 2)) // (81 * input_length)
    )
    high_consumes = (
        high_weight_charge_lower_bound
        >= conservative_population_lower_bound
    )
    low_consumes = (
        low_weight_signature_capacity
        >= conservative_population_lower_bound
    )
    return CompactGapEndpointLedger(
        scale_exponent=scale_exponent,
        input_length=input_length,
        candidate_count=candidate_count,
        level_span=level_span,
        logarithmic_scale=candidate_count.bit_length(),
        overlap_order=overlap_order,
        switch_order=switch_order,
        maximum_common_gap=maximum_common_gap,
        lcm_bit_length_lower_bound=lcm_bit_length_lower_bound,
        high_weight_charge_lower_bound=high_weight_charge_lower_bound,
        low_weight_signature_capacity=low_weight_signature_capacity,
        conservative_population_lower_bound=(
            conservative_population_lower_bound
        ),
        high_ledger_consumes_population=high_consumes,
        low_ledger_consumes_population=low_consumes,
        certificate_blocked=high_consumes or low_consumes,
    )


def compact_gap_high_weight_population_upper_bound(
    input_length: int,
    candidate_levels: tuple[int, ...],
    high_weight_threshold: int,
) -> int:
    """Union-bound primes that can hit ``high_weight_threshold`` candidates."""
    if (
        isinstance(input_length, bool)
        or not isinstance(input_length, int)
        or input_length < 9
    ):
        raise ValueError("input_length must be an integer at least nine")
    _validate_levels(candidate_levels)
    if (
        isinstance(high_weight_threshold, bool)
        or not isinstance(high_weight_threshold, int)
        or high_weight_threshold < 2
    ):
        raise ValueError("high_weight_threshold must be at least two")
    candidate_count = len(candidate_levels)
    if high_weight_threshold > candidate_count:
        return 0
    population_prime_bits = (input_length - 1) // 2
    maximum_common_gap = (
        candidate_levels[-1] - candidate_levels[0]
    ) // (high_weight_threshold - 1)
    return (
        math.comb(candidate_count, high_weight_threshold)
        * compact_gap_overlap_bit_bound(maximum_common_gap)
        // population_prime_bits
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


def compact_gap_high_weight_profile(
    input_length: int,
    candidate_levels: tuple[int, ...],
    high_weight_threshold: int,
) -> CompactGapHighWeightProfile:
    """Compute exact wide-span signatures and the high-weight support bound."""
    if (
        isinstance(input_length, bool)
        or not isinstance(input_length, int)
        or input_length < 9
    ):
        raise ValueError("input_length must be an integer at least nine")
    _validate_levels(candidate_levels)
    if (
        isinstance(high_weight_threshold, bool)
        or not isinstance(high_weight_threshold, int)
        or high_weight_threshold < 2
    ):
        raise ValueError("high_weight_threshold must be at least two")
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
    weights = tuple(signature.bit_count() for signature in signatures)
    high_weight_count = sum(
        weight >= high_weight_threshold for weight in weights
    )
    high_weight_bound = compact_gap_high_weight_population_upper_bound(
        input_length,
        candidate_levels,
        high_weight_threshold,
    )
    if high_weight_count > high_weight_bound:
        raise AssertionError("M49 high-weight population bound failed")
    low_weight_capacity = compact_gap_low_weight_signature_capacity(
        len(candidate_levels),
        high_weight_threshold,
    )
    return CompactGapHighWeightProfile(
        input_length=input_length,
        candidate_levels=candidate_levels,
        high_weight_threshold=high_weight_threshold,
        population_size=len(primes),
        candidate_count=len(candidate_levels),
        level_span=candidate_levels[-1] - candidate_levels[0],
        compact_evaluation_level_sum=sum(candidate_levels),
        distinct_signature_count=len(counts),
        zero_signature_count=counts.get(0, 0),
        high_weight_prime_count=high_weight_count,
        maximum_signature_weight=max(weights),
        pair_count=accounting.pair_count,
        separated_pair_count=accounting.separated_pair_count,
        collision_pair_count=accounting.collision_pair_count,
        high_weight_population_upper_bound=high_weight_bound,
        low_weight_signature_capacity=low_weight_capacity,
        theorem_forces_collision=(
            len(primes) - high_weight_bound > low_weight_capacity
        ),
        injective=accounting.injective,
        maximum_bucket_size=max(counts.values()),
    )


def compact_gap_variable_order_profile(
    input_length: int,
    candidate_levels: tuple[int, ...],
) -> CompactGapHighWeightProfile:
    """Evaluate the M51 public-list profile at its balanced overlap order."""
    _validate_levels(candidate_levels)
    overlap_order = compact_gap_balanced_overlap_order(
        len(candidate_levels),
        candidate_levels[-1] - candidate_levels[0],
    )
    return compact_gap_high_weight_profile(
        input_length,
        candidate_levels,
        overlap_order + 1,
    )
