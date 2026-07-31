"""Build the M96 matching-equality perturbation profile."""

from __future__ import annotations

import hashlib
import itertools
import json
from collections.abc import Iterable, Mapping
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "schemas" / "m95-coverer-graph-profile-v1.json"
TYPE_IDS = ("T0", "T1", "T2", "T3", "T4")
SEED_SOURCE_ID = "M92"
SEED_INPUT_LENGTH = 27


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


def canonical_slots(seed: Mapping[str, Any]) -> tuple[tuple[str, ...], ...]:
    """Extract the ordered coverer slots of the frozen seed."""
    return tuple(
        tuple(str(type_id) for type_id in record["coverer_type_ids"])
        for record in seed["coverer_sets"]
    )


def minimum_vertex_cover(
    vertices: tuple[str, ...],
    edges: tuple[tuple[int, tuple[str, str]], ...],
) -> tuple[str, ...]:
    """Return the lexicographically first exact residual vertex cover."""
    for size in range(len(vertices) + 1):
        for selected in itertools.combinations(vertices, size):
            chosen = set(selected)
            if all(left in chosen or right in chosen for _, (left, right) in edges):
                return selected
    raise AssertionError("finite residual graph has no vertex cover")


def maximum_matching(
    edges: tuple[tuple[int, tuple[str, str]], ...],
) -> tuple[int, ...]:
    """Return the lexicographically first maximum residual matching."""
    for size in range(len(edges), -1, -1):
        for selected in itertools.combinations(edges, size):
            endpoints = [
                endpoint
                for _, edge in selected
                for endpoint in edge
            ]
            if len(endpoints) == len(set(endpoints)):
                return tuple(column_index for column_index, _ in selected)
    raise AssertionError("finite residual graph has no matching")


def template_slots(kind: str) -> tuple[tuple[str, ...], ...]:
    """Return one complete M95 five-type template."""
    loops = tuple((type_id,) for type_id in TYPE_IDS)
    edges = tuple(itertools.combinations(TYPE_IDS, 2))
    if kind == "loop_only":
        return loops
    if kind == "looped_clique":
        return loops + edges
    if kind == "loopless_clique":
        return edges
    raise AssertionError(f"unknown template: {kind}")


def is_m95_template(slots: Iterable[tuple[str, ...]]) -> bool:
    """Return whether a duplicate-sensitive slot list is an M95 template."""
    observed = sorted(slots)
    return any(
        observed == sorted(template_slots(kind))
        for kind in ("loop_only", "looped_clique", "loopless_clique")
    )


def complete_normal_form(slots: tuple[tuple[str, ...], ...]) -> bool:
    """Check that the induced five types are nonempty and pairwise distinct."""
    signatures = tuple(
        frozenset(
            column_index
            for column_index, slot in enumerate(slots)
            if type_id in slot
        )
        for type_id in TYPE_IDS
    )
    return all(signatures) and len(set(signatures)) == len(signatures)


def seed_slot_maps(
    slots: tuple[tuple[str, ...], ...],
) -> tuple[dict[str, int], dict[tuple[str, str], int]]:
    """Index singleton and ordinary seed slots."""
    loops: dict[str, int] = {}
    edges: dict[tuple[str, str], int] = {}
    for column_index, slot in enumerate(slots):
        if len(slot) == 1:
            loops[slot[0]] = column_index
        elif len(slot) == 2:
            edges[(slot[0], slot[1])] = column_index
        else:
            raise AssertionError("seed rank changed")
    if set(loops) != set(TYPE_IDS) or len(edges) != 10:
        raise AssertionError("seed is not the registered looped K5")
    return loops, edges


def perturbation_specs() -> tuple[tuple[int, bool], ...]:
    """Return the bounded non-template perturbation grammar."""
    specs: list[tuple[int, bool]] = []
    for unlooped_count in range(1, 6):
        if unlooped_count == 1:
            specs.append((unlooped_count, False))
        elif unlooped_count == 5:
            specs.append((unlooped_count, True))
        else:
            specs.extend(
                (
                    (unlooped_count, False),
                    (unlooped_count, True),
                )
            )
    return tuple(specs)


def build_perturbation(
    seed_slots: tuple[tuple[str, ...], ...],
    loop_indices: Mapping[str, int],
    edge_indices: Mapping[tuple[str, str], int],
    unlooped_count: int,
    delete_edge: bool,
) -> dict[str, Any]:
    """Build one loop/edge-deletion perturbation and its witnesses."""
    unlooped = TYPE_IDS[:unlooped_count]
    forced = TYPE_IDS[unlooped_count:]
    deleted_loops = tuple(loop_indices[type_id] for type_id in unlooped)
    deleted_edges = (
        (edge_indices[("T0", "T1")],)
        if delete_edge
        else ()
    )
    deleted = set(deleted_loops + deleted_edges)
    retained = tuple(
        slot
        for column_index, slot in enumerate(seed_slots)
        if column_index not in deleted
    )
    if is_m95_template(retained):
        raise AssertionError("M96 grammar admitted an M95 template")
    if not complete_normal_form(retained):
        raise AssertionError("M96 perturbation left complete normal form")
    residual_edges = tuple(
        (column_index, (slot[0], slot[1]))
        for column_index, slot in enumerate(seed_slots)
        if column_index not in deleted
        and len(slot) == 2
        and slot[0] in unlooped
        and slot[1] in unlooped
    )
    cover = minimum_vertex_cover(unlooped, residual_edges)
    matching = maximum_matching(residual_edges)
    tau = len(cover)
    nu = len(matching)
    tight = tau == nu
    type_index_bits = max(1, (len(TYPE_IDS) - 1).bit_length())
    column_index_bits = max(1, (len(seed_slots) - 1).bit_length())
    witness_size_bits = max(1, len(TYPE_IDS).bit_length())
    certificate_bits = (
        witness_size_bits
        + tau * (type_index_bits + column_index_bits)
        if tight
        else None
    )
    verifier_tests = (
        len(residual_edges) + 2 * tau + 1 if tight else None
    )
    suffix = "drop-e01" if delete_edge else "keep-edges"
    return {
        "perturbation_id": f"U{unlooped_count}-{suffix}",
        "unlooped_type_ids": list(unlooped),
        "forced_type_ids": list(forced),
        "deleted_loop_column_indices": list(deleted_loops),
        "deleted_edge_column_indices": list(deleted_edges),
        "retained_column_count": len(retained),
        "complete_normal_form": True,
        "m95_template": False,
        "residual_edges": [
            {
                "column_index": column_index,
                "endpoints": list(edge),
            }
            for column_index, edge in residual_edges
        ],
        "minimum_cover_type_ids": list(cover),
        "maximum_matching_column_indices": list(matching),
        "residual_vertex_cover_number": tau,
        "residual_matching_number": nu,
        "matching_equality": tight,
        "matching_gap": tau - nu,
        "exact_repair_number": len(forced) + tau,
        "matching_lower_bound": len(forced) + nu,
        "matching_certificate": {
            "status": "exact" if tight else "insufficient",
            "type_index_bits": type_index_bits,
            "column_index_bits": column_index_bits,
            "witness_size_bits": witness_size_bits,
            "witness_size": tau if tight else None,
            "payload_bits": certificate_bits,
            "verification_tests": verifier_tests,
        },
    }


def build_summary() -> dict[str, Any]:
    """Build the canonical M96 perturbation summary."""
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    seed = next(
        instance
        for instance in source["instances"]
        if instance["source_id"] == SEED_SOURCE_ID
        and int(instance["input_length"]) == SEED_INPUT_LENGTH
    )
    slots = canonical_slots(seed)
    loop_indices, edge_indices = seed_slot_maps(slots)
    perturbations = [
        build_perturbation(
            slots,
            loop_indices,
            edge_indices,
            unlooped_count,
            delete_edge,
        )
        for unlooped_count, delete_edge in perturbation_specs()
    ]
    tight = [
        record for record in perturbations if record["matching_equality"]
    ]
    gaps = [
        record for record in perturbations if not record["matching_equality"]
    ]
    summary: dict[str, Any] = {
        "schema_version": "1.0.0",
        "experiment_id": "EXP-0067",
        "claim_ids": ["DEF-052", "THM-025", "REF-065", "EMP-067"],
        "source": {
            "path": str(SOURCE.relative_to(ROOT)).replace("\\", "/"),
            "file_sha256": file_sha256(SOURCE),
            "summary_sha256": str(source["summary_sha256"]),
            "seed_source_id": SEED_SOURCE_ID,
            "seed_input_length": SEED_INPUT_LENGTH,
            "seed_instance_sha256": str(seed["source_instance_sha256"]),
        },
        "seed": {
            "type_ids": list(TYPE_IDS),
            "column_count": len(slots),
            "template_kind": str(seed["template_kind"]),
            "slots": [
                {
                    "column_index": column_index,
                    "coverer_type_ids": list(slot),
                }
                for column_index, slot in enumerate(slots)
            ],
        },
        "perturbation_grammar": {
            "operation": (
                "delete the loops on T0,...,T(r-1), then optionally "
                "delete edge {T0,T1}"
            ),
            "registered_parameters": [
                {
                    "unlooped_count": unlooped_count,
                    "delete_edge_t0_t1": delete_edge,
                }
                for unlooped_count, delete_edge in perturbation_specs()
            ],
        },
        "perturbations": perturbations,
        "totals": {
            "perturbation_count": len(perturbations),
            "matching_equality_count": len(tight),
            "matching_gap_count": len(gaps),
            "residual_vertex_cover_number_sum": sum(
                int(record["residual_vertex_cover_number"])
                for record in perturbations
            ),
            "residual_matching_number_sum": sum(
                int(record["residual_matching_number"])
                for record in perturbations
            ),
            "exact_repair_number_sum": sum(
                int(record["exact_repair_number"])
                for record in perturbations
            ),
            "matching_certificate_payload_bits": sum(
                int(record["matching_certificate"]["payload_bits"])
                for record in tight
            ),
            "matching_certificate_verification_tests": sum(
                int(record["matching_certificate"]["verification_tests"])
                for record in tight
            ),
            "maximum_matching_gap": max(
                int(record["matching_gap"]) for record in perturbations
            ),
        },
        "scope": {
            "classification": "EMPIRICAL",
            "source_dependency": "EMP-066",
            "synthetic_perturbations": True,
            "not_claimed": [
                "a factor-promise recognizer",
                "a polynomial algorithm for arbitrary vertex cover",
                "matching equality for every residual coverer graph",
                "an asymptotic selector theorem",
                "general classical polynomial-time factoring",
            ],
        },
    }
    summary["summary_sha256"] = canonical_hash(summary)
    return summary


def main() -> int:
    """Print the deterministic M96 profile summary."""
    totals = build_summary()["totals"]
    print(
        "M96 matching-certificate profile: PASS "
        f"({totals['perturbation_count']} perturbations, "
        f"{totals['matching_equality_count']} equality certificates, "
        f"{totals['matching_gap_count']} matching gaps, "
        f"{totals['matching_certificate_payload_bits']} witness bits)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
