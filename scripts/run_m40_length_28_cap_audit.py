"""Deterministic M40 audit of the length-28 finite envelope."""

from __future__ import annotations

import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "python"))
from mosef_reference import (
    ExceptionalSelectorDescriptor,
    diversified_exceptional_selector,
    diversified_selector_profile,
    primitive_exit_mask,
)
from mosef_reference.diversified_compact_signatures import (
    PRIMITIVE_EXIT_KINDS,
)

from scripts.run_m32_widened_selector_cap_audit import (
    assert_normalization_equivalence,
)

INPUT_LENGTH = 28
ADDITIVE_CAP = 88
MULTIPLICATIVE_CAP = 90
PREDECESSOR_CAP = 103
REPAIR_CAP = 104
TRACKED_PRIMES = (11867, 12791, 13633, 13967, 14051, 15559)
FINAL_COLLISION = (11867, 12791)
ADDITIONAL_SOURCES = (
    (ExceptionalSelectorDescriptor("phi4", 95, 35, 7), "cofactor"),
    (ExceptionalSelectorDescriptor("phi6", 59, 75, 92), "cofactor"),
    (ExceptionalSelectorDescriptor("phi4", 55, 27, 97), "cofactor"),
    (ExceptionalSelectorDescriptor("phi4", 31, 43, 91), "cofactor"),
    (ExceptionalSelectorDescriptor("phi4", 15, 99, 104), "cofactor"),
)
EXPECTED_SOURCE_CAPS = (95, 92, 97, 91, 104)
EXPECTED_NEW_PATTERNS = (
    (0, 0, 0, 0, 0, 1),
    (0, 0, 0, 0, 1, 0),
    (0, 0, 0, 1, 0, 0),
    (0, 0, 1, 0, 0, 0),
    (0, 1, 0, 0, 0, 0),
)
EXPECTED_PROFILE = (
    507,
    58464,
    467712,
    908,
    502,
    15,
    6,
    (TRACKED_PRIMES,),
)
EXPECTED_TRANSITIONS = {
    88: (58464, 0, 15, (TRACKED_PRIMES,)),
    89: (60456, 1992, 15, (TRACKED_PRIMES,)),
    90: (61143, 687, 15, (TRACKED_PRIMES,)),
    91: (65790, 4647, 10, ((11867, 12791, 13967, 14051, 15559),)),
    92: (66521, 731, 6, ((11867, 12791, 13967, 15559),)),
    93: (68632, 2111, 6, ((11867, 12791, 13967, 15559),)),
    94: (69378, 746, 6, ((11867, 12791, 13967, 15559),)),
    95: (75952, 6574, 3, ((11867, 12791, 13967),)),
    96: (76760, 808, 3, ((11867, 12791, 13967),)),
    97: (77568, 808, 1, (FINAL_COLLISION,)),
    98: (78376, 808, 1, (FINAL_COLLISION,)),
    99: (85456, 7080, 1, (FINAL_COLLISION,)),
    100: (86328, 872, 1, (FINAL_COLLISION,)),
    101: (88900, 2572, 1, (FINAL_COLLISION,)),
    102: (89789, 889, 1, (FINAL_COLLISION,)),
    103: (95778, 5989, 1, (FINAL_COLLISION,)),
    104: (96717, 939, 0, ()),
}


def _source_hit(
    descriptor: ExceptionalSelectorDescriptor,
    kind: str,
    prime: int,
) -> bool:
    """Evaluate one primitive support coordinate."""
    kind_index = PRIMITIVE_EXIT_KINDS.index(kind)
    return bool(primitive_exit_mask(descriptor, prime) & (1 << kind_index))


def _transition_records(
    old_descriptors: tuple[ExceptionalSelectorDescriptor, ...],
) -> tuple[tuple[dict[str, object], ...], dict[str, int]]:
    """Refine the complete cap-88 bucket using only newly added descriptors."""
    previous_keys = {descriptor.key for descriptor in old_descriptors}
    signatures = {prime: bytearray() for prime in TRACKED_PRIMES}
    first_caps: dict[str, int] = {}
    records: list[dict[str, object]] = [
        {
            "selector_cap": ADDITIVE_CAP,
            "descriptor_count": len(old_descriptors),
            "new_descriptor_count": 0,
            "tracked_population_size": len(TRACKED_PRIMES),
            "collision_pair_count": 15,
            "collision_buckets": (TRACKED_PRIMES,),
        }
    ]

    for cap in range(ADDITIVE_CAP + 1, REPAIR_CAP + 1):
        descriptors = diversified_exceptional_selector(INPUT_LENGTH, cap)
        current_keys = {descriptor.key for descriptor in descriptors}
        if not previous_keys <= current_keys:
            raise AssertionError("M40 raw selector inclusion failed")
        added = tuple(
            descriptor
            for descriptor in descriptors
            if descriptor.key not in previous_keys
        )
        for descriptor in added:
            first_caps.setdefault(descriptor.key, cap)
        for prime in TRACKED_PRIMES:
            signatures[prime].extend(
                primitive_exit_mask(descriptor, prime)
                for descriptor in added
            )

        grouped: defaultdict[bytes, list[int]] = defaultdict(list)
        for prime in TRACKED_PRIMES:
            grouped[bytes(signatures[prime])].append(prime)
        buckets = tuple(
            tuple(bucket) for bucket in grouped.values() if len(bucket) > 1
        )
        collision_pairs = sum(
            len(bucket) * (len(bucket) - 1) // 2 for bucket in buckets
        )
        observed = (
            len(descriptors),
            len(added),
            collision_pairs,
            buckets,
        )
        if observed != EXPECTED_TRANSITIONS[cap]:
            raise AssertionError(
                f"registered M40 transition changed: cap={cap}, {observed}"
            )
        records.append(
            {
                "selector_cap": cap,
                "descriptor_count": len(descriptors),
                "new_descriptor_count": len(added),
                "tracked_population_size": len(TRACKED_PRIMES),
                "collision_pair_count": collision_pairs,
                "collision_buckets": buckets,
            }
        )
        previous_keys = current_keys
    return tuple(records), first_caps


def _repair_pattern_audit(
    old_keys: set[str],
    first_caps: dict[str, int],
) -> tuple[int, tuple[tuple[int, ...], ...]]:
    """Audit every nonconstant new primitive pattern on the tracked bucket."""
    patterns: set[tuple[int, ...]] = set()
    raw_nonconstant = 0
    for descriptor in diversified_exceptional_selector(
        INPUT_LENGTH,
        REPAIR_CAP,
    ):
        if descriptor.key in old_keys:
            continue
        masks = tuple(
            primitive_exit_mask(descriptor, prime)
            for prime in TRACKED_PRIMES
        )
        for kind_index in range(len(PRIMITIVE_EXIT_KINDS)):
            pattern = tuple(
                int(bool(mask & (1 << kind_index))) for mask in masks
            )
            if len(set(pattern)) == 1:
                continue
            raw_nonconstant += 1
            patterns.add(pattern)

    observed_patterns = tuple(sorted(patterns))
    if observed_patterns != tuple(sorted(EXPECTED_NEW_PATTERNS)):
        raise AssertionError(
            f"registered M40 repair pattern family changed: {observed_patterns}"
        )
    if raw_nonconstant != 14:
        raise AssertionError(
            f"registered M40 nonconstant raw count changed: {raw_nonconstant}"
        )
    for (descriptor, kind), expected_cap, expected_pattern in zip(
        ADDITIONAL_SOURCES,
        EXPECTED_SOURCE_CAPS,
        EXPECTED_NEW_PATTERNS,
        strict=True,
    ):
        if first_caps.get(descriptor.key) != expected_cap:
            raise AssertionError("registered M40 repair source cap changed")
        pattern = tuple(
            int(_source_hit(descriptor, kind, prime))
            for prime in TRACKED_PRIMES
        )
        if pattern != expected_pattern:
            raise AssertionError("registered M40 repair source changed")
    return raw_nonconstant, observed_patterns


def build_summary() -> dict[str, object]:
    """Run the complete cap-88, transition, and repair audit."""
    if ADDITIVE_CAP != INPUT_LENGTH + 60:
        raise AssertionError("registered M40 additive schedule changed")
    if MULTIPLICATIVE_CAP != (16 * INPUT_LENGTH + 4) // 5:
        raise AssertionError("registered M40 multiplicative schedule changed")
    if REPAIR_CAP != (26 * INPUT_LENGTH + 6) // 7:
        raise AssertionError("registered M40 succeeding witness changed")

    profile = diversified_selector_profile(
        INPUT_LENGTH,
        ADDITIVE_CAP,
        compute_minimum_certificate=False,
    )
    observed_profile = (
        len(profile.population_primes),
        profile.descriptor_count,
        profile.raw_coordinate_count,
        len(profile.normalized_columns),
        profile.distinct_signature_count,
        profile.collision_pair_count,
        profile.maximum_bucket_size,
        profile.collision_buckets,
    )
    if observed_profile != EXPECTED_PROFILE:
        raise AssertionError(
            f"registered M40 cap-88 profile changed: {observed_profile}"
        )

    old_descriptors = diversified_exceptional_selector(
        INPUT_LENGTH,
        ADDITIVE_CAP,
    )
    transition_profiles, first_caps = _transition_records(old_descriptors)
    predecessor = transition_profiles[PREDECESSOR_CAP - ADDITIVE_CAP]
    if predecessor["collision_buckets"] != (FINAL_COLLISION,):
        raise AssertionError("registered M40 predecessor changed")

    old_keys = {descriptor.key for descriptor in old_descriptors}
    raw_nonconstant, distinct_patterns = _repair_pattern_audit(
        old_keys,
        first_caps,
    )
    old_coordinate_count = len(profile.normalized_columns)
    signatures = tuple(
        signature
        | sum(
            1 << (old_coordinate_count + source_index)
            for source_index, (descriptor, kind) in enumerate(
                ADDITIONAL_SOURCES
            )
            if _source_hit(descriptor, kind, prime)
        )
        for prime, signature in zip(
            profile.population_primes,
            profile.signatures,
            strict=True,
        )
    )
    if len(set(signatures)) != len(signatures):
        raise AssertionError("cap-104 incremental certificate is not injective")
    tracked_patterns = tuple(
        tuple(
            int(_source_hit(descriptor, kind, prime))
            for prime in TRACKED_PRIMES
        )
        for descriptor, kind in ADDITIONAL_SOURCES
    )
    tracked_signatures = tuple(
        sum(
            pattern[prime_index] << source_index
            for source_index, pattern in enumerate(tracked_patterns)
        )
        for prime_index in range(len(TRACKED_PRIMES))
    )
    if tracked_signatures != (0, 16, 8, 4, 2, 1):
        raise AssertionError("registered M40 tracked signatures changed")

    construction_sources = tuple(
        column.source_keys[0] for column in profile.normalized_columns
    ) + tuple(
        f"{descriptor.key}:{kind}" for descriptor, kind in ADDITIONAL_SOURCES
    )
    transition_new_descriptors = sum(
        int(record["new_descriptor_count"])
        for record in transition_profiles[1:]
    )
    counts = {
        "input_lengths": 1,
        "full_cap_profiles": 1,
        "transition_cap_profiles": len(transition_profiles),
        "balanced_primes": len(profile.population_primes),
        "descriptors": profile.descriptor_count,
        "local_exit_profiles": (
            profile.descriptor_count * len(profile.population_primes)
        ),
        "raw_coordinates": profile.raw_coordinate_count,
        "normalized_coordinates": len(profile.normalized_columns),
        "normalization_pair_checks": assert_normalization_equivalence(profile),
        "transition_new_descriptors": transition_new_descriptors,
        "transition_local_exit_profiles": (
            transition_new_descriptors * len(TRACKED_PRIMES)
        ),
        "transition_raw_coordinate_checks": (
            transition_new_descriptors * len(PRIMITIVE_EXIT_KINDS)
        ),
        "transition_pair_checks": (
            len(transition_profiles)
            * len(TRACKED_PRIMES)
            * (len(TRACKED_PRIMES) - 1)
            // 2
        ),
        "repair_raw_nonconstant_coordinates": raw_nonconstant,
        "repair_distinct_nonconstant_patterns": len(distinct_patterns),
        "new_repair_coordinates": len(ADDITIONAL_SOURCES),
        "certificate_pair_checks": profile.pair_count,
    }
    cap_profile = {
        "selector_cap": ADDITIVE_CAP,
        "population_size": len(profile.population_primes),
        "descriptor_count": profile.descriptor_count,
        "raw_coordinate_count": profile.raw_coordinate_count,
        "constant_coordinate_count": profile.constant_coordinate_count,
        "duplicate_coordinate_count": profile.duplicate_coordinate_count,
        "normalized_coordinate_count": len(profile.normalized_columns),
        "distinct_signature_count": profile.distinct_signature_count,
        "collision_pair_count": profile.collision_pair_count,
        "collision_buckets": profile.collision_buckets,
    }
    repair_profile = {
        "selector_cap": REPAIR_CAP,
        "population_size": len(profile.population_primes),
        "descriptor_count": int(transition_profiles[-1]["descriptor_count"]),
        "construction_coordinate_count": len(construction_sources),
        "new_repair_coordinate_count": len(ADDITIONAL_SOURCES),
        "distinct_signature_count": len(set(signatures)),
        "collision_pair_count": 0,
        "collision_buckets": (),
    }
    summary: dict[str, object] = {
        "schema_version": "1.0.0",
        "experiment_id": "EXP-0039",
        "input_length": INPUT_LENGTH,
        "failed_schedules": {
            "m_plus_60": ADDITIVE_CAP,
            "ceil_16m_over_5": MULTIPLICATIVE_CAP,
        },
        "cap_profile": cap_profile,
        "transition_profiles": transition_profiles,
        "additive_failed_profile": cap_profile,
        "multiplicative_failed_profile": transition_profiles[
            MULTIPLICATIVE_CAP - ADDITIVE_CAP
        ],
        "predecessor_profile": predecessor,
        "repair_profile": repair_profile,
        "construction_certificate": {
            "input_length": INPUT_LENGTH,
            "selector_cap": REPAIR_CAP,
            "primes": profile.population_primes,
            "column_sources": construction_sources,
            "restricted_signatures": signatures,
            "tracked_primes": TRACKED_PRIMES,
            "new_source_patterns": tracked_patterns,
            "tracked_restricted_signatures": tracked_signatures,
            "minimum_new_coordinate_count": len(ADDITIONAL_SOURCES),
        },
        "continued_additive_schedule": {
            "cap": "m+76",
            "minimal_integer_offset_through_28": 76,
        },
        "continued_multiplicative_schedule": {
            "admissible_coefficients_through_28": "c>103/28",
            "infimum": "103/28",
            "working_witness": "ceil(26m/7)",
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
    """Print the registered M40 summary."""
    print(json.dumps(build_summary(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
