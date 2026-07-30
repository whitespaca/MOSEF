"""Independently validate registered M58 overlap-prime order records."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas/m58-overlap-prime-order-v1.json"


def _primes_up_to(limit: int) -> tuple[int, ...]:
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[:2] = b"\x00\x00"
    for prime in range(2, math.isqrt(limit) + 1):
        if sieve[prime]:
            start = prime * prime
            sieve[start : limit + 1 : prime] = b"\x00" * (
                (limit - start) // prime + 1
            )
    return tuple(
        value
        for value in range(11, limit + 1)
        if sieve[value]
    )


def _factorization(value: int) -> tuple[tuple[int, int], ...]:
    factors: list[tuple[int, int]] = []
    divisor = 2
    remaining = value
    while divisor * divisor <= remaining:
        exponent = 0
        while remaining % divisor == 0:
            remaining //= divisor
            exponent += 1
        if exponent:
            factors.append((divisor, exponent))
        divisor += 1 if divisor == 2 else 2
    if remaining > 1:
        factors.append((remaining, 1))
    return tuple(factors)


def _order(base: int, modulus: int) -> int:
    if modulus == 1:
        return 1
    totient = modulus
    for prime, _ in _factorization(modulus):
        totient = totient // prime * (prime - 1)
    order = totient
    for prime, _ in _factorization(totient):
        while order % prime == 0 and pow(
            base,
            order // prime,
            modulus,
        ) == 1:
            order //= prime
    return order


def _sequence_sha256(values: tuple[int, ...]) -> str:
    payload = ",".join(str(value) for value in values).encode("ascii")
    return hashlib.sha256(payload).hexdigest()


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
        raise AssertionError("M58 canonical summary hash changed")

    maximum_gap = int(data["maximum_gap"])
    prime_checks = 0
    direct_checks = 0
    periodicity_checks = 0
    hash_checks = 0
    hit_primes = 0
    aggregate = hashlib.sha256()
    reconstructed_hits: list[dict[str, int | bool | list[int] | str]] = []
    for prime in _primes_up_to(int(data["prime_maximum"])):
        if len(_factorization(prime)) != 1:
            raise AssertionError("M58 record is not prime")
        ratio = 3 * pow(32, -1, prime) % prime
        ratio_order = _order(ratio, prime)
        half = (
            ratio_order // 2
            if ratio_order % 2 == 0 and (ratio_order // 2) % 2 == 1
            else 0
        )
        period = _order(2, half) if half else 0
        predicted = (
            tuple(
                gap
                for gap in range(1, maximum_gap + 1)
                if gap % period == 0
            )
            if period
            else ()
        )
        direct = tuple(
            gap
            for gap in range(1, maximum_gap + 1)
            if (
                pow(3, (1 << gap) - 1, prime)
                + pow(32, (1 << gap) - 1, prime)
            )
            % prime
            == 0
        )
        record: dict[str, int | bool | list[int] | str] = {
            "prime": prime,
            "ratio_residue": ratio,
            "ratio_order": ratio_order,
            "odd_half_order": half,
            "occurrence_period": period,
            "predicted_occurrence_gaps": list(predicted),
            "direct_occurrence_gaps": list(direct),
            "occurrence_sha256": _sequence_sha256(direct),
            "characterization_holds": predicted == direct,
        }
        aggregate.update(
            json.dumps(
                record,
                sort_keys=True,
                separators=(",", ":"),
            ).encode("utf-8")
        )
        aggregate.update(b"\n")
        if direct:
            hit_primes += 1
            periodicity_checks += len(direct)
            reconstructed_hits.append(record)
            if ratio_order != 2 * half or math.gcd(2, half) != 1:
                raise AssertionError("M58 odd-half order condition failed")
        prime_checks += 1
        direct_checks += maximum_gap
        hash_checks += 1

    counts = data["counts"]
    expected_counts = {
        "prime_profiles": prime_checks,
        "hit_primes": hit_primes,
        "miss_primes": prime_checks - hit_primes,
        "direct_divisibility_checks": direct_checks,
        "periodicity_checks": periodicity_checks,
        "sequence_hash_checks": hash_checks,
    }
    if counts != expected_counts:
        raise AssertionError("M58 registered counts changed")
    if data["all_profiles_sha256"] != aggregate.hexdigest():
        raise AssertionError("M58 aggregate profile hash changed")
    if data["hit_profiles"] != reconstructed_hits:
        raise AssertionError("M58 registered hit profiles changed")
    print(
        "M58 overlap-prime order differential validation: PASS "
        f"({prime_checks} primes, {direct_checks} divisibility checks, "
        f"{periodicity_checks} periodic hits, {hash_checks} hashes)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
