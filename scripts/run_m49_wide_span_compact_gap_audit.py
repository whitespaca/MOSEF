"""Deterministic M49 audit of wide-span compact-gap signatures."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "python")]

from mosef_reference import phi4_compact_signature
from mosef_reference.compact_gap_overlap_budget import (
    compact_gap_common_support_gap,
    compact_gap_common_support_integer,
    compact_gap_high_weight_profile,
)

INPUT_LENGTHS = (20, 24, 28, 32, 36, 40)
COMMON_SUPPORT_WITNESSES = (
    (11, (4, 8, 12, 16)),
    (179, (6, 17, 28)),
    (409, (9, 17, 25)),
)


def _unit_span_levels(input_length: int) -> tuple[int, ...]:
    return tuple(range(input_length, 2 * input_length + 1))


def _double_span_levels(input_length: int) -> tuple[int, ...]:
    return tuple(range(2 * input_length, 4 * input_length + 1))


def build_summary() -> dict[str, object]:
    """Build registered wide-span profiles and higher-overlap witnesses."""
    witness_records: list[dict[str, object]] = []
    for prime, levels in COMMON_SUPPORT_WITNESSES:
        signature = phi4_compact_signature(levels, prime)
        expected_signature = (1 << len(levels)) - 1
        common_gap = compact_gap_common_support_gap(levels)
        overlap_remainder = (
            compact_gap_common_support_integer(levels) % prime
        )
        if signature != expected_signature or overlap_remainder:
            raise AssertionError("M49 common-support witness failed")
        witness_records.append(
            {
                "prime": prime,
                "candidate_levels": levels,
                "signature": signature,
                "signature_weight": signature.bit_count(),
                "common_gap": common_gap,
                "overlap_remainder": overlap_remainder,
            }
        )

    profiles: list[dict[str, int | bool | str | list[int]]] = []
    for input_length in INPUT_LENGTHS:
        schedules = (
            ("unit_span", _unit_span_levels(input_length), 4),
            ("double_span", _double_span_levels(input_length), 6),
        )
        for schedule_name, levels, threshold in schedules:
            profile = compact_gap_high_weight_profile(
                input_length,
                levels,
                threshold,
            )
            if profile.theorem_forces_collision and profile.injective:
                raise AssertionError("M49 forced-collision theorem failed")
            profiles.append(
                {
                    "input_length": input_length,
                    "schedule": schedule_name,
                    "candidate_levels": list(levels),
                    "candidate_count": profile.candidate_count,
                    "level_span": profile.level_span,
                    "compact_evaluation_level_sum": (
                        profile.compact_evaluation_level_sum
                    ),
                    "high_weight_threshold": threshold,
                    "population_size": profile.population_size,
                    "distinct_signature_count": (
                        profile.distinct_signature_count
                    ),
                    "zero_signature_count": profile.zero_signature_count,
                    "high_weight_prime_count": (
                        profile.high_weight_prime_count
                    ),
                    "maximum_signature_weight": (
                        profile.maximum_signature_weight
                    ),
                    "high_weight_population_upper_bound": (
                        profile.high_weight_population_upper_bound
                    ),
                    "low_weight_signature_capacity": (
                        profile.low_weight_signature_capacity
                    ),
                    "pair_count": profile.pair_count,
                    "separated_pair_count": profile.separated_pair_count,
                    "collision_pair_count": profile.collision_pair_count,
                    "maximum_bucket_size": profile.maximum_bucket_size,
                    "theorem_forces_collision": (
                        profile.theorem_forces_collision
                    ),
                    "injective": profile.injective,
                }
            )

    counts = {
        "common_support_witnesses": len(witness_records),
        "selector_profiles": len(profiles),
        "prime_signatures": sum(
            int(profile["population_size"]) for profile in profiles
        ),
        "signature_coordinates": sum(
            int(profile["population_size"])
            * int(profile["candidate_count"])
            for profile in profiles
        ),
        "injective_profiles": sum(
            bool(profile["injective"]) for profile in profiles
        ),
        "observed_high_weight_primes": sum(
            int(profile["high_weight_prime_count"]) for profile in profiles
        ),
        "theorem_forced_profiles": sum(
            bool(profile["theorem_forces_collision"])
            for profile in profiles
        ),
    }
    summary: dict[str, object] = {
        "schema_version": "1.0.0",
        "experiment_id": "EXP-0048",
        "selector": {
            "family": "phi4",
            "first_factor": 3,
            "second_factor": "2^t+3",
            "base": 2,
            "unit_span": "t=m,...,2m",
            "double_span": "t=2m,...,4m",
        },
        "higher_overlap": {
            "level_subset": "t_0<...<t_h",
            "common_gap": "q=gcd(t_1-t_0,...,t_h-t_0)",
            "forced_integer": "R_q=3^(2^q-1)+32^(2^q-1)",
            "gap_upper_bound": "q<=Delta/h",
        },
        "common_support_witnesses": witness_records,
        "profiles": profiles,
        "counts": counts,
        "status": "PASS",
    }
    canonical = json.dumps(summary, sort_keys=True, separators=(",", ":"))
    summary["summary_sha256"] = hashlib.sha256(
        canonical.encode("utf-8")
    ).hexdigest()
    return summary


def main() -> int:
    summary = build_summary()
    counts = summary["counts"]
    if not isinstance(counts, dict):
        raise AssertionError("M49 counts have the wrong shape")
    print(
        "M49 wide-span compact-gap audit: PASS "
        f"(summary_sha256={summary['summary_sha256']}, "
        f"profiles={counts['selector_profiles']}, "
        f"coordinates={counts['signature_coordinates']}, "
        f"high_weight={counts['observed_high_weight_primes']})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
