"""Build the M97 constructive bipartite-cover profile."""

from __future__ import annotations

import hashlib
import itertools
import json
from collections import deque
from collections.abc import Iterable, Mapping
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "schemas" / "m95-coverer-graph-profile-v1.json"
TYPE_IDS = ("T0", "T1", "T2", "T3", "T4")
SEED_SOURCE_ID = "M92"
SEED_INPUT_LENGTH = 27

CaseSpec = tuple[
    str,
    str,
    int,
    tuple[tuple[str, str], ...],
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
    """Return one ordered undirected type pair."""
    return (left, right) if left <= right else (right, left)


def case_specs() -> tuple[CaseSpec, ...]:
    """Return the bounded constructive and boundary graph registry."""
    return (
        (
            "B1-P3",
            "path_3",
            3,
            (("T0", "T1"), ("T1", "T2")),
            None,
        ),
        (
            "B2-P4",
            "path_4",
            4,
            (("T0", "T1"), ("T1", "T2"), ("T2", "T3")),
            None,
        ),
        (
            "B3-K1-3",
            "star_1_3",
            4,
            (("T0", "T1"), ("T0", "T2"), ("T0", "T3")),
            None,
        ),
        (
            "B4-C4",
            "cycle_4",
            4,
            (
                ("T0", "T1"),
                ("T1", "T2"),
                ("T2", "T3"),
                ("T0", "T3"),
            ),
            None,
        ),
        (
            "B5-P5",
            "path_5",
            5,
            (
                ("T0", "T1"),
                ("T1", "T2"),
                ("T2", "T3"),
                ("T3", "T4"),
            ),
            None,
        ),
        (
            "B6-K2-3",
            "complete_bipartite_2_3",
            5,
            (
                ("T0", "T2"),
                ("T0", "T3"),
                ("T0", "T4"),
                ("T1", "T2"),
                ("T1", "T3"),
                ("T1", "T4"),
            ),
            None,
        ),
        (
            "N1-triangle-pendant",
            "triangle_with_pendant",
            4,
            (
                ("T0", "T1"),
                ("T1", "T2"),
                ("T0", "T2"),
                ("T2", "T3"),
            ),
            ("T0", "T1", "T2", "T0"),
        ),
        (
            "N2-C5",
            "cycle_5",
            5,
            (
                ("T0", "T1"),
                ("T1", "T2"),
                ("T2", "T3"),
                ("T3", "T4"),
                ("T0", "T4"),
            ),
            ("T0", "T1", "T2", "T3", "T4", "T0"),
        ),
    )


def canonical_slots(seed: Mapping[str, Any]) -> tuple[tuple[str, ...], ...]:
    """Extract the ordered coverer slots of the frozen seed."""
    return tuple(
        tuple(str(type_id) for type_id in record["coverer_type_ids"])
        for record in seed["coverer_sets"]
    )


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
            edges[canonical_edge(slot[0], slot[1])] = column_index
        else:
            raise AssertionError("seed rank changed")
    if set(loops) != set(TYPE_IDS) or len(edges) != 10:
        raise AssertionError("seed is not the registered looped K5")
    return loops, edges


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
    """Check that all induced type signatures are nonempty and distinct."""
    signatures = tuple(
        frozenset(
            column_index
            for column_index, slot in enumerate(slots)
            if type_id in slot
        )
        for type_id in TYPE_IDS
    )
    return all(signatures) and len(set(signatures)) == len(signatures)


def minimum_vertex_cover(
    vertices: tuple[str, ...],
    edges: tuple[tuple[int, tuple[str, str]], ...],
) -> tuple[str, ...]:
    """Return the lexicographically first exact residual cover."""
    for size in range(len(vertices) + 1):
        for selected in itertools.combinations(vertices, size):
            chosen = set(selected)
            if all(left in chosen or right in chosen for _, (left, right) in edges):
                return selected
    raise AssertionError("finite residual graph has no vertex cover")


def maximum_matching(
    edges: tuple[tuple[int, tuple[str, str]], ...],
) -> tuple[int, ...]:
    """Return the lexicographically first exact residual matching."""
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


def bipartition(
    vertices: tuple[str, ...],
    edges: tuple[tuple[int, tuple[str, str]], ...],
) -> tuple[tuple[str, ...], tuple[str, ...]] | None:
    """Return the canonical two-color classes, or None on an odd cycle."""
    adjacency: dict[str, list[str]] = {vertex: [] for vertex in vertices}
    for _, (left, right) in edges:
        adjacency[left].append(right)
        adjacency[right].append(left)
    colors: dict[str, int] = {}
    for root in vertices:
        if root in colors:
            continue
        colors[root] = 0
        queue = deque([root])
        while queue:
            vertex = queue.popleft()
            for neighbor in sorted(adjacency[vertex]):
                if neighbor not in colors:
                    colors[neighbor] = 1 - colors[vertex]
                    queue.append(neighbor)
                elif colors[neighbor] == colors[vertex]:
                    return None
    return (
        tuple(vertex for vertex in vertices if colors[vertex] == 0),
        tuple(vertex for vertex in vertices if colors[vertex] == 1),
    )


def oriented_adjacency(
    left: tuple[str, ...],
    edges: tuple[tuple[int, tuple[str, str]], ...],
) -> tuple[
    dict[str, list[tuple[int, str]]],
    dict[int, tuple[str, str]],
]:
    """Orient every residual edge occurrence from the left color class."""
    left_set = set(left)
    adjacency: dict[str, list[tuple[int, str]]] = {
        vertex: [] for vertex in left
    }
    endpoints: dict[int, tuple[str, str]] = {}
    for column_index, (first, second) in edges:
        if first in left_set:
            oriented = (first, second)
        else:
            oriented = (second, first)
        adjacency[oriented[0]].append((column_index, oriented[1]))
        endpoints[column_index] = oriented
    for records in adjacency.values():
        records.sort()
    return adjacency, endpoints


def find_augmenting_path(
    left: tuple[str, ...],
    adjacency: Mapping[str, list[tuple[int, str]]],
    endpoints: Mapping[int, tuple[str, str]],
    matching: set[int],
) -> tuple[int, ...] | None:
    """Find one deterministic augmenting path in a bipartite multigraph."""
    match_left: dict[str, tuple[str, int]] = {}
    match_right: dict[str, tuple[str, int]] = {}
    for column_index in matching:
        left_vertex, right_vertex = endpoints[column_index]
        match_left[left_vertex] = (right_vertex, column_index)
        match_right[right_vertex] = (left_vertex, column_index)
    queue = deque(vertex for vertex in left if vertex not in match_left)
    visited_left = set(queue)
    parent_left: dict[str, tuple[str, int]] = {}
    parent_right: dict[str, tuple[str, int]] = {}
    terminal: str | None = None
    while queue and terminal is None:
        left_vertex = queue.popleft()
        matched_column = match_left.get(left_vertex, ("", -1))[1]
        for column_index, right_vertex in adjacency[left_vertex]:
            if column_index == matched_column or right_vertex in parent_right:
                continue
            parent_right[right_vertex] = (left_vertex, column_index)
            if right_vertex not in match_right:
                terminal = right_vertex
                break
            next_left, matching_column = match_right[right_vertex]
            if next_left not in visited_left:
                visited_left.add(next_left)
                parent_left[next_left] = (right_vertex, matching_column)
                queue.append(next_left)
    if terminal is None:
        return None
    reverse_path: list[int] = []
    right_vertex = terminal
    while True:
        left_vertex, unmatched_column = parent_right[right_vertex]
        reverse_path.append(unmatched_column)
        if left_vertex not in parent_left:
            break
        right_vertex, matched_column = parent_left[left_vertex]
        reverse_path.append(matched_column)
    return tuple(reversed(reverse_path))


def construct_maximum_matching(
    left: tuple[str, ...],
    edges: tuple[tuple[int, tuple[str, str]], ...],
) -> tuple[tuple[int, ...], int]:
    """Augment until no augmenting path remains."""
    adjacency, endpoints = oriented_adjacency(left, edges)
    matching: set[int] = set()
    searches = 0
    while True:
        searches += 1
        path = find_augmenting_path(
            left,
            adjacency,
            endpoints,
            matching,
        )
        if path is None:
            break
        for column_index in path:
            if column_index in matching:
                matching.remove(column_index)
            else:
                matching.add(column_index)
    return tuple(sorted(matching)), searches


def construct_minimum_cover(
    left: tuple[str, ...],
    right: tuple[str, ...],
    edges: tuple[tuple[int, tuple[str, str]], ...],
    matching: tuple[int, ...],
) -> tuple[str, ...]:
    """Apply alternating reachability to one maximum matching."""
    adjacency, endpoints = oriented_adjacency(left, edges)
    matching_set = set(matching)
    match_left: dict[str, tuple[str, int]] = {}
    match_right: dict[str, tuple[str, int]] = {}
    for column_index in matching:
        left_vertex, right_vertex = endpoints[column_index]
        match_left[left_vertex] = (right_vertex, column_index)
        match_right[right_vertex] = (left_vertex, column_index)
    reachable_left = {vertex for vertex in left if vertex not in match_left}
    reachable_right: set[str] = set()
    queue = deque(sorted(reachable_left))
    while queue:
        left_vertex = queue.popleft()
        for column_index, right_vertex in adjacency[left_vertex]:
            if column_index in matching_set or right_vertex in reachable_right:
                continue
            reachable_right.add(right_vertex)
            if right_vertex in match_right:
                next_left = match_right[right_vertex][0]
                if next_left not in reachable_left:
                    reachable_left.add(next_left)
                    queue.append(next_left)
    return tuple(
        sorted(
            (set(left) - reachable_left)
            | (set(right) & reachable_right)
        )
    )


def validate_odd_cycle(
    cycle: tuple[str, ...],
    target_edges: set[tuple[str, str]],
) -> None:
    """Check one explicit closed odd-cycle certificate."""
    if (
        len(cycle) < 4
        or cycle[0] != cycle[-1]
        or (len(cycle) - 1) % 2 != 1
        or len(set(cycle[:-1])) != len(cycle) - 1
    ):
        raise AssertionError("invalid registered odd cycle")
    if any(
        canonical_edge(left, right) not in target_edges
        for left, right in itertools.pairwise(cycle)
    ):
        raise AssertionError("registered odd cycle uses a missing edge")


def build_case(
    seed_slots: tuple[tuple[str, ...], ...],
    loop_indices: Mapping[str, int],
    edge_indices: Mapping[tuple[str, str], int],
    spec: CaseSpec,
) -> dict[str, Any]:
    """Construct one target residual graph and its exact audit."""
    case_id, graph_kind, unlooped_count, raw_edges, odd_cycle = spec
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
    if is_m95_template(retained):
        raise AssertionError("M97 grammar admitted an M95 template")
    if not complete_normal_form(retained):
        raise AssertionError("M97 target left complete normal form")
    residual_edges = tuple(
        (column_index, canonical_edge(slot[0], slot[1]))
        for column_index, slot in enumerate(seed_slots)
        if column_index not in deleted
        and len(slot) == 2
        and slot[0] in unlooped
        and slot[1] in unlooped
    )
    if {edge for _, edge in residual_edges} != target_edges:
        raise AssertionError("M97 target edge reconstruction failed")
    cover = minimum_vertex_cover(unlooped, residual_edges)
    matching = maximum_matching(residual_edges)
    partition = bipartition(unlooped, residual_edges)
    if odd_cycle is None and partition is None:
        raise AssertionError("registered bipartite case is not bipartite")
    if odd_cycle is not None and partition is not None:
        raise AssertionError("registered boundary case became bipartite")
    if odd_cycle is not None:
        validate_odd_cycle(odd_cycle, target_edges)
    type_bits = max(1, (len(TYPE_IDS) - 1).bit_length())
    column_bits = max(1, (len(seed_slots) - 1).bit_length())
    size_bits = max(1, len(TYPE_IDS).bit_length())
    tight = len(cover) == len(matching)
    if partition is not None:
        left, right = partition
        constructed_matching, searches = construct_maximum_matching(
            left,
            residual_edges,
        )
        constructed_cover = construct_minimum_cover(
            left,
            right,
            residual_edges,
            constructed_matching,
        )
        if (
            len(constructed_matching) != len(matching)
            or len(constructed_cover) != len(cover)
        ):
            raise AssertionError("M97 constructor failed the bounded audit")
        constructor: dict[str, Any] = {
            "status": "constructed_exact",
            "left_type_ids": list(left),
            "right_type_ids": list(right),
            "maximum_matching_column_indices": list(constructed_matching),
            "minimum_cover_type_ids": list(constructed_cover),
            "augmentations": len(constructed_matching),
            "augmenting_path_searches": searches,
            "output_payload_bits": (
                size_bits
                + len(constructed_cover) * (type_bits + column_bits)
            ),
            "output_verification_tests": (
                len(residual_edges) + 2 * len(constructed_cover) + 1
            ),
        }
    else:
        constructor = {
            "status": "rejected_non_bipartite",
            "left_type_ids": None,
            "right_type_ids": None,
            "maximum_matching_column_indices": None,
            "minimum_cover_type_ids": None,
            "augmentations": None,
            "augmenting_path_searches": None,
            "output_payload_bits": None,
            "output_verification_tests": None,
        }
    return {
        "case_id": case_id,
        "residual_graph_kind": graph_kind,
        "unlooped_type_ids": list(unlooped),
        "forced_type_ids": list(forced),
        "target_edge_pairs": [list(edge) for edge in sorted(target_edges)],
        "deleted_loop_column_indices": list(deleted_loops),
        "deleted_edge_column_indices": sorted(deleted_edges),
        "retained_column_count": len(retained),
        "complete_normal_form": True,
        "m95_template": False,
        "residual_edges": [
            {"column_index": column_index, "endpoints": list(edge)}
            for column_index, edge in residual_edges
        ],
        "bipartite": partition is not None,
        "odd_cycle_type_ids": list(odd_cycle) if odd_cycle is not None else None,
        "constructor": constructor,
        "exact_audit": {
            "minimum_cover_type_ids": list(cover),
            "maximum_matching_column_indices": list(matching),
            "residual_vertex_cover_number": len(cover),
            "residual_matching_number": len(matching),
            "matching_equality": tight,
            "matching_gap": len(cover) - len(matching),
            "exact_repair_number": len(forced) + len(cover),
            "equality_certificate_payload_bits": (
                size_bits + len(cover) * (type_bits + column_bits)
                if tight
                else None
            ),
        },
    }


def build_summary() -> dict[str, Any]:
    """Build the canonical M97 constructive profile."""
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
    bipartite_cases = [record for record in cases if record["bipartite"]]
    nonbipartite_cases = [
        record for record in cases if not record["bipartite"]
    ]
    summary: dict[str, Any] = {
        "schema_version": "1.0.0",
        "experiment_id": "EXP-0068",
        "claim_ids": ["DEF-053", "THM-026", "REF-066", "EMP-068"],
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
        "case_grammar": {
            "operation": (
                "delete all loops on the residual prefix, then delete "
                "residual ordinary edges outside the registered target graph"
            ),
            "registered_cases": [
                {
                    "case_id": spec[0],
                    "residual_graph_kind": spec[1],
                    "unlooped_count": spec[2],
                    "target_edge_pairs": [
                        list(canonical_edge(*edge)) for edge in spec[3]
                    ],
                    "odd_cycle_type_ids": (
                        list(spec[4]) if spec[4] is not None else None
                    ),
                }
                for spec in case_specs()
            ],
        },
        "cases": cases,
        "totals": {
            "case_count": len(cases),
            "bipartite_case_count": len(bipartite_cases),
            "nonbipartite_case_count": len(nonbipartite_cases),
            "constructed_exact_count": len(bipartite_cases),
            "nonbipartite_equality_count": sum(
                bool(record["exact_audit"]["matching_equality"])
                for record in nonbipartite_cases
            ),
            "matching_gap_count": sum(
                not bool(record["exact_audit"]["matching_equality"])
                for record in cases
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
            "constructed_output_payload_bits": sum(
                int(record["constructor"]["output_payload_bits"])
                for record in bipartite_cases
            ),
            "constructed_output_verification_tests": sum(
                int(record["constructor"]["output_verification_tests"])
                for record in bipartite_cases
            ),
            "augmentations": sum(
                int(record["constructor"]["augmentations"])
                for record in bipartite_cases
            ),
            "augmenting_path_searches": sum(
                int(record["constructor"]["augmenting_path_searches"])
                for record in bipartite_cases
            ),
            "nonbipartite_equality_payload_bits": sum(
                int(record["exact_audit"]["equality_certificate_payload_bits"])
                for record in nonbipartite_cases
                if record["exact_audit"]["matching_equality"]
            ),
            "maximum_matching_gap": max(
                int(record["exact_audit"]["matching_gap"])
                for record in cases
            ),
        },
        "scope": {
            "classification": "EMPIRICAL",
            "source_dependency": "EMP-066",
            "synthetic_target_graphs": True,
            "not_claimed": [
                "a factor-promise recognizer",
                "a polynomial constructor for arbitrary vertex cover",
                "bipartiteness of every residual coverer graph",
                "factor-independent construction of complete type lists",
                "an asymptotic selector theorem",
                "general classical polynomial-time factoring",
            ],
        },
    }
    summary["summary_sha256"] = canonical_hash(summary)
    return summary


def main() -> int:
    """Print the deterministic M97 constructive summary."""
    totals = build_summary()["totals"]
    print(
        "M97 bipartite-cover profile: PASS "
        f"({totals['case_count']} cases, "
        f"{totals['bipartite_case_count']} constructed bipartite repairs, "
        f"{totals['nonbipartite_equality_count']} nonbipartite equality, "
        f"{totals['matching_gap_count']} matching gap)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
