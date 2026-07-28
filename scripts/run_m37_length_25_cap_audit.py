"""Deterministic M37 audit of the length-25 finite envelope."""

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
    diversified_exceptional_selector,
    diversified_selector_profile,
    greedy_separating_column_indices,
    primitive_exit_mask,
)

from scripts.run_m32_widened_selector_cap_audit import (
    assert_normalization_equivalence,
    collision_pairs,
    restricted_signatures,
)

INPUT_LENGTH = 25
ADDITIVE_CAP = 52
MULTIPLICATIVE_CAP = 53
PREDECESSOR_CAP = 64
REPAIR_CAP = 65
TRACKED_PRIMES = (
    4133,
    4297,
    4337,
    4423,
    4663,
    5011,
    5179,
    5233,
    5297,
)
EXPECTED_PROFILES = {
    52: (
        196,
        11628,
        93024,
        311,
        188,
        36,
        9,
        (TRACKED_PRIMES,),
    ),
    53: (
        196,
        12324,
        98592,
        320,
        189,
        28,
        8,
        ((4297, 4337, 4423, 4663, 5011, 5179, 5233, 5297),),
    ),
    65: (196, 23104, 184832, 437, 196, 0, 1, ()),
}
EXPECTED_TRANSITION_BUCKETS = {
    52: (TRACKED_PRIMES,),
    53: ((4297, 4337, 4423, 4663, 5011, 5179, 5233, 5297),),
    54: ((4297, 4337, 4423, 4663, 5011, 5179, 5233, 5297),),
    55: ((4297, 4337, 4423, 5011, 5179, 5233),),
    56: ((4297, 4423, 5011, 5179, 5233),),
    57: ((4297, 4423, 5011, 5179, 5233),),
    58: ((4297, 4423, 5011, 5179, 5233),),
    59: ((5011, 5179, 5233),),
    60: ((5011, 5179, 5233),),
    61: ((5011, 5179, 5233),),
    62: ((5011, 5179, 5233),),
    63: ((5011, 5179),),
    64: ((5011, 5179),),
    65: (),
}


def _tracked_collision_record(selector_cap: int) -> dict[str, object]:
    """Return collisions induced on the complete cap-52 collision bucket."""
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
            "registered M37 transition changed: "
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
    if ADDITIVE_CAP != INPUT_LENGTH + 27:
        raise AssertionError("registered M37 additive schedule changed")
    if MULTIPLICATIVE_CAP != (209 * INPUT_LENGTH + 99) // 100:
        raise AssertionError("registered M37 multiplicative schedule changed")
    if PREDECESSOR_CAP != (64 * INPUT_LENGTH + 24) // 25:
        raise AssertionError("registered M37 strict endpoint changed")
    if REPAIR_CAP != (257 * INPUT_LENGTH + 99) // 100:
        raise AssertionError("registered M37 succeeding witness changed")

    caps = (ADDITIVE_CAP, MULTIPLICATIVE_CAP, REPAIR_CAP)
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
                f"registered M37 cap-{cap} profile changed: {observed}"
            )

    pair_count = profiles[-1].pair_count
    monotonicity_pair_checks = 0
    for lower, upper in pairwise(profiles):
        if not collision_pairs(upper.signatures).issubset(
            collision_pairs(lower.signatures)
        ):
            raise AssertionError(
                "a widened M37 selector merged an already separated pair"
            )
        monotonicity_pair_checks += pair_count

    transition_profiles = tuple(
        _tracked_collision_record(cap)
        for cap in range(ADDITIVE_CAP, REPAIR_CAP + 1)
    )
    predecessor = transition_profiles[PREDECESSOR_CAP - ADDITIVE_CAP]
    if predecessor["collision_buckets"] != ((5011, 5179),):
        raise AssertionError("registered M37 predecessor changed")

    repaired = profiles[-1]
    if not repaired.injective:
        raise AssertionError("registered M37 repair is not injective")
    indices = greedy_separating_column_indices(repaired)
    if indices is None:
        raise AssertionError("cap-65 profile lacks a certificate")
    signatures = restricted_signatures(repaired, indices)
    if len(set(signatures)) != len(signatures):
        raise AssertionError("cap-65 certificate is not injective")

    transition_descriptor_checks = sum(
        int(record["descriptor_count"])
        for record in transition_profiles
        if MULTIPLICATIVE_CAP < int(record["selector_cap"]) < REPAIR_CAP
    )
    counts = {
        "input_lengths": 1,
        "full_cap_profiles": len(profiles),
        "transition_cap_profiles": len(transition_profiles),
        "balanced_primes": len(repaired.population_primes),
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
    summary: dict[str, object] = {
        "schema_version": "1.0.0",
        "experiment_id": "EXP-0036",
        "input_length": INPUT_LENGTH,
        "failed_schedules": {
            "m_plus_27": ADDITIVE_CAP,
            "ceil_209m_over_100": MULTIPLICATIVE_CAP,
        },
        "cap_profiles": cap_profiles,
        "transition_profiles": transition_profiles,
        "additive_failed_profile": cap_profiles[0],
        "multiplicative_failed_profile": cap_profiles[1],
        "predecessor_profile": predecessor,
        "repair_profile": cap_profiles[-1],
        "construction_certificate": {
            "input_length": INPUT_LENGTH,
            "selector_cap": REPAIR_CAP,
            "primes": repaired.population_primes,
            "column_sources": tuple(
                repaired.normalized_columns[index].source_keys[0]
                for index in indices
            ),
            "restricted_signatures": signatures,
        },
        "continued_additive_schedule": {
            "cap": "m+40",
            "minimal_integer_offset_through_25": 40,
        },
        "continued_multiplicative_schedule": {
            "admissible_coefficients_through_25": "c>64/25",
            "infimum": "64/25",
            "working_witness": "ceil(257m/100)",
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
    """Print the registered M37 summary."""
    print(json.dumps(build_summary(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
