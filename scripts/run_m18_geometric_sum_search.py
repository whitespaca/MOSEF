"""Audit the M18 arbitrary-exponent binary geometric-sum circuit."""

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
    evaluate_geometric_sum,
    geometric_sum_coefficients,
)


def canonical_json(value: Any) -> bytes:
    """Serialize one result deterministically for hashing."""
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def add_polynomials(
    left: tuple[int, ...],
    right: tuple[int, ...],
) -> tuple[int, ...]:
    result = [0] * max(len(left), len(right))
    for index, value in enumerate(left):
        result[index] += value
    for index, value in enumerate(right):
        result[index] += value
    return tuple(result)


def multiply_polynomials(
    left: tuple[int, ...],
    right: tuple[int, ...],
) -> tuple[int, ...]:
    result = [0] * (len(left) + len(right) - 1)
    for left_index, left_value in enumerate(left):
        for right_index, right_value in enumerate(right):
            result[left_index + right_index] += left_value * right_value
    return tuple(result)


def binary_coefficients(exponent: int) -> tuple[int, ...]:
    """Build S_M from S_2r=S_r(1+X^r) and S_2r+1=S_2r+X^2r."""
    if exponent == 1:
        return (1,)
    half = exponent // 2
    lower = binary_coefficients(half)
    doubled = multiply_polynomials(
        lower,
        (1,) + (0,) * (half - 1) + (1,),
    )
    if exponent % 2 == 0:
        return doubled
    return add_polynomials(doubled, (0,) * (2 * half) + (1,))


def search(
    exponent_max: int,
    modulus_max: int,
    base_max: int,
) -> dict[str, Any]:
    """Run the deterministic symbolic and modular arbitrary-exponent audit."""
    if not 1 <= exponent_max <= 256:
        raise ValueError("exponent_max must lie in [1, 256]")
    if not 4 <= modulus_max <= 512:
        raise ValueError("modulus_max must lie in [4, 512]")
    if not 1 <= base_max <= 64:
        raise ValueError("base_max must lie in [1, 64]")

    symbolic_identities = 0
    coefficient_checks = 0
    even_identities = 0
    odd_identities = 0
    for exponent in range(1, exponent_max + 1):
        actual = binary_coefficients(exponent)
        expected = geometric_sum_coefficients(exponent)
        if actual != expected:
            raise AssertionError("binary geometric-sum polynomial identity failed")
        symbolic_identities += 1
        coefficient_checks += exponent
        if exponent > 1:
            if exponent % 2 == 0:
                even_identities += 1
            else:
                odd_identities += 1

    circuit_checks = 0
    binary_step_checks = 0
    residue_identity_checks = 0
    unit_endpoint_reductions = 0
    proper_denominator_exits = 0
    full_exponent_reductions = 0
    unexplained_reductions = 0
    complementary_proper_values = 0
    base_unit_prechecks = 0
    base_proper_nonunit_prechecks = 0
    base_full_nonunit_prechecks = 0

    for modulus in range(4, modulus_max + 1):
        for base in range(base_max + 1):
            base_gcd = math.gcd(base, modulus)
            if base_gcd != 1:
                if base_gcd == modulus:
                    base_full_nonunit_prechecks += 1
                else:
                    base_proper_nonunit_prechecks += 1
                continue
            base_unit_prechecks += 1
            for exponent in range(1, exponent_max + 1):
                evaluation = evaluate_geometric_sum(base, modulus, exponent)
                circuit_checks += 1
                binary_step_checks += exponent.bit_length() - 1

                direct_sum = sum(
                    pow(base, index, modulus) for index in range(exponent)
                ) % modulus
                if (
                    evaluation.power_residue != pow(base, exponent, modulus)
                    or evaluation.sum_residue != direct_sum
                ):
                    raise AssertionError("binary composition disagreed with direct values")
                residue_identity_checks += 1
                if (
                    evaluation.denominator_residue
                    * evaluation.sum_residue
                    % modulus
                    != evaluation.numerator_residue
                ):
                    raise AssertionError("geometric-sum residue identity failed")

                if evaluation.division_status == "unit":
                    unit_endpoint_reductions += 1
                    if (
                        evaluation.division_quotient != evaluation.sum_residue
                        or evaluation.sum_gcd != evaluation.numerator_gcd
                    ):
                        unexplained_reductions += 1
                elif evaluation.division_status == "proper_factor":
                    proper_denominator_exits += 1
                    if not 1 < evaluation.denominator_gcd < modulus:
                        unexplained_reductions += 1
                    if (
                        1 < evaluation.sum_gcd < modulus
                        and evaluation.sum_gcd != evaluation.denominator_gcd
                    ):
                        complementary_proper_values += 1
                elif evaluation.division_status == "full_collision":
                    full_exponent_reductions += 1
                    if (
                        evaluation.sum_residue != exponent % modulus
                        or evaluation.sum_gcd != evaluation.exponent_gcd
                    ):
                        unexplained_reductions += 1
                else:
                    raise AssertionError("unknown division status")

    if unexplained_reductions:
        raise AssertionError("a geometric-sum extraction reduction failed")

    proper = evaluate_geometric_sum(4, 15, 2)
    full = evaluate_geometric_sum(1, 15, 5)
    unit = evaluate_geometric_sum(2, 15, 2)
    repeated = evaluate_geometric_sum(1, 8, 4)
    if (
        proper.denominator_gcd != 3
        or proper.sum_gcd != 5
        or proper.numerator_gcd != 15
    ):
        raise AssertionError("named complementary proper-factor case failed")
    if full.sum_residue != 5 or full.sum_gcd != full.exponent_gcd:
        raise AssertionError("named full-denominator exponent reduction failed")
    if unit.sum_gcd != 3 or unit.sum_gcd != unit.numerator_gcd:
        raise AssertionError("named unit-denominator endpoint reduction failed")
    if repeated.sum_gcd != 4 or repeated.exponent_gcd != 4:
        raise AssertionError("named repeated-prime-power case failed")

    result: dict[str, Any] = {
        "schema_version": "1.0.0",
        "parameters": {
            "exponent_max": exponent_max,
            "modulus_max": modulus_max,
            "base_max": base_max,
        },
        "symbolic": {
            "identity_checks": symbolic_identities,
            "coefficient_checks": coefficient_checks,
            "even_identities": even_identities,
            "odd_identities": odd_identities,
            "maximum_monomials": exponent_max,
        },
        "modular": {
            "circuit_checks": circuit_checks,
            "binary_step_checks": binary_step_checks,
            "residue_identity_checks": residue_identity_checks,
            "unit_endpoint_reductions": unit_endpoint_reductions,
            "proper_denominator_exits": proper_denominator_exits,
            "full_exponent_reductions": full_exponent_reductions,
            "unexplained_reductions": unexplained_reductions,
            "complementary_proper_values": complementary_proper_values,
            "base_unit_prechecks": base_unit_prechecks,
            "base_proper_nonunit_prechecks": base_proper_nonunit_prechecks,
            "base_full_nonunit_prechecks": base_full_nonunit_prechecks,
        },
        "named_proper_denominator": {
            "base": 4,
            "modulus": 15,
            "exponent": 2,
            "denominator_gcd": proper.denominator_gcd,
            "sum_gcd": proper.sum_gcd,
            "numerator_gcd": proper.numerator_gcd,
        },
        "named_full_denominator": {
            "base": 1,
            "modulus": 15,
            "exponent": 5,
            "sum_residue": full.sum_residue,
            "sum_gcd": full.sum_gcd,
            "exponent_gcd": full.exponent_gcd,
        },
        "named_unit_denominator": {
            "base": 2,
            "modulus": 15,
            "exponent": 2,
            "sum_gcd": unit.sum_gcd,
            "numerator_gcd": unit.numerator_gcd,
        },
        "named_repeated_prime_power": {
            "base": 1,
            "modulus": 8,
            "exponent": 4,
            "sum_gcd": repeated.sum_gcd,
            "exponent_gcd": repeated.exponent_gcd,
        },
    }
    result["summary_sha256"] = hashlib.sha256(canonical_json(result)).hexdigest()
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--exponent-max", type=int, default=64)
    parser.add_argument("--modulus-max", type=int, default=256)
    parser.add_argument("--base-max", type=int, default=32)
    args = parser.parse_args()
    result = search(args.exponent_max, args.modulus_max, args.base_max)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
