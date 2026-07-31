"""Build the M99 iterative-compression OCT discovery profile."""

from __future__ import annotations

import hashlib
import itertools
import json
import sys
from collections import deque
from collections.abc import Iterable, Mapping
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.run_m98_oct_cover_profile import (
    solve_with_transversal,
)

SOURCE = ROOT / "schemas" / "m98-oct-cover-v1.json"
M98_CONSTRUCTOR = ROOT / "scripts" / "run_m98_oct_cover_profile.py"

Edge = tuple[int, tuple[str, str]]


def canonical_hash(record: Mapping[str, Any]) -> str:
    """Hash one JSON record after removing its self-hash."""
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
    """Return one ordered undirected edge."""
    return (left, right) if left <= right else (right, left)


def bipartition(
    vertices: tuple[str, ...],
    edges: tuple[Edge, ...],
) -> tuple[tuple[str, ...], tuple[str, ...]] | None:
    """Return one deterministic bipartition or None."""
    adjacency: dict[str, set[str]] = {
        vertex: set() for vertex in vertices
    }
    for _, (left, right) in edges:
        if left == right:
            return None
        adjacency[left].add(right)
        adjacency[right].add(left)
    color: dict[str, int] = {}
    for start in vertices:
        if start in color:
            continue
        color[start] = 0
        queue = deque([start])
        while queue:
            current = queue.popleft()
            for neighbor in sorted(adjacency[current]):
                expected = 1 - color[current]
                if neighbor in color:
                    if color[neighbor] != expected:
                        return None
                else:
                    color[neighbor] = expected
                    queue.append(neighbor)
    return (
        tuple(vertex for vertex in vertices if color[vertex] == 0),
        tuple(vertex for vertex in vertices if color[vertex] == 1),
    )


def induced_without(
    vertices: tuple[str, ...],
    edges: tuple[Edge, ...],
    deleted: Iterable[str],
) -> tuple[tuple[str, ...], tuple[Edge, ...]]:
    """Delete a vertex set and every incident edge occurrence."""
    deleted_set = set(deleted)
    remaining_vertices = tuple(
        vertex for vertex in vertices if vertex not in deleted_set
    )
    remaining_edges = tuple(
        (index, edge)
        for index, edge in edges
        if edge[0] not in deleted_set and edge[1] not in deleted_set
    )
    return remaining_vertices, remaining_edges


def is_oct(
    vertices: tuple[str, ...],
    edges: tuple[Edge, ...],
    candidate: Iterable[str],
) -> bool:
    """Return whether deleting candidate makes the graph bipartite."""
    remaining_vertices, remaining_edges = induced_without(
        vertices,
        edges,
        candidate,
    )
    return bipartition(remaining_vertices, remaining_edges) is not None


def _add_arc(
    adjacency: list[set[int]],
    capacity: dict[tuple[int, int], int],
    source: int,
    target: int,
    value: int,
) -> None:
    """Add or enlarge one residual-network arc."""
    adjacency[source].add(target)
    adjacency[target].add(source)
    capacity[(source, target)] = max(
        capacity.get((source, target), 0),
        value,
    )
    capacity.setdefault((target, source), 0)


def _residual_path(
    adjacency: list[set[int]],
    capacity: Mapping[tuple[int, int], int],
    source: int,
    sink: int,
) -> list[int] | None:
    """Find one deterministic residual path by breadth-first search."""
    parent = {source: -1}
    queue = deque([source])
    while queue and sink not in parent:
        current = queue.popleft()
        for neighbor in sorted(adjacency[current]):
            if neighbor not in parent and capacity[(current, neighbor)] > 0:
                parent[neighbor] = current
                queue.append(neighbor)
    if sink not in parent:
        return None
    path = [sink]
    while path[-1] != source:
        path.append(parent[path[-1]])
    path.reverse()
    return path


def minimum_vertex_separator(
    vertices: tuple[str, ...],
    edges: tuple[Edge, ...],
    sources: Iterable[str],
    sinks: Iterable[str],
    budget: int,
) -> tuple[tuple[str, ...] | None, dict[str, int]]:
    """Find a minimum allowed terminal-deleting separator up to budget."""
    source_set = set(sources)
    sink_set = set(sinks)
    if budget < 0:
        return None, {"flow_augmentations": 0, "flow_searches": 0}
    if not source_set or not sink_set:
        return (), {"flow_augmentations": 0, "flow_searches": 0}
    index = {vertex: position for position, vertex in enumerate(vertices)}
    node_count = 2 * len(vertices) + 2
    super_source = node_count - 2
    super_sink = node_count - 1
    adjacency: list[set[int]] = [set() for _ in range(node_count)]
    capacity: dict[tuple[int, int], int] = {}
    infinity = budget + 1
    for vertex, position in index.items():
        vertex_in = 2 * position
        vertex_out = vertex_in + 1
        _add_arc(adjacency, capacity, vertex_in, vertex_out, 1)
        if vertex in source_set:
            _add_arc(
                adjacency,
                capacity,
                super_source,
                vertex_in,
                infinity,
            )
        if vertex in sink_set:
            _add_arc(
                adjacency,
                capacity,
                vertex_out,
                super_sink,
                infinity,
            )
    for _, (left, right) in edges:
        left_out = 2 * index[left] + 1
        left_in = left_out - 1
        right_out = 2 * index[right] + 1
        right_in = right_out - 1
        _add_arc(adjacency, capacity, left_out, right_in, infinity)
        _add_arc(adjacency, capacity, right_out, left_in, infinity)
    flow = 0
    augmentations = 0
    searches = 0
    while True:
        searches += 1
        path = _residual_path(
            adjacency,
            capacity,
            super_source,
            super_sink,
        )
        if path is None:
            break
        amount = min(
            capacity[(left, right)]
            for left, right in itertools.pairwise(path)
        )
        for node_from, node_to in itertools.pairwise(path):
            capacity[(node_from, node_to)] -= amount
            capacity[(node_to, node_from)] += amount
        flow += amount
        augmentations += 1
        if flow > budget:
            return None, {
                "flow_augmentations": augmentations,
                "flow_searches": searches,
            }
    reachable = {super_source}
    queue = deque([super_source])
    while queue:
        current = queue.popleft()
        for neighbor in sorted(adjacency[current]):
            if (
                neighbor not in reachable
                and capacity[(current, neighbor)] > 0
            ):
                reachable.add(neighbor)
                queue.append(neighbor)
    separator = tuple(
        vertex
        for vertex, position in index.items()
        if 2 * position in reachable and 2 * position + 1 not in reachable
    )
    if len(separator) != flow or len(separator) > budget:
        raise AssertionError("M99 separator reconstruction changed")
    return separator, {
        "flow_augmentations": augmentations,
        "flow_searches": searches,
    }


def compress_oct(
    vertices: tuple[str, ...],
    edges: tuple[Edge, ...],
    almost_oct: tuple[str, ...],
    cap: int,
) -> tuple[tuple[str, ...] | None, dict[str, int]]:
    """Compress a known OCT of size at most cap+1."""
    if len(almost_oct) > cap + 1 or not set(almost_oct) <= set(vertices):
        raise AssertionError("M99 compression input changed")
    if not is_oct(vertices, edges, almost_oct):
        raise AssertionError("M99 compression advice is not an OCT")
    base_vertices, base_edges = induced_without(
        vertices,
        edges,
        almost_oct,
    )
    partition = bipartition(base_vertices, base_edges)
    if partition is None:
        raise AssertionError("M99 compression base changed")
    base_left, base_right = partition
    left_set = set(base_left)
    right_set = set(base_right)
    best: tuple[str, ...] | None = None
    partitions = 0
    flow_calls = 0
    augmentations = 0
    searches = 0
    edge_pairs = [edge for _, edge in edges]
    for states in itertools.product(range(3), repeat=len(almost_oct)):
        partitions += 1
        left = {
            vertex
            for vertex, state in zip(almost_oct, states, strict=True)
            if state == 0
        }
        right = {
            vertex
            for vertex, state in zip(almost_oct, states, strict=True)
            if state == 1
        }
        deleted = {
            vertex
            for vertex, state in zip(almost_oct, states, strict=True)
            if state == 2
        }
        if len(deleted) > cap:
            continue
        if any(
            (first in left and second in left)
            or (first in right and second in right)
            for first, second in edge_pairs
        ):
            continue
        left_neighbors = {
            endpoint
            for first, second in edge_pairs
            for endpoint, other in ((first, second), (second, first))
            if other in left and endpoint in set(base_vertices)
        }
        right_neighbors = {
            endpoint
            for first, second in edge_pairs
            for endpoint, other in ((first, second), (second, first))
            if other in right and endpoint in set(base_vertices)
        }
        separator_sources = (
            (left_neighbors & left_set)
            | (right_neighbors & right_set)
        )
        separator_sinks = (
            (right_neighbors & left_set)
            | (left_neighbors & right_set)
        )
        flow_calls += 1
        separator, metrics = minimum_vertex_separator(
            base_vertices,
            base_edges,
            separator_sources,
            separator_sinks,
            cap - len(deleted),
        )
        augmentations += metrics["flow_augmentations"]
        searches += metrics["flow_searches"]
        if separator is None:
            continue
        candidate = tuple(sorted(deleted | set(separator)))
        if len(candidate) > cap or not is_oct(vertices, edges, candidate):
            raise AssertionError("M99 compression candidate changed")
        if best is None or (len(candidate), candidate) < (len(best), best):
            best = candidate
    return best, {
        "partition_count": partitions,
        "flow_call_count": flow_calls,
        "flow_augmentations": augmentations,
        "flow_searches": searches,
    }


def discover_oct(
    vertices: tuple[str, ...],
    edges: tuple[Edge, ...],
    cap: int,
) -> dict[str, Any]:
    """Discover a minimum OCT of size at most cap by iterative compression."""
    if cap < 0:
        raise ValueError("cap must be nonnegative")
    current: tuple[str, ...] = ()
    compression_calls = 0
    partition_count = 0
    flow_calls = 0
    augmentations = 0
    searches = 0
    for prefix_size in range(1, len(vertices) + 1):
        prefix_vertices = vertices[:prefix_size]
        prefix_set = set(prefix_vertices)
        prefix_edges = tuple(
            (index, edge)
            for index, edge in edges
            if edge[0] in prefix_set and edge[1] in prefix_set
        )
        almost_oct = tuple(sorted(set(current) | {prefix_vertices[-1]}))
        compression_calls += 1
        current_result, metrics = compress_oct(
            prefix_vertices,
            prefix_edges,
            almost_oct,
            cap,
        )
        partition_count += metrics["partition_count"]
        flow_calls += metrics["flow_call_count"]
        augmentations += metrics["flow_augmentations"]
        searches += metrics["flow_searches"]
        if current_result is None:
            return {
                "status": "rejected_above_cap",
                "cap": cap,
                "rejected_prefix_size": prefix_size,
                "oct_type_ids": None,
                "oct_size": None,
                "compression_calls": compression_calls,
                "partition_count": partition_count,
                "flow_call_count": flow_calls,
                "flow_augmentations": augmentations,
                "flow_searches": searches,
            }
        current = current_result
    return {
        "status": "discovered_exact",
        "cap": cap,
        "rejected_prefix_size": None,
        "oct_type_ids": list(current),
        "oct_size": len(current),
        "compression_calls": compression_calls,
        "partition_count": partition_count,
        "flow_call_count": flow_calls,
        "flow_augmentations": augmentations,
        "flow_searches": searches,
    }


def source_cases(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    """Extract the eight exact M98 target graphs and discovery caps."""
    cases: list[dict[str, Any]] = []
    for record in source["cases"]:
        edges = tuple(
            (
                int(edge_record["column_index"]),
                canonical_edge(*edge_record["endpoints"]),
            )
            for edge_record in record["residual_edges"]
        )
        cases.append(
            {
                "case_id": str(record["case_id"]),
                "vertices": tuple(str(item) for item in record["unlooped_type_ids"]),
                "edges": edges,
                "cap": int(record["transversal_size"]),
                "exact_cover_number": int(
                    record["exact_audit"]["residual_vertex_cover_number"]
                ),
            }
        )
    return cases


def build_case(spec: Mapping[str, Any]) -> dict[str, Any]:
    """Run discovery and, when accepted, compose the M98 exact cover."""
    vertices = tuple(spec["vertices"])
    edges = tuple(spec["edges"])
    cap = int(spec["cap"])
    discovery = discover_oct(vertices, edges, cap)
    if discovery["status"] == "discovered_exact":
        oct_vertices = tuple(discovery["oct_type_ids"])
        constructor = solve_with_transversal(vertices, edges, oct_vertices)
        if constructor["status"] != "constructed_exact":
            raise AssertionError("M99 discovered OCT failed M98")
        if int(constructor["minimum_cover_number"]) != int(
            spec["exact_cover_number"]
        ):
            raise AssertionError("M99 composed cover changed")
        cover = constructor["minimum_cover_type_ids"]
        cover_number = constructor["minimum_cover_number"]
    else:
        cover = None
        cover_number = None
    type_bits = max(1, (len(vertices) - 1).bit_length())
    size_bits = max(1, len(vertices).bit_length())
    return {
        "case_id": str(spec["case_id"]),
        "vertex_type_ids": list(vertices),
        "residual_edges": [
            {"column_index": index, "endpoints": list(edge)}
            for index, edge in edges
        ],
        "cap": cap,
        "discovery": discovery,
        "discovered_oct_payload_bits": (
            size_bits + int(discovery["oct_size"]) * type_bits
            if discovery["oct_size"] is not None
            else 0
        ),
        "composed_minimum_cover_type_ids": cover,
        "composed_minimum_cover_number": cover_number,
        "composed_cover_payload_bits": (
            size_bits + len(cover) * type_bits if cover is not None else 0
        ),
    }


def build_summary() -> dict[str, Any]:
    """Build the canonical M99 discovery and composition profile."""
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    specs = source_cases(source)
    cases = [build_case(spec) for spec in specs]
    accepted = [
        record
        for record in cases
        if record["discovery"]["status"] == "discovered_exact"
    ]
    rejected = [
        record
        for record in cases
        if record["discovery"]["status"] == "rejected_above_cap"
    ]
    summary: dict[str, Any] = {
        "schema_version": "1.0.0",
        "experiment_id": "EXP-0070",
        "claim_ids": ["DEF-055", "THM-028", "REF-068", "EMP-070"],
        "source": {
            "path": str(SOURCE.relative_to(ROOT)).replace("\\", "/"),
            "file_sha256": file_sha256(SOURCE),
            "summary_sha256": str(source["summary_sha256"]),
            "m98_constructor_path": str(
                M98_CONSTRUCTOR.relative_to(ROOT)
            ).replace("\\", "/"),
            "m98_constructor_sha256": file_sha256(M98_CONSTRUCTOR),
        },
        "literature_basis": {
            "citation_key": "lokshtanov2009oct",
            "doi": "10.1007/978-3-642-10217-2_37",
            "inspected_url": (
                "https://sites.cs.ucsb.edu/~daniello/papers/"
                "octIterComp.pdf"
            ),
            "inspected_pages": 5,
            "imported_result": (
                "iterative-compression OCT discovery in "
                "O(3^k k |E| |V|)"
            ),
            "local_status": (
                "self-contained reconstruction with conservative "
                "O(3^(k+1)(k+1)t(t+q)) bound"
            ),
        },
        "cases": cases,
        "totals": {
            "case_count": len(cases),
            "accepted_count": len(accepted),
            "rejected_count": len(rejected),
            "cap_sum": sum(int(record["cap"]) for record in cases),
            "discovered_oct_size_sum": sum(
                int(record["discovery"]["oct_size"])
                for record in accepted
            ),
            "compression_calls": sum(
                int(record["discovery"]["compression_calls"])
                for record in cases
            ),
            "partition_count": sum(
                int(record["discovery"]["partition_count"])
                for record in cases
            ),
            "flow_call_count": sum(
                int(record["discovery"]["flow_call_count"])
                for record in cases
            ),
            "flow_augmentations": sum(
                int(record["discovery"]["flow_augmentations"])
                for record in cases
            ),
            "flow_searches": sum(
                int(record["discovery"]["flow_searches"])
                for record in cases
            ),
            "discovered_oct_payload_bits": sum(
                int(record["discovered_oct_payload_bits"])
                for record in accepted
            ),
            "composed_cover_number_sum": sum(
                int(record["composed_minimum_cover_number"])
                for record in accepted
            ),
            "composed_cover_payload_bits": sum(
                int(record["composed_cover_payload_bits"])
                for record in accepted
            ),
        },
        "scope": {
            "classification": "EMPIRICAL",
            "explicit_graph_oct_discovery": True,
            "not_claimed": [
                "factor-independent construction of the coverer graph",
                "a polynomial algorithm for unrestricted OCT cap",
                "a polynomial constructor for arbitrary vertex cover",
                "a factor-promise recognizer",
                "an asymptotic selector theorem",
                "general classical polynomial-time factoring",
            ],
        },
    }
    summary["summary_sha256"] = canonical_hash(summary)
    return summary


def main() -> int:
    """Print the deterministic M99 discovery summary."""
    totals = build_summary()["totals"]
    digest = hashlib.sha256(
        json.dumps(totals, sort_keys=True).encode("utf-8")
    ).hexdigest()
    print(
        "M99 OCT-discovery profile: PASS "
        f"({totals['case_count']} cases, "
        f"{totals['accepted_count']} discovered, "
        f"{totals['rejected_count']} rejected, "
        f"ledger {digest[:12]})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
