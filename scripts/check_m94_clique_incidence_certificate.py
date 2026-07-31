"""Independently validate the M94 complete-graph incidence certificates."""

from __future__ import annotations

import hashlib
import itertools
import json
import math
from collections.abc import Iterable, Mapping
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas" / "m94-clique-incidence-certificates-v1.json"
SOURCE = ROOT / "schemas" / "m93-early-repair-certificates-v1.json"
SOURCE_FILE_SHA256 = (
    "3fba1bc8ef78594e32083f8576a43874159390bbccbcc669b658015ce8431641"
)
SOURCE_SUMMARY_SHA256 = (
    "77c8ae289277875815e7744b37456627f619fc601d4fb2ccca35031b7f248aae"
)
TARGET_LENGTHS = (16, 24)


def canonical_hash(record: Mapping[str, Any]) -> str:
    """Hash one record after removing its self-hash."""
    payload = dict(record)
    payload.pop("summary_sha256", None)
    return hashlib.sha256(
        json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
        ).encode("utf-8")
    ).hexdigest()


def file_sha256(path: Path) -> str:
    """Return the SHA-256 digest of one file."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pair_universe(
    buckets: tuple[tuple[int, ...], ...],
) -> tuple[tuple[int, int], ...]:
    """Independently reconstruct the within-bucket pair order."""
    return tuple(
        pair
        for bucket in buckets
        for pair in itertools.combinations(bucket, 2)
    )


def coverage_mask(
    pattern: tuple[int, ...],
    buckets: tuple[tuple[int, ...], ...],
) -> int:
    """Rebuild one pair-coverage mask from its point pattern."""
    result = 0
    offset = 0
    point_offset = 0
    for bucket in buckets:
        size = len(bucket)
        local = pattern[point_offset : point_offset + size]
        for left, right in itertools.combinations(range(size), 2):
            if local[left] != local[right]:
                result |= 1 << offset
            offset += 1
        point_offset += size
    if point_offset != len(pattern):
        raise AssertionError("coverage pattern length changed")
    return result


def or_masks(masks: Iterable[int]) -> int:
    """OR a finite sequence of masks."""
    result = 0
    for mask in masks:
        result |= mask
    return result


def exact_cover_number(masks: tuple[int, ...], target: int) -> int:
    """Return the exact bounded cover number for defense only."""
    for size in range(len(masks) + 1):
        for subset in itertools.combinations(masks, size):
            if or_masks(subset) == target:
                return size
    raise AssertionError("coverage types do not cover the universe")


def reconstruct_coverers(
    type_ids: tuple[str, ...],
    masks: tuple[int, ...],
    pairs: tuple[tuple[int, int], ...],
) -> list[dict[str, Any]]:
    """Rebuild the coverer set of every universe element."""
    result: list[dict[str, Any]] = []
    for pair_index, pair in enumerate(pairs):
        result.append(
            {
                "pair_index": pair_index,
                "pair": list(pair),
                "coverer_type_ids": [
                    type_id
                    for type_id, mask in zip(type_ids, masks, strict=True)
                    if (mask >> pair_index) & 1
                ],
            }
        )
    return result


def expected_cost(
    buckets: tuple[tuple[int, ...], ...],
    type_count: int,
    pair_count: int,
    incumbent: Mapping[str, Any],
) -> dict[str, int]:
    """Reconstruct the compact structural and incumbent cost ledger."""
    tracked = tuple(prime for bucket in buckets for prime in bucket)
    pattern_bits = type_count * len(tracked)
    mask_bits = type_count * pair_count
    label_bits = sum(prime.bit_length() for prime in tracked)
    pattern_tests = type_count * pair_count
    incidence_tests = type_count * pair_count
    pair_slot_tests = pair_count
    payload = pattern_bits + mask_bits + label_bits
    verifier_tests = pattern_tests + incidence_tests + pair_slot_tests
    incumbent_payload = int(incumbent["abstract_certificate_payload_bits"])
    incumbent_tests = int(incumbent["certificate_verifier_bit_tests"])
    return {
        "pattern_storage_bits": pattern_bits,
        "mask_storage_bits": mask_bits,
        "bucket_label_bits": label_bits,
        "upper_witness_index_bits": 0,
        "lower_witness_payload_bits": 0,
        "abstract_certificate_payload_bits": payload,
        "pattern_pair_tests": pattern_tests,
        "incidence_mask_bit_tests": incidence_tests,
        "pair_slot_tests": pair_slot_tests,
        "certificate_verifier_bit_tests": verifier_tests,
        "incumbent_payload_bits": incumbent_payload,
        "payload_bits_saved": incumbent_payload - payload,
        "incumbent_verifier_bit_tests": incumbent_tests,
        "verifier_bit_test_delta": verifier_tests - incumbent_tests,
    }


def validate_instance(
    instance: Mapping[str, Any],
    source: Mapping[str, Any],
) -> dict[str, int]:
    """Validate one complete-graph incidence certificate."""
    input_length = int(instance["input_length"])
    if input_length != int(source["input_length"]):
        raise AssertionError("M94 source length changed")
    if instance["source_instance_sha256"] != canonical_hash(source):
        raise AssertionError("M94 source instance hash changed")
    buckets = tuple(
        tuple(int(prime) for prime in bucket)
        for bucket in source["collision_buckets"]
    )
    registered_buckets = tuple(
        tuple(int(prime) for prime in bucket)
        for bucket in instance["collision_buckets"]
    )
    if registered_buckets != buckets:
        raise AssertionError("M94 collision buckets changed")
    pairs = pair_universe(buckets)
    source_types = source["coverage_types"]
    registered_types = instance["coverage_types"]
    if len(registered_types) != len(source_types):
        raise AssertionError("M94 coverage type count changed")
    expected_types: list[dict[str, Any]] = []
    masks: list[int] = []
    for index, record in enumerate(registered_types):
        type_id = f"T{index}"
        if record["type_id"] != type_id:
            raise AssertionError("M94 coverage type order changed")
        pattern = tuple(int(bit) for bit in record["pattern"])
        if not pattern or pattern[0] != 0 or any(
            bit not in (0, 1) for bit in pattern
        ):
            raise AssertionError("M94 coverage pattern is not canonical")
        mask = coverage_mask(pattern, buckets)
        width = max(1, math.ceil(len(pairs) / 4))
        expected_types.append(
            {
                "type_id": type_id,
                "pattern": list(pattern),
                "coverage_mask_hex": f"{mask:0{width}x}",
            }
        )
        masks.append(mask)
    stripped_source = [
        {
            "type_id": str(record["type_id"]),
            "pattern": [int(bit) for bit in record["pattern"]],
            "coverage_mask_hex": str(record["coverage_mask_hex"]),
        }
        for record in source_types
    ]
    if registered_types != expected_types:
        raise AssertionError("M94 coverage masks changed")
    if registered_types != stripped_source:
        raise AssertionError("M94 source coverage types changed")
    type_ids = tuple(str(record["type_id"]) for record in expected_types)
    mask_tuple = tuple(masks)
    coverers = reconstruct_coverers(type_ids, mask_tuple, pairs)
    if instance["coverer_sets"] != coverers:
        raise AssertionError("M94 coverer sets changed")
    if any(len(record["coverer_type_ids"]) != 2 for record in coverers):
        raise AssertionError("M94 column does not have two coverers")
    observed_pairs: list[tuple[str, ...]] = [
        tuple(str(type_id) for type_id in record["coverer_type_ids"])
        for record in coverers
    ]
    expected_pairs = list(itertools.combinations(type_ids, 2))
    if len(pairs) != math.comb(len(type_ids), 2):
        raise AssertionError("M94 universe size is not a clique edge count")
    if sorted(observed_pairs) != expected_pairs:
        raise AssertionError("M94 type pairs do not form a complete graph")
    expected_minimum = len(type_ids) - 1
    if int(instance["exact_repair_number"]) != expected_minimum:
        raise AssertionError("M94 exact repair number changed")
    if int(source["minimum_coordinate_count"]) != expected_minimum:
        raise AssertionError("M94 source minimum changed")
    if instance["canonical_omitted_type_id"] != type_ids[-1]:
        raise AssertionError("M94 canonical omitted type changed")
    target = (1 << len(pairs)) - 1
    if or_masks(mask_tuple[:-1]) != target:
        raise AssertionError("M94 implicit upper witness failed")
    if exact_cover_number(mask_tuple, target) != expected_minimum:
        raise AssertionError("M94 bounded exact-cover defense failed")
    if (
        instance["incumbent_lower_witness_kind"]
        != source["lower_witness"]["kind"]
    ):
        raise AssertionError("M94 incumbent witness kind changed")
    expected = expected_cost(
        buckets,
        len(type_ids),
        len(pairs),
        source["verification_cost"],
    )
    if instance["verification_cost"] != expected:
        raise AssertionError("M94 verification cost changed")
    if int(instance["tracked_point_count"]) != sum(
        len(bucket) for bucket in buckets
    ):
        raise AssertionError("M94 tracked point count changed")
    if int(instance["pair_count"]) != len(pairs):
        raise AssertionError("M94 pair count changed")
    if int(instance["type_count"]) != len(type_ids):
        raise AssertionError("M94 type count changed")
    if int(instance["complete_graph_edge_count"]) != len(pairs):
        raise AssertionError("M94 complete graph edge count changed")
    return {
        "tracked_point_count": sum(len(bucket) for bucket in buckets),
        "pair_count": len(pairs),
        "type_count": len(type_ids),
        "coverer_incidence_count": 2 * len(pairs),
        **{
            field: expected[field]
            for field in (
                "abstract_certificate_payload_bits",
                "certificate_verifier_bit_tests",
                "incumbent_payload_bits",
                "payload_bits_saved",
                "incumbent_verifier_bit_tests",
                "verifier_bit_test_delta",
            )
        },
    }


def validate_all(
    schema: Mapping[str, Any] | None = None,
    source: Mapping[str, Any] | None = None,
) -> dict[str, int]:
    """Validate the two-instance M94 portfolio."""
    data = (
        json.loads(SCHEMA.read_text(encoding="utf-8"))
        if schema is None
        else dict(schema)
    )
    m93 = (
        json.loads(SOURCE.read_text(encoding="utf-8"))
        if source is None
        else dict(source)
    )
    if source is None and file_sha256(SOURCE) != SOURCE_FILE_SHA256:
        raise AssertionError("M94 M93 source file hash changed")
    if m93.get("summary_sha256") != SOURCE_SUMMARY_SHA256:
        raise AssertionError("M94 M93 source summary hash changed")
    if canonical_hash(m93) != SOURCE_SUMMARY_SHA256:
        raise AssertionError("M94 M93 source content changed")
    expected_source = {
        "path": "schemas/m93-early-repair-certificates-v1.json",
        "file_sha256": SOURCE_FILE_SHA256,
        "summary_sha256": SOURCE_SUMMARY_SHA256,
    }
    if data.get("source") != expected_source:
        raise AssertionError("M94 source anchor changed")
    if data.get("schema_version") != "1.0.0":
        raise AssertionError("unsupported M94 schema version")
    if data.get("experiment_id") != "EXP-0065":
        raise AssertionError("M94 experiment ID changed")
    if data.get("claim_ids") != [
        "DEF-050",
        "THM-023",
        "REF-063",
        "EMP-065",
    ]:
        raise AssertionError("M94 claim registry changed")
    if data.get("summary_sha256") != canonical_hash(data):
        raise AssertionError("M94 canonical summary hash changed")
    instances = data.get("instances")
    if not isinstance(instances, list) or len(instances) != 2:
        raise AssertionError("M94 instance count changed")
    if [int(instance["input_length"]) for instance in instances] != list(
        TARGET_LENGTHS
    ):
        raise AssertionError("M94 instance order changed")
    by_length = {
        int(instance["input_length"]): instance
        for instance in m93["instances"]
    }
    reports = [
        validate_instance(
            instance,
            by_length[int(instance["input_length"])],
        )
        for instance in instances
    ]
    fields = (
        "tracked_point_count",
        "pair_count",
        "type_count",
        "coverer_incidence_count",
        "abstract_certificate_payload_bits",
        "certificate_verifier_bit_tests",
        "incumbent_payload_bits",
        "payload_bits_saved",
        "incumbent_verifier_bit_tests",
        "verifier_bit_test_delta",
    )
    totals = {
        "instance_count": len(reports),
        **{
            field: sum(report[field] for report in reports)
            for field in fields
        },
    }
    if data.get("totals") != totals:
        raise AssertionError("M94 totals changed")
    return totals


def main() -> int:
    """Run the standalone incidence checker."""
    totals = validate_all()
    print(
        "M94 clique-incidence certificate checker: PASS "
        f"({totals['instance_count']} instances, "
        f"{totals['pair_count']} pairs, "
        f"{totals['coverer_incidence_count']} incidences, "
        f"{totals['payload_bits_saved']} payload bits saved)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
