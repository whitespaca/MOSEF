"""Independently validate the registered M53 distinct-gap ledgers."""

from __future__ import annotations

import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas/m53-distinct-gap-v1.json"


def _integer_sha256(value: int) -> str:
    width = max(1, (value.bit_length() + 7) // 8)
    return hashlib.sha256(value.to_bytes(width, "big")).hexdigest()


def _overlap_bit_bound(level_gap: int) -> int:
    return 5 * ((1 << level_gap) - 1) + 1


def _prefix_bit_bound(maximum_gap: int) -> int:
    return sum(_overlap_bit_bound(gap) for gap in range(1, maximum_gap + 1))


def _low_weight_capacity(candidate_count: int, threshold: int) -> int:
    return sum(
        math.comb(candidate_count, weight)
        for weight in range(min(threshold, candidate_count + 1))
    )


def main() -> int:
    data = json.loads(SCHEMA.read_text(encoding="utf-8"))
    canonical = dict(data)
    expected_hash = canonical.pop("summary_sha256")
    actual_hash = hashlib.sha256(
        json.dumps(canonical, sort_keys=True, separators=(",", ":")).encode(
            "utf-8"
        )
    ).hexdigest()
    if actual_hash != expected_hash:
        raise AssertionError("M53 canonical summary hash changed")

    profile_checks = 0
    integer_hash_checks = 0
    reduction_checks = 0
    for record in data["profiles"]:
        input_length = int(record["input_length"])
        constant = Fraction(
            int(record["constant_numerator"]),
            int(record["constant_denominator"]),
        )
        multiplier = Fraction(
            int(record["multiplier_numerator"]),
            int(record["multiplier_denominator"]),
        )
        if record["regime"] == "packed_quadratic_limit":
            input_logarithm = input_length.bit_length() - 1
            candidate_count = max(
                2,
                constant.numerator
                * input_length
                * input_length
                // (constant.denominator * 4 * input_logarithm),
            )
            low_coefficient = multiplier / 2
        elif record["regime"] == "linear_growth":
            candidate_count = input_length + 1
            low_coefficient = Fraction(0, 1)
        else:
            raise AssertionError("M53 regime changed")
        logarithmic_scale = candidate_count.bit_length()
        level_span = (
            constant.numerator * input_length * input_length
            // (constant.denominator * logarithmic_scale)
        )
        order_numerator = multiplier.numerator * input_length
        order_denominator = multiplier.denominator * logarithmic_scale
        overlap_order = min(
            candidate_count,
            max(
                1,
                (order_numerator + order_denominator - 1)
                // order_denominator,
            ),
        )
        threshold = overlap_order + 1
        maximum_common_gap = (
            0
            if overlap_order == candidate_count
            else level_span // overlap_order
        )
        population_prime_bits = (input_length - 1) // 2
        if overlap_order == candidate_count:
            subset_bound = 0
            distinct_gap_bound = 0
        else:
            subset_bound = (
                math.comb(candidate_count, threshold)
                * _overlap_bit_bound(maximum_common_gap)
                // population_prime_bits
            )
            distinct_gap_bound = (
                _prefix_bit_bound(maximum_common_gap)
                // population_prime_bits
            )
        low_weight_capacity = _low_weight_capacity(
            candidate_count,
            threshold,
        )
        population_lower_bound = (
            (1 << (input_length // 2)) // (81 * input_length)
        )
        theorem_forces_collision = (
            population_lower_bound - distinct_gap_bound
            > low_weight_capacity
        )
        high_coefficient = constant / multiplier
        leading_coefficient = max(high_coefficient, low_coefficient)
        expected = {
            "candidate_count": candidate_count,
            "logarithmic_scale": logarithmic_scale,
            "level_span": level_span,
            "packing_slack": level_span - candidate_count + 1,
            "overlap_order": overlap_order,
            "high_weight_threshold": threshold,
            "maximum_common_gap": maximum_common_gap,
            "distinct_gap_count": maximum_common_gap,
            "high_coefficient_numerator": high_coefficient.numerator,
            "high_coefficient_denominator": high_coefficient.denominator,
            "low_coefficient_numerator": low_coefficient.numerator,
            "low_coefficient_denominator": low_coefficient.denominator,
            "leading_coefficient_numerator": leading_coefficient.numerator,
            "leading_coefficient_denominator": leading_coefficient.denominator,
            "theorem_eligible": leading_coefficient < Fraction(1, 2),
            "subset_bound_bit_length": subset_bound.bit_length(),
            "distinct_gap_bound_bit_length": distinct_gap_bound.bit_length(),
            "subset_reduction_bits": (
                subset_bound.bit_length() - distinct_gap_bound.bit_length()
            ),
            "low_weight_capacity_bit_length": (
                low_weight_capacity.bit_length()
            ),
            "population_lower_bound_bit_length": (
                population_lower_bound.bit_length()
            ),
            "distinct_gap_bound_sha256": _integer_sha256(distinct_gap_bound),
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
                raise AssertionError(f"M53 field changed: {field}")
        if level_span < candidate_count - 1:
            raise AssertionError("M53 packing inequality failed")
        if distinct_gap_bound >= subset_bound:
            raise AssertionError("M53 subset reduction failed")
        profile_checks += 1
        integer_hash_checks += 3
        reduction_checks += 1

    print(
        "M53 distinct-gap differential validation: PASS "
        f"({profile_checks} profile checks, "
        f"{integer_hash_checks} exact-integer hash checks, "
        f"{reduction_checks} subset-reduction checks)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
