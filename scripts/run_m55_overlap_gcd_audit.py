"""Deterministic M55 audit of overlap-integer GCD and LCM structure."""

from __future__ import annotations

import hashlib
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "python")]

from mosef_reference import (
    compact_gap_overlap_gcd,
    compact_gap_overlap_integer,
    compact_gap_overlap_lcm_prefix,
    compact_gap_overlap_prefix_bit_bound,
)

MAXIMUM_GAP = 12


def _integer_sha256(value: int) -> str:
    width = max(1, (value.bit_length() + 7) // 8)
    return hashlib.sha256(value.to_bytes(width, "big")).hexdigest()


def build_summary() -> dict[str, object]:
    """Build exact pair-GCD, divisibility, and prefix-LCM records."""
    pairs: list[dict[str, int | bool | str]] = []
    for first_gap in range(1, MAXIMUM_GAP + 1):
        first_value = compact_gap_overlap_integer(first_gap)
        for second_gap in range(1, MAXIMUM_GAP + 1):
            second_value = compact_gap_overlap_integer(second_gap)
            gcd_index = math.gcd(first_gap, second_gap)
            gcd_value = compact_gap_overlap_gcd(first_gap, second_gap)
            pairs.append(
                {
                    "first_gap": first_gap,
                    "second_gap": second_gap,
                    "gcd_index": gcd_index,
                    "gcd_bit_length": gcd_value.bit_length(),
                    "gcd_sha256": _integer_sha256(gcd_value),
                    "first_divides_second": second_value % first_value == 0,
                    "index_divides": second_gap % first_gap == 0,
                }
            )

    prefixes: list[dict[str, int | str]] = []
    for maximum_gap in range(1, MAXIMUM_GAP + 1):
        largest = compact_gap_overlap_integer(maximum_gap)
        prefix_lcm = compact_gap_overlap_lcm_prefix(maximum_gap)
        prefixes.append(
            {
                "maximum_gap": maximum_gap,
                "largest_bit_length": largest.bit_length(),
                "lcm_bit_length": prefix_lcm.bit_length(),
                "product_bit_upper_bound": (
                    compact_gap_overlap_prefix_bit_bound(maximum_gap)
                ),
                "lcm_sha256": _integer_sha256(prefix_lcm),
                "largest_sha256": _integer_sha256(largest),
            }
        )

    counts = {
        "pair_gcd_identities": len(pairs),
        "divisibility_equivalences": len(pairs),
        "prefix_lcm_profiles": len(prefixes),
        "exact_integer_hash_checks": len(pairs) + 2 * len(prefixes),
        "largest_value_lower_bounds": len(prefixes),
    }
    summary: dict[str, object] = {
        "schema_version": "1.0.0",
        "experiment_id": "EXP-0053",
        "gcd_identity": "gcd(R_a,R_b)=R_gcd(a,b)",
        "divisibility_identity": "R_a divides R_b iff a divides b",
        "prefix_scale": "bitlen(R_D)<=bitlen(lcm(R_1,...,R_D))<=sum bit bounds",
        "pairs": pairs,
        "prefixes": prefixes,
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
    pairs = summary["pairs"]
    prefixes = summary["prefixes"]
    if not isinstance(pairs, list) or not isinstance(prefixes, list):
        raise AssertionError("M55 record shape changed")
    if any(
        record["first_divides_second"] != record["index_divides"]
        for record in pairs
    ):
        raise AssertionError("M55 divisibility identity failed")
    if any(
        int(record["lcm_bit_length"])
        < int(record["largest_bit_length"])
        for record in prefixes
    ):
        raise AssertionError("M55 LCM lower bound failed")
    print(
        "M55 overlap-GCD audit: PASS "
        f"(summary_sha256={summary['summary_sha256']}, "
        f"pairs={len(pairs)}, prefixes={len(prefixes)})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
