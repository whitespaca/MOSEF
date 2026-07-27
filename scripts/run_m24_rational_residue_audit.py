"""Deterministic M24 audit of content, resultants, and cyclotomic factors."""

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
    cleared_root_of_unity_coefficients,
    cyclotomic_factor_orders,
    evaluate_rational_residue_audit,
    polynomial_multiply,
    signed_numerator_coefficients,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--factor-max", type=int, default=8)
    parser.add_argument("--coefficient-max", type=int, default=3)
    parser.add_argument("--cyclotomic-order-max", type=int, default=128)
    parser.add_argument("--modulus-max", type=int, default=128)
    parser.add_argument("--base-max", type=int, default=16)
    return parser.parse_args()


def geometric_coefficients(exponent: int, step: int = 1) -> tuple[int, ...]:
    result = [0] * (step * (exponent - 1) + 1)
    for index in range(exponent):
        result[step * index] = 1
    return tuple(result)


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


def scale(values: tuple[int, ...], multiplier: int) -> tuple[int, ...]:
    return tuple(multiplier * value for value in values)


def first_stage_bezout_cofactor(
    first_factor: int,
    second_factor: int,
    first_coefficient: int,
    second_coefficient: int,
) -> tuple[int, ...]:
    weighted = [0] * (first_factor * (second_factor - 2) + 1)
    for index in range(second_factor - 1):
        weighted[first_factor * index] = second_factor - 1 - index
    inner = polynomial_add(
        (first_coefficient,),
        scale(polynomial_multiply((-1, 1), tuple(weighted)), second_coefficient),
    )
    return polynomial_add(
        polynomial_multiply(
            geometric_coefficients(first_factor),
            inner,
        ),
        (second_coefficient * second_factor,),
    )


def is_proper(value: int, modulus: int) -> bool:
    return 1 < value < modulus


def main() -> int:
    args = parse_args()
    if (
        args.factor_max < 3
        or args.coefficient_max < 1
        or args.cyclotomic_order_max < 4
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
        "coefficient_pairs": 0,
        "primitive_coefficient_pairs": 0,
        "content_normalizations": 0,
        "first_stage_bezout_checks": 0,
        "cleared_root_of_unity_checks": 0,
        "cyclotomic_divisibility_checks": 0,
        "cyclotomic_factors": 0,
        "phi1_boundary_factors": 0,
        "difference_common_step_factors": 0,
        "exceptional_cyclotomic_factors": 0,
        "identity_failures": 0,
    }
    first_exception: dict[str, Any] | None = None
    for first_factor in range(2, args.factor_max + 1):
        for second_factor in range(2, args.factor_max + 1):
            if first_factor == second_factor:
                continue
            symbolic["unequal_pairs"] += 1
            common_step = math.gcd(first_factor - 1, second_factor - 1)
            for first_coefficient in coefficients:
                for second_coefficient in coefficients:
                    symbolic["coefficient_pairs"] += 1
                    content = math.gcd(
                        abs(first_coefficient),
                        abs(second_coefficient),
                    )
                    primitive = (
                        first_coefficient // content,
                        second_coefficient // content,
                    )
                    symbolic["content_normalizations"] += 1
                    if math.gcd(abs(primitive[0]), abs(primitive[1])) != 1:
                        symbolic["identity_failures"] += 1

                    numerator = signed_numerator_coefficients(
                        first_factor,
                        second_factor,
                        first_coefficient,
                        second_coefficient,
                    )
                    symbolic["first_stage_bezout_checks"] += 1
                    if first_stage_bezout_cofactor(
                        first_factor,
                        second_factor,
                        first_coefficient,
                        second_coefficient,
                    ) != numerator:
                        symbolic["identity_failures"] += 1

                    first_endpoint = (
                        (-1,)
                        + (0,) * (first_factor - 1)
                        + (1,)
                    )
                    symbolic["cleared_root_of_unity_checks"] += 1
                    if polynomial_multiply(
                        polynomial_multiply((-1, 1), first_endpoint),
                        numerator,
                    ) != cleared_root_of_unity_coefficients(
                        first_factor,
                        second_factor,
                        first_coefficient,
                        second_coefficient,
                    ):
                        symbolic["identity_failures"] += 1

                    if content != 1:
                        continue
                    symbolic["primitive_coefficient_pairs"] += 1
                    orders = cyclotomic_factor_orders(
                        first_factor,
                        second_factor,
                        first_coefficient,
                        second_coefficient,
                        args.cyclotomic_order_max,
                    )
                    symbolic[
                        "cyclotomic_divisibility_checks"
                    ] += args.cyclotomic_order_max
                    for order in orders:
                        symbolic["cyclotomic_factors"] += 1
                        phi1_boundary = (
                            order == 1
                            and first_coefficient * first_factor
                            + second_coefficient * second_factor
                            == 0
                        )
                        difference_common = (
                            order > 1
                            and first_coefficient + second_coefficient == 0
                            and common_step % order == 0
                        )
                        if phi1_boundary:
                            symbolic["phi1_boundary_factors"] += 1
                        elif difference_common:
                            symbolic["difference_common_step_factors"] += 1
                        else:
                            symbolic["exceptional_cyclotomic_factors"] += 1
                            if first_exception is None:
                                first_exception = {
                                    "first_factor": first_factor,
                                    "second_factor": second_factor,
                                    "first_coefficient": first_coefficient,
                                    "second_coefficient": second_coefficient,
                                    "content": content,
                                    "order": order,
                                }

    modular = {
        "unit_bases": 0,
        "nonunit_bases": 0,
        "evaluations": 0,
        "unit_contents": 0,
        "proper_contents": 0,
        "full_contents": 0,
        "unit_prefixes": 0,
        "proper_prefixes": 0,
        "full_prefixes": 0,
        "content_unit_normalization_checks": 0,
        "rational_reduction_checks": 0,
        "first_overlap_checks": 0,
        "second_overlap_checks": 0,
        "strict_residual_proper_factors": 0,
        "unexplained_failures": 0,
    }
    first_strict_residual: dict[str, Any] | None = None
    for modulus in range(4, args.modulus_max + 1):
        for base in range(min(modulus - 1, args.base_max) + 1):
            if math.gcd(base, modulus) != 1:
                modular["nonunit_bases"] += 1
                continue
            modular["unit_bases"] += 1
            for first_factor in range(2, args.factor_max + 1):
                for second_factor in range(2, args.factor_max + 1):
                    if first_factor == second_factor:
                        continue
                    for first_coefficient in coefficients:
                        for second_coefficient in coefficients:
                            value = evaluate_rational_residue_audit(
                                base,
                                modulus,
                                first_factor,
                                second_factor,
                                first_coefficient,
                                second_coefficient,
                            )
                            modular["evaluations"] += 1
                            content_key = {
                                "unit": "unit_contents",
                                "proper_factor": "proper_contents",
                                "full_collision": "full_contents",
                            }[value.content_status]
                            modular[content_key] += 1
                            if value.content_status == "unit":
                                modular["content_unit_normalization_checks"] += 1
                                if (
                                    value.aggregate_gcd
                                    != value.primitive_aggregate_gcd
                                ):
                                    modular["unexplained_failures"] += 1
                            prefix_key = {
                                "unit": "unit_prefixes",
                                "proper_factor": "proper_prefixes",
                                "full_collision": "full_prefixes",
                            }[value.prefix_status]
                            modular[prefix_key] += 1
                            if value.prefix_status == "unit":
                                modular["rational_reduction_checks"] += 1
                                if value.aggregate_gcd != value.rational_gcd:
                                    modular["unexplained_failures"] += 1
                            modular["first_overlap_checks"] += 1
                            modular["second_overlap_checks"] += 1
                            if (
                                value.first_public_bound_gcd
                                % value.first_overlap_gcd
                                or value.second_public_bound_gcd
                                % value.second_overlap_gcd
                            ):
                                modular["unexplained_failures"] += 1
                            if (
                                value.content_status == "unit"
                                and value.first_quotient_gcd == 1
                                and value.second_quotient_gcd == 1
                                and value.first_public_bound_gcd == 1
                                and value.second_public_bound_gcd == 1
                                and is_proper(value.aggregate_gcd, modulus)
                            ):
                                modular["strict_residual_proper_factors"] += 1
                                if first_strict_residual is None:
                                    first_strict_residual = {
                                        "modulus": modulus,
                                        "base": base,
                                        "first_factor": first_factor,
                                        "second_factor": second_factor,
                                        "first_coefficient": first_coefficient,
                                        "second_coefficient": second_coefficient,
                                        "aggregate_gcd": value.aggregate_gcd,
                                    }

    named = evaluate_rational_residue_audit(2, 55, 3, 7, 1, 1)
    named_orders = cyclotomic_factor_orders(3, 7, 1, 1, 20)
    if (
        named_orders != (4,)
        or named.first_quotient_gcd != 1
        or named.second_quotient_gcd != 1
        or named.aggregate_gcd != 5
        or named.first_public_bound_gcd != 1
        or named.second_public_bound_gcd != 1
    ):
        raise AssertionError("named Phi_4 witness was not reproduced")
    if symbolic["identity_failures"] or modular["unexplained_failures"]:
        raise AssertionError("M24 registered identity or reduction failed")

    summary = {
        "schema_version": "1.0.0",
        "parameters": vars(args),
        "symbolic": symbolic,
        "modular": modular,
        "first_exceptional_cyclotomic_factor": first_exception,
        "first_strict_residual": first_strict_residual,
        "named_phi4_witness": {
            "modulus": 55,
            "base": 2,
            "first_factor": 3,
            "second_factor": 7,
            "first_coefficient": 1,
            "second_coefficient": 1,
            "cyclotomic_orders_through_20": named_orders,
            "first_quotient": named.first_quotient_residue,
            "second_quotient": named.second_quotient_residue,
            "aggregate": named.aggregate_residue,
            "aggregate_gcd": named.aggregate_gcd,
            "rational_gcd": named.rational_gcd,
        },
    }
    canonical = json.dumps(summary, sort_keys=True, separators=(",", ":"))
    summary["summary_sha256"] = hashlib.sha256(canonical.encode()).hexdigest()
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
