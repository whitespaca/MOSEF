"""Deterministic M22 audit of the symmetric quotient-difference reduction."""

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
    evaluate_symmetric_quotient_difference,
    symmetric_cofactor_terms,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--exponent-max", type=int, default=24)
    parser.add_argument("--modulus-max", type=int, default=128)
    parser.add_argument("--base-max", type=int, default=16)
    return parser.parse_args()


def prime_powers(value: int) -> tuple[tuple[int, int], ...]:
    factors: list[tuple[int, int]] = []
    remaining = value
    prime = 2
    while prime <= remaining // prime:
        exponent = 0
        while remaining % prime == 0:
            remaining //= prime
            exponent += 1
        if exponent:
            factors.append((prime, exponent))
        prime += 1 if prime == 2 else 2
    if remaining > 1:
        factors.append((remaining, 1))
    return tuple(factors)


def capped_valuation(residue: int, prime: int, exponent: int) -> int:
    if residue == 0:
        return exponent
    valuation = 0
    remaining = residue
    while valuation < exponent and remaining % prime == 0:
        remaining //= prime
        valuation += 1
    return valuation


def is_proper(value: int, modulus: int) -> bool:
    return 1 < value < modulus


def formal_difference(exponent: int) -> dict[int, int]:
    result: dict[int, int] = {}
    for index in range(exponent):
        result[exponent * index] = result.get(exponent * index, 0) + 1
        result[index] = result.get(index, 0) - 1
    return {degree: coefficient for degree, coefficient in result.items() if coefficient}


def formal_factored(exponent: int) -> dict[int, int]:
    result: dict[int, int] = {}
    for degree in symmetric_cofactor_terms(exponent):
        result[degree + exponent] = result.get(degree + exponent, 0) + 1
        result[degree + 1] = result.get(degree + 1, 0) - 1
    return {degree: coefficient for degree, coefficient in result.items() if coefficient}


def main() -> int:
    args = parse_args()
    if args.exponent_max < 2 or args.modulus_max < 4 or args.base_max < 0:
        raise SystemExit("invalid search bounds")

    symbolic = {
        "exponents": 0,
        "cofactor_monomials": 0,
        "difference_nonzero_terms": 0,
        "identity_failures": 0,
    }
    for exponent in range(2, args.exponent_max + 1):
        left = formal_difference(exponent)
        right = formal_factored(exponent)
        symbolic["exponents"] += 1
        symbolic["cofactor_monomials"] += len(
            symmetric_cofactor_terms(exponent)
        )
        symbolic["difference_nonzero_terms"] += len(left)
        if left != right:
            symbolic["identity_failures"] += 1

    modular = {
        "unit_bases": 0,
        "nonunit_bases": 0,
        "evaluations": 0,
        "prime_power_components": 0,
        "valuation_checks": 0,
        "expanded_cofactor_checks": 0,
        "unit_endpoints": 0,
        "proper_endpoints": 0,
        "full_endpoints": 0,
        "proper_differences": 0,
        "proper_via_endpoint": 0,
        "proper_via_unit_endpoint_cofactor": 0,
        "full_differences": 0,
        "unit_stage_new_proper_differences": 0,
        "unit_stage_endpoint_paths": 0,
        "unit_stage_cofactor_paths": 0,
        "unexplained_failures": 0,
    }
    first_cofactor_path: dict[str, Any] | None = None

    for modulus in range(4, args.modulus_max + 1):
        components = prime_powers(modulus)
        for base in range(min(modulus - 1, args.base_max) + 1):
            if math.gcd(base, modulus) != 1:
                modular["nonunit_bases"] += 1
                continue
            modular["unit_bases"] += 1
            for exponent in range(2, args.exponent_max + 1):
                value = evaluate_symmetric_quotient_difference(
                    base,
                    modulus,
                    exponent,
                )
                modular["evaluations"] += 1
                modular["prime_power_components"] += len(components)
                direct_cofactor = sum(
                    pow(base, degree, modulus)
                    for degree in symmetric_cofactor_terms(exponent)
                ) % modulus
                modular["expanded_cofactor_checks"] += 1
                if direct_cofactor != value.cofactor_residue:
                    modular["unexplained_failures"] += 1

                for prime, prime_exponent in components:
                    endpoint_valuation = capped_valuation(
                        value.endpoint_residue,
                        prime,
                        prime_exponent,
                    )
                    cofactor_valuation = capped_valuation(
                        value.cofactor_residue,
                        prime,
                        prime_exponent,
                    )
                    difference_valuation = capped_valuation(
                        value.difference_residue,
                        prime,
                        prime_exponent,
                    )
                    modular["valuation_checks"] += 1
                    if difference_valuation != min(
                        prime_exponent,
                        endpoint_valuation + cofactor_valuation,
                    ):
                        modular["unexplained_failures"] += 1

                if value.endpoint_status == "unit":
                    modular["unit_endpoints"] += 1
                    if value.difference_gcd != value.cofactor_gcd:
                        modular["unexplained_failures"] += 1
                elif value.endpoint_status == "proper_factor":
                    modular["proper_endpoints"] += 1
                else:
                    modular["full_endpoints"] += 1
                    if value.difference_gcd != modulus:
                        modular["unexplained_failures"] += 1

                if value.difference_gcd == modulus:
                    modular["full_differences"] += 1
                if not is_proper(value.difference_gcd, modulus):
                    continue
                modular["proper_differences"] += 1
                if is_proper(value.endpoint_gcd, modulus):
                    modular["proper_via_endpoint"] += 1
                elif value.endpoint_gcd == 1 and is_proper(
                    value.cofactor_gcd,
                    modulus,
                ):
                    modular["proper_via_unit_endpoint_cofactor"] += 1
                else:
                    modular["unexplained_failures"] += 1

                first_gcd = math.gcd(value.first_quotient_residue, modulus)
                second_gcd = math.gcd(value.second_quotient_residue, modulus)
                if first_gcd == second_gcd == 1:
                    modular["unit_stage_new_proper_differences"] += 1
                    if is_proper(value.endpoint_gcd, modulus):
                        modular["unit_stage_endpoint_paths"] += 1
                    elif value.endpoint_gcd == 1 and is_proper(
                        value.cofactor_gcd,
                        modulus,
                    ):
                        modular["unit_stage_cofactor_paths"] += 1
                        if first_cofactor_path is None:
                            first_cofactor_path = {
                                "modulus": modulus,
                                "base": base,
                                "exponent": exponent,
                                "first_quotient": value.first_quotient_residue,
                                "second_quotient": value.second_quotient_residue,
                                "difference": value.difference_residue,
                                "difference_gcd": value.difference_gcd,
                                "endpoint": value.endpoint_residue,
                                "cofactor": value.cofactor_residue,
                            }
                    else:
                        modular["unexplained_failures"] += 1

    if symbolic["identity_failures"] or modular["unexplained_failures"]:
        raise AssertionError("M22 registered identity or reduction failed")
    witness = evaluate_symmetric_quotient_difference(2, 9, 5)
    if witness.endpoint_gcd != 3 or witness.difference_gcd != 3:
        raise AssertionError("M21 witness did not reduce through the endpoint")

    summary = {
        "schema_version": "1.0.0",
        "parameters": vars(args),
        "symbolic": symbolic,
        "modular": modular,
        "first_unit_stage_cofactor_path": first_cofactor_path,
        "named_m21_endpoint_reduction": {
            "modulus": 9,
            "base": 2,
            "exponent": 5,
            "difference": 3,
            "endpoint": 6,
            "endpoint_gcd": 3,
        },
    }
    canonical = json.dumps(summary, sort_keys=True, separators=(",", ":"))
    summary["summary_sha256"] = hashlib.sha256(canonical.encode()).hexdigest()
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
