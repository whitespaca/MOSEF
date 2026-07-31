"""Build the M98 odd-cycle-transversal exact-cover profile."""

from __future__ import annotations

import json
import sys
from collections.abc import Mapping
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.run_m97_bipartite_cover_profile import (
    TYPE_IDS,
    bipartition,
    canonical_edge,
    canonical_hash,
    canonical_slots,
    complete_normal_form,
    construct_maximum_matching,
    construct_minimum_cover,
    file_sha256,
    is_m95_template,
    maximum_matching,
    minimum_vertex_cover,
    seed_slot_maps,
)

SOURCE = ROOT / "schemas" / "m95-coverer-graph-profile-v1.json"
M97_CONSTRUCTOR = ROOT / "scripts" / "run_m97_bipartite_cover_profile.py"
SEED_SOURCE_ID = "M92"
SEED_INPUT_LENGTH = 27

CaseSpec = tuple[
    str,
    str,
    int,
    tuple[tuple[str, str], ...],
    tuple[str, ...],
    tuple[str, ...] | None,
]


def case_specs() -> tuple[CaseSpec, ...]:
    """Return valid OCT cases plus one deliberate rejection."""
    return (
        (
            "O1-triangle-pendant",
            "triangle_with_pendant",
            4,
            (
                ("T0", "T1"),
                ("T1", "T2"),
                ("T0", "T2"),
                ("T2", "T3"),
            ),
            ("T0",),
            None,
        ),
        (
            "O2-C5",
            "cycle_5",
            5,
            (
                ("T0", "T1"),
                ("T1", "T2"),
                ("T2", "T3"),
                ("T3", "T4"),
                ("T0", "T4"),
            ),
            ("T0",),
            None,
        ),
        (
            "O3-bowtie",
            "two_triangles_shared_vertex",
            5,
            (
                ("T0", "T1"),
                ("T1", "T2"),
                ("T0", "T2"),
                ("T0", "T3"),
                ("T3", "T4"),
                ("T0", "T4"),
            ),
            ("T0",),
            None,
        ),
        (
            "O4-house",
            "cycle_4_with_roof",
            5,
            (
                ("T0", "T1"),
                ("T1", "T2"),
                ("T2", "T3"),
                ("T0", "T3"),
                ("T1", "T4"),
                ("T2", "T4"),
            ),
            ("T4",),
            None,
        ),
        (
            "O5-K4",
            "complete_graph_4",
            4,
            (
                ("T0", "T1"),
                ("T0", "T2"),
                ("T0", "T3"),
                ("T1", "T2"),
                ("T1", "T3"),
                ("T2", "T3"),
            ),
            ("T0", "T1"),
            None,
        ),
        (
            "O6-K5-e",
            "complete_graph_5_minus_e01",
            5,
            (
                ("T0", "T2"),
                ("T0", "T3"),
                ("T0", "T4"),
                ("T1", "T2"),
                ("T1", "T3"),
                ("T1", "T4"),
                ("T2", "T3"),
                ("T2", "T4"),
                ("T3", "T4"),
            ),
            ("T2", "T3"),
            None,
        ),
        (
            "O7-K5-valid",
            "complete_graph_5",
            5,
            tuple(
                (TYPE_IDS[left], TYPE_IDS[right])
                for left in range(5)
                for right in range(left + 1, 5)
            ),
            ("T0", "T1", "T2"),
            None,
        ),
        (
            "R1-K5-invalid",
            "complete_graph_5",
            5,
            tuple(
                (TYPE_IDS[left], TYPE_IDS[right])
                for left in range(5)
                for right in range(left + 1, 5)
            ),
            ("T0", "T1"),
            ("T2", "T3", "T4", "T2"),
        ),
    )


def validate_odd_cycle(
    cycle: tuple[str, ...],
    edge_pairs: set[tuple[str, str]],
) -> None:
    """Validate a closed simple odd-cycle rejection certificate."""
    if (
        len(cycle) < 4
        or cycle[0] != cycle[-1]
        or (len(cycle) - 1) % 2 != 1
        or len(set(cycle[:-1])) != len(cycle) - 1
    ):
        raise AssertionError("invalid M98 odd cycle")
    for index in range(len(cycle) - 1):
        if canonical_edge(cycle[index], cycle[index + 1]) not in edge_pairs:
            raise AssertionError("M98 odd cycle uses a missing edge")


def covers_all(
    cover: tuple[str, ...],
    edges: tuple[tuple[int, tuple[str, str]], ...],
) -> bool:
    """Return whether one type set covers every edge occurrence."""
    chosen = set(cover)
    return all(
        left in chosen or right in chosen for _, (left, right) in edges
    )


def solve_with_transversal(
    vertices: tuple[str, ...],
    edges: tuple[tuple[int, tuple[str, str]], ...],
    transversal: tuple[str, ...],
) -> dict[str, Any]:
    """Enumerate transversal choices and solve each bipartite remainder."""
    if len(transversal) != len(set(transversal)) or not set(
        transversal
    ) <= set(vertices):
        raise AssertionError("invalid M98 transversal registry")
    transversal_set = set(transversal)
    base_vertices = tuple(
        vertex for vertex in vertices if vertex not in transversal_set
    )
    base_edges = tuple(
        (column_index, edge)
        for column_index, edge in edges
        if edge[0] in base_vertices and edge[1] in base_vertices
    )
    partition = bipartition(base_vertices, base_edges)
    if partition is None:
        return {
            "status": "rejected_invalid_transversal",
            "base_type_ids": list(base_vertices),
            "base_bipartition": None,
            "branch_count": 0,
            "feasible_branch_count": 0,
            "branches": [],
            "minimum_cover_type_ids": None,
            "minimum_cover_number": None,
        }
    base_left, base_right = partition
    branches: list[dict[str, Any]] = []
    best_cover: tuple[str, ...] | None = None
    for mask in range(1 << len(transversal)):
        selected = tuple(
            vertex
            for index, vertex in enumerate(transversal)
            if mask & (1 << index)
        )
        unselected = tuple(
            vertex for vertex in transversal if vertex not in selected
        )
        unselected_set = set(unselected)
        blocking_edges = tuple(
            column_index
            for column_index, (left, right) in edges
            if left in unselected_set and right in unselected_set
        )
        if blocking_edges:
            branches.append(
                {
                    "branch_mask": mask,
                    "selected_transversal_type_ids": list(selected),
                    "unselected_transversal_type_ids": list(unselected),
                    "status": "infeasible_internal_edge",
                    "blocking_column_indices": list(blocking_edges),
                    "forced_base_type_ids": None,
                    "remaining_base_type_ids": None,
                    "remaining_edge_column_indices": None,
                    "bipartite_matching_column_indices": None,
                    "bipartite_cover_type_ids": None,
                    "candidate_cover_type_ids": None,
                    "candidate_cover_number": None,
                }
            )
            continue
        forced = tuple(
            sorted(
                {
                    endpoint
                    for _, edge in edges
                    for endpoint in edge
                    if endpoint in base_vertices
                    and any(
                        other in unselected_set
                        for other in edge
                        if other != endpoint
                    )
                }
            )
        )
        forced_set = set(forced)
        remaining_vertices = tuple(
            vertex for vertex in base_vertices if vertex not in forced_set
        )
        remaining_edges = tuple(
            (column_index, edge)
            for column_index, edge in base_edges
            if edge[0] in remaining_vertices and edge[1] in remaining_vertices
        )
        remaining_left = tuple(
            vertex for vertex in base_left if vertex in remaining_vertices
        )
        remaining_right = tuple(
            vertex for vertex in base_right if vertex in remaining_vertices
        )
        matching, _ = construct_maximum_matching(
            remaining_left,
            remaining_edges,
        )
        bipartite_cover = construct_minimum_cover(
            remaining_left,
            remaining_right,
            remaining_edges,
            matching,
        )
        candidate = tuple(sorted(set(selected) | forced_set | set(bipartite_cover)))
        if not covers_all(candidate, edges):
            raise AssertionError("M98 branch candidate missed an edge")
        if best_cover is None or (len(candidate), candidate) < (
            len(best_cover),
            best_cover,
        ):
            best_cover = candidate
        branches.append(
            {
                "branch_mask": mask,
                "selected_transversal_type_ids": list(selected),
                "unselected_transversal_type_ids": list(unselected),
                "status": "feasible_exact",
                "blocking_column_indices": [],
                "forced_base_type_ids": list(forced),
                "remaining_base_type_ids": list(remaining_vertices),
                "remaining_edge_column_indices": [
                    column_index for column_index, _ in remaining_edges
                ],
                "bipartite_matching_column_indices": list(matching),
                "bipartite_cover_type_ids": list(bipartite_cover),
                "candidate_cover_type_ids": list(candidate),
                "candidate_cover_number": len(candidate),
            }
        )
    if best_cover is None:
        raise AssertionError("M98 valid transversal has no feasible branch")
    return {
        "status": "constructed_exact",
        "base_type_ids": list(base_vertices),
        "base_bipartition": {
            "left_type_ids": list(base_left),
            "right_type_ids": list(base_right),
        },
        "branch_count": len(branches),
        "feasible_branch_count": sum(
            branch["status"] == "feasible_exact" for branch in branches
        ),
        "branches": branches,
        "minimum_cover_type_ids": list(best_cover),
        "minimum_cover_number": len(best_cover),
    }


def build_case(
    seed_slots: tuple[tuple[str, ...], ...],
    loop_indices: Mapping[str, int],
    edge_indices: Mapping[tuple[str, str], int],
    spec: CaseSpec,
) -> dict[str, Any]:
    """Build one target graph and its transversal-branch ledger."""
    (
        case_id,
        graph_kind,
        unlooped_count,
        raw_edges,
        transversal,
        rejection_cycle,
    ) = spec
    unlooped = TYPE_IDS[:unlooped_count]
    forced = TYPE_IDS[unlooped_count:]
    target_edges = {canonical_edge(*edge) for edge in raw_edges}
    deleted_loops = tuple(loop_indices[type_id] for type_id in unlooped)
    deleted_edges = tuple(
        column_index
        for edge, column_index in edge_indices.items()
        if edge[0] in unlooped
        and edge[1] in unlooped
        and edge not in target_edges
    )
    deleted = set(deleted_loops + deleted_edges)
    retained = tuple(
        slot
        for column_index, slot in enumerate(seed_slots)
        if column_index not in deleted
    )
    if not complete_normal_form(retained):
        raise AssertionError("M98 target left complete normal form")
    residual_edges = tuple(
        (column_index, canonical_edge(slot[0], slot[1]))
        for column_index, slot in enumerate(seed_slots)
        if column_index not in deleted
        and len(slot) == 2
        and slot[0] in unlooped
        and slot[1] in unlooped
    )
    if {edge for _, edge in residual_edges} != target_edges:
        raise AssertionError("M98 target edge reconstruction failed")
    if rejection_cycle is not None:
        validate_odd_cycle(rejection_cycle, target_edges)
    constructor = solve_with_transversal(
        unlooped,
        residual_edges,
        transversal,
    )
    cover = minimum_vertex_cover(unlooped, residual_edges)
    matching = maximum_matching(residual_edges)
    rejected = rejection_cycle is not None
    if rejected != (constructor["status"] == "rejected_invalid_transversal"):
        raise AssertionError("M98 rejection registry changed")
    if not rejected and int(constructor["minimum_cover_number"]) != len(cover):
        raise AssertionError("M98 constructor failed exact audit")
    size_bits = max(1, len(TYPE_IDS).bit_length())
    type_bits = max(1, (len(TYPE_IDS) - 1).bit_length())
    return {
        "case_id": case_id,
        "residual_graph_kind": graph_kind,
        "unlooped_type_ids": list(unlooped),
        "forced_type_ids": list(forced),
        "target_edge_pairs": [list(edge) for edge in sorted(target_edges)],
        "transversal_type_ids": list(transversal),
        "transversal_size": len(transversal),
        "transversal_payload_bits": size_bits + len(transversal) * type_bits,
        "rejection_odd_cycle_type_ids": (
            list(rejection_cycle) if rejection_cycle is not None else None
        ),
        "deleted_loop_column_indices": list(deleted_loops),
        "deleted_edge_column_indices": sorted(deleted_edges),
        "retained_column_count": len(retained),
        "complete_normal_form": True,
        "m95_template": is_m95_template(retained),
        "residual_edges": [
            {"column_index": column_index, "endpoints": list(edge)}
            for column_index, edge in residual_edges
        ],
        "constructor": constructor,
        "exact_audit": {
            "minimum_cover_type_ids": list(cover),
            "maximum_matching_column_indices": list(matching),
            "residual_vertex_cover_number": len(cover),
            "residual_matching_number": len(matching),
            "matching_gap": len(cover) - len(matching),
            "exact_repair_number": len(forced) + len(cover),
            "output_cover_payload_bits": size_bits + len(cover) * type_bits,
        },
    }


def build_summary() -> dict[str, Any]:
    """Build the canonical M98 transversal profile."""
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    seed = next(
        instance
        for instance in source["instances"]
        if instance["source_id"] == SEED_SOURCE_ID
        and int(instance["input_length"]) == SEED_INPUT_LENGTH
    )
    slots = canonical_slots(seed)
    loop_indices, edge_indices = seed_slot_maps(slots)
    cases = [
        build_case(slots, loop_indices, edge_indices, spec)
        for spec in case_specs()
    ]
    valid = [
        record
        for record in cases
        if record["constructor"]["status"] == "constructed_exact"
    ]
    rejected = [
        record
        for record in cases
        if record["constructor"]["status"] == "rejected_invalid_transversal"
    ]
    summary: dict[str, Any] = {
        "schema_version": "1.0.0",
        "experiment_id": "EXP-0069",
        "claim_ids": ["DEF-054", "THM-027", "REF-067", "EMP-069"],
        "source": {
            "path": str(SOURCE.relative_to(ROOT)).replace("\\", "/"),
            "file_sha256": file_sha256(SOURCE),
            "summary_sha256": str(source["summary_sha256"]),
            "seed_source_id": SEED_SOURCE_ID,
            "seed_input_length": SEED_INPUT_LENGTH,
            "seed_instance_sha256": str(seed["source_instance_sha256"]),
            "m97_constructor_path": str(
                M97_CONSTRUCTOR.relative_to(ROOT)
            ).replace("\\", "/"),
            "m97_constructor_sha256": file_sha256(M97_CONSTRUCTOR),
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
        "case_grammar": {
            "operation": (
                "delete residual-prefix loops and non-target residual edges, "
                "then supply the registered transversal"
            ),
            "registered_cases": [
                {
                    "case_id": spec[0],
                    "residual_graph_kind": spec[1],
                    "unlooped_count": spec[2],
                    "target_edge_pairs": [
                        list(canonical_edge(*edge)) for edge in spec[3]
                    ],
                    "transversal_type_ids": list(spec[4]),
                    "rejection_odd_cycle_type_ids": (
                        list(spec[5]) if spec[5] is not None else None
                    ),
                }
                for spec in case_specs()
            ],
        },
        "cases": cases,
        "totals": {
            "case_count": len(cases),
            "valid_transversal_count": len(valid),
            "rejected_transversal_count": len(rejected),
            "transversal_size_sum": sum(
                int(record["transversal_size"]) for record in cases
            ),
            "branch_count": sum(
                int(record["constructor"]["branch_count"])
                for record in valid
            ),
            "feasible_branch_count": sum(
                int(record["constructor"]["feasible_branch_count"])
                for record in valid
            ),
            "residual_vertex_cover_number_sum": sum(
                int(record["exact_audit"]["residual_vertex_cover_number"])
                for record in cases
            ),
            "residual_matching_number_sum": sum(
                int(record["exact_audit"]["residual_matching_number"])
                for record in cases
            ),
            "exact_repair_number_sum": sum(
                int(record["exact_audit"]["exact_repair_number"])
                for record in cases
            ),
            "transversal_payload_bits": sum(
                int(record["transversal_payload_bits"]) for record in cases
            ),
            "valid_output_cover_payload_bits": sum(
                int(record["exact_audit"]["output_cover_payload_bits"])
                for record in valid
            ),
            "maximum_matching_gap": max(
                int(record["exact_audit"]["matching_gap"])
                for record in cases
            ),
            "maximum_transversal_size": max(
                int(record["transversal_size"]) for record in cases
            ),
        },
        "scope": {
            "classification": "EMPIRICAL",
            "source_dependency": "EMP-066 and THM-026",
            "synthetic_target_graphs": True,
            "not_claimed": [
                "a factor-promise recognizer",
                "an odd-cycle-transversal discovery algorithm",
                "a polynomial algorithm for unrestricted transversal size",
                "a polynomial constructor for arbitrary vertex cover",
                "factor-independent construction of complete type lists",
                "an asymptotic selector theorem",
                "general classical polynomial-time factoring",
            ],
        },
    }
    summary["summary_sha256"] = canonical_hash(summary)
    return summary


def main() -> int:
    """Print the deterministic M98 profile summary."""
    totals = build_summary()["totals"]
    print(
        "M98 OCT-cover profile: PASS "
        f"({totals['case_count']} cases, "
        f"{totals['valid_transversal_count']} exact constructors, "
        f"{totals['rejected_transversal_count']} rejection, "
        f"{totals['branch_count']} explicit branches)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
