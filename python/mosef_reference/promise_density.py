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
