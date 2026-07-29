"""Deterministic M48 audit of shifted compact-gap overlap signatures."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "python")]

from mosef_reference import phi4_compact_signature
from mosef_reference.compact_gap_overlap_budget import (
    compact_gap_overlap_bit_bound,
    compact_gap_overlap_integer,
    compact_gap_overlap_profile,
)

INPUT_LENGTHS = tuple(range(20, 41))
WINDOW_SHIFTS = (1, 2)
OVERLAP_WITNESSES = (
    (11, 4, 8),
    (179, 6, 17),
    (409, 9, 17),
)


def _candidate_levels(input_length: int, shift: int) -> tuple[int, ...]:
    start = shift * input_length
    span = input_length // 4
    return tuple(range(start, start + span + 1))


def build_summary() -> dict[str, object]:
    """Build the registered finite overlap and signature audit."""
    overlap_records: list[dict[str, int]] = []
    for gap in range(1, 12):
        exact = compact_gap_overlap_integer(gap)
        bit_bound = compact_gap_overlap_bit_bound(gap)
        if exact.bit_length() > bit_bound:
            raise AssertionError("M48 exact overlap bit bound failed")
        overlap_records.append(
            {
                "level_gap": gap,
                "odd_exponent": (1 << gap) - 1,
                "exact_bit_length": exact.bit_length(),
                "bit_length_upper_bound": bit_bound,
            }
        )

    overlap_witnesses: list[dict[str, int]] = []
    for prime, first_level, second_level in OVERLAP_WITNESSES:
        signature = phi4_compact_signature(
            (first_level, second_level),
            prime,
        )
        gap = second_level - first_level
        overlap_remainder = compact_gap_overlap_integer(gap) % prime
        if signature != 3 or overlap_remainder:
            raise AssertionError("M48 overlap witness failed")
        overlap_witnesses.append(
            {
                "prime": prime,
                "first_level": first_level,
                "second_level": second_level,
                "level_gap": gap,
                "signature": signature,
                "overlap_remainder": overlap_remainder,
            }
        )

    profiles: list[dict[str, int | bool | list[int]]] = []
    for input_length in INPUT_LENGTHS:
        for shift in WINDOW_SHIFTS:
            levels = _candidate_levels(input_length, shift)
            profile = compact_gap_overlap_profile(input_length, levels)
            if profile.theorem_forces_collision and profile.injective:
                raise AssertionError("M48 forced-collision theorem failed")
            profiles.append(
                {
                    "input_length": input_length,
                    "window_shift": shift,
                    "candidate_levels": list(levels),
                    "candidate_count": profile.candidate_count,
                    "level_span": profile.level_span,
                    "compact_evaluation_level_sum": (
                        profile.compact_evaluation_level_sum
                    ),
                    "population_size": profile.population_size,
                    "distinct_signature_count": (
                        profile.distinct_signature_count
                    ),
                    "zero_signature_count": profile.zero_signature_count,
                    "multi_hit_prime_count": profile.multi_hit_prime_count,
                    "low_weight_prime_count": profile.low_weight_prime_count,
                    "overlap_population_upper_bound": (
                        profile.overlap_population_upper_bound
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
        "overlap_gap_records": len(overlap_records),
        "overlap_witnesses": len(overlap_witnesses),
        "selector_profiles": len(profiles),
        "prime_signatures": sum(
            int(profile["population_size"]) for profile in profiles
        ),
        "signature_coordinates": sum(
            int(profile["population_size"])
            * int(profile["candidate_count"])
            for profile in profiles
        ),
        "theorem_forced_profiles": sum(
            bool(profile["theorem_forces_collision"])
            for profile in profiles
        ),
        "injective_profiles": sum(
            bool(profile["injective"]) for profile in profiles
        ),
    }
    summary: dict[str, object] = {
        "schema_version": "1.0.0",
        "experiment_id": "EXP-0047",
        "selector": {
            "family": "phi4",
            "first_factor": 3,
            "second_factor": "2^t+3",
            "base": 2,
            "windows": "t=shift*m,...,shift*m+floor(m/4)",
            "shifts": WINDOW_SHIFTS,
        },
        "overlap_formula": {
            "gap": "d=|u-t|",
            "odd_exponent": "k=2^d-1",
            "overlap_integer": "R_d=3^k+32^k",
            "bit_length_upper_bound": "5*(2^d-1)+1",
        },
        "overlap_records": overlap_records,
        "overlap_witnesses": overlap_witnesses,
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
        raise AssertionError("M48 counts have the wrong shape")
    print(
        "M48 compact-gap overlap audit: PASS "
        f"(summary_sha256={summary['summary_sha256']}, "
        f"profiles={counts['selector_profiles']}, "
        f"coordinates={counts['signature_coordinates']}, "
        f"forced={counts['theorem_forced_profiles']})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
