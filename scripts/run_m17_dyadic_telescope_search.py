"""Audit the M17 dyadic rational/compositional circuit."""

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
    dyadic_geometric_coefficients,
    evaluate_dyadic_telescope,
)


def canonical_json(value: Any) -> bytes:
    """Serialize one result deterministically for hashing."""
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def multiply_polynomials(
    left: tuple[int, ...],
    right: tuple[int, ...],
) -> tuple[int, ...]:
    """Multiply two small exact integer coefficient vectors."""
    result = [0] * (len(left) + len(right) - 1)
    for left_index, left_value in enumerate(left):
        for right_index, right_value in enumerate(right):
            result[left_index + right_index] += left_value * right_value
    return tuple(result)


def search(
    level_max: int,
    modulus_max: int,
    base_max: int,
) -> dict[str, Any]:
    """Run the deterministic symbolic and modular dyadic audit."""
    if not 0 <= level_max <= 12:
        raise ValueError("level_max must lie in [0, 12]")
    if not 4 <= modulus_max <= 512:
        raise ValueError("modulus_max must lie in [4, 512]")
    if not 1 <= base_max <= 64:
        raise ValueError("base_max must lie in [1, 64]")

    symbolic_identities = 0
    coefficient_checks = 0
    maximum_monomials = 0
    for levels in range(level_max + 1):
        product = (1,)
        for index in range(levels):
            factor = [0] * ((1 << index) + 1)
            factor[0] = 1
            factor[-1] = 1
            product = multiply_polynomials(product, tuple(factor))
        expected = dyadic_geometric_coefficients(levels)
        if product != expected:
            raise AssertionError("dyadic polynomial identity failed")
        symbolic_identities += 1
        coefficient_checks += len(expected)
        maximum_monomials = max(maximum_monomials, len(expected))

    circuit_checks = 0
    recurrence_checks = 0
    product_identity_checks = 0
    division_checks = 0
    quotient_implication_checks = 0
    numerator_implication_checks = 0
    unexplained_proper_successes = 0
    masked_quotient_successes = 0
    unit_denominators = 0
    proper_denominator_exits = 0
    full_denominator_collisions = 0
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
            for levels in range(level_max + 1):
                evaluation = evaluate_dyadic_telescope(base, modulus, levels)
                circuit_checks += 1

                for left, right in zip(
                    evaluation.power_residues,
                    evaluation.power_residues[1:],
                    strict=False,
                ):
                    recurrence_checks += 1
                    if left * left % modulus != right:
                        raise AssertionError("dyadic composition recurrence failed")

                product_identity_checks += 1
                if (
                    evaluation.denominator_residue
                    * evaluation.quotient_residue
                    % modulus
                    != evaluation.numerator_residue
                ):
                    raise AssertionError("telescoping residue identity failed")

                proper_factors = tuple(
                    divisor
                    for divisor in evaluation.factor_gcds
                    if 1 < divisor < modulus
                )
                if 1 < evaluation.quotient_gcd < modulus:
                    quotient_implication_checks += 1
                    if not proper_factors:
                        unexplained_proper_successes += 1
                if evaluation.quotient_gcd == modulus and proper_factors:
                    masked_quotient_successes += 1

                if 1 < evaluation.numerator_gcd < modulus:
                    numerator_implication_checks += 1
                    if not (
                        1 < evaluation.denominator_gcd < modulus
                        or proper_factors
                    ):
                        unexplained_proper_successes += 1

                if evaluation.division_status == "unit":
                    unit_denominators += 1
                    division_checks += 1
                    if evaluation.division_quotient != evaluation.quotient_residue:
                        raise AssertionError("unit division disagreed with product path")
                elif evaluation.division_status == "proper_factor":
                    proper_denominator_exits += 1
                    if not 1 < evaluation.denominator_gcd < modulus:
                        raise AssertionError("proper denominator exit was misclassified")
                elif evaluation.division_status == "full_collision":
                    full_denominator_collisions += 1
                    if evaluation.denominator_gcd != modulus:
                        raise AssertionError("full denominator collision was misclassified")
                else:
                    raise AssertionError("unknown division status")

    if unexplained_proper_successes:
        raise AssertionError("aggregate success lacked a proper explicit component")

    proper_denominator = evaluate_dyadic_telescope(4, 15, 1)
    full_denominator = evaluate_dyadic_telescope(1, 6, 3)
    unit_denominator = evaluate_dyadic_telescope(2, 15, 1)
    if (
        proper_denominator.denominator_gcd != 3
        or proper_denominator.factor_gcds != (5,)
        or proper_denominator.numerator_gcd != 15
    ):
        raise AssertionError("named complementary collision failed")
    if (
        full_denominator.denominator_gcd != 6
        or full_denominator.quotient_gcd != 2
        or full_denominator.division_quotient is not None
    ):
        raise AssertionError("named full-denominator branch failed")
    if (
        unit_denominator.denominator_gcd != 1
        or unit_denominator.quotient_gcd != 3
        or unit_denominator.division_quotient
        != unit_denominator.quotient_residue
    ):
        raise AssertionError("named unit-denominator quotient failed")

    result: dict[str, Any] = {
        "schema_version": "1.0.0",
        "parameters": {
            "level_max": level_max,
            "modulus_max": modulus_max,
            "base_max": base_max,
        },
        "symbolic": {
            "identity_checks": symbolic_identities,
            "coefficient_checks": coefficient_checks,
            "maximum_monomials": maximum_monomials,
        },
        "modular": {
            "circuit_checks": circuit_checks,
            "recurrence_checks": recurrence_checks,
            "product_identity_checks": product_identity_checks,
            "division_checks": division_checks,
            "quotient_implication_checks": quotient_implication_checks,
            "numerator_implication_checks": numerator_implication_checks,
            "unexplained_proper_successes": unexplained_proper_successes,
            "masked_quotient_successes": masked_quotient_successes,
            "unit_denominators": unit_denominators,
            "proper_denominator_exits": proper_denominator_exits,
            "full_denominator_collisions": full_denominator_collisions,
            "base_unit_prechecks": base_unit_prechecks,
            "base_proper_nonunit_prechecks": base_proper_nonunit_prechecks,
            "base_full_nonunit_prechecks": base_full_nonunit_prechecks,
        },
        "named_proper_denominator": {
            "base": 4,
            "modulus": 15,
            "levels": 1,
            "denominator_gcd": proper_denominator.denominator_gcd,
            "factor_gcds": list(proper_denominator.factor_gcds),
            "numerator_gcd": proper_denominator.numerator_gcd,
        },
        "named_full_denominator": {
            "base": 1,
            "modulus": 6,
            "levels": 3,
            "denominator_gcd": full_denominator.denominator_gcd,
            "quotient_gcd": full_denominator.quotient_gcd,
            "division_status": full_denominator.division_status,
        },
        "named_unit_denominator": {
            "base": 2,
            "modulus": 15,
            "levels": 1,
            "denominator_gcd": unit_denominator.denominator_gcd,
            "quotient_gcd": unit_denominator.quotient_gcd,
            "division_status": unit_denominator.division_status,
        },
    }
    result["summary_sha256"] = hashlib.sha256(canonical_json(result)).hexdigest()
    return result


def main() -> int:
    """Parse arguments, run the audit, and print deterministic JSON."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--level-max", type=int, default=10)
    parser.add_argument("--modulus-max", type=int, default=256)
    parser.add_argument("--base-max", type=int, default=32)
    args = parser.parse_args()
    result = search(args.level_max, args.modulus_max, args.base_max)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
