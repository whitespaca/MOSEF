"""Clean-room semantic checker for the frozen M41 finite certificate.

This checker intentionally uses only the Python standard library.  It does
not import the M41 generator, the MOSEF reference implementation, or another
certificate checker.  The finite mathematics is reconstructed directly from
the public definitions recorded in THM-004, THM-005, and THM-014.
"""

from __future__ import annotations

import hashlib
import json
from math import isqrt
from pathlib import Path
from typing import Any, NamedTuple

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "m41-length-29-cap-v1.json"

INPUT_LENGTH = 29
PREDECESSOR_CAP = 102
REPAIR_CAP = 103
ADDITIVE_CAP = 105
MULTIPLICATIVE_CAP = 108
TRACKED_PAIR = (18979, 21031)
REPAIR_SOURCE = "phi4:87:95:103:cofactor"
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
    """One public exceptional-family descriptor."""

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


class SemanticReport(NamedTuple):
    """Bounded result returned after a complete semantic validation."""

    population_size: int
    certificate_coordinate_count: int
    certificate_pair_count: int
    predecessor_descriptor_count: int
    new_raw_coordinate_count: int
    summary_sha256: str


def read_artifact(path: Path = ARTIFACT) -> dict[str, Any]:
    """Read one JSON object using only the Python standard library."""
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise AssertionError("M41 artifact must be a JSON object")
    return value


def canonical_hash(value: dict[str, Any]) -> str:
    """Recompute the generator-independent embedded summary hash.

    The four primitive vectors were appended after EXP-0040 computed its
    registered summary hash, so they are intentionally outside this legacy
    hash projection and are checked semantically below.
    """
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
    """Reconstruct every prime p with 2**(m-1) <= p**2 < 2**m."""
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
    """Check the exact DEF-032 public descriptor grammar."""
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


def selector_descriptors(cap: int) -> tuple[Descriptor, ...]:
    """Reconstruct the lexicographically specified public selector."""
    if cap < INPUT_LENGTH:
        raise ValueError("M41 selector cap must be at least the input length")
    descriptors: list[Descriptor] = []
    for family in ("phi4", "phi6"):
        for first in range(2, cap + 1):
            for second in range(2, cap + 1):
                for base in range(2, cap + 1):
                    descriptor = Descriptor(family, first, second, base)
                    if descriptor_is_valid(descriptor, cap):
                        descriptors.append(descriptor)
    return tuple(descriptors)


def parse_source(source: str, cap: int) -> tuple[Descriptor, str]:
    """Parse and validate one canonical primitive-coordinate source."""
    parts = source.split(":")
    if len(parts) != 5:
        raise AssertionError(f"noncanonical M41 source: {source}")
    family, first_text, second_text, base_text, kind = parts
    try:
        descriptor = Descriptor(
            family,
            int(first_text),
            int(second_text),
            int(base_text),
        )
    except ValueError as exc:
        raise AssertionError(f"noninteger M41 source: {source}") from exc
    if not descriptor_is_valid(descriptor, cap):
        raise AssertionError(f"source is outside the cap-{cap} grammar: {source}")
    if kind not in EXIT_KINDS:
        raise AssertionError(f"unknown primitive exit kind: {kind}")
    if source != f"{descriptor.key}:{kind}":
        raise AssertionError(f"noncanonical M41 source: {source}")
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


def geometric_derivative(base: int, count: int, prime: int) -> int:
    """Return the derivative of the geometric sum modulo a prime."""
    base %= prime
    if base == 1:
        return (count * (count - 1) // 2) % prime
    denominator = (base - 1) % prime
    numerator = (
        count * pow(base, count - 1, prime) * denominator
        - (pow(base, count, prime) - 1)
    )
    return numerator * pow(denominator * denominator % prime, -1, prime) % prime


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


def cofactor_residue(descriptor: Descriptor, prime: int) -> int:
    """Evaluate the quotient by division or a simple-root derivative.

    For F(X)=Phi(X)C(X), ordinary modular division gives C(g) when Phi(g)
    is a unit.  At a root of Phi, differentiating gives
    C(g)=F'(g)/Phi'(g), because these large M41 primes do not divide the
    discriminants of Phi4 or Phi6.
    """
    first = descriptor.first_factor
    second = descriptor.second_factor
    base = descriptor.base % prime
    nested_base = pow(base, first, prime)
    first_sum = geometric_sum(base, first, prime)
    second_sum = geometric_sum(nested_base, second, prime)
    coefficient = 1 if descriptor.family == "phi4" else 2
    aggregate = (coefficient * first_sum + second_sum) % prime
    if descriptor.family == "phi4":
        cyclotomic = (base * base + 1) % prime
        cyclotomic_derivative = 2 * base % prime
    else:
        cyclotomic = (base * base - base + 1) % prime
        cyclotomic_derivative = (2 * base - 1) % prime
    if cyclotomic:
        return aggregate * pow(cyclotomic, -1, prime) % prime
    if aggregate:
        raise AssertionError("exceptional numerator missed its cyclotomic factor")
    aggregate_derivative = (
        coefficient * geometric_derivative(base, first, prime)
        + first
        * pow(base, first - 1, prime)
        * geometric_derivative(nested_base, second, prime)
    ) % prime
    if not cyclotomic_derivative:
        raise AssertionError("cyclotomic root is not simple")
    return aggregate_derivative * pow(cyclotomic_derivative, -1, prime) % prime


def primitive_exit_mask(descriptor: Descriptor, prime: int) -> int:
    """Recompute all eight charged primitive support bits."""
    base = descriptor.base % prime
    if base == 0:
        return 1
    first = descriptor.first_factor
    second = descriptor.second_factor
    first_power = pow(base, first, prime)
    first_sum = geometric_sum(base, first, prime)
    second_sum = geometric_sum(first_power, second, prime)
    coefficient = 1 if descriptor.family == "phi4" else 2
    cyclotomic = (
        (base * base + 1) % prime
        if descriptor.family == "phi4"
        else (base * base - base + 1) % prime
    )
    hits = (
        False,
        first_sum == 0,
        second_sum == 0,
        second % prime == 0,
        coefficient * second % prime == 0,
        cyclotomic == 0,
        overlap_resultant(descriptor) % prime == 0,
        cofactor_residue(descriptor, prime) == 0,
    )
    return sum(1 << index for index, hit in enumerate(hits) if hit)


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
    """Reject any mutation of the frozen packed certificate signatures."""
    observed = tuple(int(value) for value in registered)
    if observed != recomputed:
        raise AssertionError("registered M41 restricted signatures changed")


def check_profile_metadata(
    profile: dict[str, Any],
    cap: int,
    population_size: int,
    descriptor_count: int,
    buckets: list[list[int]],
) -> None:
    """Check exact profile fields implied by the semantic certificate."""
    collision_pairs = sum(
        len(bucket) * (len(bucket) - 1) // 2 for bucket in buckets
    )
    distinct = population_size - sum(len(bucket) - 1 for bucket in buckets)
    maximum = max((len(bucket) for bucket in buckets), default=1)
    expected = {
        "selector_cap": cap,
        "population_size": population_size,
        "descriptor_count": descriptor_count,
        "raw_coordinate_count": descriptor_count * len(EXIT_KINDS),
        "distinct_signature_count": distinct,
        "collision_pair_count": collision_pairs,
        "maximum_bucket_size": maximum,
        "collision_buckets": buckets,
    }
    for key, value in expected.items():
        if profile.get(key) != value:
            raise AssertionError(f"wrong cap-{cap} profile field: {key}")


def validate_semantics(artifact: dict[str, Any]) -> SemanticReport:
    """Validate the frozen M41 threshold certificate from public semantics."""
    if artifact.get("schema_version") != "1.0.0":
        raise AssertionError("unsupported M41 schema version")
    if artifact.get("experiment_id") != "EXP-0040":
        raise AssertionError("wrong M41 experiment identifier")
    if artifact.get("input_length") != INPUT_LENGTH:
        raise AssertionError("wrong M41 input length")
    if artifact.get("status") != "PASS":
        raise AssertionError("M41 artifact is not registered as PASS")
    observed_hash = canonical_hash(artifact)
    if artifact.get("summary_sha256") != observed_hash:
        raise AssertionError("M41 canonical summary hash changed")

    certificate = artifact.get("construction_certificate")
    if not isinstance(certificate, dict):
        raise AssertionError("missing M41 construction certificate")
    primes = balanced_prime_population(INPUT_LENGTH)
    registered_primes = tuple(int(value) for value in certificate.get("primes", []))
    if registered_primes != primes:
        raise AssertionError("registered M41 balanced population changed")
    if len(primes) != 685:
        raise AssertionError("unexpected M41 population size")

    primitive_vectors = artifact.get("primitive_exit_vectors")
    if not isinstance(primitive_vectors, list):
        raise AssertionError("missing M41 primitive vectors")
    for vector in primitive_vectors:
        descriptor = Descriptor(
            str(vector["family"]),
            int(vector["first_factor"]),
            int(vector["second_factor"]),
            int(vector["base"]),
        )
        if not descriptor_is_valid(descriptor, REPAIR_CAP):
            raise AssertionError("invalid M41 primitive vector descriptor")
        if primitive_exit_mask(descriptor, int(vector["prime"])) != int(
            vector["expected_mask"]
        ):
            raise AssertionError("M41 primitive exit vector changed")

    source_values = certificate.get("column_sources")
    if not isinstance(source_values, list):
        raise AssertionError("missing M41 certificate sources")
    sources = tuple(str(value) for value in source_values)
    if len(sources) != 1528 or len(set(sources)) != len(sources):
        raise AssertionError("M41 certificate source count or uniqueness changed")
    parsed_sources = tuple(parse_source(source, REPAIR_CAP) for source in sources)
    if any(
        max(descriptor.first_factor, descriptor.second_factor, descriptor.base)
        > PREDECESSOR_CAP
        for descriptor, _kind in parsed_sources[:-1]
    ):
        raise AssertionError("predecessor certificate contains a cap-103 source")
    if sources[-1] != REPAIR_SOURCE:
        raise AssertionError("M41 final repair source changed")

    signatures = [0] * len(primes)
    for column_index, (descriptor, kind) in enumerate(parsed_sources):
        kind_index = EXIT_KINDS.index(kind)
        kind_bit = 1 << kind_index
        for prime_index, prime in enumerate(primes):
            if primitive_exit_mask(descriptor, prime) & kind_bit:
                signatures[prime_index] |= 1 << column_index
    recomputed_signatures = tuple(signatures)
    registered_signatures = certificate.get("restricted_signatures")
    if not isinstance(registered_signatures, list):
        raise AssertionError("missing M41 restricted signatures")
    check_registered_signatures(recomputed_signatures, registered_signatures)

    predecessor_mask = (1 << (len(sources) - 1)) - 1
    predecessor_signatures = tuple(
        signature & predecessor_mask for signature in recomputed_signatures
    )
    predecessor_buckets = collision_buckets(primes, predecessor_signatures)
    if predecessor_buckets != [list(TRACKED_PAIR)]:
        raise AssertionError("M41 certificate predecessor collision changed")
    if len(set(recomputed_signatures)) != len(primes):
        raise AssertionError("M41 cap-103 certificate is not injective")

    tracked_indices = tuple(primes.index(prime) for prime in TRACKED_PAIR)
    tracked_signatures = tuple(
        recomputed_signatures[index] for index in tracked_indices
    )
    if certificate.get("tracked_primes") != list(TRACKED_PAIR):
        raise AssertionError("M41 tracked predecessor pair changed")
    if certificate.get("tracked_restricted_signatures") != list(
        tracked_signatures
    ):
        raise AssertionError("M41 tracked signatures changed")
    repair_pattern = tuple(
        int(bool(signature & (1 << (len(sources) - 1))))
        for signature in tracked_signatures
    )
    if repair_pattern != (0, 1):
        raise AssertionError("M41 repair bit does not separate the tracked pair")
    if certificate.get("new_source_pattern") != list(repair_pattern):
        raise AssertionError("M41 registered repair pattern changed")
    if certificate.get("minimum_new_coordinate_count") != 1:
        raise AssertionError("M41 minimum repair count changed")
    if certificate.get("unique_new_pair_source") != REPAIR_SOURCE:
        raise AssertionError("M41 unique repair source metadata changed")

    predecessor_descriptors = selector_descriptors(PREDECESSOR_CAP)
    predecessor_pair_masks = tuple(
        tuple(primitive_exit_mask(descriptor, prime) for prime in TRACKED_PAIR)
        for descriptor in predecessor_descriptors
    )
    if any(left != right for left, right in predecessor_pair_masks):
        raise AssertionError("tracked M41 pair does not collide in the raw predecessor")

    repair_descriptors = selector_descriptors(REPAIR_CAP)
    predecessor_keys = {descriptor.key for descriptor in predecessor_descriptors}
    added_descriptors = tuple(
        descriptor
        for descriptor in repair_descriptors
        if descriptor.key not in predecessor_keys
    )
    distinguishing_sources: list[str] = []
    for descriptor in added_descriptors:
        left_mask = primitive_exit_mask(descriptor, TRACKED_PAIR[0])
        right_mask = primitive_exit_mask(descriptor, TRACKED_PAIR[1])
        difference = left_mask ^ right_mask
        for kind_index, kind in enumerate(EXIT_KINDS):
            if difference & (1 << kind_index):
                distinguishing_sources.append(f"{descriptor.key}:{kind}")
    if distinguishing_sources != [REPAIR_SOURCE]:
        raise AssertionError("M41 unique cap-103 repair coordinate changed")

    cap_descriptors = {
        PREDECESSOR_CAP: predecessor_descriptors,
        REPAIR_CAP: repair_descriptors,
        ADDITIVE_CAP: selector_descriptors(ADDITIVE_CAP),
        MULTIPLICATIVE_CAP: selector_descriptors(MULTIPLICATIVE_CAP),
    }
    profile_buckets = {
        PREDECESSOR_CAP: [list(TRACKED_PAIR)],
        REPAIR_CAP: [],
        ADDITIVE_CAP: [],
        MULTIPLICATIVE_CAP: [],
    }
    raw_profiles = artifact.get("registered_raw_profiles")
    if not isinstance(raw_profiles, list) or len(raw_profiles) != 4:
        raise AssertionError("M41 raw-profile registry changed")
    by_cap = {int(profile["selector_cap"]): profile for profile in raw_profiles}
    if set(by_cap) != set(cap_descriptors):
        raise AssertionError("M41 registered cap set changed")
    for cap, descriptors in cap_descriptors.items():
        check_profile_metadata(
            by_cap[cap],
            cap,
            len(primes),
            len(descriptors),
            profile_buckets[cap],
        )
    check_profile_metadata(
        artifact["predecessor_profile"],
        PREDECESSOR_CAP,
        len(primes),
        len(predecessor_descriptors),
        [list(TRACKED_PAIR)],
    )
    check_profile_metadata(
        artifact["repair_profile"],
        REPAIR_CAP,
        len(primes),
        len(repair_descriptors),
        [],
    )
    if artifact["additive_success_profile"] != by_cap[ADDITIVE_CAP]:
        raise AssertionError("M41 additive profile projection changed")
    if artifact["multiplicative_success_profile"] != by_cap[MULTIPLICATIVE_CAP]:
        raise AssertionError("M41 multiplicative profile projection changed")
    repair_profile = artifact["repair_profile"]
    normalization_total = (
        int(repair_profile["constant_coordinate_count"])
        + int(repair_profile["duplicate_coordinate_count"])
        + int(repair_profile["normalized_coordinate_count"])
    )
    if normalization_total != int(repair_profile["raw_coordinate_count"]):
        raise AssertionError("M41 normalization partition is inconsistent")

    if artifact.get("exact_length_29_threshold") != REPAIR_CAP:
        raise AssertionError("M41 exact threshold changed")
    pair_count = len(primes) * (len(primes) - 1) // 2
    return SemanticReport(
        population_size=len(primes),
        certificate_coordinate_count=len(sources),
        certificate_pair_count=pair_count,
        predecessor_descriptor_count=len(predecessor_descriptors),
        new_raw_coordinate_count=len(added_descriptors) * len(EXIT_KINDS),
        summary_sha256=observed_hash,
    )


def main() -> int:
    """Run the independent semantic validation."""
    report = validate_semantics(read_artifact())
    print(
        "M85 independent M41 semantic checker: PASS "
        f"({report.population_size} primes, "
        f"{report.certificate_coordinate_count} certificate coordinates, "
        f"{report.certificate_pair_count} pairs, "
        f"{report.predecessor_descriptor_count} predecessor descriptors, "
        f"{report.new_raw_coordinate_count} new raw coordinates)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
