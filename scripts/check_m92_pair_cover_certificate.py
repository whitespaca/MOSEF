"""Independently check the compact M92 pair-cover certificates."""

from __future__ import annotations

import hashlib
import itertools
import json
import math
from collections.abc import Mapping
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas" / "m92-pair-cover-certificates-v1.json"
EXPECTED_SOURCES = {
    26: "schemas/m38-length-26-cap-v1.json",
    27: "schemas/m39-length-27-cap-v1.json",
    28: "schemas/m40-length-28-cap-v1.json",
    29: "schemas/m41-length-29-cap-v1.json",
    30: "schemas/m42-length-30-cap-v1.json",
    31: "schemas/m43-length-31-cap-v1.json",
    32: "schemas/m44-length-32-cap-v1.json",
    33: "schemas/m45-length-33-cap-v1.json",
    34: "schemas/m46-length-34-cap-v1.json",
}


def canonical_hash(record: Mapping[str, Any]) -> str:
    """Hash a JSON object while excluding its registered hash."""
    payload = dict(record)
    payload.pop("summary_sha256", None)
    encoded = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def file_sha256(path: Path) -> str:
    """Return one binary file digest."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalized_pattern(pattern: tuple[int, ...]) -> tuple[int, ...]:
    """Canonicalize a nonempty binary pattern modulo complementation."""
    if not pattern or any(bit not in (0, 1) for bit in pattern):
        raise AssertionError("nonbinary repair pattern")
    complement = tuple(1 - bit for bit in pattern)
    return min(pattern, complement)


def pair_universe(
    buckets: tuple[tuple[int, ...], ...],
) -> tuple[tuple[int, int], ...]:
    """Enumerate the canonical within-bucket unordered pairs."""
    return tuple(
        (bucket[left], bucket[right])
        for bucket in buckets
        for left in range(len(bucket))
        for right in range(left + 1, len(bucket))
    )


def coverage_mask(
    pattern: tuple[int, ...],
    buckets: tuple[tuple[int, ...], ...],
) -> int:
    """Return the pair-separation mask of one binary pattern."""
    result = 0
    pair_index = 0
    offset = 0
    for bucket in buckets:
        for left in range(len(bucket)):
            for right in range(left + 1, len(bucket)):
                if pattern[offset + left] != pattern[offset + right]:
                    result |= 1 << pair_index
                pair_index += 1
        offset += len(bucket)
    return result


def registered_patterns(
    certificate: Mapping[str, Any],
) -> tuple[tuple[int, ...], ...]:
    """Read the bounded cross-generation repair-pattern adapters."""
    raw = certificate.get("new_source_patterns_on_final_collision")
    if raw is None:
        raw = certificate.get("new_source_patterns")
    if raw is None and certificate.get("new_source_pattern") is not None:
        raw = [certificate["new_source_pattern"]]
    if not isinstance(raw, list):
        raise AssertionError("source repair patterns are missing")
    return tuple(tuple(int(bit) for bit in pattern) for pattern in raw)


def source_projection(
    input_length: int,
    data: Mapping[str, Any],
) -> tuple[
    int,
    int,
    tuple[tuple[int, ...], ...],
    int,
    tuple[tuple[int, ...], ...],
    tuple[str, ...],
]:
    """Project only the source fields needed by the combinatorial checker."""
    certificate = data["construction_certificate"]
    profile = (
        data["cap_profile"]
        if input_length in (27, 28)
        else data["predecessor_profile"]
    )
    buckets = tuple(
        tuple(int(prime) for prime in bucket)
        for bucket in profile["collision_buckets"]
    )
    minimum = data["repair_profile"].get("new_repair_coordinate_count")
    if minimum is None:
        minimum = certificate["minimum_new_coordinate_count"]
    count = int(minimum)
    sources = tuple(str(source) for source in certificate["column_sources"])
    return (
        int(profile["selector_cap"]),
        int(data["repair_profile"]["selector_cap"]),
        buckets,
        count,
        registered_patterns(certificate),
        sources[-count:],
    )


def index_width(value_count: int) -> int:
    """Return the exact fixed-width index cost."""
    return 0 if value_count <= 1 else math.ceil(math.log2(value_count))


def exact_minimum(masks: tuple[int, ...], target: int) -> int:
    """Brute-force the small abstract set-cover optimum."""
    for size in range(len(masks) + 1):
        for subset in itertools.combinations(masks, size):
            union = 0
            for mask in subset:
                union |= mask
            if union == target:
                return size
    raise AssertionError("coverage types do not cover the pair universe")


def expected_cost(
    buckets: tuple[tuple[int, ...], ...],
    type_count: int,
    repair_count: int,
) -> dict[str, int]:
    """Reconstruct the declared bit-operation and payload ledger."""
    tracked_primes = tuple(prime for bucket in buckets for prime in bucket)
    pair_count = len(pair_universe(buckets))
    selected_bits = repair_count * index_width(type_count)
    private_bits = repair_count * index_width(pair_count)
    label_bits = sum(prime.bit_length() for prime in tracked_primes)
    return {
        "pattern_pair_tests": type_count * pair_count,
        "upper_mask_bit_tests": repair_count * pair_count,
        "private_type_tests": repair_count * type_count,
        "certificate_verifier_bit_tests": (
            type_count * pair_count
            + repair_count * pair_count
            + repair_count * type_count
        ),
        "defense_subset_count": 1 << type_count,
        "defense_mask_bit_tests": (
            pair_count * type_count * (1 << (type_count - 1))
        ),
        "pattern_storage_bits": type_count * len(tracked_primes),
        "mask_storage_bits": type_count * pair_count,
        "selected_type_index_bits": selected_bits,
        "private_pair_index_bits": private_bits,
        "bucket_label_bits": label_bits,
        "abstract_certificate_payload_bits": (
            type_count * (pair_count + len(tracked_primes))
            + selected_bits
            + private_bits
            + label_bits
        ),
    }


def validate_instance(
    instance: Mapping[str, Any],
    source_override: Mapping[str, Any] | None = None,
) -> dict[str, int]:
    """Validate one source-bound upper/private-pair certificate."""
    input_length = int(instance["input_length"])
    expected_path = EXPECTED_SOURCES.get(input_length)
    if expected_path is None or instance["source_path"] != expected_path:
        raise AssertionError("unexpected M92 source path")
    path = ROOT / expected_path
    if instance["source_sha256"] != file_sha256(path):
        raise AssertionError("M92 source digest changed")
    if int(instance["source_file_bytes"]) != path.stat().st_size:
        raise AssertionError("M92 source size changed")
    source = (
        dict(source_override)
        if source_override is not None
        else json.loads(path.read_text(encoding="utf-8"))
    )
    (
        base_cap,
        repair_cap,
        buckets,
        repair_count,
        source_patterns,
        repair_sources,
    ) = source_projection(input_length, source)
    if int(instance["base_cap"]) != base_cap:
        raise AssertionError("base cap changed")
    if int(instance["repair_cap"]) != repair_cap:
        raise AssertionError("repair cap changed")
    registered_buckets = tuple(
        tuple(int(prime) for prime in bucket)
        for bucket in instance["collision_buckets"]
    )
    if registered_buckets != buckets:
        raise AssertionError("collision buckets changed")
    tracked_primes = tuple(prime for bucket in buckets for prime in bucket)
    if len(set(tracked_primes)) != len(tracked_primes):
        raise AssertionError("collision buckets overlap")
    pairs = pair_universe(buckets)
    if int(instance["tracked_prime_count"]) != len(tracked_primes):
        raise AssertionError("tracked-prime count changed")
    if int(instance["pair_count"]) != len(pairs):
        raise AssertionError("pair count changed")
    if tuple(instance["repair_sources"]) != repair_sources:
        raise AssertionError("repair sources changed")

    source_types: dict[int, tuple[int, ...]] = {}
    for raw_pattern in source_patterns:
        pattern = normalized_pattern(raw_pattern)
        if len(pattern) != len(tracked_primes):
            raise AssertionError("source pattern width changed")
        mask = coverage_mask(pattern, buckets)
        source_types.setdefault(mask, pattern)
    registered_types: dict[str, int] = {}
    width = max(1, math.ceil(len(pairs) / 4))
    for index, coverage_type in enumerate(instance["coverage_types"]):
        type_id = str(coverage_type["type_id"])
        if type_id != f"T{index}":
            raise AssertionError("coverage type order changed")
        pattern = tuple(int(bit) for bit in coverage_type["pattern"])
        if pattern != normalized_pattern(pattern):
            raise AssertionError("coverage pattern is not canonical")
        mask = coverage_mask(pattern, buckets)
        if coverage_type["coverage_mask_hex"] != f"{mask:0{width}x}":
            raise AssertionError("coverage mask changed")
        registered_types[type_id] = mask
    if len(registered_types) != len(instance["coverage_types"]):
        raise AssertionError("duplicate coverage type identifier")
    if {
        mask: pattern for mask, pattern in sorted(source_types.items())
    } != {
        registered_types[f"T{index}"]: tuple(record["pattern"])
        for index, record in enumerate(instance["coverage_types"])
    }:
        raise AssertionError("source coverage types changed")

    upper_ids = tuple(str(value) for value in instance["upper_witness"])
    if len(set(upper_ids)) != len(upper_ids):
        raise AssertionError("upper witness repeats a type")
    try:
        upper_masks = tuple(registered_types[type_id] for type_id in upper_ids)
    except KeyError as error:
        raise AssertionError("upper witness names an unknown type") from error
    target = (1 << len(pairs)) - 1
    union = 0
    for mask in upper_masks:
        union |= mask
    if union != target:
        raise AssertionError("upper witness leaves an uncovered pair")

    lower = instance["private_pair_lower_witness"]
    if len(lower) != len(upper_ids):
        raise AssertionError("private-pair witness count changed")
    seen_types: set[str] = set()
    for witness in lower:
        type_id = str(witness["type_id"])
        if type_id not in upper_ids or type_id in seen_types:
            raise AssertionError("private-pair type changed")
        seen_types.add(type_id)
        pair_index = int(witness["pair_index"])
        if not 0 <= pair_index < len(pairs):
            raise AssertionError("private-pair index is outside the universe")
        if tuple(int(value) for value in witness["pair"]) != pairs[pair_index]:
            raise AssertionError("private-pair label changed")
        covering = tuple(
            candidate
            for candidate, mask in registered_types.items()
            if (mask >> pair_index) & 1
        )
        if covering != (type_id,):
            raise AssertionError("lower witness pair is not private")
    if seen_types != set(upper_ids):
        raise AssertionError("private-pair witness misses an upper type")

    masks = tuple(registered_types.values())
    observed_minimum = exact_minimum(masks, target)
    if observed_minimum != repair_count:
        raise AssertionError("abstract repair minimum changed")
    if int(instance["minimum_coordinate_count"]) != repair_count:
        raise AssertionError("registered repair minimum changed")
    cost = expected_cost(buckets, len(masks), repair_count)
    if instance["verification_cost"] != cost:
        raise AssertionError("verification cost ledger changed")
    return {
        "tracked_prime_count": len(tracked_primes),
        "pair_count": len(pairs),
        "coverage_type_count": len(masks),
        "minimum_coordinate_count": repair_count,
        "pattern_pair_tests": cost["pattern_pair_tests"],
        "private_type_tests": cost["private_type_tests"],
        "certificate_verifier_bit_tests": cost[
            "certificate_verifier_bit_tests"
        ],
        "defense_subset_count": cost["defense_subset_count"],
        "defense_mask_bit_tests": cost["defense_mask_bit_tests"],
        "source_file_bytes": path.stat().st_size,
        "abstract_certificate_payload_bits": cost[
            "abstract_certificate_payload_bits"
        ],
    }


def validate_all(
    schema: Mapping[str, Any] | None = None,
) -> dict[str, int]:
    """Validate the registered nine-instance certificate portfolio."""
    data = (
        json.loads(SCHEMA.read_text(encoding="utf-8"))
        if schema is None
        else dict(schema)
    )
    if data.get("schema_version") != "1.0.0":
        raise AssertionError("unsupported M92 schema version")
    if data.get("experiment_id") != "EXP-0063":
        raise AssertionError("M92 experiment ID changed")
    if data.get("claim_ids") != ["DEF-048", "THM-021", "EMP-063"]:
        raise AssertionError("M92 claim registry changed")
    if data.get("summary_sha256") != canonical_hash(data):
        raise AssertionError("M92 canonical summary hash changed")
    instances = data.get("instances")
    if not isinstance(instances, list) or len(instances) != 9:
        raise AssertionError("M92 instance count changed")
    reports = [validate_instance(instance) for instance in instances]
    if [int(instance["input_length"]) for instance in instances] != list(
        range(26, 35)
    ):
        raise AssertionError("M92 instance order changed")
    totals = {
        "instance_count": len(reports),
        "tracked_prime_count": sum(
            report["tracked_prime_count"] for report in reports
        ),
        "pair_count": sum(report["pair_count"] for report in reports),
        "coverage_type_count": sum(
            report["coverage_type_count"] for report in reports
        ),
        "minimum_coordinate_count": sum(
            report["minimum_coordinate_count"] for report in reports
        ),
        "pattern_pair_tests": sum(
            report["pattern_pair_tests"] for report in reports
        ),
        "private_type_tests": sum(
            report["private_type_tests"] for report in reports
        ),
        "certificate_verifier_bit_tests": sum(
            report["certificate_verifier_bit_tests"] for report in reports
        ),
        "defense_subset_count": sum(
            report["defense_subset_count"] for report in reports
        ),
        "defense_mask_bit_tests": sum(
            report["defense_mask_bit_tests"] for report in reports
        ),
        "source_file_bytes": sum(
            report["source_file_bytes"] for report in reports
        ),
        "abstract_certificate_payload_bits": sum(
            report["abstract_certificate_payload_bits"] for report in reports
        ),
    }
    if data.get("totals") != totals:
        raise AssertionError("M92 totals changed")
    return totals


def main() -> int:
    """Run the standalone certificate check."""
    totals = validate_all()
    print(
        "M92 pair-cover certificate checker: PASS "
        f"({totals['instance_count']} instances, "
        f"{totals['pair_count']} pairs, "
        f"{totals['coverage_type_count']} coverage types, "
        f"{totals['minimum_coordinate_count']} selected types, "
        f"{totals['abstract_certificate_payload_bits']} payload bits)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
