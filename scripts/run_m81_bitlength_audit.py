"""Build the deterministic M81 standard-bit-length migration audit."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "python")]

from mosef_reference.bitlength_audit import (
    balanced_prime_interval,
    balanced_prime_population,
    compare_lengths,
)

FINITE_SUMMARY = ROOT / "schemas/m50-finite-threshold-summary-v1.json"

STANDARD_IMPLEMENTATIONS = (
    {
        "language": "Python",
        "path": "python/mosef_reference/length_indexed_cofactor_schedule.py",
        "required_token": "(first_prime * second_prime).bit_length()",
    },
    {
        "language": "Rust",
        "path": "crates/mosef-arithmetic/src/lib.rs",
        "required_token": "u128::BITS - product.leading_zeros()",
    },
    {
        "language": "C#",
        "path": "verification/csharp/Program.cs",
        "required_token": ".GetBitLength()",
    },
)


def _row_hash(row: dict[str, int | str]) -> str:
    return hashlib.sha256(
        json.dumps(row, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def build_summary(maximum_exponent: int = 20) -> dict[str, object]:
    if maximum_exponent < 1:
        raise ValueError("maximum_exponent must be positive")

    maximum_value = 1 << maximum_exponent
    discrepancy_rows: list[dict[str, int | str]] = []
    discrepancy_count = 0
    for value in range(1, maximum_value + 1):
        comparison = compare_lengths(value)
        if comparison.discrepancy == 0:
            continue
        discrepancy_count += 1
        row: dict[str, int | str] = {
            "value": value,
            "standard_bit_length": comparison.standard_bit_length,
            "legacy_ceiling_log_length": comparison.legacy_ceiling_log_length,
            "discrepancy": comparison.discrepancy,
        }
        row["row_sha256"] = _row_hash(row)
        discrepancy_rows.append(row)

    finite_data = json.loads(FINITE_SUMMARY.read_text(encoding="utf-8"))
    finite_rows: list[dict[str, int | str]] = []
    total_population_primes = 0
    total_distinct_pairs = 0
    for source_row in finite_data["rows"]:
        input_length = int(source_row["input_length"])
        lower, upper = balanced_prime_interval(input_length)
        primes = balanced_prime_population(input_length)
        population_size = len(primes)
        if population_size != int(source_row["population_size"]):
            raise AssertionError("M50 finite population size changed")
        if not primes or primes[0] % 2 == 0 or primes[-1] % 2 == 0:
            raise AssertionError("balanced population must contain odd primes")
        minimum_product = primes[0] * primes[0]
        maximum_product = primes[-1] * primes[-1]
        minimum_comparison = compare_lengths(minimum_product)
        maximum_comparison = compare_lengths(maximum_product)
        if (
            minimum_comparison.standard_bit_length != input_length
            or maximum_comparison.standard_bit_length != input_length
            or minimum_comparison.legacy_ceiling_log_length != input_length
            or maximum_comparison.legacy_ceiling_log_length != input_length
        ):
            raise AssertionError("balanced-product length boundary changed")
        pair_count = population_size * (population_size - 1) // 2
        row = {
            "input_length": input_length,
            "interval_lower": lower,
            "interval_upper": upper,
            "population_size": population_size,
            "distinct_pair_count": pair_count,
            "minimum_product_bit_length": minimum_comparison.standard_bit_length,
            "maximum_product_bit_length": maximum_comparison.standard_bit_length,
            "legacy_index_agrees": 1,
        }
        row["row_sha256"] = _row_hash(row)
        finite_rows.append(row)
        total_population_primes += population_size
        total_distinct_pairs += pair_count

    implementation_rows: list[dict[str, str]] = []
    for implementation in STANDARD_IMPLEMENTATIONS:
        path = ROOT / implementation["path"]
        required_token = implementation["required_token"]
        if required_token not in path.read_text(encoding="utf-8"):
            raise AssertionError(f"standard bit-length token missing from {path}")
        implementation_rows.append(dict(implementation))

    summary: dict[str, object] = {
        "schema_version": "1.0.0",
        "experiment_id": "EXP-0059",
        "maximum_audited_value": maximum_value,
        "discrepancy_rows": discrepancy_rows,
        "finite_certificate_source": {
            "path": FINITE_SUMMARY.relative_to(ROOT).as_posix(),
            "summary_sha256": finite_data["summary_sha256"],
        },
        "finite_certificate_rows": finite_rows,
        "implementation_semantics": implementation_rows,
        "counts": {
            "positive_integers_checked": maximum_value,
            "power_of_two_discrepancies": discrepancy_count,
            "non_power_agreements": maximum_value - discrepancy_count,
            "finite_input_lengths_checked": len(finite_rows),
            "finite_population_primes": total_population_primes,
            "finite_distinct_prime_pairs": total_distinct_pairs,
            "standard_implementations_checked": len(implementation_rows),
            "row_hashes": len(discrepancy_rows) + len(finite_rows),
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
        raise AssertionError("M81 counts have the wrong shape")
    print(
        "M81 bit-length audit: PASS "
        f"(summary_sha256={summary['summary_sha256']}, "
        f"integers={counts['positive_integers_checked']}, "
        f"discrepancies={counts['power_of_two_discrepancies']}, "
        f"finite_rows={counts['finite_input_lengths_checked']})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
