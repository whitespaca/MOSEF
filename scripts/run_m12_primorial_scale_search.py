"""Audit the M12 factor-scale divisor bound and finite promise fractions."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

from mosef_reference import (
    combined_signature,
    first_primes,
    primorial_divisors,
    primorial_factor_scale_bound,
)


def canonical_json(value: Any) -> bytes:
    """Serialize a value deterministically for hashing."""
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def prime_table(limit: int) -> list[int]:
    """Return every prime through ``limit`` by an exact bytearray sieve."""
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0:2] = b"\x00\x00"
    for prime in range(2, math.isqrt(limit) + 1):
        if not sieve[prime]:
            continue
        start = prime * prime
        sieve[start : limit + 1 : prime] = b"\x00" * (
            (limit - start) // prime + 1
        )
    return [value for value, flag in enumerate(sieve) if flag]


def primorial(count: int) -> int:
    """Return the product of the first ``count`` primes."""
    value = 1
    for prime in first_primes(count):
        value *= prime
    return value


def search(primorial_count_max: int, target_bit_max: int) -> dict[str, Any]:
    """Run the registered exact finite checks."""
    if not 1 <= primorial_count_max <= 18:
        raise ValueError("primorial_count_max must lie in [1, 18]")
    if not 4 <= target_bit_max <= 22:
        raise ValueError("target_bit_max must lie in [4, 22]")

    primes = prime_table(1 << target_bit_max)
    prime_set = set(primes)
    divisor_checks = 0
    support_checks = 0
    prime_candidate_checks = 0
    records: list[dict[str, int]] = []
    for count in range(1, primorial_count_max + 1):
        divisors = primorial_divisors(count)
        schedule_primes = first_primes(count)
        for target_bits in range(2, target_bit_max + 1):
            target_max = (1 << target_bits) - 1
            bound = primorial_factor_scale_bound(count, target_max)
            relevant = [
                divisor for divisor in divisors if divisor <= target_max + 1
            ]
            divisor_checks += len(divisors)
            if len(relevant) > bound.divisor_candidate_bound:
                raise AssertionError("factor-scale divisor bound failed")
            for divisor in relevant:
                support = sum(divisor % prime == 0 for prime in schedule_primes)
                support_checks += 1
                if support > bound.support_limit:
                    raise AssertionError("support threshold failed")
            hits = {
                candidate
                for divisor in relevant
                for candidate in (divisor - 1, divisor + 1)
                if 3 <= candidate <= target_max
                and candidate % 2 == 1
                and candidate in prime_set
            }
            prime_candidate_checks += 2 * len(relevant)
            if len(hits) > bound.prime_candidate_bound:
                raise AssertionError("prime-candidate bound failed")
        final_bound = primorial_factor_scale_bound(
            count, (1 << target_bit_max) - 1
        )
        records.append(
            {
                "prime_count": count,
                "total_divisors": len(divisors),
                "relevant_divisors": sum(
                    divisor <= 1 << target_bit_max for divisor in divisors
                ),
                "support_limit": final_bound.support_limit,
                "divisor_bound": final_bound.divisor_candidate_bound,
            }
        )

    population_records: list[dict[str, int]] = []
    pair_formula_checks = 0
    for factor_bits in range(4, target_bit_max + 1):
        # For k=2*factor_bits, every product of two primes in this interval
        # lies in [2^(k-1), 2^k), so all products have common bit length k.
        lower = math.isqrt(1 << (2 * factor_bits - 1))
        if lower * lower < 1 << (2 * factor_bits - 1):
            lower += 1
        upper = 1 << factor_bits
        population = [prime for prime in primes if lower <= prime < upper]
        if len(population) < 2:
            continue
        input_bits = 2 * factor_bits
        exponent = primorial(input_bits)
        signatures = {
            prime: combined_signature(prime, [exponent])[0]
            for prime in population
        }
        minus = sum(value == (True, False) for value in signatures.values())
        plus = sum(value == (False, True) for value in signatures.values())
        zero = sum(value == (False, False) for value in signatures.values())
        if any(value == (True, True) for value in signatures.values()):
            raise AssertionError("odd prime hit both primorial channels")
        promised_pairs = minus * plus + zero * (minus + plus)
        pair_formula_checks += 1
        if factor_bits <= 12:
            direct = sum(
                signatures[left] != signatures[right]
                for index, left in enumerate(population)
                for right in population[index + 1 :]
            )
            if direct != promised_pairs:
                raise AssertionError("three-signature pair formula failed")
        population_records.append(
            {
                "input_bits": input_bits,
                "population_size": len(population),
                "minus_hits": minus,
                "plus_hits": plus,
                "zero_signatures": zero,
                "promised_pairs": promised_pairs,
                "total_pairs": math.comb(len(population), 2),
            }
        )

    result: dict[str, Any] = {
        "schema_version": "1.0.0",
        "parameters": {
            "primorial_count_max": primorial_count_max,
            "target_bit_max": target_bit_max,
        },
        "counts": {
            "divisor_checks": divisor_checks,
            "support_checks": support_checks,
            "prime_candidate_checks": prime_candidate_checks,
            "pair_formula_checks": pair_formula_checks,
        },
        "primorial_records": records,
        "population_records": population_records,
    }
    result["summary_sha256"] = hashlib.sha256(canonical_json(result)).hexdigest()
    return result


def main() -> int:
    """Parse arguments, execute the audit, and print canonical JSON."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--primorial-count-max", type=int, default=18)
    parser.add_argument("--target-bit-max", type=int, default=20)
    args = parser.parse_args()
    result = search(args.primorial_count_max, args.target_bit_max)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
