"""Exhaustively falsify the M9 exponent-encoding divisor-budget barrier."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

from mosef_reference import bit_length_divisor_budget


def canonical_json(value: Any) -> bytes:
    """Serialize a value deterministically for hashing."""
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def smallest_prime_factors(limit: int) -> tuple[list[int], tuple[int, ...]]:
    """Return an SPF table and every prime through ``limit``."""
    spf = list(range(limit + 1))
    if limit >= 1:
        spf[1] = 1
    for candidate in range(2, int(limit**0.5) + 1):
        if spf[candidate] != candidate:
            continue
        for multiple in range(candidate * candidate, limit + 1, candidate):
            if spf[multiple] == multiple:
                spf[multiple] = candidate
    primes = tuple(value for value in range(2, limit + 1) if spf[value] == value)
    return spf, primes


def factorization(value: int, spf: list[int]) -> tuple[tuple[int, int], ...]:
    """Factor ``value`` exactly with a precomputed SPF table."""
    factors: list[tuple[int, int]] = []
    remaining = value
    while remaining > 1:
        prime = spf[remaining]
        exponent = 0
        while remaining % prime == 0:
            remaining //= prime
            exponent += 1
        factors.append((prime, exponent))
    return tuple(factors)


def divisors_from_factors(
    factors: tuple[tuple[int, int], ...],
) -> tuple[int, ...]:
    """Enumerate every positive divisor from an exact factorization."""
    divisors = [1]
    for prime, exponent in factors:
        previous = tuple(divisors)
        power = 1
        for _ in range(exponent):
            power *= prime
            divisors.extend(divisor * power for divisor in previous)
    return tuple(divisors)


def divisor_count_from_factors(factors: tuple[tuple[int, int], ...]) -> int:
    """Return the divisor count from prime multiplicities."""
    result = 1
    for _, exponent in factors:
        result *= exponent + 1
    return result


def hit_set_from_divisors(
    divisors: tuple[int, ...],
    is_prime: list[bool],
) -> frozenset[int]:
    """Construct the exact global odd-prime hit set from divisors."""
    hits: set[int] = set()
    for divisor in divisors:
        for candidate in (divisor - 1, divisor + 1):
            if (
                candidate >= 3
                and candidate % 2 == 1
                and candidate < len(is_prime)
                and is_prime[candidate]
            ):
                hits.add(candidate)
    return frozenset(hits)


def search(
    bit_length_max: int,
    direct_exponent_max: int,
    prime_max: int,
) -> dict[str, Any]:
    """Run the deterministic M9 search and return its exact summary."""
    if bit_length_max < 3:
        raise ValueError("bit_length_max must be at least 3")
    exponent_max = (1 << bit_length_max) - 1
    if direct_exponent_max < 7 or direct_exponent_max > exponent_max:
        raise ValueError("direct_exponent_max must lie in [7, exponent_max]")
    if prime_max < 5 or prime_max > exponent_max + 1:
        raise ValueError("prime_max must lie in [5, exponent_max + 1]")

    spf, all_primes = smallest_prime_factors(exponent_max + 1)
    is_prime = [False] * (exponent_max + 2)
    for prime in all_primes:
        is_prime[prime] = True
    direct_primes = tuple(
        prime for prime in all_primes if 3 <= prime <= prime_max and prime % 2
    )
    budgets = {
        length: bit_length_divisor_budget(length)
        for length in range(1, bit_length_max + 1)
    }

    exact_budget_checks = 0
    single_hit_bound_checks = 0
    direct_oracle_checks = 0
    per_length_records: dict[int, tuple[int, int]] = {}
    hit_sets: dict[int, frozenset[int]] = {}
    divisor_counts: dict[int, int] = {}
    largest_hit: tuple[int, int] | None = None

    for exponent in range(1, exponent_max + 1):
        factors = factorization(exponent, spf)
        count = divisor_count_from_factors(factors)
        divisors = divisors_from_factors(factors)
        if len(divisors) != count or len(set(divisors)) != count:
            raise AssertionError(("divisor enumeration", exponent, factors))

        length = exponent.bit_length()
        budget = budgets[length]
        exact_budget_checks += 1
        if count > budget.one_length_bound:
            raise AssertionError(("one-length budget", exponent, count, budget))
        if budget.one_length_bound > budget.monotone_bound:
            raise AssertionError(("monotone envelope", exponent, budget))

        hits = hit_set_from_divisors(divisors, is_prime)
        single_hit_bound_checks += 1
        if len(hits) > 2 * count:
            raise AssertionError(("single hit bound", exponent, count, hits))

        current_record = per_length_records.get(length)
        if current_record is None or count > current_record[0]:
            per_length_records[length] = (count, exponent)
        hit_record = (len(hits), exponent)
        if largest_hit is None or hit_record[0] > largest_hit[0]:
            largest_hit = hit_record

        if exponent <= direct_exponent_max:
            hit_sets[exponent] = hits
            divisor_counts[exponent] = count
            for prime in direct_primes:
                direct_oracle_checks += 1
                direct = (
                    exponent % (prime - 1) == 0
                    or exponent % (prime + 1) == 0
                )
                if direct != (prime in hits):
                    raise AssertionError(("direct hit oracle", exponent, prime))

    record_exponents = tuple(
        per_length_records[length][1] for length in sorted(per_length_records)
    )
    record_hit_sets = {
        exponent: hit_set_from_divisors(
            divisors_from_factors(factorization(exponent, spf)),
            is_prime,
        )
        for exponent in record_exponents
    }
    record_divisor_counts = {
        exponent: divisor_count_from_factors(factorization(exponent, spf))
        for exponent in record_exponents
    }
    family_hit_bound_checks = 0
    for size in range(1, min(3, len(record_exponents)) + 1):
        for family in itertools.combinations(record_exponents, size):
            family_hit_bound_checks += 1
            hits = frozenset().union(*(record_hit_sets[value] for value in family))
            divisor_sum = sum(record_divisor_counts[value] for value in family)
            maximum_length = max(value.bit_length() for value in family)
            if len(hits) > 2 * divisor_sum:
                raise AssertionError(("family divisor bound", family, hits))
            if len(hits) > 2 * len(family) * budgets[maximum_length].monotone_bound:
                raise AssertionError(("family encoding bound", family, hits))

    smallest_large_value_zero_pair: dict[str, int] | None = None
    for exponent in range(1, direct_exponent_max + 1):
        eligible = tuple(
            prime
            for prime in direct_primes
            if prime + 1 < exponent
        )
        zero_primes = tuple(
            prime for prime in eligible if prime not in hit_sets[exponent]
        )
        if len(zero_primes) >= 2:
            left, right = zero_primes[:2]
            smallest_large_value_zero_pair = {
                "exponent": exponent,
                "p": left,
                "q": right,
                "n": left * right,
            }
            break
    if smallest_large_value_zero_pair != {
        "exponent": 7,
        "p": 3,
        "q": 5,
        "n": 15,
    }:
        raise AssertionError(
            ("REF-005 minimization", smallest_large_value_zero_pair)
        )
    if largest_hit is None:
        raise AssertionError("registered range must contain one exponent")

    maximum_divisor_records = [
        {
            "bit_length": length,
            "exponent": per_length_records[length][1],
            "divisor_count": per_length_records[length][0],
            "one_length_bound": budgets[length].one_length_bound,
            "monotone_bound": budgets[length].monotone_bound,
        }
        for length in sorted(per_length_records)
    ]
    summary: dict[str, Any] = {
        "bounds": {
            "bit_length": [1, bit_length_max],
            "exponent": [1, exponent_max],
            "direct_exponent": [1, direct_exponent_max],
            "direct_odd_prime": [3, prime_max],
            "record_family_size": [1, 3],
        },
        "seed": None,
        "odd_prime_count": len(direct_primes),
        "exact_budget_checks": exact_budget_checks,
        "single_hit_bound_checks": single_hit_bound_checks,
        "direct_oracle_checks": direct_oracle_checks,
        "family_hit_bound_checks": family_hit_bound_checks,
        "smallest_large_value_zero_pair": smallest_large_value_zero_pair,
        "largest_single_hit_set": {
            "count": largest_hit[0],
            "exponent": largest_hit[1],
        },
        "maximum_divisor_records": maximum_divisor_records,
        "checked": {
            "exact_divisor_enumeration": True,
            "one_length_divisor_budget": True,
            "monotone_envelope": True,
            "single_exponent_hit_bound": True,
            "record_family_hit_bound": True,
            "direct_hit_oracle": True,
            "refuted_claim_minimality": True,
        },
    }
    summary["summary_sha256"] = hashlib.sha256(canonical_json(summary)).hexdigest()
    return summary


def main() -> int:
    """Command-line entry point."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bit-length-max", type=int, default=18)
    parser.add_argument("--direct-exponent-max", type=int, default=4096)
    parser.add_argument("--prime-max", type=int, default=4093)
    args = parser.parse_args()
    print(
        json.dumps(
            search(
                args.bit_length_max,
                args.direct_exponent_max,
                args.prime_max,
            ),
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
