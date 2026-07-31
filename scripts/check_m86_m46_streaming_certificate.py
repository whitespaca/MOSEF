"""Streaming clean-room checker for the frozen M46 finite certificate.

This executable uses only the Python standard library. It does not import an
M31--M46 generator, a project number-theory module, or an earlier checker.
The certificate matrix is never materialized: one coordinate is evaluated at
a time while only one packed signature per population prime remains live.
"""

from __future__ import annotations

import hashlib
import json
import time
from collections.abc import Iterator
from math import isqrt
from pathlib import Path
from typing import Any, NamedTuple

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "m46-length-34-cap-v1.json"

INPUT_LENGTH = 34
PREDECESSOR_CAP = 200
REPAIR_CAP = 201
TRACKED_PAIR = (97927, 99527)
REPAIR_SOURCE = "phi6:149:201:45:cofactor"
EXIT_KINDS = (
    "base",
    "first_stage",
    "second_stage",
    "first_public_bound",
    "second_public_bound",
    "cyclotomic",
    "overlap_resultant",
    "cofactor",
)


class Descriptor(NamedTuple):
    """One public order-four or order-six descriptor."""

    family: str
    first_factor: int
    second_factor: int
    base: int

    @property
    def key(self) -> str:
        """Return the canonical descriptor key."""
        return (
            f"{self.family}:{self.first_factor}:"
            f"{self.second_factor}:{self.base}"
        )


class StreamingReport(NamedTuple):
    """Bounded result returned after complete M46 validation."""

    population_size: int
    certificate_coordinate_count: int
    certificate_pair_count: int
    certificate_evaluation_count: int
    predecessor_descriptor_count: int
    new_descriptor_count: int
    new_raw_coordinate_count: int
    peak_signature_slots: int
    summary_sha256: str


def read_artifact(path: Path = ARTIFACT) -> dict[str, Any]:
    """Read one JSON object."""
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise AssertionError("M46 artifact must be a JSON object")
    return value


def canonical_hash(value: dict[str, Any]) -> str:
    """Recompute the legacy summary hash without trusting its serializer."""
    canonical = dict(value)
    canonical.pop("summary_sha256", None)
    canonical.pop("primitive_exit_vectors", None)
    encoded = json.dumps(
        canonical,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def balanced_prime_population(input_length: int) -> tuple[int, ...]:
    """Reconstruct all primes p with 2**(m-1) <= p**2 < 2**m."""
    if input_length < 2:
        raise ValueError("input_length must be at least two")
    lower_square = 1 << (input_length - 1)
    lower = isqrt(lower_square)
    if lower * lower < lower_square:
        lower += 1
    upper = isqrt((1 << input_length) - 1)

    prime_flags = bytearray(b"\x01") * (upper + 1)
    prime_flags[:2] = b"\x00\x00"
    for candidate in range(2, isqrt(upper) + 1):
        if not prime_flags[candidate]:
            continue
        start = candidate * candidate
        count = (upper - start) // candidate + 1
        prime_flags[start : upper + 1 : candidate] = b"\x00" * count
    return tuple(
        candidate
        for candidate in range(lower, upper + 1)
        if prime_flags[candidate]
    )


def descriptor_is_valid(descriptor: Descriptor, cap: int) -> bool:
    """Check the exact public descriptor grammar."""
    first = descriptor.first_factor
    second = descriptor.second_factor
    base = descriptor.base
    if not (
        2 <= first <= cap
        and 2 <= second <= cap
        and 2 <= base <= cap
        and first != second
    ):
        return False
    if descriptor.family == "phi4":
        return first % 4 == 3 and second % 4 == 3
    if descriptor.family == "phi6":
        return first % 6 == 5 and second % 6 == 3
    return False


def iter_selector_descriptors(cap: int) -> Iterator[Descriptor]:
    """Yield the selector directly from its congruence grammar."""
    if cap < INPUT_LENGTH:
        raise ValueError("M46 selector cap must be at least the input length")
    phi4_values = range(3, cap + 1, 4)
    for first in phi4_values:
        for second in range(3, cap + 1, 4):
            if first == second:
                continue
            for base in range(2, cap + 1):
                yield Descriptor("phi4", first, second, base)
    for first in range(5, cap + 1, 6):
        for second in range(3, cap + 1, 6):
            for base in range(2, cap + 1):
                yield Descriptor("phi6", first, second, base)


def descriptor_count(cap: int) -> int:
    """Count the streamed grammar without retaining descriptors."""
    return sum(1 for _descriptor in iter_selector_descriptors(cap))


def parse_source(source: str, cap: int) -> tuple[Descriptor, str]:
    """Parse and validate one canonical primitive-coordinate source."""
    parts = source.split(":")
    if len(parts) != 5:
        raise AssertionError(f"noncanonical M46 source: {source}")
    family, first_text, second_text, base_text, kind = parts
    try:
        descriptor = Descriptor(
            family,
            int(first_text),
            int(second_text),
            int(base_text),
        )
    except ValueError as exc:
        raise AssertionError(f"noninteger M46 source: {source}") from exc
    if not descriptor_is_valid(descriptor, cap):
        raise AssertionError(f"source is outside the cap-{cap} grammar: {source}")
    if kind not in EXIT_KINDS:
        raise AssertionError(f"unknown primitive exit kind: {kind}")
    if source != f"{descriptor.key}:{kind}":
        raise AssertionError(f"noncanonical M46 source: {source}")
    return descriptor, kind


def geometric_sum(base: int, count: int, prime: int) -> int:
    """Return 1 + base + ... + base**(count-1) modulo a prime."""
    base %= prime
    if base == 1:
        return count % prime
    return (
        (pow(base, count, prime) - 1)
        * pow(base - 1, -1, prime)
    ) % prime


def overlap_resultant(descriptor: Descriptor) -> int:
    """Reconstruct the exact cyclotomic/cofactor resultant."""
    first = descriptor.first_factor
    second = descriptor.second_factor
    if descriptor.family == "phi4":
        constant_numerator = first * (second + 2) + 1
        linear_numerator = first * (second - 2) + 1
        if constant_numerator % 4 or linear_numerator % 4:
            raise AssertionError("phi4 remainder coefficients are not integral")
        constant = constant_numerator // 4
        linear = linear_numerator // 4
        return constant * constant + linear * linear
    residual = first * (second - 2) + 1
    linear_numerator = first * (second + 4) + 4
    if (2 * residual) % 3 or linear_numerator % 3:
        raise AssertionError("phi6 remainder coefficients are not integral")
    constant = -(2 * residual // 3)
    linear = linear_numerator // 3
    return constant * constant + constant * linear + linear * linear


def cyclotomic_residue(descriptor: Descriptor, prime: int) -> int:
    """Evaluate Phi4 or Phi6 at the public base modulo a prime."""
    base = descriptor.base % prime
    if descriptor.family == "phi4":
        return (base * base + 1) % prime
    return (base * base - base + 1) % prime


def cofactor_residue(descriptor: Descriptor, prime: int) -> int:
    """Evaluate the M46 exceptional cofactor by finite-field division."""
    base = descriptor.base % prime
    first = descriptor.first_factor
    first_power = pow(base, first, prime)
    first_sum = geometric_sum(base, first, prime)
    second_sum = geometric_sum(
        first_power,
        descriptor.second_factor,
        prime,
    )
    coefficient = 1 if descriptor.family == "phi4" else 2
    aggregate = (coefficient * first_sum + second_sum) % prime
    cyclotomic = cyclotomic_residue(descriptor, prime)
    if not cyclotomic:
        raise AssertionError("M46 cyclotomic denominator unexpectedly vanished")
    return aggregate * pow(cyclotomic, -1, prime) % prime


def primitive_exit_hit(descriptor: Descriptor, kind: str, prime: int) -> bool:
    """Evaluate only the requested primitive coordinate."""
    base = descriptor.base % prime
    if kind == "base":
        return base == 0
    if base == 0:
        return False
    first = descriptor.first_factor
    second = descriptor.second_factor
    if kind == "first_stage":
        return geometric_sum(base, first, prime) == 0
    if kind == "second_stage":
        return geometric_sum(pow(base, first, prime), second, prime) == 0
    if kind == "first_public_bound":
        return second % prime == 0
    if kind == "second_public_bound":
        coefficient = 1 if descriptor.family == "phi4" else 2
        return coefficient * second % prime == 0
    if kind == "cyclotomic":
        return cyclotomic_residue(descriptor, prime) == 0
    if kind == "overlap_resultant":
        return overlap_resultant(descriptor) % prime == 0
    if kind == "cofactor":
        return cofactor_residue(descriptor, prime) == 0
    raise AssertionError(f"unknown primitive exit kind: {kind}")


def primitive_exit_mask(descriptor: Descriptor, prime: int) -> int:
    """Evaluate all eight charged primitive exits once."""
    base = descriptor.base % prime
    if base == 0:
        return 1
    first = descriptor.first_factor
    second = descriptor.second_factor
    first_power = pow(base, first, prime)
    first_sum = geometric_sum(base, first, prime)
    second_sum = geometric_sum(first_power, second, prime)
    coefficient = 1 if descriptor.family == "phi4" else 2
    hits = (
        False,
        first_sum == 0,
        second_sum == 0,
        second % prime == 0,
        coefficient * second % prime == 0,
        cyclotomic_residue(descriptor, prime) == 0,
        overlap_resultant(descriptor) % prime == 0,
        cofactor_residue(descriptor, prime) == 0,
    )
    return sum(1 << index for index, hit in enumerate(hits) if hit)


def stream_certificate_signatures(
    primes: tuple[int, ...],
    sources: tuple[tuple[Descriptor, str], ...],
) -> tuple[tuple[int, ...], int]:
    """Stream coordinates into one packed signature per population prime."""
    signatures = [0] * len(primes)
    evaluation_count = 0
    for column_index, (descriptor, kind) in enumerate(sources):
        column_bit = 1 << column_index
        for prime_index, prime in enumerate(primes):
            if primitive_exit_hit(descriptor, kind, prime):
                signatures[prime_index] |= column_bit
            evaluation_count += 1
    return tuple(signatures), evaluation_count


def collision_buckets(
    primes: tuple[int, ...],
    signatures: tuple[int, ...],
) -> list[list[int]]:
    """Return all equal-signature buckets in population order."""
    if len(primes) != len(signatures):
        raise AssertionError("prime/signature length mismatch")
    grouped: dict[int, list[int]] = {}
    for prime, signature in zip(primes, signatures, strict=True):
        grouped.setdefault(signature, []).append(prime)
    return [bucket for bucket in grouped.values() if len(bucket) > 1]


def check_registered_signatures(
    recomputed: tuple[int, ...],
    registered: list[Any],
) -> None:
    """Reject any mutation of the packed certificate signatures."""
    observed = tuple(int(value) for value in registered)
    if observed != recomputed:
        raise AssertionError("registered M46 restricted signatures changed")


def check_profile_metadata(
    profile: dict[str, Any],
    cap: int,
    population_size: int,
    descriptors: int,
    selected_coordinates: int,
    buckets: list[list[int]],
) -> None:
    """Check the profile fields implied by the semantic reconstruction."""
    collision_pairs = sum(
        len(bucket) * (len(bucket) - 1) // 2 for bucket in buckets
    )
    expected = {
        "selector_cap": cap,
        "population_size": population_size,
        "descriptor_count": descriptors,
        "raw_coordinate_count": descriptors * len(EXIT_KINDS),
        "selected_coordinate_count": selected_coordinates,
        "distinct_signature_count": population_size
        - sum(len(bucket) - 1 for bucket in buckets),
        "collision_pair_count": collision_pairs,
        "maximum_bucket_size": max(
            (len(bucket) for bucket in buckets),
            default=1,
        ),
        "collision_buckets": buckets,
    }
    for key, value in expected.items():
        if profile.get(key) != value:
            raise AssertionError(f"wrong cap-{cap} profile field: {key}")


def validate_primitive_vectors(artifact: dict[str, Any]) -> None:
    """Recompute all registered primitive vectors."""
    vectors = artifact.get("primitive_exit_vectors")
    if not isinstance(vectors, list) or len(vectors) != 4:
        raise AssertionError("M46 primitive-vector registry changed")
    for vector in vectors:
        descriptor = Descriptor(
            str(vector["family"]),
            int(vector["first_factor"]),
            int(vector["second_factor"]),
            int(vector["base"]),
        )
        if not descriptor_is_valid(descriptor, REPAIR_CAP):
            raise AssertionError("invalid M46 primitive vector descriptor")
        if primitive_exit_mask(descriptor, int(vector["prime"])) != int(
            vector["expected_mask"]
        ):
            raise AssertionError("M46 primitive exit vector changed")


def validate_semantics(artifact: dict[str, Any]) -> StreamingReport:
    """Validate the frozen M46 threshold certificate from public semantics."""
    if artifact.get("schema_version") != "1.0.0":
        raise AssertionError("unsupported M46 schema version")
    if artifact.get("experiment_id") != "EXP-0045":
        raise AssertionError("wrong M46 experiment identifier")
    if artifact.get("input_length") != INPUT_LENGTH:
        raise AssertionError("wrong M46 input length")
    if artifact.get("status") != "PASS":
        raise AssertionError("M46 artifact is not registered as PASS")
    observed_hash = canonical_hash(artifact)
    if artifact.get("summary_sha256") != observed_hash:
        raise AssertionError("M46 canonical summary hash changed")

    certificate = artifact.get("construction_certificate")
    if not isinstance(certificate, dict):
        raise AssertionError("missing M46 construction certificate")
    primes = balanced_prime_population(INPUT_LENGTH)
    registered_primes = tuple(int(value) for value in certificate.get("primes", []))
    if registered_primes != primes:
        raise AssertionError("registered M46 balanced population changed")
    if len(primes) != 3299:
        raise AssertionError("unexpected M46 population size")
    if primes[0] <= REPAIR_CAP * REPAIR_CAP + 1:
        raise AssertionError("M46 unit-division boundary is not discharged")

    validate_primitive_vectors(artifact)

    source_values = certificate.get("column_sources")
    if not isinstance(source_values, list):
        raise AssertionError("missing M46 certificate sources")
    source_names = tuple(str(value) for value in source_values)
    if len(source_names) != 3298 or len(set(source_names)) != len(source_names):
        raise AssertionError("M46 certificate source count or uniqueness changed")
    parsed_sources = tuple(
        parse_source(source, REPAIR_CAP) for source in source_names
    )
    predecessor_columns = int(certificate.get("predecessor_column_count", -1))
    if predecessor_columns != 3297:
        raise AssertionError("M46 predecessor column count changed")
    if any(
        max(descriptor.first_factor, descriptor.second_factor, descriptor.base)
        > PREDECESSOR_CAP
        for descriptor, _kind in parsed_sources[:predecessor_columns]
    ):
        raise AssertionError("predecessor certificate contains a cap-201 source")
    if source_names[predecessor_columns:] != (REPAIR_SOURCE,):
        raise AssertionError("M46 final repair source changed")
    if certificate.get("repair_sources") != [REPAIR_SOURCE]:
        raise AssertionError("M46 repair-source registry changed")
    if certificate.get("minimum_new_coordinate_count") != 1:
        raise AssertionError("M46 minimum repair count changed")

    recomputed_signatures, evaluation_count = stream_certificate_signatures(
        primes,
        parsed_sources,
    )
    registered_signatures = certificate.get("restricted_signatures")
    if not isinstance(registered_signatures, list):
        raise AssertionError("missing M46 restricted signatures")
    check_registered_signatures(recomputed_signatures, registered_signatures)

    predecessor_mask = (1 << predecessor_columns) - 1
    predecessor_signatures = tuple(
        signature & predecessor_mask for signature in recomputed_signatures
    )
    predecessor_buckets = collision_buckets(primes, predecessor_signatures)
    if predecessor_buckets != [list(TRACKED_PAIR)]:
        raise AssertionError("M46 certificate predecessor collision changed")
    if len(set(recomputed_signatures)) != len(primes):
        raise AssertionError("M46 cap-201 certificate is not injective")

    if certificate.get("tracked_primes") != list(TRACKED_PAIR):
        raise AssertionError("M46 tracked pair changed")
    tracked_indices = tuple(primes.index(prime) for prime in TRACKED_PAIR)
    tracked_predecessor = [
        predecessor_signatures[index] for index in tracked_indices
    ]
    if certificate.get("tracked_predecessor_signatures") != tracked_predecessor:
        raise AssertionError("M46 tracked predecessor signatures changed")
    repair_pattern = [
        int(bool(recomputed_signatures[index] & (1 << predecessor_columns)))
        for index in tracked_indices
    ]
    if repair_pattern != [1, 0]:
        raise AssertionError("M46 repair bit does not separate the tracked pair")
    if certificate.get("new_source_patterns") != [repair_pattern]:
        raise AssertionError("M46 repair pattern registry changed")
    if certificate.get("tracked_repair_signatures") != repair_pattern:
        raise AssertionError("M46 tracked repair signatures changed")

    predecessor_descriptors = 0
    for descriptor in iter_selector_descriptors(PREDECESSOR_CAP):
        predecessor_descriptors += 1
        left = primitive_exit_mask(descriptor, TRACKED_PAIR[0])
        right = primitive_exit_mask(descriptor, TRACKED_PAIR[1])
        if left != right:
            raise AssertionError("tracked pair separates in the raw predecessor")
    if predecessor_descriptors != 704261:
        raise AssertionError("M46 cap-200 descriptor count changed")

    new_descriptors = 0
    distinguishing_sources: list[str] = []
    for descriptor in iter_selector_descriptors(REPAIR_CAP):
        if max(
            descriptor.first_factor,
            descriptor.second_factor,
            descriptor.base,
        ) != REPAIR_CAP:
            continue
        new_descriptors += 1
        left_mask = primitive_exit_mask(descriptor, TRACKED_PAIR[0])
        right_mask = primitive_exit_mask(descriptor, TRACKED_PAIR[1])
        difference = left_mask ^ right_mask
        for kind_index, kind in enumerate(EXIT_KINDS):
            if difference & (1 << kind_index):
                distinguishing_sources.append(f"{descriptor.key}:{kind}")
    if new_descriptors != 10139:
        raise AssertionError("M46 new descriptor count changed")
    if distinguishing_sources != [REPAIR_SOURCE]:
        raise AssertionError("M46 unique cap-201 repair coordinate changed")

    repair_descriptors = predecessor_descriptors + new_descriptors
    public_profiles = artifact.get("registered_public_profiles")
    if not isinstance(public_profiles, list):
        raise AssertionError("M46 public-profile registry changed")
    public_by_cap = {
        int(profile["selector_cap"]): profile for profile in public_profiles
    }
    check_profile_metadata(
        public_by_cap[PREDECESSOR_CAP],
        PREDECESSOR_CAP,
        len(primes),
        predecessor_descriptors,
        predecessor_columns,
        [list(TRACKED_PAIR)],
    )
    check_profile_metadata(
        artifact["predecessor_profile"],
        PREDECESSOR_CAP,
        len(primes),
        predecessor_descriptors,
        predecessor_columns,
        [list(TRACKED_PAIR)],
    )
    check_profile_metadata(
        artifact["repair_profile"],
        REPAIR_CAP,
        len(primes),
        repair_descriptors,
        len(source_names),
        [],
    )
    transition_profiles = artifact.get("transition_profiles")
    if not isinstance(transition_profiles, list):
        raise AssertionError("M46 transition-profile registry changed")
    transition_by_cap = {
        int(profile["selector_cap"]): profile for profile in transition_profiles
    }
    check_profile_metadata(
        transition_by_cap[PREDECESSOR_CAP],
        PREDECESSOR_CAP,
        len(primes),
        predecessor_descriptors,
        predecessor_columns,
        [list(TRACKED_PAIR)],
    )
    check_profile_metadata(
        transition_by_cap[REPAIR_CAP],
        REPAIR_CAP,
        len(primes),
        repair_descriptors,
        len(source_names),
        [],
    )
    if transition_by_cap[REPAIR_CAP].get("new_descriptor_count") != new_descriptors:
        raise AssertionError("M46 transition descriptor count changed")

    counts = artifact.get("counts")
    if not isinstance(counts, dict):
        raise AssertionError("M46 count registry changed")
    pair_count = len(primes) * (len(primes) - 1) // 2
    expected_counts = {
        "balanced_primes": len(primes),
        "balanced_prime_pairs": pair_count,
        "construction_coordinates": len(source_names),
        "construction_local_exit_profiles": evaluation_count,
        "predecessor_coordinate_count": predecessor_columns,
        "public_cap_maximum_descriptors": predecessor_descriptors,
        "repair_cap_descriptors": repair_descriptors,
        "repair_cap_raw_coordinates": repair_descriptors * len(EXIT_KINDS),
        "transition_new_descriptors": new_descriptors,
        "repair_raw_coordinate_checks": new_descriptors * len(EXIT_KINDS),
        "minimum_new_coordinate_count": 1,
        "certificate_pair_checks": pair_count,
    }
    for key, value in expected_counts.items():
        if counts.get(key) != value:
            raise AssertionError(f"wrong M46 count field: {key}")

    if artifact.get("exact_length_34_threshold") != REPAIR_CAP:
        raise AssertionError("M46 exact threshold changed")
    if artifact["repaired_additive_schedule"].get("cap") != "m+167":
        raise AssertionError("M46 additive schedule changed")
    if (
        artifact["repaired_multiplicative_schedule"].get("working_witness")
        != "ceil(53m/9)"
    ):
        raise AssertionError("M46 multiplicative schedule changed")

    return StreamingReport(
        population_size=len(primes),
        certificate_coordinate_count=len(source_names),
        certificate_pair_count=pair_count,
        certificate_evaluation_count=evaluation_count,
        predecessor_descriptor_count=predecessor_descriptors,
        new_descriptor_count=new_descriptors,
        new_raw_coordinate_count=new_descriptors * len(EXIT_KINDS),
        peak_signature_slots=len(primes),
        summary_sha256=observed_hash,
    )


def main() -> int:
    """Run the complete streaming validation."""
    started = time.perf_counter()
    report = validate_semantics(read_artifact())
    elapsed = time.perf_counter() - started
    print(
        "M86 streaming M46 semantic checker: PASS "
        f"({report.population_size} primes, "
        f"{report.certificate_coordinate_count} coordinates, "
        f"{report.certificate_evaluation_count} streamed evaluations, "
        f"{report.predecessor_descriptor_count} predecessor descriptors, "
        f"{report.new_raw_coordinate_count} new raw coordinates, "
        f"{report.peak_signature_slots} peak signature slots, "
        f"{elapsed:.2f} s)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
