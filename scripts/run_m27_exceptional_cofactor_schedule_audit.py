"""Deterministic M27 audit of local roots, overlaps, and fixed schedules."""

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
    evaluate_exceptional_cofactor_local_profile,
    evaluate_exceptional_cyclotomic,
    exceptional_cofactor_coefficients,
    exceptional_cofactor_overlap,
    exceptional_cofactor_root_residues,
    is_prime,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--factor-max", type=int, default=19)
    parser.add_argument("--prime-max", type=int, default=97)
    parser.add_argument("--valuation-exponent-max", type=int, default=3)
    parser.add_argument("--prefix-max", type=int, default=16)
    parser.add_argument("--schedule-prime-max", type=int, default=400)
    return parser.parse_args()


def family_pairs(factor_max: int) -> list[tuple[int, int, str]]:
    pairs: list[tuple[int, int, str]] = []
    for first_factor in range(2, factor_max + 1):
        for second_factor in range(2, factor_max + 1):
            if first_factor == second_factor:
                continue
            if first_factor % 4 == 3 and second_factor % 4 == 3:
                pairs.append((first_factor, second_factor, "phi4"))
            if first_factor % 6 == 5 and second_factor % 6 == 3:
                pairs.append((first_factor, second_factor, "phi6"))
    return pairs


def evaluate_coefficients(
    coefficients: tuple[int, ...],
    base: int,
    modulus: int,
) -> int:
    result = 0
    for coefficient in reversed(coefficients):
        result = (result * base + coefficient) % modulus
    return result


def reduce_quadratic(
    coefficients: tuple[int, ...],
    linear_coefficient: int,
) -> tuple[int, int]:
    power_constant, power_linear = 1, 0
    result_constant, result_linear = 0, 0
    for coefficient in coefficients:
        result_constant += coefficient * power_constant
        result_linear += coefficient * power_linear
        power_constant, power_linear = (
            -power_linear,
            power_constant - linear_coefficient * power_linear,
        )
    return result_constant, result_linear


def geometric_residue(base: int, count: int, modulus: int) -> int:
    return sum(pow(base, exponent, modulus) for exponent in range(count)) % modulus


def capped_valuation(residue: int, prime: int, exponent: int) -> int:
    if residue == 0:
        return exponent
    valuation = 0
    while valuation < exponent and residue % prime == 0:
        residue //= prime
        valuation += 1
    return valuation


def schedule_misses(
    modulus: int,
    first_factor: int,
    second_factor: int,
    family: str,
    prefix_length: int,
) -> bool:
    overlap = exceptional_cofactor_overlap(
        first_factor,
        second_factor,
        family,
    )
    resultant_gcd = math.gcd(
        overlap.cyclotomic_cofactor_resultant,
        modulus,
    )
    if 1 < resultant_gcd < modulus:
        return False
    for base in range(2, prefix_length + 2):
        if math.gcd(base, modulus) != 1:
            return False
        value = evaluate_exceptional_cyclotomic(
            base,
            modulus,
            first_factor,
            second_factor,
            family,
        )
        component_gcds = (
            value.first_quotient_gcd,
            value.second_quotient_gcd,
            value.first_public_bound_gcd,
            value.second_public_bound_gcd,
            value.cyclotomic_gcd,
            value.cofactor_gcd,
        )
        if any(
            component is not None and 1 < component < modulus
            for component in component_gcds
        ):
            return False
    return True


def main() -> int:
    args = parse_args()
    if (
        args.factor_max < 19
        or args.prime_max < 97
        or args.valuation_exponent_max < 3
        or args.prefix_max < 16
        or args.schedule_prime_max < 400
    ):
        raise SystemExit("bounds do not cover the registered M27 audit")
    counts = {
        "exceptional_factor_pairs": 0,
        "exact_remainder_checks": 0,
        "cyclotomic_resultant_checks": 0,
        "prime_root_enumerations": 0,
        "unit_root_trials": 0,
        "cofactor_roots": 0,
        "root_degree_bound_checks": 0,
        "stage_overlap_implication_checks": 0,
        "cyclotomic_overlap_implication_checks": 0,
        "prime_power_valuation_checks": 0,
        "dense_compact_checks": 0,
        "fixed_prefix_searches": 0,
        "semiprime_candidates": 0,
        "failures": 0,
    }
    primes = [prime for prime in range(2, args.prime_max + 1) if is_prime(prime)]
    root_extrema: dict[str, dict[str, int]] = {}
    for first_factor, second_factor, family in family_pairs(args.factor_max):
        counts["exceptional_factor_pairs"] += 1
        overlap = exceptional_cofactor_overlap(
            first_factor,
            second_factor,
            family,
        )
        cofactor = exceptional_cofactor_coefficients(
            first_factor,
            second_factor,
            family,
        )
        linear_coefficient = 0 if family == "phi4" else -1
        remainder = reduce_quadratic(cofactor, linear_coefficient)
        if remainder != (
            overlap.remainder_constant,
            overlap.remainder_linear,
        ):
            counts["failures"] += 1
        counts["exact_remainder_checks"] += 1
        constant, linear = remainder
        resultant = (
            constant * constant + linear * linear
            if family == "phi4"
            else constant * constant + constant * linear + linear * linear
        )
        if resultant != overlap.cyclotomic_cofactor_resultant or resultant <= 0:
            counts["failures"] += 1
        counts["cyclotomic_resultant_checks"] += 1

        for prime in primes:
            roots = exceptional_cofactor_root_residues(
                prime,
                first_factor,
                second_factor,
                family,
            )
            counts["prime_root_enumerations"] += 1
            counts["unit_root_trials"] += prime - 1
            counts["cofactor_roots"] += len(roots)
            if len(roots) > min(overlap.cofactor_degree, prime - 1):
                counts["failures"] += 1
            counts["root_degree_bound_checks"] += 1
            current = root_extrema.get(family)
            if current is None or len(roots) > current["root_count"]:
                root_extrema[family] = {
                    "first_factor": first_factor,
                    "second_factor": second_factor,
                    "prime": prime,
                    "root_count": len(roots),
                    "degree": overlap.cofactor_degree,
                }
            for base in range(1, prime):
                first_stage = geometric_residue(base, first_factor, prime)
                second_stage = geometric_residue(
                    pow(base, first_factor, prime),
                    second_factor,
                    prime,
                )
                cofactor_residue = evaluate_coefficients(
                    cofactor,
                    base,
                    prime,
                )
                if (
                    first_stage == 0
                    and cofactor_residue == 0
                    and second_factor % prime != 0
                ):
                    counts["failures"] += 1
                if (
                    second_stage == 0
                    and cofactor_residue == 0
                    and all(value % prime != 0 for value in overlap.stage_overlap_support)
                ):
                    counts["failures"] += 1
                counts["stage_overlap_implication_checks"] += 2
                cyclotomic = (
                    (base * base + 1) % prime
                    if family == "phi4"
                    else (base * base - base + 1) % prime
                )
                if (
                    cyclotomic == 0
                    and cofactor_residue == 0
                    and resultant % prime != 0
                ):
                    counts["failures"] += 1
                counts["cyclotomic_overlap_implication_checks"] += 1

            for exponent in range(1, args.valuation_exponent_max + 1):
                modulus = prime**exponent
                for base in range(1, min(prime, 20)):
                    profile = evaluate_exceptional_cofactor_local_profile(
                        base,
                        prime,
                        exponent,
                        first_factor,
                        second_factor,
                        family,
                    )
                    dense = evaluate_coefficients(cofactor, base, modulus)
                    if dense != profile.cofactor_residue:
                        counts["failures"] += 1
                    counts["dense_compact_checks"] += 1
                    if profile.cofactor_valuation != capped_valuation(
                        dense,
                        prime,
                        exponent,
                    ):
                        counts["failures"] += 1
                    counts["prime_power_valuation_checks"] += 1

    prefix_lengths = [1, 2, 4, 8, 16]
    schedule_primes = [
        prime
        for prime in range(2, args.schedule_prime_max + 1)
        if is_prime(prime)
    ]
    avoidance_witnesses: dict[str, dict[str, int | str]] = {}
    families = (("phi4", 3, 7), ("phi6", 5, 3))
    for family, first_factor, second_factor in families:
        for prefix_length in prefix_lengths:
            found: dict[str, int | str] | None = None
            eligible = [
                prime
                for prime in schedule_primes
                if prime > prefix_length + 1
            ]
            for index, first_prime in enumerate(eligible):
                for second_prime in eligible[index + 1 :]:
                    counts["semiprime_candidates"] += 1
                    modulus = first_prime * second_prime
                    if schedule_misses(
                        modulus,
                        first_factor,
                        second_factor,
                        family,
                        prefix_length,
                    ):
                        rank = (modulus, first_prime, second_prime)
                        if found is None or rank < (
                            found["modulus"],
                            found["first_prime"],
                            found["second_prime"],
                        ):
                            found = {
                                "family": family,
                                "first_factor": first_factor,
                                "second_factor": second_factor,
                                "prefix_length": prefix_length,
                                "modulus": modulus,
                                "first_prime": first_prime,
                                "second_prime": second_prime,
                            }
            counts["fixed_prefix_searches"] += 1
            if found is None:
                counts["failures"] += 1
            else:
                avoidance_witnesses[f"{family}_prefix_{prefix_length}"] = found

    expected_minima = {
        "phi4_prefix_1": (33, 3, 11),
        "phi4_prefix_2": (187, 11, 17),
        "phi4_prefix_4": (209, 11, 19),
        "phi4_prefix_8": (517, 11, 47),
        "phi4_prefix_16": (2491, 47, 53),
        "phi6_prefix_1": (55, 5, 11),
        "phi6_prefix_2": (391, 17, 23),
        "phi6_prefix_4": (391, 17, 23),
        "phi6_prefix_8": (493, 17, 29),
        "phi6_prefix_16": (1537, 29, 53),
    }
    for key, expected in expected_minima.items():
        witness = avoidance_witnesses.get(key)
        if witness is None or (
            witness["modulus"],
            witness["first_prime"],
            witness["second_prime"],
        ) != expected:
            counts["failures"] += 1
    if counts["failures"]:
        raise AssertionError("M27 exceptional-cofactor schedule audit failed")
    summary: dict[str, Any] = {
        "schema_version": "1.0.0",
        "parameters": vars(args),
        "counts": counts,
        "root_extrema": root_extrema,
        "fixed_prefix_avoidance_witnesses": avoidance_witnesses,
    }
    canonical = json.dumps(summary, sort_keys=True, separators=(",", ":"))
    summary["summary_sha256"] = hashlib.sha256(canonical.encode()).hexdigest()
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
