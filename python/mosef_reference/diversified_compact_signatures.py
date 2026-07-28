"""Diversified exceptional-family support signatures for the M31 audit."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from functools import cache
from itertools import combinations

from .baseline import is_prime
from .compact_support_signatures import minimum_candidate_count
from .exceptional_cofactor_schedule import exceptional_cofactor_overlap
from .exceptional_cyclotomic import evaluate_exceptional_cyclotomic
from .length_indexed_cofactor_schedule import balanced_prime_population

PRIMITIVE_EXIT_KINDS = (
    "base",
    "first_stage",
    "second_stage",
    "first_public_bound",
    "second_public_bound",
    "cyclotomic",
    "overlap_resultant",
    "cofactor",
)


@dataclass(frozen=True, order=True)
class ExceptionalSelectorDescriptor:
    """One public exceptional-family descriptor."""

    family: str
    first_factor: int
    second_factor: int
    base: int

    @property
    def key(self) -> str:
        """Return the canonical stable descriptor key."""
        return (
            f"{self.family}:{self.first_factor}:"
            f"{self.second_factor}:{self.base}"
        )


@dataclass(frozen=True)
class NormalizedSupportColumn:
    """One distinct nonconstant support column and all its sources."""

    support_mask: int
    source_keys: tuple[str, ...]
    source_kinds: tuple[str, ...]


@dataclass(frozen=True)
class DiversifiedSelectorProfile:
    """Exact normalized pair accounting on one balanced-prime population."""

    input_length: int
    population_primes: tuple[int, ...]
    descriptor_count: int
    raw_coordinate_count: int
    constant_coordinate_count: int
    duplicate_coordinate_count: int
    normalized_columns: tuple[NormalizedSupportColumn, ...]
    signatures: tuple[int, ...]
    distinct_signature_count: int
    zero_signature_count: int
    pair_count: int
    separated_pair_count: int
    collision_pair_count: int
    maximum_bucket_size: int
    injective: bool
    minimum_separating_column_indices: tuple[int, ...] | None
    cofactor_novel_column_count: int
    cofactor_novel_pair_count: int
    collision_buckets: tuple[tuple[int, ...], ...]


def _validate_input_length(input_length: int) -> None:
    if (
        isinstance(input_length, bool)
        or not isinstance(input_length, int)
        or input_length < 9
    ):
        raise ValueError("input_length must be an integer at least nine")


def diversified_exceptional_selector(
    input_length: int,
) -> tuple[ExceptionalSelectorDescriptor, ...]:
    """Construct every valid ``(family, A, B, g)`` with entries at most ``m``."""
    _validate_input_length(input_length)
    descriptors: list[ExceptionalSelectorDescriptor] = []
    for family in ("phi4", "phi6"):
        for first_factor in range(2, input_length + 1):
            for second_factor in range(2, input_length + 1):
                if first_factor == second_factor:
                    continue
                valid = (
                    family == "phi4"
                    and first_factor % 4 == 3
                    and second_factor % 4 == 3
                ) or (
                    family == "phi6"
                    and first_factor % 6 == 5
                    and second_factor % 6 == 3
                )
                if not valid:
                    continue
                for base in range(2, input_length + 1):
                    descriptors.append(
                        ExceptionalSelectorDescriptor(
                            family=family,
                            first_factor=first_factor,
                            second_factor=second_factor,
                            base=base,
                        )
                    )
    return tuple(descriptors)


@cache
def primitive_exit_mask(
    descriptor: ExceptionalSelectorDescriptor,
    prime: int,
) -> int:
    """Pack the eight primitive charged-exit support bits for one prime."""
    if not isinstance(descriptor, ExceptionalSelectorDescriptor):
        raise ValueError("descriptor must be an ExceptionalSelectorDescriptor")
    if (
        isinstance(prime, bool)
        or not isinstance(prime, int)
        or not is_prime(prime)
    ):
        raise ValueError("prime must be prime")

    overlap = exceptional_cofactor_overlap(
        descriptor.first_factor,
        descriptor.second_factor,
        descriptor.family,
    )
    if descriptor.base % prime == 0:
        return 1

    evaluation = evaluate_exceptional_cyclotomic(
        descriptor.base,
        prime,
        descriptor.first_factor,
        descriptor.second_factor,
        descriptor.family,
    )
    support = (
        False,
        evaluation.first_quotient_gcd == prime,
        evaluation.second_quotient_gcd == prime,
        evaluation.first_public_bound_gcd == prime,
        evaluation.second_public_bound_gcd == prime,
        evaluation.cyclotomic_gcd == prime,
        overlap.cyclotomic_cofactor_resultant % prime == 0,
        evaluation.cofactor_gcd == prime,
    )
    aggregate_hit = evaluation.aggregate_gcd == prime
    if aggregate_hit != (support[5] or support[7]):
        raise AssertionError("aggregate support is not cyclotomic-or-cofactor")
    if support[1] and support[7] and not support[3]:
        raise AssertionError("first-stage/cofactor overlap escaped its bound")
    if support[2] and support[7] and not support[4]:
        raise AssertionError("second-stage/cofactor overlap escaped its bound")
    if support[5] and support[7] and not support[6]:
        raise AssertionError("cyclotomic/cofactor overlap escaped its resultant")
    return sum(1 << index for index, hit in enumerate(support) if hit)


def _raw_support_columns(
    descriptors: tuple[ExceptionalSelectorDescriptor, ...],
    primes: tuple[int, ...],
) -> tuple[tuple[str, str, int], ...]:
    masks: dict[tuple[str, str], int] = {
        (descriptor.key, kind): 0
        for kind in PRIMITIVE_EXIT_KINDS
        for descriptor in descriptors
    }
    for prime_index, prime in enumerate(primes):
        for descriptor in descriptors:
            exit_mask = primitive_exit_mask(descriptor, prime)
            for kind_index, kind in enumerate(PRIMITIVE_EXIT_KINDS):
                if exit_mask & (1 << kind_index):
                    masks[(descriptor.key, kind)] |= 1 << prime_index
    return tuple(
        (descriptor.key, kind, masks[(descriptor.key, kind)])
        for kind in PRIMITIVE_EXIT_KINDS
        for descriptor in descriptors
    )


def _normalize_columns(
    raw_columns: tuple[tuple[str, str, int], ...],
    population_size: int,
) -> tuple[tuple[NormalizedSupportColumn, ...], int, int]:
    full_mask = (1 << population_size) - 1
    by_mask: dict[int, tuple[list[str], list[str]]] = {}
    constant_count = 0
    duplicate_count = 0
    for descriptor_key, kind, support_mask in raw_columns:
        if support_mask in (0, full_mask):
            constant_count += 1
            continue
        source_key = f"{descriptor_key}:{kind}"
        if support_mask in by_mask:
            duplicate_count += 1
            by_mask[support_mask][0].append(source_key)
            by_mask[support_mask][1].append(kind)
        else:
            by_mask[support_mask] = ([source_key], [kind])
    columns = tuple(
        NormalizedSupportColumn(
            support_mask=support_mask,
            source_keys=tuple(sources),
            source_kinds=tuple(kinds),
        )
        for support_mask, (sources, kinds) in by_mask.items()
    )
    return columns, constant_count, duplicate_count


def _signatures(
    columns: tuple[NormalizedSupportColumn, ...],
    population_size: int,
) -> tuple[int, ...]:
    return tuple(
        sum(
            1 << column_index
            for column_index, column in enumerate(columns)
            if column.support_mask & (1 << prime_index)
        )
        for prime_index in range(population_size)
    )


def _collision_count(signatures: tuple[int, ...]) -> int:
    return sum(
        count * (count - 1) // 2 for count in Counter(signatures).values()
    )


def _minimum_separating_subset(
    columns: tuple[NormalizedSupportColumn, ...],
    population_size: int,
) -> tuple[int, ...] | None:
    if population_size < 2:
        return None
    lower_bound = minimum_candidate_count(population_size)
    for size in range(lower_bound, len(columns) + 1):
        for indices in combinations(range(len(columns)), size):
            restricted = tuple(
                sum(
                    1 << output_index
                    for output_index, column_index in enumerate(indices)
                    if columns[column_index].support_mask
                    & (1 << prime_index)
                )
                for prime_index in range(population_size)
            )
            if len(set(restricted)) == population_size:
                return indices
    return None


def diversified_selector_profile(
    input_length: int,
) -> DiversifiedSelectorProfile:
    """Construct, normalize, and audit the public selector at one length."""
    descriptors = diversified_exceptional_selector(input_length)
    primes = balanced_prime_population(input_length)
    if len(primes) < 2:
        raise ValueError("balanced population must contain at least two primes")
    if min(primes) <= input_length:
        raise AssertionError("balanced primes must exceed every selector entry")

    raw_columns = _raw_support_columns(descriptors, primes)
    columns, constant_count, duplicate_count = _normalize_columns(
        raw_columns,
        len(primes),
    )
    signatures = _signatures(columns, len(primes))
    counts = Counter(signatures)
    pair_count = len(primes) * (len(primes) - 1) // 2
    collision_pair_count = _collision_count(signatures)
    buckets = tuple(
        tuple(
            prime
            for prime, prime_signature in zip(primes, signatures, strict=True)
            if prime_signature == signature
        )
        for signature, count in sorted(counts.items())
        if count > 1
    )

    direct_columns = tuple(
        column
        for column in columns
        if "cofactor" not in column.source_kinds
        or any(kind != "cofactor" for kind in column.source_kinds)
    )
    direct_signatures = _signatures(direct_columns, len(primes))
    direct_collisions = _collision_count(direct_signatures)
    cofactor_masks = {
        column.support_mask
        for column in columns
        if "cofactor" in column.source_kinds
        and all(kind == "cofactor" for kind in column.source_kinds)
    }
    cofactor_columns = tuple(
        NormalizedSupportColumn(mask, (), ()) for mask in sorted(cofactor_masks)
    )
    with_cofactors = _signatures(
        direct_columns + cofactor_columns,
        len(primes),
    )
    cofactor_novel_pair_count = (
        direct_collisions - _collision_count(with_cofactors)
    )

    injective = len(counts) == len(primes)
    return DiversifiedSelectorProfile(
        input_length=input_length,
        population_primes=primes,
        descriptor_count=len(descriptors),
        raw_coordinate_count=len(raw_columns),
        constant_coordinate_count=constant_count,
        duplicate_coordinate_count=duplicate_count,
        normalized_columns=columns,
        signatures=signatures,
        distinct_signature_count=len(counts),
        zero_signature_count=counts.get(0, 0),
        pair_count=pair_count,
        separated_pair_count=pair_count - collision_pair_count,
        collision_pair_count=collision_pair_count,
        maximum_bucket_size=max(counts.values()),
        injective=injective,
        minimum_separating_column_indices=(
            _minimum_separating_subset(columns, len(primes))
            if injective
            else None
        ),
        cofactor_novel_column_count=len(cofactor_columns),
        cofactor_novel_pair_count=cofactor_novel_pair_count,
        collision_buckets=buckets,
    )
