"""Deterministic M46 audit of the length-34 finite envelope."""

from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "python")]

from mosef_reference import (
    ExceptionalSelectorDescriptor,
    balanced_prime_population,
    diversified_exceptional_selector,
)
from mosef_reference.diversified_compact_signatures import (
    PRIMITIVE_EXIT_KINDS,
    _primitive_exit_mask_from_resultant,
)
from mosef_reference.exceptional_cofactor_schedule import (
    exceptional_cofactor_overlap,
)

from scripts.run_m45_length_33_cap_audit import _profile, _refine, _signatures

INPUT_LENGTH = 34
ADDITIVE_CAP = 196
MULTIPLICATIVE_CAP = 200
PREDECESSOR_CAP = 200
REPAIR_CAP = 201
ADDITIVE_COLLISION = (97927, 99527, 127877)
MULTIPLICATIVE_COLLISION = (97927, 99527)
FINAL_COLLISION = MULTIPLICATIVE_COLLISION
REPAIR_SOURCE = "phi6:149:201:45:cofactor"

# descriptor count, distinct signatures, pairs, bucket, selected sources,
# cumulative optimized local-exit evaluations
EXPECTED_PUBLIC_PROFILES = {
    196: (
        664560,
        3297,
        3,
        (ADDITIVE_COLLISION,),
        3296,
        306238137,
    ),
    200: (
        704261,
        3298,
        1,
        (MULTIPLICATIVE_COLLISION,),
        3297,
        306350153,
    ),
}

# descriptor count, new descriptors, distinct signatures, pairs, bucket,
# selected sources, optimized local-exit evaluations after cap 200
EXPECTED_TRANSITIONS = {
    201: (714400, 10139, 3299, 0, (), 3298, 16238),
}


def _first_cap(descriptor: ExceptionalSelectorDescriptor) -> int:
    return int(
        max(
            INPUT_LENGTH,
            descriptor.first_factor,
            descriptor.second_factor,
            descriptor.base,
        )
    )


def _partition_audit(
    primes: tuple[int, ...],
) -> tuple[
    tuple[dict[str, object], ...],
    tuple[dict[str, object], ...],
    tuple[str, ...],
    tuple[str, ...],
]:
    descriptors = diversified_exceptional_selector(INPUT_LENGTH, REPAIR_CAP)
    by_cap: defaultdict[int, list[ExceptionalSelectorDescriptor]] = defaultdict(
        list
    )
    for descriptor in descriptors:
        by_cap[_first_cap(descriptor)].append(descriptor)

    buckets: tuple[tuple[int, ...], ...] = (primes,)
    selected: list[str] = []
    public: list[dict[str, object]] = []
    transitions: list[dict[str, object]] = []
    descriptor_count = 0
    checks = 0
    baseline = 0
    predecessor_sources: tuple[str, ...] = ()
    selected_caps = set(EXPECTED_PUBLIC_PROFILES) | set(EXPECTED_TRANSITIONS)
    for cap in range(INPUT_LENGTH, REPAIR_CAP + 1):
        added = by_cap[cap]
        for descriptor in added:
            buckets, sources, local_checks = _refine(buckets, descriptor)
            selected.extend(sources)
            checks += local_checks
        descriptor_count += len(added)
        if cap not in selected_caps:
            continue
        record = _profile(
            cap,
            descriptor_count,
            len(added),
            len(primes),
            buckets,
            len(selected),
            checks,
        )
        if cap in EXPECTED_PUBLIC_PROFILES:
            observed = (
                descriptor_count,
                record["distinct_signature_count"],
                record["collision_pair_count"],
                buckets,
                len(selected),
                checks,
            )
            if observed != EXPECTED_PUBLIC_PROFILES[cap]:
                raise AssertionError(f"M46 public profile changed: {cap}, {observed}")
            public.append(record)
            if cap == MULTIPLICATIVE_CAP:
                baseline = checks
                predecessor_sources = tuple(selected)
                transitions.append(
                    {
                        **record,
                        "new_descriptor_count": 0,
                        "tracked_population_size": len(MULTIPLICATIVE_COLLISION),
                        "optimized_transition_local_exit_checks": 0,
                    }
                )
            continue

        observed_transition = (
            descriptor_count,
            len(added),
            record["distinct_signature_count"],
            record["collision_pair_count"],
            buckets,
            len(selected),
            checks - baseline,
        )
        if observed_transition != EXPECTED_TRANSITIONS[cap]:
            raise AssertionError(
                f"M46 transition changed: {cap}, {observed_transition}"
            )
        transitions.append(
            {
                **record,
                "tracked_population_size": len(MULTIPLICATIVE_COLLISION),
                "optimized_transition_local_exit_checks": checks - baseline,
            }
        )

    if descriptor_count != len(descriptors):
        raise AssertionError("M46 descriptor accounting changed")
    if len(predecessor_sources) != 3297:
        raise AssertionError("M46 predecessor source count changed")
    if tuple(selected[len(predecessor_sources) :]) != (REPAIR_SOURCE,):
        raise AssertionError("M46 final repair source changed")
    return (
        tuple(public),
        tuple(transitions),
        predecessor_sources,
        tuple(selected),
    )


def _repair_patterns() -> tuple[dict[tuple[int, ...], tuple[str, ...]], int]:
    old_keys = {
        descriptor.key
        for descriptor in diversified_exceptional_selector(
            INPUT_LENGTH,
            PREDECESSOR_CAP,
        )
    }
    patterns: defaultdict[tuple[int, ...], list[str]] = defaultdict(list)
    checks = 0
    for descriptor in diversified_exceptional_selector(
        INPUT_LENGTH,
        REPAIR_CAP,
    ):
        if descriptor.key in old_keys:
            continue
        resultant = exceptional_cofactor_overlap(
            descriptor.first_factor,
            descriptor.second_factor,
            descriptor.family,
        ).cyclotomic_cofactor_resultant
        masks = tuple(
            _primitive_exit_mask_from_resultant(descriptor, prime, resultant)
            for prime in FINAL_COLLISION
        )
        for kind_index, kind in enumerate(PRIMITIVE_EXIT_KINDS):
            pattern = tuple(
                int(bool(mask & (1 << kind_index))) for mask in masks
            )
            if len(set(pattern)) > 1:
                patterns[pattern].append(f"{descriptor.key}:{kind}")
            checks += 1
    return (
        {pattern: tuple(sources) for pattern, sources in patterns.items()},
        checks,
    )


def build_summary() -> dict[str, object]:
    """Run the exact partition, construction, and repair audit."""
    if ADDITIVE_CAP != INPUT_LENGTH + 162:
        raise AssertionError("M46 additive schedule changed")
    if MULTIPLICATIVE_CAP != (147 * INPUT_LENGTH + 24) // 25:
        raise AssertionError("M46 multiplicative schedule changed")

    primes = balanced_prime_population(INPUT_LENGTH)
    if len(primes) != 3299:
        raise AssertionError("M46 balanced population changed")
    pair_count = len(primes) * (len(primes) - 1) // 2
    public, transitions, predecessor_sources, sources = _partition_audit(primes)
    signatures = _signatures(sources, primes)
    predecessor_mask = (1 << len(predecessor_sources)) - 1
    predecessor_signatures = tuple(
        signature & predecessor_mask for signature in signatures
    )
    counts_by_signature = Counter(predecessor_signatures)
    predecessor_buckets = tuple(
        tuple(
            prime
            for prime, signature in zip(
                primes,
                predecessor_signatures,
                strict=True,
            )
            if signature == repeated
        )
        for repeated, count in counts_by_signature.items()
        if count > 1
    )
    if predecessor_buckets != (FINAL_COLLISION,):
        raise AssertionError(f"M46 predecessor changed: {predecessor_buckets}")
    if len(set(signatures)) != len(primes):
        raise AssertionError("M46 construction certificate collides")

    patterns, repair_checks = _repair_patterns()
    if patterns != {(1, 0): (REPAIR_SOURCE,)}:
        raise AssertionError(f"M46 repair patterns changed: {patterns}")
    if repair_checks != 81112:
        raise AssertionError("M46 repair-coordinate count changed")
    tracked_indices = tuple(primes.index(prime) for prime in FINAL_COLLISION)
    tracked_predecessor = tuple(
        predecessor_signatures[index] for index in tracked_indices
    )
    if len(set(tracked_predecessor)) != 1:
        raise AssertionError("M46 predecessor pair no longer collides")

    public_by_cap = {int(record["selector_cap"]): record for record in public}
    counts = {
        "input_lengths": 1,
        "public_cap_profiles": len(public),
        "transition_cap_profiles": len(transitions),
        "balanced_primes": len(primes),
        "balanced_prime_pairs": pair_count,
        "public_cap_maximum_descriptors": int(
            public_by_cap[MULTIPLICATIVE_CAP]["descriptor_count"]
        ),
        "public_partition_local_exit_checks": int(
            public_by_cap[MULTIPLICATIVE_CAP]["optimized_local_exit_checks"]
        ),
        "repair_partition_local_exit_checks": int(
            transitions[-1]["optimized_local_exit_checks"]
        ),
        "transition_new_descriptors": (
            int(transitions[-1]["descriptor_count"])
            - int(transitions[0]["descriptor_count"])
        ),
        "transition_full_local_exit_profiles": (
            (
                int(transitions[-1]["descriptor_count"])
                - int(transitions[0]["descriptor_count"])
            )
            * len(MULTIPLICATIVE_COLLISION)
        ),
        "repair_cap_descriptors": int(transitions[-1]["descriptor_count"]),
        "repair_cap_raw_coordinates": int(
            transitions[-1]["raw_coordinate_count"]
        ),
        "predecessor_coordinate_count": len(predecessor_sources),
        "minimum_new_coordinate_count": 1,
        "construction_coordinates": len(sources),
        "construction_local_exit_profiles": len(sources) * len(primes),
        "certificate_pair_checks": pair_count,
        "repair_raw_coordinate_checks": repair_checks,
    }
    summary: dict[str, object] = {
        "schema_version": "1.0.0",
        "experiment_id": "EXP-0045",
        "input_length": INPUT_LENGTH,
        "registered_public_profiles": public,
        "additive_failed_profile": public_by_cap[ADDITIVE_CAP],
        "multiplicative_failed_profile": public_by_cap[MULTIPLICATIVE_CAP],
        "transition_profiles": transitions,
        "predecessor_profile": transitions[-2],
        "repair_profile": transitions[-1],
        "exact_length_34_threshold": REPAIR_CAP,
        "partition_refinement_invariant": (
            "After each descriptor, the retained buckets are exactly the "
            "non-singleton raw-signature equivalence classes; discarded "
            "singletons cannot merge under coordinate appending."
        ),
        "construction_certificate": {
            "input_length": INPUT_LENGTH,
            "selector_cap": REPAIR_CAP,
            "primes": primes,
            "column_sources": sources,
            "restricted_signatures": signatures,
            "predecessor_column_count": len(predecessor_sources),
            "tracked_primes": FINAL_COLLISION,
            "tracked_predecessor_signatures": tracked_predecessor,
            "new_source_patterns": ((1, 0),),
            "tracked_repair_signatures": (1, 0),
            "minimum_new_coordinate_count": 1,
            "repair_sources": (REPAIR_SOURCE,),
        },
        "repaired_additive_schedule": {
            "cap": "m+167",
            "minimal_integer_offset_through_34": 167,
            "length_34_slack": 0,
        },
        "repaired_multiplicative_schedule": {
            "admissible_coefficients_through_34": "c>100/17",
            "infimum": "100/17",
            "length_34_local_endpoint": "100/17",
            "working_witness": "ceil(53m/9)",
            "witness_gap": "1/153",
            "length_34_slack": 0,
        },
        "counts": counts,
        "status": "PASS",
    }
    canonical = json.dumps(summary, sort_keys=True, separators=(",", ":"))
    summary["summary_sha256"] = hashlib.sha256(
        canonical.encode("utf-8")
    ).hexdigest()
    return summary


def main() -> int:
    summary = build_summary()
    counts = summary["counts"]
    if not isinstance(counts, dict):
        raise AssertionError("M46 counts have the wrong shape")
    print(
        "M46 length-34 cap audit: PASS "
        f"(threshold={summary['exact_length_34_threshold']}, "
        f"summary_sha256={summary['summary_sha256']}, "
        f"construction_coordinates={counts['construction_coordinates']})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
