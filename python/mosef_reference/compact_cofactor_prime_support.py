"""Prime-support semantics for the M29 compact length-indexed cofactor."""

from __future__ import annotations

from dataclasses import dataclass

from .baseline import is_prime
from .exceptional_cyclotomic import compact_exceptional_cofactor_residue
from .length_indexed_cofactor_schedule import balanced_prime_population


@dataclass(frozen=True)
class Phi4PrimeDivisibilityProfile:
    """Exact divisibility data for one prime and one compact cofactor."""

    level: int
    prime: int
    second_factor: int
    exponent: int
    cofactor_residue: int
    criterion_residue: int
    divides: bool
    rule: str


@dataclass(frozen=True)
class Phi4PairOutcome:
    """GCD outcome for a square-free pair without materializing the cofactor."""

    level: int
    first_prime: int
    second_prime: int
    first_hit: bool
    second_hit: bool
    status: str
    factor: int | None


@dataclass(frozen=True)
class Phi4BalancedSupportProfile:
    """Exact signature-cut accounting on one balanced prime population."""

    input_length: int
    population_size: int
    hit_primes: tuple[int, ...]
    missed_primes: tuple[int, ...]
    hit_prime_count: int
    pair_count: int
    proper_pair_count: int
    full_collision_pair_count: int
    unit_pair_count: int
    maximum_proper_pair_count: int
    universal_pair_coverage_possible: bool


def _validate_level(level: int) -> None:
    if isinstance(level, bool) or not isinstance(level, int) or level < 2:
        raise ValueError("level must be an integer at least two")


def phi4_prime_divisibility_profile(
    level: int,
    prime: int,
) -> Phi4PrimeDivisibilityProfile:
    """Return the exact M29 divisibility rule for ``C_level(2)`` modulo a prime."""
    _validate_level(level)
    if (
        isinstance(prime, bool)
        or not isinstance(prime, int)
        or not is_prime(prime)
    ):
        raise ValueError("prime must be prime")

    second_factor = (1 << level) + 3
    exponent = 3 * (1 << level) + 5
    cofactor_residue = compact_exceptional_cofactor_residue(
        2,
        prime,
        3,
        second_factor,
        "phi4",
    )
    criterion_residue = (pow(2, exponent, prime) + 3) % prime
    if prime == 2:
        divides = True
        rule = "two_adic"
    elif prime == 3:
        divides = False
        rule = "three_exception"
    elif prime == 5:
        divides = level % 4 == 2
        rule = "five_quotient"
    elif prime == 7:
        divides = level % 3 == 2
        rule = "seven_quotient"
    else:
        divides = criterion_residue == 0
        rule = "generic_congruence"
    if divides != (cofactor_residue == 0):
        raise AssertionError("compact residue disagrees with the divisibility rule")
    return Phi4PrimeDivisibilityProfile(
        level=level,
        prime=prime,
        second_factor=second_factor,
        exponent=exponent,
        cofactor_residue=cofactor_residue,
        criterion_residue=criterion_residue,
        divides=divides,
        rule=rule,
    )


def phi4_pair_outcome(
    level: int,
    first_prime: int,
    second_prime: int,
) -> Phi4PairOutcome:
    """Classify ``gcd(C_level(2), first_prime * second_prime)`` exactly."""
    if first_prime == second_prime:
        raise ValueError("pair primes must be distinct")
    first = phi4_prime_divisibility_profile(level, first_prime)
    second = phi4_prime_divisibility_profile(level, second_prime)
    if first.divides and second.divides:
        status = "full_collision"
        factor = None
    elif first.divides:
        status = "proper_factor"
        factor = first_prime
    elif second.divides:
        status = "proper_factor"
        factor = second_prime
    else:
        status = "unit"
        factor = None
    return Phi4PairOutcome(
        level=level,
        first_prime=first_prime,
        second_prime=second_prime,
        first_hit=first.divides,
        second_hit=second.divides,
        status=status,
        factor=factor,
    )


def phi4_balanced_support_profile(
    input_length: int,
) -> Phi4BalancedSupportProfile:
    """Account for the single compact candidate on the M28 balanced population."""
    _validate_level(input_length)
    primes = balanced_prime_population(input_length)
    if len(primes) < 2:
        raise ValueError("balanced population must contain at least two primes")
    hit_primes = tuple(
        prime
        for prime in primes
        if phi4_prime_divisibility_profile(input_length, prime).divides
    )
    hit_set = set(hit_primes)
    missed_primes = tuple(prime for prime in primes if prime not in hit_set)
    population_size = len(primes)
    hit_prime_count = len(hit_primes)
    missed_count = len(missed_primes)
    pair_count = population_size * (population_size - 1) // 2
    proper_pair_count = hit_prime_count * missed_count
    full_collision_pair_count = hit_prime_count * (hit_prime_count - 1) // 2
    unit_pair_count = missed_count * (missed_count - 1) // 2
    return Phi4BalancedSupportProfile(
        input_length=input_length,
        population_size=population_size,
        hit_primes=hit_primes,
        missed_primes=missed_primes,
        hit_prime_count=hit_prime_count,
        pair_count=pair_count,
        proper_pair_count=proper_pair_count,
        full_collision_pair_count=full_collision_pair_count,
        unit_pair_count=unit_pair_count,
        maximum_proper_pair_count=(population_size * population_size) // 4,
        universal_pair_coverage_possible=(
            pair_count == proper_pair_count
        ),
    )
