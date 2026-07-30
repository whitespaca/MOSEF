"""Independently validate the registered M59 half-order constraints."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas/m59-half-order-size-v1.json"


def _primes(lower: int, upper: int) -> tuple[int, ...]:
    def is_prime(value: int) -> bool:
        if value < 2:
            return False
        divisor = 2
        while divisor * divisor <= value:
            if value % divisor == 0:
                return False
            divisor += 1 if divisor == 2 else 2
        return True

    return tuple(value for value in range(lower, upper + 1) if is_prime(value))


def _factorization(value: int) -> tuple[int, ...]:
    factors: list[int] = []
    divisor = 2
    remaining = value
    while divisor * divisor <= remaining:
        if remaining % divisor == 0:
            factors.append(divisor)
            while remaining % divisor == 0:
                remaining //= divisor
        divisor += 1 if divisor == 2 else 2
    if remaining > 1:
        factors.append(remaining)
    return tuple(factors)


def _order(base: int, prime: int) -> int:
    order = prime - 1
    for divisor in _factorization(prime - 1):
        while order % divisor == 0 and pow(
            base,
            order // divisor,
            prime,
        ) == 1:
            order //= divisor
    return order


def _order_modulus(base: int, modulus: int) -> int:
    if modulus == 1:
        return 1
    phi = modulus
    for divisor in _factorization(modulus):
        phi = phi // divisor * (divisor - 1)
    order = phi
    for divisor in _factorization(phi):
        while order % divisor == 0 and pow(
            base,
            order // divisor,
            modulus,
        ) == 1:
            order //= divisor
    return order


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
        raise AssertionError("M59 canonical summary hash changed")

    rows: list[dict[str, int | str]] = []
    total_primes = 0
    total_hits = 0
    for input_length in range(
        int(data["input_length_minimum"]),
        int(data["input_length_maximum"]) + 1,
    ):
        lower = math.isqrt((1 << (input_length - 1)) - 1) + 1
        upper = math.isqrt((1 << input_length) - 1)
        primes = _primes(lower, upper)
        threshold = 3
        while 33**threshold <= lower:
            threshold += 2
        aggregate = hashlib.sha256()
        hits = 0
        for prime in primes:
            ratio = 3 * pow(32, -1, prime) % prime
            ratio_order = _order(ratio, prime)
            half = (
                ratio_order // 2
                if ratio_order % 2 == 0
                and (ratio_order // 2) % 2 == 1
                else 0
            )
            first_gap = _order_modulus(2, half) if half else 0
            record = {
                "input_length": input_length,
                "prime": prime,
                "odd_half_order": half,
                "first_occurrence_gap": first_gap,
                "minimum_size_odd_half_order": threshold,
                "minimum_size_gap": threshold.bit_length(),
                "strict_size_bound_holds": (
                    half == 0 or prime < 33**half
                ),
                "residue_class_holds": (
                    half == 0 or (prime - 1) % (2 * half) == 0
                ),
            }
            if not record["strict_size_bound_holds"]:
                raise AssertionError("M59 strict size inequality failed")
            if not record["residue_class_holds"]:
                raise AssertionError("M59 residue class failed")
            if half and (
                half < threshold or first_gap < threshold.bit_length()
            ):
                raise AssertionError("M59 balanced lower bound failed")
            aggregate.update(
                json.dumps(
                    record,
                    sort_keys=True,
                    separators=(",", ":"),
                ).encode("utf-8")
            )
            aggregate.update(b"\n")
            hits += int(bool(half))
        rows.append(
            {
                "input_length": input_length,
                "population_size": len(primes),
                "eligible_order_primes": hits,
                "minimum_size_odd_half_order": threshold,
                "minimum_size_gap": threshold.bit_length(),
                "profiles_sha256": aggregate.hexdigest(),
            }
        )
        total_primes += len(primes)
        total_hits += hits
    if rows != data["rows"]:
        raise AssertionError("M59 rows changed")
    expected_counts = {
        "input_lengths": len(rows),
        "prime_profiles": total_primes,
        "eligible_order_primes": total_hits,
        "strict_inequality_checks": total_hits,
        "residue_class_checks": total_hits,
        "profile_hashes": total_primes,
    }
    if expected_counts != data["counts"]:
        raise AssertionError("M59 counts changed")
    print(
        "M59 half-order size differential validation: PASS "
        f"({len(rows)} lengths, {total_primes} primes, "
        f"{total_hits} eligible orders)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
