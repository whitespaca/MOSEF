"""Independently validate registered M55 overlap GCD and LCM records."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas/m55-overlap-gcd-v1.json"


def _overlap_integer(gap: int) -> int:
    exponent = (1 << gap) - 1
    return pow(3, exponent) + pow(32, exponent)


def _integer_sha256(value: int) -> str:
    width = max(1, (value.bit_length() + 7) // 8)
    return hashlib.sha256(value.to_bytes(width, "big")).hexdigest()


def _lcm(values: list[int]) -> int:
    result = 1
    for value in values:
        result = result // math.gcd(result, value) * value
    return result


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
        raise AssertionError("M55 canonical summary hash changed")

    pair_checks = 0
    prefix_checks = 0
    hash_checks = 0
    for record in data["pairs"]:
        first_gap = int(record["first_gap"])
        second_gap = int(record["second_gap"])
        first = _overlap_integer(first_gap)
        second = _overlap_integer(second_gap)
        gcd_value = math.gcd(first, second)
        expected = {
            "gcd_index": math.gcd(first_gap, second_gap),
            "gcd_bit_length": gcd_value.bit_length(),
            "gcd_sha256": _integer_sha256(gcd_value),
            "first_divides_second": second % first == 0,
            "index_divides": second_gap % first_gap == 0,
        }
        if gcd_value != _overlap_integer(int(record["gcd_index"])):
            raise AssertionError("M55 GCD identity failed")
        for field, value in expected.items():
            if record[field] != value:
                raise AssertionError(f"M55 pair field changed: {field}")
        pair_checks += 1
        hash_checks += 1

    values: list[int] = []
    for record in data["prefixes"]:
        maximum_gap = int(record["maximum_gap"])
        values.append(_overlap_integer(maximum_gap))
        prefix_lcm = _lcm(values)
        largest = values[-1]
        product_upper = sum(
            5 * ((1 << gap) - 1) + 1
            for gap in range(1, maximum_gap + 1)
        )
        expected = {
            "largest_bit_length": largest.bit_length(),
            "lcm_bit_length": prefix_lcm.bit_length(),
            "product_bit_upper_bound": product_upper,
            "lcm_sha256": _integer_sha256(prefix_lcm),
            "largest_sha256": _integer_sha256(largest),
        }
        for field, value in expected.items():
            if record[field] != value:
                raise AssertionError(f"M55 prefix field changed: {field}")
        prefix_checks += 1
        hash_checks += 2

    print(
        "M55 overlap-GCD differential validation: PASS "
        f"({pair_checks} pair identities, "
        f"{prefix_checks} LCM prefixes, "
        f"{hash_checks} exact-integer hashes)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
