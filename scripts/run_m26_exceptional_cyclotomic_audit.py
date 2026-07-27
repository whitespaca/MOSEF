"""Deterministic M26 audit of exceptional cyclotomic cofactors."""

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
    evaluate_exceptional_cyclotomic,
    exceptional_cofactor_coefficients,
    exceptional_cyclotomic_coefficients,
    polynomial_multiply,
    signed_numerator_coefficients,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--factor-max", type=int, default=19)
    parser.add_argument("--modulus-max", type=int, default=160)
    parser.add_argument("--base-max", type=int, default=40)
    return parser.parse_args()


def factorization(value: int) -> dict[int, int]:
    result: dict[int, int] = {}
    divisor = 2
    while divisor * divisor <= value:
        while value % divisor == 0:
            result[divisor] = result.get(divisor, 0) + 1
            value //= divisor
        divisor += 1
    if value > 1:
        result[value] = result.get(value, 0) + 1
    return result


def is_composite(value: int) -> bool:
    factors = factorization(value)
    return len(factors) > 1 or next(iter(factors.values()), 0) > 1


def evaluate_coefficients(
    coefficients: tuple[int, ...], base: int, modulus: int
) -> int:
    result = 0
    for coefficient in reversed(coefficients):
        result = (result * base + coefficient) % modulus
    return result


def capped_valuation(residue: int, prime: int, exponent: int) -> int:
    if residue == 0:
        return exponent
    result = 0
    while result < exponent and residue % prime == 0:
        residue //= prime
        result += 1
    return result


def family_pairs(factor_max: int) -> list[tuple[int, int, str, int]]:
    result: list[tuple[int, int, str, int]] = []
    for first_factor in range(2, factor_max + 1):
        for second_factor in range(2, factor_max + 1):
            if first_factor == second_factor:
                continue
            degree = first_factor * (second_factor - 1)
            if first_factor % 4 == 3 and second_factor % 4 == 3:
                result.append((degree, first_factor, second_factor, "phi4"))
            if first_factor % 6 == 5 and second_factor % 6 == 3:
                result.append((degree, first_factor, second_factor, "phi6"))
    return sorted(result)


def witness(
    base: int,
    modulus: int,
    first_factor: int,
    second_factor: int,
    family: str,
    expected_source: str,
    expected_gcd: int | None,
) -> dict[str, Any]:
    value = evaluate_exceptional_cyclotomic(
        base,
        modulus,
        first_factor,
        second_factor,
        family,
    )
    if (
        value.extraction_source != expected_source
        or value.extraction_gcd != expected_gcd
    ):
        raise AssertionError("registered extraction witness failed")
    return {
        "base": base,
        "modulus": modulus,
        "first_factor": first_factor,
        "second_factor": second_factor,
        "family": family,
        "cyclotomic_gcd": value.cyclotomic_gcd,
        "aggregate_gcd": value.aggregate_gcd,
        "extraction_source": value.extraction_source,
        "extraction_gcd": value.extraction_gcd,
    }


def main() -> int:
    args = parse_args()
    if args.factor_max < 11 or args.modulus_max < 55 or args.base_max < 12:
        raise SystemExit("bounds do not cover the registered witnesses")
    counts = {
        "exceptional_factor_pairs": 0,
        "phi4_factor_pairs": 0,
        "phi6_factor_pairs": 0,
        "exact_symbolic_divisions": 0,
        "modular_evaluations": 0,
        "compact_dense_cofactor_checks": 0,
        "dense_modular_product_checks": 0,
        "prime_power_valuation_checks": 0,
        "cyclotomic_unit_branches": 0,
        "cyclotomic_proper_factor_branches": 0,
        "cyclotomic_full_collision_branches": 0,
        "unit_cyclotomic_residual_proper_factors": 0,
        "clean_residual_proper_factors": 0,
        "failures": 0,
    }
    pairs = family_pairs(args.factor_max)
    cofactors: dict[tuple[int, int, str], tuple[int, ...]] = {}
    for _, first_factor, second_factor, family in pairs:
        counts["exceptional_factor_pairs"] += 1
        counts[f"{family}_factor_pairs"] += 1
        cyclotomic = exceptional_cyclotomic_coefficients(
            first_factor, second_factor, family
        )
        cofactor = exceptional_cofactor_coefficients(
            first_factor, second_factor, family
        )
        first_coefficient = 1 if family == "phi4" else 2
        numerator = signed_numerator_coefficients(
            first_factor,
            second_factor,
            first_coefficient,
            1,
        )
        counts["exact_symbolic_divisions"] += 1
        if polynomial_multiply(cyclotomic, cofactor) != numerator:
            counts["failures"] += 1
        cofactors[(first_factor, second_factor, family)] = cofactor

    minima: dict[str, tuple[tuple[int, ...], dict[str, int | str]]] = {}
    for modulus in range(4, args.modulus_max + 1):
        if not is_composite(modulus):
            continue
        prime_powers = factorization(modulus)
        square_free = (
            len(prime_powers) >= 2
            and all(exponent == 1 for exponent in prime_powers.values())
        )
        repeated_prime = any(
            exponent > 1 for exponent in prime_powers.values()
        )
        for _, first_factor, second_factor, family in pairs:
            cofactor = cofactors[(first_factor, second_factor, family)]
            for base in range(2, min(args.base_max, modulus - 1) + 1):
                if math.gcd(base, modulus) != 1:
                    continue
                value = evaluate_exceptional_cyclotomic(
                    base,
                    modulus,
                    first_factor,
                    second_factor,
                    family,
                )
                counts["modular_evaluations"] += 1
                counts[
                    f"cyclotomic_{value.cyclotomic_status}_branches"
                ] += 1
                cofactor_residue = evaluate_coefficients(
                    cofactor, base, modulus
                )
                if cofactor_residue != value.cofactor_residue:
                    counts["failures"] += 1
                counts["compact_dense_cofactor_checks"] += 1
                if (
                    value.cyclotomic_residue * cofactor_residue % modulus
                    != value.aggregate_residue
                ):
                    counts["failures"] += 1
                counts["dense_modular_product_checks"] += 1
                for prime, exponent in prime_powers.items():
                    aggregate_valuation = capped_valuation(
                        value.aggregate_residue,
                        prime,
                        exponent,
                    )
                    cyclotomic_valuation = capped_valuation(
                        value.cyclotomic_residue,
                        prime,
                        exponent,
                    )
                    cofactor_valuation = capped_valuation(
                        cofactor_residue,
                        prime,
                        exponent,
                    )
                    if aggregate_valuation != min(
                        cyclotomic_valuation + cofactor_valuation,
                        exponent,
                    ):
                        counts["failures"] += 1
                    counts["prime_power_valuation_checks"] += 1
                clean = (
                    value.cyclotomic_status == "unit"
                    and value.aggregate_status == "proper_factor"
                    and value.first_quotient_gcd == 1
                    and value.second_quotient_gcd == 1
                    and value.first_public_bound_gcd == 1
                    and value.second_public_bound_gcd == 1
                )
                if (
                    value.cyclotomic_status == "unit"
                    and value.aggregate_status == "proper_factor"
                ):
                    counts["unit_cyclotomic_residual_proper_factors"] += 1
                if not clean:
                    continue
                counts["clean_residual_proper_factors"] += 1
                for shape, enabled in (
                    ("square_free", square_free),
                    ("repeated_prime", repeated_prime),
                ):
                    if not enabled:
                        continue
                    key = f"{family}_{shape}"
                    rank = (
                        modulus,
                        first_factor * (second_factor - 1),
                        first_factor,
                        second_factor,
                        base,
                    )
                    record: dict[str, int | str] = {
                        "base": base,
                        "modulus": modulus,
                        "first_factor": first_factor,
                        "second_factor": second_factor,
                        "family": family,
                        "cyclotomic_gcd": value.cyclotomic_gcd,
                        "aggregate_gcd": value.aggregate_gcd,
                    }
                    if key not in minima or rank < minima[key][0]:
                        minima[key] = (rank, record)

    minimal_witnesses = {
        key: value[1] for key, value in sorted(minima.items())
    }
    expected_minima = {
        "phi4_repeated_prime": (9, 4, 11, 7, 3),
        "phi4_square_free": (15, 11, 3, 7, 5),
        "phi6_repeated_prime": (25, 3, 5, 3, 5),
        "phi6_square_free": (35, 8, 5, 3, 5),
    }
    for key, expected in expected_minima.items():
        actual = minimal_witnesses.get(key)
        if actual is None or (
            actual["modulus"],
            actual["base"],
            actual["first_factor"],
            actual["second_factor"],
            actual["aggregate_gcd"],
        ) != expected:
            counts["failures"] += 1
    registered_witnesses = {
        "phi4_direct": witness(2, 55, 3, 7, "phi4", "cyclotomic", 5),
        "phi4_full": witness(2, 5, 3, 7, "phi4", "full_collision", None),
        "phi4_residual_square_free": witness(
            11, 15, 3, 7, "phi4", "cofactor", 5
        ),
        "phi4_residual_repeated_prime": witness(
            4, 9, 11, 7, "phi4", "cofactor", 3
        ),
        "phi6_direct": witness(12, 35, 5, 3, "phi6", "cyclotomic", 7),
        "phi6_residual_square_free": witness(
            8, 35, 5, 3, "phi6", "cofactor", 5
        ),
        "phi6_residual_repeated_prime": witness(
            3, 25, 5, 3, "phi6", "cofactor", 5
        ),
    }
    if counts["failures"]:
        raise AssertionError("M26 exceptional-cyclotomic audit failed")
    summary = {
        "schema_version": "1.0.0",
        "parameters": vars(args),
        "counts": counts,
        "minimal_clean_residual_witnesses": minimal_witnesses,
        "registered_witnesses": registered_witnesses,
    }
    canonical = json.dumps(summary, sort_keys=True, separators=(",", ":"))
    summary["summary_sha256"] = hashlib.sha256(canonical.encode()).hexdigest()
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
