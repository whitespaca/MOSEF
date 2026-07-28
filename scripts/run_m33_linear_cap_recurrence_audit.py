"""Deterministic M33 audit of the first post-M32 linear-cap population."""

from __future__ import annotations

import hashlib
import json
import sys
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

INPUT_LENGTH = 21
FAILED_CAP = 32
REPAIR_CAP = 33
EXPECTED_FAILED = (
    57,
    2511,
    20088,
    69,
    54,
    6,
    4,
    ((1031, 1231, 1319, 1433),),
)
EXPECTED_REPAIRED = (57, 2752, 22016, 74, 57, 0)


def build_summary() -> dict[str, object]:
    """Run the complete two-cap recurrence and repair audit."""
    failed = diversified_selector_profile(
        INPUT_LENGTH,
        FAILED_CAP,
        compute_minimum_certificate=False,
    )
    repaired = diversified_selector_profile(
        INPUT_LENGTH,
        REPAIR_CAP,
        compute_minimum_certificate=False,
    )
    failed_observed = (
        len(failed.population_primes),
        failed.descriptor_count,
        failed.raw_coordinate_count,
        len(failed.normalized_columns),
        failed.distinct_signature_count,
        failed.collision_pair_count,
        failed.maximum_bucket_size,
        failed.collision_buckets,
    )
    repaired_observed = (
        len(repaired.population_primes),
        repaired.descriptor_count,
        repaired.raw_coordinate_count,
        len(repaired.normalized_columns),
        repaired.distinct_signature_count,
        repaired.collision_pair_count,
    )
    if failed_observed != EXPECTED_FAILED:
        raise AssertionError(
            f"registered M33 collision changed: {failed_observed}"
        )
    if repaired_observed != EXPECTED_REPAIRED or not repaired.injective:
        raise AssertionError(
            f"registered M33 repair changed: {repaired_observed}"
        )
    if not collision_pairs(repaired.signatures).issubset(
        collision_pairs(failed.signatures)
    ):
        raise AssertionError("cap 33 merged a pair separated at cap 32")

    indices = greedy_separating_column_indices(repaired)
    if indices is None:
        raise AssertionError("cap-33 profile lacks a certificate")
    signatures = restricted_signatures(repaired, indices)
    if len(set(signatures)) != len(signatures):
        raise AssertionError("cap-33 certificate is not injective")

    pair_count = repaired.pair_count
    counts = {
        "input_lengths": 1,
        "cap_profiles": 2,
        "balanced_primes": len(repaired.population_primes),
        "descriptors": failed.descriptor_count + repaired.descriptor_count,
        "local_exit_profiles": (
            failed.descriptor_count + repaired.descriptor_count
        )
        * len(repaired.population_primes),
        "raw_coordinates": (
            failed.raw_coordinate_count + repaired.raw_coordinate_count
        ),
        "normalized_coordinates": (
            len(failed.normalized_columns)
            + len(repaired.normalized_columns)
        ),
        "monotonicity_pair_checks": pair_count,
        "normalization_pair_checks": (
            assert_normalization_equivalence(failed)
            + assert_normalization_equivalence(repaired)
        ),
        "certificate_pair_checks": pair_count,
    }
    summary: dict[str, object] = {
        "schema_version": "1.0.0",
        "experiment_id": "EXP-0032",
        "input_length": INPUT_LENGTH,
        "failed_schedules": {
            "m_plus_11": FAILED_CAP,
            "ceil_151m_over_100": FAILED_CAP,
        },
        "failed_profile": {
            "selector_cap": FAILED_CAP,
            "population_size": len(failed.population_primes),
            "descriptor_count": failed.descriptor_count,
            "raw_coordinate_count": failed.raw_coordinate_count,
            "normalized_coordinate_count": len(failed.normalized_columns),
            "distinct_signature_count": failed.distinct_signature_count,
            "collision_pair_count": failed.collision_pair_count,
            "collision_buckets": failed.collision_buckets,
        },
        "repair_profile": {
            "selector_cap": REPAIR_CAP,
            "population_size": len(repaired.population_primes),
            "descriptor_count": repaired.descriptor_count,
            "raw_coordinate_count": repaired.raw_coordinate_count,
            "normalized_coordinate_count": len(repaired.normalized_columns),
            "distinct_signature_count": repaired.distinct_signature_count,
            "collision_pair_count": repaired.collision_pair_count,
        },
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
            "cap": "m+12",
            "minimal_integer_offset_through_21": 12,
        },
        "continued_multiplicative_schedule": {
            "admissible_coefficients_through_21": "c>32/21",
            "infimum": "32/21",
            "working_witness": "ceil(153m/100)",
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
    """Print the registered M33 summary."""
    print(json.dumps(build_summary(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
