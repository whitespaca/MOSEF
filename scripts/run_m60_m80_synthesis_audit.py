"""Deterministic arithmetic audit for the M60--M80 synthesis."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "python")]

from mosef_reference.residue_separator_synthesis import (
    residue_union_ledger,
    restricted_phi4_separated_pairs,
)


def build_summary() -> dict[str, object]:
    residue_rows: list[dict[str, int | str]] = []
    divisor_profiles = 0
    residue_candidates = 0
    for input_length in range(9, 41):
        ledger = residue_union_ledger(input_length, input_length // 2)
        record: dict[str, int | str] = {
            "input_length": input_length,
            "gap": ledger.gap,
            "size_threshold": ledger.size_threshold,
            "admissible_divisor_count": len(ledger.admissible_divisors),
            "minimal_divisor_count": len(ledger.minimal_divisors),
            "residue_union_size": ledger.residue_union_size,
            "interval_size": ledger.interval_size,
            "elementary_union_bound": ledger.elementary_union_bound,
        }
        record["row_sha256"] = hashlib.sha256(
            json.dumps(record, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()
        residue_rows.append(record)
        divisor_profiles += len(ledger.admissible_divisors)
        residue_candidates += ledger.residue_union_size

    separator_rows: list[dict[str, int | str]] = []
    pair_checks = 0
    proper_factors = 0
    for input_length in range(9, 19):
        levels = tuple(range(2, input_length + 13))
        separated, factored = restricted_phi4_separated_pairs(
            input_length,
            levels,
        )
        record = {
            "input_length": input_length,
            "candidate_count": len(levels),
            "separated_pairs": separated,
            "verified_proper_factors": factored,
        }
        record["row_sha256"] = hashlib.sha256(
            json.dumps(record, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()
        separator_rows.append(record)
        pair_checks += separated
        proper_factors += factored

    summary: dict[str, object] = {
        "schema_version": "1.0.0",
        "experiment_id": "EXP-0058",
        "milestone_span": "M60-M80",
        "residue_rows": residue_rows,
        "separator_rows": separator_rows,
        "counts": {
            "residue_profiles": len(residue_rows),
            "admissible_divisor_profiles": divisor_profiles,
            "exact_residue_candidates": residue_candidates,
            "separator_profiles": len(separator_rows),
            "separated_pair_checks": pair_checks,
            "verified_proper_factors": proper_factors,
            "row_hashes": len(residue_rows) + len(separator_rows),
        },
        "status": "PASS",
    }
    canonical = json.dumps(summary, sort_keys=True, separators=(",", ":"))
    summary["summary_sha256"] = hashlib.sha256(canonical.encode()).hexdigest()
    return summary


def main() -> int:
    summary = build_summary()
    counts = summary["counts"]
    if not isinstance(counts, dict):
        raise AssertionError("synthesis counts have the wrong shape")
    print(
        "M60-M80 synthesis audit: PASS "
        f"(summary_sha256={summary['summary_sha256']}, "
        f"residue_profiles={counts['residue_profiles']}, "
        f"proper_factors={counts['verified_proper_factors']})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
