"""Independently validate the M97 constructive bipartite covers."""

from __future__ import annotations

import hashlib
import itertools
import json
from collections.abc import Iterable, Mapping
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas" / "m97-bipartite-cover-v1.json"
SOURCE = ROOT / "schemas" / "m95-coverer-graph-profile-v1.json"
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
}
EXPECTED_SCOPE = {
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
}

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
    """Return the independently frozen M97 case registry."""
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


def template_slots(kind: str) -> tuple[tuple[str, ...], ...]:
    """Return one complete five-type M95 slot template."""
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
    """Check nonempty, pairwise-distinct induced type signatures."""
    signatures = tuple(
        frozenset(
            column_index
            for column_index, slot in enumerate(slots)
            if type_id in slot
        )
        for type_id in TYPE_IDS
    )
    return all(signatures) and len(set(signatures)) == len(signatures)


def seed_from_source() -> tuple[Mapping[str, Any], tuple[tuple[str, ...], ...]]:
    """Bind and reconstruct the frozen M95 looped-K5 seed."""
    if file_sha256(SOURCE) != SOURCE_ANCHOR["file_sha256"]:
        raise AssertionError("M97 source file hash changed")
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    if source.get("summary_sha256") != SOURCE_ANCHOR["summary_sha256"]:
        raise AssertionError("M97 source summary hash changed")
    if canonical_hash(source) != SOURCE_ANCHOR["summary_sha256"]:
        raise AssertionError("M97 source content changed")
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
        raise AssertionError("M97 seed instance changed")
    slots = tuple(
        tuple(str(type_id) for type_id in record["coverer_type_ids"])
        for record in seed["coverer_sets"]
    )
    if len(slots) != 15 or sorted(slots) != sorted(
        template_slots("looped_clique")
    ):
        raise AssertionError("M97 seed is not looped K5")
    return seed, slots


def slot_maps(
    slots: tuple[tuple[str, ...], ...],
) -> tuple[dict[str, int], dict[tuple[str, str], int]]:
    """Index the independently reconstructed seed slots."""
    loops: dict[str, int] = {}
    edges: dict[tuple[str, str], int] = {}
    for column_index, slot in enumerate(slots):
        if len(slot) == 1:
            loops[slot[0]] = column_index
        elif len(slot) == 2:
            edges[canonical_edge(slot[0], slot[1])] = column_index
        else:
            raise AssertionError("M97 seed rank changed")
    if set(loops) != set(TYPE_IDS) or set(edges) != set(
        itertools.combinations(TYPE_IDS, 2)
    ):
        raise AssertionError("M97 seed slot registry changed")
    return loops, edges


def minimum_vertex_cover(
    vertices: tuple[str, ...],
    edges: tuple[tuple[int, tuple[str, str]], ...],
) -> tuple[str, ...]:
    """Independently enumerate the first minimum cover."""
    for size in range(len(vertices) + 1):
        for selected in itertools.combinations(vertices, size):
            chosen = set(selected)
            if all(left in chosen or right in chosen for _, (left, right) in edges):
                return selected
    raise AssertionError("residual graph has no cover")


def maximum_matching(
    edges: tuple[tuple[int, tuple[str, str]], ...],
) -> tuple[int, ...]:
    """Independently enumerate the first maximum matching."""
    for size in range(len(edges), -1, -1):
        for selected in itertools.combinations(edges, size):
            endpoints = [
                endpoint
                for _, edge in selected
                for endpoint in edge
            ]
            if len(endpoints) == len(set(endpoints)):
                return tuple(column_index for column_index, _ in selected)
    raise AssertionError("residual graph has no matching")


def validate_partition(
    vertices: tuple[str, ...],
    edges: tuple[tuple[int, tuple[str, str]], ...],
    left: list[str],
    right: list[str],
) -> None:
    """Validate a supplied bipartition without constructing it."""
    if (
        len(left) != len(set(left))
        or len(right) != len(set(right))
        or set(left) & set(right)
        or set(left) | set(right) != set(vertices)
    ):
        raise AssertionError("M97 bipartition vertex registry changed")
    left_set = set(left)
    right_set = set(right)
    if any(
        not (
            (first in left_set and second in right_set)
            or (first in right_set and second in left_set)
        )
        for _, (first, second) in edges
    ):
        raise AssertionError("M97 bipartition crossing failed")


def validate_odd_cycle(
    cycle: list[str],
    target_edges: set[tuple[str, str]],
) -> None:
    """Validate a closed simple odd-cycle certificate."""
    if (
        len(cycle) < 4
        or cycle[0] != cycle[-1]
        or (len(cycle) - 1) % 2 != 1
        or len(set(cycle[:-1])) != len(cycle) - 1
    ):
        raise AssertionError("M97 odd cycle framing changed")
    if any(
        canonical_edge(left, right) not in target_edges
        for left, right in itertools.pairwise(cycle)
    ):
        raise AssertionError("M97 odd cycle edge changed")


def validate_matching(
    columns: list[int],
    edges: tuple[tuple[int, tuple[str, str]], ...],
) -> None:
    """Validate one supplied matching by edge occurrence."""
    edge_map = dict(edges)
    if len(columns) != len(set(columns)) or any(
        column not in edge_map for column in columns
    ):
        raise AssertionError("M97 constructor matching registry changed")
    endpoints = [
        endpoint
        for column in columns
        for endpoint in edge_map[column]
    ]
    if len(endpoints) != len(set(endpoints)):
        raise AssertionError("M97 constructor matching endpoints overlap")


def validate_cover(
    cover: list[str],
    vertices: tuple[str, ...],
    edges: tuple[tuple[int, tuple[str, str]], ...],
) -> None:
    """Validate one supplied residual cover."""
    if len(cover) != len(set(cover)) or not set(cover) <= set(vertices):
        raise AssertionError("M97 constructor cover registry changed")
    chosen = set(cover)
    if any(
        first not in chosen and second not in chosen
        for _, (first, second) in edges
    ):
        raise AssertionError("M97 constructor cover missed an edge")


def expected_case_grammar() -> dict[str, Any]:
    """Return the exact public case registry."""
    return {
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
    }


def validate_case(
    record: Mapping[str, Any],
    slots: tuple[tuple[str, ...], ...],
    loop_indices: Mapping[str, int],
    edge_indices: Mapping[tuple[str, str], int],
    spec: CaseSpec,
) -> dict[str, int | bool]:
    """Validate one target graph, constructor result, and exact audit."""
    case_id, graph_kind, unlooped_count, raw_edges, odd_cycle = spec
    unlooped = TYPE_IDS[:unlooped_count]
    forced = TYPE_IDS[unlooped_count:]
    target_edges = {canonical_edge(*edge) for edge in raw_edges}
    deleted_loops = [loop_indices[type_id] for type_id in unlooped]
    deleted_edges = sorted(
        column_index
        for edge, column_index in edge_indices.items()
        if edge[0] in unlooped
        and edge[1] in unlooped
        and edge not in target_edges
    )
    expected_scalars = {
        "case_id": case_id,
        "residual_graph_kind": graph_kind,
        "unlooped_type_ids": list(unlooped),
        "forced_type_ids": list(forced),
        "target_edge_pairs": [list(edge) for edge in sorted(target_edges)],
        "deleted_loop_column_indices": deleted_loops,
        "deleted_edge_column_indices": deleted_edges,
        "complete_normal_form": True,
        "m95_template": False,
        "bipartite": odd_cycle is None,
        "odd_cycle_type_ids": (
            list(odd_cycle) if odd_cycle is not None else None
        ),
    }
    for field, expected in expected_scalars.items():
        if record.get(field) != expected:
            raise AssertionError(f"M97 {field} changed")
    deleted = set(deleted_loops + deleted_edges)
    retained = tuple(
        slot
        for column_index, slot in enumerate(slots)
        if column_index not in deleted
    )
    if int(record["retained_column_count"]) != len(retained):
        raise AssertionError("M97 retained column count changed")
    if not complete_normal_form(retained):
        raise AssertionError("M97 complete normal form failed")
    if is_m95_template(retained):
        raise AssertionError("M97 target became an M95 template")
    residual_edges = tuple(
        (column_index, canonical_edge(slot[0], slot[1]))
        for column_index, slot in enumerate(slots)
        if column_index not in deleted
        and len(slot) == 2
        and slot[0] in unlooped
        and slot[1] in unlooped
    )
    expected_edges = [
        {"column_index": index, "endpoints": list(edge)}
        for index, edge in residual_edges
    ]
    if record["residual_edges"] != expected_edges:
        raise AssertionError("M97 residual edges changed")
    cover = minimum_vertex_cover(unlooped, residual_edges)
    matching = maximum_matching(residual_edges)
    tau = len(cover)
    nu = len(matching)
    tight = tau == nu
    exact_audit = {
        "minimum_cover_type_ids": list(cover),
        "maximum_matching_column_indices": list(matching),
        "residual_vertex_cover_number": tau,
        "residual_matching_number": nu,
        "matching_equality": tight,
        "matching_gap": tau - nu,
        "exact_repair_number": len(forced) + tau,
        "equality_certificate_payload_bits": (
            3 + tau * 7 if tight else None
        ),
    }
    if record["exact_audit"] != exact_audit:
        raise AssertionError("M97 exact audit changed")
    constructor = record["constructor"]
    if odd_cycle is None:
        if constructor.get("status") != "constructed_exact":
            raise AssertionError("M97 constructor status changed")
        left = constructor.get("left_type_ids")
        right = constructor.get("right_type_ids")
        constructed_matching = constructor.get(
            "maximum_matching_column_indices"
        )
        constructed_cover = constructor.get("minimum_cover_type_ids")
        if not all(
            isinstance(value, list)
            for value in (
                left,
                right,
                constructed_matching,
                constructed_cover,
            )
        ):
            raise AssertionError("M97 constructor list framing changed")
        validate_partition(unlooped, residual_edges, left, right)
        validate_matching(constructed_matching, residual_edges)
        validate_cover(constructed_cover, unlooped, residual_edges)
        if (
            len(constructed_matching) != nu
            or len(constructed_cover) != tau
            or len(constructed_matching) != len(constructed_cover)
        ):
            raise AssertionError("M97 constructor equality changed")
        expected_ledger = {
            "augmentations": nu,
            "augmenting_path_searches": nu + 1,
            "output_payload_bits": 3 + tau * 7,
            "output_verification_tests": len(residual_edges) + 2 * tau + 1,
        }
        for field, expected in expected_ledger.items():
            if constructor.get(field) != expected:
                raise AssertionError(f"M97 constructor {field} changed")
        payload_bits = 3 + tau * 7
        verification_tests = len(residual_edges) + 2 * tau + 1
        searches = nu + 1
    else:
        validate_odd_cycle(list(odd_cycle), target_edges)
        expected_constructor = {
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
        if constructor != expected_constructor:
            raise AssertionError("M97 nonbipartite constructor boundary changed")
        payload_bits = 0
        verification_tests = 0
        searches = 0
    return {
        "bipartite": odd_cycle is None,
        "matching_equality": tight,
        "residual_vertex_cover_number": tau,
        "residual_matching_number": nu,
        "exact_repair_number": len(forced) + tau,
        "matching_gap": tau - nu,
        "payload_bits": payload_bits,
        "verification_tests": verification_tests,
        "augmentations": nu if odd_cycle is None else 0,
        "searches": searches,
        "nonbipartite_equality_payload_bits": (
            3 + tau * 7 if odd_cycle is not None and tight else 0
        ),
    }


def validate_all(
    schema: Mapping[str, Any] | None = None,
) -> dict[str, int]:
    """Validate the full M97 constructive and boundary portfolio."""
    data = (
        json.loads(SCHEMA.read_text(encoding="utf-8"))
        if schema is None
        else dict(schema)
    )
    if data.get("schema_version") != "1.0.0":
        raise AssertionError("unsupported M97 schema version")
    if data.get("experiment_id") != "EXP-0068":
        raise AssertionError("M97 experiment ID changed")
    if data.get("claim_ids") != [
        "DEF-053",
        "THM-026",
        "REF-066",
        "EMP-068",
    ]:
        raise AssertionError("M97 claim registry changed")
    if data.get("source") != SOURCE_ANCHOR:
        raise AssertionError("M97 source anchor changed")
    if data.get("scope") != EXPECTED_SCOPE:
        raise AssertionError("M97 scope boundary changed")
    if data.get("summary_sha256") != canonical_hash(data):
        raise AssertionError("M97 canonical summary hash changed")
    _, slots = seed_from_source()
    expected_seed = {
        "type_ids": list(TYPE_IDS),
        "column_count": len(slots),
        "template_kind": "looped_clique",
        "slots": [
            {
                "column_index": column_index,
                "coverer_type_ids": list(slot),
            }
            for column_index, slot in enumerate(slots)
        ],
    }
    if data.get("seed") != expected_seed:
        raise AssertionError("M97 seed registry changed")
    if data.get("case_grammar") != expected_case_grammar():
        raise AssertionError("M97 case grammar changed")
    records = data.get("cases")
    specs = case_specs()
    if not isinstance(records, list) or len(records) != len(specs):
        raise AssertionError("M97 case count changed")
    loop_indices, edge_indices = slot_maps(slots)
    reports = [
        validate_case(
            record,
            slots,
            loop_indices,
            edge_indices,
            spec,
        )
        for record, spec in zip(records, specs, strict=True)
    ]
    bipartite = [report for report in reports if report["bipartite"]]
    nonbipartite = [
        report for report in reports if not report["bipartite"]
    ]
    totals = {
        "case_count": len(reports),
        "bipartite_case_count": len(bipartite),
        "nonbipartite_case_count": len(nonbipartite),
        "constructed_exact_count": len(bipartite),
        "nonbipartite_equality_count": sum(
            bool(report["matching_equality"]) for report in nonbipartite
        ),
        "matching_gap_count": sum(
            not bool(report["matching_equality"]) for report in reports
        ),
        "residual_vertex_cover_number_sum": sum(
            int(report["residual_vertex_cover_number"])
            for report in reports
        ),
        "residual_matching_number_sum": sum(
            int(report["residual_matching_number"])
            for report in reports
        ),
        "exact_repair_number_sum": sum(
            int(report["exact_repair_number"]) for report in reports
        ),
        "constructed_output_payload_bits": sum(
            int(report["payload_bits"]) for report in bipartite
        ),
        "constructed_output_verification_tests": sum(
            int(report["verification_tests"]) for report in bipartite
        ),
        "augmentations": sum(
            int(report["augmentations"]) for report in bipartite
        ),
        "augmenting_path_searches": sum(
            int(report["searches"]) for report in bipartite
        ),
        "nonbipartite_equality_payload_bits": sum(
            int(report["nonbipartite_equality_payload_bits"])
            for report in nonbipartite
        ),
        "maximum_matching_gap": max(
            int(report["matching_gap"]) for report in reports
        ),
    }
    if data.get("totals") != totals:
        raise AssertionError("M97 totals changed")
    return totals


def main() -> int:
    """Run the standalone M97 constructive checker."""
    totals = validate_all()
    print(
        "M97 bipartite-cover checker: PASS "
        f"({totals['case_count']} cases, "
        f"{totals['bipartite_case_count']} constructed repairs, "
        f"{totals['nonbipartite_equality_count']} nonbipartite equality, "
        f"{totals['matching_gap_count']} matching gap)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
