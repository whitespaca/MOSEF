"""Independently reconstruct the registered M81 bit-length audit."""

from __future__ import annotations

import hashlib
import json
from math import isqrt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas/m81-bitlength-audit-v1.json"
FINITE_SUMMARY = ROOT / "schemas/m50-finite-threshold-summary-v1.json"


def _standard_length(value: int) -> int:
    count = 0
    remaining = value
    while remaining:
        count += 1
        remaining //= 2
    return count


def _legacy_length(value: int) -> int:
    exponent = 0
    threshold = 1
    while threshold < value:
        threshold *= 2
        exponent += 1
    return exponent


def _is_prime(value: int) -> bool:
    if value < 2:
        return False
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            return False
        divisor += 1 if divisor == 2 else 2
    return True


def _row_hash(row: dict[str, int | str]) -> str:
    return hashlib.sha256(
        json.dumps(row, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def _discrepancy_rows(maximum_value: int) -> list[dict[str, int | str]]:
    rows: list[dict[str, int | str]] = []
    for value in range(1, maximum_value + 1):
        standard = _standard_length(value)
        legacy = _legacy_length(value)
        if standard == legacy:
            continue
        row: dict[str, int | str] = {
            "value": value,
            "standard_bit_length": standard,
            "legacy_ceiling_log_length": legacy,
            "discrepancy": standard - legacy,
        }
        row["row_sha256"] = _row_hash(row)
        rows.append(row)
    return rows


def _finite_rows() -> tuple[list[dict[str, int | str]], int, int]:
    source = json.loads(FINITE_SUMMARY.read_text(encoding="utf-8"))
    rows: list[dict[str, int | str]] = []
    total_primes = 0
    total_pairs = 0
    for source_row in source["rows"]:
        input_length = int(source_row["input_length"])
        lower = isqrt((1 << (input_length - 1)) - 1) + 1
        upper = isqrt((1 << input_length) - 1)
        primes = tuple(
            value for value in range(lower, upper + 1) if _is_prime(value)
        )
        if len(primes) != int(source_row["population_size"]):
            raise AssertionError("independent M50 population changed")
        minimum_product = primes[0] * primes[0]
        maximum_product = primes[-1] * primes[-1]
        if (
            _standard_length(minimum_product) != input_length
            or _standard_length(maximum_product) != input_length
            or _legacy_length(minimum_product) != input_length
            or _legacy_length(maximum_product) != input_length
        ):
            raise AssertionError("independent balanced boundary changed")
        pair_count = len(primes) * (len(primes) - 1) // 2
        row: dict[str, int | str] = {
            "input_length": input_length,
            "interval_lower": lower,
            "interval_upper": upper,
            "population_size": len(primes),
            "distinct_pair_count": pair_count,
            "minimum_product_bit_length": _standard_length(minimum_product),
            "maximum_product_bit_length": _standard_length(maximum_product),
            "legacy_index_agrees": 1,
        }
        row["row_sha256"] = _row_hash(row)
        rows.append(row)
        total_primes += len(primes)
        total_pairs += pair_count
    return rows, total_primes, total_pairs


def main() -> int:
    data = json.loads(SCHEMA.read_text(encoding="utf-8"))
    canonical = dict(data)
    expected_hash = canonical.pop("summary_sha256")
    actual_hash = hashlib.sha256(
        json.dumps(canonical, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    if actual_hash != expected_hash:
        raise AssertionError("M81 canonical hash changed")

    maximum_value = int(data["maximum_audited_value"])
    discrepancy_rows = _discrepancy_rows(maximum_value)
    if discrepancy_rows != data["discrepancy_rows"]:
        raise AssertionError("M81 discrepancy rows changed")

    finite_rows, total_primes, total_pairs = _finite_rows()
    if finite_rows != data["finite_certificate_rows"]:
        raise AssertionError("M81 finite-certificate rows changed")

    source = json.loads(FINITE_SUMMARY.read_text(encoding="utf-8"))
    if data["finite_certificate_source"]["summary_sha256"] != source["summary_sha256"]:
        raise AssertionError("M50 source summary changed")

    for row in data["implementation_semantics"]:
        text = (ROOT / row["path"]).read_text(encoding="utf-8")
        if row["required_token"] not in text:
            raise AssertionError(f"implementation token changed: {row['path']}")

    counts = {
        "positive_integers_checked": maximum_value,
        "power_of_two_discrepancies": len(discrepancy_rows),
        "non_power_agreements": maximum_value - len(discrepancy_rows),
        "finite_input_lengths_checked": len(finite_rows),
        "finite_population_primes": total_primes,
        "finite_distinct_prime_pairs": total_pairs,
        "standard_implementations_checked": len(data["implementation_semantics"]),
        "row_hashes": len(discrepancy_rows) + len(finite_rows),
    }
    if counts != data["counts"]:
        raise AssertionError("M81 counts changed")
    print(
        "M81 bit-length differential validation: PASS "
        f"({maximum_value} integers, {len(discrepancy_rows)} discrepancies, "
        f"{len(finite_rows)} finite rows)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
