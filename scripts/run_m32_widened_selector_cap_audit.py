"""Deterministic M32 audit of widened public exceptional-selector caps."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
from mosef_reference import (
    DiversifiedSelectorProfile,
    diversified_exceptional_selector,
    diversified_selector_profile,
    greedy_separating_column_indices,
    primitive_exit_mask,
)

EXPECTED_THRESHOLDS = {
    16: {
        "cap": 19,
        "before": (357, 10, 10, 3, ((191, 227, 233),)),
        "at": (522, 16, 12, 0),
    },
    17: {
        "cap": 19,
        "before": (357, 21, 16, 2, ((277, 317), (263, 349))),
        "at": (522, 24, 18, 0),
    },
    18: {
        "cap": 27,
        "before": (1150, 33, 24, 1, ((503, 509),)),
        "at": (1612, 42, 25, 0),
    },
    19: {
        "cap": 27,
        "before": (1150, 44, 30, 1, ((569, 719),)),
        "at": (1612, 47, 31, 0),
    },
    20: {
        "cap": 31,
        "before": (1943, 56, 43, 1, ((809, 827),)),
        "at": (2430, 59, 44, 0),
    },
}


def collision_pairs(signatures: tuple[int, ...]) -> set[tuple[int, int]]:
    """Return all colliding population-index pairs."""
    return {
        (first, second)
        for first in range(len(signatures))
        for second in range(first + 1, len(signatures))
        if signatures[first] == signatures[second]
    }


def restricted_signatures(
    profile: DiversifiedSelectorProfile,
    indices: tuple[int, ...],
) -> tuple[int, ...]:
    """Pack signatures on a selected normalized-column certificate."""
    columns = profile.normalized_columns
    return tuple(
        sum(
            1 << output_index
            for output_index, column_index in enumerate(indices)
            if columns[column_index].support_mask & (1 << prime_index)
        )
        for prime_index in range(len(profile.population_primes))
    )


def assert_normalization_equivalence(
    profile: DiversifiedSelectorProfile,
) -> int:
    """Check raw versus normalized separation on every population pair."""
    descriptors = diversified_exceptional_selector(
        profile.input_length,
        profile.selector_cap,
    )
    checks = 0
    for first_index, first_prime in enumerate(profile.population_primes):
        for second_index in range(
            first_index + 1,
            len(profile.population_primes),
        ):
            second_prime = profile.population_primes[second_index]
            raw_separates = any(
                primitive_exit_mask(descriptor, first_prime)
                != primitive_exit_mask(descriptor, second_prime)
                for descriptor in descriptors
            )
            normalized_separates = (
                profile.signatures[first_index]
                != profile.signatures[second_index]
            )
            if raw_separates != normalized_separates:
                raise AssertionError("normalization changed pair separation")
            checks += 1
    return checks


def build_summary() -> dict[str, object]:
    """Run the complete registered audit and return its summary."""
    counts = {
        "input_lengths": len(EXPECTED_THRESHOLDS),
        "cap_profiles": 0,
        "descriptors": 0,
        "local_exit_profiles": 0,
        "raw_coordinates": 0,
        "normalized_coordinates": 0,
        "monotonicity_pair_checks": 0,
        "normalization_pair_checks": 0,
        "certificate_pair_checks": 0,
    }
    records: list[dict[str, object]] = []
    certificates: list[dict[str, object]] = []

    for input_length, expected in EXPECTED_THRESHOLDS.items():
        threshold = int(expected["cap"])
        previous_collisions: set[tuple[int, int]] | None = None
        threshold_profile = None
        predecessor_profile = None
        for selector_cap in range(input_length, threshold + 1):
            profile = diversified_selector_profile(
                input_length,
                selector_cap,
                compute_minimum_certificate=False,
            )
            collisions = collision_pairs(profile.signatures)
            if previous_collisions is not None:
                if not collisions.issubset(previous_collisions):
                    raise AssertionError(
                        "a widened selector merged a previously separated pair"
                    )
                counts["monotonicity_pair_checks"] += profile.pair_count
            previous_collisions = collisions
            counts["cap_profiles"] += 1
            counts["descriptors"] += profile.descriptor_count
            counts["local_exit_profiles"] += (
                profile.descriptor_count * len(profile.population_primes)
            )
            counts["raw_coordinates"] += profile.raw_coordinate_count
            counts["normalized_coordinates"] += len(profile.normalized_columns)
            if selector_cap < threshold and profile.injective:
                raise AssertionError("registered threshold is not minimal")
            if selector_cap == threshold:
                threshold_profile = profile
            if selector_cap == threshold - 1:
                predecessor_profile = profile

        if threshold_profile is None or predecessor_profile is None:
            raise AssertionError("threshold profiles were not constructed")
        before_observed = (
            predecessor_profile.descriptor_count,
            len(predecessor_profile.normalized_columns),
            predecessor_profile.distinct_signature_count,
            predecessor_profile.collision_pair_count,
            predecessor_profile.collision_buckets,
        )
        at_observed = (
            threshold_profile.descriptor_count,
            len(threshold_profile.normalized_columns),
            threshold_profile.distinct_signature_count,
            threshold_profile.collision_pair_count,
        )
        if before_observed != expected["before"]:
            raise AssertionError(
                f"pre-threshold profile changed at m={input_length}: "
                f"{before_observed} != {expected['before']}"
            )
        if at_observed != expected["at"] or not threshold_profile.injective:
            raise AssertionError(
                f"threshold profile changed at m={input_length}: "
                f"{at_observed} != {expected['at']}"
            )
        counts["normalization_pair_checks"] += (
            assert_normalization_equivalence(predecessor_profile)
            + assert_normalization_equivalence(threshold_profile)
        )

        indices = greedy_separating_column_indices(threshold_profile)
        if indices is None:
            raise AssertionError("injective profile lacks a certificate")
        signatures = restricted_signatures(threshold_profile, indices)
        if len(set(signatures)) != len(signatures):
            raise AssertionError("greedy construction certificate collides")
        counts["certificate_pair_checks"] += threshold_profile.pair_count

        records.append(
            {
                "input_length": input_length,
                "minimal_selector_cap": threshold,
                "additive_offset": threshold - input_length,
                "population_size": len(threshold_profile.population_primes),
                "predecessor_collision_buckets": (
                    predecessor_profile.collision_buckets
                ),
                "threshold_descriptor_count": (
                    threshold_profile.descriptor_count
                ),
                "threshold_raw_coordinate_count": (
                    threshold_profile.raw_coordinate_count
                ),
                "threshold_normalized_coordinate_count": len(
                    threshold_profile.normalized_columns
                ),
                "certificate_size": len(indices),
            }
        )
        certificates.append(
            {
                "input_length": input_length,
                "selector_cap": threshold,
                "primes": threshold_profile.population_primes,
                "column_sources": tuple(
                    threshold_profile.normalized_columns[
                        index
                    ].source_keys[0]
                    for index in indices
                ),
                "restricted_signatures": signatures,
            }
        )

    additive_offset = max(
        int(record["additive_offset"]) for record in records
    )
    if additive_offset != 11:
        raise AssertionError("minimal common additive offset changed")
    if any(
        input_length + additive_offset
        < int(EXPECTED_THRESHOLDS[input_length]["cap"])
        for input_length in EXPECTED_THRESHOLDS
    ):
        raise AssertionError("registered additive schedule misses a threshold")
    failed_endpoint = diversified_selector_profile(
        20,
        20 + additive_offset - 1,
        compute_minimum_certificate=False,
    )
    if failed_endpoint.injective or failed_endpoint.collision_buckets != (
        (809, 827),
    ):
        raise AssertionError("additive minimality witness changed")

    multiplier_numerator = 151
    multiplier_denominator = 100
    if any(
        (
            multiplier_numerator * input_length
            + multiplier_denominator
            - 1
        )
        // multiplier_denominator
        < int(EXPECTED_THRESHOLDS[input_length]["cap"])
        for input_length in EXPECTED_THRESHOLDS
    ):
        raise AssertionError("registered multiplicative witness misses a threshold")
    closed_endpoint = diversified_selector_profile(
        20,
        (3 * 20 + 2 - 1) // 2,
        compute_minimum_certificate=False,
    )
    if closed_endpoint.injective or closed_endpoint.collision_buckets != (
        (809, 827),
    ):
        raise AssertionError("multiplicative infimum witness changed")

    summary: dict[str, object] = {
        "schema_version": "1.0.0",
        "experiment_id": "EXP-0031",
        "selector": {
            "families": ("phi4", "phi6"),
            "parameter_interval": "2..L(m)",
            "base_interval": "2..L(m)",
            "descriptor_upper_bound": "2(L(m)-1)^3",
        },
        "threshold_records": records,
        "construction_certificates": certificates,
        "common_additive_schedule": {
            "cap": "m+11",
            "minimal_integer_offset": 11,
            "failure_witness": {
                "input_length": 20,
                "selector_cap": 30,
                "collision_bucket": (809, 827),
            },
        },
        "multiplicative_schedule": {
            "working_witness": "ceil(151m/100)",
            "admissible_coefficients": "c>3/2",
            "infimum": "3/2",
            "closed_endpoint_failure": {
                "input_length": 20,
                "selector_cap": 30,
                "collision_bucket": (809, 827),
            },
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
    """Print the complete registered audit summary."""
    summary = build_summary()
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
