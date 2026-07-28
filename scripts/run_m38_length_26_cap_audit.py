"""Deterministic M38 audit of the length-26 finite envelope."""

from __future__ import annotations

import hashlib
import json
import sys
from collections import defaultdict
from itertools import pairwise
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
    collision_pairs,
)

INPUT_LENGTH = 26
ADDITIVE_CAP = 66
MULTIPLICATIVE_CAP = 67
PREDECESSOR_CAP = 70
REPAIR_CAP = 71
TRACKED_PRIMES = (6229, 6703, 6793, 6947, 7187, 7229, 7649)
FINAL_COLLISION = (7187, 7229, 7649)
ADDITIONAL_SOURCES = (
    (ExceptionalSelectorDescriptor("phi4", 7, 71, 65), "cofactor"),
    (ExceptionalSelectorDescriptor("phi4", 19, 71, 50), "cofactor"),
)
EXPECTED_PROFILES = {
    66: (
        268,
        23465,
        187720,
        540,
        262,
        21,
        7,
        (TRACKED_PRIMES,),
    ),
    67: (
        268,
        25938,
        207504,
        561,
        266,
        3,
        3,
        (FINAL_COLLISION,),
    ),
}
EXPECTED_TRANSITION_BUCKETS = {
    66: (TRACKED_PRIMES,),
    67: (FINAL_COLLISION,),
    68: (FINAL_COLLISION,),
    69: (FINAL_COLLISION,),
    70: (FINAL_COLLISION,),
    71: (),
}


def _source_hit(
    descriptor: ExceptionalSelectorDescriptor,
    kind: str,
    prime: int,
) -> bool:
    """Evaluate one primitive support coordinate."""
    kind_index = PRIMITIVE_EXIT_KINDS.index(kind)
    return bool(primitive_exit_mask(descriptor, prime) & (1 << kind_index))


def _tracked_collision_record(selector_cap: int) -> dict[str, object]:
    """Return collisions induced on the complete cap-66 collision bucket."""
    descriptors = diversified_exceptional_selector(
        INPUT_LENGTH,
        selector_cap,
    )
    by_signature: defaultdict[tuple[int, ...], list[int]] = defaultdict(list)
    for prime in TRACKED_PRIMES:
        signature = tuple(
            primitive_exit_mask(descriptor, prime)
            for descriptor in descriptors
        )
        by_signature[signature].append(prime)
    collision_buckets = tuple(
        tuple(bucket) for bucket in by_signature.values() if len(bucket) > 1
    )
    if collision_buckets != EXPECTED_TRANSITION_BUCKETS[selector_cap]:
        raise AssertionError(
            "registered M38 transition changed: "
            f"cap={selector_cap}, buckets={collision_buckets}"
        )
    return {
        "selector_cap": selector_cap,
        "descriptor_count": len(descriptors),
        "tracked_population_size": len(TRACKED_PRIMES),
        "collision_pair_count": sum(
            len(bucket) * (len(bucket) - 1) // 2
            for bucket in collision_buckets
        ),
        "collision_buckets": collision_buckets,
    }


def build_summary() -> dict[str, object]:
    """Run the complete distinct-schedule, transition, and repair audit."""
    if ADDITIVE_CAP != INPUT_LENGTH + 40:
        raise AssertionError("registered M38 additive schedule changed")
    if MULTIPLICATIVE_CAP != (257 * INPUT_LENGTH + 99) // 100:
        raise AssertionError("registered M38 multiplicative schedule changed")
    if PREDECESSOR_CAP != (35 * INPUT_LENGTH + 12) // 13:
        raise AssertionError("registered M38 strict endpoint changed")
    if REPAIR_CAP != (27 * INPUT_LENGTH + 9) // 10:
        raise AssertionError("registered M38 succeeding witness changed")

    caps = (ADDITIVE_CAP, MULTIPLICATIVE_CAP)
    profiles = tuple(
        diversified_selector_profile(
            INPUT_LENGTH,
            cap,
            compute_minimum_certificate=False,
        )
        for cap in caps
    )
    for cap, profile in zip(caps, profiles, strict=True):
        observed = (
            len(profile.population_primes),
            profile.descriptor_count,
            profile.raw_coordinate_count,
            len(profile.normalized_columns),
            profile.distinct_signature_count,
            profile.collision_pair_count,
            profile.maximum_bucket_size,
            profile.collision_buckets,
        )
        if observed != EXPECTED_PROFILES[cap]:
            raise AssertionError(
                f"registered M38 cap-{cap} profile changed: {observed}"
            )

    pair_count = profiles[-1].pair_count
    monotonicity_pair_checks = 0
    for lower, upper in pairwise(profiles):
        if not collision_pairs(upper.signatures).issubset(
            collision_pairs(lower.signatures)
        ):
            raise AssertionError(
                "a widened M38 selector merged an already separated pair"
            )
        monotonicity_pair_checks += pair_count

    transition_profiles = tuple(
        _tracked_collision_record(cap)
        for cap in range(ADDITIVE_CAP, REPAIR_CAP + 1)
    )
    predecessor = transition_profiles[PREDECESSOR_CAP - ADDITIVE_CAP]
    if predecessor["collision_buckets"] != (FINAL_COLLISION,):
        raise AssertionError("registered M38 predecessor changed")

    multiplicative = profiles[-1]
    old_descriptor_keys = {
        descriptor.key
        for descriptor in diversified_exceptional_selector(
            INPUT_LENGTH,
            MULTIPLICATIVE_CAP,
        )
    }
    for descriptor, kind in ADDITIONAL_SOURCES:
        if descriptor.key in old_descriptor_keys:
            raise AssertionError("M38 repair coordinate is not new")
        if kind not in PRIMITIVE_EXIT_KINDS:
            raise AssertionError("M38 repair coordinate kind changed")

    old_coordinate_count = len(multiplicative.normalized_columns)
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
            multiplicative.population_primes,
            multiplicative.signatures,
            strict=True,
        )
    )
    if len(set(signatures)) != len(signatures):
        raise AssertionError("cap-71 incremental certificate is not injective")
    final_patterns = tuple(
        tuple(
            int(_source_hit(descriptor, kind, prime))
            for prime in FINAL_COLLISION
        )
        for descriptor, kind in ADDITIONAL_SOURCES
    )
    if final_patterns != ((0, 0, 1), (0, 1, 0)):
        raise AssertionError("registered M38 repair patterns changed")

    transition_descriptor_checks = sum(
        int(record["descriptor_count"])
        for record in transition_profiles
        if MULTIPLICATIVE_CAP < int(record["selector_cap"]) <= REPAIR_CAP
    )
    counts = {
        "input_lengths": 1,
        "full_cap_profiles": len(profiles),
        "transition_cap_profiles": len(transition_profiles),
        "balanced_primes": len(multiplicative.population_primes),
        "descriptors": sum(profile.descriptor_count for profile in profiles),
        "local_exit_profiles": sum(
            profile.descriptor_count * len(profile.population_primes)
            for profile in profiles
        ),
        "raw_coordinates": sum(
            profile.raw_coordinate_count for profile in profiles
        ),
        "normalized_coordinates": sum(
            len(profile.normalized_columns) for profile in profiles
        ),
        "monotonicity_pair_checks": monotonicity_pair_checks,
        "normalization_pair_checks": sum(
            assert_normalization_equivalence(profile) for profile in profiles
        ),
        "transition_descriptor_checks": transition_descriptor_checks,
        "transition_local_exit_profiles": (
            transition_descriptor_checks * len(TRACKED_PRIMES)
        ),
        "new_repair_coordinates": len(ADDITIONAL_SOURCES),
        "certificate_pair_checks": pair_count,
    }
    cap_profiles = tuple(
        {
            "selector_cap": cap,
            "population_size": len(profile.population_primes),
            "descriptor_count": profile.descriptor_count,
            "raw_coordinate_count": profile.raw_coordinate_count,
            "normalized_coordinate_count": len(profile.normalized_columns),
            "distinct_signature_count": profile.distinct_signature_count,
            "collision_pair_count": profile.collision_pair_count,
            "collision_buckets": profile.collision_buckets,
        }
        for cap, profile in zip(caps, profiles, strict=True)
    )
    construction_sources = tuple(
        column.source_keys[0] for column in multiplicative.normalized_columns
    ) + tuple(
        f"{descriptor.key}:{kind}" for descriptor, kind in ADDITIONAL_SOURCES
    )
    repair_profile = {
        "selector_cap": REPAIR_CAP,
        "population_size": len(multiplicative.population_primes),
        "descriptor_count": int(
            transition_profiles[REPAIR_CAP - ADDITIVE_CAP][
                "descriptor_count"
            ]
        ),
        "construction_coordinate_count": len(construction_sources),
        "new_repair_coordinate_count": len(ADDITIONAL_SOURCES),
        "distinct_signature_count": len(set(signatures)),
        "collision_pair_count": 0,
        "collision_buckets": (),
    }
    summary: dict[str, object] = {
        "schema_version": "1.0.0",
        "experiment_id": "EXP-0037",
        "input_length": INPUT_LENGTH,
        "failed_schedules": {
            "m_plus_40": ADDITIVE_CAP,
            "ceil_257m_over_100": MULTIPLICATIVE_CAP,
        },
        "cap_profiles": cap_profiles,
        "transition_profiles": transition_profiles,
        "additive_failed_profile": cap_profiles[0],
        "multiplicative_failed_profile": cap_profiles[1],
        "predecessor_profile": predecessor,
        "repair_profile": repair_profile,
        "construction_certificate": {
            "input_length": INPUT_LENGTH,
            "selector_cap": REPAIR_CAP,
            "primes": multiplicative.population_primes,
            "column_sources": construction_sources,
            "restricted_signatures": signatures,
            "new_source_patterns_on_final_collision": final_patterns,
        },
        "continued_additive_schedule": {
            "cap": "m+45",
            "minimal_integer_offset_through_26": 45,
        },
        "continued_multiplicative_schedule": {
            "admissible_coefficients_through_26": "c>35/13",
            "infimum": "35/13",
            "working_witness": "ceil(27m/10)",
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
    """Print the registered M38 summary."""
    print(json.dumps(build_summary(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
