"""Deterministic M57 audit of the exact endpoint two-ledger obstruction."""

from __future__ import annotations

import hashlib
import json
import math
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "python")]

from mosef_reference import compact_gap_endpoint_dense_ledger

SCALE_EXPONENTS = tuple(range(6, 23))
RATIONAL_DENOMINATOR_MAX = 12


def _integer_sha256(value: int) -> str:
    width = max(1, (value.bit_length() + 7) // 8)
    return hashlib.sha256(value.to_bytes(width, "big")).hexdigest()


def _rational_profiles() -> list[dict[str, int | bool]]:
    values = {
        Fraction(numerator, denominator)
        for denominator in range(1, RATIONAL_DENOMINATOR_MAX + 1)
        for numerator in range(1, 2 * RATIONAL_DENOMINATOR_MAX + 1)
        if Fraction(1, 2)
        <= Fraction(numerator, denominator)
        <= Fraction(3, 2)
    }
    profiles: list[dict[str, int | bool]] = []
    for value in sorted(values):
        high = Fraction(1, 2) / value
        low = value / 2
        maximum = max(high, low)
        profiles.append(
            {
                "x_numerator": value.numerator,
                "x_denominator": value.denominator,
                "high_numerator": high.numerator,
                "high_denominator": high.denominator,
                "low_numerator": low.numerator,
                "low_denominator": low.denominator,
                "maximum_numerator": maximum.numerator,
                "maximum_denominator": maximum.denominator,
                "at_least_one_half": maximum >= Fraction(1, 2),
                "equality_only_at_one": (
                    maximum == Fraction(1, 2) and value == 1
                ),
            }
        )
    return profiles


def build_summary() -> dict[str, object]:
    """Build exact switch-side profiles and rational coefficient records."""
    endpoint_profiles: list[dict[str, int | bool | str]] = []
    for scale_exponent in SCALE_EXPONENTS:
        level_span = (1 << scale_exponent) - 2
        radicand = 2 * scale_exponent * level_span
        root = math.isqrt(radicand)
        input_length = root + (root * root < radicand)
        switch_order = (2 * level_span) // input_length
        for side, overlap_order in (
            ("high", switch_order),
            ("low", switch_order + 1),
        ):
            ledger = compact_gap_endpoint_dense_ledger(
                scale_exponent,
                overlap_order,
            )
            endpoint_profiles.append(
                {
                    "scale_exponent": scale_exponent,
                    "side": side,
                    "input_length": ledger.input_length,
                    "candidate_count": ledger.candidate_count,
                    "level_span": ledger.level_span,
                    "logarithmic_scale": ledger.logarithmic_scale,
                    "overlap_order": ledger.overlap_order,
                    "switch_order": ledger.switch_order,
                    "maximum_common_gap": ledger.maximum_common_gap,
                    "lcm_bit_length_lower_bound": (
                        ledger.lcm_bit_length_lower_bound
                    ),
                    "high_weight_charge_lower_bound_sha256": (
                        _integer_sha256(
                            ledger.high_weight_charge_lower_bound
                        )
                    ),
                    "low_weight_signature_capacity_sha256": (
                        _integer_sha256(
                            ledger.low_weight_signature_capacity
                        )
                    ),
                    "population_lower_bound_sha256": _integer_sha256(
                        ledger.conservative_population_lower_bound
                    ),
                    "high_ledger_consumes_population": (
                        ledger.high_ledger_consumes_population
                    ),
                    "low_ledger_consumes_population": (
                        ledger.low_ledger_consumes_population
                    ),
                    "certificate_blocked": ledger.certificate_blocked,
                }
            )

    rational_profiles = _rational_profiles()
    counts = {
        "scale_exponents": len(SCALE_EXPONENTS),
        "endpoint_profiles": len(endpoint_profiles),
        "switch_dichotomies": len(SCALE_EXPONENTS),
        "rational_coefficient_profiles": len(rational_profiles),
        "exact_integer_hash_checks": 3 * len(endpoint_profiles),
    }
    summary: dict[str, object] = {
        "schema_version": "1.0.0",
        "experiment_id": "EXP-0055",
        "endpoint_family": (
            "r=2^ell-1, Delta=2^ell-2, "
            "m=ceil(sqrt(2*ell*Delta))"
        ),
        "endpoint_profiles": endpoint_profiles,
        "rational_profiles": rational_profiles,
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
    endpoint_profiles = summary["endpoint_profiles"]
    rational_profiles = summary["rational_profiles"]
    if not isinstance(endpoint_profiles, list) or not isinstance(
        rational_profiles,
        list,
    ):
        raise AssertionError("M57 record shape changed")
    if any(not record["certificate_blocked"] for record in endpoint_profiles):
        raise AssertionError("M57 endpoint certificate unexpectedly opened")
    if any(
        not record["at_least_one_half"]
        for record in rational_profiles
    ):
        raise AssertionError("M57 rational leading balance fell below one half")
    print(
        "M57 endpoint zero-slack audit: PASS "
        f"(summary_sha256={summary['summary_sha256']}, "
        f"endpoint_profiles={len(endpoint_profiles)}, "
        f"rational_profiles={len(rational_profiles)})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
