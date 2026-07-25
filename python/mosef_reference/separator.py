"""Exact small-input semantics for multiplicative order separators."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from math import gcd


class CandidateKind(str, Enum):
    """Exhaustive outcomes for one multiplicative separator candidate."""

    DIRECT_FACTOR = "direct_factor"
    INVALID_BASE = "invalid_base"
    MISS = "miss"
    FACTOR = "factor"
    SIMULTANEOUS_COLLISION = "simultaneous_collision"


@dataclass(frozen=True)
class CandidateOutcome:
    """Result of evaluating ``gcd(g**d - 1, n)`` after the base GCD branch."""

    kind: CandidateKind
    factor: int | None
    residue: int | None


def prime_factorization(n: int) -> tuple[tuple[int, int], ...]:
    """Return the exact prime-power factorization of ``n`` by trial division."""
    if n < 2:
        raise ValueError("n must be at least 2")
    factors: list[tuple[int, int]] = []
    remaining = n
    divisor = 2
    while divisor <= remaining // divisor:
        exponent = 0
        while remaining % divisor == 0:
            remaining //= divisor
            exponent += 1
        if exponent:
            factors.append((divisor, exponent))
        divisor = 3 if divisor == 2 else divisor + 2
    if remaining > 1:
        factors.append((remaining, 1))
    return tuple(factors)


def multiplicative_order_mod_prime(g: int, prime: int) -> int:
    """Return the multiplicative order of ``g`` modulo the given prime."""
    factorization = prime_factorization(prime) if prime >= 2 else ()
    if len(factorization) != 1 or factorization[0][1] != 1:
        raise ValueError("prime must be prime")
    if gcd(g, prime) != 1:
        raise ValueError("g must be coprime to prime")
    order = prime - 1
    for divisor, _ in prime_factorization(order) if order > 1 else ():
        while order % divisor == 0 and pow(g, order // divisor, prime) == 1:
            order //= divisor
    return order


def order_support(n: int, g: int, d: int) -> tuple[int, ...]:
    """Return the distinct prime divisors whose orders divide ``d``."""
    if d <= 0:
        raise ValueError("d must be positive")
    if gcd(g, n) != 1:
        raise ValueError("g must be coprime to n")
    return tuple(
        prime
        for prime, _ in prime_factorization(n)
        if d % multiplicative_order_mod_prime(g, prime) == 0
    )


def capped_valuation_profile(n: int, g: int, d: int) -> tuple[tuple[int, int, int], ...]:
    """Return ``(p, e_p, min(e_p, v_p(g**d - 1)))`` for every ``p**e_p | n``."""
    if d <= 0:
        raise ValueError("d must be positive")
    if gcd(g, n) != 1:
        raise ValueError("g must be coprime to n")
    profile: list[tuple[int, int, int]] = []
    for prime, exponent in prime_factorization(n):
        prime_power = prime**exponent
        difference = (pow(g, d, prime_power) - 1) % prime_power
        valuation = 0
        if difference == 0:
            valuation = exponent
        else:
            while valuation < exponent and difference % prime == 0:
                difference //= prime
                valuation += 1
        profile.append((prime, exponent, valuation))
    return tuple(profile)


def support_is_separator(n: int, g: int, d: int) -> bool:
    """Return whether the order support is nonempty and proper."""
    primes = tuple(prime for prime, _ in prime_factorization(n))
    support = order_support(n, g, d)
    return bool(support) and len(support) < len(primes)


def valuation_predicts_factor(n: int, g: int, d: int) -> bool:
    """Apply the exact valuation criterion for a nontrivial candidate GCD."""
    profile = capped_valuation_profile(n, g, d)
    return any(valuation > 0 for _, _, valuation in profile) and any(
        valuation < exponent for _, exponent, valuation in profile
    )


def evaluate_separator_candidate(n: int, g: int, d: int) -> CandidateOutcome:
    """Evaluate one candidate and report every terminal branch explicitly."""
    if n < 2:
        raise ValueError("n must be at least 2")
    if d <= 0:
        raise ValueError("d must be positive")
    reduced_base = g % n
    base_gcd = gcd(reduced_base, n)
    if 1 < base_gcd < n:
        return CandidateOutcome(CandidateKind.DIRECT_FACTOR, base_gcd, None)
    if base_gcd == n:
        return CandidateOutcome(CandidateKind.INVALID_BASE, None, None)

    residue = pow(reduced_base, d, n)
    candidate_gcd = gcd((residue - 1) % n, n)
    if candidate_gcd == 1:
        return CandidateOutcome(CandidateKind.MISS, None, residue)
    if candidate_gcd == n:
        return CandidateOutcome(CandidateKind.SIMULTANEOUS_COLLISION, None, residue)
    return CandidateOutcome(CandidateKind.FACTOR, candidate_gcd, residue)
