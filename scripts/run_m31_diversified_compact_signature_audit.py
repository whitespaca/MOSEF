"""Deterministic M31 audit of a diversified exceptional-family selector."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
from mosef_reference import (
    diversified_exceptional_selector,
    diversified_selector_profile,
    primitive_exit_mask,
)

EXPECTED_PROFILES = {
    9: (2, 32, 2, 2, 0, 1),
    10: (3, 36, 3, 3, 0, 2),
    11: (3, 100, 4, 3, 0, 2),
    12: (4, 110, 4, 4, 0, 3),
    13: (6, 120, 9, 6, 0, 4),
    14: (7, 130, 7, 7, 0, 6),
    15: (11, 252, 12, 11, 0, 10),
    16: (12, 270, 10, 10, 3, 0),
    17: (18, 336, 21, 16, 2, 0),
    18: (25, 357, 22, 21, 10, 0),
    19: (31, 522, 25, 21, 55, 0),
    20: (44, 551, 33, 30, 105, 0),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-length-min", type=int, default=9)
    parser.add_argument("--input-length-max", type=int, default=20)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if (args.input_length_min, args.input_length_max) != (9, 20):
        raise ValueError("the registered M31 audit requires lengths 9 through 20")

    counts = {
        "input_lengths": 0,
        "balanced_primes": 0,
        "descriptors": 0,
        "local_exit_profiles": 0,
        "raw_coordinates": 0,
        "normalized_coordinates": 0,
        "normalization_pair_checks": 0,
        "minimal_certificate_pair_checks": 0,
        "cofactor_novel_pairs": 0,
        "cross_length_collision_pairs": 0,
    }
    profile_records: list[dict[str, object]] = []
    construction_certificates: list[dict[str, object]] = []
    collision_certificates: list[dict[str, object]] = []

    for input_length in range(
        args.input_length_min,
        args.input_length_max + 1,
    ):
        profile = diversified_selector_profile(input_length)
        descriptors = diversified_exceptional_selector(input_length)
        expected = EXPECTED_PROFILES[input_length]
        minimum_size = len(
            profile.minimum_separating_column_indices or ()
        )
        observed = (
            len(profile.population_primes),
            profile.descriptor_count,
            len(profile.normalized_columns),
            profile.distinct_signature_count,
            profile.collision_pair_count,
            minimum_size,
        )
        if observed != expected:
            raise AssertionError(
                f"registered M31 profile changed at length {input_length}: "
                f"{observed} != {expected}"
            )

        if profile.injective != (input_length <= 15):
            raise AssertionError("finite construction boundary changed")
        if profile.injective != (
            profile.collision_pair_count == 0
            and profile.distinct_signature_count
            == len(profile.population_primes)
        ):
            raise AssertionError("injectivity accounting disagrees")
        if (
            profile.raw_coordinate_count
            != profile.constant_coordinate_count
            + profile.duplicate_coordinate_count
            + len(profile.normalized_columns)
        ):
            raise AssertionError("normalization did not partition coordinates")

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
                    raise AssertionError(
                        "normalization changed pair separation"
                    )
                counts["normalization_pair_checks"] += 1

        counts["input_lengths"] += 1
        counts["balanced_primes"] += len(profile.population_primes)
        counts["descriptors"] += profile.descriptor_count
        counts["local_exit_profiles"] += (
            profile.descriptor_count * len(profile.population_primes)
        )
        counts["raw_coordinates"] += profile.raw_coordinate_count
        counts["normalized_coordinates"] += len(profile.normalized_columns)
        counts["cofactor_novel_pairs"] += profile.cofactor_novel_pair_count
        counts["cross_length_collision_pairs"] += (
            profile.collision_pair_count
        )

        record = {
            "input_length": input_length,
            "population_size": len(profile.population_primes),
            "descriptor_count": profile.descriptor_count,
            "raw_coordinate_count": profile.raw_coordinate_count,
            "constant_coordinate_count": profile.constant_coordinate_count,
            "duplicate_coordinate_count": profile.duplicate_coordinate_count,
            "normalized_coordinate_count": len(profile.normalized_columns),
            "distinct_signature_count": profile.distinct_signature_count,
            "collision_pair_count": profile.collision_pair_count,
            "maximum_bucket_size": profile.maximum_bucket_size,
            "cofactor_novel_column_count": (
                profile.cofactor_novel_column_count
            ),
            "cofactor_novel_pair_count": profile.cofactor_novel_pair_count,
        }
        profile_records.append(record)

        if profile.injective:
            indices = profile.minimum_separating_column_indices
            if indices is None:
                raise AssertionError("injective profile lacks a certificate")
            restricted_signatures = tuple(
                sum(
                    1 << output_index
                    for output_index, column_index in enumerate(indices)
                    if profile.normalized_columns[
                        column_index
                    ].support_mask
                    & (1 << prime_index)
                )
                for prime_index in range(len(profile.population_primes))
            )
            if len(set(restricted_signatures)) != len(
                profile.population_primes
            ):
                raise AssertionError("minimal construction is not injective")
            counts["minimal_certificate_pair_checks"] += profile.pair_count
            construction_certificates.append(
                {
                    "input_length": input_length,
                    "primes": profile.population_primes,
                    "column_indices": indices,
                    "column_sources": tuple(
                        profile.normalized_columns[index].source_keys[0]
                        for index in indices
                    ),
                    "restricted_signatures": restricted_signatures,
                }
            )
        else:
            if not profile.collision_buckets:
                raise AssertionError("noninjective profile lacks a collision")
            collision_certificates.append(
                {
                    "input_length": input_length,
                    "collision_buckets": profile.collision_buckets,
                }
            )

    summary: dict[str, object] = {
        "schema_version": "1.0.0",
        "experiment_id": "EXP-0030",
        "selector": {
            "families": ("phi4", "phi6"),
            "parameter_interval": "2..m",
            "base_interval": "2..m",
            "primitive_exit_kinds": (
                "base",
                "first_stage",
                "second_stage",
                "first_public_bound",
                "second_public_bound",
                "cyclotomic",
                "overlap_resultant",
                "cofactor",
            ),
        },
        "counts": counts,
        "profiles": profile_records,
        "construction_certificates": construction_certificates,
        "collision_certificates": collision_certificates,
        "status": "PASS",
    }
    canonical = json.dumps(summary, sort_keys=True, separators=(",", ":"))
    summary["summary_sha256"] = hashlib.sha256(
        canonical.encode("utf-8")
    ).hexdigest()
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
