"""Deterministic M51 audit of superlinear compact-gap level lists."""

from __future__ import annotations

import hashlib
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "python")]

from mosef_reference import compact_gap_variable_order_profile

INPUT_LENGTHS = (20, 24, 28, 32, 36, 40)


def _integer_fourth_root(value: int) -> int:
    """Return ``floor(value**(1/4))`` using exact integer arithmetic."""
    return math.isqrt(math.isqrt(value))


def _spread_levels(
    input_length: int,
    level_span: int,
) -> tuple[int, ...]:
    """Spread ``m+1`` public levels monotonically across an exact span."""
    candidate_count = input_length + 1
    denominator = candidate_count - 1
    levels = tuple(
        input_length + (index * level_span) // denominator
        for index in range(candidate_count)
    )
    if len(set(levels)) != candidate_count:
        raise AssertionError("M51 public levels are not distinct")
    if levels[-1] - levels[0] != level_span:
        raise AssertionError("M51 public level span changed")
    return levels


def _three_halves_span(input_length: int) -> int:
    return math.isqrt(input_length**3)


def _seven_quarters_span(input_length: int) -> int:
    return _integer_fourth_root(input_length**7)


def build_summary() -> dict[str, object]:
    """Build registered variable-order profiles for two superlinear spans."""
    profiles: list[dict[str, int | bool | str | list[int]]] = []
    for input_length in INPUT_LENGTHS:
        schedules = (
            ("three_halves_span", "3/2", _three_halves_span(input_length)),
            ("seven_quarters_span", "7/4", _seven_quarters_span(input_length)),
        )
        for schedule_name, span_power, level_span in schedules:
            levels = _spread_levels(input_length, level_span)
            profile = compact_gap_variable_order_profile(
                input_length,
                levels,
            )
            overlap_order = profile.high_weight_threshold - 1
            logarithmic_scale = profile.candidate_count.bit_length()
            if overlap_order * overlap_order * logarithmic_scale < level_span:
                raise AssertionError("M51 overlap-order balance failed")
            if profile.theorem_forces_collision and profile.injective:
                raise AssertionError("M51 finite collision certificate failed")
            profiles.append(
                {
                    "input_length": input_length,
                    "schedule": schedule_name,
                    "span_power": span_power,
                    "candidate_levels": list(levels),
                    "candidate_count": profile.candidate_count,
                    "level_span": profile.level_span,
                    "compact_evaluation_level_sum": (
                        profile.compact_evaluation_level_sum
                    ),
                    "overlap_order": overlap_order,
                    "high_weight_threshold": profile.high_weight_threshold,
                    "maximum_common_gap": level_span // overlap_order,
                    "logarithmic_scale": logarithmic_scale,
                    "balance_product": (
                        overlap_order * overlap_order * logarithmic_scale
                    ),
                    "span_log_product": level_span * logarithmic_scale,
                    "input_length_squared": input_length**2,
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
                    "high_weight_upper_bound_bit_length": (
                        profile.high_weight_population_upper_bound.bit_length()
                    ),
                    "low_weight_signature_capacity": (
                        profile.low_weight_signature_capacity
                    ),
                    "low_weight_capacity_bit_length": (
                        profile.low_weight_signature_capacity.bit_length()
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
        "experiment_id": "EXP-0049",
        "selector": {
            "family": "phi4",
            "first_factor": 3,
            "second_factor": "2^t+3",
            "base": 2,
            "candidate_count": "r_m=m+1",
            "level_start": "t_0=m",
            "three_halves_span": "floor(m^(3/2))",
            "seven_quarters_span": "floor(m^(7/4))",
        },
        "variable_order": {
            "logarithmic_scale": "ell_m=ceil(log2(r_m+1))",
            "overlap_order": (
                "h_m=min(r_m,ceil(sqrt(Delta_m/ell_m)))"
            ),
            "high_weight_threshold": "h_m+1",
            "asymptotic_condition": (
                "Delta_m*log2(r_m+1)=o(m^2)"
            ),
        },
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
    """Run the deterministic M51 superlinear-span audit."""
    summary = build_summary()
    counts = summary["counts"]
    if not isinstance(counts, dict):
        raise AssertionError("M51 counts have the wrong shape")
    print(
        "M51 subquadratic-span audit: PASS "
        f"(summary_sha256={summary['summary_sha256']}, "
        f"profiles={counts['selector_profiles']}, "
        f"coordinates={counts['signature_coordinates']}, "
        f"high_weight={counts['observed_high_weight_primes']})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
