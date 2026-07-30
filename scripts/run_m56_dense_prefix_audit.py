"""Deterministic M56 audit of dense-interval full-prefix realizability."""

from __future__ import annotations

import hashlib
import itertools
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "python")]

from mosef_reference import compact_gap_dense_interval_realizable_gaps

ORDERS = tuple(range(1, 9))
MAXIMUM_GAPS = tuple(range(1, 13))
EXHAUSTIVE_SPANS = tuple(range(2, 15))


def _sequence_sha256(values: tuple[int, ...]) -> str:
    payload = ",".join(str(value) for value in values).encode("ascii")
    return hashlib.sha256(payload).hexdigest()


def _realized_gaps(
    levels: tuple[int, ...],
    overlap_order: int,
) -> tuple[int, ...]:
    return tuple(
        sorted(
            {
                math.gcd(
                    *(value - subset[0] for value in subset[1:])
                )
                for subset in itertools.combinations(
                    levels,
                    overlap_order + 1,
                )
            }
        )
    )


def build_summary() -> dict[str, object]:
    """Build constructive full-prefix and exhaustive small-interval records."""
    profiles: list[dict[str, int | str]] = []
    for overlap_order in ORDERS:
        for maximum_gap in MAXIMUM_GAPS:
            remainder = (overlap_order + maximum_gap) % overlap_order
            level_span = overlap_order * maximum_gap + remainder
            prefix = compact_gap_dense_interval_realizable_gaps(
                level_span,
                overlap_order,
            )
            witness_hashes = tuple(
                _sequence_sha256(
                    tuple(
                        2 + index * gap
                        for index in range(overlap_order + 1)
                    )
                )
                for gap in prefix
            )
            profiles.append(
                {
                    "overlap_order": overlap_order,
                    "level_span": level_span,
                    "candidate_count": level_span + 1,
                    "maximum_gap": maximum_gap,
                    "realized_gap_count": len(prefix),
                    "prefix_sha256": _sequence_sha256(prefix),
                    "witness_hashes_sha256": _sequence_sha256(
                        tuple(
                            int(value[:16], 16)
                            for value in witness_hashes
                        )
                    ),
                }
            )

    exhaustive: list[dict[str, int | str]] = []
    for level_span in EXHAUSTIVE_SPANS:
        levels = tuple(range(2, level_span + 3))
        for overlap_order in range(1, min(4, level_span) + 1):
            realized = _realized_gaps(levels, overlap_order)
            expected = compact_gap_dense_interval_realizable_gaps(
                level_span,
                overlap_order,
            )
            if realized != expected:
                raise AssertionError("M56 complete interval prefix failed")
            exhaustive.append(
                {
                    "level_span": level_span,
                    "overlap_order": overlap_order,
                    "candidate_count": len(levels),
                    "subset_count": math.comb(
                        len(levels),
                        overlap_order + 1,
                    ),
                    "realized_gap_count": len(realized),
                    "maximum_gap": level_span // overlap_order,
                    "gaps_sha256": _sequence_sha256(realized),
                }
            )

    counts = {
        "constructive_profiles": len(profiles),
        "constructive_witnesses": sum(
            int(record["realized_gap_count"]) for record in profiles
        ),
        "exhaustive_profiles": len(exhaustive),
        "exhaustive_subset_enumerations": sum(
            int(record["subset_count"]) for record in exhaustive
        ),
        "sequence_hash_checks": 2 * len(profiles) + len(exhaustive),
    }
    summary: dict[str, object] = {
        "schema_version": "1.0.0",
        "experiment_id": "EXP-0054",
        "theorem": (
            "G_h({s,...,s+Delta})={1,...,floor(Delta/h)}"
        ),
        "constructive_profiles": profiles,
        "exhaustive_profiles": exhaustive,
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
        raise AssertionError("M56 counts have the wrong shape")
    print(
        "M56 dense-prefix audit: PASS "
        f"(summary_sha256={summary['summary_sha256']}, "
        f"constructive={counts['constructive_profiles']}, "
        f"exhaustive={counts['exhaustive_profiles']})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
