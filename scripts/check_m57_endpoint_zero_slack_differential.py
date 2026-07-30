"""Independently validate registered M57 endpoint obstruction records."""

from __future__ import annotations

import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas/m57-endpoint-zero-slack-v1.json"


def _integer_sha256(value: int) -> str:
    width = max(1, (value.bit_length() + 7) // 8)
    return hashlib.sha256(value.to_bytes(width, "big")).hexdigest()


def _low_capacity(candidate_count: int, order: int) -> int:
    return sum(
        math.comb(candidate_count, weight)
        for weight in range(order + 1)
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
        raise AssertionError("M57 canonical summary hash changed")

    endpoint_checks = 0
    integer_hash_checks = 0
    for record in data["endpoint_profiles"]:
        scale_exponent = int(record["scale_exponent"])
        level_span = (1 << scale_exponent) - 2
        candidate_count = level_span + 1
        radicand = 2 * scale_exponent * level_span
        root = math.isqrt(radicand)
        input_length = root + (root * root < radicand)
        switch_order = (2 * level_span) // input_length
        order = int(record["overlap_order"])
        maximum_gap = level_span // order
        lcm_bits = 5 * ((1 << maximum_gap) - 1) + 1
        prime_bits = (input_length - 1) // 2
        high_charge = lcm_bits // prime_bits
        low_capacity = _low_capacity(candidate_count, order)
        population = (1 << (input_length // 2)) // (81 * input_length)
        expected = {
            "input_length": input_length,
            "candidate_count": candidate_count,
            "level_span": level_span,
            "logarithmic_scale": candidate_count.bit_length(),
            "switch_order": switch_order,
            "maximum_common_gap": maximum_gap,
            "lcm_bit_length_lower_bound": lcm_bits,
            "high_weight_charge_lower_bound_sha256": _integer_sha256(
                high_charge
            ),
            "low_weight_signature_capacity_sha256": _integer_sha256(
                low_capacity
            ),
            "population_lower_bound_sha256": _integer_sha256(population),
            "high_ledger_consumes_population": high_charge >= population,
            "low_ledger_consumes_population": low_capacity >= population,
            "certificate_blocked": (
                high_charge >= population or low_capacity >= population
            ),
        }
        for field, value in expected.items():
            if record[field] != value:
                raise AssertionError(f"M57 endpoint field changed: {field}")
        endpoint_checks += 1
        integer_hash_checks += 3

    rational_checks = 0
    equality_checks = 0
    for record in data["rational_profiles"]:
        value = Fraction(
            int(record["x_numerator"]),
            int(record["x_denominator"]),
        )
        high = Fraction(1, 2) / value
        low = value / 2
        maximum = max(high, low)
        expected = {
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
        for field, expected_value in expected.items():
            if record[field] != expected_value:
                raise AssertionError(
                    f"M57 rational field changed: {field}"
                )
        rational_checks += 1
        equality_checks += maximum == Fraction(1, 2)

    if equality_checks != 1:
        raise AssertionError("M57 equality must occur only at x=1")
    print(
        "M57 endpoint zero-slack differential validation: PASS "
        f"({endpoint_checks} endpoint profiles, "
        f"{rational_checks} rational profiles, "
        f"{integer_hash_checks} integer hashes)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
