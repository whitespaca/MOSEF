"""Clean-room semantic checker for all 26 frozen finite-threshold rows.

The executable uses only the Python standard library. It does not import a
project number-theory module, an M31--M50 generator, or an earlier checker.
It reconstructs the public descriptor grammar, balanced-prime populations,
certificate signatures, predecessor collisions, and every certified
incremental repair directly from the frozen JSON artifacts.
"""

from __future__ import annotations

import hashlib
import json
import time
from collections.abc import Iterator, Mapping, Sequence
from math import isqrt
from pathlib import Path
from typing import NamedTuple, cast

ROOT = Path(__file__).resolve().parents[1]
SUMMARY_PATH = ROOT / "schemas" / "m50-finite-threshold-summary-v1.json"
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
SOURCE_BY_LENGTH = (
    *(("schemas/m31-diversified-compact-signature-vectors-v1.json",) * 7),
    *(("schemas/m32-widened-selector-cap-v1.json",) * 5),
    "schemas/m33-linear-cap-recurrence-v1.json",
    "schemas/m34-next-envelope-v1.json",
    "schemas/m35-next-envelope-v1.json",
    "schemas/m36-distinct-cap-v1.json",
    "schemas/m37-length-25-cap-v1.json",
    "schemas/m38-length-26-cap-v1.json",
    "schemas/m39-length-27-cap-v1.json",
    "schemas/m40-length-28-cap-v1.json",
    "schemas/m41-length-29-cap-v1.json",
    "schemas/m42-length-30-cap-v1.json",
    "schemas/m43-length-31-cap-v1.json",
    "schemas/m44-length-32-cap-v1.json",
    "schemas/m45-length-33-cap-v1.json",
    "schemas/m46-length-34-cap-v1.json",
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

    @property
    def cap(self) -> int:
        """Return the first selector cap admitting the descriptor."""
        return max(self.first_factor, self.second_factor, self.base)


class RowReport(NamedTuple):
    """Logical work and result counts for one reconstructed row."""

    input_length: int
    population_size: int
    selector_cap: int
    descriptor_count: int
    certificate_coordinates: int
    certificate_evaluations: int
    raw_mask_evaluations: int
    repair_minimum: int | None


class SemanticReport(NamedTuple):
    """Aggregate result of the complete table-wide reconstruction."""

    rows: tuple[RowReport, ...]
    source_count: int
    population_total: int
    certificate_coordinates: int
    certificate_evaluations: int
    raw_mask_evaluations: int


def read_json(path: Path) -> dict[str, object]:
    """Read one JSON object without a project parser."""
    decoded = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(decoded, dict):
        raise AssertionError(f"{path.name} is not a JSON object")
    return cast(dict[str, object], decoded)


def canonical_hash(value: Mapping[str, object]) -> str:
    """Hash an object after omitting its embedded summary digest."""
    canonical = dict(value)
    canonical.pop("summary_sha256", None)
    encoded = json.dumps(
        canonical,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def file_sha256(path: Path) -> str:
    """Return the exact file SHA-256."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require_dict(value: object, label: str) -> dict[str, object]:
    """Narrow one decoded object."""
    if not isinstance(value, dict):
        raise AssertionError(f"{label} is not an object")
    return cast(dict[str, object], value)


def require_list(value: object, label: str) -> list[object]:
    """Narrow one decoded array."""
    if not isinstance(value, list):
        raise AssertionError(f"{label} is not an array")
    return cast(list[object], value)


def require_int(value: object, label: str) -> int:
    """Narrow one decoded non-boolean integer."""
    if not isinstance(value, int) or isinstance(value, bool):
        raise AssertionError(f"{label} is not an integer")
    return value


def balanced_prime_population(input_length: int) -> tuple[int, ...]:
    """Reconstruct primes p with 2**(m-1) <= p**2 < 2**m."""
    if input_length < 2:
        raise ValueError("input length must be at least two")
    lower_square = 1 << (input_length - 1)
    lower = isqrt(lower_square)
    if lower * lower < lower_square:
        lower += 1
    upper = isqrt((1 << input_length) - 1)
    flags = bytearray(b"\x01") * (upper + 1)
    flags[:2] = b"\x00\x00"
    for candidate in range(2, isqrt(upper) + 1):
        if not flags[candidate]:
            continue
        start = candidate * candidate
        count = (upper - start) // candidate + 1
        flags[start : upper + 1 : candidate] = b"\x00" * count
    return tuple(
        candidate for candidate in range(lower, upper + 1) if flags[candidate]
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
    """Yield every descriptor once from the congruence grammar."""
    for first in range(3, cap + 1, 4):
        for second in range(3, cap + 1, 4):
            if first == second:
                continue
            for base in range(2, cap + 1):
                yield Descriptor("phi4", first, second, base)
    for first in range(5, cap + 1, 6):
        for second in range(3, cap + 1, 6):
            for base in range(2, cap + 1):
                yield Descriptor("phi6", first, second, base)


def selector_descriptor_count(cap: int) -> int:
    """Count the grammar independently of an artifact profile."""
    phi4 = len(range(3, cap + 1, 4))
    phi6_first = len(range(5, cap + 1, 6))
    phi6_second = len(range(3, cap + 1, 6))
    bases = cap - 1
    return (
        phi4 * (phi4 - 1) * bases
        + phi6_first * phi6_second * bases
    )


def parse_source(source: str, cap: int) -> tuple[Descriptor, str]:
    """Parse and validate one canonical primitive-coordinate source."""
    parts = source.split(":")
    if len(parts) != 5:
        raise AssertionError(f"noncanonical coordinate source: {source}")
    family, first_text, second_text, base_text, kind = parts
    try:
        descriptor = Descriptor(
            family,
            int(first_text),
            int(second_text),
            int(base_text),
        )
    except ValueError as exc:
        raise AssertionError(f"noninteger coordinate source: {source}") from exc
    if not descriptor_is_valid(descriptor, cap):
        raise AssertionError(f"source is outside the cap-{cap} grammar: {source}")
    if kind not in EXIT_KINDS:
        raise AssertionError(f"unknown primitive exit kind: {kind}")
    if source != f"{descriptor.key}:{kind}":
        raise AssertionError(f"noncanonical coordinate source: {source}")
    return descriptor, kind


def geometric_sum(base: int, count: int, prime: int) -> int:
    """Return 1 + base + ... + base**(count-1) modulo a prime."""
    base %= prime
    if base == 1:
        return count % prime
    return (
        (pow(base, count, prime) - 1) * pow(base - 1, -1, prime)
    ) % prime


def geometric_derivative(base: int, count: int, prime: int) -> int:
    """Return the derivative of a geometric sum modulo a prime."""
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


def cyclotomic_residue(descriptor: Descriptor, prime: int) -> int:
    """Evaluate Phi4 or Phi6 at the public base."""
    base = descriptor.base % prime
    if descriptor.family == "phi4":
        return (base * base + 1) % prime
    return (base * base - base + 1) % prime


def cofactor_residue(descriptor: Descriptor, prime: int) -> int:
    """Evaluate the exceptional quotient, including simple-root cases."""
    first = descriptor.first_factor
    second = descriptor.second_factor
    base = descriptor.base % prime
    nested_base = pow(base, first, prime)
    coefficient = 1 if descriptor.family == "phi4" else 2
    aggregate = (
        coefficient * geometric_sum(base, first, prime)
        + geometric_sum(nested_base, second, prime)
    ) % prime
    cyclotomic = cyclotomic_residue(descriptor, prime)
    if cyclotomic:
        return aggregate * pow(cyclotomic, -1, prime) % prime
    if aggregate:
        raise AssertionError("exceptional numerator missed its factor")
    derivative = (
        coefficient * geometric_derivative(base, first, prime)
        + first
        * pow(base, first - 1, prime)
        * geometric_derivative(nested_base, second, prime)
    ) % prime
    cyclotomic_derivative = (
        2 * base
        if descriptor.family == "phi4"
        else 2 * base - 1
    ) % prime
    if not cyclotomic_derivative:
        raise AssertionError("cyclotomic root is not simple")
    return derivative * pow(cyclotomic_derivative, -1, prime) % prime


def primitive_exit_mask(descriptor: Descriptor, prime: int) -> int:
    """Evaluate all eight charged primitive coordinates."""
    base = descriptor.base % prime
    if base == 0:
        return 1
    first = descriptor.first_factor
    second = descriptor.second_factor
    first_power = pow(base, first, prime)
    coefficient = 1 if descriptor.family == "phi4" else 2
    hits = (
        False,
        geometric_sum(base, first, prime) == 0,
        geometric_sum(first_power, second, prime) == 0,
        second % prime == 0,
        coefficient * second % prime == 0,
        cyclotomic_residue(descriptor, prime) == 0,
        overlap_resultant(descriptor) % prime == 0,
        cofactor_residue(descriptor, prime) == 0,
    )
    return sum(1 << index for index, hit in enumerate(hits) if hit)


def primitive_exit_hit(descriptor: Descriptor, kind: str, prime: int) -> bool:
    """Evaluate only one requested primitive coordinate."""
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


def stream_certificate_signatures(
    primes: tuple[int, ...],
    sources: tuple[tuple[Descriptor, str], ...],
) -> tuple[tuple[int, ...], int]:
    """Stream selected columns into one packed signature per prime."""
    signatures = [0] * len(primes)
    for column_index, (descriptor, kind) in enumerate(sources):
        column_bit = 1 << column_index
        for prime_index, prime in enumerate(primes):
            if primitive_exit_hit(descriptor, kind, prime):
                signatures[prime_index] |= column_bit
    return tuple(signatures), len(primes) * len(sources)


def collision_buckets(
    primes: Sequence[int],
    signatures: Sequence[int],
) -> list[list[int]]:
    """Return equal-signature buckets in population order."""
    if len(primes) != len(signatures):
        raise AssertionError("prime/signature length mismatch")
    grouped: dict[int, list[int]] = {}
    for prime, signature in zip(primes, signatures, strict=True):
        grouped.setdefault(signature, []).append(prime)
    return [bucket for bucket in grouped.values() if len(bucket) > 1]


def canonical_buckets(
    buckets: Sequence[Sequence[int]],
) -> tuple[tuple[int, ...], ...]:
    """Canonicalize unordered collision classes for semantic comparison."""
    return tuple(sorted(tuple(sorted(bucket)) for bucket in buckets))


def raw_collision_buckets(
    primes: tuple[int, ...],
    cap: int,
) -> tuple[list[list[int]], int]:
    """Refine unresolved buckets with every raw descriptor mask."""
    unresolved: list[tuple[int, ...]] = [tuple(range(len(primes)))]
    evaluations = 0
    for descriptor in iter_selector_descriptors(cap):
        refined: list[tuple[int, ...]] = []
        for bucket in unresolved:
            groups: dict[int, list[int]] = {}
            for prime_index in bucket:
                mask = primitive_exit_mask(descriptor, primes[prime_index])
                evaluations += 1
                groups.setdefault(mask, []).append(prime_index)
            refined.extend(
                tuple(indices)
                for indices in groups.values()
                if len(indices) > 1
            )
        unresolved = refined
        if not unresolved:
            break
    return (
        [[primes[index] for index in bucket] for bucket in unresolved],
        evaluations,
    )


def raw_buckets_persist(
    buckets: Sequence[Sequence[int]],
    cap: int,
) -> int:
    """Prove registered buckets survive every raw selector descriptor."""
    evaluations = 0
    for descriptor in iter_selector_descriptors(cap):
        for bucket in buckets:
            masks = {
                primitive_exit_mask(descriptor, prime) for prime in bucket
            }
            evaluations += len(bucket)
            if len(masks) != 1:
                raise AssertionError(
                    f"cap-{cap} raw descriptor splits a registered bucket"
                )
    return evaluations


def certificate_for(
    data: Mapping[str, object],
    input_length: int,
) -> dict[str, object]:
    """Select one construction certificate across the schema generations."""
    direct = data.get("construction_certificate")
    if direct is not None:
        return require_dict(direct, "construction certificate")
    candidates = require_list(
        data.get("construction_certificates"),
        "construction certificates",
    )
    matches = [
        require_dict(candidate, "construction certificate")
        for candidate in candidates
        if require_dict(candidate, "construction certificate").get(
            "input_length"
        )
        == input_length
    ]
    if len(matches) != 1:
        raise AssertionError(
            f"length {input_length} construction certificate is ambiguous"
        )
    return matches[0]


def registered_patterns(
    certificate: Mapping[str, object],
) -> tuple[tuple[int, ...], ...]:
    """Read the cross-generation registered repair-pattern field."""
    raw = certificate.get("new_source_patterns_on_final_collision")
    if raw is None:
        raw = certificate.get("new_source_patterns")
    if raw is None and certificate.get("new_source_pattern") is not None:
        raw = [certificate["new_source_pattern"]]
    rows = require_list(raw, "registered repair patterns")
    return tuple(
        tuple(require_int(bit, "repair pattern bit") for bit in require_list(
            row,
            "repair pattern",
        ))
        for row in rows
    )


def pair_universe(
    buckets: Sequence[Sequence[int]],
) -> tuple[tuple[int, int], ...]:
    """Return all unordered pairs that a repair must separate."""
    pairs: list[tuple[int, int]] = []
    offset = 0
    for bucket in buckets:
        pairs.extend(
            (offset + left, offset + right)
            for left in range(len(bucket))
            for right in range(left + 1, len(bucket))
        )
        offset += len(bucket)
    return tuple(pairs)


def pattern_coverage(
    pattern: Sequence[int],
    pairs: Sequence[tuple[int, int]],
) -> int:
    """Encode which unresolved pairs one binary coordinate separates."""
    return sum(
        1 << index
        for index, (left, right) in enumerate(pairs)
        if bool(pattern[left]) != bool(pattern[right])
    )


def minimum_cover_size(coverages: set[int], target: int) -> int:
    """Return the exact minimum number of coordinate coverages."""
    if target == 0:
        return 0
    best: dict[int, int] = {0: 0}
    for coverage in sorted(coverages):
        updated = dict(best)
        for current, count in best.items():
            union = current | coverage
            previous = updated.get(union)
            if previous is None or count + 1 < previous:
                updated[union] = count + 1
        best = updated
    if target not in best:
        raise AssertionError("new raw coordinates do not repair the bucket")
    return best[target]


def all_new_coverages(
    base_cap: int,
    repair_cap: int,
    tracked_primes: tuple[int, ...],
    pairs: tuple[tuple[int, int], ...],
) -> tuple[set[int], int]:
    """Enumerate every distinct new raw-coordinate separation pattern."""
    coverages: set[int] = set()
    evaluations = 0
    for descriptor in iter_selector_descriptors(repair_cap):
        if descriptor.cap <= base_cap:
            continue
        masks = tuple(
            primitive_exit_mask(descriptor, prime) for prime in tracked_primes
        )
        evaluations += len(tracked_primes)
        for kind_index in range(len(EXIT_KINDS)):
            pattern = tuple(
                (mask >> kind_index) & 1 for mask in masks
            )
            coverage = pattern_coverage(pattern, pairs)
            if coverage:
                coverages.add(coverage)
    return coverages, evaluations


def exact_buckets(value: object, label: str) -> list[list[int]]:
    """Read one nested prime-bucket list."""
    return [
        [
            require_int(prime, f"{label} prime")
            for prime in require_list(bucket, f"{label} bucket")
        ]
        for bucket in require_list(value, label)
    ]


def row_source_records(
    data: Mapping[str, object],
    input_length: int,
) -> tuple[int, int, list[list[int]] | None, int | None, str]:
    """Project cap/population/predecessor/repair semantics from one source."""
    if input_length <= 15:
        profiles = require_list(data.get("selector_profiles"), "selector profiles")
        profile = next(
            require_dict(item, "selector profile")
            for item in profiles
            if require_dict(item, "selector profile").get("input_length")
            == input_length
        )
        return (
            input_length,
            require_int(profile.get("population_size"), "population size"),
            None,
            None,
            "NOT_APPLICABLE_DOMAIN_FLOOR",
        )
    if input_length <= 20:
        records = require_list(data.get("threshold_records"), "threshold records")
        record = next(
            require_dict(item, "threshold record")
            for item in records
            if require_dict(item, "threshold record").get("input_length")
            == input_length
        )
        return (
            require_int(record.get("minimal_selector_cap"), "selector cap"),
            require_int(record.get("population_size"), "population size"),
            exact_buckets(
                record.get("predecessor_collision_buckets"),
                "predecessor buckets",
            ),
            None,
            "NOT_SEPARATELY_CERTIFIED",
        )
    repair = require_dict(data.get("repair_profile"), "repair profile")
    predecessor_value = data.get("predecessor_profile")
    if predecessor_value is None:
        predecessor_value = data.get("failed_profile")
    predecessor = require_dict(predecessor_value, "predecessor profile")
    repair_count_value = repair.get("new_repair_coordinate_count")
    if repair_count_value is None:
        repair_count_value = certificate_for(
            data,
            input_length,
        ).get("minimum_new_coordinate_count")
    repair_count = (
        None
        if repair_count_value is None
        else require_int(repair_count_value, "repair coordinate count")
    )
    return (
        require_int(repair.get("selector_cap"), "selector cap"),
        require_int(repair.get("population_size"), "population size"),
        exact_buckets(
            predecessor.get("collision_buckets"),
            "predecessor buckets",
        ),
        repair_count,
        (
            "CERTIFIED_MINIMUM"
            if repair_count is not None
            else "NOT_SEPARATELY_CERTIFIED"
        ),
    )


def check_profile_descriptor_count(
    data: Mapping[str, object],
    input_length: int,
    cap: int,
    observed: int,
) -> None:
    """Compare the grammar count to the applicable source profile."""
    if input_length <= 15:
        profiles = require_list(data.get("selector_profiles"), "selector profiles")
        record = next(
            require_dict(item, "selector profile")
            for item in profiles
            if require_dict(item, "selector profile").get("input_length")
            == input_length
        )
        registered = record.get("descriptor_count")
    elif input_length <= 20:
        records = require_list(data.get("threshold_records"), "threshold records")
        record = next(
            require_dict(item, "threshold record")
            for item in records
            if require_dict(item, "threshold record").get("input_length")
            == input_length
        )
        registered = record.get("threshold_descriptor_count")
    else:
        record = require_dict(data.get("repair_profile"), "repair profile")
        registered = record.get("descriptor_count")
    if require_int(registered, "registered descriptor count") != observed:
        raise AssertionError(
            f"length {input_length} cap-{cap} descriptor count changed"
        )


def validate_summary_sources(summary: Mapping[str, object]) -> None:
    """Bind the consolidated artifact to the exact 16 frozen source files."""
    expected_paths = tuple(dict.fromkeys(SOURCE_BY_LENGTH))
    sources = require_list(summary.get("sources"), "M50 sources")
    if len(sources) != len(expected_paths):
        raise AssertionError("M50 source count changed")
    for expected_path, source_value in zip(
        expected_paths,
        sources,
        strict=True,
    ):
        source = require_dict(source_value, "M50 source")
        if source.get("path") != expected_path:
            raise AssertionError("M50 source order or path changed")
        if source.get("file_sha256") != file_sha256(ROOT / expected_path):
            raise AssertionError(f"{expected_path} file digest changed")


def validate_repair(
    input_length: int,
    data: Mapping[str, object],
    cap: int,
    repair_count: int,
    primes: tuple[int, ...],
    parsed_sources: tuple[tuple[Descriptor, str], ...],
    signatures: tuple[int, ...],
    predecessor_buckets: list[list[int]],
) -> int:
    """Reconstruct one certified minimum incremental repair."""
    certificate = certificate_for(data, input_length)
    if input_length in (27, 28):
        base_profile = require_dict(data.get("cap_profile"), "base cap profile")
        base_cap = require_int(base_profile.get("selector_cap"), "base cap")
        base_buckets = exact_buckets(
            base_profile.get("collision_buckets"),
            "base collision buckets",
        )
    else:
        base_cap = cap - 1
        base_buckets = predecessor_buckets

    if repair_count <= 0 or repair_count >= len(parsed_sources):
        raise AssertionError("invalid repair-coordinate count")
    base_column_count = len(parsed_sources) - repair_count
    if any(
        descriptor.cap > base_cap
        for descriptor, _kind in parsed_sources[:base_column_count]
    ):
        raise AssertionError("base certificate contains a later descriptor")
    if any(
        descriptor.cap <= base_cap
        for descriptor, _kind in parsed_sources[base_column_count:]
    ):
        raise AssertionError("repair certificate contains a base descriptor")

    base_mask = (1 << base_column_count) - 1
    base_signatures = tuple(signature & base_mask for signature in signatures)
    if canonical_buckets(collision_buckets(primes, base_signatures)) != (
        canonical_buckets(base_buckets)
    ):
        raise AssertionError(
            f"length {input_length} base certificate buckets changed"
        )
    raw_evaluations = (
        raw_buckets_persist(base_buckets, base_cap)
        if base_cap != cap - 1
        else 0
    )

    tracked_primes = tuple(prime for bucket in base_buckets for prime in bucket)
    pairs = pair_universe(base_buckets)
    target = (1 << len(pairs)) - 1
    available, pattern_evaluations = all_new_coverages(
        base_cap,
        cap,
        tracked_primes,
        pairs,
    )
    raw_evaluations += pattern_evaluations
    observed_minimum = minimum_cover_size(available, target)
    if observed_minimum != repair_count:
        raise AssertionError(
            f"length {input_length} repair minimum changed"
        )

    frozen_patterns = registered_patterns(certificate)
    if any(len(pattern) != len(tracked_primes) for pattern in frozen_patterns):
        raise AssertionError("registered repair-pattern width changed")
    frozen_coverages = {
        pattern_coverage(pattern, pairs) for pattern in frozen_patterns
    }
    if 0 in frozen_coverages or frozen_coverages != available:
        raise AssertionError("registered exhaustive repair patterns changed")

    selected_coverages = {
        pattern_coverage(
            tuple(
                int(primitive_exit_hit(descriptor, kind, prime))
                for prime in tracked_primes
            ),
            pairs,
        )
        for descriptor, kind in parsed_sources[base_column_count:]
    }
    if selected_coverages != frozen_coverages:
        raise AssertionError("selected repair sources changed")
    return raw_evaluations


def validate_one_row(
    row: Mapping[str, object],
    data: Mapping[str, object],
) -> RowReport:
    """Reconstruct one M50 row from source semantics."""
    input_length = require_int(row.get("input_length"), "M50 input length")
    if not 9 <= input_length <= 34:
        raise AssertionError("M50 input length is outside the finite window")
    expected_source = SOURCE_BY_LENGTH[input_length - 9]
    if row.get("source_schema") != expected_source:
        raise AssertionError(f"length {input_length} source schema changed")

    (
        cap,
        source_population_size,
        predecessor_buckets,
        repair_count,
        repair_status,
    ) = row_source_records(data, input_length)
    if row.get("family_relative_minimal_cap") != cap:
        raise AssertionError(f"length {input_length} M50 cap drifted")
    if row.get("population_size") != source_population_size:
        raise AssertionError(f"length {input_length} M50 population drifted")
    if row.get("predecessor_collision_buckets") != predecessor_buckets:
        raise AssertionError(
            f"length {input_length} M50 predecessor buckets drifted"
        )
    if (
        row.get("repair_coordinate_count") != repair_count
        or row.get("repair_coordinate_status") != repair_status
    ):
        raise AssertionError(f"length {input_length} M50 repair drifted")

    descriptor_count = selector_descriptor_count(cap)
    check_profile_descriptor_count(
        data,
        input_length,
        cap,
        descriptor_count,
    )
    certificate = certificate_for(data, input_length)
    if certificate.get("input_length") != input_length:
        raise AssertionError("construction certificate input length changed")
    if certificate.get("selector_cap") not in (None, cap):
        raise AssertionError("construction certificate cap changed")

    primes = balanced_prime_population(input_length)
    registered_primes = tuple(
        require_int(prime, "certificate prime")
        for prime in require_list(certificate.get("primes"), "certificate primes")
    )
    if registered_primes != primes or len(primes) != source_population_size:
        raise AssertionError(
            f"length {input_length} balanced population changed"
        )
    source_names = tuple(
        str(source)
        for source in require_list(
            certificate.get("column_sources"),
            "certificate sources",
        )
    )
    if len(set(source_names)) != len(source_names):
        raise AssertionError("construction certificate sources are not unique")
    parsed_sources = tuple(parse_source(source, cap) for source in source_names)
    signatures, certificate_evaluations = stream_certificate_signatures(
        primes,
        parsed_sources,
    )
    registered_signatures = tuple(
        require_int(signature, "certificate signature")
        for signature in require_list(
            certificate.get("restricted_signatures"),
            "certificate signatures",
        )
    )
    if signatures != registered_signatures:
        raise AssertionError(
            f"length {input_length} packed signatures changed"
        )
    if len(set(signatures)) != len(primes):
        raise AssertionError(
            f"length {input_length} construction is not injective"
        )

    raw_evaluations = 0
    if 16 <= input_length <= 25:
        if predecessor_buckets is None:
            raise AssertionError("missing predecessor buckets")
        observed_buckets, raw_evaluations = raw_collision_buckets(
            primes,
            cap - 1,
        )
        if canonical_buckets(observed_buckets) != canonical_buckets(
            predecessor_buckets
        ):
            raise AssertionError(
                f"length {input_length} raw predecessor changed"
            )
    elif input_length >= 26:
        if predecessor_buckets is None or repair_count is None:
            raise AssertionError("missing certified repair data")
        predecessor_indices = tuple(
            index
            for index, (descriptor, _kind) in enumerate(parsed_sources)
            if descriptor.cap <= cap - 1
        )
        predecessor_mask = sum(1 << index for index in predecessor_indices)
        predecessor_signatures = tuple(
            signature & predecessor_mask for signature in signatures
        )
        if canonical_buckets(
            collision_buckets(primes, predecessor_signatures)
        ) != canonical_buckets(predecessor_buckets):
            raise AssertionError(
                f"length {input_length} predecessor subcertificate changed"
            )
        raw_evaluations += raw_buckets_persist(
            predecessor_buckets,
            cap - 1,
        )
        raw_evaluations += validate_repair(
            input_length,
            data,
            cap,
            repair_count,
            primes,
            parsed_sources,
            signatures,
            predecessor_buckets,
        )

    return RowReport(
        input_length,
        len(primes),
        cap,
        descriptor_count,
        len(parsed_sources),
        certificate_evaluations,
        raw_evaluations,
        repair_count,
    )


def validate_all(
    summary: Mapping[str, object] | None = None,
) -> SemanticReport:
    """Validate all 26 rows and all 16 source bindings."""
    loaded_summary = read_json(SUMMARY_PATH) if summary is None else dict(summary)
    if loaded_summary.get("schema_version") != "1.0.0":
        raise AssertionError("unsupported M50 schema version")
    if loaded_summary.get("summary_sha256") != canonical_hash(loaded_summary):
        raise AssertionError("M50 canonical summary hash changed")
    validate_summary_sources(loaded_summary)
    rows = require_list(loaded_summary.get("rows"), "M50 rows")
    if len(rows) != 26:
        raise AssertionError("M50 row count changed")

    reports: list[RowReport] = []
    for expected_input_length, row_value in enumerate(rows, start=9):
        row = require_dict(row_value, "M50 row")
        if row.get("input_length") != expected_input_length:
            raise AssertionError("M50 row order changed")
        source_path = SOURCE_BY_LENGTH[expected_input_length - 9]
        reports.append(validate_one_row(row, read_json(ROOT / source_path)))
    report_rows = tuple(reports)
    return SemanticReport(
        report_rows,
        len(tuple(dict.fromkeys(SOURCE_BY_LENGTH))),
        sum(row.population_size for row in report_rows),
        sum(row.certificate_coordinates for row in report_rows),
        sum(row.certificate_evaluations for row in report_rows),
        sum(row.raw_mask_evaluations for row in report_rows),
    )


def main() -> int:
    """Run the complete bounded semantic gate and report resources."""
    started = time.perf_counter()
    report = validate_all()
    elapsed = time.perf_counter() - started
    print(
        "M91 all-row semantic checker: PASS "
        f"({len(report.rows)} rows, {report.source_count} sources, "
        f"{report.population_total} population entries, "
        f"{report.certificate_coordinates} certificate coordinates, "
        f"{report.certificate_evaluations} certificate evaluations, "
        f"{report.raw_mask_evaluations} raw mask evaluations, "
        f"{elapsed:.2f}s)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
