"""Deterministic M39 audit of the length-27 finite envelope."""

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

INPUT_LENGTH = 27
ADDITIVE_CAP = 72
MULTIPLICATIVE_CAP = 73
PREDECESSOR_CAP = 86
REPAIR_CAP = 87
TRACKED_PRIMES = (9463, 9791, 10607, 10939, 11087, 11213)
FINAL_COLLISION = (10607, 10939)
ADDITIONAL_SOURCES = (
    (ExceptionalSelectorDescriptor("phi4", 11, 15, 73), "second_stage"),
    (ExceptionalSelectorDescriptor("phi4", 15, 87, 83), "cofactor"),
    (ExceptionalSelectorDescriptor("phi4", 63, 75, 24), "cofactor"),
    (ExceptionalSelectorDescriptor("phi6", 35, 75, 46), "cofactor"),
    (ExceptionalSelectorDescriptor("phi6", 53, 81, 78), "cofactor"),
)
EXPECTED_SOURCE_CAPS = (73, 87, 75, 75, 81)
EXPECTED_NEW_PATTERNS = (
    (0, 1, 0, 0, 0, 0),
    (0, 0, 0, 1, 0, 0),
    (1, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 1, 0),
    (0, 0, 0, 0, 0, 1),
)
EXPECTED_PROFILE = (
    365,
    31950,
    255600,
    625,
    360,
    15,
    6,
    (TRACKED_PRIMES,),
)
EXPECTED_TRANSITIONS = {
    72: (31950, 0, 15, (TRACKED_PRIMES,)),
    73: (32400, 450, 10, ((9463, 10607, 10939, 11087, 11213),)),
    74: (32850, 450, 10, ((9463, 10607, 10939, 11087, 11213),)),
    75: (36852, 4002, 3, ((10607, 10939, 11213),)),
    76: (37350, 498, 3, ((10607, 10939, 11213),)),
    77: (38836, 1486, 3, ((10607, 10939, 11213),)),
    78: (39347, 511, 3, ((10607, 10939, 11213),)),
    79: (42822, 3475, 3, ((10607, 10939, 11213),)),
    80: (43371, 549, 3, ((10607, 10939, 11213),)),
    81: (44960, 1589, 1, (FINAL_COLLISION,)),
    82: (45522, 562, 1, (FINAL_COLLISION,)),
    83: (50512, 4990, 1, (FINAL_COLLISION,)),
    84: (51128, 616, 1, (FINAL_COLLISION,)),
    85: (51744, 616, 1, (FINAL_COLLISION,)),
    86: (52360, 616, 1, (FINAL_COLLISION,)),
    87: (57792, 5432, 0, ()),
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
    """Refine the complete cap-72 bucket using only newly added descriptors."""
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
            raise AssertionError("M39 raw selector inclusion failed")
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
                f"registered M39 transition changed: cap={cap}, {observed}"
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
            f"registered M39 repair pattern family changed: {observed_patterns}"
        )
    if raw_nonconstant != 235:
        raise AssertionError(
            f"registered M39 nonconstant raw count changed: {raw_nonconstant}"
        )
    for (descriptor, kind), expected_cap, expected_pattern in zip(
        ADDITIONAL_SOURCES,
        EXPECTED_SOURCE_CAPS,
        EXPECTED_NEW_PATTERNS,
        strict=True,
    ):
        if first_caps.get(descriptor.key) != expected_cap:
            raise AssertionError("registered M39 repair source cap changed")
        pattern = tuple(
            int(_source_hit(descriptor, kind, prime))
            for prime in TRACKED_PRIMES
        )
        if pattern != expected_pattern:
            raise AssertionError("registered M39 repair source changed")
    return raw_nonconstant, observed_patterns


def build_summary() -> dict[str, object]:
    """Run the complete cap-72, transition, and repair audit."""
    if ADDITIVE_CAP != INPUT_LENGTH + 45:
        raise AssertionError("registered M39 additive schedule changed")
    if MULTIPLICATIVE_CAP != (27 * INPUT_LENGTH + 9) // 10:
        raise AssertionError("registered M39 multiplicative schedule changed")
    if REPAIR_CAP != (16 * INPUT_LENGTH + 4) // 5:
        raise AssertionError("registered M39 succeeding witness changed")

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
            f"registered M39 cap-72 profile changed: {observed_profile}"
        )

    old_descriptors = diversified_exceptional_selector(
        INPUT_LENGTH,
        ADDITIVE_CAP,
    )
    transition_profiles, first_caps = _transition_records(old_descriptors)
    predecessor = transition_profiles[PREDECESSOR_CAP - ADDITIVE_CAP]
    if predecessor["collision_buckets"] != (FINAL_COLLISION,):
        raise AssertionError("registered M39 predecessor changed")

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
        raise AssertionError("cap-87 incremental certificate is not injective")
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
    if tracked_signatures != (4, 1, 0, 2, 8, 16):
        raise AssertionError("registered M39 tracked signatures changed")

    construction_sources = tuple(
        column.source_keys[0] for column in profile.normalized_columns
    ) + tuple(
        f"{descriptor.key}:{kind}" for descriptor, kind in ADDITIONAL_SOURCES
    )
    pair_count = profile.pair_count
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
        "certificate_pair_checks": pair_count,
    }
    cap_profile = {
        "selector_cap": ADDITIVE_CAP,
        "population_size": len(profile.population_primes),
        "descriptor_count": profile.descriptor_count,
        "raw_coordinate_count": profile.raw_coordinate_count,
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
        "experiment_id": "EXP-0038",
        "input_length": INPUT_LENGTH,
        "failed_schedules": {
            "m_plus_45": ADDITIVE_CAP,
            "ceil_27m_over_10": MULTIPLICATIVE_CAP,
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
            "cap": "m+60",
            "minimal_integer_offset_through_27": 60,
        },
        "continued_multiplicative_schedule": {
            "admissible_coefficients_through_27": "c>86/27",
            "infimum": "86/27",
            "working_witness": "ceil(16m/5)",
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
    """Print the registered M39 summary."""
    print(json.dumps(build_summary(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
