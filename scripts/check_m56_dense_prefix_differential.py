"""Independently validate registered M56 dense-interval prefix records."""

from __future__ import annotations

import hashlib
import itertools
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas/m56-dense-prefix-v1.json"


def _sequence_sha256(values: tuple[int, ...]) -> str:
    payload = ",".join(str(value) for value in values).encode("ascii")
    return hashlib.sha256(payload).hexdigest()


def _realized_gaps(
    levels: tuple[int, ...],
    order: int,
) -> tuple[int, ...]:
    gaps: set[int] = set()
    for subset in itertools.combinations(levels, order + 1):
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
        raise AssertionError("M56 canonical summary hash changed")

    constructive_checks = 0
    witness_checks = 0
    exhaustive_checks = 0
    subset_checks = 0
    hash_checks = 0
    for record in data["constructive_profiles"]:
        order = int(record["overlap_order"])
        span = int(record["level_span"])
        maximum_gap = span // order
        prefix = tuple(range(1, maximum_gap + 1))
        witness_hashes = tuple(
            _sequence_sha256(
                tuple(2 + index * gap for index in range(order + 1))
            )
            for gap in prefix
        )
        expected = {
            "candidate_count": span + 1,
            "maximum_gap": maximum_gap,
            "realized_gap_count": len(prefix),
            "prefix_sha256": _sequence_sha256(prefix),
            "witness_hashes_sha256": _sequence_sha256(
                tuple(int(value[:16], 16) for value in witness_hashes)
            ),
        }
        for field, value in expected.items():
            if record[field] != value:
                raise AssertionError(
                    f"M56 constructive field changed: {field}"
                )
        for gap in prefix:
            if order * gap > span:
                raise AssertionError("M56 witness left the interval")
        constructive_checks += 1
        witness_checks += len(prefix)
        hash_checks += 2

    for record in data["exhaustive_profiles"]:
        span = int(record["level_span"])
        order = int(record["overlap_order"])
        levels = tuple(range(2, span + 3))
        realized = _realized_gaps(levels, order)
        expected_prefix = tuple(range(1, span // order + 1))
        if realized != expected_prefix:
            raise AssertionError("M56 exhaustive prefix changed")
        expected = {
            "candidate_count": len(levels),
            "subset_count": math.comb(len(levels), order + 1),
            "realized_gap_count": len(realized),
            "maximum_gap": span // order,
            "gaps_sha256": _sequence_sha256(realized),
        }
        for field, value in expected.items():
            if record[field] != value:
                raise AssertionError(
                    f"M56 exhaustive field changed: {field}"
                )
        exhaustive_checks += 1
        subset_checks += int(record["subset_count"])
        hash_checks += 1

    print(
        "M56 dense-prefix differential validation: PASS "
        f"({constructive_checks} constructive profiles, "
        f"{witness_checks} explicit witnesses, "
        f"{exhaustive_checks} exhaustive profiles, "
        f"{subset_checks} subset enumerations, "
        f"{hash_checks} sequence hashes)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
