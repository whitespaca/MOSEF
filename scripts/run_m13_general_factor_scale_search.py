"""Audit the M13 arbitrary-exponent factor-scale divisor bound."""

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

from mosef_reference import (  # noqa: E402
    factor_scale_divisor_bound,
    factor_scale_threshold,
    positive_divisors,
)


def canonical_json(value: Any) -> bytes:
    """Serialize a value deterministically for hashing."""
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def prime_set(limit: int) -> set[int]:
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
    return {value for value, flag in enumerate(sieve) if flag}


def family_record(name: str, exponent: int, target_max: int) -> dict[str, int | str]:
    """Return one exact adversarial-family record."""
    threshold = factor_scale_threshold(2 * target_max.bit_length())
    bound = factor_scale_divisor_bound(exponent, target_max, threshold)
    divisors = positive_divisors(exponent)
    relevant = sum(divisor <= target_max + 1 for divisor in divisors)
    if relevant > bound.divisor_candidate_bound:
        raise AssertionError(f"family bound failed: {name}")
    return {
        "name": name,
        "exponent": exponent,
        "exponent_bits": exponent.bit_length(),
        "target_max": target_max,
        "threshold": threshold,
        "relevant_divisors": relevant,
        "divisor_bound": bound.divisor_candidate_bound,
    }


def search(exponent_max: int, target_bit_max: int) -> dict[str, Any]:
    """Run the registered deterministic finite audit."""
    if not 2 <= exponent_max <= 1 << 18:
        raise ValueError("exponent_max must lie in [2, 2^18]")
    if not 4 <= target_bit_max <= 18:
        raise ValueError("target_bit_max must lie in [4, 18]")

    primes = prime_set(1 << target_bit_max)
    bound_checks = 0
    divisor_membership_checks = 0
    prime_candidate_checks = 0
    closest_slack: tuple[int, int, int, int, int] | None = None
    thresholds = (2, 3, 5, 11)
    target_maxima = tuple((1 << bits) - 1 for bits in range(4, target_bit_max + 1, 2))

    for exponent in range(2, exponent_max):
        divisors = positive_divisors(exponent)
        for target_max in target_maxima:
            relevant_divisors = [
                divisor for divisor in divisors if divisor <= target_max + 1
            ]
            divisor_membership_checks += len(divisors)
            for threshold in thresholds:
                bound = factor_scale_divisor_bound(
                    exponent, target_max, threshold
                )
                bound_checks += 1
                if len(relevant_divisors) > bound.divisor_candidate_bound:
                    raise AssertionError("factor-scale divisor bound failed")
                slack = bound.divisor_candidate_bound - len(relevant_divisors)
                record = (
                    slack,
                    exponent,
                    target_max,
                    threshold,
                    bound.divisor_candidate_bound,
                )
                if closest_slack is None or record < closest_slack:
                    closest_slack = record
            hits = {
                candidate
                for divisor in relevant_divisors
                for candidate in (divisor - 1, divisor + 1)
                if 3 <= candidate <= target_max
                and candidate % 2 == 1
                and candidate in primes
            }
            prime_candidate_checks += 2 * len(relevant_divisors)
            weakest = min(
                factor_scale_divisor_bound(exponent, target_max, threshold)
                .prime_candidate_bound
                for threshold in thresholds
            )
            if len(hits) > weakest:
                raise AssertionError("prime-candidate bound failed")

    assert closest_slack is not None
    families = [
        family_record("prime_power", 2**48, (1 << target_bit_max) - 1),
        family_record(
            "squareful",
            2**12 * 3**8 * 5**5 * 7**3,
            (1 << target_bit_max) - 1,
        ),
        family_record(
            "noninitial_squarefree",
            17 * 19 * 23 * 29 * 31 * 37,
            (1 << target_bit_max) - 1,
        ),
        family_record(
            "mixed_noninitial_squareful",
            2**4 * 11**5 * 17**3 * 43**2,
            (1 << target_bit_max) - 1,
        ),
    ]
    result: dict[str, Any] = {
        "schema_version": "1.0.0",
        "parameters": {
            "exponent_max": exponent_max,
            "target_bit_max": target_bit_max,
            "thresholds": list(thresholds),
        },
        "counts": {
            "bound_checks": bound_checks,
            "divisor_membership_checks": divisor_membership_checks,
            "prime_candidate_checks": prime_candidate_checks,
        },
        "closest_slack": {
            "slack": closest_slack[0],
            "exponent": closest_slack[1],
            "target_max": closest_slack[2],
            "threshold": closest_slack[3],
            "bound": closest_slack[4],
        },
        "adversarial_families": families,
    }
    result["summary_sha256"] = hashlib.sha256(canonical_json(result)).hexdigest()
    return result


def main() -> int:
    """Parse arguments, run the audit, and print deterministic JSON."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--exponent-max", type=int, default=65536)
    parser.add_argument("--target-bit-max", type=int, default=14)
    args = parser.parse_args()
    print(json.dumps(search(args.exponent_max, args.target_bit_max), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
