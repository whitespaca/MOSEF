"""Independently validate the registered M52 exact entropy ledgers."""

from __future__ import annotations

import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas/m52-boundary-constant-v1.json"


def _integer_sha256(value: int) -> str:
    width = max(1, (value.bit_length() + 7) // 8)
    return hashlib.sha256(value.to_bytes(width, "big")).hexdigest()


def _overlap_bit_bound(level_gap: int) -> int:
    return 5 * ((1 << level_gap) - 1) + 1


def _low_weight_capacity(candidate_count: int, threshold: int) -> int:
    return sum(
        math.comb(candidate_count, weight)
        for weight in range(min(threshold, candidate_count + 1))
    )


def main() -> int:
    """Check hashes, packing, orders, exact integers, and classifications."""
    data = json.loads(SCHEMA.read_text(encoding="utf-8"))
    canonical = dict(data)
    expected_hash = canonical.pop("summary_sha256")
    actual_hash = hashlib.sha256(
        json.dumps(canonical, sort_keys=True, separators=(",", ":")).encode(
            "utf-8"
        )
    ).hexdigest()
    if actual_hash != expected_hash:
        raise AssertionError("M52 canonical summary hash changed")

    profile_checks = 0
    integer_hash_checks = 0
    packing_checks = 0
    classification_checks = 0
    for record in data["profiles"]:
        input_length = int(record["input_length"])
        candidate_count = int(record["candidate_count"])
        logarithmic_scale = candidate_count.bit_length()
        constant = Fraction(
            int(record["constant_numerator"]),
            int(record["constant_denominator"]),
        )
        multiplier = Fraction(
            int(record["multiplier_numerator"]),
            int(record["multiplier_denominator"]),
        )
        expected_coefficient = multiplier / 2 + constant / multiplier
        level_span = (
            constant.numerator * input_length * input_length
            // (constant.denominator * logarithmic_scale)
        )
        order_numerator = (
            multiplier.numerator * input_length
        )
        order_denominator = (
            multiplier.denominator * logarithmic_scale
        )
        overlap_order = min(
            candidate_count,
            max(
                1,
                (
                    order_numerator
                    + order_denominator
                    - 1
                )
                // order_denominator,
            ),
        )
        threshold = overlap_order + 1
        low_weight_capacity = _low_weight_capacity(
            candidate_count,
            threshold,
        )
        if overlap_order == candidate_count:
            maximum_common_gap = 0
            high_weight_bound = 0
        else:
            maximum_common_gap = level_span // overlap_order
            high_weight_bound = (
                math.comb(candidate_count, threshold)
                * _overlap_bit_bound(maximum_common_gap)
                // ((input_length - 1) // 2)
            )
        population_lower_bound = (
            (1 << (input_length // 2)) // (81 * input_length)
        )
        theorem_forces_collision = (
            population_lower_bound - high_weight_bound
            > low_weight_capacity
        )
        expected = {
            "logarithmic_scale": logarithmic_scale,
            "level_span": level_span,
            "packing_slack": level_span - candidate_count + 1,
            "overlap_order": overlap_order,
            "high_weight_threshold": threshold,
            "maximum_common_gap": maximum_common_gap,
            "leading_coefficient_numerator": expected_coefficient.numerator,
            "leading_coefficient_denominator": (
                expected_coefficient.denominator
            ),
            "theorem_eligible": expected_coefficient < Fraction(1, 2),
            "high_weight_bound_bit_length": high_weight_bound.bit_length(),
            "low_weight_capacity_bit_length": (
                low_weight_capacity.bit_length()
            ),
            "population_lower_bound_bit_length": (
                population_lower_bound.bit_length()
            ),
            "high_weight_bound_sha256": _integer_sha256(high_weight_bound),
            "low_weight_capacity_sha256": _integer_sha256(
                low_weight_capacity
            ),
            "population_lower_bound_sha256": _integer_sha256(
                population_lower_bound
            ),
            "theorem_forces_collision": theorem_forces_collision,
        }
        for field, value in expected.items():
            if record[field] != value:
                raise AssertionError(f"M52 field changed: {field}")
        if level_span < candidate_count - 1:
            raise AssertionError("M52 packing inequality failed")
        if theorem_forces_collision != bool(record["theorem_eligible"]):
            raise AssertionError("M52 finite classification changed")
        profile_checks += 1
        integer_hash_checks += 3
        packing_checks += 1
        classification_checks += 1

    expected_thresholds = {
        "linear": (None, None),
        "four_thirds": (1, 4),
        "three_halves": (3, 16),
        "five_thirds": (5, 32),
        "quadratic_limit": (1, 8),
    }
    for record in data["growth_thresholds"]:
        expected = expected_thresholds[record["regime"]]
        actual = (
            record["threshold_numerator"],
            record["threshold_denominator"],
        )
        if actual != expected:
            raise AssertionError("M52 growth threshold changed")

    print(
        "M52 boundary-constant differential validation: PASS "
        f"({profile_checks} profile checks, "
        f"{integer_hash_checks} exact-integer hash checks, "
        f"{packing_checks} packing checks, "
        f"{classification_checks} classification checks)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
