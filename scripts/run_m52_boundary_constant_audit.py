"""Deterministic M52 audit of the compact-gap boundary constants."""

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
)

INPUT_LENGTHS = (1024, 4096, 16384, 65536)
BOUNDARY_CASES = (
    ("one_thirty_second", 1, 32, 1, 4),
    ("one_sixteenth", 1, 16, 3, 8),
    ("three_thirty_seconds", 3, 32, 7, 16),
    ("one_eighth_endpoint", 1, 8, 1, 2),
    ("five_thirty_seconds", 5, 32, 9, 16),
)
GROWTH_EXPONENTS = (
    ("linear", 1, 1),
    ("four_thirds", 4, 3),
    ("three_halves", 3, 2),
    ("five_thirds", 5, 3),
    ("quadratic_limit", 2, 1),
)


def _integer_sha256(value: int) -> str:
    """Hash one nonnegative integer in unsigned big-endian form."""
    if value < 0:
        raise ValueError("value must be nonnegative")
    width = max(1, (value.bit_length() + 7) // 8)
    return hashlib.sha256(value.to_bytes(width, "big")).hexdigest()


def _packed_candidate_count(
    input_length: int,
    constant_numerator: int,
    constant_denominator: int,
) -> int:
    """Choose a near-quadratic list with roughly one quarter of the span."""
    input_logarithm = input_length.bit_length() - 1
    return max(
        2,
        constant_numerator
        * input_length
        * input_length
        // (constant_denominator * 4 * input_logarithm),
    )


def _growth_threshold(
    numerator: int,
    denominator: int,
) -> dict[str, int | str | None]:
    """Return ``a/(16(a-1))`` for ``a>1`` and infinity at ``a=1``."""
    exponent = Fraction(numerator, denominator)
    if exponent == 1:
        return {
            "growth_exponent": "1",
            "threshold_numerator": None,
            "threshold_denominator": None,
            "interpretation": "every fixed boundary constant",
        }
    threshold = exponent / (16 * (exponent - 1))
    return {
        "growth_exponent": f"{numerator}/{denominator}",
        "threshold_numerator": threshold.numerator,
        "threshold_denominator": threshold.denominator,
        "interpretation": "constants strictly below threshold",
    }


def build_summary() -> dict[str, object]:
    """Build exact finite ledgers and symbolic constant thresholds."""
    profiles: list[dict[str, int | bool | str]] = []
    for (
        case_name,
        constant_numerator,
        constant_denominator,
        multiplier_numerator,
        multiplier_denominator,
    ) in BOUNDARY_CASES:
        boundary_constant = Fraction(
            constant_numerator,
            constant_denominator,
        )
        multiplier = Fraction(
            multiplier_numerator,
            multiplier_denominator,
        )
        leading_coefficient = (
            multiplier / 2 + boundary_constant / multiplier
        )
        theorem_eligible = leading_coefficient < Fraction(1, 2)
        for input_length in INPUT_LENGTHS:
            candidate_count = _packed_candidate_count(
                input_length,
                constant_numerator,
                constant_denominator,
            )
            logarithmic_scale = candidate_count.bit_length()
            level_span = (
                constant_numerator * input_length * input_length
                // (constant_denominator * logarithmic_scale)
            )
            if level_span < candidate_count - 1:
                raise AssertionError("M52 packed list does not fit its span")
            overlap_order = compact_gap_boundary_overlap_order(
                input_length,
                candidate_count,
                multiplier_numerator,
                multiplier_denominator,
            )
            ledger = compact_gap_boundary_ledger(
                input_length,
                candidate_count,
                level_span,
                overlap_order,
            )
            if ledger.theorem_forces_collision != theorem_eligible:
                raise AssertionError(
                    "M52 finite ledger disagrees with registered eligibility"
                )
            profiles.append(
                {
                    "case": case_name,
                    "input_length": input_length,
                    "constant_numerator": constant_numerator,
                    "constant_denominator": constant_denominator,
                    "multiplier_numerator": multiplier_numerator,
                    "multiplier_denominator": multiplier_denominator,
                    "leading_coefficient_numerator": (
                        leading_coefficient.numerator
                    ),
                    "leading_coefficient_denominator": (
                        leading_coefficient.denominator
                    ),
                    "theorem_eligible": theorem_eligible,
                    "candidate_count": candidate_count,
                    "logarithmic_scale": logarithmic_scale,
                    "level_span": level_span,
                    "packing_slack": level_span - candidate_count + 1,
                    "overlap_order": overlap_order,
                    "high_weight_threshold": (
                        ledger.high_weight_threshold
                    ),
                    "maximum_common_gap": ledger.maximum_common_gap,
                    "high_weight_bound_bit_length": (
                        ledger.high_weight_population_upper_bound.bit_length()
                    ),
                    "low_weight_capacity_bit_length": (
                        ledger.low_weight_signature_capacity.bit_length()
                    ),
                    "population_lower_bound_bit_length": (
                        ledger.conservative_population_lower_bound.bit_length()
                    ),
                    "high_weight_bound_sha256": _integer_sha256(
                        ledger.high_weight_population_upper_bound
                    ),
                    "low_weight_capacity_sha256": _integer_sha256(
                        ledger.low_weight_signature_capacity
                    ),
                    "population_lower_bound_sha256": _integer_sha256(
                        ledger.conservative_population_lower_bound
                    ),
                    "theorem_forces_collision": (
                        ledger.theorem_forces_collision
                    ),
                }
            )

    growth_thresholds = [
        {
            "regime": regime,
            **_growth_threshold(numerator, denominator),
        }
        for regime, numerator, denominator in GROWTH_EXPONENTS
    ]
    counts = {
        "boundary_profiles": len(profiles),
        "theorem_eligible_profiles": sum(
            bool(profile["theorem_eligible"]) for profile in profiles
        ),
        "finite_collision_certificates": sum(
            bool(profile["theorem_forces_collision"]) for profile in profiles
        ),
        "endpoint_or_above_profiles": sum(
            not bool(profile["theorem_eligible"]) for profile in profiles
        ),
        "growth_thresholds": len(growth_thresholds),
    }
    summary: dict[str, object] = {
        "schema_version": "1.0.0",
        "experiment_id": "EXP-0050",
        "uniform_boundary": {
            "span_condition": (
                "Delta_m<=(c+o(1))*m^2/ceil(log2(r_m+1))"
            ),
            "packing_condition": "r_m<=Delta_m+1",
            "overlap_order": "h_m=ceil(x*m/ell_m)",
            "leading_coefficient": "x/2+c/x",
            "minimum_coefficient": "sqrt(2c)",
            "proved_range": "0<c<1/8",
            "unresolved_endpoint": "c=1/8",
        },
        "profiles": profiles,
        "growth_thresholds": growth_thresholds,
        "counts": counts,
        "status": "PASS",
    }
    canonical = json.dumps(summary, sort_keys=True, separators=(",", ":"))
    summary["summary_sha256"] = hashlib.sha256(
        canonical.encode("utf-8")
    ).hexdigest()
    return summary


def main() -> int:
    """Run the exact M52 boundary-constant audit."""
    summary = build_summary()
    counts = summary["counts"]
    if not isinstance(counts, dict):
        raise AssertionError("M52 counts have the wrong shape")
    print(
        "M52 boundary-constant audit: PASS "
        f"(summary_sha256={summary['summary_sha256']}, "
        f"profiles={counts['boundary_profiles']}, "
        f"certificates={counts['finite_collision_certificates']}, "
        f"open={counts['endpoint_or_above_profiles']})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
