"""Independently validate the M95 coverer-graph portfolio."""

from __future__ import annotations

import hashlib
import itertools
import json
from collections import Counter
from collections.abc import Iterable, Mapping
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas" / "m95-coverer-graph-profile-v1.json"
SOURCE_PATHS = {
    "M92": ROOT / "schemas" / "m92-pair-cover-certificates-v1.json",
    "M93": ROOT / "schemas" / "m93-early-repair-certificates-v1.json",
}
SOURCE_ANCHORS = {
    "M92": {
        "path": "schemas/m92-pair-cover-certificates-v1.json",
        "file_sha256": (
            "0c58d6d28079aac4975861836b714c9c8d63e805bbc86c5c3b101b3c85ae636e"
        ),
        "summary_sha256": (
            "3bf4b744d30d31f5e52725ca9cb70302bc4654ab1e7cfbe1707448392dbc19b0"
        ),
        "semantic_dependency": "EMP-062",
    },
    "M93": {
        "path": "schemas/m93-early-repair-certificates-v1.json",
        "file_sha256": (
            "3fba1bc8ef78594e32083f8576a43874159390bbccbcc669b658015ce8431641"
        ),
        "summary_sha256": (
            "77c8ae289277875815e7744b37456627f619fc601d4fb2ccca35031b7f248aae"
        ),
        "semantic_dependency": "EMP-064",
    },
}
SOURCE_LENGTHS = {
    "M92": tuple(range(26, 35)),
    "M93": tuple(range(16, 26)),
}
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
    """Independently rebuild one mask from its normalized pattern."""
    result = 0
    point_offset = 0
    pair_offset = 0
    for bucket in buckets:
        size = len(bucket)
        local = pattern[point_offset : point_offset + size]
        if len(local) != size:
            raise AssertionError("coverage pattern is too short")
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
    """Return the exact bounded set-cover number for defense only."""
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
    """Reconstruct every coverer set directly from masks."""
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


def template_slots(
    type_ids: tuple[str, ...],
    kind: str,
) -> list[tuple[str, ...]]:
    """Return one canonical loop/clique template."""
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
    """Classify an exact rank-one/two slot family."""
    observed = sorted(
        tuple(str(type_id) for type_id in record["coverer_type_ids"])
        for record in coverers
    )
    if any(len(slot) not in (1, 2) for slot in observed):
        raise AssertionError("coverer hyperedge rank exceeds two")
    for kind in TEMPLATE_KINDS:
        if observed == sorted(template_slots(type_ids, kind)):
            return kind
    raise AssertionError("coverer slots do not match an M95 graph template")


def graph_cover_number(
    type_ids: tuple[str, ...],
    slots: tuple[tuple[str, ...], ...],
) -> int:
    """Return the exact cover number of a small looped graph."""
    for size in range(len(type_ids) + 1):
        for selected in itertools.combinations(type_ids, size):
            chosen = set(selected)
            if all(chosen.intersection(slot) for slot in slots):
                return size
    raise AssertionError("graph slots cannot be covered")


def expected_cost(
    buckets: tuple[tuple[int, ...], ...],
    type_count: int,
    pair_count: int,
    incumbent: Mapping[str, Any],
) -> dict[str, int]:
    """Reconstruct the graph-profile and incumbent cost ledger."""
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
    """Normalize the incumbent lower-certificate label."""
    if source_id == "M92":
        return "private_pairs"
    return str(source["lower_witness"]["kind"])


def validate_instance(
    instance: Mapping[str, Any],
    source_id: str,
    source: Mapping[str, Any],
) -> dict[str, int | str]:
    """Validate one source-bound graph-template certificate."""
    if instance["source_id"] != source_id:
        raise AssertionError("M95 source ID changed")
    if int(instance["input_length"]) != int(source["input_length"]):
        raise AssertionError("M95 source length changed")
    if instance["source_instance_sha256"] != canonical_hash(source):
        raise AssertionError("M95 source instance hash changed")
    buckets = tuple(
        tuple(int(point) for point in bucket)
        for bucket in source["collision_buckets"]
    )
    registered_buckets = tuple(
        tuple(int(point) for point in bucket)
        for bucket in instance["collision_buckets"]
    )
    if registered_buckets != buckets:
        raise AssertionError("M95 collision buckets changed")
    pairs = pair_universe(buckets)
    registered_types = instance["coverage_types"]
    source_types = source["coverage_types"]
    if len(registered_types) != len(source_types):
        raise AssertionError("M95 coverage type count changed")
    expected_types: list[dict[str, Any]] = []
    masks: list[int] = []
    for index, record in enumerate(registered_types):
        type_id = f"T{index}"
        if record["type_id"] != type_id:
            raise AssertionError("M95 coverage type order changed")
        pattern = tuple(int(bit) for bit in record["pattern"])
        if not pattern or pattern[0] != 0 or any(
            bit not in (0, 1) for bit in pattern
        ):
            raise AssertionError("M95 coverage pattern is not canonical")
        mask = coverage_mask(pattern, buckets)
        width = max(1, (len(pairs) + 3) // 4)
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
        raise AssertionError("M95 coverage masks changed")
    if registered_types != stripped_source:
        raise AssertionError("M95 source coverage types changed")
    type_ids = tuple(str(record["type_id"]) for record in expected_types)
    mask_tuple = tuple(masks)
    coverers = reconstruct_coverers(type_ids, mask_tuple, pairs)
    if instance["coverer_sets"] != coverers:
        raise AssertionError("M95 coverer sets changed")
    template_kind = classify_template(type_ids, coverers)
    if instance["template_kind"] != template_kind:
        raise AssertionError("M95 graph template changed")
    histogram = Counter(
        len(record["coverer_type_ids"]) for record in coverers
    )
    expected_histogram = {
        str(degree): histogram[degree] for degree in sorted(histogram)
    }
    if instance["column_degree_histogram"] != expected_histogram:
        raise AssertionError("M95 degree histogram changed")
    looped_type_ids = sorted(
        str(record["coverer_type_ids"][0])
        for record in coverers
        if len(record["coverer_type_ids"]) == 1
    )
    if instance["looped_type_ids"] != looped_type_ids:
        raise AssertionError("M95 looped type list changed")
    if template_kind == "loopless_clique":
        expected_minimum = len(type_ids) - 1
        upper_type_ids = type_ids[:-1]
        upper_kind = "omit_last_type"
    else:
        expected_minimum = len(type_ids)
        upper_type_ids = type_ids
        upper_kind = "all_types"
    if instance["implicit_upper_kind"] != upper_kind:
        raise AssertionError("M95 implicit upper kind changed")
    if int(instance["exact_repair_number"]) != expected_minimum:
        raise AssertionError("M95 exact repair number changed")
    if int(source["minimum_coordinate_count"]) != expected_minimum:
        raise AssertionError("M95 source minimum changed")
    target = (1 << len(pairs)) - 1
    masks_by_id = dict(zip(type_ids, mask_tuple, strict=True))
    if or_masks(masks_by_id[type_id] for type_id in upper_type_ids) != target:
        raise AssertionError("M95 implicit upper witness failed")
    if exact_cover_number(mask_tuple, target) != expected_minimum:
        raise AssertionError("M95 bounded exact-cover defense failed")
    if (
        instance["incumbent_lower_witness_kind"]
        != incumbent_witness_kind(source_id, source)
    ):
        raise AssertionError("M95 incumbent witness kind changed")
    cost = expected_cost(
        buckets,
        len(type_ids),
        len(pairs),
        source["verification_cost"],
    )
    if instance["verification_cost"] != cost:
        raise AssertionError("M95 verification cost changed")
    tracked_count = sum(len(bucket) for bucket in buckets)
    incidence_count = sum(
        len(record["coverer_type_ids"]) for record in coverers
    )
    scalar_fields = {
        "tracked_point_count": tracked_count,
        "pair_count": len(pairs),
        "type_count": len(type_ids),
        "coverer_incidence_count": incidence_count,
    }
    for field, expected in scalar_fields.items():
        if int(instance[field]) != expected:
            raise AssertionError(f"M95 {field} changed")
    return {
        **scalar_fields,
        "degree_one_column_count": histogram[1],
        "degree_two_column_count": histogram[2],
        "minimum_coordinate_count": expected_minimum,
        "template_kind": template_kind,
        **{
            field: cost[field]
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


def validate_boundary(record: Mapping[str, Any]) -> None:
    """Validate the same-profile star/path counterexample."""
    expected_profile = {
        "type_count": 4,
        "universe_count": 3,
        "column_degree_histogram": {"2": 3},
    }
    if record.get("shared_profile") != expected_profile:
        raise AssertionError("M95 boundary profile changed")
    type_ids = ("T0", "T1", "T2", "T3")
    expected_edges = {
        "star_k1_3": (
            ("T0", "T1"),
            ("T0", "T2"),
            ("T0", "T3"),
        ),
        "path_p4": (
            ("T0", "T1"),
            ("T1", "T2"),
            ("T2", "T3"),
        ),
    }
    expected_minima = {"star_k1_3": 1, "path_p4": 2}
    for name, edges in expected_edges.items():
        registered = record.get(name)
        if not isinstance(registered, Mapping):
            raise AssertionError("M95 boundary graph is missing")
        registered_edges = tuple(
            tuple(str(type_id) for type_id in edge)
            for edge in registered["edges"]
        )
        if registered_edges != edges:
            raise AssertionError("M95 boundary edges changed")
        exact = graph_cover_number(type_ids, edges)
        if exact != expected_minima[name]:
            raise AssertionError("M95 boundary exact minimum changed")
        if int(registered["exact_cover_number"]) != exact:
            raise AssertionError("M95 boundary registered minimum changed")


def validate_all(
    schema: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Validate the complete nineteen-instance M95 portfolio."""
    data = (
        json.loads(SCHEMA.read_text(encoding="utf-8"))
        if schema is None
        else dict(schema)
    )
    if data.get("schema_version") != "1.0.0":
        raise AssertionError("unsupported M95 schema version")
    if data.get("experiment_id") != "EXP-0066":
        raise AssertionError("M95 experiment ID changed")
    if data.get("claim_ids") != [
        "DEF-051",
        "THM-024",
        "REF-064",
        "EMP-066",
    ]:
        raise AssertionError("M95 claim registry changed")
    expected_scope = {
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
    }
    if data.get("scope") != expected_scope:
        raise AssertionError("M95 scope boundary changed")
    if data.get("summary_sha256") != canonical_hash(data):
        raise AssertionError("M95 canonical summary hash changed")
    expected_sources = [
        {"source_id": source_id, **SOURCE_ANCHORS[source_id]}
        for source_id in ("M92", "M93")
    ]
    if data.get("sources") != expected_sources:
        raise AssertionError("M95 source anchors changed")
    source_data: dict[str, Mapping[str, Any]] = {}
    for source_id, path in SOURCE_PATHS.items():
        if file_sha256(path) != SOURCE_ANCHORS[source_id]["file_sha256"]:
            raise AssertionError(f"M95 {source_id} source file hash changed")
        source = json.loads(path.read_text(encoding="utf-8"))
        if source.get("summary_sha256") != SOURCE_ANCHORS[source_id][
            "summary_sha256"
        ]:
            raise AssertionError(f"M95 {source_id} summary hash changed")
        if canonical_hash(source) != SOURCE_ANCHORS[source_id][
            "summary_sha256"
        ]:
            raise AssertionError(f"M95 {source_id} content changed")
        source_data[source_id] = source
    instances = data.get("instances")
    if not isinstance(instances, list) or len(instances) != 19:
        raise AssertionError("M95 instance count changed")
    source_instances = {
        source_id: {
            int(instance["input_length"]): instance
            for instance in source["instances"]
        }
        for source_id, source in source_data.items()
    }
    observed_order = [
        (str(instance["source_id"]), int(instance["input_length"]))
        for instance in instances
    ]
    expected_order = [
        (source_id, input_length)
        for source_id in ("M92", "M93")
        for input_length in SOURCE_LENGTHS[source_id]
    ]
    if observed_order != expected_order:
        raise AssertionError("M95 instance order changed")
    reports = [
        validate_instance(
            instance,
            source_id,
            source_instances[source_id][input_length],
        )
        for instance, (source_id, input_length) in zip(
            instances,
            expected_order,
            strict=True,
        )
    ]
    fields = (
        "tracked_point_count",
        "pair_count",
        "type_count",
        "coverer_incidence_count",
        "degree_one_column_count",
        "degree_two_column_count",
        "minimum_coordinate_count",
        "abstract_certificate_payload_bits",
        "certificate_verifier_bit_tests",
        "incumbent_payload_bits",
        "payload_bits_saved",
        "incumbent_verifier_bit_tests",
        "verifier_bit_test_delta",
    )
    counts = Counter(str(report["template_kind"]) for report in reports)
    totals = {
        "instance_count": len(reports),
        **{
            field: sum(int(report[field]) for report in reports)
            for field in fields
        },
        "template_counts": {
            kind: counts[kind] for kind in TEMPLATE_KINDS
        },
    }
    expected_totals = {
        "instance_count": totals.pop("instance_count"),
        **{
            field: totals.pop(field)
            for field in fields[:7]
        },
        "template_counts": totals.pop("template_counts"),
        **totals,
    }
    if data.get("totals") != expected_totals:
        raise AssertionError("M95 totals changed")
    validate_boundary(data["rank_two_boundary_counterexample"])
    return expected_totals


def main() -> int:
    """Run the standalone M95 coverer-graph checker."""
    totals = validate_all()
    print(
        "M95 coverer-graph certificate checker: PASS "
        f"({totals['instance_count']} instances, "
        f"{totals['pair_count']} columns, "
        f"{totals['degree_one_column_count']} loops, "
        f"{totals['degree_two_column_count']} ordinary edges, "
        f"{totals['payload_bits_saved']} payload bits saved)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
