"""Falsify M5 conjugate-channel independence on a registered finite box."""

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
    LucasCandidateKind,
    analyze_conjugate_pair,
    candidate_succeeds,
    evaluate_lucas_candidate,
    evaluate_separator_candidate,
)


def canonical_json(value: Any) -> bytes:
    """Serialize a value deterministically for hashing."""
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def prime_divisors(value: int) -> tuple[int, ...]:
    """Return the distinct prime divisors of ``value``."""
    remaining = value
    factors: list[int] = []
    divisor = 2
    while divisor <= remaining // divisor:
        if remaining % divisor == 0:
            factors.append(divisor)
            while remaining % divisor == 0:
                remaining //= divisor
        divisor += 1
    if remaining > 1:
        factors.append(remaining)
    return tuple(factors)


def is_composite(value: int) -> bool:
    """Return whether ``value`` is composite."""
    return value >= 4 and bool(prime_divisors(value)) and prime_divisors(value) != (value,)


def is_squarefree(value: int) -> bool:
    """Return whether no prime square divides ``value``."""
    return all(value % (prime * prime) for prime in prime_divisors(value))


def is_carmichael(value: int) -> bool:
    """Apply Korselt's criterion exactly."""
    factors = prime_divisors(value)
    return (
        is_composite(value)
        and len(factors) >= 3
        and is_squarefree(value)
        and all((value - 1) % (prime - 1) == 0 for prime in factors)
    )


def first_independent_lucas_complement(
    modulus_max: int,
    base_max: int,
    parameter_max: int,
    exponent_max: int,
) -> tuple[dict[str, Any] | None, int]:
    """Find and count same-exponent Lucas factors missed by multiplication."""
    first: dict[str, Any] | None = None
    count = 0
    for n in range(9, modulus_max + 1, 2):
        if not is_composite(n):
            continue
        for base in range(2, min(n, base_max + 1)):
            if math.gcd(base, n) != 1:
                continue
            for exponent in range(1, exponent_max + 1):
                multiplicative = evaluate_separator_candidate(n, base, exponent)
                if candidate_succeeds(multiplicative):
                    continue
                for parameter in range(min(n, parameter_max + 1)):
                    lucas = evaluate_lucas_candidate(n, parameter, exponent)
                    if lucas.kind is not LucasCandidateKind.FACTOR:
                        continue
                    count += 1
                    if first is None:
                        first = {
                            "n": n,
                            "base": base,
                            "parameter": parameter,
                            "exponent": exponent,
                            "multiplicative_kind": multiplicative.kind.value,
                            "lucas_kind": lucas.kind.value,
                            "factor": lucas.factor,
                            "discriminant_gcd": lucas.discriminant_gcd,
                        }
    return first, count


def search(
    modulus_max: int,
    base_max: int,
    parameter_max: int,
    exponent_max: int,
) -> dict[str, Any]:
    """Run the deterministic M5 search and return its exact summary."""
    if modulus_max < 4:
        raise ValueError("modulus_max must be at least 4")
    if min(base_max, parameter_max) < 1:
        raise ValueError("base_max and parameter_max must be positive")
    if exponent_max < 2:
        raise ValueError("exponent_max must include exponent 2")

    identity_checks = 0
    squarefree_gcd_checks = 0
    conjugate_families = 0
    multiplicative_success_families = 0
    lucas_success_families = 0
    combined_success_families = 0
    derived_lucas_only_families = 0
    both_failed_families = 0
    carmichael_families = 0
    carmichael_both_failed_families = 0
    first_discriminant_degenerate_factor: dict[str, int] | None = None
    first_prime_power_degradation: dict[str, Any] | None = None

    for n in range(4, modulus_max + 1):
        if not is_composite(n):
            continue
        carmichael = is_carmichael(n)
        squarefree = is_squarefree(n)
        for base in range(1, min(n, base_max + 1)):
            if math.gcd(base, n) != 1:
                continue
            conjugate_families += 1
            if carmichael:
                carmichael_families += 1
            multiplicative_success = False
            lucas_success = False
            for exponent in range(1, exponent_max + 1):
                analysis = analyze_conjugate_pair(n, base, exponent)
                if not analysis.discriminant_identity or not analysis.lucas_identity:
                    raise AssertionError(("conjugate identity", n, base, exponent))
                identity_checks += 1
                if squarefree:
                    if analysis.multiplicative_gcd != analysis.lucas_gcd:
                        raise AssertionError(("squarefree gcd", n, base, exponent))
                    squarefree_gcd_checks += 1
                multiplicative_success |= candidate_succeeds(analysis.multiplicative)
                lucas_success |= candidate_succeeds(analysis.lucas)
                if (
                    first_discriminant_degenerate_factor is None
                    and analysis.lucas.kind
                    is LucasCandidateKind.DEGENERATE_FACTOR
                ):
                    first_discriminant_degenerate_factor = {
                        "n": n,
                        "base": base,
                        "parameter": analysis.parameter,
                        "exponent": exponent,
                        "factor": analysis.lucas.factor,
                    }
                if (
                    first_prime_power_degradation is None
                    and candidate_succeeds(analysis.multiplicative)
                    and analysis.lucas.kind
                    is LucasCandidateKind.SIMULTANEOUS_COLLISION
                    and analysis.discriminant_gcd == 1
                ):
                    first_prime_power_degradation = {
                        "n": n,
                        "base": base,
                        "parameter": analysis.parameter,
                        "exponent": exponent,
                        "multiplicative_gcd": analysis.multiplicative_gcd,
                        "lucas_gcd": analysis.lucas_gcd,
                    }
            multiplicative_success_families += int(multiplicative_success)
            lucas_success_families += int(lucas_success)
            combined_success_families += int(
                multiplicative_success or lucas_success
            )
            derived_lucas_only_families += int(
                lucas_success and not multiplicative_success
            )
            both_failed_families += int(
                not multiplicative_success and not lucas_success
            )
            if carmichael and not multiplicative_success and not lucas_success:
                carmichael_both_failed_families += 1

    if derived_lucas_only_families:
        raise AssertionError("a conjugately derived Lucas family added success")
    if combined_success_families != multiplicative_success_families:
        raise AssertionError("combined and multiplicative success domains differ")

    independent_first, independent_count = first_independent_lucas_complement(
        modulus_max,
        base_max,
        parameter_max,
        exponent_max,
    )
    summary: dict[str, Any] = {
        "bounds": {
            "modulus": [4, modulus_max],
            "base": [1, base_max],
            "parameter": [0, parameter_max],
            "exponent": [1, exponent_max],
        },
        "seed": None,
        "identity_checks": identity_checks,
        "squarefree_gcd_checks": squarefree_gcd_checks,
        "conjugate_family_count": conjugate_families,
        "multiplicative_success_family_count": multiplicative_success_families,
        "derived_lucas_success_family_count": lucas_success_families,
        "combined_success_family_count": combined_success_families,
        "derived_lucas_only_success_family_count": derived_lucas_only_families,
        "both_failed_family_count": both_failed_families,
        "carmichael_family_count": carmichael_families,
        "carmichael_both_failed_family_count": carmichael_both_failed_families,
        "first_discriminant_degenerate_factor": (
            first_discriminant_degenerate_factor
        ),
        "first_prime_power_degradation": first_prime_power_degradation,
        "first_independent_lucas_complement": independent_first,
        "independent_lucas_complement_count": independent_count,
        "checked": {
            "conjugate_identities": True,
            "squarefree_raw_gcd_equality": True,
            "family_success_domain_equality_when_exponent_two_is_present": True,
            "independent_parameter_complement_search": True,
        },
    }
    summary["summary_sha256"] = hashlib.sha256(canonical_json(summary)).hexdigest()
    return summary


def main() -> int:
    """Command-line entry point."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--modulus-max", type=int, default=700)
    parser.add_argument("--base-max", type=int, default=32)
    parser.add_argument("--parameter-max", type=int, default=32)
    parser.add_argument("--exponent-max", type=int, default=12)
    args = parser.parse_args()
    print(
        json.dumps(
            search(
                args.modulus_max,
                args.base_max,
                args.parameter_max,
                args.exponent_max,
            ),
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
