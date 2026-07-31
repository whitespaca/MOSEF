"""Build compact pair-cover certificates for the nine finite repairs."""

from __future__ import annotations

import hashlib
import json
import math
from collections.abc import Iterable
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SOURCE_BY_LENGTH = {
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


def file_sha256(path: Path) -> str:
    """Return one binary file digest."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_hash(record: dict[str, Any]) -> str:
    """Hash a JSON object while excluding its hash field."""
    payload = dict(record)
    payload.pop("summary_sha256", None)
    encoded = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def registered_patterns(
    certificate: dict[str, Any],
) -> tuple[tuple[int, ...], ...]:
    """Read the three historical repair-pattern spellings."""
    raw = certificate.get("new_source_patterns_on_final_collision")
    if raw is None:
        raw = certificate.get("new_source_patterns")
    if raw is None and certificate.get("new_source_pattern") is not None:
        raw = [certificate["new_source_pattern"]]
    if not isinstance(raw, list):
        raise AssertionError("missing repair patterns")
    return tuple(tuple(int(bit) for bit in pattern) for pattern in raw)


def normalized_pattern(pattern: tuple[int, ...]) -> tuple[int, ...]:
    """Choose a canonical representative modulo binary complementation."""
    if not pattern or any(bit not in (0, 1) for bit in pattern):
        raise AssertionError("repair pattern is not a nonempty bit vector")
    complement = tuple(1 - bit for bit in pattern)
    return min(pattern, complement)


def pair_universe(
    buckets: tuple[tuple[int, ...], ...],
) -> tuple[tuple[int, int], ...]:
    """Enumerate within-bucket pairs in the public canonical order."""
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
    """Encode the pairs separated by one tracked binary pattern."""
    mask = 0
    pair_index = 0
    pattern_offset = 0
    for bucket in buckets:
        for left in range(len(bucket)):
            for right in range(left + 1, len(bucket)):
                if pattern[pattern_offset + left] != pattern[
                    pattern_offset + right
                ]:
                    mask |= 1 << pair_index
                pair_index += 1
        pattern_offset += len(bucket)
    return mask


def exact_log2_width(value_count: int) -> int:
    """Return bits needed for an index into a nonempty finite set."""
    if value_count <= 1:
        return 0
    return math.ceil(math.log2(value_count))


def source_fields(
    input_length: int,
    data: dict[str, Any],
) -> tuple[
    int,
    int,
    tuple[tuple[int, ...], ...],
    int,
    tuple[tuple[int, ...], ...],
    tuple[str, ...],
]:
    """Project the repair fields across M38--M46 schema generations."""
    certificate = data["construction_certificate"]
    repair_cap = int(data["repair_profile"]["selector_cap"])
    if input_length in (27, 28):
        base_profile = data["cap_profile"]
    else:
        base_profile = data["predecessor_profile"]
    base_cap = int(base_profile["selector_cap"])
    buckets = tuple(
        tuple(int(prime) for prime in bucket)
        for bucket in base_profile["collision_buckets"]
    )
    minimum = data["repair_profile"].get("new_repair_coordinate_count")
    if minimum is None:
        minimum = certificate["minimum_new_coordinate_count"]
    repair_count = int(minimum)
    patterns = registered_patterns(certificate)
    sources = tuple(str(source) for source in certificate["column_sources"])
    return (
        base_cap,
        repair_cap,
        buckets,
        repair_count,
        patterns,
        sources[-repair_count:],
    )


def build_instance(input_length: int, source_path: str) -> dict[str, Any]:
    """Construct one exact upper/private-pair certificate."""
    path = ROOT / source_path
    data = json.loads(path.read_text(encoding="utf-8"))
    (
        base_cap,
        repair_cap,
        buckets,
        repair_count,
        raw_patterns,
        repair_sources,
    ) = source_fields(input_length, data)
    tracked_primes = tuple(prime for bucket in buckets for prime in bucket)
    pairs = pair_universe(buckets)
    pair_index = {pair: index for index, pair in enumerate(pairs)}
    width = max(1, math.ceil(len(pairs) / 4))

    pattern_by_mask: dict[int, tuple[int, ...]] = {}
    for raw_pattern in raw_patterns:
        pattern = normalized_pattern(raw_pattern)
        if len(pattern) != len(tracked_primes):
            raise AssertionError("repair pattern width changed")
        mask = coverage_mask(pattern, buckets)
        if mask == 0:
            raise AssertionError("zero repair coverage is not useful")
        pattern_by_mask.setdefault(mask, pattern)
    if len(pattern_by_mask) != repair_count:
        raise AssertionError("repair types do not match the minimum")

    ordered_types = sorted(pattern_by_mask.items())
    type_ids = tuple(f"T{index}" for index in range(len(ordered_types)))
    coverage_types = [
        {
            "type_id": type_id,
            "pattern": list(pattern),
            "coverage_mask_hex": f"{mask:0{width}x}",
        }
        for type_id, (mask, pattern) in zip(
            type_ids,
            ordered_types,
            strict=True,
        )
    ]
    target = (1 << len(pairs)) - 1
    if _or_masks(mask for mask, _ in ordered_types) != target:
        raise AssertionError("registered repair types do not cover every pair")

    private_pairs: list[dict[str, object]] = []
    for type_id, (mask, _pattern) in zip(
        type_ids,
        ordered_types,
        strict=True,
    ):
        private_index = next(
            (
                index
                for index in range(len(pairs))
                if (mask >> index) & 1
                and sum(
                    (other_mask >> index) & 1
                    for other_mask, _ in ordered_types
                )
                == 1
            ),
            None,
        )
        if private_index is None:
            raise AssertionError("repair type lacks a private pair")
        private_pairs.append(
            {
                "type_id": type_id,
                "pair_index": private_index,
                "pair": list(pairs[private_index]),
            }
        )
        if pair_index[pairs[private_index]] != private_index:
            raise AssertionError("pair index construction changed")

    type_count = len(ordered_types)
    pair_count = len(pairs)
    index_bits = repair_count * exact_log2_width(type_count)
    private_bits = repair_count * exact_log2_width(pair_count)
    label_bits = sum(prime.bit_length() for prime in tracked_primes)
    cost = {
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
        "selected_type_index_bits": index_bits,
        "private_pair_index_bits": private_bits,
        "bucket_label_bits": label_bits,
        "abstract_certificate_payload_bits": (
            type_count * (pair_count + len(tracked_primes))
            + index_bits
            + private_bits
            + label_bits
        ),
    }
    return {
        "input_length": input_length,
        "source_path": source_path,
        "source_sha256": file_sha256(path),
        "source_file_bytes": path.stat().st_size,
        "semantic_anchor": "EMP-062",
        "base_cap": base_cap,
        "repair_cap": repair_cap,
        "collision_buckets": [list(bucket) for bucket in buckets],
        "tracked_prime_count": len(tracked_primes),
        "pair_count": pair_count,
        "coverage_types": coverage_types,
        "upper_witness": list(type_ids),
        "private_pair_lower_witness": private_pairs,
        "repair_sources": list(repair_sources),
        "minimum_coordinate_count": repair_count,
        "verification_cost": cost,
    }


def _or_masks(masks: Iterable[int]) -> int:
    """OR an iterable of integer masks without importing functools."""
    result = 0
    for mask in masks:
        result |= int(mask)
    return result


def build_summary() -> dict[str, Any]:
    """Build the complete registered M92 schema."""
    instances = [
        build_instance(input_length, source_path)
        for input_length, source_path in SOURCE_BY_LENGTH.items()
    ]
    totals = {
        "instance_count": len(instances),
        "tracked_prime_count": sum(
            int(instance["tracked_prime_count"]) for instance in instances
        ),
        "pair_count": sum(int(instance["pair_count"]) for instance in instances),
        "coverage_type_count": sum(
            len(instance["coverage_types"]) for instance in instances
        ),
        "minimum_coordinate_count": sum(
            int(instance["minimum_coordinate_count"]) for instance in instances
        ),
        "pattern_pair_tests": sum(
            int(instance["verification_cost"]["pattern_pair_tests"])
            for instance in instances
        ),
        "private_type_tests": sum(
            int(instance["verification_cost"]["private_type_tests"])
            for instance in instances
        ),
        "certificate_verifier_bit_tests": sum(
            int(
                instance["verification_cost"][
                    "certificate_verifier_bit_tests"
                ]
            )
            for instance in instances
        ),
        "defense_subset_count": sum(
            int(instance["verification_cost"]["defense_subset_count"])
            for instance in instances
        ),
        "defense_mask_bit_tests": sum(
            int(instance["verification_cost"]["defense_mask_bit_tests"])
            for instance in instances
        ),
        "source_file_bytes": sum(
            int(instance["source_file_bytes"]) for instance in instances
        ),
        "abstract_certificate_payload_bits": sum(
            int(
                instance["verification_cost"][
                    "abstract_certificate_payload_bits"
                ]
            )
            for instance in instances
        ),
    }
    summary: dict[str, Any] = {
        "schema_version": "1.0.0",
        "experiment_id": "EXP-0063",
        "claim_ids": ["DEF-048", "THM-021", "EMP-063"],
        "pair_order": (
            "bucket order, then increasing left index, then increasing right index"
        ),
        "complement_rule": (
            "binary patterns are canonicalized with their bitwise complement"
        ),
        "semantic_dependency": {
            "claim_id": "EMP-062",
            "scope": (
                "exhaustiveness of each frozen raw-coordinate coverage type"
            ),
        },
        "instances": instances,
        "totals": totals,
        "status": "PASS",
    }
    summary["summary_sha256"] = canonical_hash(summary)
    return summary


def main() -> int:
    """Run the abstract certificate construction."""
    summary = build_summary()
    totals = summary["totals"]
    print(
        "M92 pair-cover audit: PASS "
        f"({totals['instance_count']} instances, "
        f"{totals['pair_count']} pairs, "
        f"{totals['coverage_type_count']} coverage types, "
        f"{totals['abstract_certificate_payload_bits']} payload bits, "
        f"summary_sha256={summary['summary_sha256']})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
