"""Build the M94 complete-graph incidence certificate portfolio."""

from __future__ import annotations

import hashlib
import itertools
import json
import math
from collections.abc import Iterable, Mapping
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "schemas" / "m93-early-repair-certificates-v1.json"
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


def or_masks(masks: Iterable[int]) -> int:
    """OR a finite mask sequence."""
    result = 0
    for mask in masks:
        result |= mask
    return result


def pair_universe(
    buckets: tuple[tuple[int, ...], ...],
) -> tuple[tuple[int, int], ...]:
    """Use the public lexicographic within-bucket pair order."""
    return tuple(
        pair
        for bucket in buckets
        for pair in itertools.combinations(bucket, 2)
    )


def coverer_records(
    type_ids: tuple[str, ...],
    masks: tuple[int, ...],
    pairs: tuple[tuple[int, int], ...],
) -> list[dict[str, Any]]:
    """Reconstruct the complete coverer set of every universe element."""
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


def expected_cost(
    buckets: tuple[tuple[int, ...], ...],
    type_count: int,
    pair_count: int,
    incumbent: Mapping[str, Any],
) -> dict[str, int]:
    """Construct the compact incidence and incumbent cost comparison."""
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


def build_instance(source: Mapping[str, Any]) -> dict[str, Any]:
    """Build one source-bound complete-graph incidence certificate."""
    input_length = int(source["input_length"])
    if input_length not in TARGET_LENGTHS:
        raise AssertionError("unexpected M94 source instance")
    buckets = tuple(
        tuple(int(prime) for prime in bucket)
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
    coverers = coverer_records(type_ids, masks, pairs)
    observed: set[tuple[str, ...]] = {
        tuple(str(type_id) for type_id in record["coverer_type_ids"])
        for record in coverers
    }
    expected = set(itertools.combinations(type_ids, 2))
    if any(len(record["coverer_type_ids"]) != 2 for record in coverers):
        raise AssertionError("a universe element is not covered by two types")
    if observed != expected or len(coverers) != len(expected):
        raise AssertionError("coverage incidence is not a complete graph")
    target = (1 << len(pairs)) - 1
    canonical_upper = type_ids[:-1]
    masks_by_id = dict(zip(type_ids, masks, strict=True))
    if or_masks(masks_by_id[type_id] for type_id in canonical_upper) != target:
        raise AssertionError("canonical complete-graph upper witness failed")
    exact_minimum = len(type_ids) - 1
    if int(source["minimum_coordinate_count"]) != exact_minimum:
        raise AssertionError("M93 minimum is not the clique cover number")
    cost = expected_cost(
        buckets,
        len(type_ids),
        len(pairs),
        source["verification_cost"],
    )
    return {
        "input_length": input_length,
        "source_instance_sha256": canonical_hash(source),
        "collision_buckets": [list(bucket) for bucket in buckets],
        "tracked_point_count": sum(len(bucket) for bucket in buckets),
        "pair_count": len(pairs),
        "type_count": len(type_ids),
        "complete_graph_edge_count": math.comb(len(type_ids), 2),
        "coverage_types": coverage_types,
        "coverer_sets": coverers,
        "canonical_omitted_type_id": type_ids[-1],
        "exact_repair_number": exact_minimum,
        "incumbent_lower_witness_kind": str(
            source["lower_witness"]["kind"]
        ),
        "verification_cost": cost,
    }


def build_summary() -> dict[str, Any]:
    """Build the canonical M94 summary."""
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    by_length = {
        int(instance["input_length"]): instance
        for instance in source["instances"]
    }
    instances = [
        build_instance(by_length[input_length])
        for input_length in TARGET_LENGTHS
    ]
    cost_fields = (
        "abstract_certificate_payload_bits",
        "certificate_verifier_bit_tests",
        "incumbent_payload_bits",
        "payload_bits_saved",
        "incumbent_verifier_bit_tests",
        "verifier_bit_test_delta",
    )
    summary: dict[str, Any] = {
        "schema_version": "1.0.0",
        "experiment_id": "EXP-0065",
        "claim_ids": ["DEF-050", "THM-023", "REF-063", "EMP-065"],
        "source": {
            "path": "schemas/m93-early-repair-certificates-v1.json",
            "file_sha256": file_sha256(SOURCE),
            "summary_sha256": str(source["summary_sha256"]),
        },
        "instances": instances,
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
                sum(
                    len(record["coverer_type_ids"])
                    for record in instance["coverer_sets"]
                )
                for instance in instances
            ),
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
            "finite_input_lengths": list(TARGET_LENGTHS),
            "complete_type_dependency": "EMP-064",
            "not_claimed": [
                "number-theoretic reconstruction beyond the frozen M93 types",
                "a factor-promise recognizer",
                "an asymptotic repair theorem",
                "a result for another selector family",
                "general classical polynomial-time factoring",
            ],
        },
    }
    summary["summary_sha256"] = canonical_hash(summary)
    return summary


def main() -> int:
    """Print the deterministic audit summary."""
    summary = build_summary()
    totals = summary["totals"]
    print(
        "M94 clique-incidence audit: PASS "
        f"({totals['instance_count']} instances, "
        f"{totals['pair_count']} pairs, "
        f"{totals['coverer_incidence_count']} incidences, "
        f"{totals['payload_bits_saved']} payload bits saved)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
