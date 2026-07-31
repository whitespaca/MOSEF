"""Build the M95 portfolio-wide coverer-graph profile."""

from __future__ import annotations

import hashlib
import itertools
import json
from collections import Counter
from collections.abc import Iterable, Mapping
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SOURCE_SPECS = (
    (
        "M92",
        ROOT / "schemas" / "m92-pair-cover-certificates-v1.json",
        "EMP-062",
    ),
    (
        "M93",
        ROOT / "schemas" / "m93-early-repair-certificates-v1.json",
        "EMP-064",
    ),
)
TEMPLATE_KINDS = (
    "loop_only",
    "looped_clique",
    "loopless_clique",
)


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
    """Use the public lexicographic within-bucket pair order."""
    return tuple(
        pair
        for bucket in buckets
        for pair in itertools.combinations(bucket, 2)
    )


def coverage_mask(
    pattern: tuple[int, ...],
    buckets: tuple[tuple[int, ...], ...],
) -> int:
    """Reconstruct one coverage mask from a normalized point pattern."""
    result = 0
    point_offset = 0
    pair_offset = 0
    for bucket in buckets:
        size = len(bucket)
        local = pattern[point_offset : point_offset + size]
        for left, right in itertools.combinations(range(size), 2):
            if local[left] != local[right]:
                result |= 1 << pair_offset
            pair_offset += 1
        point_offset += size
    if point_offset != len(pattern):
        raise AssertionError("coverage pattern length changed")
    return result


def or_masks(masks: Iterable[int]) -> int:
    """OR a finite mask sequence."""
    result = 0
    for mask in masks:
        result |= mask
    return result


def exact_cover_number(masks: tuple[int, ...], target: int) -> int:
    """Return the exact bounded cover number for a construction defense."""
    for size in range(len(masks) + 1):
        for subset in itertools.combinations(masks, size):
            if or_masks(subset) == target:
                return size
    raise AssertionError("coverage types do not cover the universe")


def coverer_records(
    type_ids: tuple[str, ...],
    masks: tuple[int, ...],
    pairs: tuple[tuple[int, int], ...],
) -> list[dict[str, Any]]:
    """Reconstruct the coverer set of every universe element."""
    records: list[dict[str, Any]] = []
    for pair_index, pair in enumerate(pairs):
        coverers = [
            type_id
            for type_id, mask in zip(type_ids, masks, strict=True)
            if (mask >> pair_index) & 1
        ]
        records.append(
            {
                "pair_index": pair_index,
                "pair": list(pair),
                "coverer_type_ids": coverers,
            }
        )
    return records


def template_slots(
    type_ids: tuple[str, ...],
    kind: str,
) -> list[tuple[str, ...]]:
    """Return the canonical slots of one graph-incidence template."""
    singles: list[tuple[str, ...]] = [
        (type_id,) for type_id in type_ids
    ]
    pairs: list[tuple[str, ...]] = list(
        itertools.combinations(type_ids, 2)
    )
    if kind == "loop_only":
        return singles
    if kind == "looped_clique":
        return singles + pairs
    if kind == "loopless_clique":
        return pairs
    raise AssertionError(f"unknown graph template: {kind}")


def classify_template(
    type_ids: tuple[str, ...],
    coverers: Iterable[Mapping[str, Any]],
) -> str:
    """Classify an exact loop/clique coverer-slot family."""
    observed = sorted(
        tuple(str(type_id) for type_id in record["coverer_type_ids"])
        for record in coverers
    )
    if any(len(slot) not in (1, 2) for slot in observed):
        raise AssertionError("coverer hyperedge rank exceeds two")
    for kind in TEMPLATE_KINDS:
        expected = sorted(template_slots(type_ids, kind))
        if observed == expected:
            return kind
    raise AssertionError("coverer slots do not match an M95 graph template")


def expected_cost(
    buckets: tuple[tuple[int, ...], ...],
    type_count: int,
    pair_count: int,
    incumbent: Mapping[str, Any],
) -> dict[str, int]:
    """Construct the graph-profile and incumbent cost comparison."""
    tracked = tuple(point for bucket in buckets for point in bucket)
    pattern_bits = type_count * len(tracked)
    mask_bits = type_count * pair_count
    label_bits = sum(point.bit_length() for point in tracked)
    pattern_tests = type_count * pair_count
    incidence_tests = type_count * pair_count
    slot_tests = pair_count
    payload = pattern_bits + mask_bits + label_bits
    verifier_tests = pattern_tests + incidence_tests + slot_tests
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
        "template_slot_tests": slot_tests,
        "certificate_verifier_bit_tests": verifier_tests,
        "incumbent_payload_bits": incumbent_payload,
        "payload_bits_saved": incumbent_payload - payload,
        "incumbent_verifier_bit_tests": incumbent_tests,
        "verifier_bit_test_delta": verifier_tests - incumbent_tests,
    }


def incumbent_witness_kind(source_id: str, source: Mapping[str, Any]) -> str:
    """Normalize the predecessor certificate kind."""
    if source_id == "M92":
        return "private_pairs"
    return str(source["lower_witness"]["kind"])


def build_instance(
    source_id: str,
    source: Mapping[str, Any],
) -> dict[str, Any]:
    """Build one source-bound coverer-graph profile."""
    buckets = tuple(
        tuple(int(point) for point in bucket)
        for bucket in source["collision_buckets"]
    )
    pairs = pair_universe(buckets)
    coverage_types: list[dict[str, Any]] = [
        {
            "type_id": str(record["type_id"]),
            "pattern": [int(bit) for bit in record["pattern"]],
            "coverage_mask_hex": str(record["coverage_mask_hex"]),
        }
        for record in source["coverage_types"]
    ]
    type_ids = tuple(str(record["type_id"]) for record in coverage_types)
    masks = tuple(
        int(record["coverage_mask_hex"], 16) for record in coverage_types
    )
    for record, mask in zip(coverage_types, masks, strict=True):
        pattern = tuple(int(bit) for bit in record["pattern"])
        if coverage_mask(pattern, buckets) != mask:
            raise AssertionError("source coverage mask changed")
    coverers = coverer_records(type_ids, masks, pairs)
    template_kind = classify_template(type_ids, coverers)
    degree_histogram = Counter(
        len(record["coverer_type_ids"]) for record in coverers
    )
    looped_type_ids = sorted(
        str(record["coverer_type_ids"][0])
        for record in coverers
        if len(record["coverer_type_ids"]) == 1
    )
    if template_kind == "loopless_clique":
        exact_minimum = len(type_ids) - 1
        implicit_upper = type_ids[:-1]
        implicit_upper_kind = "omit_last_type"
    else:
        exact_minimum = len(type_ids)
        implicit_upper = type_ids
        implicit_upper_kind = "all_types"
    target = (1 << len(pairs)) - 1
    masks_by_id = dict(zip(type_ids, masks, strict=True))
    if or_masks(masks_by_id[type_id] for type_id in implicit_upper) != target:
        raise AssertionError("implicit graph upper witness failed")
    if int(source["minimum_coordinate_count"]) != exact_minimum:
        raise AssertionError("source minimum does not match graph profile")
    if exact_cover_number(masks, target) != exact_minimum:
        raise AssertionError("bounded graph-cover defense failed")
    return {
        "source_id": source_id,
        "input_length": int(source["input_length"]),
        "source_instance_sha256": canonical_hash(source),
        "collision_buckets": [list(bucket) for bucket in buckets],
        "tracked_point_count": sum(len(bucket) for bucket in buckets),
        "pair_count": len(pairs),
        "type_count": len(type_ids),
        "coverage_types": coverage_types,
        "coverer_sets": coverers,
        "column_degree_histogram": {
            str(degree): degree_histogram[degree]
            for degree in sorted(degree_histogram)
        },
        "coverer_incidence_count": sum(
            len(record["coverer_type_ids"]) for record in coverers
        ),
        "template_kind": template_kind,
        "looped_type_ids": looped_type_ids,
        "implicit_upper_kind": implicit_upper_kind,
        "exact_repair_number": exact_minimum,
        "incumbent_lower_witness_kind": incumbent_witness_kind(
            source_id,
            source,
        ),
        "verification_cost": expected_cost(
            buckets,
            len(type_ids),
            len(pairs),
            source["verification_cost"],
        ),
    }


def boundary_counterexample() -> dict[str, Any]:
    """Return two rank-two profiles with different exact minima."""
    return {
        "shared_profile": {
            "type_count": 4,
            "universe_count": 3,
            "column_degree_histogram": {"2": 3},
        },
        "star_k1_3": {
            "edges": [["T0", "T1"], ["T0", "T2"], ["T0", "T3"]],
            "exact_cover_number": 1,
        },
        "path_p4": {
            "edges": [["T0", "T1"], ["T1", "T2"], ["T2", "T3"]],
            "exact_cover_number": 2,
        },
    }


def build_summary() -> dict[str, Any]:
    """Build the canonical M95 graph-profile summary."""
    sources: list[dict[str, Any]] = []
    instances: list[dict[str, Any]] = []
    for source_id, path, dependency in SOURCE_SPECS:
        source = json.loads(path.read_text(encoding="utf-8"))
        sources.append(
            {
                "source_id": source_id,
                "path": str(path.relative_to(ROOT)).replace("\\", "/"),
                "file_sha256": file_sha256(path),
                "summary_sha256": str(source["summary_sha256"]),
                "semantic_dependency": dependency,
            }
        )
        instances.extend(
            build_instance(source_id, instance)
            for instance in source["instances"]
        )
    cost_fields = (
        "abstract_certificate_payload_bits",
        "certificate_verifier_bit_tests",
        "incumbent_payload_bits",
        "payload_bits_saved",
        "incumbent_verifier_bit_tests",
        "verifier_bit_test_delta",
    )
    template_counts = Counter(
        str(instance["template_kind"]) for instance in instances
    )
    summary: dict[str, Any] = {
        "schema_version": "1.0.0",
        "experiment_id": "EXP-0066",
        "claim_ids": ["DEF-051", "THM-024", "REF-064", "EMP-066"],
        "sources": sources,
        "instances": instances,
        "rank_two_boundary_counterexample": boundary_counterexample(),
        "totals": {
            "instance_count": len(instances),
            "tracked_point_count": sum(
                int(instance["tracked_point_count"])
                for instance in instances
            ),
            "pair_count": sum(
                int(instance["pair_count"]) for instance in instances
            ),
            "type_count": sum(
                int(instance["type_count"]) for instance in instances
            ),
            "coverer_incidence_count": sum(
                int(instance["coverer_incidence_count"])
                for instance in instances
            ),
            "degree_one_column_count": sum(
                int(instance["column_degree_histogram"].get("1", 0))
                for instance in instances
            ),
            "degree_two_column_count": sum(
                int(instance["column_degree_histogram"].get("2", 0))
                for instance in instances
            ),
            "minimum_coordinate_count": sum(
                int(instance["exact_repair_number"])
                for instance in instances
            ),
            "template_counts": {
                kind: template_counts[kind] for kind in TEMPLATE_KINDS
            },
            **{
                field: sum(
                    int(instance["verification_cost"][field])
                    for instance in instances
                )
                for field in cost_fields
            },
        },
        "scope": {
            "classification": "EMPIRICAL",
            "finite_input_lengths": list(range(16, 35)),
            "complete_type_dependencies": ["EMP-062", "EMP-064"],
            "not_claimed": [
                "rank at most two for another repair portfolio",
                "a polynomial exact solver for arbitrary coverer graphs",
                "a factor-promise recognizer",
                "an asymptotic selector theorem",
                "general classical polynomial-time factoring",
            ],
        },
    }
    summary["summary_sha256"] = canonical_hash(summary)
    return summary


def main() -> int:
    """Print the deterministic M95 profile summary."""
    summary = build_summary()
    totals = summary["totals"]
    print(
        "M95 coverer-graph profile: PASS "
        f"({totals['instance_count']} instances, "
        f"{totals['pair_count']} columns, "
        f"{totals['degree_one_column_count']} loops, "
        f"{totals['degree_two_column_count']} ordinary edges, "
        f"{totals['payload_bits_saved']} payload bits saved)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
