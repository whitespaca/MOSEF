"""Multi-candidate prime-support signatures for the M30 audit."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

from .baseline import is_prime
from .length_indexed_cofactor_schedule import balanced_prime_population


@dataclass(frozen=True)
class SignaturePairAccounting:
    """Exact pair-separation accounting for a finite binary signature map."""

    candidate_count: int
    population_size: int
    signature_counts: tuple[tuple[int, int], ...]
    distinct_signature_count: int
    zero_signature_count: int
    pair_count: int
    separated_pair_count: int
    collision_pair_count: int
    minimum_collision_pair_count: int
    information_candidate_lower_bound: int
    coverage_candidate_lower_bound: int
    injective: bool
    covers_every_population_member: bool


@dataclass(frozen=True)
class Phi4PrefixSignatureProfile:
    """Signature accounting for the public prefix ``C_2, ..., C_m``."""

    input_length: int
    candidate_levels: tuple[int, ...]
    population_size: int
    signature_counts: tuple[tuple[int, int], ...]
    distinct_signature_count: int
    zero_signature_count: int
    covered_prime_count: int
    pair_count: int
    separated_pair_count: int
    collision_pair_count: int
    information_candidate_lower_bound: int
    injective: bool


def _validate_population_size(population_size: int) -> None:
    if (
        isinstance(population_size, bool)
        or not isinstance(population_size, int)
        or population_size < 2
    ):
        raise ValueError("population_size must be an integer at least two")


def _validate_candidate_count(candidate_count: int) -> None:
    if (
        isinstance(candidate_count, bool)
        or not isinstance(candidate_count, int)
        or candidate_count < 0
    ):
        raise ValueError("candidate_count must be a nonnegative integer")


def minimum_candidate_count(
    population_size: int,
    *,
    require_nonzero: bool = False,
) -> int:
    """Return the binary information lower bound for injective signatures."""
    _validate_population_size(population_size)
    if not isinstance(require_nonzero, bool):
        raise ValueError("require_nonzero must be boolean")
    if require_nonzero:
        return population_size.bit_length()
    return (population_size - 1).bit_length()


def minimum_signature_collision_count(
    population_size: int,
    candidate_count: int,
    *,
    require_nonzero: bool = False,
) -> int:
    """Return the least possible number of equal-signature prime pairs."""
    _validate_population_size(population_size)
    _validate_candidate_count(candidate_count)
    if not isinstance(require_nonzero, bool):
        raise ValueError("require_nonzero must be boolean")
    cell_count = (1 << candidate_count) - int(require_nonzero)
    if cell_count <= 0:
        raise ValueError("no nonzero signature exists with zero candidates")
    quotient, remainder = divmod(population_size, cell_count)
    return (
        (cell_count - remainder) * quotient * (quotient - 1) // 2
        + remainder * quotient * (quotient + 1) // 2
    )


def signature_pair_accounting(
    signatures: tuple[int, ...],
    candidate_count: int,
) -> SignaturePairAccounting:
    """Count separated and colliding pairs from their exact signatures."""
    _validate_candidate_count(candidate_count)
    if len(signatures) < 2:
        raise ValueError("signatures must contain at least two values")
    signature_limit = 1 << candidate_count
    if any(
        isinstance(signature, bool)
        or not isinstance(signature, int)
        or signature < 0
        or signature >= signature_limit
        for signature in signatures
    ):
        raise ValueError("every signature must fit the candidate count")

    counts = Counter(signatures)
    population_size = len(signatures)
    pair_count = population_size * (population_size - 1) // 2
    collision_pair_count = sum(
        multiplicity * (multiplicity - 1) // 2
        for multiplicity in counts.values()
    )
    zero_signature_count = counts.get(0, 0)
    return SignaturePairAccounting(
        candidate_count=candidate_count,
        population_size=population_size,
        signature_counts=tuple(sorted(counts.items())),
        distinct_signature_count=len(counts),
        zero_signature_count=zero_signature_count,
        pair_count=pair_count,
        separated_pair_count=pair_count - collision_pair_count,
        collision_pair_count=collision_pair_count,
        minimum_collision_pair_count=minimum_signature_collision_count(
            population_size,
            candidate_count,
        ),
        information_candidate_lower_bound=minimum_candidate_count(
            population_size
        ),
        coverage_candidate_lower_bound=minimum_candidate_count(
            population_size,
            require_nonzero=True,
        ),
        injective=len(counts) == population_size,
        covers_every_population_member=zero_signature_count == 0,
    )


def materialized_support_signature(
    candidates: tuple[int, ...],
    prime: int,
) -> int:
    """Return the support signature of explicit nonzero integer candidates."""
    if not candidates:
        raise ValueError("candidates must be nonempty")
    if any(
        isinstance(candidate, bool)
        or not isinstance(candidate, int)
        or candidate == 0
        for candidate in candidates
    ):
        raise ValueError("candidates must be nonzero integers")
    if (
        isinstance(prime, bool)
        or not isinstance(prime, int)
        or not is_prime(prime)
    ):
        raise ValueError("prime must be prime")
    return sum(
        1 << index
        for index, candidate in enumerate(candidates)
        if candidate % prime == 0
    )


def _phi4_level_divides_prime(level: int, prime: int) -> bool:
    if prime == 2:
        return True
    if prime == 3:
        return False
    if prime == 5:
        return level % 4 == 2
    if prime == 7:
        return level % 3 == 2
    exponent = 3 * (1 << level) + 5
    return (pow(2, exponent, prime) + 3) % prime == 0


def phi4_compact_signature(
    candidate_levels: tuple[int, ...],
    prime: int,
) -> int:
    """Return the M29 ``C_level`` support signature of one prime."""
    if not candidate_levels:
        raise ValueError("candidate_levels must be nonempty")
    if any(
        isinstance(level, bool)
        or not isinstance(level, int)
        or level < 2
        for level in candidate_levels
    ):
        raise ValueError("candidate levels must be integers at least two")
    if (
        isinstance(prime, bool)
        or not isinstance(prime, int)
        or not is_prime(prime)
    ):
        raise ValueError("prime must be prime")
    return sum(
        1 << index
        for index, level in enumerate(candidate_levels)
        if _phi4_level_divides_prime(level, prime)
    )


def phi4_prefix_signature_profile(
    input_length: int,
) -> Phi4PrefixSignatureProfile:
    """Audit the canonical public prefix ``C_2, ..., C_input_length``."""
    if (
        isinstance(input_length, bool)
        or not isinstance(input_length, int)
        or input_length < 4
    ):
        raise ValueError("input_length must be an integer at least four")
    candidate_levels = tuple(range(2, input_length + 1))
    primes = balanced_prime_population(input_length)
    if len(primes) < 2:
        raise ValueError("balanced population must contain at least two primes")
    signatures = tuple(
        phi4_compact_signature(candidate_levels, prime) for prime in primes
    )
    accounting = signature_pair_accounting(signatures, len(candidate_levels))
    return Phi4PrefixSignatureProfile(
        input_length=input_length,
        candidate_levels=candidate_levels,
        population_size=accounting.population_size,
        signature_counts=accounting.signature_counts,
        distinct_signature_count=accounting.distinct_signature_count,
        zero_signature_count=accounting.zero_signature_count,
        covered_prime_count=(
            accounting.population_size - accounting.zero_signature_count
        ),
        pair_count=accounting.pair_count,
        separated_pair_count=accounting.separated_pair_count,
        collision_pair_count=accounting.collision_pair_count,
        information_candidate_lower_bound=(
            accounting.information_candidate_lower_bound
        ),
        injective=accounting.injective,
    )
