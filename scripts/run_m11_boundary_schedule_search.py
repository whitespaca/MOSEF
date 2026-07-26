"""Audit the M11 boundary divisor budget and first-primes primorial schedule."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

from mosef_reference import (  # noqa: E402
    boundary_divisor_budget,
    primorial_divisors,
    primorial_schedule,
)


def canonical_json(value: Any) -> bytes:
    """Serialize a value deterministically for hashing."""
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def smallest_prime_factors(limit: int) -> list[int]:
    """Return an exact smallest-prime-factor table through ``limit``."""
    spf = list(range(limit + 1))
    if limit >= 1:
        spf[1] = 1
    for prime in range(2, math.isqrt(limit) + 1):
        if spf[prime] != prime:
            continue
        for multiple in range(prime * prime, limit + 1, prime):
            if spf[multiple] == multiple:
                spf[multiple] = prime
    return spf


def divisor_count_from_spf(value: int, spf: list[int]) -> int:
    """Return ``tau(value)`` using an exact smallest-prime-factor table."""
    remaining = value
    count = 1
    while remaining > 1:
        prime = spf[remaining]
        multiplicity = 0
        while remaining % prime == 0:
            remaining //= prime
            multiplicity += 1
        count *= multiplicity + 1
    return count


def prime_table(limit: int) -> list[int]:
    """Return every prime through ``limit`` by an exact bytearray sieve."""
    sieve = bytearray(b"\x01") * (limit + 1)
    if limit >= 0:
        sieve[0] = 0
    if limit >= 1:
        sieve[1] = 0
    for prime in range(2, math.isqrt(limit) + 1):
        if not sieve[prime]:
            continue
        start = prime * prime
        sieve[start : limit + 1 : prime] = b"\x00" * (
            (limit - start) // prime + 1
        )
    return [value for value, flag in enumerate(sieve) if flag]


def search(exponent_max: int, primorial_count_max: int) -> dict[str, Any]:
    """Run the registered exact finite checks."""
    if exponent_max < 2 or exponent_max > 1 << 20:
        raise ValueError("exponent_max must lie in [2, 2^20]")
    if primorial_count_max < 1 or primorial_count_max > 12:
        raise ValueError("primorial_count_max must lie in [1, 12]")

    spf = smallest_prime_factors(exponent_max - 1)
    budgets = {
        length: boundary_divisor_budget(length)
        for length in range(1, (exponent_max - 1).bit_length() + 1)
    }
    divisor_budget_checks = 0
    maximum_divisor_records: dict[int, tuple[int, int]] = {}
    for exponent in range(1, exponent_max):
        length = exponent.bit_length()
        count = divisor_count_from_spf(exponent, spf)
        budget = budgets[length]
        divisor_budget_checks += 1
        if count > budget.one_length_bound:
            raise AssertionError(("boundary divisor budget", exponent, count, budget))
        record = maximum_divisor_records.get(length, (0, 0))
        if count > record[0]:
            maximum_divisor_records[length] = (count, exponent)

    diagnostic_lengths = (16, 32, 64, 128, 256, 512, 1024, 2048, 4096)
    boundary_diagnostics: list[dict[str, int | str]] = []
    for length in diagnostic_lengths:
        budget = boundary_divisor_budget(length)
        normalized = (
            Fraction(
                (budget.one_length_bound.bit_length() - 1)
                * max(1, length.bit_length() - 1),
                length,
            )
        )
        boundary_diagnostics.append(
            {
                "bit_length": length,
                "split_threshold": budget.split_threshold,
                "large_multiplicity_bound": budget.large_multiplicity_bound,
                "one_length_bound_bit_length": budget.one_length_bound.bit_length(),
                "lower_log_normalized_ratio": (
                    f"{normalized.numerator}/{normalized.denominator}"
                ),
            }
        )

    largest_schedule = primorial_schedule(primorial_count_max)
    trial_primes = prime_table(math.isqrt(largest_schedule.exponent + 1))
    primality_cache: dict[int, bool] = {}
    primality_divisions = 0

    def is_prime_exact(value: int) -> bool:
        nonlocal primality_divisions
        if value in primality_cache:
            return primality_cache[value]
        if value < 2:
            primality_cache[value] = False
            return False
        for prime in trial_primes:
            if prime > value // prime:
                primality_cache[value] = True
                return True
            primality_divisions += 1
            if value % prime == 0:
                result = value == prime
                primality_cache[value] = result
                return result
        primality_cache[value] = True
        return True

    primorial_records: list[dict[str, int | str]] = []
    rosser_schoenfeld_checks = 0
    for count in range(1, primorial_count_max + 1):
        schedule = primorial_schedule(count)
        divisors = primorial_divisors(count)
        if len(divisors) != schedule.divisor_count:
            raise AssertionError(("primorial divisor count", count))
        if len(set(divisors)) != schedule.divisor_count:
            raise AssertionError(("duplicate primorial divisor", count))
        if any(schedule.exponent % divisor for divisor in divisors):
            raise AssertionError(("nondivisor", count))
        if schedule.binary_multiplication_nodes > 2 * schedule.bit_length - 2:
            raise AssertionError(("binary node bound", count))

        minus_hits = {
            divisor + 1
            for divisor in divisors
            if divisor + 1 >= 3 and is_prime_exact(divisor + 1)
        }
        plus_hits = {
            divisor - 1
            for divisor in divisors
            if divisor - 1 >= 3 and is_prime_exact(divisor - 1)
        }
        both_hits = minus_hits & plus_hits
        if both_hits:
            raise AssertionError(("primorial channel collision", count, both_hits))
        hits = minus_hits | plus_hits
        if len(hits) > 2 * schedule.divisor_count:
            raise AssertionError(("divisor hit bound", count))
        for prime in hits:
            signature = (
                schedule.exponent % (prime - 1) == 0,
                schedule.exponent % (prime + 1) == 0,
            )
            if signature not in ((True, False), (False, True)):
                raise AssertionError(("direct signature", count, prime, signature))

        if count >= 6:
            largest_prime = schedule.primes[-1]
            explicit_upper = count * (
                math.log(count) + math.log(math.log(count))
            )
            rosser_schoenfeld_checks += 1
            if not largest_prime < explicit_upper:
                raise AssertionError(("Rosser-Schoenfeld (3.13)", count))

        hit_count = len(hits)
        total_hit_pairs = math.comb(hit_count, 2)
        promised_hit_pairs = len(minus_hits) * len(plus_hits)
        fraction = (
            Fraction(promised_hit_pairs, total_hit_pairs)
            if total_hit_pairs
            else Fraction(0, 1)
        )
        primorial_records.append(
            {
                "prime_count": count,
                "largest_prime": schedule.primes[-1],
                "exponent": schedule.exponent,
                "bit_length": schedule.bit_length,
                "divisor_count": schedule.divisor_count,
                "binary_multiplication_nodes": schedule.binary_multiplication_nodes,
                "minus_hit_count": len(minus_hits),
                "plus_hit_count": len(plus_hits),
                "both_hit_count": len(both_hits),
                "hit_count": hit_count,
                "promised_pairs_within_hits": promised_hit_pairs,
                "total_pairs_within_hits": total_hit_pairs,
                "promised_fraction_within_hits": (
                    f"{fraction.numerator}/{fraction.denominator}"
                ),
            }
        )

    summary: dict[str, Any] = {
        "bounds": {
            "explicit_exponents": [1, exponent_max - 1],
            "primorial_prime_counts": [1, primorial_count_max],
            "diagnostic_bit_lengths": list(diagnostic_lengths),
        },
        "seed": None,
        "divisor_budget_checks": divisor_budget_checks,
        "maximum_divisor_records": [
            {
                "bit_length": length,
                "divisor_count": maximum_divisor_records[length][0],
                "exponent": maximum_divisor_records[length][1],
            }
            for length in sorted(maximum_divisor_records)
        ],
        "boundary_diagnostics": boundary_diagnostics,
        "primorial_records": primorial_records,
        "rosser_schoenfeld_checks": rosser_schoenfeld_checks,
        "primality_candidates": len(primality_cache),
        "primality_trial_divisions": primality_divisions,
        "checked": {
            "exact_boundary_divisor_budget": True,
            "primorial_divisor_enumeration": True,
            "binary_straight_line_node_accounting": True,
            "direct_combined_signatures": True,
            "squarefree_even_channel_disjointness": True,
            "rosser_schoenfeld_explicit_upper_bound": True,
        },
    }
    summary["summary_sha256"] = hashlib.sha256(canonical_json(summary)).hexdigest()
    return summary


def main() -> int:
    """Command-line entry point."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--exponent-max", type=int, default=1 << 18)
    parser.add_argument("--primorial-count-max", type=int, default=12)
    args = parser.parse_args()
    print(
        json.dumps(
            search(args.exponent_max, args.primorial_count_max),
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
