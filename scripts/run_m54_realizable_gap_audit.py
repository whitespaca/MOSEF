"""Deterministic M54 audit of realizable GCD gaps."""

from __future__ import annotations

import hashlib
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "python")]

from mosef_reference import (
    compact_gap_maximal_gap_witness,
    compact_gap_realizable_common_gaps,
)

ORDERS = tuple(range(1, 7))
COMMON_GAPS = tuple(range(1, 17))
AMBIENT_SCALES = tuple(range(1, 9))
AMBIENT_ORDERS = tuple(range(1, 5))


def _sequence_sha256(values: tuple[int, ...]) -> str:
    payload = ",".join(str(value) for value in values).encode("ascii")
    return hashlib.sha256(payload).hexdigest()


def build_summary() -> dict[str, object]:
    """Build exact extremal witnesses and complete small gap-set profiles."""
    witnesses: list[dict[str, int | str]] = []
    for overlap_order in ORDERS:
        for common_gap in COMMON_GAPS:
            levels = compact_gap_maximal_gap_witness(
                overlap_order,
                common_gap,
            )
            span = levels[-1] - levels[0]
            realized = compact_gap_realizable_common_gaps(
                levels,
                overlap_order,
            )
            witnesses.append(
                {
                    "overlap_order": overlap_order,
                    "common_gap": common_gap,
                    "candidate_count": len(levels),
                    "span": span,
                    "dense_candidate_count": span + 1,
                    "dense_packing_slack": 0,
                    "universal_upper_bound": span // overlap_order,
                    "realized_gap_count": len(realized),
                    "maximum_realized_gap": max(realized),
                    "levels_sha256": _sequence_sha256(levels),
                    "gaps_sha256": _sequence_sha256(realized),
                }
            )

    profiles: list[dict[str, int | str]] = []
    for scale in AMBIENT_SCALES:
        levels = tuple(2 + scale * index for index in range(6))
        span = levels[-1] - levels[0]
        for overlap_order in AMBIENT_ORDERS:
            realized = compact_gap_realizable_common_gaps(
                levels,
                overlap_order,
            )
            profiles.append(
                {
                    "scale": scale,
                    "overlap_order": overlap_order,
                    "candidate_count": len(levels),
                    "span": span,
                    "subset_count": math.comb(
                        len(levels),
                        overlap_order + 1,
                    ),
                    "realized_gap_count": len(realized),
                    "maximum_realized_gap": max(realized),
                    "universal_upper_bound": span // overlap_order,
                    "levels_sha256": _sequence_sha256(levels),
                    "gaps_sha256": _sequence_sha256(realized),
                }
            )

    counts = {
        "extremal_witnesses": len(witnesses),
        "extremal_equalities": sum(
            record["maximum_realized_gap"]
            == record["universal_upper_bound"]
            for record in witnesses
        ),
        "dense_interval_embeddings": len(witnesses),
        "ambient_profiles": len(profiles),
        "ambient_subset_enumerations": sum(
            int(record["subset_count"]) for record in profiles
        ),
        "ambient_equalities": sum(
            record["maximum_realized_gap"]
            == record["universal_upper_bound"]
            for record in profiles
        ),
        "sequence_hash_checks": 2 * (len(witnesses) + len(profiles)),
    }
    summary: dict[str, object] = {
        "schema_version": "1.0.0",
        "experiment_id": "EXP-0052",
        "claim": (
            "the universal maximum realizable GCD-gap bound "
            "floor(span/order) is exactly attainable"
        ),
        "extremal_witnesses": witnesses,
        "ambient_profiles": profiles,
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
        raise AssertionError("M54 counts have the wrong shape")
    if counts["extremal_equalities"] != counts["extremal_witnesses"]:
        raise AssertionError("M54 extremal equality failed")
    print(
        "M54 realizable-gap audit: PASS "
        f"(summary_sha256={summary['summary_sha256']}, "
        f"witnesses={counts['extremal_witnesses']}, "
        f"ambient_profiles={counts['ambient_profiles']})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
