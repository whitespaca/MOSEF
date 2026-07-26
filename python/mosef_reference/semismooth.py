"""Exact small-input semantics for the M3 semismooth promise class.

The factor-aware witness functions and exhaustive residue search are analysis
oracles.  The Las Vegas splitter samples residues without using the
factorization.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd, lcm
from random import Random

from .baseline import is_prime, perfect_power
from .separator import (
    CandidateKind,
    evaluate_separator_candidate,
    multiplicative_order_mod_prime,
    prime_factorization,
)


@dataclass(frozen=True)
class SemismoothWitness:
    """A fixed-base analysis witness retained for the M3 negative result."""

    p: int
    q: int
    base: int
    multiplier: int
    exponent: int


@dataclass(frozen=True)
class SemismoothFactor:
    """One factor returned by the executable family."""

    factor: int
    base: int
    multiplier: int | None
    exponent: int | None


@dataclass(frozen=True)
class SemismoothAsymmetryWitness:
    """A factor-aware witness for the noncircular M3 promise."""

    p: int
    q: int
    multiplier: int
    exponent: int


def stage_one_exponent(bound: int) -> int:
    """Return ``lcm(1, ..., bound)`` exactly."""
    if bound < 1:
        raise ValueError("bound must be positive")
    exponent = 1
    for value in range(2, bound + 1):
        exponent = lcm(exponent, value)
    return exponent


def find_semismooth_witness(
    n: int,
    base_bound: int,
    smooth_bound: int,
    cofactor_bound: int,
) -> SemismoothWitness | None:
    """Find a factor-aware witness, for analysis only."""
    if n < 2:
        raise ValueError("n must be at least 2")
    if base_bound < 2 or smooth_bound < 1 or cofactor_bound < 1:
        raise ValueError("bounds must satisfy A >= 2, B >= 1, R >= 1")
    primes = tuple(prime for prime, _ in prime_factorization(n))
    if len(primes) < 2:
        return None
    stage_exponent = stage_one_exponent(smooth_bound)
    for base in range(2, min(base_bound, n - 1) + 1):
        if gcd(base, n) != 1:
            continue
        for multiplier in range(1, cofactor_bound + 1):
            exponent = multiplier * stage_exponent
            for p in primes:
                if exponent % (p - 1) != 0:
                    continue
                for q in primes:
                    if q == p:
                        continue
                    if exponent % multiplicative_order_mod_prime(base, q) != 0:
                        return SemismoothWitness(p, q, base, multiplier, exponent)
    return None


def find_semismooth_asymmetry_witness(
    n: int,
    smooth_bound: int,
    cofactor_bound: int,
) -> SemismoothAsymmetryWitness | None:
    """Find a ``p-1``/``q-1`` asymmetry witness, for analysis only."""
    witnesses = semismooth_asymmetry_witnesses(
        n,
        smooth_bound,
        cofactor_bound,
    )
    return witnesses[0] if witnesses else None


def semismooth_asymmetry_witnesses(
    n: int,
    smooth_bound: int,
    cofactor_bound: int,
) -> tuple[SemismoothAsymmetryWitness, ...]:
    """Enumerate every ordered bounded asymmetry witness, for analysis only."""
    if n < 2:
        raise ValueError("n must be at least 2")
    if smooth_bound < 1 or cofactor_bound < 1:
        raise ValueError("bounds must satisfy B >= 1 and R >= 1")
    primes = tuple(prime for prime, _ in prime_factorization(n))
    if len(primes) < 2:
        return ()
    witnesses: list[SemismoothAsymmetryWitness] = []
    stage_exponent = stage_one_exponent(smooth_bound)
    for multiplier in range(1, cofactor_bound + 1):
        exponent = multiplier * stage_exponent
        for p in primes:
            if exponent % (p - 1) != 0:
                continue
            for q in primes:
                if q != p and exponent % (q - 1) != 0:
                    witnesses.append(
                        SemismoothAsymmetryWitness(
                            p,
                            q,
                            multiplier,
                            exponent,
                        )
                    )
    return tuple(witnesses)


def try_semismooth_factor(
    n: int,
    base_bound: int,
    smooth_bound: int,
    cofactor_bound: int,
) -> SemismoothFactor | None:
    """Try the explicit ``[2,A] x [1,R]`` semismooth exponent family."""
    if n < 2:
        raise ValueError("n must be at least 2")
    if base_bound < 2 or smooth_bound < 1 or cofactor_bound < 1:
        raise ValueError("bounds must satisfy A >= 2, B >= 1, R >= 1")
    stage_exponent = stage_one_exponent(smooth_bound)
    for base in range(2, min(base_bound, n - 1) + 1):
        base_gcd = gcd(base, n)
        if 1 < base_gcd < n:
            return SemismoothFactor(base_gcd, base, None, None)
        if base_gcd == n:
            continue
        for multiplier in range(1, cofactor_bound + 1):
            exponent = multiplier * stage_exponent
            outcome = evaluate_separator_candidate(n, base, exponent)
            if outcome.kind == CandidateKind.FACTOR:
                assert outcome.factor is not None
                return SemismoothFactor(outcome.factor, base, multiplier, exponent)
    return None


def _factor_from_residue(n: int, residue: int, exponent: int) -> int | None:
    """Return the factor exposed by one residue/exponent trial."""
    base_gcd = gcd(residue, n)
    if 1 < base_gcd < n:
        return base_gcd
    if base_gcd == n:
        return None
    factor = gcd(pow(residue, exponent, n) - 1, n)
    return factor if 1 < factor < n else None


def successful_residue_count(n: int, exponent: int) -> int:
    """Count exactly the successful residues in ``{0, ..., n-1}``."""
    if n < 2 or exponent < 1:
        raise ValueError("n must be at least 2 and exponent positive")
    return sum(
        _factor_from_residue(n, residue, exponent) is not None
        for residue in range(n)
    )


def try_randomized_semismooth_factor(
    n: int,
    smooth_bound: int,
    cofactor_bound: int,
    rng: Random,
    cycles: int,
) -> SemismoothFactor | None:
    """Run a bounded prefix of the Las Vegas split procedure.

    A ``None`` result is only an exhausted experiment budget, never a
    compositeness or promise-membership decision.
    """
    if n < 2:
        raise ValueError("n must be at least 2")
    if smooth_bound < 1 or cofactor_bound < 1 or cycles < 1:
        raise ValueError("bounds and cycles must be positive")
    stage_exponent = stage_one_exponent(smooth_bound)
    for _ in range(cycles):
        for multiplier in range(1, cofactor_bound + 1):
            exponent = multiplier * stage_exponent
            residue = rng.randrange(n)
            factor = _factor_from_residue(n, residue, exponent)
            if factor is not None:
                return SemismoothFactor(
                    factor,
                    residue,
                    multiplier,
                    exponent,
                )
    return None


def try_exhaustive_semismooth_factor(
    n: int,
    smooth_bound: int,
    cofactor_bound: int,
) -> SemismoothFactor | None:
    """Exhaust all residues as a finite correctness oracle, not an algorithm."""
    if n < 2:
        raise ValueError("n must be at least 2")
    if smooth_bound < 1 or cofactor_bound < 1:
        raise ValueError("bounds must be positive")
    stage_exponent = stage_one_exponent(smooth_bound)
    for multiplier in range(1, cofactor_bound + 1):
        exponent = multiplier * stage_exponent
        for residue in range(n):
            factor = _factor_from_residue(n, residue, exponent)
            if factor is not None:
                return SemismoothFactor(
                    factor,
                    residue,
                    multiplier,
                    exponent,
                )
    return None


def factor_semismooth_promised(
    n: int,
    base_bound: int,
    smooth_bound: int,
    cofactor_bound: int,
) -> tuple[int, ...] | None:
    """Completely factor a small promised input, or return ``None``."""
    if n < 1:
        raise ValueError("n must be positive")
    if n == 1:
        return ()
    if is_prime(n):
        return (n,)
    power = perfect_power(n)
    if power is not None:
        base, exponent = power
        base_factors = factor_semismooth_promised(
            base,
            base_bound,
            smooth_bound,
            cofactor_bound,
        )
        if base_factors is None:
            return None
        return tuple(sorted(base_factors * exponent))

    result = try_semismooth_factor(n, base_bound, smooth_bound, cofactor_bound)
    if result is None:
        return None
    left = factor_semismooth_promised(
        result.factor,
        base_bound,
        smooth_bound,
        cofactor_bound,
    )
    right = factor_semismooth_promised(
        n // result.factor,
        base_bound,
        smooth_bound,
        cofactor_bound,
    )
    if left is None or right is None:
        return None
    return tuple(sorted(left + right))


def factor_semismooth_oracle(
    n: int,
    smooth_bound: int,
    cofactor_bound: int,
) -> tuple[int, ...] | None:
    """Factor through exhaustive residue search for bounded M3 validation."""
    if n < 1:
        raise ValueError("n must be positive")
    if n == 1:
        return ()
    if is_prime(n):
        return (n,)
    power = perfect_power(n)
    if power is not None:
        base, exponent = power
        base_factors = factor_semismooth_oracle(
            base,
            smooth_bound,
            cofactor_bound,
        )
        if base_factors is None:
            return None
        return tuple(sorted(base_factors * exponent))

    result = try_exhaustive_semismooth_factor(
        n,
        smooth_bound,
        cofactor_bound,
    )
    if result is None:
        return None
    left = factor_semismooth_oracle(
        result.factor,
        smooth_bound,
        cofactor_bound,
    )
    right = factor_semismooth_oracle(
        n // result.factor,
        smooth_bound,
        cofactor_bound,
    )
    if left is None or right is None:
        return None
    return tuple(sorted(left + right))


def _divisors(n: int) -> tuple[int, ...]:
    divisors = [1]
    for prime, exponent in prime_factorization(n):
        prior = tuple(divisors)
        power = 1
        for _ in range(exponent):
            power *= prime
            divisors.extend(value * power for value in prior)
    return tuple(sorted(divisors))


def is_hereditarily_semismooth_separable(
    n: int,
    base_bound: int,
    smooth_bound: int,
    cofactor_bound: int,
) -> bool:
    """Check the factor-aware hereditary promise for a small analysis input."""
    if n < 2:
        raise ValueError("n must be at least 2")
    for divisor in _divisors(n):
        if divisor < 4 or is_prime(divisor) or perfect_power(divisor) is not None:
            continue
        if (
            find_semismooth_witness(
                divisor,
                base_bound,
                smooth_bound,
                cofactor_bound,
            )
            is None
        ):
            return False
    return True


def is_hereditarily_semismooth_asymmetric(
    n: int,
    smooth_bound: int,
    cofactor_bound: int,
) -> bool:
    """Check the hereditary ``p-1``/``q-1`` promise on a small input."""
    if n < 2:
        raise ValueError("n must be at least 2")
    for divisor in _divisors(n):
        if divisor < 4 or is_prime(divisor) or perfect_power(divisor) is not None:
            continue
        if (
            find_semismooth_asymmetry_witness(
                divisor,
                smooth_bound,
                cofactor_bound,
            )
            is None
        ):
            return False
    return True
