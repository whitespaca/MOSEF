"""Deterministic M34 audit of the next repaired linear-cap population."""

from __future__ import annotations

import hashlib
import json
import sys
from itertools import pairwise
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "python"))
from mosef_reference import (
    diversified_selector_profile,
    greedy_separating_column_indices,
)

from scripts.run_m32_widened_selector_cap_audit import (
    assert_normalization_equivalence,
    collision_pairs,
    restricted_signatures,
)

INPUT_LENGTH = 22
FAILED_CAP = 34
PREDECESSOR_CAP = 38
REPAIR_CAP = 39
EXPECTED_PROFILES = {
    34: (
        80,
        2838,
        22704,
        83,
        71,
        37,
        9,
        (
            (1481, 1511, 1571, 1663, 1721, 1747, 1867, 1931, 2029),
            (1907, 1999),
        ),
    ),
    35: (
        80,
        3672,
        29376,
        91,
        75,
        15,
        6,
        ((1481, 1571, 1721, 1747, 1867, 1931),),
    ),
    36: (
        80,
        3780,
        30240,
        94,
        76,
        10,
        5,
        ((1481, 1571, 1721, 1867, 1931),),
    ),
    37: (
        80,
        3888,
        31104,
        95,
        77,
        6,
        4,
        ((1481, 1571, 1721, 1867),),
    ),
    38: (
        80,
        3996,
        31968,
        100,
        79,
        1,
        2,
        ((1481, 1571),),
    ),
    39: (80, 5016, 40128, 115, 80, 0, 1, ()),
}


def build_summary() -> dict[str, object]:
    """Run the complete six-cap recurrence and repair audit."""
    profiles = tuple(
        diversified_selector_profile(
            INPUT_LENGTH,
            cap,
            compute_minimum_certificate=False,
        )
        for cap in range(FAILED_CAP, REPAIR_CAP + 1)
    )
    for cap, profile in zip(range(FAILED_CAP, REPAIR_CAP + 1), profiles):
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
                f"registered M34 cap-{cap} profile changed: {observed}"
            )

    pair_count = profiles[-1].pair_count
    monotonicity_pair_checks = 0
    for lower, upper in pairwise(profiles):
        if not collision_pairs(upper.signatures).issubset(
            collision_pairs(lower.signatures)
        ):
            raise AssertionError(
                "a widened M34 selector merged an already separated pair"
            )
        monotonicity_pair_checks += pair_count

    repaired = profiles[-1]
    if not repaired.injective:
        raise AssertionError("registered M34 repair is not injective")
    indices = greedy_separating_column_indices(repaired)
    if indices is None:
        raise AssertionError("cap-39 profile lacks a certificate")
    signatures = restricted_signatures(repaired, indices)
    if len(set(signatures)) != len(signatures):
        raise AssertionError("cap-39 certificate is not injective")

    counts = {
        "input_lengths": 1,
        "cap_profiles": len(profiles),
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
        for cap, profile in zip(
            range(FAILED_CAP, REPAIR_CAP + 1),
            profiles,
        )
    )
    summary: dict[str, object] = {
        "schema_version": "1.0.0",
        "experiment_id": "EXP-0033",
        "input_length": INPUT_LENGTH,
        "failed_schedules": {
            "m_plus_12": FAILED_CAP,
            "ceil_153m_over_100": FAILED_CAP,
        },
        "cap_profiles": cap_profiles,
        "failed_profile": cap_profiles[0],
        "predecessor_profile": cap_profiles[-2],
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
            "cap": "m+17",
            "minimal_integer_offset_through_22": 17,
        },
        "continued_multiplicative_schedule": {
            "admissible_coefficients_through_22": "c>19/11",
            "infimum": "19/11",
            "working_witness": "ceil(173m/100)",
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
    """Print the registered M34 summary."""
    print(json.dumps(build_summary(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
