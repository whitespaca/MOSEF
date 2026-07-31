"""Independently validate the M96 matching-equality certificates."""

from __future__ import annotations

import hashlib
import itertools
import json
from collections.abc import Iterable, Mapping
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas" / "m96-matching-certificates-v1.json"
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
    "synthetic_perturbations": True,
    "not_claimed": [
        "a factor-promise recognizer",
        "a polynomial algorithm for arbitrary vertex cover",
        "matching equality for every residual coverer graph",
        "an asymptotic selector theorem",
        "general classical polynomial-time factoring",
    ],
}


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


def perturbation_specs() -> tuple[tuple[int, bool], ...]:
    """Return the hard-coded bounded perturbation registry."""
    return (
        (1, False),
        (2, False),
        (2, True),
        (3, False),
        (3, True),
        (4, False),
        (4, True),
        (5, True),
    )


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
    raise AssertionError("residual graph has no vertex cover")


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
        raise AssertionError("M96 source file hash changed")
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    if source.get("summary_sha256") != SOURCE_ANCHOR["summary_sha256"]:
        raise AssertionError("M96 source summary hash changed")
    if canonical_hash(source) != SOURCE_ANCHOR["summary_sha256"]:
        raise AssertionError("M96 source content changed")
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
        raise AssertionError("M96 seed instance changed")
    slots = tuple(
        tuple(str(type_id) for type_id in record["coverer_type_ids"])
        for record in seed["coverer_sets"]
    )
    if len(slots) != 15 or sorted(slots) != sorted(
        template_slots("looped_clique")
    ):
        raise AssertionError("M96 seed is not looped K5")
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
            edges[(slot[0], slot[1])] = column_index
        else:
            raise AssertionError("M96 seed rank changed")
    if set(loops) != set(TYPE_IDS) or set(edges) != set(
        itertools.combinations(TYPE_IDS, 2)
    ):
        raise AssertionError("M96 seed slot registry changed")
    return loops, edges


def validate_perturbation(
    record: Mapping[str, Any],
    slots: tuple[tuple[str, ...], ...],
    loop_indices: Mapping[str, int],
    edge_indices: Mapping[tuple[str, str], int],
    unlooped_count: int,
    delete_edge: bool,
) -> dict[str, int | bool]:
    """Validate one registered perturbation and both witnesses."""
    unlooped = TYPE_IDS[:unlooped_count]
    forced = TYPE_IDS[unlooped_count:]
    expected_id = (
        f"U{unlooped_count}-"
        + ("drop-e01" if delete_edge else "keep-edges")
    )
    scalar = {
        "perturbation_id": expected_id,
        "unlooped_type_ids": list(unlooped),
        "forced_type_ids": list(forced),
        "deleted_loop_column_indices": [
            loop_indices[type_id] for type_id in unlooped
        ],
        "deleted_edge_column_indices": (
            [edge_indices[("T0", "T1")]] if delete_edge else []
        ),
        "complete_normal_form": True,
        "m95_template": False,
    }
    for field, expected in scalar.items():
        if record.get(field) != expected:
            raise AssertionError(f"M96 {field} changed")
    deleted = {
        int(index)
        for field in (
            "deleted_loop_column_indices",
            "deleted_edge_column_indices",
        )
        for index in record[field]
    }
    retained = tuple(
        slot
        for column_index, slot in enumerate(slots)
        if column_index not in deleted
    )
    if int(record["retained_column_count"]) != len(retained):
        raise AssertionError("M96 retained column count changed")
    if not complete_normal_form(retained):
        raise AssertionError("M96 complete normal form failed")
    if is_m95_template(retained):
        raise AssertionError("M96 perturbation became an M95 template")
    residual_edges = tuple(
        (column_index, (slot[0], slot[1]))
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
        raise AssertionError("M96 residual edges changed")
    cover = minimum_vertex_cover(unlooped, residual_edges)
    matching = maximum_matching(residual_edges)
    if record["minimum_cover_type_ids"] != list(cover):
        raise AssertionError("M96 minimum cover witness changed")
    if record["maximum_matching_column_indices"] != list(matching):
        raise AssertionError("M96 maximum matching witness changed")
    tau = len(cover)
    nu = len(matching)
    tight = tau == nu
    expected_numbers = {
        "residual_vertex_cover_number": tau,
        "residual_matching_number": nu,
        "matching_equality": tight,
        "matching_gap": tau - nu,
        "exact_repair_number": len(forced) + tau,
        "matching_lower_bound": len(forced) + nu,
    }
    for field, expected in expected_numbers.items():
        if record[field] != expected:
            raise AssertionError(f"M96 {field} changed")
    type_bits = 3
    column_bits = 4
    size_bits = 3
    certificate = {
        "status": "exact" if tight else "insufficient",
        "type_index_bits": type_bits,
        "column_index_bits": column_bits,
        "witness_size_bits": size_bits,
        "witness_size": tau if tight else None,
        "payload_bits": (
            size_bits + tau * (type_bits + column_bits)
            if tight
            else None
        ),
        "verification_tests": (
            len(residual_edges) + 2 * tau + 1 if tight else None
        ),
    }
    if record["matching_certificate"] != certificate:
        raise AssertionError("M96 matching certificate cost changed")
    return {
        "matching_equality": tight,
        "residual_vertex_cover_number": tau,
        "residual_matching_number": nu,
        "exact_repair_number": len(forced) + tau,
        "matching_gap": tau - nu,
        "payload_bits": int(certificate["payload_bits"] or 0),
        "verification_tests": int(certificate["verification_tests"] or 0),
    }


def validate_all(
    schema: Mapping[str, Any] | None = None,
) -> dict[str, int]:
    """Validate the full M96 certificate and counterexample portfolio."""
    data = (
        json.loads(SCHEMA.read_text(encoding="utf-8"))
        if schema is None
        else dict(schema)
    )
    if data.get("schema_version") != "1.0.0":
        raise AssertionError("unsupported M96 schema version")
    if data.get("experiment_id") != "EXP-0067":
        raise AssertionError("M96 experiment ID changed")
    if data.get("claim_ids") != [
        "DEF-052",
        "THM-025",
        "REF-065",
        "EMP-067",
    ]:
        raise AssertionError("M96 claim registry changed")
    if data.get("source") != SOURCE_ANCHOR:
        raise AssertionError("M96 source anchor changed")
    if data.get("scope") != EXPECTED_SCOPE:
        raise AssertionError("M96 scope boundary changed")
    if data.get("summary_sha256") != canonical_hash(data):
        raise AssertionError("M96 canonical summary hash changed")
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
        raise AssertionError("M96 seed registry changed")
    specs = perturbation_specs()
    expected_grammar = {
        "operation": (
            "delete the loops on T0,...,T(r-1), then optionally "
            "delete edge {T0,T1}"
        ),
        "registered_parameters": [
            {
                "unlooped_count": unlooped_count,
                "delete_edge_t0_t1": delete_edge,
            }
            for unlooped_count, delete_edge in specs
        ],
    }
    if data.get("perturbation_grammar") != expected_grammar:
        raise AssertionError("M96 perturbation grammar changed")
    records = data.get("perturbations")
    if not isinstance(records, list) or len(records) != len(specs):
        raise AssertionError("M96 perturbation count changed")
    loop_indices, edge_indices = slot_maps(slots)
    reports = [
        validate_perturbation(
            record,
            slots,
            loop_indices,
            edge_indices,
            unlooped_count,
            delete_edge,
        )
        for record, (unlooped_count, delete_edge) in zip(
            records,
            specs,
            strict=True,
        )
    ]
    totals = {
        "perturbation_count": len(reports),
        "matching_equality_count": sum(
            bool(report["matching_equality"]) for report in reports
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
        "matching_certificate_payload_bits": sum(
            int(report["payload_bits"]) for report in reports
        ),
        "matching_certificate_verification_tests": sum(
            int(report["verification_tests"]) for report in reports
        ),
        "maximum_matching_gap": max(
            int(report["matching_gap"]) for report in reports
        ),
    }
    if data.get("totals") != totals:
        raise AssertionError("M96 totals changed")
    return totals


def main() -> int:
    """Run the standalone M96 matching-certificate checker."""
    totals = validate_all()
    print(
        "M96 matching-certificate checker: PASS "
        f"({totals['perturbation_count']} perturbations, "
        f"{totals['matching_equality_count']} equality certificates, "
        f"{totals['matching_gap_count']} matching gaps, "
        f"{totals['matching_certificate_payload_bits']} witness bits)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
