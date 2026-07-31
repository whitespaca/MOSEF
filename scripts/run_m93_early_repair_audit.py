"""Build exact early repair certificates for input lengths 16 through 25."""

from __future__ import annotations

import hashlib
import itertools
import json
import math
import sys
from collections.abc import Iterable
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts import check_m91_all_rows_semantic_certificate as m91

SUMMARY_PATH = ROOT / "schemas" / "m50-finite-threshold-summary-v1.json"
SOURCE_BY_LENGTH = {
    16: "schemas/m32-widened-selector-cap-v1.json",
    17: "schemas/m32-widened-selector-cap-v1.json",
    18: "schemas/m32-widened-selector-cap-v1.json",
    19: "schemas/m32-widened-selector-cap-v1.json",
    20: "schemas/m32-widened-selector-cap-v1.json",
    21: "schemas/m33-linear-cap-recurrence-v1.json",
    22: "schemas/m34-next-envelope-v1.json",
    23: "schemas/m35-next-envelope-v1.json",
    24: "schemas/m36-distinct-cap-v1.json",
    25: "schemas/m37-length-25-cap-v1.json",
}


def file_sha256(path: Path) -> str:
    """Return one exact binary file digest."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_hash(record: dict[str, Any]) -> str:
    """Hash a JSON object after excluding its registered digest."""
    payload = dict(record)
    payload.pop("summary_sha256", None)
    encoded = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def normalized_pattern(pattern: tuple[int, ...]) -> tuple[int, ...]:
    """Canonicalize one nonconstant binary pattern modulo complementation."""
    if not pattern or any(bit not in (0, 1) for bit in pattern):
        raise AssertionError("repair pattern is not a nonempty bit vector")
    complement = tuple(1 - bit for bit in pattern)
    return min(pattern, complement)


def pair_universe(
    buckets: tuple[tuple[int, ...], ...],
) -> tuple[tuple[int, int], ...]:
    """Enumerate labeled within-bucket pairs in canonical order."""
    return tuple(
        (bucket[left], bucket[right])
        for bucket in buckets
        for left in range(len(bucket))
        for right in range(left + 1, len(bucket))
    )


def pair_indices(
    buckets: tuple[tuple[int, ...], ...],
) -> tuple[tuple[int, int], ...]:
    """Enumerate flattened within-bucket index pairs."""
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
    """Return the bit mask of pairs separated by one pattern."""
    return sum(
        1 << index
        for index, (left, right) in enumerate(pairs)
        if pattern[left] != pattern[right]
    )


def exact_cover(
    masks: tuple[int, ...],
    target: int,
) -> tuple[int, ...]:
    """Return the lexicographically first minimum cover by type index."""
    for size in range(len(masks) + 1):
        for subset in itertools.combinations(range(len(masks)), size):
            if _or_masks(masks[index] for index in subset) == target:
                return subset
    raise AssertionError("raw coverage types do not repair the buckets")


def index_width(value_count: int) -> int:
    """Return the exact fixed-width index cost for a nonempty finite set."""
    return 0 if value_count <= 1 else math.ceil(math.log2(value_count))


def _or_masks(masks: Iterable[int]) -> int:
    """OR an iterable without an additional project dependency."""
    result = 0
    for mask in masks:
        result |= int(mask)
    return result


def enumerate_coverage_types(
    base_cap: int,
    repair_cap: int,
    tracked_primes: tuple[int, ...],
    pairs: tuple[tuple[int, int], ...],
) -> tuple[dict[int, tuple[tuple[int, ...], str]], int]:
    """Enumerate every distinct nonzero newly admitted coverage type."""
    types: dict[int, tuple[tuple[int, ...], str]] = {}
    descriptor_count = 0
    for descriptor in m91.iter_selector_descriptors(repair_cap):
        if descriptor.cap <= base_cap:
            continue
        descriptor_count += 1
        primitive_masks = tuple(
            m91.primitive_exit_mask(descriptor, prime)
            for prime in tracked_primes
        )
        for kind_index, kind in enumerate(m91.EXIT_KINDS):
            raw_pattern = tuple(
                (mask >> kind_index) & 1 for mask in primitive_masks
            )
            pattern = normalized_pattern(raw_pattern)
            coverage = pattern_coverage(pattern, pairs)
            if coverage:
                types.setdefault(
                    coverage,
                    (pattern, f"{descriptor.key}:{kind}"),
                )
    return types, descriptor_count


def private_pair_witness(
    selected_ids: tuple[str, ...],
    masks_by_id: dict[str, int],
    pairs: tuple[tuple[int, int], ...],
) -> list[dict[str, object]] | None:
    """Return private-pair witnesses, or None when one type lacks one."""
    witness: list[dict[str, object]] = []
    for type_id in selected_ids:
        private_index = next(
            (
                pair_index
                for pair_index in range(len(pairs))
                if (masks_by_id[type_id] >> pair_index) & 1
                and sum(
                    (mask >> pair_index) & 1
                    for mask in masks_by_id.values()
                )
                == 1
            ),
            None,
        )
        if private_index is None:
            return None
        witness.append(
            {
                "type_id": type_id,
                "pair_index": private_index,
                "pair": list(pairs[private_index]),
            }
        )
    return witness


def lower_witness(
    input_length: int,
    selected_ids: tuple[str, ...],
    masks_by_id: dict[str, int],
    buckets: tuple[tuple[int, ...], ...],
    pairs: tuple[tuple[int, int], ...],
) -> dict[str, Any]:
    """Choose the registered exact lower certificate for one instance."""
    minimum = len(selected_ids)
    private = private_pair_witness(selected_ids, masks_by_id, pairs)
    if private is not None:
        return {
            "kind": "private_pairs",
            "lower_bound": minimum,
            "entries": private,
        }
    if input_length == 16:
        maximum_bucket_size = max(len(bucket) for bucket in buckets)
        bound = math.ceil(math.log2(maximum_bucket_size))
        if bound != minimum:
            raise AssertionError("cardinality lower bound is not exact")
        return {
            "kind": "cardinality",
            "lower_bound": bound,
            "maximum_bucket_size": maximum_bucket_size,
        }
    if input_length != 24:
        raise AssertionError("unexpected failure of the private-pair criterion")
    subset_size = minimum - 1
    entries: list[dict[str, object]] = []
    type_ids = tuple(masks_by_id)
    for subset in itertools.combinations(type_ids, subset_size):
        union = _or_masks(masks_by_id[type_id] for type_id in subset)
        pair_index = next(
            (
                index
                for index in range(len(pairs))
                if not (union >> index) & 1
            ),
            None,
        )
        if pair_index is None:
            raise AssertionError("a smaller subset unexpectedly covers all pairs")
        entries.append(
            {
                "type_ids": list(subset),
                "uncovered_pair_index": pair_index,
                "uncovered_pair": list(pairs[pair_index]),
            }
        )
    return {
        "kind": "subset_obstructions",
        "lower_bound": minimum,
        "subset_size": subset_size,
        "entries": entries,
    }


def lower_cost(
    lower: dict[str, Any],
    type_count: int,
    pair_count: int,
) -> tuple[int, int]:
    """Return verifier bit tests and abstract payload bits for one lower bound."""
    kind = lower["kind"]
    if kind == "private_pairs":
        entry_count = len(lower["entries"])
        return (
            entry_count * type_count,
            entry_count
            * (index_width(type_count) + index_width(pair_count)),
        )
    if kind == "cardinality":
        maximum = int(lower["maximum_bucket_size"])
        bound = int(lower["lower_bound"])
        return 1, maximum.bit_length() + bound.bit_length()
    if kind == "subset_obstructions":
        entries = lower["entries"]
        subset_size = int(lower["subset_size"])
        return (
            len(entries) * subset_size,
            len(entries)
            * (
                subset_size * index_width(type_count)
                + index_width(pair_count)
            ),
        )
    raise AssertionError("unknown lower witness kind")


def build_instance(
    row: dict[str, Any],
    source_records: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    """Build one source-bound early repair certificate."""
    input_length = int(row["input_length"])
    repair_cap = int(row["family_relative_minimal_cap"])
    base_cap = repair_cap - 1
    source_path = str(row["source_schema"])
    if SOURCE_BY_LENGTH[input_length] != source_path:
        raise AssertionError("M50 early source map changed")
    source_record = source_records[source_path]
    path = ROOT / source_path
    if source_record["file_sha256"] != file_sha256(path):
        raise AssertionError("M50 source digest no longer matches its file")
    buckets = tuple(
        tuple(int(prime) for prime in bucket)
        for bucket in row["predecessor_collision_buckets"]
    )
    tracked_primes = tuple(prime for bucket in buckets for prime in bucket)
    labeled_pairs = pair_universe(buckets)
    indexed_pairs = pair_indices(buckets)
    raw_types, descriptor_count = enumerate_coverage_types(
        base_cap,
        repair_cap,
        tracked_primes,
        indexed_pairs,
    )
    ordered_types = tuple(sorted(raw_types.items()))
    masks = tuple(mask for mask, _record in ordered_types)
    target = (1 << len(labeled_pairs)) - 1
    selected_indices = exact_cover(masks, target)
    type_ids = tuple(f"T{index}" for index in range(len(ordered_types)))
    selected_ids = tuple(type_ids[index] for index in selected_indices)
    width = max(1, math.ceil(len(labeled_pairs) / 4))
    coverage_types = [
        {
            "type_id": type_id,
            "pattern": list(pattern),
            "coverage_mask_hex": f"{mask:0{width}x}",
            "representative_source": source,
        }
        for type_id, (mask, (pattern, source)) in zip(
            type_ids,
            ordered_types,
            strict=True,
        )
    ]
    masks_by_id = dict(zip(type_ids, masks, strict=True))
    lower = lower_witness(
        input_length,
        selected_ids,
        masks_by_id,
        buckets,
        labeled_pairs,
    )
    minimum = len(selected_ids)
    lower_tests, lower_bits = lower_cost(
        lower,
        len(ordered_types),
        len(labeled_pairs),
    )
    selected_bits = minimum * index_width(len(ordered_types))
    label_bits = sum(prime.bit_length() for prime in tracked_primes)
    pattern_bits = len(ordered_types) * len(tracked_primes)
    mask_bits = len(ordered_types) * len(labeled_pairs)
    cost = {
        "new_descriptor_count": descriptor_count,
        "descriptor_prime_evaluations": descriptor_count
        * len(tracked_primes),
        "raw_coordinate_tests": descriptor_count
        * len(tracked_primes)
        * len(m91.EXIT_KINDS),
        "pattern_pair_tests": len(ordered_types) * len(labeled_pairs),
        "upper_mask_bit_tests": minimum * len(labeled_pairs),
        "lower_witness_bit_tests": lower_tests,
        "certificate_verifier_bit_tests": (
            len(ordered_types) * len(labeled_pairs)
            + minimum * len(labeled_pairs)
            + lower_tests
        ),
        "defense_subset_count": 1 << len(ordered_types),
        "defense_mask_bit_tests": (
            len(labeled_pairs)
            * len(ordered_types)
            * (1 << (len(ordered_types) - 1))
        ),
        "pattern_storage_bits": pattern_bits,
        "mask_storage_bits": mask_bits,
        "selected_type_index_bits": selected_bits,
        "lower_witness_payload_bits": lower_bits,
        "bucket_label_bits": label_bits,
        "abstract_certificate_payload_bits": (
            pattern_bits + mask_bits + selected_bits + lower_bits + label_bits
        ),
    }
    return {
        "input_length": input_length,
        "source_path": source_path,
        "source_sha256": source_record["file_sha256"],
        "source_file_bytes": path.stat().st_size,
        "base_cap": base_cap,
        "repair_cap": repair_cap,
        "collision_buckets": [list(bucket) for bucket in buckets],
        "tracked_prime_count": len(tracked_primes),
        "pair_count": len(labeled_pairs),
        "coverage_types": coverage_types,
        "upper_witness": list(selected_ids),
        "lower_witness": lower,
        "minimum_coordinate_count": minimum,
        "verification_cost": cost,
    }


def build_summary() -> dict[str, Any]:
    """Build the complete registered M93 certificate portfolio."""
    m50 = json.loads(SUMMARY_PATH.read_text(encoding="utf-8"))
    if file_sha256(SUMMARY_PATH) != (
        "2f9974d45a350f65694bd048bf67dae4b27a90493b07ecd895c251d102aab75b"
    ):
        raise AssertionError("M50 frozen summary digest changed")
    source_records = {
        str(record["path"]): record for record in m50["sources"]
    }
    rows = {
        int(row["input_length"]): row
        for row in m50["rows"]
        if 16 <= int(row["input_length"]) <= 25
    }
    instances = [
        build_instance(rows[input_length], source_records)
        for input_length in range(16, 26)
    ]
    summed_fields = (
        "tracked_prime_count",
        "pair_count",
        "minimum_coordinate_count",
    )
    cost_fields = (
        "new_descriptor_count",
        "descriptor_prime_evaluations",
        "raw_coordinate_tests",
        "pattern_pair_tests",
        "upper_mask_bit_tests",
        "lower_witness_bit_tests",
        "certificate_verifier_bit_tests",
        "defense_subset_count",
        "defense_mask_bit_tests",
        "source_file_bytes",
        "abstract_certificate_payload_bits",
    )
    totals = {
        "instance_count": len(instances),
        **{
            field: sum(int(instance[field]) for instance in instances)
            for field in summed_fields
        },
        "coverage_type_count": sum(
            len(instance["coverage_types"]) for instance in instances
        ),
        **{
            field: sum(
                int(
                    instance[field]
                    if field == "source_file_bytes"
                    else instance["verification_cost"][field]
                )
                for instance in instances
            )
            for field in cost_fields
        },
    }
    summary: dict[str, Any] = {
        "schema_version": "1.0.0",
        "experiment_id": "EXP-0064",
        "claim_ids": ["DEF-049", "THM-022", "REF-062", "EMP-064"],
        "finite_summary": {
            "path": "schemas/m50-finite-threshold-summary-v1.json",
            "file_sha256": file_sha256(SUMMARY_PATH),
            "summary_sha256": m50["summary_sha256"],
        },
        "pair_order": (
            "bucket order, then increasing left index, then increasing right index"
        ),
        "complement_rule": (
            "binary patterns are canonicalized with their bitwise complement"
        ),
        "lower_witness_rules": {
            "private_pairs": "one pair covered by exactly one selected type",
            "cardinality": "ceil(log2(maximum bucket size))",
            "subset_obstructions": (
                "one explicit uncovered pair for every (k-1)-type subset"
            ),
        },
        "instances": instances,
        "totals": totals,
        "status": "PASS",
    }
    summary["summary_sha256"] = canonical_hash(summary)
    return summary


def main() -> int:
    """Run the abstract early-repair audit."""
    summary = build_summary()
    totals = summary["totals"]
    print(
        "M93 early repair audit: PASS "
        f"({totals['instance_count']} instances, "
        f"{totals['pair_count']} pairs, "
        f"{totals['coverage_type_count']} coverage types, "
        f"{totals['minimum_coordinate_count']} selected types, "
        f"{totals['abstract_certificate_payload_bits']} payload bits, "
        f"summary_sha256={summary['summary_sha256']})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
