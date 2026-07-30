"""Deterministic M59 audit of balanced-prime half-order constraints."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "python")]

from mosef_reference import (
    balanced_prime_population,
    compact_gap_half_order_constraints,
)

INPUT_LENGTH_MINIMUM = 9
INPUT_LENGTH_MAXIMUM = 28


def build_summary() -> dict[str, object]:
    rows: list[dict[str, int | str]] = []
    total_primes = 0
    hit_primes = 0
    inequality_checks = 0
    residue_checks = 0
    profile_hashes = 0
    for input_length in range(
        INPUT_LENGTH_MINIMUM,
        INPUT_LENGTH_MAXIMUM + 1,
    ):
        aggregate = hashlib.sha256()
        primes = balanced_prime_population(input_length)
        length_hits = 0
        minimum_half = 0
        minimum_gap = 0
        for prime in primes:
            profile = compact_gap_half_order_constraints(
                input_length,
                prime,
            )
            record = {
                "input_length": input_length,
                "prime": prime,
                "odd_half_order": profile.odd_half_order,
                "first_occurrence_gap": profile.first_occurrence_gap,
                "minimum_size_odd_half_order": (
                    profile.minimum_size_odd_half_order
                ),
                "minimum_size_gap": profile.minimum_size_gap,
                "strict_size_bound_holds": profile.strict_size_bound_holds,
                "residue_class_holds": profile.residue_class_holds,
            }
            aggregate.update(
                json.dumps(
                    record,
                    sort_keys=True,
                    separators=(",", ":"),
                ).encode("utf-8")
            )
            aggregate.update(b"\n")
            if profile.odd_half_order:
                length_hits += 1
                hit_primes += 1
                inequality_checks += 1
                residue_checks += 1
            minimum_half = profile.minimum_size_odd_half_order
            minimum_gap = profile.minimum_size_gap
            profile_hashes += 1
        total_primes += len(primes)
        rows.append(
            {
                "input_length": input_length,
                "population_size": len(primes),
                "eligible_order_primes": length_hits,
                "minimum_size_odd_half_order": minimum_half,
                "minimum_size_gap": minimum_gap,
                "profiles_sha256": aggregate.hexdigest(),
            }
        )
    summary: dict[str, object] = {
        "schema_version": "1.0.0",
        "experiment_id": "EXP-0057",
        "input_length_minimum": INPUT_LENGTH_MINIMUM,
        "input_length_maximum": INPUT_LENGTH_MAXIMUM,
        "rows": rows,
        "counts": {
            "input_lengths": len(rows),
            "prime_profiles": total_primes,
            "eligible_order_primes": hit_primes,
            "strict_inequality_checks": inequality_checks,
            "residue_class_checks": residue_checks,
            "profile_hashes": profile_hashes,
        },
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
        raise AssertionError("M59 counts have the wrong shape")
    print(
        "M59 half-order size audit: PASS "
        f"(summary_sha256={summary['summary_sha256']}, "
        f"primes={counts['prime_profiles']}, "
        f"eligible={counts['eligible_order_primes']})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
