"""Audit public construction of the frozen M95 coverer graphs and OCT caps."""

from __future__ import annotations

import hashlib
import itertools
import json
import math
import sys
from collections.abc import Mapping
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts import check_m91_all_rows_semantic_certificate as m91

M50_PATH = ROOT / "schemas" / "m50-finite-threshold-summary-v1.json"
M92_PATH = ROOT / "schemas" / "m92-pair-cover-certificates-v1.json"
M93_PATH = ROOT / "schemas" / "m93-early-repair-certificates-v1.json"
M95_PATH = ROOT / "schemas" / "m95-coverer-graph-profile-v1.json"
M91_PATH = ROOT / "scripts" / "check_m91_all_rows_semantic_certificate.py"


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
    """Return the exact SHA-256 digest of one file."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def selector_descriptor_count(cap: int) -> int:
    """Count the exact public DEF-032 descriptor grammar."""
    phi4 = len(range(3, cap + 1, 4))
    phi6_first = len(range(5, cap + 1, 6))
    phi6_second = len(range(3, cap + 1, 6))
    return (cap - 1) * (
        phi4 * (phi4 - 1) + phi6_first * phi6_second
    )


def normalized_pattern(pattern: tuple[int, ...]) -> tuple[int, ...]:
    """Canonicalize one binary pattern modulo global complementation."""
    complement = tuple(1 - bit for bit in pattern)
    return min(pattern, complement)


def pair_indices(
    buckets: tuple[tuple[int, ...], ...],
) -> tuple[tuple[int, int], ...]:
    """Enumerate flattened within-bucket pairs."""
    pairs: list[tuple[int, int]] = []
    offset = 0
    for bucket in buckets:
        pairs.extend(
            (offset + left, offset + right)
            for left in range(len(bucket))
            for right in range(left + 1, len(bucket))
        )
        offset += len(bucket)
    return tuple(pairs)


def coverage_mask(
    pattern: tuple[int, ...],
    pairs: tuple[tuple[int, int], ...],
) -> int:
    """Encode the pairs separated by one binary pattern."""
    return sum(
        1 << index
        for index, (left, right) in enumerate(pairs)
        if pattern[left] != pattern[right]
    )


def public_coverage_types(
    base_cap: int,
    repair_cap: int,
    tracked_primes: tuple[int, ...],
    pairs: tuple[tuple[int, int], ...],
) -> tuple[dict[int, tuple[int, ...]], int]:
    """Enumerate every public newly admitted nonzero coverage type."""
    types: dict[int, tuple[int, ...]] = {}
    descriptor_count = 0
    for descriptor in m91.iter_selector_descriptors(repair_cap):
        if descriptor.cap <= base_cap:
            continue
        descriptor_count += 1
        primitive_masks = tuple(
            m91.primitive_exit_mask(descriptor, prime)
            for prime in tracked_primes
        )
        for kind_index in range(len(m91.EXIT_KINDS)):
            pattern = normalized_pattern(
                tuple(
                    (mask >> kind_index) & 1 for mask in primitive_masks
                )
            )
            mask = coverage_mask(pattern, pairs)
            if mask:
                types.setdefault(mask, pattern)
    return types, descriptor_count


def certificate_for(
    data: Mapping[str, Any],
    input_length: int,
) -> Mapping[str, Any]:
    """Select the public coordinate certificate for one frozen row."""
    direct = data.get("construction_certificate")
    if isinstance(direct, dict):
        return direct
    candidates = data.get("construction_certificates")
    if not isinstance(candidates, list):
        raise AssertionError("missing public construction certificate")
    matches = [
        candidate
        for candidate in candidates
        if isinstance(candidate, dict)
        and candidate.get("input_length") == input_length
    ]
    if len(matches) != 1:
        raise AssertionError("ambiguous public construction certificate")
    return matches[0]


def baseline_collision_partition(
    source_id: str,
    base_cap: int,
    repair_cap: int,
    population: tuple[int, ...],
    certificate: Mapping[str, Any],
) -> tuple[tuple[tuple[int, ...], ...], str, int, int, int]:
    """Derive exact baseline blocks without reading the M95 comparison."""
    source_names = tuple(str(item) for item in certificate["column_sources"])
    if len(set(source_names)) != len(source_names):
        raise AssertionError("public coordinate sources are not unique")
    parsed = tuple(
        m91.parse_source(source, repair_cap) for source in source_names
    )
    if source_id == "M92":
        selected = tuple(
            item for item in parsed if item[0].cap <= base_cap
        )
        signatures, selected_evaluations = (
            m91.stream_certificate_signatures(population, selected)
        )
        buckets = tuple(
            tuple(bucket)
            for bucket in m91.collision_buckets(population, signatures)
        )
        persistence_evaluations = m91.raw_buckets_persist(
            buckets,
            base_cap,
        )
        return (
            buckets,
            "selected-subfamily-plus-raw-persistence",
            len(selected),
            selected_evaluations,
            persistence_evaluations,
        )

    raw_buckets, raw_descriptor_evaluations = m91.raw_collision_buckets(
        population,
        base_cap,
    )
    return (
        tuple(tuple(bucket) for bucket in raw_buckets),
        "full-raw-family-refinement",
        selector_descriptor_count(base_cap) * len(m91.EXIT_KINDS),
        raw_descriptor_evaluations * len(m91.EXIT_KINDS),
        0,
    )


def construct_graph(
    masks_to_patterns: Mapping[int, tuple[int, ...]],
    tracked_primes: tuple[int, ...],
    pairs: tuple[tuple[int, int], ...],
) -> dict[str, Any]:
    """Construct every type, coverer column, loop, and residual edge."""
    width = max(1, math.ceil(len(pairs) / 4))
    sorted_masks = tuple(sorted(masks_to_patterns))
    type_ids = tuple(f"T{index}" for index in range(len(sorted_masks)))
    coverage_types = [
        {
            "type_id": type_id,
            "pattern": list(masks_to_patterns[mask]),
            "coverage_mask_hex": f"{mask:0{width}x}",
        }
        for type_id, mask in zip(type_ids, sorted_masks, strict=True)
    ]
    coverer_sets: list[dict[str, Any]] = []
    for pair_index, (left, right) in enumerate(pairs):
        coverers = [
            type_id
            for type_id, mask in zip(type_ids, sorted_masks, strict=True)
            if (mask >> pair_index) & 1
        ]
        if not 1 <= len(coverers) <= 2:
            raise AssertionError("public coverer column rank is outside 1..2")
        coverer_sets.append(
            {
                "pair_index": pair_index,
                "pair": [tracked_primes[left], tracked_primes[right]],
                "coverer_type_ids": coverers,
            }
        )
    forced = tuple(
        type_id
        for type_id in type_ids
        if any(
            column["coverer_type_ids"] == [type_id]
            for column in coverer_sets
        )
    )
    vertices = tuple(
        type_id for type_id in type_ids if type_id not in set(forced)
    )
    edges: tuple[tuple[str, ...], ...] = tuple(
        tuple(column["coverer_type_ids"])
        for column in coverer_sets
        if len(column["coverer_type_ids"]) == 2
        and not set(forced).intersection(column["coverer_type_ids"])
    )
    degree_histogram: dict[str, int] = {}
    for column in coverer_sets:
        key = str(len(column["coverer_type_ids"]))
        degree_histogram[key] = degree_histogram.get(key, 0) + 1
    return {
        "coverage_types": coverage_types,
        "coverer_sets": coverer_sets,
        "column_degree_histogram": degree_histogram,
        "coverer_incidence_count": sum(
            len(column["coverer_type_ids"]) for column in coverer_sets
        ),
        "forced_type_ids": forced,
        "residual_vertex_ids": vertices,
        "residual_edges": edges,
    }


def compare_to_m95(
    graph: Mapping[str, Any],
    constructed: Mapping[str, Any],
) -> None:
    """Use M95 only as a label-invariant post-construction oracle."""
    derived_keys = {
        str(record["type_id"]): tuple(
            sorted(
                tuple(int(prime) for prime in column["pair"])
                for column in constructed["coverer_sets"]
                if record["type_id"] in column["coverer_type_ids"]
            )
        )
        for record in constructed["coverage_types"]
    }
    comparison_keys = {
        str(record["type_id"]): tuple(
            sorted(
                tuple(int(prime) for prime in column["pair"])
                for column in graph["coverer_sets"]
                if record["type_id"] in column["coverer_type_ids"]
            )
        )
        for record in graph["coverage_types"]
    }
    if set(derived_keys.values()) != set(comparison_keys.values()):
        raise AssertionError("M95 coverage-type semantics changed")

    derived_columns = {
        tuple(int(prime) for prime in record["pair"]): tuple(
            sorted(derived_keys[str(type_id)] for type_id in record[
                "coverer_type_ids"
            ])
        )
        for record in constructed["coverer_sets"]
    }
    comparison_columns = {
        tuple(int(prime) for prime in record["pair"]): tuple(
            sorted(comparison_keys[str(type_id)] for type_id in record[
                "coverer_type_ids"
            ])
        )
        for record in graph["coverer_sets"]
    }
    if derived_columns != comparison_columns:
        raise AssertionError("M95 coverer-column semantics changed")
    derived_forced = {
        derived_keys[str(type_id)]
        for type_id in constructed["forced_type_ids"]
    }
    comparison_forced = {
        comparison_keys[str(type_id)] for type_id in graph["looped_type_ids"]
    }
    if derived_forced != comparison_forced:
        raise AssertionError("M95 forced-loop semantics changed")
    if constructed["column_degree_histogram"] != graph[
        "column_degree_histogram"
    ]:
        raise AssertionError("M95 coverer degree histogram changed")
    if constructed["coverer_incidence_count"] != graph[
        "coverer_incidence_count"
    ]:
        raise AssertionError("M95 coverer incidence count changed")


def minimum_oct(
    vertices: tuple[str, ...],
    edges: tuple[tuple[str, str], ...],
) -> tuple[str, ...]:
    """Return the lexicographically first minimum OCT by bounded defense."""

    def bipartite_after(deleted: set[str]) -> bool:
        adjacency: dict[str, set[str]] = {
            vertex: set() for vertex in vertices if vertex not in deleted
        }
        for left, right in edges:
            if left in deleted or right in deleted:
                continue
            if left == right:
                return False
            adjacency[left].add(right)
            adjacency[right].add(left)
        colors: dict[str, int] = {}
        for start in adjacency:
            if start in colors:
                continue
            colors[start] = 0
            stack = [start]
            while stack:
                current = stack.pop()
                for neighbor in adjacency[current]:
                    expected = 1 - colors[current]
                    if neighbor in colors:
                        if colors[neighbor] != expected:
                            return False
                    else:
                        colors[neighbor] = expected
                        stack.append(neighbor)
        return True

    for size in range(len(vertices) + 1):
        for chosen in itertools.combinations(vertices, size):
            if bipartite_after(set(chosen)):
                return chosen
    raise AssertionError("finite graph has no OCT")


def public_oct_cap(input_length: int) -> int:
    """Return the public schedule ceil(log2(m))."""
    if input_length < 2:
        raise ValueError("input length must be at least two")
    return (input_length - 1).bit_length()


def source_caps(source_id: str, source: Mapping[str, Any]) -> tuple[int, int]:
    """Project the public base and repair caps from M92/M93."""
    if source_id == "M92":
        return int(source["base_cap"]), int(source["repair_cap"])
    repair_cap = int(source["repair_cap"])
    return repair_cap - 1, repair_cap


def source_anchors() -> list[dict[str, Any]]:
    """Bind every semantic layer used by the public reconstruction."""
    specs = (
        (
            "M50",
            M50_PATH,
            "public finite row, cap, and source registry",
            "EMP-062",
        ),
        (
            "M91",
            M91_PATH,
            "factor-independent population and collision completeness checker",
            "EMP-062",
        ),
        (
            "M92",
            M92_PATH,
            "late repair caps and comparison type systems",
            "EMP-063",
        ),
        (
            "M93",
            M93_PATH,
            "early repair caps and comparison type systems",
            "EMP-064",
        ),
        (
            "M95",
            M95_PATH,
            "comparison-only coverer graphs",
            "EMP-066",
        ),
    )
    records = []
    for source_id, path, role, claim_id in specs:
        record: dict[str, Any] = {
            "source_id": source_id,
            "path": str(path.relative_to(ROOT)).replace("\\", "/"),
            "file_sha256": file_sha256(path),
            "role": role,
            "semantic_dependency": claim_id,
        }
        if path.suffix == ".json":
            data = json.loads(path.read_text(encoding="utf-8"))
            if "summary_sha256" in data:
                record["summary_sha256"] = str(data["summary_sha256"])
        records.append(record)
    return records


def build_instance(
    source_id: str,
    input_length: int,
    graph: Mapping[str, Any],
    source: Mapping[str, Any],
    m50_row: Mapping[str, Any],
    source_artifact: Mapping[str, Any],
) -> dict[str, Any]:
    """Construct one factor-independent frozen graph audit record."""
    if (
        graph["source_id"] != source_id
        or graph["input_length"] != input_length
    ):
        raise AssertionError("M95 comparison identity changed")
    base_cap, repair_cap = source_caps(source_id, source)
    population = m91.balanced_prime_population(input_length)
    if len(population) != int(m50_row["population_size"]):
        raise AssertionError("public balanced population changed")
    certificate = certificate_for(source_artifact, input_length)
    certificate_primes = tuple(int(prime) for prime in certificate["primes"])
    if certificate_primes != population:
        raise AssertionError("public certificate prime registry changed")
    (
        buckets,
        baseline_mode,
        selected_coordinate_count,
        selected_evaluations,
        persistence_descriptor_evaluations,
    ) = baseline_collision_partition(
        source_id,
        base_cap,
        repair_cap,
        population,
        certificate,
    )
    comparison_buckets = tuple(
        tuple(int(prime) for prime in bucket)
        for bucket in graph["collision_buckets"]
    )
    if tuple(sorted(buckets)) != tuple(sorted(comparison_buckets)):
        raise AssertionError(
            f"length {input_length} M95 collision buckets changed: "
            f"{buckets!r} != {graph['collision_buckets']!r}"
        )
    tracked_primes = tuple(prime for bucket in buckets for prime in bucket)
    pairs = pair_indices(buckets)
    public_types, descriptor_count = public_coverage_types(
        base_cap,
        repair_cap,
        tracked_primes,
        pairs,
    )
    expected_descriptor_count = (
        selector_descriptor_count(repair_cap)
        - selector_descriptor_count(base_cap)
    )
    if descriptor_count != expected_descriptor_count:
        raise AssertionError("new descriptor count changed")
    constructed = construct_graph(public_types, tracked_primes, pairs)
    compare_to_m95(graph, constructed)
    residual_vertices = constructed["residual_vertex_ids"]
    residual_edges = constructed["residual_edges"]
    optimum_oct = minimum_oct(residual_vertices, residual_edges)
    cap = public_oct_cap(input_length)
    if len(optimum_oct) > cap:
        raise AssertionError("public logarithmic cap rejected a frozen graph")

    return {
        "source_id": source_id,
        "input_length": input_length,
        "source_schema": str(m50_row["source_schema"]),
        "source_schema_sha256": file_sha256(
            ROOT / str(m50_row["source_schema"])
        ),
        "base_cap": base_cap,
        "repair_cap": repair_cap,
        "population_size": len(population),
        "population_label_bits": sum(prime.bit_length() for prime in population),
        "baseline_partition_mode": baseline_mode,
        "baseline_collision_buckets": [list(bucket) for bucket in buckets],
        "selected_coordinate_count": selected_coordinate_count,
        "selected_certificate_evaluations": selected_evaluations,
        "baseline_persistence_descriptor_evaluations": (
            persistence_descriptor_evaluations
        ),
        "baseline_persistence_primitive_tests": (
            persistence_descriptor_evaluations * len(m91.EXIT_KINDS)
        ),
        "tracked_point_count": len(tracked_primes),
        "pair_count": len(pairs),
        "new_descriptor_count": descriptor_count,
        "new_descriptor_prime_evaluations": descriptor_count
        * len(tracked_primes),
        "primitive_coordinate_tests": descriptor_count
        * len(tracked_primes)
        * len(m91.EXIT_KINDS),
        "complete_type_count": len(public_types),
        "complete_coverage_masks_hex": [
            f"{mask:0{max(1, math.ceil(len(pairs) / 4))}x}"
            for mask in sorted(public_types)
        ],
        "coverage_types": constructed["coverage_types"],
        "coverer_sets": constructed["coverer_sets"],
        "coverer_rank": max(
            len(record["coverer_type_ids"])
            for record in constructed["coverer_sets"]
        ),
        "forced_type_ids": list(constructed["forced_type_ids"]),
        "forced_type_count": len(constructed["forced_type_ids"]),
        "residual_vertex_ids": list(residual_vertices),
        "residual_vertex_count": len(residual_vertices),
        "residual_edges": [list(edge) for edge in residual_edges],
        "residual_edge_count": len(residual_edges),
        "public_oct_cap": cap,
        "exact_oct_number": len(optimum_oct),
        "exact_oct_type_ids": list(optimum_oct),
        "within_public_oct_cap": True,
        "graph_payload_bits": int(
            graph["verification_cost"]["abstract_certificate_payload_bits"]
        ),
    }


def hash_only_counterexample() -> dict[str, Any]:
    """Show that a self-consistent digest cannot prove type completeness."""
    claimed = {
        "universe": ["u0", "u1"],
        "claimed_types": {"T0": ["u0"], "T1": ["u1"]},
        "claimed_exact_cover_number": 2,
    }
    omitted = {"T2": ["u0", "u1"]}
    digest = hashlib.sha256(
        json.dumps(
            claimed,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()
    return {
        "claimed_payload": claimed,
        "recomputed_sha256": digest,
        "omitted_realized_type": omitted,
        "actual_exact_cover_number": 1,
        "conclusion": (
            "the digest binds the claimed bytes but does not prove that "
            "the realized type family is complete"
        ),
    }


def build_summary() -> dict[str, Any]:
    """Build the canonical M100 public graph-construction audit."""
    m50 = json.loads(M50_PATH.read_text(encoding="utf-8"))
    m92 = json.loads(M92_PATH.read_text(encoding="utf-8"))
    m93 = json.loads(M93_PATH.read_text(encoding="utf-8"))
    m95 = json.loads(M95_PATH.read_text(encoding="utf-8"))
    source_instances = {
        (source_id, int(instance["input_length"])): instance
        for source_id, data in (("M92", m92), ("M93", m93))
        for instance in data["instances"]
    }
    m50_rows = {
        int(row["input_length"]): row for row in m50["rows"]
    }
    comparison_graphs = {
        (str(graph["source_id"]), int(graph["input_length"])): graph
        for graph in m95["instances"]
    }
    source_cache: dict[str, Mapping[str, Any]] = {}
    instances = []
    for input_length in range(16, 35):
        source_id = "M92" if input_length >= 26 else "M93"
        row = m50_rows[input_length]
        path = str(row["source_schema"])
        if path not in source_cache:
            source_cache[path] = json.loads(
                (ROOT / path).read_text(encoding="utf-8")
            )
        instances.append(
            build_instance(
                source_id,
                input_length,
                comparison_graphs[(source_id, input_length)],
                source_instances[(source_id, input_length)],
                row,
                source_cache[path],
            )
        )

    summed = (
        "population_size",
        "population_label_bits",
            "selected_coordinate_count",
            "selected_certificate_evaluations",
            "baseline_persistence_descriptor_evaluations",
            "baseline_persistence_primitive_tests",
        "tracked_point_count",
        "pair_count",
        "new_descriptor_count",
        "new_descriptor_prime_evaluations",
        "primitive_coordinate_tests",
        "complete_type_count",
        "forced_type_count",
        "residual_vertex_count",
        "residual_edge_count",
        "public_oct_cap",
        "exact_oct_number",
        "graph_payload_bits",
    )
    summary: dict[str, Any] = {
        "schema_version": "1.0.0",
        "experiment_id": "EXP-0071",
        "claim_ids": ["DEF-056", "THM-029", "REF-069", "EMP-071"],
        "sources": source_anchors(),
        "constructor_contract": {
            "public_inputs": [
                "input length m",
                "public balanced-prime predicate",
                "public DEF-032 selector grammar and base/repair caps",
                "public selected-coordinate collision-completeness certificate",
            ],
            "forbidden_advice": [
                "hidden factors of the integer input",
                "precomputed baseline collision blocks or tracked point labels",
                "precomputed complete coverage types",
                "precomputed coverer edges",
                "a per-instance OCT cap",
            ],
            "steps": [
                "enumerate and verify the complete balanced-prime population",
                "derive exact base collisions from public baseline coordinates",
                "enumerate every newly admitted public primitive coordinate",
                "deduplicate nonzero pair-coverage masks into complete types",
                "construct coverer columns, forced loops, and the residual graph",
                "compare the completed construction to the frozen M95 oracle",
                "derive k(m)=ceil(log2(m)) and run capped OCT discovery",
            ],
            "explicit_size_cost": (
                "O(P+C*n*E+D0*b*E+D1*b*E+t*(b+q)"
                "+3^k*k*t*(t+q))"
            ),
            "symbols": {
                "P": "public population enumeration and representation cost",
                "n": "public population cardinality",
                "C": "selected completeness-certificate coordinates",
                "D0": "base public descriptors checked on candidate buckets",
                "D1": "new public descriptors used to form coverage types",
                "b": "tracked collision points",
                "E": (
                    "cost bound for one selected coordinate or one "
                    "eight-exit descriptor evaluation"
                ),
                "t": "complete nonzero coverage types",
                "q": "unresolved within-bucket pairs",
                "k": "public OCT cap ceil(log2(m))",
            },
        },
        "public_oct_schedule": {
            "formula": "ceil(log2(m))",
            "depends_only_on": "input length m",
            "application_status": "EMPIRICAL for the frozen lengths 16 through 34",
            "asymptotic_status": "OPEN for future coverer graphs",
        },
        "instances": instances,
        "totals": {
            "instance_count": len(instances),
            **{
                field: sum(int(instance[field]) for instance in instances)
                for field in summed
            },
            "maximum_exact_oct_number": max(
                int(instance["exact_oct_number"]) for instance in instances
            ),
            "all_public_caps_accepted": all(
                bool(instance["within_public_oct_cap"])
                for instance in instances
            ),
        },
        "hash_only_counterexample": hash_only_counterexample(),
        "boundary": {
            "registered_path_is_factor_independent": True,
            "registered_path_is_polynomial_in_explicit_artifacts": True,
            "registered_path_is_polynomial_in_m": False,
            "reason": (
                "the registered verifier explicitly enumerates P_m; "
                "BAR-041 gives |P_m|=Omega(2^(m/2)/m)"
            ),
            "compact_graph_hash_proves_semantic_completeness": False,
            "hidden_input_to_population_vertex_map": (
                "not needed for offline public graph construction, but "
                "recognizing an arbitrary input's balanced-semiprime promise "
                "and obtaining a general asymptotic graph/cap law remain open"
            ),
        },
        "scope": {
            "classification": "EMPIRICAL",
            "finite_input_lengths": list(range(16, 35)),
            "not_claimed": [
                "a bit-polynomial graph constructor for unbounded m",
                "an asymptotic logarithmic OCT theorem",
                "a factor-promise recognizer",
                "a result for another selector grammar",
                "a lower bound against all compact completeness proofs",
                "general classical polynomial-time factoring",
            ],
        },
    }
    summary["summary_sha256"] = canonical_hash(summary)
    return summary


def main() -> int:
    """Run the deterministic M100 audit."""
    summary = build_summary()
    totals = summary["totals"]
    print(
        "M100 public coverer-graph audit: PASS "
        f"({totals['instance_count']} instances, "
        f"{totals['complete_type_count']} complete types, "
        f"{totals['primitive_coordinate_tests']} primitive tests, "
        f"max OCT {totals['maximum_exact_oct_number']})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
