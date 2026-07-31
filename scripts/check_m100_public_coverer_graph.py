"""Independently validate the M100 public coverer-graph construction audit."""

from __future__ import annotations

import hashlib
import itertools
import json
import math
from collections.abc import Iterator, Mapping
from functools import cache
from math import isqrt
from pathlib import Path
from typing import Any, NamedTuple

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas" / "m100-public-coverer-graph-v1.json"
M50_PATH = ROOT / "schemas" / "m50-finite-threshold-summary-v1.json"
M91_PATH = ROOT / "scripts" / "check_m91_all_rows_semantic_certificate.py"
M92_PATH = ROOT / "schemas" / "m92-pair-cover-certificates-v1.json"
M93_PATH = ROOT / "schemas" / "m93-early-repair-certificates-v1.json"
M95_PATH = ROOT / "schemas" / "m95-coverer-graph-profile-v1.json"
EXIT_KINDS = (
    "base",
    "first_stage",
    "second_stage",
    "first_public_bound",
    "second_public_bound",
    "cyclotomic",
    "overlap_resultant",
    "cofactor",
)
EXIT_COUNT = len(EXIT_KINDS)
INSTANCE_CACHE: dict[tuple[str, int], dict[str, Any]] = {}


class Descriptor(NamedTuple):
    """One public DEF-032 descriptor."""

    family: str
    first: int
    second: int
    base: int

    @property
    def cap(self) -> int:
        """Return the first cap admitting this descriptor."""
        return max(self.first, self.second, self.base)


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


def balanced_population(input_length: int) -> tuple[int, ...]:
    """Enumerate the public primes p with 2^(m-1) <= p^2 < 2^m."""
    lower_square = 1 << (input_length - 1)
    lower = isqrt(lower_square)
    if lower * lower < lower_square:
        lower += 1
    upper = isqrt((1 << input_length) - 1)
    flags = bytearray(b"\x01") * (upper + 1)
    flags[:2] = b"\x00\x00"
    for candidate in range(2, isqrt(upper) + 1):
        if not flags[candidate]:
            continue
        start = candidate * candidate
        count = (upper - start) // candidate + 1
        flags[start : upper + 1 : candidate] = b"\x00" * count
    return tuple(
        candidate for candidate in range(lower, upper + 1) if flags[candidate]
    )


def iter_descriptors(cap: int) -> Iterator[Descriptor]:
    """Enumerate the exact public descriptor grammar."""
    for first in range(3, cap + 1, 4):
        for second in range(3, cap + 1, 4):
            if first == second:
                continue
            for base in range(2, cap + 1):
                yield Descriptor("phi4", first, second, base)
    for first in range(5, cap + 1, 6):
        for second in range(3, cap + 1, 6):
            for base in range(2, cap + 1):
                yield Descriptor("phi6", first, second, base)


def descriptor_count(cap: int) -> int:
    """Count the descriptor grammar without enumerating it."""
    phi4 = len(range(3, cap + 1, 4))
    phi6_first = len(range(5, cap + 1, 6))
    phi6_second = len(range(3, cap + 1, 6))
    return (cap - 1) * (
        phi4 * (phi4 - 1) + phi6_first * phi6_second
    )


def descriptor_is_valid(descriptor: Descriptor, cap: int) -> bool:
    """Check the exact public descriptor grammar."""
    if not (
        2 <= descriptor.first <= cap
        and 2 <= descriptor.second <= cap
        and 2 <= descriptor.base <= cap
        and descriptor.first != descriptor.second
    ):
        return False
    if descriptor.family == "phi4":
        return descriptor.first % 4 == 3 and descriptor.second % 4 == 3
    return (
        descriptor.family == "phi6"
        and descriptor.first % 6 == 5
        and descriptor.second % 6 == 3
    )


def parse_source(source: str, cap: int) -> tuple[Descriptor, int]:
    """Parse one canonical selected-coordinate source independently."""
    parts = source.split(":")
    if len(parts) != 5:
        raise AssertionError("noncanonical coordinate source")
    family, first, second, base, kind = parts
    try:
        descriptor = Descriptor(family, int(first), int(second), int(base))
    except ValueError as exc:
        raise AssertionError("noninteger coordinate source") from exc
    if not descriptor_is_valid(descriptor, cap) or kind not in EXIT_KINDS:
        raise AssertionError("coordinate source is outside the public grammar")
    canonical = (
        f"{descriptor.family}:{descriptor.first}:"
        f"{descriptor.second}:{descriptor.base}:{kind}"
    )
    if source != canonical:
        raise AssertionError("noncanonical coordinate source")
    return descriptor, EXIT_KINDS.index(kind)


def geometric_sum(base: int, count: int, prime: int) -> int:
    """Evaluate a geometric sum modulo a prime."""
    base %= prime
    if base == 1:
        return count % prime
    return (
        (pow(base, count, prime) - 1) * pow(base - 1, -1, prime)
    ) % prime


def geometric_derivative(base: int, count: int, prime: int) -> int:
    """Evaluate the derivative of a geometric sum modulo a prime."""
    base %= prime
    if base == 1:
        return count * (count - 1) // 2 % prime
    denominator = (base - 1) % prime
    numerator = (
        count * pow(base, count - 1, prime) * denominator
        - (pow(base, count, prime) - 1)
    )
    return numerator * pow(denominator * denominator % prime, -1, prime) % prime


def overlap_resultant(descriptor: Descriptor) -> int:
    """Reconstruct the exact exceptional resultant."""
    first = descriptor.first
    second = descriptor.second
    if descriptor.family == "phi4":
        constant_numerator = first * (second + 2) + 1
        linear_numerator = first * (second - 2) + 1
        if constant_numerator % 4 or linear_numerator % 4:
            raise AssertionError("nonintegral phi4 coefficients")
        constant = constant_numerator // 4
        linear = linear_numerator // 4
        return constant * constant + linear * linear
    residual = first * (second - 2) + 1
    linear_numerator = first * (second + 4) + 4
    if (2 * residual) % 3 or linear_numerator % 3:
        raise AssertionError("nonintegral phi6 coefficients")
    constant = -(2 * residual // 3)
    linear = linear_numerator // 3
    return constant * constant + constant * linear + linear * linear


def cyclotomic_residue(descriptor: Descriptor, prime: int) -> int:
    """Evaluate the applicable quadratic cyclotomic polynomial."""
    base = descriptor.base % prime
    if descriptor.family == "phi4":
        return (base * base + 1) % prime
    return (base * base - base + 1) % prime


def cofactor_residue(descriptor: Descriptor, prime: int) -> int:
    """Evaluate the exceptional quotient, including simple roots."""
    first = descriptor.first
    second = descriptor.second
    base = descriptor.base % prime
    nested_base = pow(base, first, prime)
    coefficient = 1 if descriptor.family == "phi4" else 2
    aggregate = (
        coefficient * geometric_sum(base, first, prime)
        + geometric_sum(nested_base, second, prime)
    ) % prime
    cyclotomic = cyclotomic_residue(descriptor, prime)
    if cyclotomic:
        return aggregate * pow(cyclotomic, -1, prime) % prime
    if aggregate:
        raise AssertionError("exceptional factorization changed")
    derivative = (
        coefficient * geometric_derivative(base, first, prime)
        + first
        * pow(base, first - 1, prime)
        * geometric_derivative(nested_base, second, prime)
    ) % prime
    cyclotomic_derivative = (
        2 * base
        if descriptor.family == "phi4"
        else 2 * base - 1
    ) % prime
    if not cyclotomic_derivative:
        raise AssertionError("cyclotomic root is not simple")
    return derivative * pow(cyclotomic_derivative, -1, prime) % prime


def primitive_mask(descriptor: Descriptor, prime: int) -> int:
    """Evaluate all eight public primitive exit bits."""
    base = descriptor.base % prime
    if base == 0:
        return 1
    first_power = pow(base, descriptor.first, prime)
    coefficient = 1 if descriptor.family == "phi4" else 2
    hits = (
        False,
        geometric_sum(base, descriptor.first, prime) == 0,
        geometric_sum(first_power, descriptor.second, prime) == 0,
        descriptor.second % prime == 0,
        coefficient * descriptor.second % prime == 0,
        cyclotomic_residue(descriptor, prime) == 0,
        overlap_resultant(descriptor) % prime == 0,
        cofactor_residue(descriptor, prime) == 0,
    )
    return sum(1 << index for index, hit in enumerate(hits) if hit)


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


def pattern_coverage(
    pattern: tuple[int, ...],
    pairs: tuple[tuple[int, int], ...],
) -> int:
    """Encode every pair separated by a binary pattern."""
    return sum(
        1 << index
        for index, (left, right) in enumerate(pairs)
        if pattern[left] != pattern[right]
    )


def normalized_pattern(pattern: tuple[int, ...]) -> tuple[int, ...]:
    """Canonicalize a binary point pattern modulo complementation."""
    complement = tuple(1 - bit for bit in pattern)
    return min(pattern, complement)


def public_type_masks(
    base_cap: int,
    repair_cap: int,
    tracked: tuple[int, ...],
    pairs: tuple[tuple[int, int], ...],
) -> tuple[dict[int, tuple[int, ...]], int]:
    """Independently enumerate every nonzero public coverage type."""
    masks: dict[int, tuple[int, ...]] = {}
    observed_descriptors = 0
    for descriptor in iter_descriptors(repair_cap):
        if descriptor.cap <= base_cap:
            continue
        observed_descriptors += 1
        exits = tuple(primitive_mask(descriptor, prime) for prime in tracked)
        for kind_index in range(EXIT_COUNT):
            pattern = normalized_pattern(
                tuple((value >> kind_index) & 1 for value in exits)
            )
            coverage = pattern_coverage(pattern, pairs)
            if coverage:
                masks.setdefault(coverage, pattern)
    return masks, observed_descriptors


def certificate_for(
    data: Mapping[str, Any],
    input_length: int,
) -> Mapping[str, Any]:
    """Select one public coordinate certificate."""
    direct = data.get("construction_certificate")
    if isinstance(direct, dict):
        return direct
    candidates = data.get("construction_certificates")
    if not isinstance(candidates, list):
        raise AssertionError("missing construction certificate")
    matches = [
        item
        for item in candidates
        if isinstance(item, dict) and item.get("input_length") == input_length
    ]
    if len(matches) != 1:
        raise AssertionError("ambiguous construction certificate")
    return matches[0]


def collision_buckets(
    population: tuple[int, ...],
    signatures: tuple[int, ...],
) -> tuple[tuple[int, ...], ...]:
    """Return nontrivial equal-signature classes in population order."""
    grouped: dict[int, list[int]] = {}
    for prime, signature in zip(population, signatures, strict=True):
        grouped.setdefault(signature, []).append(prime)
    return tuple(
        tuple(bucket) for bucket in grouped.values() if len(bucket) > 1
    )


@cache
def raw_baseline_partition(
    input_length: int,
    cap: int,
) -> tuple[tuple[tuple[int, ...], ...], int]:
    """Derive baseline blocks from the full raw public family."""
    population = balanced_population(input_length)
    unresolved: list[tuple[int, ...]] = [tuple(range(len(population)))]
    evaluations = 0
    for descriptor in iter_descriptors(cap):
        refined: list[tuple[int, ...]] = []
        for bucket in unresolved:
            groups: dict[int, list[int]] = {}
            for index in bucket:
                value = primitive_mask(descriptor, population[index])
                evaluations += 1
                groups.setdefault(value, []).append(index)
            refined.extend(
                tuple(group)
                for group in groups.values()
                if len(group) > 1
            )
        unresolved = refined
        if not unresolved:
            break
    return (
        tuple(
            tuple(population[index] for index in bucket)
            for bucket in unresolved
        ),
        evaluations,
    )


def baseline_partition(
    source_id: str,
    input_length: int,
    base_cap: int,
    repair_cap: int,
    population: tuple[int, ...],
    certificate: Mapping[str, Any],
) -> tuple[tuple[tuple[int, ...], ...], str, int, int, int]:
    """Reconstruct the public baseline partition without M95 labels."""
    names = tuple(str(item) for item in certificate["column_sources"])
    if len(set(names)) != len(names):
        raise AssertionError("public coordinate sources are not unique")
    parsed = tuple(parse_source(name, repair_cap) for name in names)
    if source_id == "M92":
        selected = tuple(item for item in parsed if item[0].cap <= base_cap)
        signatures = [0] * len(population)
        for column, (descriptor, kind_index) in enumerate(selected):
            bit = 1 << column
            for index, prime in enumerate(population):
                if (primitive_mask(descriptor, prime) >> kind_index) & 1:
                    signatures[index] |= bit
        buckets = collision_buckets(population, tuple(signatures))
        persistence_evaluations = 0
        for descriptor in iter_descriptors(base_cap):
            for bucket in buckets:
                values = {
                    primitive_mask(descriptor, prime) for prime in bucket
                }
                persistence_evaluations += len(bucket)
                if len(values) != 1:
                    raise AssertionError("selected baseline block was split")
        return (
            buckets,
            "selected-subfamily-plus-raw-persistence",
            len(selected),
            len(selected) * len(population),
            persistence_evaluations,
        )

    buckets, evaluations = raw_baseline_partition(input_length, base_cap)
    return (
        buckets,
        "full-raw-family-refinement",
        descriptor_count(base_cap) * EXIT_COUNT,
        evaluations * EXIT_COUNT,
        0,
    )


def construct_graph(
    masks_to_patterns: Mapping[int, tuple[int, ...]],
    tracked: tuple[int, ...],
    pairs: tuple[tuple[int, int], ...],
) -> dict[str, Any]:
    """Construct canonical types, columns, loops, and residual edges."""
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
                "pair": [tracked[left], tracked[right]],
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
    forced_set = set(forced)
    vertices = tuple(
        type_id for type_id in type_ids if type_id not in forced_set
    )
    edges: tuple[tuple[str, ...], ...] = tuple(
        tuple(column["coverer_type_ids"])
        for column in coverer_sets
        if len(column["coverer_type_ids"]) == 2
        and not forced_set.intersection(column["coverer_type_ids"])
    )
    histogram: dict[str, int] = {}
    for column in coverer_sets:
        key = str(len(column["coverer_type_ids"]))
        histogram[key] = histogram.get(key, 0) + 1
    return {
        "coverage_types": coverage_types,
        "coverer_sets": coverer_sets,
        "column_degree_histogram": histogram,
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
    """Compare a completed graph to M95 modulo type and bucket order."""
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
        raise AssertionError("M100 comparison coverage types changed")
    derived_columns = {
        tuple(int(prime) for prime in record["pair"]): tuple(
            sorted(
                derived_keys[str(type_id)]
                for type_id in record["coverer_type_ids"]
            )
        )
        for record in constructed["coverer_sets"]
    }
    comparison_columns = {
        tuple(int(prime) for prime in record["pair"]): tuple(
            sorted(
                comparison_keys[str(type_id)]
                for type_id in record["coverer_type_ids"]
            )
        )
        for record in graph["coverer_sets"]
    }
    if derived_columns != comparison_columns:
        raise AssertionError("M100 comparison coverer columns changed")
    if {
        derived_keys[str(type_id)]
        for type_id in constructed["forced_type_ids"]
    } != {
        comparison_keys[str(type_id)] for type_id in graph["looped_type_ids"]
    }:
        raise AssertionError("M100 comparison forced loops changed")
    if constructed["column_degree_histogram"] != graph[
        "column_degree_histogram"
    ]:
        raise AssertionError("M100 comparison degree histogram changed")
    if constructed["coverer_incidence_count"] != graph[
        "coverer_incidence_count"
    ]:
        raise AssertionError("M100 comparison incidence count changed")


def bipartite_after(
    vertices: tuple[str, ...],
    edges: tuple[tuple[str, str], ...],
    deleted: set[str],
) -> bool:
    """Test bipartiteness after deleting a vertex set."""
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


def minimum_oct(
    vertices: tuple[str, ...],
    edges: tuple[tuple[str, str], ...],
) -> tuple[str, ...]:
    """Return the lexicographically first exact OCT by bounded enumeration."""
    for size in range(len(vertices) + 1):
        for chosen in itertools.combinations(vertices, size):
            if bipartite_after(vertices, edges, set(chosen)):
                return chosen
    raise AssertionError("finite graph has no OCT")


def expected_sources() -> list[dict[str, Any]]:
    """Construct the exact source binding registry."""
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
    for source_id, path, role, dependency in specs:
        record: dict[str, Any] = {
            "source_id": source_id,
            "path": str(path.relative_to(ROOT)).replace("\\", "/"),
            "file_sha256": file_sha256(path),
            "role": role,
            "semantic_dependency": dependency,
        }
        if path.suffix == ".json":
            data = json.loads(path.read_text(encoding="utf-8"))
            if "summary_sha256" in data:
                record["summary_sha256"] = str(data["summary_sha256"])
        records.append(record)
    return records


EXPECTED_CONTRACT = {
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
}
EXPECTED_SCHEDULE = {
    "formula": "ceil(log2(m))",
    "depends_only_on": "input length m",
    "application_status": "EMPIRICAL for the frozen lengths 16 through 34",
    "asymptotic_status": "OPEN for future coverer graphs",
}
EXPECTED_BOUNDARY = {
    "registered_path_is_factor_independent": True,
    "registered_path_is_polynomial_in_explicit_artifacts": True,
    "registered_path_is_polynomial_in_m": False,
    "reason": (
        "the registered verifier explicitly enumerates P_m; "
        "BAR-041 gives |P_m|=Omega(2^(m/2)/m)"
    ),
    "compact_graph_hash_proves_semantic_completeness": False,
    "hidden_input_to_population_vertex_map": (
        "not needed for offline public graph construction, but recognizing "
        "an arbitrary input's balanced-semiprime promise and obtaining a "
        "general asymptotic graph/cap law remain open"
    ),
}
EXPECTED_SCOPE = {
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
}


def validate_counterexample(record: Mapping[str, Any]) -> None:
    """Validate the semantic failure of a self-consistent hash."""
    claimed = record.get("claimed_payload")
    if not isinstance(claimed, dict):
        raise AssertionError("hash counterexample framing changed")
    expected_claimed = {
        "universe": ["u0", "u1"],
        "claimed_types": {"T0": ["u0"], "T1": ["u1"]},
        "claimed_exact_cover_number": 2,
    }
    if claimed != expected_claimed:
        raise AssertionError("hash counterexample payload changed")
    digest = hashlib.sha256(
        json.dumps(
            claimed,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()
    if record.get("recomputed_sha256") != digest:
        raise AssertionError("hash counterexample digest changed")
    if record.get("omitted_realized_type") != {"T2": ["u0", "u1"]}:
        raise AssertionError("hash counterexample omitted type changed")
    if record.get("actual_exact_cover_number") != 1:
        raise AssertionError("hash counterexample minimum changed")
    if record.get("conclusion") != (
        "the digest binds the claimed bytes but does not prove that "
        "the realized type family is complete"
    ):
        raise AssertionError("hash counterexample conclusion changed")


def source_caps(
    source_id: str,
    source: Mapping[str, Any],
) -> tuple[int, int]:
    """Read the exact public cap interval."""
    if source_id == "M92":
        return int(source["base_cap"]), int(source["repair_cap"])
    repair_cap = int(source["repair_cap"])
    return repair_cap - 1, repair_cap


def validate_instance(
    record: Mapping[str, Any],
    source_id: str,
    input_length: int,
    graph: Mapping[str, Any],
    source: Mapping[str, Any],
    m50_row: Mapping[str, Any],
    source_artifact: Mapping[str, Any],
) -> dict[str, int | bool]:
    """Independently reconstruct one complete frozen public graph record."""
    if (
        graph["source_id"] != source_id
        or graph["input_length"] != input_length
    ):
        raise AssertionError("M100 comparison identity changed")
    if (
        record.get("source_id") != source_id
        or record.get("input_length") != input_length
    ):
        raise AssertionError("M100 instance identity changed")
    base_cap, repair_cap = source_caps(source_id, source)
    if (
        record.get("base_cap") != base_cap
        or record.get("repair_cap") != repair_cap
    ):
        raise AssertionError("M100 public cap interval changed")
    source_path = str(m50_row["source_schema"])
    if (
        record.get("source_schema") != source_path
        or record.get("source_schema_sha256")
        != file_sha256(ROOT / source_path)
    ):
        raise AssertionError("M100 row source binding changed")
    cache_key = (source_id, input_length)
    cached = INSTANCE_CACHE.get(cache_key)
    if cached is not None:
        if dict(record) != cached:
            raise AssertionError("M100 instance ledger changed")
        return {
            key: value
            for key, value in cached.items()
            if isinstance(value, (int, bool))
        }

    population = balanced_population(input_length)
    certificate = certificate_for(source_artifact, input_length)
    if tuple(int(prime) for prime in certificate["primes"]) != population:
        raise AssertionError("M100 public population certificate changed")
    if len(population) != int(m50_row["population_size"]):
        raise AssertionError("M100 public population size changed")
    (
        buckets,
        baseline_mode,
        selected_count,
        selected_evaluations,
        persistence_descriptor_evaluations,
    ) = baseline_partition(
        source_id,
        input_length,
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
        raise AssertionError("M100 comparison collision buckets changed")
    tracked = tuple(prime for bucket in buckets for prime in bucket)
    pairs = pair_indices(buckets)
    masks, observed_descriptors = public_type_masks(
        base_cap,
        repair_cap,
        tracked,
        pairs,
    )
    expected_descriptors = (
        descriptor_count(repair_cap) - descriptor_count(base_cap)
    )
    if observed_descriptors != expected_descriptors:
        raise AssertionError("M100 descriptor count changed")
    constructed = construct_graph(masks, tracked, pairs)
    compare_to_m95(graph, constructed)
    width = max(1, math.ceil(len(pairs) / 4))
    encoded_masks = [f"{mask:0{width}x}" for mask in sorted(masks)]
    vertices = constructed["residual_vertex_ids"]
    edges = constructed["residual_edges"]
    optimum = minimum_oct(vertices, edges)
    cap = (input_length - 1).bit_length()
    coverer_rank = max(
        len(column["coverer_type_ids"])
        for column in constructed["coverer_sets"]
    )
    expected = {
        "source_id": source_id,
        "input_length": input_length,
        "source_schema": source_path,
        "source_schema_sha256": file_sha256(ROOT / source_path),
        "base_cap": base_cap,
        "repair_cap": repair_cap,
        "population_size": len(population),
        "population_label_bits": sum(prime.bit_length() for prime in population),
        "baseline_partition_mode": baseline_mode,
        "baseline_collision_buckets": [list(bucket) for bucket in buckets],
        "selected_coordinate_count": selected_count,
        "selected_certificate_evaluations": selected_evaluations,
        "baseline_persistence_descriptor_evaluations": (
            persistence_descriptor_evaluations
        ),
        "baseline_persistence_primitive_tests": (
            persistence_descriptor_evaluations * EXIT_COUNT
        ),
        "tracked_point_count": len(tracked),
        "pair_count": len(pairs),
        "new_descriptor_count": expected_descriptors,
        "new_descriptor_prime_evaluations": expected_descriptors * len(tracked),
        "primitive_coordinate_tests": (
            expected_descriptors * len(tracked) * EXIT_COUNT
        ),
        "complete_type_count": len(masks),
        "complete_coverage_masks_hex": encoded_masks,
        "coverage_types": constructed["coverage_types"],
        "coverer_sets": constructed["coverer_sets"],
        "coverer_rank": coverer_rank,
        "forced_type_ids": list(constructed["forced_type_ids"]),
        "forced_type_count": len(constructed["forced_type_ids"]),
        "residual_vertex_ids": list(vertices),
        "residual_vertex_count": len(vertices),
        "residual_edges": [list(edge) for edge in edges],
        "residual_edge_count": len(edges),
        "public_oct_cap": cap,
        "exact_oct_number": len(optimum),
        "exact_oct_type_ids": list(optimum),
        "within_public_oct_cap": len(optimum) <= cap,
        "graph_payload_bits": int(
            graph["verification_cost"]["abstract_certificate_payload_bits"]
        ),
    }
    if dict(record) != expected:
        raise AssertionError("M100 instance ledger changed")
    INSTANCE_CACHE[cache_key] = expected
    return {
        key: value
        for key, value in expected.items()
        if isinstance(value, (int, bool))
    }


def validate_all(
    schema: Mapping[str, Any] | None = None,
) -> dict[str, int | bool]:
    """Validate the complete M100 public-construction portfolio."""
    data = (
        json.loads(SCHEMA.read_text(encoding="utf-8"))
        if schema is None
        else dict(schema)
    )
    if data.get("schema_version") != "1.0.0":
        raise AssertionError("unsupported M100 schema version")
    if data.get("experiment_id") != "EXP-0071":
        raise AssertionError("M100 experiment ID changed")
    if data.get("claim_ids") != [
        "DEF-056",
        "THM-029",
        "REF-069",
        "EMP-071",
    ]:
        raise AssertionError("M100 claim registry changed")
    if data.get("sources") != expected_sources():
        raise AssertionError("M100 source registry changed")
    if data.get("constructor_contract") != EXPECTED_CONTRACT:
        raise AssertionError("M100 constructor contract changed")
    if data.get("public_oct_schedule") != EXPECTED_SCHEDULE:
        raise AssertionError("M100 public OCT schedule changed")
    if data.get("boundary") != EXPECTED_BOUNDARY:
        raise AssertionError("M100 boundary changed")
    if data.get("scope") != EXPECTED_SCOPE:
        raise AssertionError("M100 scope changed")
    if data.get("summary_sha256") != canonical_hash(data):
        raise AssertionError("M100 canonical summary hash changed")
    validate_counterexample(data["hash_only_counterexample"])

    m50 = json.loads(M50_PATH.read_text(encoding="utf-8"))
    m92 = json.loads(M92_PATH.read_text(encoding="utf-8"))
    m93 = json.loads(M93_PATH.read_text(encoding="utf-8"))
    m95 = json.loads(M95_PATH.read_text(encoding="utf-8"))
    source_instances = {
        (source_id, int(item["input_length"])): item
        for source_id, source_data in (("M92", m92), ("M93", m93))
        for item in source_data["instances"]
    }
    m50_rows = {
        int(row["input_length"]): row for row in m50["rows"]
    }
    comparison_graphs = {
        (str(graph["source_id"]), int(graph["input_length"])): graph
        for graph in m95["instances"]
    }
    source_cache: dict[str, Mapping[str, Any]] = {}
    records = data.get("instances")
    if not isinstance(records, list) or len(records) != 19:
        raise AssertionError("M100 instance count changed")
    reports = []
    for record, input_length in zip(records, range(16, 35), strict=True):
        source_id = "M92" if input_length >= 26 else "M93"
        row = m50_rows[input_length]
        path = str(row["source_schema"])
        if path not in source_cache:
            source_cache[path] = json.loads(
                (ROOT / path).read_text(encoding="utf-8")
            )
        reports.append(
            validate_instance(
                record,
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
    totals: dict[str, int | bool] = {
        "instance_count": len(reports),
        **{
            field: sum(int(report[field]) for report in reports)
            for field in summed
        },
        "maximum_exact_oct_number": max(
            int(report["exact_oct_number"]) for report in reports
        ),
        "all_public_caps_accepted": all(
            bool(report["within_public_oct_cap"]) for report in reports
        ),
    }
    if data.get("totals") != totals:
        raise AssertionError("M100 totals changed")
    return totals


def main() -> int:
    """Run the standalone M100 checker."""
    totals = validate_all()
    print(
        "M100 public coverer-graph checker: PASS "
        f"({totals['instance_count']} instances, "
        f"{totals['complete_type_count']} complete types, "
        f"{totals['primitive_coordinate_tests']} primitive tests, "
        f"max OCT {totals['maximum_exact_oct_number']})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
