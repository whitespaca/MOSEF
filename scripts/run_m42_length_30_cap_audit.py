"""Deterministic M42 audit of the length-30 finite envelope."""

from __future__ import annotations

import hashlib
import json
import sys
from collections import defaultdict
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "python"))

from mosef_reference import (
    ExceptionalSelectorDescriptor,
    balanced_prime_population,
    diversified_exceptional_selector,
    diversified_selector_profile,
    primitive_exit_mask,
)
from mosef_reference.diversified_compact_signatures import (
    PRIMITIVE_EXIT_KINDS,
    DiversifiedSelectorProfile,
    _primitive_exit_mask_from_resultant,
)
from mosef_reference.exceptional_cofactor_schedule import (
    exceptional_cofactor_overlap,
)

INPUT_LENGTH = 30
ADDITIVE_CAP = 106
MULTIPLICATIVE_CAP = 112
PREDECESSOR_CAP = 122
REPAIR_CAP = 123
ADDITIVE_COLLISION = (
    26297,
    27701,
    28447,
    28591,
    29131,
    29209,
    29387,
    30817,
    31177,
    31327,
    31723,
    31849,
    32027,
    32633,
)
TRACKED_PRIMES = (
    26297,
    27701,
    28591,
    29209,
    29387,
    30817,
    31177,
    31849,
    32027,
)
FINAL_COLLISION = (28591, 29209, 29387)
EXPECTED_RAW_PROFILES = {
    ADDITIVE_CAP: (
        100380,
        914,
        91,
        14,
        (ADDITIVE_COLLISION,),
    ),
    MULTIPLICATIVE_CAP: (
        121878,
        919,
        36,
        9,
        (TRACKED_PRIMES,),
    ),
}
EXPECTED_TRANSITIONS = {
    113: (125104, 3226, 36, (TRACKED_PRIMES,)),
    114: (126221, 1117, 36, (TRACKED_PRIMES,)),
    115: (
        133722,
        7501,
        21,
        ((26297, 28591, 29209, 29387, 30817, 31177, 31849),),
    ),
    116: (
        134895,
        1173,
        21,
        ((26297, 28591, 29209, 29387, 30817, 31177, 31849),),
    ),
    117: (
        138272,
        3377,
        21,
        ((26297, 28591, 29209, 29387, 30817, 31177, 31849),),
    ),
    118: (
        139464,
        1192,
        15,
        ((26297, 28591, 29209, 29387, 30817, 31849),),
    ),
    119: (
        149860,
        10396,
        10,
        ((26297, 28591, 29209, 29387, 31849),),
    ),
    120: (
        151130,
        1270,
        10,
        ((26297, 28591, 29209, 29387, 31849),),
    ),
    121: (152400, 1270, 3, (FINAL_COLLISION,)),
    122: (153670, 1270, 3, (FINAL_COLLISION,)),
    123: (164700, 11030, 0, ()),
}
EXPECTED_REPAIR_PROFILE = (
    927,
    164700,
    1317600,
    1264248,
    50849,
    2503,
    927,
    0,
    1,
    (),
)


def _descriptor_first_cap(descriptor: ExceptionalSelectorDescriptor) -> int:
    """Return the first public cap containing one descriptor at length 30."""
    return max(
        INPUT_LENGTH,
        descriptor.first_factor,
        descriptor.second_factor,
        descriptor.base,
    )


def _source_hit(
    descriptor: ExceptionalSelectorDescriptor,
    kind: str,
    prime: int,
) -> bool:
    """Evaluate one primitive support coordinate."""
    kind_index = PRIMITIVE_EXIT_KINDS.index(kind)
    return bool(primitive_exit_mask(descriptor, prime) & (1 << kind_index))


def _complete_raw_prefix_audit(
    primes: tuple[int, ...],
) -> tuple[dict[str, object], ...]:
    """Evaluate exact lossless raw signatures once through public cap 112."""
    descriptors = diversified_exceptional_selector(
        INPUT_LENGTH,
        MULTIPLICATIVE_CAP,
    )
    by_first_cap: defaultdict[
        int,
        list[ExceptionalSelectorDescriptor],
    ] = defaultdict(list)
    for descriptor in descriptors:
        by_first_cap[_descriptor_first_cap(descriptor)].append(descriptor)

    signatures = {prime: bytearray() for prime in primes}
    records: list[dict[str, object]] = []
    descriptor_count = 0
    selected = {ADDITIVE_CAP, MULTIPLICATIVE_CAP}
    for cap in range(INPUT_LENGTH, MULTIPLICATIVE_CAP + 1):
        for descriptor in by_first_cap[cap]:
            overlap_resultant = exceptional_cofactor_overlap(
                descriptor.first_factor,
                descriptor.second_factor,
                descriptor.family,
            ).cyclotomic_cofactor_resultant
            for prime in primes:
                signatures[prime].append(
                    _primitive_exit_mask_from_resultant(
                        descriptor,
                        prime,
                        overlap_resultant,
                    )
                )
            descriptor_count += 1
        if cap not in selected:
            continue

        grouped: defaultdict[bytes, list[int]] = defaultdict(list)
        for prime in primes:
            grouped[bytes(signatures[prime])].append(prime)
        buckets = tuple(
            tuple(bucket) for bucket in grouped.values() if len(bucket) > 1
        )
        collision_pairs = sum(
            len(bucket) * (len(bucket) - 1) // 2 for bucket in buckets
        )
        maximum_bucket_size = max(map(len, grouped.values()))
        observed = (
            descriptor_count,
            len(grouped),
            collision_pairs,
            maximum_bucket_size,
            buckets,
        )
        if observed != EXPECTED_RAW_PROFILES[cap]:
            raise AssertionError(
                f"registered M42 raw profile changed: cap={cap}, {observed}"
            )
        records.append(
            {
                "selector_cap": cap,
                "population_size": len(primes),
                "descriptor_count": descriptor_count,
                "raw_coordinate_count": (
                    descriptor_count * len(PRIMITIVE_EXIT_KINDS)
                ),
                "distinct_signature_count": len(grouped),
                "collision_pair_count": collision_pairs,
                "maximum_bucket_size": maximum_bucket_size,
                "collision_buckets": buckets,
            }
        )
    if descriptor_count != len(descriptors):
        raise AssertionError("M42 raw selector inclusion accounting changed")
    return tuple(records)


def _transition_records() -> tuple[dict[str, object], ...]:
    """Refine only the complete cap-112 collision bucket through cap 123."""
    old = diversified_exceptional_selector(INPUT_LENGTH, MULTIPLICATIVE_CAP)
    previous_keys = {descriptor.key for descriptor in old}
    signatures = {prime: bytearray() for prime in TRACKED_PRIMES}
    records: list[dict[str, object]] = [
        {
            "selector_cap": MULTIPLICATIVE_CAP,
            "descriptor_count": len(old),
            "new_descriptor_count": 0,
            "tracked_population_size": len(TRACKED_PRIMES),
            "collision_pair_count": 36,
            "collision_buckets": (TRACKED_PRIMES,),
        }
    ]
    for cap in range(MULTIPLICATIVE_CAP + 1, REPAIR_CAP + 1):
        descriptors = diversified_exceptional_selector(INPUT_LENGTH, cap)
        current_keys = {descriptor.key for descriptor in descriptors}
        if not previous_keys <= current_keys:
            raise AssertionError("M42 raw selector inclusion failed")
        added = tuple(
            descriptor
            for descriptor in descriptors
            if descriptor.key not in previous_keys
        )
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
                f"registered M42 transition changed: cap={cap}, {observed}"
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
    return tuple(records)


def _old_construction_sources(
    profile: DiversifiedSelectorProfile,
    old_keys: set[str],
) -> tuple[tuple[str, ...], tuple[int, ...]]:
    """Select one cap-122 source for every old normalized support mask."""
    source_keys: list[str] = []
    support_masks: list[int] = []
    for column in profile.normalized_columns:
        old_source = next(
            (
                source
                for source in column.source_keys
                if source.rsplit(":", 1)[0] in old_keys
            ),
            None,
        )
        if old_source is None:
            continue
        source_keys.append(old_source)
        support_masks.append(column.support_mask)
    return tuple(source_keys), tuple(support_masks)


def _new_repair_patterns(
    old_keys: set[str],
) -> tuple[dict[tuple[int, ...], tuple[str, ...]], int]:
    """Audit every new cap-123 primitive pattern on the final triple."""
    sources_by_pattern: defaultdict[tuple[int, ...], list[str]] = defaultdict(
        list
    )
    raw_checks = 0
    for descriptor in diversified_exceptional_selector(
        INPUT_LENGTH,
        REPAIR_CAP,
    ):
        if descriptor.key in old_keys:
            continue
        masks = tuple(
            primitive_exit_mask(descriptor, prime)
            for prime in FINAL_COLLISION
        )
        for kind_index, kind in enumerate(PRIMITIVE_EXIT_KINDS):
            pattern = tuple(
                int(bool(mask & (1 << kind_index))) for mask in masks
            )
            if len(set(pattern)) > 1:
                sources_by_pattern[pattern].append(
                    f"{descriptor.key}:{kind}"
                )
            raw_checks += 1
    return (
        {
            pattern: tuple(sources)
            for pattern, sources in sources_by_pattern.items()
        },
        raw_checks,
    )


def build_summary() -> dict[str, object]:
    """Run the complete raw, transition, normalized, and repair audit."""
    if ADDITIVE_CAP != INPUT_LENGTH + 76:
        raise AssertionError("registered M42 additive schedule changed")
    if MULTIPLICATIVE_CAP != (26 * INPUT_LENGTH + 6) // 7:
        raise AssertionError("registered M42 multiplicative schedule changed")

    primes = balanced_prime_population(INPUT_LENGTH)
    if len(primes) != 927:
        raise AssertionError("registered M42 balanced population changed")
    raw_profiles = _complete_raw_prefix_audit(primes)
    profiles_by_cap = {
        int(record["selector_cap"]): record for record in raw_profiles
    }
    transitions = _transition_records()

    profile = diversified_selector_profile(
        INPUT_LENGTH,
        REPAIR_CAP,
        compute_minimum_certificate=False,
    )
    observed_profile = (
        len(profile.population_primes),
        profile.descriptor_count,
        profile.raw_coordinate_count,
        profile.constant_coordinate_count,
        profile.duplicate_coordinate_count,
        len(profile.normalized_columns),
        profile.distinct_signature_count,
        profile.collision_pair_count,
        profile.maximum_bucket_size,
        profile.collision_buckets,
    )
    if observed_profile != EXPECTED_REPAIR_PROFILE:
        raise AssertionError(
            f"registered M42 repair profile changed: {observed_profile}"
        )
    if profile.population_primes != primes:
        raise AssertionError("M42 population order changed")

    old_descriptors = diversified_exceptional_selector(
        INPUT_LENGTH,
        PREDECESSOR_CAP,
    )
    old_keys = {descriptor.key for descriptor in old_descriptors}
    construction_sources, construction_masks = _old_construction_sources(
        profile,
        old_keys,
    )
    patterns, new_raw_checks = _new_repair_patterns(old_keys)
    expected_patterns = {
        (0, 0, 1): ("phi4:123:59:87:cofactor",),
        (1, 0, 0): ("phi4:79:123:54:cofactor",),
    }
    if patterns != expected_patterns:
        raise AssertionError(
            f"registered M42 repair patterns changed: {patterns}"
        )

    pattern_keys = tuple(sorted(patterns))
    selected_patterns: tuple[tuple[int, ...], ...] | None = None
    for size in range(1, len(pattern_keys) + 1):
        for candidate in combinations(pattern_keys, size):
            signatures = tuple(
                tuple(pattern[index] for pattern in candidate)
                for index in range(len(FINAL_COLLISION))
            )
            if len(set(signatures)) == len(FINAL_COLLISION):
                selected_patterns = candidate
                break
        if selected_patterns is not None:
            break
    if selected_patterns != ((0, 0, 1), (1, 0, 0)):
        raise AssertionError("registered M42 minimum repair changed")

    repair_sources = tuple(patterns[pattern][0] for pattern in selected_patterns)
    for source in repair_sources:
        descriptor_key, kind = source.rsplit(":", 1)
        family, first, second, base = descriptor_key.split(":")
        descriptor = ExceptionalSelectorDescriptor(
            family,
            int(first),
            int(second),
            int(base),
        )
        support_mask = sum(
            1 << prime_index
            for prime_index, prime in enumerate(primes)
            if _source_hit(descriptor, kind, prime)
        )
        if support_mask in construction_masks:
            raise AssertionError("M42 repair support already existed at cap 122")
        construction_sources += (source,)
        construction_masks += (support_mask,)

    restricted_signatures = tuple(
        sum(
            1 << column_index
            for column_index, support_mask in enumerate(construction_masks)
            if support_mask & (1 << prime_index)
        )
        for prime_index in range(len(primes))
    )
    if len(set(restricted_signatures)) != len(primes):
        raise AssertionError("M42 incremental construction is not injective")
    tracked_signatures = tuple(
        restricted_signatures[primes.index(prime)]
        for prime in FINAL_COLLISION
    )
    tracked_repair_signatures = tuple(
        sum(
            pattern[index] << pattern_index
            for pattern_index, pattern in enumerate(selected_patterns)
        )
        for index in range(len(FINAL_COLLISION))
    )
    if tracked_repair_signatures != (2, 0, 1):
        raise AssertionError("registered M42 repair signatures changed")

    pair_count = len(primes) * (len(primes) - 1) // 2
    transition_new_descriptors = sum(
        int(record["new_descriptor_count"]) for record in transitions[1:]
    )
    counts = {
        "input_lengths": 1,
        "raw_prefix_profiles": len(raw_profiles),
        "transition_cap_profiles": len(transitions),
        "full_normalized_profiles": 1,
        "balanced_primes": len(primes),
        "public_cap_maximum_descriptors": int(
            profiles_by_cap[MULTIPLICATIVE_CAP]["descriptor_count"]
        ),
        "raw_prefix_local_exit_profiles": (
            int(profiles_by_cap[MULTIPLICATIVE_CAP]["descriptor_count"])
            * len(primes)
        ),
        "transition_new_descriptors": transition_new_descriptors,
        "transition_local_exit_profiles": (
            transition_new_descriptors * len(TRACKED_PRIMES)
        ),
        "transition_pair_checks": (
            len(transitions) * len(TRACKED_PRIMES)
            * (len(TRACKED_PRIMES) - 1)
            // 2
        ),
        "repair_cap_descriptors": profile.descriptor_count,
        "repair_cap_local_exit_profiles": (
            profile.descriptor_count * len(primes)
        ),
        "repair_cap_raw_coordinates": profile.raw_coordinate_count,
        "repair_cap_normalized_coordinates": len(
            profile.normalized_columns
        ),
        "normalization_pair_checks": pair_count,
        "predecessor_to_repair_new_descriptors": (
            profile.descriptor_count - len(old_descriptors)
        ),
        "predecessor_repair_raw_coordinate_checks": new_raw_checks,
        "predecessor_distinct_repair_patterns": len(patterns),
        "minimum_new_coordinate_count": len(selected_patterns),
        "construction_coordinates": len(construction_sources),
        "certificate_pair_checks": pair_count,
    }
    summary: dict[str, object] = {
        "schema_version": "1.0.0",
        "experiment_id": "EXP-0041",
        "input_length": INPUT_LENGTH,
        "registered_raw_profiles": raw_profiles,
        "additive_failed_profile": profiles_by_cap[ADDITIVE_CAP],
        "multiplicative_failed_profile": profiles_by_cap[MULTIPLICATIVE_CAP],
        "transition_profiles": transitions,
        "predecessor_profile": transitions[-2],
        "repair_profile": {
            "selector_cap": REPAIR_CAP,
            "population_size": len(primes),
            "descriptor_count": profile.descriptor_count,
            "raw_coordinate_count": profile.raw_coordinate_count,
            "constant_coordinate_count": profile.constant_coordinate_count,
            "duplicate_coordinate_count": profile.duplicate_coordinate_count,
            "normalized_coordinate_count": len(
                profile.normalized_columns
            ),
            "distinct_signature_count": profile.distinct_signature_count,
            "collision_pair_count": profile.collision_pair_count,
            "maximum_bucket_size": profile.maximum_bucket_size,
            "collision_buckets": profile.collision_buckets,
        },
        "exact_length_30_threshold": REPAIR_CAP,
        "construction_certificate": {
            "input_length": INPUT_LENGTH,
            "selector_cap": REPAIR_CAP,
            "primes": primes,
            "column_sources": construction_sources,
            "restricted_signatures": restricted_signatures,
            "tracked_primes": FINAL_COLLISION,
            "new_source_patterns": selected_patterns,
            "tracked_repair_signatures": tracked_repair_signatures,
            "tracked_restricted_signatures": tracked_signatures,
            "minimum_new_coordinate_count": len(selected_patterns),
            "repair_sources": repair_sources,
        },
        "repaired_additive_schedule": {
            "cap": "m+93",
            "minimal_integer_offset_through_30": 93,
            "length_30_slack": 0,
        },
        "repaired_multiplicative_schedule": {
            "admissible_coefficients_through_30": "c>61/15",
            "infimum": "61/15",
            "length_30_local_endpoint": "61/15",
            "working_witness": "ceil(49m/12)",
            "length_30_slack": 0,
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
    """Print the registered M42 summary."""
    print(json.dumps(build_summary(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
