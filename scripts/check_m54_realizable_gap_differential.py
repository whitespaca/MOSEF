"""Independently validate the registered M54 realizable-gap records."""

from __future__ import annotations

import hashlib
import itertools
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas/m54-realizable-gap-v1.json"


def _sequence_sha256(values: tuple[int, ...]) -> str:
    payload = ",".join(str(value) for value in values).encode("ascii")
    return hashlib.sha256(payload).hexdigest()


def _realized_gaps(
    levels: tuple[int, ...],
    overlap_order: int,
) -> tuple[int, ...]:
    gaps: set[int] = set()
    for subset in itertools.combinations(levels, overlap_order + 1):
        gaps.add(
            math.gcd(*(value - subset[0] for value in subset[1:]))
        )
    return tuple(sorted(gaps))


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
        raise AssertionError("M54 canonical summary hash changed")

    witness_checks = 0
    profile_checks = 0
    subset_checks = 0
    hash_checks = 0
    for record in data["extremal_witnesses"]:
        order = int(record["overlap_order"])
        gap = int(record["common_gap"])
        levels = tuple(2 + index * gap for index in range(order + 1))
        realized = _realized_gaps(levels, order)
        expected = {
            "candidate_count": len(levels),
            "span": order * gap,
            "dense_candidate_count": order * gap + 1,
            "dense_packing_slack": 0,
            "universal_upper_bound": gap,
            "realized_gap_count": 1,
            "maximum_realized_gap": gap,
            "levels_sha256": _sequence_sha256(levels),
            "gaps_sha256": _sequence_sha256(realized),
        }
        for field, value in expected.items():
            if record[field] != value:
                raise AssertionError(f"M54 witness field changed: {field}")
        witness_checks += 1
        subset_checks += 1
        hash_checks += 2

    for record in data["ambient_profiles"]:
        scale = int(record["scale"])
        order = int(record["overlap_order"])
        levels = tuple(2 + scale * index for index in range(6))
        realized = _realized_gaps(levels, order)
        span = levels[-1] - levels[0]
        expected = {
            "candidate_count": len(levels),
            "span": span,
            "subset_count": math.comb(len(levels), order + 1),
            "realized_gap_count": len(realized),
            "maximum_realized_gap": max(realized),
            "universal_upper_bound": span // order,
            "levels_sha256": _sequence_sha256(levels),
            "gaps_sha256": _sequence_sha256(realized),
        }
        for field, value in expected.items():
            if record[field] != value:
                raise AssertionError(f"M54 profile field changed: {field}")
        profile_checks += 1
        subset_checks += int(record["subset_count"])
        hash_checks += 2

    print(
        "M54 realizable-gap differential validation: PASS "
        f"({witness_checks} extremal witnesses, "
        f"{profile_checks} ambient profiles, "
        f"{subset_checks} subset enumerations, "
        f"{hash_checks} sequence-hash checks)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
