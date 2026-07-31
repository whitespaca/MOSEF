"""Independently validate the M98 odd-cycle-transversal covers."""

from __future__ import annotations

import hashlib
import itertools
import json
from collections.abc import Iterable, Mapping
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas" / "m98-oct-cover-v1.json"
SOURCE = ROOT / "schemas" / "m95-coverer-graph-profile-v1.json"
M97_CONSTRUCTOR = ROOT / "scripts" / "run_m97_bipartite_cover_profile.py"
TYPE_IDS = ("T0", "T1", "T2", "T3", "T4")
SOURCE_ANCHOR = {
    "path": "schemas/m95-coverer-graph-profile-v1.json",
    "file_sha256": (
        "e5e069554a3249e04084b505b590ff197ff26e75e4fd2467115caeeca1d08e03"
    ),
    "summary_sha256": (
        "0b99798516bda32cc78e8fd7474fbaddce9cd024a021d81c08fca8514c64154a"
    ),
    "seed_source_id": "M92",
    "seed_input_length": 27,
    "seed_instance_sha256": (
        "55830ccb41686b432fc7710380652937209fd24885c2ad4de81607784d0a6348"
    ),
    "m97_constructor_path": (
        "scripts/run_m97_bipartite_cover_profile.py"
    ),
    "m97_constructor_sha256": (
        "d811f6cf39c0ae00b28e17bb93d322b07a2fac22da236a66d31e4f75fc1dfa39"
    ),
}
EXPECTED_SCOPE = {
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
}

CaseSpec = tuple[
    str,
    str,
    int,
    tuple[tuple[str, str], ...],
    tuple[str, ...],
    tuple[str, ...] | None,
]


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


def canonical_edge(left: str, right: str) -> tuple[str, str]:
    """Return one ordered undirected pair."""
    return (left, right) if left <= right else (right, left)


def case_specs() -> tuple[CaseSpec, ...]:
    """Return the independently frozen M98 case registry."""
    complete_five = tuple(itertools.combinations(TYPE_IDS, 2))
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
            tuple(itertools.combinations(TYPE_IDS[:4], 2)),
            ("T0", "T1"),
            None,
        ),
        (
            "O6-K5-e",
            "complete_graph_5_minus_e01",
            5,
            tuple(edge for edge in complete_five if edge != ("T0", "T1")),
            ("T2", "T3"),
            None,
        ),
        (
            "O7-K5-valid",
            "complete_graph_5",
            5,
            complete_five,
            ("T0", "T1", "T2"),
            None,
        ),
        (
            "R1-K5-invalid",
            "complete_graph_5",
            5,
            complete_five,
            ("T0", "T1"),
            ("T2", "T3", "T4", "T2"),
        ),
    )


def template_slots(kind: str) -> tuple[tuple[str, ...], ...]:
    """Return one complete five-type M95 template."""
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
    """Recognize the three duplicate-sensitive M95 templates."""
    observed = sorted(slots)
    return any(
        observed == sorted(template_slots(kind))
        for kind in ("loop_only", "looped_clique", "loopless_clique")
    )


def complete_normal_form(slots: tuple[tuple[str, ...], ...]) -> bool:
    """Check nonempty, pairwise-distinct induced signatures."""
    signatures = tuple(
        frozenset(
            index
            for index, slot in enumerate(slots)
            if type_id in slot
        )
        for type_id in TYPE_IDS
    )
    return all(signatures) and len(set(signatures)) == len(signatures)


def seed_from_source() -> tuple[Mapping[str, Any], tuple[tuple[str, ...], ...]]:
    """Bind and reconstruct the frozen M95 seed."""
    if file_sha256(SOURCE) != SOURCE_ANCHOR["file_sha256"]:
        raise AssertionError("M98 source file hash changed")
    if file_sha256(M97_CONSTRUCTOR) != SOURCE_ANCHOR[
        "m97_constructor_sha256"
    ]:
        raise AssertionError("M98 M97 constructor hash changed")
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    if source.get("summary_sha256") != SOURCE_ANCHOR["summary_sha256"]:
        raise AssertionError("M98 source summary hash changed")
    if canonical_hash(source) != SOURCE_ANCHOR["summary_sha256"]:
        raise AssertionError("M98 source content changed")
    seed = next(
        instance
        for instance in source["instances"]
        if instance["source_id"] == SOURCE_ANCHOR["seed_source_id"]
        and int(instance["input_length"])
        == SOURCE_ANCHOR["seed_input_length"]
    )
    if seed["source_instance_sha256"] != SOURCE_ANCHOR[
        "seed_instance_sha256"
    ]:
        raise AssertionError("M98 seed instance changed")
    slots = tuple(
        tuple(str(type_id) for type_id in record["coverer_type_ids"])
        for record in seed["coverer_sets"]
    )
    if len(slots) != 15 or sorted(slots) != sorted(
        template_slots("looped_clique")
    ):
        raise AssertionError("M98 seed is not looped K5")
    return seed, slots


def slot_maps(
    slots: tuple[tuple[str, ...], ...],
) -> tuple[dict[str, int], dict[tuple[str, str], int]]:
    """Index singleton and ordinary seed slots."""
    loops: dict[str, int] = {}
    edges: dict[tuple[str, str], int] = {}
    for index, slot in enumerate(slots):
        if len(slot) == 1:
            loops[slot[0]] = index
        elif len(slot) == 2:
            edges[canonical_edge(slot[0], slot[1])] = index
        else:
            raise AssertionError("M98 seed rank changed")
    if set(loops) != set(TYPE_IDS) or set(edges) != set(
        itertools.combinations(TYPE_IDS, 2)
    ):
        raise AssertionError("M98 seed slot registry changed")
    return loops, edges


def minimum_vertex_cover(
    vertices: tuple[str, ...],
    edges: tuple[tuple[int, tuple[str, str]], ...],
) -> tuple[str, ...]:
    """Enumerate the first exact cover."""
    for size in range(len(vertices) + 1):
        for selected in itertools.combinations(vertices, size):
            chosen = set(selected)
            if all(left in chosen or right in chosen for _, (left, right) in edges):
                return selected
    raise AssertionError("residual graph has no cover")


def maximum_matching(
    edges: tuple[tuple[int, tuple[str, str]], ...],
) -> tuple[int, ...]:
    """Enumerate the first exact matching."""
    for size in range(len(edges), -1, -1):
        for selected in itertools.combinations(edges, size):
            endpoints = [
                endpoint
                for _, edge in selected
                for endpoint in edge
            ]
            if len(endpoints) == len(set(endpoints)):
                return tuple(index for index, _ in selected)
    raise AssertionError("residual graph has no matching")


def first_bipartition(
    vertices: tuple[str, ...],
    edges: tuple[tuple[int, tuple[str, str]], ...],
) -> tuple[tuple[str, ...], tuple[str, ...]] | None:
    """Brute-force one lexicographically first valid bipartition."""
    if not vertices:
        return (), ()
    for mask in range(1 << len(vertices)):
        left = {
            vertex
            for index, vertex in enumerate(vertices)
            if mask & (1 << index)
        }
        if all(
            (first in left) != (second in left)
            for _, (first, second) in edges
        ):
            return (
                tuple(vertex for vertex in vertices if vertex in left),
                tuple(vertex for vertex in vertices if vertex not in left),
            )
    return None


def validate_cover(
    cover: list[str],
    vertices: tuple[str, ...],
    edges: tuple[tuple[int, tuple[str, str]], ...],
) -> None:
    """Validate one explicit cover."""
    if len(cover) != len(set(cover)) or not set(cover) <= set(vertices):
        raise AssertionError("M98 cover registry changed")
    chosen = set(cover)
    if any(
        left not in chosen and right not in chosen
        for _, (left, right) in edges
    ):
        raise AssertionError("M98 cover missed an edge")


def validate_matching(
    matching: list[int],
    edges: tuple[tuple[int, tuple[str, str]], ...],
) -> None:
    """Validate one matching by edge occurrence."""
    edge_map = dict(edges)
    if len(matching) != len(set(matching)) or any(
        index not in edge_map for index in matching
    ):
        raise AssertionError("M98 matching registry changed")
    endpoints = [
        endpoint
        for index in matching
        for endpoint in edge_map[index]
    ]
    if len(endpoints) != len(set(endpoints)):
        raise AssertionError("M98 matching endpoints overlap")


def validate_odd_cycle(
    cycle: list[str],
    edge_pairs: set[tuple[str, str]],
) -> None:
    """Validate one closed simple odd cycle."""
    if (
        len(cycle) < 4
        or cycle[0] != cycle[-1]
        or (len(cycle) - 1) % 2 != 1
        or len(set(cycle[:-1])) != len(cycle) - 1
    ):
        raise AssertionError("M98 rejection odd cycle framing changed")
    if any(
        canonical_edge(left, right) not in edge_pairs
        for left, right in itertools.pairwise(cycle)
    ):
        raise AssertionError("M98 rejection odd cycle edge changed")


def expected_case_grammar() -> dict[str, Any]:
    """Return the exact public case registry."""
    return {
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
    }


def validate_branches(
    constructor: Mapping[str, Any],
    vertices: tuple[str, ...],
    edges: tuple[tuple[int, tuple[str, str]], ...],
    transversal: tuple[str, ...],
) -> tuple[int, int, tuple[str, ...]]:
    """Independently validate every transversal branch."""
    transversal_set = set(transversal)
    base_vertices = tuple(
        vertex for vertex in vertices if vertex not in transversal_set
    )
    base_edges = tuple(
        (index, edge)
        for index, edge in edges
        if edge[0] in base_vertices and edge[1] in base_vertices
    )
    partition = first_bipartition(base_vertices, base_edges)
    if partition is None:
        raise AssertionError("M98 valid branch base is not bipartite")
    supplied_partition = constructor.get("base_bipartition")
    if not isinstance(supplied_partition, dict):
        raise AssertionError("M98 base bipartition framing changed")
    supplied_left = supplied_partition.get("left_type_ids")
    supplied_right = supplied_partition.get("right_type_ids")
    if not isinstance(supplied_left, list) or not isinstance(
        supplied_right,
        list,
    ):
        raise AssertionError("M98 base bipartition lists changed")
    if (
        set(supplied_left) | set(supplied_right) != set(base_vertices)
        or set(supplied_left) & set(supplied_right)
        or any(
            (left in supplied_left) == (right in supplied_left)
            for _, (left, right) in base_edges
        )
    ):
        raise AssertionError("M98 base bipartition crossing failed")
    if constructor.get("base_type_ids") != list(base_vertices):
        raise AssertionError("M98 base type registry changed")
    branches = constructor.get("branches")
    if not isinstance(branches, list) or len(branches) != 1 << len(
        transversal
    ):
        raise AssertionError("M98 branch count changed")
    best_cover: tuple[str, ...] | None = None
    feasible_count = 0
    for mask, branch in enumerate(branches):
        selected = tuple(
            vertex
            for index, vertex in enumerate(transversal)
            if mask & (1 << index)
        )
        unselected = tuple(
            vertex for vertex in transversal if vertex not in selected
        )
        if branch.get("branch_mask") != mask:
            raise AssertionError("M98 branch mask changed")
        if branch.get("selected_transversal_type_ids") != list(selected):
            raise AssertionError("M98 selected transversal changed")
        if branch.get("unselected_transversal_type_ids") != list(unselected):
            raise AssertionError("M98 unselected transversal changed")
        unselected_set = set(unselected)
        blocking = [
            index
            for index, (left, right) in edges
            if left in unselected_set and right in unselected_set
        ]
        if blocking:
            expected = {
                "branch_mask": mask,
                "selected_transversal_type_ids": list(selected),
                "unselected_transversal_type_ids": list(unselected),
                "status": "infeasible_internal_edge",
                "blocking_column_indices": blocking,
                "forced_base_type_ids": None,
                "remaining_base_type_ids": None,
                "remaining_edge_column_indices": None,
                "bipartite_matching_column_indices": None,
                "bipartite_cover_type_ids": None,
                "candidate_cover_type_ids": None,
                "candidate_cover_number": None,
            }
            if branch != expected:
                raise AssertionError("M98 infeasible branch changed")
            continue
        feasible_count += 1
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
            (index, edge)
            for index, edge in base_edges
            if edge[0] in remaining_vertices and edge[1] in remaining_vertices
        )
        matching = branch.get("bipartite_matching_column_indices")
        cover = branch.get("bipartite_cover_type_ids")
        candidate = branch.get("candidate_cover_type_ids")
        if (
            not isinstance(matching, list)
            or not isinstance(cover, list)
            or not isinstance(candidate, list)
        ):
            raise AssertionError("M98 feasible branch framing changed")
        validate_matching(matching, remaining_edges)
        validate_cover(cover, remaining_vertices, remaining_edges)
        exact_remaining_cover = minimum_vertex_cover(
            remaining_vertices,
            remaining_edges,
        )
        exact_remaining_matching = maximum_matching(remaining_edges)
        if (
            len(cover) != len(exact_remaining_cover)
            or len(matching) != len(exact_remaining_matching)
            or len(cover) != len(matching)
        ):
            raise AssertionError("M98 bipartite branch exactness changed")
        expected_candidate = tuple(
            sorted(set(selected) | forced_set | set(cover))
        )
        validate_cover(list(expected_candidate), vertices, edges)
        expected_scalars = {
            "status": "feasible_exact",
            "blocking_column_indices": [],
            "forced_base_type_ids": list(forced),
            "remaining_base_type_ids": list(remaining_vertices),
            "remaining_edge_column_indices": [
                index for index, _ in remaining_edges
            ],
            "candidate_cover_type_ids": list(expected_candidate),
            "candidate_cover_number": len(expected_candidate),
        }
        for field, expected_value in expected_scalars.items():
            if branch.get(field) != expected_value:
                raise AssertionError(f"M98 branch {field} changed")
        candidate_tuple = tuple(candidate)
        if best_cover is None or (len(candidate_tuple), candidate_tuple) < (
            len(best_cover),
            best_cover,
        ):
            best_cover = candidate_tuple
    if best_cover is None:
        raise AssertionError("M98 no feasible branch remained")
    if constructor.get("branch_count") != len(branches):
        raise AssertionError("M98 constructor branch count changed")
    if constructor.get("feasible_branch_count") != feasible_count:
        raise AssertionError("M98 feasible branch count changed")
    if constructor.get("minimum_cover_type_ids") != list(best_cover):
        raise AssertionError("M98 constructor minimum cover changed")
    if constructor.get("minimum_cover_number") != len(best_cover):
        raise AssertionError("M98 constructor minimum number changed")
    return len(branches), feasible_count, best_cover


def validate_case(
    record: Mapping[str, Any],
    slots: tuple[tuple[str, ...], ...],
    loop_indices: Mapping[str, int],
    edge_indices: Mapping[tuple[str, str], int],
    spec: CaseSpec,
) -> dict[str, int | bool]:
    """Validate one M98 graph, transversal, and exact result."""
    (
        case_id,
        graph_kind,
        unlooped_count,
        raw_edges,
        transversal,
        rejection_cycle,
    ) = spec
    unlooped = TYPE_IDS[:unlooped_count]
    forced_types = TYPE_IDS[unlooped_count:]
    target_edges = {canonical_edge(*edge) for edge in raw_edges}
    deleted_loops = [loop_indices[type_id] for type_id in unlooped]
    deleted_edges = sorted(
        index
        for edge, index in edge_indices.items()
        if edge[0] in unlooped
        and edge[1] in unlooped
        and edge not in target_edges
    )
    deleted = set(deleted_loops + deleted_edges)
    retained = tuple(
        slot
        for index, slot in enumerate(slots)
        if index not in deleted
    )
    residual_edges = tuple(
        (index, canonical_edge(slot[0], slot[1]))
        for index, slot in enumerate(slots)
        if index not in deleted
        and len(slot) == 2
        and slot[0] in unlooped
        and slot[1] in unlooped
    )
    expected_scalars = {
        "case_id": case_id,
        "residual_graph_kind": graph_kind,
        "unlooped_type_ids": list(unlooped),
        "forced_type_ids": list(forced_types),
        "target_edge_pairs": [list(edge) for edge in sorted(target_edges)],
        "transversal_type_ids": list(transversal),
        "transversal_size": len(transversal),
        "transversal_payload_bits": 3 + 3 * len(transversal),
        "rejection_odd_cycle_type_ids": (
            list(rejection_cycle) if rejection_cycle is not None else None
        ),
        "deleted_loop_column_indices": deleted_loops,
        "deleted_edge_column_indices": deleted_edges,
        "retained_column_count": len(retained),
        "complete_normal_form": True,
        "m95_template": is_m95_template(retained),
        "residual_edges": [
            {"column_index": index, "endpoints": list(edge)}
            for index, edge in residual_edges
        ],
    }
    for field, expected in expected_scalars.items():
        if record.get(field) != expected:
            raise AssertionError(f"M98 {field} changed")
    if not complete_normal_form(retained):
        raise AssertionError("M98 complete normal form failed")
    cover = minimum_vertex_cover(unlooped, residual_edges)
    matching = maximum_matching(residual_edges)
    exact_audit = {
        "minimum_cover_type_ids": list(cover),
        "maximum_matching_column_indices": list(matching),
        "residual_vertex_cover_number": len(cover),
        "residual_matching_number": len(matching),
        "matching_gap": len(cover) - len(matching),
        "exact_repair_number": len(forced_types) + len(cover),
        "output_cover_payload_bits": 3 + 3 * len(cover),
    }
    if record.get("exact_audit") != exact_audit:
        raise AssertionError("M98 exact audit changed")
    constructor = record.get("constructor")
    if not isinstance(constructor, dict):
        raise AssertionError("M98 constructor framing changed")
    base_vertices = tuple(
        vertex for vertex in unlooped if vertex not in set(transversal)
    )
    base_edges = tuple(
        (index, edge)
        for index, edge in residual_edges
        if edge[0] in base_vertices and edge[1] in base_vertices
    )
    if rejection_cycle is not None:
        validate_odd_cycle(list(rejection_cycle), target_edges)
        if first_bipartition(base_vertices, base_edges) is not None:
            raise AssertionError("M98 rejected transversal became valid")
        expected_constructor = {
            "status": "rejected_invalid_transversal",
            "base_type_ids": list(base_vertices),
            "base_bipartition": None,
            "branch_count": 0,
            "feasible_branch_count": 0,
            "branches": [],
            "minimum_cover_type_ids": None,
            "minimum_cover_number": None,
        }
        if constructor != expected_constructor:
            raise AssertionError("M98 rejection constructor changed")
        branch_count = 0
        feasible_count = 0
        valid = False
    else:
        if constructor.get("status") != "constructed_exact":
            raise AssertionError("M98 constructor status changed")
        branch_count, feasible_count, best_cover = validate_branches(
            constructor,
            unlooped,
            residual_edges,
            transversal,
        )
        if len(best_cover) != len(cover):
            raise AssertionError("M98 constructor failed exact audit")
        valid = True
    return {
        "valid": valid,
        "transversal_size": len(transversal),
        "branch_count": branch_count,
        "feasible_branch_count": feasible_count,
        "cover_number": len(cover),
        "matching_number": len(matching),
        "repair_number": len(forced_types) + len(cover),
        "transversal_payload_bits": 3 + 3 * len(transversal),
        "output_cover_payload_bits": 3 + 3 * len(cover) if valid else 0,
        "matching_gap": len(cover) - len(matching),
    }


def validate_all(
    schema: Mapping[str, Any] | None = None,
) -> dict[str, int]:
    """Validate the complete M98 portfolio."""
    data = (
        json.loads(SCHEMA.read_text(encoding="utf-8"))
        if schema is None
        else dict(schema)
    )
    if data.get("schema_version") != "1.0.0":
        raise AssertionError("unsupported M98 schema version")
    if data.get("experiment_id") != "EXP-0069":
        raise AssertionError("M98 experiment ID changed")
    if data.get("claim_ids") != [
        "DEF-054",
        "THM-027",
        "REF-067",
        "EMP-069",
    ]:
        raise AssertionError("M98 claim registry changed")
    if data.get("source") != SOURCE_ANCHOR:
        raise AssertionError("M98 source anchor changed")
    if data.get("scope") != EXPECTED_SCOPE:
        raise AssertionError("M98 scope boundary changed")
    if data.get("summary_sha256") != canonical_hash(data):
        raise AssertionError("M98 canonical summary hash changed")
    _, slots = seed_from_source()
    expected_seed = {
        "type_ids": list(TYPE_IDS),
        "column_count": len(slots),
        "template_kind": "looped_clique",
        "slots": [
            {
                "column_index": index,
                "coverer_type_ids": list(slot),
            }
            for index, slot in enumerate(slots)
        ],
    }
    if data.get("seed") != expected_seed:
        raise AssertionError("M98 seed registry changed")
    if data.get("case_grammar") != expected_case_grammar():
        raise AssertionError("M98 case grammar changed")
    records = data.get("cases")
    specs = case_specs()
    if not isinstance(records, list) or len(records) != len(specs):
        raise AssertionError("M98 case count changed")
    loop_indices, edge_indices = slot_maps(slots)
    reports = [
        validate_case(record, slots, loop_indices, edge_indices, spec)
        for record, spec in zip(records, specs, strict=True)
    ]
    valid = [report for report in reports if report["valid"]]
    rejected = [report for report in reports if not report["valid"]]
    totals = {
        "case_count": len(reports),
        "valid_transversal_count": len(valid),
        "rejected_transversal_count": len(rejected),
        "transversal_size_sum": sum(
            int(report["transversal_size"]) for report in reports
        ),
        "branch_count": sum(
            int(report["branch_count"]) for report in valid
        ),
        "feasible_branch_count": sum(
            int(report["feasible_branch_count"]) for report in valid
        ),
        "residual_vertex_cover_number_sum": sum(
            int(report["cover_number"]) for report in reports
        ),
        "residual_matching_number_sum": sum(
            int(report["matching_number"]) for report in reports
        ),
        "exact_repair_number_sum": sum(
            int(report["repair_number"]) for report in reports
        ),
        "transversal_payload_bits": sum(
            int(report["transversal_payload_bits"]) for report in reports
        ),
        "valid_output_cover_payload_bits": sum(
            int(report["output_cover_payload_bits"]) for report in valid
        ),
        "maximum_matching_gap": max(
            int(report["matching_gap"]) for report in reports
        ),
        "maximum_transversal_size": max(
            int(report["transversal_size"]) for report in reports
        ),
    }
    if data.get("totals") != totals:
        raise AssertionError("M98 totals changed")
    return totals


def main() -> int:
    """Run the standalone M98 checker."""
    totals = validate_all()
    print(
        "M98 OCT-cover checker: PASS "
        f"({totals['case_count']} cases, "
        f"{totals['valid_transversal_count']} exact constructors, "
        f"{totals['rejected_transversal_count']} rejection, "
        f"{totals['branch_count']} branches)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
