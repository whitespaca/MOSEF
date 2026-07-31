"""Independently validate the M99 OCT discovery and composition records."""

from __future__ import annotations

import hashlib
import itertools
import json
from collections import deque
from collections.abc import Mapping
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas" / "m99-oct-discovery-v1.json"
SOURCE = ROOT / "schemas" / "m98-oct-cover-v1.json"
M98_CONSTRUCTOR = ROOT / "scripts" / "run_m98_oct_cover_profile.py"
SOURCE_ANCHOR = {
    "path": "schemas/m98-oct-cover-v1.json",
    "file_sha256": (
        "c25cacc1e1e4217e87e6ff15b95c5c0356e7025b19833095feeef3f44bd45cb3"
    ),
    "summary_sha256": (
        "745cab13a67cae8f1e09ac084b75d78e870a0aacc88892be4facf032a5f3478f"
    ),
    "m98_constructor_path": "scripts/run_m98_oct_cover_profile.py",
    "m98_constructor_sha256": (
        "6d2eba94384f2b09e6b1f06f1346d8fbdd68914b34c406d76cd0d9797566c1a4"
    ),
}
LITERATURE_BASIS = {
    "citation_key": "lokshtanov2009oct",
    "doi": "10.1007/978-3-642-10217-2_37",
    "inspected_url": (
        "https://sites.cs.ucsb.edu/~daniello/papers/octIterComp.pdf"
    ),
    "inspected_pages": 5,
    "imported_result": (
        "iterative-compression OCT discovery in O(3^k k |E| |V|)"
    ),
    "local_status": (
        "self-contained reconstruction with conservative "
        "O(3^(k+1)(k+1)t(t+q)) bound"
    ),
}
EXPECTED_SCOPE = {
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
}
EXPECTED_METRICS = {
    "O1-triangle-pendant": (4, 18, 17, 8, 14),
    "O2-C5": (5, 15, 15, 2, 4),
    "O3-bowtie": (5, 27, 21, 12, 16),
    "O4-house": (5, 15, 15, 2, 4),
    "O5-K4": (4, 18, 16, 10, 18),
    "O6-K5-e": (5, 21, 19, 12, 18),
    "O7-K5-valid": (5, 45, 29, 28, 48),
    "R1-K5-invalid": (5, 45, 28, 28, 36),
}

Edge = tuple[int, tuple[str, str]]


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
    """Return one ordered undirected edge."""
    return (left, right) if left <= right else (right, left)


def is_bipartite(
    vertices: tuple[str, ...],
    edges: tuple[Edge, ...],
    deleted: set[str] | None = None,
) -> bool:
    """Independently two-color an induced graph."""
    removed = set() if deleted is None else deleted
    remaining = tuple(vertex for vertex in vertices if vertex not in removed)
    adjacency: dict[str, set[str]] = {
        vertex: set() for vertex in remaining
    }
    for _, (left, right) in edges:
        if left in removed or right in removed:
            continue
        if left == right:
            return False
        adjacency[left].add(right)
        adjacency[right].add(left)
    color: dict[str, int] = {}
    for start in remaining:
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
                        return False
                else:
                    color[neighbor] = expected
                    queue.append(neighbor)
    return True


def minimum_oct(
    vertices: tuple[str, ...],
    edges: tuple[Edge, ...],
) -> tuple[str, ...]:
    """Enumerate the lexicographically first exact OCT."""
    for size in range(len(vertices) + 1):
        for selected in itertools.combinations(vertices, size):
            if is_bipartite(vertices, edges, set(selected)):
                return selected
    raise AssertionError("finite graph has no OCT")


def minimum_vertex_cover(
    vertices: tuple[str, ...],
    edges: tuple[Edge, ...],
) -> tuple[str, ...]:
    """Enumerate the lexicographically first exact vertex cover."""
    for size in range(len(vertices) + 1):
        for selected in itertools.combinations(vertices, size):
            chosen = set(selected)
            if all(
                left in chosen or right in chosen
                for _, (left, right) in edges
            ):
                return selected
    raise AssertionError("finite graph has no vertex cover")


def source_records() -> tuple[Mapping[str, Any], list[dict[str, Any]]]:
    """Bind the M98 source and independently extract its target graphs."""
    if file_sha256(SOURCE) != SOURCE_ANCHOR["file_sha256"]:
        raise AssertionError("M99 source file hash changed")
    if file_sha256(M98_CONSTRUCTOR) != SOURCE_ANCHOR[
        "m98_constructor_sha256"
    ]:
        raise AssertionError("M99 M98 constructor hash changed")
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    if source.get("summary_sha256") != SOURCE_ANCHOR["summary_sha256"]:
        raise AssertionError("M99 source summary hash changed")
    if canonical_hash(source) != SOURCE_ANCHOR["summary_sha256"]:
        raise AssertionError("M99 source content changed")
    records = []
    for source_case in source["cases"]:
        records.append(
            {
                "case_id": str(source_case["case_id"]),
                "vertices": tuple(
                    str(item) for item in source_case["unlooped_type_ids"]
                ),
                "edges": tuple(
                    (
                        int(edge_record["column_index"]),
                        canonical_edge(*edge_record["endpoints"]),
                    )
                    for edge_record in source_case["residual_edges"]
                ),
                "cap": int(source_case["transversal_size"]),
                "cover_number": int(
                    source_case["exact_audit"][
                        "residual_vertex_cover_number"
                    ]
                ),
            }
        )
    return source, records


def validate_case(
    record: Mapping[str, Any],
    expected: Mapping[str, Any],
) -> dict[str, int | bool]:
    """Validate one discovery result against independent exact enumeration."""
    case_id = str(expected["case_id"])
    vertices = tuple(expected["vertices"])
    edges = tuple(expected["edges"])
    cap = int(expected["cap"])
    expected_edges = [
        {"column_index": index, "endpoints": list(edge)}
        for index, edge in edges
    ]
    if record.get("case_id") != case_id:
        raise AssertionError("M99 case ID changed")
    if record.get("vertex_type_ids") != list(vertices):
        raise AssertionError("M99 vertex registry changed")
    if record.get("residual_edges") != expected_edges:
        raise AssertionError("M99 residual edges changed")
    if record.get("cap") != cap:
        raise AssertionError("M99 cap changed")
    optimum_oct = minimum_oct(vertices, edges)
    optimum_cover = minimum_vertex_cover(vertices, edges)
    if len(optimum_cover) != int(expected["cover_number"]):
        raise AssertionError("M99 source cover audit changed")
    discovery = record.get("discovery")
    if not isinstance(discovery, dict):
        raise AssertionError("M99 discovery framing changed")
    metrics = (
        int(discovery.get("compression_calls", -1)),
        int(discovery.get("partition_count", -1)),
        int(discovery.get("flow_call_count", -1)),
        int(discovery.get("flow_augmentations", -1)),
        int(discovery.get("flow_searches", -1)),
    )
    if metrics != EXPECTED_METRICS[case_id]:
        raise AssertionError("M99 discovery metrics changed")
    size_bits = max(1, len(vertices).bit_length())
    type_bits = max(1, (len(vertices) - 1).bit_length())
    accepted = len(optimum_oct) <= cap
    if accepted:
        if discovery.get("status") != "discovered_exact":
            raise AssertionError("M99 accepted status changed")
        supplied_oct = discovery.get("oct_type_ids")
        if not isinstance(supplied_oct, list):
            raise AssertionError("M99 OCT framing changed")
        if tuple(supplied_oct) != optimum_oct:
            raise AssertionError("M99 discovered OCT changed")
        if discovery.get("oct_size") != len(optimum_oct):
            raise AssertionError("M99 OCT size changed")
        if discovery.get("rejected_prefix_size") is not None:
            raise AssertionError("M99 accepted prefix framing changed")
        if not is_bipartite(vertices, edges, set(supplied_oct)):
            raise AssertionError("M99 OCT failed bipartition")
        expected_oct_bits = size_bits + len(optimum_oct) * type_bits
        if record.get("discovered_oct_payload_bits") != expected_oct_bits:
            raise AssertionError("M99 OCT payload changed")
        supplied_cover = record.get("composed_minimum_cover_type_ids")
        if not isinstance(supplied_cover, list):
            raise AssertionError("M99 cover framing changed")
        if tuple(supplied_cover) != optimum_cover:
            raise AssertionError("M99 composed cover changed")
        if record.get("composed_minimum_cover_number") != len(
            optimum_cover
        ):
            raise AssertionError("M99 cover number changed")
        expected_cover_bits = size_bits + len(optimum_cover) * type_bits
        if record.get("composed_cover_payload_bits") != expected_cover_bits:
            raise AssertionError("M99 cover payload changed")
    else:
        if discovery.get("status") != "rejected_above_cap":
            raise AssertionError("M99 rejection status changed")
        if (
            discovery.get("oct_type_ids") is not None
            or discovery.get("oct_size") is not None
        ):
            raise AssertionError("M99 rejection OCT framing changed")
        if discovery.get("rejected_prefix_size") != len(vertices):
            raise AssertionError("M99 rejection prefix changed")
        if (
            record.get("discovered_oct_payload_bits") != 0
            or record.get("composed_minimum_cover_type_ids") is not None
            or record.get("composed_minimum_cover_number") is not None
            or record.get("composed_cover_payload_bits") != 0
        ):
            raise AssertionError("M99 rejection output changed")
        expected_oct_bits = 0
        expected_cover_bits = 0
    if discovery.get("cap") != cap:
        raise AssertionError("M99 discovery cap changed")
    return {
        "accepted": accepted,
        "cap": cap,
        "oct_size": len(optimum_oct) if accepted else 0,
        "compression_calls": metrics[0],
        "partition_count": metrics[1],
        "flow_call_count": metrics[2],
        "flow_augmentations": metrics[3],
        "flow_searches": metrics[4],
        "oct_bits": expected_oct_bits,
        "cover_number": len(optimum_cover) if accepted else 0,
        "cover_bits": expected_cover_bits,
    }


def validate_all(
    schema: Mapping[str, Any] | None = None,
) -> dict[str, int]:
    """Validate the complete M99 portfolio."""
    data = (
        json.loads(SCHEMA.read_text(encoding="utf-8"))
        if schema is None
        else dict(schema)
    )
    if data.get("schema_version") != "1.0.0":
        raise AssertionError("unsupported M99 schema version")
    if data.get("experiment_id") != "EXP-0070":
        raise AssertionError("M99 experiment ID changed")
    if data.get("claim_ids") != [
        "DEF-055",
        "THM-028",
        "REF-068",
        "EMP-070",
    ]:
        raise AssertionError("M99 claim registry changed")
    if data.get("source") != SOURCE_ANCHOR:
        raise AssertionError("M99 source anchor changed")
    if data.get("literature_basis") != LITERATURE_BASIS:
        raise AssertionError("M99 literature basis changed")
    if data.get("scope") != EXPECTED_SCOPE:
        raise AssertionError("M99 scope boundary changed")
    if data.get("summary_sha256") != canonical_hash(data):
        raise AssertionError("M99 canonical summary hash changed")
    _, expected_cases = source_records()
    records = data.get("cases")
    if not isinstance(records, list) or len(records) != len(expected_cases):
        raise AssertionError("M99 case count changed")
    reports = [
        validate_case(record, expected)
        for record, expected in zip(records, expected_cases, strict=True)
    ]
    accepted = [report for report in reports if report["accepted"]]
    totals = {
        "case_count": len(reports),
        "accepted_count": len(accepted),
        "rejected_count": len(reports) - len(accepted),
        "cap_sum": sum(int(report["cap"]) for report in reports),
        "discovered_oct_size_sum": sum(
            int(report["oct_size"]) for report in accepted
        ),
        "compression_calls": sum(
            int(report["compression_calls"]) for report in reports
        ),
        "partition_count": sum(
            int(report["partition_count"]) for report in reports
        ),
        "flow_call_count": sum(
            int(report["flow_call_count"]) for report in reports
        ),
        "flow_augmentations": sum(
            int(report["flow_augmentations"]) for report in reports
        ),
        "flow_searches": sum(
            int(report["flow_searches"]) for report in reports
        ),
        "discovered_oct_payload_bits": sum(
            int(report["oct_bits"]) for report in accepted
        ),
        "composed_cover_number_sum": sum(
            int(report["cover_number"]) for report in accepted
        ),
        "composed_cover_payload_bits": sum(
            int(report["cover_bits"]) for report in accepted
        ),
    }
    if data.get("totals") != totals:
        raise AssertionError("M99 totals changed")
    return totals


def main() -> int:
    """Run the standalone M99 checker."""
    totals = validate_all()
    print(
        "M99 OCT-discovery checker: PASS "
        f"({totals['case_count']} cases, "
        f"{totals['accepted_count']} exact discoveries, "
        f"{totals['rejected_count']} cap rejection, "
        f"{totals['partition_count']} partitions)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
