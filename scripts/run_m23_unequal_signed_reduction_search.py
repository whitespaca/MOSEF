"""Deterministic M23 audit of unequal depth-two signed reductions."""

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
from mosef_reference import (
    evaluate_unequal_signed_reduction,
    unequal_difference_coefficients,
    unequal_difference_cofactor_coefficients,
)

RationalPolynomial = tuple[Fraction, ...]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--factor-max", type=int, default=8)
    parser.add_argument("--coefficient-max", type=int, default=2)
    parser.add_argument("--modulus-max", type=int, default=128)
    parser.add_argument("--base-max", type=int, default=16)
    return parser.parse_args()


def trim(values: list[Fraction]) -> RationalPolynomial:
    while len(values) > 1 and values[-1] == 0:
        values.pop()
    return tuple(values)


def polynomial_add(
    left: tuple[int, ...], right: tuple[int, ...]
) -> tuple[int, ...]:
    result = [0] * max(len(left), len(right))
    for index, value in enumerate(left):
        result[index] += value
    for index, value in enumerate(right):
        result[index] += value
    while len(result) > 1 and result[-1] == 0:
        result.pop()
    return tuple(result)


def polynomial_multiply(
    left: tuple[int, ...], right: tuple[int, ...]
) -> tuple[int, ...]:
    result = [0] * (len(left) + len(right) - 1)
    for left_index, left_value in enumerate(left):
        for right_index, right_value in enumerate(right):
            result[left_index + right_index] += left_value * right_value
    return tuple(result)


def polynomial_divmod(
    dividend: RationalPolynomial,
    divisor: RationalPolynomial,
) -> tuple[RationalPolynomial, RationalPolynomial]:
    remainder = list(dividend)
    quotient = [Fraction(0)] * max(1, len(dividend) - len(divisor) + 1)
    while len(remainder) >= len(divisor) and any(remainder):
        multiplier = remainder[-1] / divisor[-1]
        offset = len(remainder) - len(divisor)
        quotient[offset] = multiplier
        for index, value in enumerate(divisor):
            remainder[offset + index] -= multiplier * value
        remainder = list(trim(remainder))
    return trim(quotient), trim(remainder)


def polynomial_gcd(
    left: tuple[int, ...],
    right: tuple[int, ...],
) -> RationalPolynomial:
    first = tuple(Fraction(value) for value in left)
    second = tuple(Fraction(value) for value in right)
    while any(second):
        _, remainder = polynomial_divmod(first, second)
        first, second = second, remainder
    leading = first[-1]
    return tuple(value / leading for value in first)


def geometric_coefficients(exponent: int, step: int = 1) -> tuple[int, ...]:
    result = [0] * (step * (exponent - 1) + 1)
    for index in range(exponent):
        result[step * index] = 1
    return tuple(result)


def endpoint_coefficients(exponent: int) -> tuple[int, ...]:
    return (-1,) + (0,) * (exponent - 1) + (1,)


def stage_bezout_right(first_factor: int, second_factor: int) -> tuple[int, ...]:
    weighted = [0] * (first_factor * (second_factor - 2) + 1)
    for index in range(second_factor - 1):
        weighted[first_factor * index] = second_factor - 1 - index
    factor = polynomial_multiply((-1, 1), tuple(weighted))
    return polynomial_add(
        polynomial_multiply(geometric_coefficients(first_factor), factor),
        (second_factor,),
    )


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


def main() -> int:
    args = parse_args()
    if (
        args.factor_max < 3
        or args.coefficient_max < 1
        or args.modulus_max < 4
        or args.base_max < 0
    ):
        raise SystemExit("invalid search bounds")

    coefficients = tuple(
        value
        for value in range(-args.coefficient_max, args.coefficient_max + 1)
        if value
    )
    symbolic = {
        "unequal_pairs": 0,
        "stage_coprimality_checks": 0,
        "stage_bezout_checks": 0,
        "endpoint_gcd_checks": 0,
        "common_step_factor_checks": 0,
        "boundary_factor_checks": 0,
        "cofactor_coefficients": 0,
        "identity_failures": 0,
    }
    for first_factor in range(2, args.factor_max + 1):
        for second_factor in range(2, args.factor_max + 1):
            if first_factor == second_factor:
                continue
            symbolic["unequal_pairs"] += 1
            first = geometric_coefficients(first_factor)
            second = geometric_coefficients(second_factor, first_factor)
            difference = unequal_difference_coefficients(
                first_factor,
                second_factor,
            )
            common_step = math.gcd(first_factor - 1, second_factor - 1)
            common_sum = geometric_coefficients(common_step)
            cofactor = unequal_difference_cofactor_coefficients(
                first_factor,
                second_factor,
            )
            symbolic["cofactor_coefficients"] += len(cofactor)
            symbolic["common_step_factor_checks"] += 1
            if polynomial_multiply((0,) + common_sum, cofactor) != difference:
                symbolic["identity_failures"] += 1

            symbolic["stage_coprimality_checks"] += 1
            if polynomial_gcd(first, second) != (Fraction(1),):
                symbolic["identity_failures"] += 1
            symbolic["stage_bezout_checks"] += 1
            if stage_bezout_right(first_factor, second_factor) != second:
                symbolic["identity_failures"] += 1

            expected_gcd = tuple(Fraction(value) for value in common_sum)
            for endpoint in (first_factor - 1, second_factor - 1):
                symbolic["endpoint_gcd_checks"] += 1
                if polynomial_gcd(
                    difference,
                    endpoint_coefficients(endpoint),
                ) != expected_gcd:
                    symbolic["identity_failures"] += 1

            for first_coefficient in coefficients:
                for second_coefficient in coefficients:
                    symbolic["boundary_factor_checks"] += 1
                    has_x = first_coefficient + second_coefficient == 0
                    has_one = (
                        first_coefficient * first_factor
                        + second_coefficient * second_factor
                        == 0
                    )
                    if has_x and has_one:
                        symbolic["identity_failures"] += 1

    modular = {
        "unit_bases": 0,
        "nonunit_bases": 0,
        "factor_pairs": 0,
        "signed_evaluations": 0,
        "unit_prefixes": 0,
        "proper_prefixes": 0,
        "full_prefixes": 0,
        "rational_reduction_checks": 0,
        "full_public_reduction_checks": 0,
        "common_stage_divisor_checks": 0,
        "difference_evaluations": 0,
        "prime_power_components": 0,
        "valuation_checks": 0,
        "unit_common_factors": 0,
        "proper_common_factors": 0,
        "full_common_factors": 0,
        "proper_differences": 0,
        "proper_via_common_factor": 0,
        "proper_via_unit_factor_cofactor": 0,
        "unit_stage_new_proper_differences": 0,
        "unit_stage_common_factor_paths": 0,
        "unit_stage_cofactor_paths": 0,
        "unexplained_failures": 0,
    }
    first_common_factor_path: dict[str, Any] | None = None
    first_cofactor_path: dict[str, Any] | None = None

    for modulus in range(4, args.modulus_max + 1):
        components = prime_powers(modulus)
        for base in range(min(modulus - 1, args.base_max) + 1):
            if math.gcd(base, modulus) != 1:
                modular["nonunit_bases"] += 1
                continue
            modular["unit_bases"] += 1
            for first_factor in range(2, args.factor_max + 1):
                for second_factor in range(2, args.factor_max + 1):
                    if first_factor == second_factor:
                        continue
                    modular["factor_pairs"] += 1
                    difference_value = evaluate_unequal_signed_reduction(
                        base,
                        modulus,
                        first_factor,
                        second_factor,
                        -1,
                        1,
                    )
                    modular["difference_evaluations"] += 1
                    modular["prime_power_components"] += len(components)
                    modular["common_stage_divisor_checks"] += 1
                    if (
                        difference_value.multiplier_gcd
                        % difference_value.common_stage_gcd
                    ):
                        modular["unexplained_failures"] += 1

                    cofactor_coefficients = (
                        unequal_difference_cofactor_coefficients(
                            first_factor,
                            second_factor,
                        )
                    )
                    expanded_cofactor = 0
                    for coefficient in reversed(cofactor_coefficients):
                        expanded_cofactor = (
                            expanded_cofactor * base + coefficient
                        ) % modulus

                    for prime, prime_exponent in components:
                        factor_valuation = capped_valuation(
                            difference_value.common_factor_residue,
                            prime,
                            prime_exponent,
                        )
                        cofactor_valuation = capped_valuation(
                            expanded_cofactor,
                            prime,
                            prime_exponent,
                        )
                        difference_valuation = capped_valuation(
                            difference_value.difference_residue,
                            prime,
                            prime_exponent,
                        )
                        modular["valuation_checks"] += 1
                        if difference_valuation != min(
                            prime_exponent,
                            factor_valuation + cofactor_valuation,
                        ):
                            modular["unexplained_failures"] += 1

                    factor_gcd = difference_value.common_factor_gcd
                    if factor_gcd == 1:
                        modular["unit_common_factors"] += 1
                        if (
                            difference_value.difference_cofactor_residue
                            != expanded_cofactor
                            or difference_value.difference_gcd
                            != difference_value.difference_cofactor_gcd
                        ):
                            modular["unexplained_failures"] += 1
                    elif factor_gcd < modulus:
                        modular["proper_common_factors"] += 1
                    else:
                        modular["full_common_factors"] += 1
                        if difference_value.difference_gcd != modulus:
                            modular["unexplained_failures"] += 1

                    if is_proper(difference_value.difference_gcd, modulus):
                        modular["proper_differences"] += 1
                        if is_proper(factor_gcd, modulus):
                            modular["proper_via_common_factor"] += 1
                        elif (
                            factor_gcd == 1
                            and difference_value.difference_cofactor_gcd
                            is not None
                            and is_proper(
                                difference_value.difference_cofactor_gcd,
                                modulus,
                            )
                        ):
                            modular["proper_via_unit_factor_cofactor"] += 1
                        else:
                            modular["unexplained_failures"] += 1

                        if (
                            difference_value.first_quotient_gcd
                            == difference_value.second_quotient_gcd
                            == 1
                        ):
                            modular["unit_stage_new_proper_differences"] += 1
                            if is_proper(factor_gcd, modulus):
                                modular["unit_stage_common_factor_paths"] += 1
                                if first_common_factor_path is None:
                                    first_common_factor_path = {
                                        "modulus": modulus,
                                        "base": base,
                                        "first_factor": first_factor,
                                        "second_factor": second_factor,
                                        "difference": difference_value.difference_residue,
                                        "difference_gcd": difference_value.difference_gcd,
                                        "common_step": difference_value.common_step,
                                        "common_factor": (
                                            difference_value.common_factor_residue
                                        ),
                                    }
                            elif (
                                factor_gcd == 1
                                and difference_value.difference_cofactor_gcd
                                is not None
                                and is_proper(
                                    difference_value.difference_cofactor_gcd,
                                    modulus,
                                )
                            ):
                                modular["unit_stage_cofactor_paths"] += 1
                                if first_cofactor_path is None:
                                    first_cofactor_path = {
                                        "modulus": modulus,
                                        "base": base,
                                        "first_factor": first_factor,
                                        "second_factor": second_factor,
                                        "first_quotient": (
                                            difference_value.first_quotient_residue
                                        ),
                                        "second_quotient": (
                                            difference_value.second_quotient_residue
                                        ),
                                        "difference": difference_value.difference_residue,
                                        "difference_gcd": difference_value.difference_gcd,
                                        "common_step": difference_value.common_step,
                                        "common_factor": (
                                            difference_value.common_factor_residue
                                        ),
                                        "cofactor": expanded_cofactor,
                                    }

                    for first_coefficient in coefficients:
                        for second_coefficient in coefficients:
                            value = evaluate_unequal_signed_reduction(
                                base,
                                modulus,
                                first_factor,
                                second_factor,
                                first_coefficient,
                                second_coefficient,
                            )
                            modular["signed_evaluations"] += 1
                            if value.first_quotient_status == "unit":
                                modular["unit_prefixes"] += 1
                                modular["rational_reduction_checks"] += 1
                                if value.aggregate_gcd != value.rational_reduction_gcd:
                                    modular["unexplained_failures"] += 1
                            elif value.first_quotient_status == "proper_factor":
                                modular["proper_prefixes"] += 1
                            else:
                                modular["full_prefixes"] += 1
                                modular["full_public_reduction_checks"] += 1
                                if value.aggregate_gcd != value.public_full_gcd:
                                    modular["unexplained_failures"] += 1

    if symbolic["identity_failures"] or modular["unexplained_failures"]:
        raise AssertionError("M23 registered identity or reduction failed")
    named_common = evaluate_unequal_signed_reduction(2, 9, 5, 7, -1, 1)
    named_cofactor = evaluate_unequal_signed_reduction(3, 25, 3, 2, -1, 1)
    if named_common.common_factor_gcd != 3 or named_cofactor.aggregate_gcd != 5:
        raise AssertionError("named M23 paths were not reproduced")

    summary = {
        "schema_version": "1.0.0",
        "parameters": vars(args),
        "symbolic": symbolic,
        "modular": modular,
        "first_unit_stage_common_factor_path": first_common_factor_path,
        "first_unit_stage_cofactor_path": first_cofactor_path,
        "named_common_factor_path": {
            "modulus": 9,
            "base": 2,
            "first_factor": 5,
            "second_factor": 7,
            "difference_gcd": named_common.difference_gcd,
            "common_step": named_common.common_step,
            "common_factor_gcd": named_common.common_factor_gcd,
        },
        "named_cofactor_path": {
            "modulus": 25,
            "base": 3,
            "first_factor": 3,
            "second_factor": 2,
            "difference_gcd": named_cofactor.difference_gcd,
            "common_step": named_cofactor.common_step,
            "cofactor_gcd": named_cofactor.difference_cofactor_gcd,
            "rational_reduction_gcd": named_cofactor.rational_reduction_gcd,
        },
    }
    canonical = json.dumps(summary, sort_keys=True, separators=(",", ":"))
    summary["summary_sha256"] = hashlib.sha256(canonical.encode()).hexdigest()
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
