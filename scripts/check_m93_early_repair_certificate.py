"""Independently reconstruct and check all ten M93 early repairs."""

from __future__ import annotations

import hashlib
import itertools
import json
import math
from collections.abc import Iterable, Iterator, Mapping
from pathlib import Path
from typing import Any, NamedTuple

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas" / "m93-early-repair-certificates-v1.json"
SUMMARY = ROOT / "schemas" / "m50-finite-threshold-summary-v1.json"
SUMMARY_FILE_SHA256 = (
    "2f9974d45a350f65694bd048bf67dae4b27a90493b07ecd895c251d102aab75b"
)
SUMMARY_CANONICAL_SHA256 = (
    "1fb6185f73b4bc2243dc2f339c1e823d7c849acd7bf33ef5f288af4baa9d00b3"
)
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
EXPECTED_SOURCES = {
    16: "schemas/m32-widened-selector-cap-v1.json",
    17: "schemas/m32-widened-selector-cap-v1.json",
    18: "schemas/m32-widened-selector-cap-v1.json",
    19: "schemas/m32-widened-selector-cap-v1.json",
    20: "schemas/m32-widened-selector-cap-v1.json",
    21: "schemas/m33-linear-cap-recurrence-v1.json",
    22: "schemas/m34-next-envelope-v1.json",
    23: "schemas/m35-next-envelope-v1.json",
    24: "schemas/m36-distinct-cap-v1.json",
    25: "schemas/m37-length-25-cap-v1.json",
}


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
        """Return the first selector cap admitting this descriptor."""
        return max(self.first_factor, self.second_factor, self.base)


def canonical_hash(record: Mapping[str, Any]) -> str:
    """Hash a JSON object after excluding its registered digest."""
    payload = dict(record)
    payload.pop("summary_sha256", None)
    encoded = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def file_sha256(path: Path) -> str:
    """Return one exact binary file digest."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def iter_selector_descriptors(cap: int) -> Iterator[Descriptor]:
    """Yield the complete public descriptor grammar exactly once."""
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


def geometric_sum(base: int, count: int, prime: int) -> int:
    """Return 1 + base + ... + base**(count-1) modulo a prime."""
    base %= prime
    if base == 1:
        return count % prime
    return (
        (pow(base, count, prime) - 1) * pow(base - 1, -1, prime)
    ) % prime


def geometric_derivative(base: int, count: int, prime: int) -> int:
    """Return the derivative of one geometric sum modulo a prime."""
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
            raise AssertionError("phi4 resultant coefficients are nonintegral")
        constant = constant_numerator // 4
        linear = linear_numerator // 4
        return constant * constant + linear * linear
    residual = first * (second - 2) + 1
    linear_numerator = first * (second + 4) + 4
    if (2 * residual) % 3 or linear_numerator % 3:
        raise AssertionError("phi6 resultant coefficients are nonintegral")
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


def normalized_pattern(pattern: tuple[int, ...]) -> tuple[int, ...]:
    """Canonicalize one binary pattern modulo complementation."""
    if not pattern or any(bit not in (0, 1) for bit in pattern):
        raise AssertionError("repair pattern is not a nonempty bit vector")
    complement = tuple(1 - bit for bit in pattern)
    return min(pattern, complement)


def labeled_pairs(
    buckets: tuple[tuple[int, ...], ...],
) -> tuple[tuple[int, int], ...]:
    """Enumerate labeled within-bucket pairs."""
    return tuple(
        (bucket[left], bucket[right])
        for bucket in buckets
        for left in range(len(bucket))
        for right in range(left + 1, len(bucket))
    )


def indexed_pairs(
    buckets: tuple[tuple[int, ...], ...],
) -> tuple[tuple[int, int], ...]:
    """Enumerate flattened within-bucket index pairs."""
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
    pattern: tuple[int, ...],
    pairs: tuple[tuple[int, int], ...],
) -> int:
    """Return the pair-separation mask of one pattern."""
    return sum(
        1 << index
        for index, (left, right) in enumerate(pairs)
        if pattern[left] != pattern[right]
    )


def or_masks(masks: Iterable[int]) -> int:
    """OR an iterable without a project helper."""
    result = 0
    for mask in masks:
        result |= int(mask)
    return result


def enumerate_types(
    base_cap: int,
    repair_cap: int,
    primes: tuple[int, ...],
    pairs: tuple[tuple[int, int], ...],
) -> tuple[dict[int, tuple[tuple[int, ...], str]], int]:
    """Reconstruct all distinct nonzero new raw coverage types."""
    types: dict[int, tuple[tuple[int, ...], str]] = {}
    descriptor_count = 0
    for descriptor in iter_selector_descriptors(repair_cap):
        if descriptor.cap <= base_cap:
            continue
        descriptor_count += 1
        masks = tuple(
            primitive_exit_mask(descriptor, prime) for prime in primes
        )
        for kind_index, kind in enumerate(EXIT_KINDS):
            pattern = normalized_pattern(
                tuple((mask >> kind_index) & 1 for mask in masks)
            )
            coverage = pattern_coverage(pattern, pairs)
            if coverage:
                types.setdefault(
                    coverage,
                    (pattern, f"{descriptor.key}:{kind}"),
                )
    return types, descriptor_count


def exact_cover(masks: tuple[int, ...], target: int) -> tuple[int, ...]:
    """Return the lexicographically first minimum cover."""
    for size in range(len(masks) + 1):
        for subset in itertools.combinations(range(len(masks)), size):
            if or_masks(masks[index] for index in subset) == target:
                return subset
    raise AssertionError("new raw types do not cover the pair universe")


def index_width(value_count: int) -> int:
    """Return the exact fixed-width index cost."""
    return 0 if value_count <= 1 else math.ceil(math.log2(value_count))


def expected_lower(
    input_length: int,
    selected_ids: tuple[str, ...],
    masks_by_id: dict[str, int],
    buckets: tuple[tuple[int, ...], ...],
    pairs: tuple[tuple[int, int], ...],
) -> dict[str, Any]:
    """Reconstruct the canonical lower certificate."""
    private: list[dict[str, object]] = []
    for type_id in selected_ids:
        pair_index = next(
            (
                index
                for index in range(len(pairs))
                if (masks_by_id[type_id] >> index) & 1
                and sum(
                    (mask >> index) & 1
                    for mask in masks_by_id.values()
                )
                == 1
            ),
            None,
        )
        if pair_index is None:
            private = []
            break
        private.append(
            {
                "type_id": type_id,
                "pair_index": pair_index,
                "pair": list(pairs[pair_index]),
            }
        )
    if private:
        return {
            "kind": "private_pairs",
            "lower_bound": len(selected_ids),
            "entries": private,
        }
    if input_length == 16:
        maximum = max(len(bucket) for bucket in buckets)
        return {
            "kind": "cardinality",
            "lower_bound": math.ceil(math.log2(maximum)),
            "maximum_bucket_size": maximum,
        }
    if input_length != 24:
        raise AssertionError("unexpected private-pair failure")
    subset_size = len(selected_ids) - 1
    entries: list[dict[str, object]] = []
    for subset in itertools.combinations(tuple(masks_by_id), subset_size):
        union = or_masks(masks_by_id[type_id] for type_id in subset)
        pair_index = next(
            index
            for index in range(len(pairs))
            if not (union >> index) & 1
        )
        entries.append(
            {
                "type_ids": list(subset),
                "uncovered_pair_index": pair_index,
                "uncovered_pair": list(pairs[pair_index]),
            }
        )
    return {
        "kind": "subset_obstructions",
        "lower_bound": len(selected_ids),
        "subset_size": subset_size,
        "entries": entries,
    }


def lower_cost(
    lower: Mapping[str, Any],
    type_count: int,
    pair_count: int,
) -> tuple[int, int]:
    """Return lower-bound verifier tests and payload bits."""
    if lower["kind"] == "private_pairs":
        count = len(lower["entries"])
        return (
            count * type_count,
            count * (index_width(type_count) + index_width(pair_count)),
        )
    if lower["kind"] == "cardinality":
        maximum = int(lower["maximum_bucket_size"])
        bound = int(lower["lower_bound"])
        return 1, maximum.bit_length() + bound.bit_length()
    if lower["kind"] == "subset_obstructions":
        count = len(lower["entries"])
        subset_size = int(lower["subset_size"])
        return (
            count * subset_size,
            count
            * (
                subset_size * index_width(type_count)
                + index_width(pair_count)
            ),
        )
    raise AssertionError("unknown lower witness kind")


def expected_cost(
    buckets: tuple[tuple[int, ...], ...],
    type_count: int,
    minimum: int,
    descriptor_count: int,
    lower: Mapping[str, Any],
) -> dict[str, int]:
    """Reconstruct the operation and abstract payload ledger."""
    primes = tuple(prime for bucket in buckets for prime in bucket)
    pair_count = len(labeled_pairs(buckets))
    lower_tests, lower_bits = lower_cost(lower, type_count, pair_count)
    pattern_bits = type_count * len(primes)
    mask_bits = type_count * pair_count
    selected_bits = minimum * index_width(type_count)
    label_bits = sum(prime.bit_length() for prime in primes)
    return {
        "new_descriptor_count": descriptor_count,
        "descriptor_prime_evaluations": descriptor_count * len(primes),
        "raw_coordinate_tests": descriptor_count
        * len(primes)
        * len(EXIT_KINDS),
        "pattern_pair_tests": type_count * pair_count,
        "upper_mask_bit_tests": minimum * pair_count,
        "lower_witness_bit_tests": lower_tests,
        "certificate_verifier_bit_tests": (
            type_count * pair_count + minimum * pair_count + lower_tests
        ),
        "defense_subset_count": 1 << type_count,
        "defense_mask_bit_tests": (
            pair_count * type_count * (1 << (type_count - 1))
        ),
        "pattern_storage_bits": pattern_bits,
        "mask_storage_bits": mask_bits,
        "selected_type_index_bits": selected_bits,
        "lower_witness_payload_bits": lower_bits,
        "bucket_label_bits": label_bits,
        "abstract_certificate_payload_bits": (
            pattern_bits + mask_bits + selected_bits + lower_bits + label_bits
        ),
    }


def validate_instance(
    instance: Mapping[str, Any],
    row: Mapping[str, Any],
    source_record: Mapping[str, Any],
) -> dict[str, int]:
    """Independently validate one exact early repair certificate."""
    input_length = int(instance["input_length"])
    expected_path = EXPECTED_SOURCES.get(input_length)
    if expected_path is None or instance["source_path"] != expected_path:
        raise AssertionError("unexpected M93 source path")
    if row["source_schema"] != expected_path:
        raise AssertionError("M50 row source path changed")
    source_path = ROOT / expected_path
    source_digest = file_sha256(source_path)
    if source_record["file_sha256"] != source_digest:
        raise AssertionError("M50 source record digest changed")
    if instance["source_sha256"] != source_digest:
        raise AssertionError("M93 source digest changed")
    if int(instance["source_file_bytes"]) != source_path.stat().st_size:
        raise AssertionError("M93 source size changed")
    repair_cap = int(row["family_relative_minimal_cap"])
    base_cap = repair_cap - 1
    if int(instance["base_cap"]) != base_cap:
        raise AssertionError("M93 base cap changed")
    if int(instance["repair_cap"]) != repair_cap:
        raise AssertionError("M93 repair cap changed")
    buckets = tuple(
        tuple(int(prime) for prime in bucket)
        for bucket in row["predecessor_collision_buckets"]
    )
    registered_buckets = tuple(
        tuple(int(prime) for prime in bucket)
        for bucket in instance["collision_buckets"]
    )
    if registered_buckets != buckets:
        raise AssertionError("M93 collision buckets changed")
    primes = tuple(prime for bucket in buckets for prime in bucket)
    if len(set(primes)) != len(primes):
        raise AssertionError("M93 collision buckets overlap")
    pairs = labeled_pairs(buckets)
    if int(instance["tracked_prime_count"]) != len(primes):
        raise AssertionError("M93 tracked-prime count changed")
    if int(instance["pair_count"]) != len(pairs):
        raise AssertionError("M93 pair count changed")

    raw_types, descriptor_count = enumerate_types(
        base_cap,
        repair_cap,
        primes,
        indexed_pairs(buckets),
    )
    ordered_types = tuple(sorted(raw_types.items()))
    width = max(1, math.ceil(len(pairs) / 4))
    expected_records = [
        {
            "type_id": f"T{index}",
            "pattern": list(pattern),
            "coverage_mask_hex": f"{mask:0{width}x}",
            "representative_source": source,
        }
        for index, (mask, (pattern, source)) in enumerate(ordered_types)
    ]
    if instance["coverage_types"] != expected_records:
        raise AssertionError("M93 raw coverage types changed")
    masks = tuple(mask for mask, _record in ordered_types)
    target = (1 << len(pairs)) - 1
    selected_indices = exact_cover(masks, target)
    selected_ids = tuple(f"T{index}" for index in selected_indices)
    if tuple(instance["upper_witness"]) != selected_ids:
        raise AssertionError("M93 upper witness changed")
    minimum = len(selected_ids)
    if int(instance["minimum_coordinate_count"]) != minimum:
        raise AssertionError("M93 exact minimum changed")
    masks_by_id = {
        f"T{index}": mask for index, mask in enumerate(masks)
    }
    lower = expected_lower(
        input_length,
        selected_ids,
        masks_by_id,
        buckets,
        pairs,
    )
    if instance["lower_witness"] != lower:
        raise AssertionError("M93 lower witness changed")
    if int(lower["lower_bound"]) != minimum:
        raise AssertionError("M93 lower witness is not exact")
    cost = expected_cost(
        buckets,
        len(masks),
        minimum,
        descriptor_count,
        lower,
    )
    if instance["verification_cost"] != cost:
        raise AssertionError("M93 cost ledger changed")
    return {
        "tracked_prime_count": len(primes),
        "pair_count": len(pairs),
        "coverage_type_count": len(masks),
        "minimum_coordinate_count": minimum,
        **{
            field: cost[field]
            for field in (
                "new_descriptor_count",
                "descriptor_prime_evaluations",
                "raw_coordinate_tests",
                "pattern_pair_tests",
                "upper_mask_bit_tests",
                "lower_witness_bit_tests",
                "certificate_verifier_bit_tests",
                "defense_subset_count",
                "defense_mask_bit_tests",
                "abstract_certificate_payload_bits",
            )
        },
        "source_file_bytes": source_path.stat().st_size,
    }


def validate_all(
    schema: Mapping[str, Any] | None = None,
    summary: Mapping[str, Any] | None = None,
) -> dict[str, int]:
    """Validate the complete ten-instance M93 portfolio."""
    data = (
        json.loads(SCHEMA.read_text(encoding="utf-8"))
        if schema is None
        else dict(schema)
    )
    m50 = (
        json.loads(SUMMARY.read_text(encoding="utf-8"))
        if summary is None
        else dict(summary)
    )
    if file_sha256(SUMMARY) != SUMMARY_FILE_SHA256 and summary is None:
        raise AssertionError("M50 frozen summary file digest changed")
    if m50.get("summary_sha256") != SUMMARY_CANONICAL_SHA256:
        raise AssertionError("M50 canonical summary digest changed")
    if canonical_hash(m50) != SUMMARY_CANONICAL_SHA256:
        raise AssertionError("M50 summary content changed")
    expected_anchor = {
        "path": "schemas/m50-finite-threshold-summary-v1.json",
        "file_sha256": SUMMARY_FILE_SHA256,
        "summary_sha256": SUMMARY_CANONICAL_SHA256,
    }
    if data.get("finite_summary") != expected_anchor:
        raise AssertionError("M93 finite summary anchor changed")
    if data.get("schema_version") != "1.0.0":
        raise AssertionError("unsupported M93 schema version")
    if data.get("experiment_id") != "EXP-0064":
        raise AssertionError("M93 experiment ID changed")
    if data.get("claim_ids") != [
        "DEF-049",
        "THM-022",
        "REF-062",
        "EMP-064",
    ]:
        raise AssertionError("M93 claim registry changed")
    if data.get("summary_sha256") != canonical_hash(data):
        raise AssertionError("M93 canonical summary hash changed")
    instances = data.get("instances")
    if not isinstance(instances, list) or len(instances) != 10:
        raise AssertionError("M93 instance count changed")
    if [int(instance["input_length"]) for instance in instances] != list(
        range(16, 26)
    ):
        raise AssertionError("M93 instance order changed")
    rows = {
        int(row["input_length"]): row
        for row in m50["rows"]
        if 16 <= int(row["input_length"]) <= 25
    }
    source_records = {
        str(record["path"]): record for record in m50["sources"]
    }
    reports = [
        validate_instance(
            instance,
            rows[int(instance["input_length"])],
            source_records[
                EXPECTED_SOURCES[int(instance["input_length"])]
            ],
        )
        for instance in instances
    ]
    fields = (
        "tracked_prime_count",
        "pair_count",
        "coverage_type_count",
        "minimum_coordinate_count",
        "new_descriptor_count",
        "descriptor_prime_evaluations",
        "raw_coordinate_tests",
        "pattern_pair_tests",
        "upper_mask_bit_tests",
        "lower_witness_bit_tests",
        "certificate_verifier_bit_tests",
        "defense_subset_count",
        "defense_mask_bit_tests",
        "source_file_bytes",
        "abstract_certificate_payload_bits",
    )
    totals = {
        "instance_count": len(reports),
        **{
            field: sum(report[field] for report in reports)
            for field in fields
        },
    }
    if data.get("totals") != totals:
        raise AssertionError("M93 totals changed")
    return totals


def main() -> int:
    """Run the standalone independent certificate checker."""
    totals = validate_all()
    print(
        "M93 early repair certificate checker: PASS "
        f"({totals['instance_count']} instances, "
        f"{totals['pair_count']} pairs, "
        f"{totals['coverage_type_count']} coverage types, "
        f"{totals['minimum_coordinate_count']} selected types, "
        f"{totals['raw_coordinate_tests']} raw coordinate tests, "
        f"{totals['abstract_certificate_payload_bits']} payload bits)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
