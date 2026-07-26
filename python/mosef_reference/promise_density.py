"""Exact combined p-1/p+1 signatures and finite density bounds for M8."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from math import comb, isqrt

from .baseline import is_prime


@dataclass(frozen=True)
class CombinedDensityAnalysis:
    """Exact pair counts and theorem bounds for one prime set and schedule."""

    prime_count: int
    hit_count: int
    total_pairs: int
    promised_pairs: int
    hit_intersecting_pairs: int
    divisor_hit_bound: int
    square_root_hit_bound: int


@dataclass(frozen=True)
class BitLengthDivisorBudget:
    """Exact integer parameters for the BAR-004 bit-length divisor budget."""

    bit_length: int
    split_threshold: int
    large_multiplicity_bound: int
    one_length_bound: int
    monotone_bound: int


@dataclass(frozen=True)
class BoundaryDivisorBudget:
    """Exact integer parameters for the BAR-006 boundary divisor budget."""

    bit_length: int
    logarithm_scale: int
    iterated_logarithm_scale: int
    split_threshold: int
    large_multiplicity_bound: int
    one_length_bound: int
    monotone_bound: int


@dataclass(frozen=True)
class PrimorialSchedule:
    """Exact accounting for the product of the first ``prime_count`` primes."""

    prime_count: int
    primes: tuple[int, ...]
    exponent: int
    bit_length: int
    divisor_count: int
    binary_multiplication_nodes: int


def _normalized_exponents(exponents: tuple[int, ...] | list[int]) -> tuple[int, ...]:
    """Return a sorted, duplicate-free positive exponent family."""
    normalized = tuple(sorted(set(exponents)))
    if not normalized or any(
        isinstance(value, bool) or value <= 0 for value in normalized
    ):
        raise ValueError("exponents must contain positive integers")
    return normalized


def _validate_odd_prime(value: int, name: str) -> None:
    """Reject values outside the odd-prime domain."""
    if isinstance(value, bool) or value < 3 or value % 2 == 0 or not is_prime(value):
        raise ValueError(f"{name} must be an odd prime")


def combined_signature(
    prime: int,
    exponents: tuple[int, ...] | list[int],
) -> tuple[tuple[bool, bool], ...]:
    """Return the schedule's ``p-1`` and ``p+1`` divisibility bits."""
    _validate_odd_prime(prime, "prime")
    normalized = _normalized_exponents(exponents)
    return tuple(
        (exponent % (prime - 1) == 0, exponent % (prime + 1) == 0)
        for exponent in normalized
    )


def combined_asymmetry(
    left_prime: int,
    right_prime: int,
    exponents: tuple[int, ...] | list[int],
) -> bool:
    """Return whether a p-1 or p+1 divisibility coordinate separates the pair."""
    if left_prime == right_prime:
        raise ValueError("prime factors must be distinct")
    return combined_signature(left_prime, exponents) != combined_signature(
        right_prime, exponents
    )


def direct_combined_asymmetry(
    left_prime: int,
    right_prime: int,
    exponents: tuple[int, ...] | list[int],
) -> bool:
    """Search both orientations and channels directly, without signatures."""
    if left_prime == right_prime:
        raise ValueError("prime factors must be distinct")
    _validate_odd_prime(left_prime, "left_prime")
    _validate_odd_prime(right_prime, "right_prime")
    normalized = _normalized_exponents(exponents)
    for exponent in normalized:
        for offset in (-1, 1):
            left_hit = exponent % (left_prime + offset) == 0
            right_hit = exponent % (right_prime + offset) == 0
            if left_hit != right_hit:
                return True
    return False


def divisor_count(value: int) -> int:
    """Return the exact number of positive divisors of ``value``."""
    if isinstance(value, bool) or value <= 0:
        raise ValueError("value must be positive")
    count = 0
    for divisor in range(1, isqrt(value) + 1):
        if value % divisor == 0:
            count += 1 if divisor * divisor == value else 2
    return count


def exponent_bit_length(value: int) -> int:
    """Return the ordinary unsigned binary representation length."""
    if isinstance(value, bool) or value <= 0:
        raise ValueError("value must be positive")
    return value.bit_length()


def _one_length_divisor_budget(bit_length: int) -> tuple[int, int, int]:
    """Return ``(threshold, large multiplicity, B(bit_length))`` exactly."""
    if isinstance(bit_length, bool) or bit_length <= 0:
        raise ValueError("bit_length must be positive")
    threshold = isqrt(bit_length)
    large_base = threshold + 1
    limit = 1 << bit_length
    power = 1
    large_multiplicity = 0
    while power * large_base < limit:
        power *= large_base
        large_multiplicity += 1
    bound = (bit_length + 1) ** threshold * (1 << large_multiplicity)
    return threshold, large_multiplicity, bound


def bit_length_divisor_budget(bit_length: int) -> BitLengthDivisorBudget:
    """Return the exact BAR-004 budget and its monotone envelope."""
    threshold, large_multiplicity, one_length_bound = (
        _one_length_divisor_budget(bit_length)
    )
    monotone_bound = max(
        _one_length_divisor_budget(current)[2]
        for current in range(1, bit_length + 1)
    )
    return BitLengthDivisorBudget(
        bit_length=bit_length,
        split_threshold=threshold,
        large_multiplicity_bound=large_multiplicity,
        one_length_bound=one_length_bound,
        monotone_bound=monotone_bound,
    )


def _one_boundary_divisor_budget(
    bit_length: int,
) -> tuple[int, int, int, int, int]:
    """Return the exact one-length parameters used by DEF-011."""
    if isinstance(bit_length, bool) or bit_length <= 0:
        raise ValueError("bit_length must be positive")
    logarithm_scale = bit_length.bit_length()
    iterated_logarithm_scale = logarithm_scale.bit_length()
    denominator = (
        logarithm_scale * logarithm_scale * iterated_logarithm_scale
    )
    threshold = max(1, bit_length // denominator)
    large_base = threshold + 1
    limit = 1 << bit_length
    power = 1
    large_multiplicity = 0
    while power * large_base < limit:
        power *= large_base
        large_multiplicity += 1
    bound = (bit_length + 1) ** threshold * (1 << large_multiplicity)
    return (
        logarithm_scale,
        iterated_logarithm_scale,
        threshold,
        large_multiplicity,
        bound,
    )


def boundary_divisor_budget(bit_length: int) -> BoundaryDivisorBudget:
    """Return DEF-011's exact budget and monotone envelope."""
    (
        logarithm_scale,
        iterated_logarithm_scale,
        threshold,
        large_multiplicity,
        one_length_bound,
    ) = _one_boundary_divisor_budget(bit_length)
    monotone_bound = max(
        _one_boundary_divisor_budget(current)[4]
        for current in range(1, bit_length + 1)
    )
    return BoundaryDivisorBudget(
        bit_length=bit_length,
        logarithm_scale=logarithm_scale,
        iterated_logarithm_scale=iterated_logarithm_scale,
        split_threshold=threshold,
        large_multiplicity_bound=large_multiplicity,
        one_length_bound=one_length_bound,
        monotone_bound=monotone_bound,
    )


def first_primes(count: int) -> tuple[int, ...]:
    """Return the first ``count`` primes in increasing order."""
    if isinstance(count, bool) or count <= 0:
        raise ValueError("count must be positive")
    primes: list[int] = []
    candidate = 2
    while len(primes) < count:
        if is_prime(candidate):
            primes.append(candidate)
        candidate = 3 if candidate == 2 else candidate + 2
    return tuple(primes)


def primorial_schedule(count: int) -> PrimorialSchedule:
    """Construct and exactly cost the first-``count``-primes exponent."""
    primes = first_primes(count)
    exponent = 1
    for prime in primes:
        exponent *= prime
    bit_length = exponent.bit_length()
    binary_multiplication_nodes = (
        bit_length - 1 + exponent.bit_count() - 1
    )
    return PrimorialSchedule(
        prime_count=count,
        primes=primes,
        exponent=exponent,
        bit_length=bit_length,
        divisor_count=1 << count,
        binary_multiplication_nodes=binary_multiplication_nodes,
    )


def primorial_divisors(count: int) -> tuple[int, ...]:
    """Enumerate every divisor of the first-``count``-primes primorial."""
    divisors = [1]
    for prime in first_primes(count):
        divisors.extend(value * prime for value in tuple(divisors))
    return tuple(sorted(divisors))


def positive_divisors(value: int) -> tuple[int, ...]:
    """Return every positive divisor in increasing order."""
    if isinstance(value, bool) or value <= 0:
        raise ValueError("value must be positive")
    lower: list[int] = []
    upper: list[int] = []
    for divisor in range(1, isqrt(value) + 1):
        if value % divisor != 0:
            continue
        lower.append(divisor)
        paired = value // divisor
        if paired != divisor:
            upper.append(paired)
    return tuple(lower + list(reversed(upper)))


def global_hit_primes(
    exponents: tuple[int, ...] | list[int],
) -> tuple[int, ...]:
    """Return every odd prime with a nonzero signature for the schedule."""
    normalized = _normalized_exponents(exponents)
    candidates: set[int] = set()
    for exponent in normalized:
        for divisor in positive_divisors(exponent):
            for prime in (divisor - 1, divisor + 1):
                if prime >= 3 and prime % 2 == 1 and is_prime(prime):
                    candidates.add(prime)
    return tuple(sorted(candidates))


def hit_primes(
    primes: tuple[int, ...] | list[int],
    exponents: tuple[int, ...] | list[int],
) -> tuple[int, ...]:
    """Return primes with at least one nonzero combined-signature bit."""
    normalized_primes = tuple(sorted(set(primes)))
    if not normalized_primes:
        raise ValueError("primes must be nonempty")
    normalized_exponents = _normalized_exponents(exponents)
    return tuple(
        prime
        for prime in normalized_primes
        if any(
            bit
            for coordinate in combined_signature(prime, normalized_exponents)
            for bit in coordinate
        )
    )


def analyze_combined_density(
    primes: tuple[int, ...] | list[int],
    exponents: tuple[int, ...] | list[int],
) -> CombinedDensityAnalysis:
    """Enumerate pair success and calculate the exact BAR-003 upper bounds."""
    normalized_primes = tuple(sorted(set(primes)))
    if len(normalized_primes) < 2:
        raise ValueError("primes must contain at least two distinct values")
    for prime in normalized_primes:
        _validate_odd_prime(prime, "prime")
    normalized_exponents = _normalized_exponents(exponents)
    hits = hit_primes(normalized_primes, normalized_exponents)
    prime_count = len(normalized_primes)
    hit_count = len(hits)
    total_pairs = comb(prime_count, 2)
    promised_pairs = sum(
        combined_asymmetry(left, right, normalized_exponents)
        for left, right in combinations(normalized_primes, 2)
    )
    hit_intersecting_pairs = total_pairs - comb(prime_count - hit_count, 2)
    divisor_hit_bound = 2 * sum(
        divisor_count(exponent) for exponent in normalized_exponents
    )
    maximum = max(normalized_exponents)
    square_root_hit_bound = 4 * len(normalized_exponents) * isqrt(maximum)
    if isqrt(maximum) ** 2 != maximum:
        square_root_hit_bound += 4 * len(normalized_exponents)
    return CombinedDensityAnalysis(
        prime_count=prime_count,
        hit_count=hit_count,
        total_pairs=total_pairs,
        promised_pairs=promised_pairs,
        hit_intersecting_pairs=hit_intersecting_pairs,
        divisor_hit_bound=divisor_hit_bound,
        square_root_hit_bound=square_root_hit_bound,
    )
