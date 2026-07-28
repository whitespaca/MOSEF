"""Deterministic M41 audit of the length-29 finite envelope."""

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

INPUT_LENGTH = 29
PREDECESSOR_CAP = 102
REPAIR_CAP = 103
ADDITIVE_CAP = 105
MULTIPLICATIVE_CAP = 108
FINAL_COLLISION = (18979, 21031)
REPAIR_SOURCE = (
    ExceptionalSelectorDescriptor("phi4", 87, 95, 103),
    "cofactor",
)
SELECTED_CAPS = (
    PREDECESSOR_CAP,
    REPAIR_CAP,
    ADDITIVE_CAP,
    MULTIPLICATIVE_CAP,
)
EXPECTED_RAW_PROFILES = {
    PREDECESSOR_CAP: (
        89789,
        684,
        1,
        2,
        (FINAL_COLLISION,),
    ),
    REPAIR_CAP: (95778, 685, 0, 1, ()),
    ADDITIVE_CAP: (99424, 685, 0, 1, ()),
    MULTIPLICATIVE_CAP: (109782, 685, 0, 1, ()),
}
EXPECTED_REPAIR_PROFILE = (
    685,
    95778,
    766224,
    733526,
    31143,
    1555,
    685,
    0,
    1,
    (),
)


def _descriptor_first_cap(descriptor: ExceptionalSelectorDescriptor) -> int:
    """Return the first public cap containing one descriptor at length 29."""
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
    """Evaluate the exact raw selector once through cap 108.

    One byte stores all eight primitive charged exits for a descriptor.
    Equality of byte prefixes is therefore exactly equality of all raw
    support coordinates, without probabilistic hashing or normalization.
    """
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

    if sum(map(len, by_first_cap.values())) != len(descriptors):
        raise AssertionError("M41 descriptor first-cap partition changed")

    signatures = {prime: bytearray() for prime in primes}
    records: list[dict[str, object]] = []
    descriptor_count = 0
    selected = set(SELECTED_CAPS)
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
                f"registered M41 raw profile changed: cap={cap}, {observed}"
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
        raise AssertionError("M41 raw selector inclusion accounting changed")
    return tuple(records)


def _old_construction_sources(
    profile: DiversifiedSelectorProfile,
    old_keys: set[str],
) -> tuple[tuple[str, ...], tuple[int, ...]]:
    """Select one cap-102 source for every old normalized support mask."""
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


def build_summary() -> dict[str, object]:
    """Run the complete raw-prefix, normalized, and repair audit."""
    if ADDITIVE_CAP != INPUT_LENGTH + 76:
        raise AssertionError("registered M41 additive schedule changed")
    if MULTIPLICATIVE_CAP != (26 * INPUT_LENGTH + 6) // 7:
        raise AssertionError("registered M41 multiplicative schedule changed")

    primes = balanced_prime_population(INPUT_LENGTH)
    if len(primes) != 685:
        raise AssertionError("registered M41 balanced population changed")
    raw_profiles = _complete_raw_prefix_audit(primes)
    profiles_by_cap = {
        int(record["selector_cap"]): record for record in raw_profiles
    }

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
            f"registered M41 repair profile changed: {observed_profile}"
        )
    if profile.population_primes != primes:
        raise AssertionError("M41 population order changed")
    if (
        int(
            profiles_by_cap[REPAIR_CAP]["collision_pair_count"]
        )
        != profile.collision_pair_count
    ):
        raise AssertionError(
            "M41 raw and normalized pair relations disagree"
        )

    old_descriptors = diversified_exceptional_selector(
        INPUT_LENGTH,
        PREDECESSOR_CAP,
    )
    old_keys = {descriptor.key for descriptor in old_descriptors}
    construction_sources, construction_masks = _old_construction_sources(
        profile,
        old_keys,
    )
    repair_descriptor, repair_kind = REPAIR_SOURCE
    repair_pattern = tuple(
        int(_source_hit(repair_descriptor, repair_kind, prime))
        for prime in FINAL_COLLISION
    )
    if repair_pattern != (0, 1):
        raise AssertionError("registered M41 repair pattern changed")

    repair_support_mask = sum(
        1 << prime_index
        for prime_index, prime in enumerate(primes)
        if _source_hit(repair_descriptor, repair_kind, prime)
    )
    if repair_support_mask in construction_masks:
        raise AssertionError("M41 repair coordinate is not new at cap 103")
    construction_sources += (
        f"{repair_descriptor.key}:{repair_kind}",
    )
    construction_masks += (repair_support_mask,)
    if len(construction_sources) != 1528:
        raise AssertionError("registered M41 construction size changed")
    restricted_signatures = tuple(
        sum(
            1 << column_index
            for column_index, support_mask in enumerate(construction_masks)
            if support_mask & (1 << prime_index)
        )
        for prime_index in range(len(primes))
    )
    if len(set(restricted_signatures)) != len(primes):
        raise AssertionError("M41 incremental construction is not injective")
    tracked_signatures = tuple(
        sum(
            int(
                bool(
                    support_mask
                    & (1 << primes.index(prime))
                )
            )
            << column_index
            for column_index, support_mask in enumerate(construction_masks)
        )
        for prime in FINAL_COLLISION
    )
    if tracked_signatures[0] == tracked_signatures[1]:
        raise AssertionError("M41 repair source does not split predecessor")
    if tracked_signatures != (0, 1 << 1527):
        raise AssertionError(
            "registered M41 tracked construction signatures changed"
        )

    added_descriptors = tuple(
        descriptor
        for descriptor in diversified_exceptional_selector(
            INPUT_LENGTH,
            REPAIR_CAP,
        )
        if descriptor.key not in old_keys
    )
    nonconstant_pair_coordinates: list[str] = []
    for descriptor in added_descriptors:
        masks = tuple(
            primitive_exit_mask(descriptor, prime)
            for prime in FINAL_COLLISION
        )
        for kind_index, kind in enumerate(PRIMITIVE_EXIT_KINDS):
            pattern = tuple(
                int(bool(mask & (1 << kind_index))) for mask in masks
            )
            if pattern[0] != pattern[1]:
                nonconstant_pair_coordinates.append(
                    f"{descriptor.key}:{kind}"
                )
    expected_repair_source = f"{repair_descriptor.key}:{repair_kind}"
    if nonconstant_pair_coordinates != [expected_repair_source]:
        raise AssertionError(
            "registered M41 unique pair-repair coordinate changed"
        )

    pair_count = len(primes) * (len(primes) - 1) // 2
    counts = {
        "input_lengths": 1,
        "raw_prefix_profiles": len(raw_profiles),
        "full_normalized_profiles": 1,
        "balanced_primes": len(primes),
        "maximum_cap_descriptors": int(
            profiles_by_cap[MULTIPLICATIVE_CAP]["descriptor_count"]
        ),
        "raw_prefix_local_exit_profiles": (
            int(profiles_by_cap[MULTIPLICATIVE_CAP]["descriptor_count"])
            * len(primes)
        ),
        "repair_cap_descriptors": profile.descriptor_count,
        "repair_cap_local_exit_profiles": (
            profile.descriptor_count * len(primes)
        ),
        "repair_cap_raw_coordinates": profile.raw_coordinate_count,
        "repair_cap_normalized_coordinates": len(
            profile.normalized_columns
        ),
        # Both exact signature families are injective on the same ordered
        # population, so every unordered pair is separated in each.
        "normalization_pair_checks": pair_count,
        "predecessor_to_repair_new_descriptors": len(added_descriptors),
        "predecessor_pair_new_local_exits": (
            len(added_descriptors) * len(FINAL_COLLISION)
        ),
        "predecessor_pair_new_raw_coordinate_checks": (
            len(added_descriptors) * len(PRIMITIVE_EXIT_KINDS)
        ),
        "predecessor_pair_distinguishing_coordinates": len(
            nonconstant_pair_coordinates
        ),
        "construction_coordinates": len(construction_sources),
        "certificate_pair_checks": pair_count,
    }
    summary: dict[str, object] = {
        "schema_version": "1.0.0",
        "experiment_id": "EXP-0040",
        "input_length": INPUT_LENGTH,
        "registered_raw_profiles": raw_profiles,
        "predecessor_profile": profiles_by_cap[PREDECESSOR_CAP],
        "repair_profile": {
            "selector_cap": REPAIR_CAP,
            "population_size": len(primes),
            "descriptor_count": profile.descriptor_count,
            "raw_coordinate_count": profile.raw_coordinate_count,
            "constant_coordinate_count": profile.constant_coordinate_count,
            "duplicate_coordinate_count": profile.duplicate_coordinate_count,
            "normalized_coordinate_count": len(profile.normalized_columns),
            "distinct_signature_count": profile.distinct_signature_count,
            "collision_pair_count": profile.collision_pair_count,
            "maximum_bucket_size": profile.maximum_bucket_size,
            "collision_buckets": profile.collision_buckets,
        },
        "additive_success_profile": profiles_by_cap[ADDITIVE_CAP],
        "multiplicative_success_profile": profiles_by_cap[
            MULTIPLICATIVE_CAP
        ],
        "exact_length_29_threshold": REPAIR_CAP,
        "construction_certificate": {
            "input_length": INPUT_LENGTH,
            "selector_cap": REPAIR_CAP,
            "primes": primes,
            "column_sources": construction_sources,
            "restricted_signatures": restricted_signatures,
            "tracked_primes": FINAL_COLLISION,
            "new_source_pattern": repair_pattern,
            "tracked_restricted_signatures": tracked_signatures,
            "minimum_new_coordinate_count": 1,
            "unique_new_pair_source": expected_repair_source,
        },
        "continued_additive_schedule": {
            "cap": "m+76",
            "minimal_integer_offset_through_29": 76,
            "length_29_slack": ADDITIVE_CAP - REPAIR_CAP,
        },
        "continued_multiplicative_schedule": {
            "admissible_coefficients_through_29": "c>103/28",
            "infimum": "103/28",
            "length_29_local_endpoint": "102/29",
            "working_witness": "ceil(26m/7)",
            "length_29_slack": MULTIPLICATIVE_CAP - REPAIR_CAP,
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
    """Print the registered M41 summary."""
    print(json.dumps(build_summary(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
