"""Deterministic M53 audit of distinct GCD-gap charging."""

from __future__ import annotations

import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "python")]

from mosef_reference import (
    compact_gap_boundary_ledger,
    compact_gap_boundary_overlap_order,
    compact_gap_distinct_gap_ledger,
)

INPUT_LENGTHS = (1024, 4096, 16384, 65536)
PACKED_CASES = (
    ("one_eighth", 1, 8, 1, 2),
    ("one_quarter", 1, 4, 3, 4),
    ("three_eighths", 3, 8, 7, 8),
    ("one_half_endpoint", 1, 2, 1, 1),
    ("five_eighths", 5, 8, 1, 1),
)
LINEAR_CASES = (
    ("one_eighth", 1, 8, 1, 2),
    ("one_quarter", 1, 4, 3, 4),
    ("three_eighths", 3, 8, 1, 1),
    ("one_half", 1, 2, 5, 4),
    ("five_eighths", 5, 8, 3, 2),
)


def _integer_sha256(value: int) -> str:
    width = max(1, (value.bit_length() + 7) // 8)
    return hashlib.sha256(value.to_bytes(width, "big")).hexdigest()


def _packed_candidate_count(
    input_length: int,
    constant_numerator: int,
    constant_denominator: int,
) -> int:
    input_logarithm = input_length.bit_length() - 1
    return max(
        2,
        constant_numerator
        * input_length
        * input_length
        // (constant_denominator * 4 * input_logarithm),
    )


def _build_profile(
    regime: str,
    case_name: str,
    constant_numerator: int,
    constant_denominator: int,
    multiplier_numerator: int,
    multiplier_denominator: int,
    input_length: int,
) -> dict[str, int | bool | str]:
    constant = Fraction(constant_numerator, constant_denominator)
    multiplier = Fraction(multiplier_numerator, multiplier_denominator)
    if regime == "packed_quadratic_limit":
        candidate_count = _packed_candidate_count(
            input_length,
            constant_numerator,
            constant_denominator,
        )
        low_coefficient = multiplier / 2
    elif regime == "linear_growth":
        candidate_count = input_length + 1
        low_coefficient = Fraction(0, 1)
    else:
        raise AssertionError("unknown M53 regime")
    logarithmic_scale = candidate_count.bit_length()
    level_span = (
        constant_numerator * input_length * input_length
        // (constant_denominator * logarithmic_scale)
    )
    if level_span < candidate_count - 1:
        raise AssertionError("M53 public list does not fit its span")
    overlap_order = compact_gap_boundary_overlap_order(
        input_length,
        candidate_count,
        multiplier_numerator,
        multiplier_denominator,
    )
    subset_ledger = compact_gap_boundary_ledger(
        input_length,
        candidate_count,
        level_span,
        overlap_order,
    )
    distinct_ledger = compact_gap_distinct_gap_ledger(
        input_length,
        candidate_count,
        level_span,
        overlap_order,
    )
    if (
        distinct_ledger.high_weight_population_upper_bound
        >= subset_ledger.high_weight_population_upper_bound
    ):
        raise AssertionError("M53 did not reduce the subset union bound")
    high_coefficient = constant / multiplier
    leading_coefficient = max(high_coefficient, low_coefficient)
    theorem_eligible = leading_coefficient < Fraction(1, 2)
    return {
        "regime": regime,
        "case": case_name,
        "input_length": input_length,
        "constant_numerator": constant_numerator,
        "constant_denominator": constant_denominator,
        "multiplier_numerator": multiplier_numerator,
        "multiplier_denominator": multiplier_denominator,
        "high_coefficient_numerator": high_coefficient.numerator,
        "high_coefficient_denominator": high_coefficient.denominator,
        "low_coefficient_numerator": low_coefficient.numerator,
        "low_coefficient_denominator": low_coefficient.denominator,
        "leading_coefficient_numerator": leading_coefficient.numerator,
        "leading_coefficient_denominator": leading_coefficient.denominator,
        "theorem_eligible": theorem_eligible,
        "candidate_count": candidate_count,
        "logarithmic_scale": logarithmic_scale,
        "level_span": level_span,
        "packing_slack": level_span - candidate_count + 1,
        "overlap_order": overlap_order,
        "high_weight_threshold": distinct_ledger.high_weight_threshold,
        "maximum_common_gap": distinct_ledger.maximum_common_gap,
        "distinct_gap_count": distinct_ledger.distinct_gap_count,
        "subset_bound_bit_length": (
            subset_ledger.high_weight_population_upper_bound.bit_length()
        ),
        "distinct_gap_bound_bit_length": (
            distinct_ledger.high_weight_population_upper_bound.bit_length()
        ),
        "subset_reduction_bits": (
            subset_ledger.high_weight_population_upper_bound.bit_length()
            - distinct_ledger.high_weight_population_upper_bound.bit_length()
        ),
        "low_weight_capacity_bit_length": (
            distinct_ledger.low_weight_signature_capacity.bit_length()
        ),
        "population_lower_bound_bit_length": (
            distinct_ledger.conservative_population_lower_bound.bit_length()
        ),
        "distinct_gap_bound_sha256": _integer_sha256(
            distinct_ledger.high_weight_population_upper_bound
        ),
        "low_weight_capacity_sha256": _integer_sha256(
            distinct_ledger.low_weight_signature_capacity
        ),
        "population_lower_bound_sha256": _integer_sha256(
            distinct_ledger.conservative_population_lower_bound
        ),
        "theorem_forces_collision": (
            distinct_ledger.theorem_forces_collision
        ),
    }


def build_summary() -> dict[str, object]:
    """Build packed-limit and linear-growth distinct-gap profiles."""
    profiles: list[dict[str, int | bool | str]] = []
    for regime, cases in (
        ("packed_quadratic_limit", PACKED_CASES),
        ("linear_growth", LINEAR_CASES),
    ):
        for case in cases:
            for input_length in INPUT_LENGTHS:
                profiles.append(
                    _build_profile(regime, *case, input_length)
                )
    counts = {
        "profiles": len(profiles),
        "packing_checks": len(profiles),
        "subset_reduction_checks": sum(
            int(profile["subset_reduction_bits"]) > 0
            for profile in profiles
        ),
        "exact_integer_hash_checks": 3 * len(profiles),
        "theorem_eligible_profiles": sum(
            bool(profile["theorem_eligible"]) for profile in profiles
        ),
        "finite_collision_certificates": sum(
            bool(profile["theorem_forces_collision"]) for profile in profiles
        ),
        "finite_noncertificates": sum(
            not bool(profile["theorem_forces_collision"])
            for profile in profiles
        ),
    }
    summary: dict[str, object] = {
        "schema_version": "1.0.0",
        "experiment_id": "EXP-0051",
        "distinct_gap_ledger": {
            "maximum_gap": "D_m=floor(Delta_m/h_m)",
            "charged_integers": "R_q for 1<=q<=D_m",
            "prefix_bit_bound": "5*2^(D_m+1)-10-4*D_m",
            "uniform_high_coefficient": "c/x",
            "uniform_low_coefficient": "x/2",
            "uniform_proved_range": "0<c<1/2",
            "uniform_unresolved_endpoint": "c=1/2",
            "growth_refined_range": (
                "c<a/(4(a-1)) for 1<a<=2; every fixed c for a<=1"
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
    summary = build_summary()
    counts = summary["counts"]
    if not isinstance(counts, dict):
        raise AssertionError("M53 counts have the wrong shape")
    print(
        "M53 distinct-gap audit: PASS "
        f"(summary_sha256={summary['summary_sha256']}, "
        f"profiles={counts['profiles']}, "
        f"certificates={counts['finite_collision_certificates']}, "
        f"reductions={counts['subset_reduction_checks']})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
