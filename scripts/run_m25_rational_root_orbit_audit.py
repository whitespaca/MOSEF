"""Deterministic M25 audit of the rational root-of-unity orbit theorem."""

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
from mosef_reference import (  # noqa: E402
    classify_rational_root_orbit,
    evaluate_rational_residue_audit,
    exact_cyclotomic_root_ratio,
    rational_root_order_descriptor,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--factor-max", type=int, default=32)
    parser.add_argument("--order-max", type=int, default=256)
    return parser.parse_args()


def euler_phi(value: int) -> int:
    result = value
    remaining = value
    prime = 2
    while prime * prime <= remaining:
        if remaining % prime == 0:
            result -= result // prime
            while remaining % prime == 0:
                remaining //= prime
        prime += 1
    if remaining > 1:
        result -= result // remaining
    return result


def cyclotomic_at_one(value: int) -> int:
    remaining = value
    prime = 2
    prime_divisors = 0
    only_prime = 1
    while prime * prime <= remaining:
        if remaining % prime == 0:
            prime_divisors += 1
            only_prime = prime
            while remaining % prime == 0:
                remaining //= prime
        prime += 1
    if remaining > 1:
        prime_divisors += 1
        only_prime = remaining
    return only_prime if prime_divisors == 1 else 1


def witness(
    base: int,
    modulus: int,
    first_factor: int,
    second_factor: int,
    first_coefficient: int,
    second_coefficient: int,
    expected_gcd: int,
) -> dict[str, Any]:
    value = evaluate_rational_residue_audit(
        base,
        modulus,
        first_factor,
        second_factor,
        first_coefficient,
        second_coefficient,
    )
    if (
        value.aggregate_gcd != expected_gcd
        or value.first_quotient_gcd != 1
        or value.second_quotient_gcd != 1
        or value.first_public_bound_gcd != 1
        or value.second_public_bound_gcd != 1
    ):
        raise AssertionError("registered modular witness failed")
    return {
        "base": base,
        "modulus": modulus,
        "first_factor": first_factor,
        "second_factor": second_factor,
        "first_coefficient": first_coefficient,
        "second_coefficient": second_coefficient,
        "aggregate": value.aggregate_residue,
        "aggregate_gcd": value.aggregate_gcd,
    }


def main() -> int:
    args = parse_args()
    if args.factor_max < 3 or args.order_max < 6:
        raise SystemExit("invalid search bounds")
    counts = {
        "unequal_factor_pairs": 0,
        "compact_descriptors": 0,
        "order_checks": 0,
        "stage_zero_orders": 0,
        "outside_stage_orders": 0,
        "phase_candidates": 0,
        "phase_only_irrational_orders": 0,
        "exact_galois_orbit_checks": 0,
        "rational_orders": 0,
        "common_step_orders": 0,
        "phi4_orders": 0,
        "phi6_orders": 0,
        "norm_checks": 0,
        "classification_failures": 0,
    }
    first_phase_only: dict[str, int] | None = None
    for first_factor in range(2, args.factor_max + 1):
        for second_factor in range(2, args.factor_max + 1):
            if first_factor == second_factor:
                continue
            counts["unequal_factor_pairs"] += 1
            descriptor = rational_root_order_descriptor(
                first_factor,
                second_factor,
            )
            counts["compact_descriptors"] += 1
            for order in range(2, args.order_max + 1):
                counts["order_checks"] += 1
                classified = classify_rational_root_orbit(
                    first_factor,
                    second_factor,
                    order,
                )
                if classified.common_step != descriptor.common_step:
                    counts["classification_failures"] += 1
                if not classified.outside_stage_zeros:
                    counts["stage_zero_orders"] += 1
                    continue
                counts["outside_stage_orders"] += 1
                if classified.phase_divisible:
                    counts["phase_candidates"] += 1
                exact = exact_cyclotomic_root_ratio(
                    first_factor,
                    second_factor,
                    order,
                )
                counts["exact_galois_orbit_checks"] += 1
                expected = (
                    None
                    if classified.rational_ratio is None
                    else Fraction(classified.rational_ratio)
                )
                if exact != expected:
                    counts["classification_failures"] += 1
                if exact is None:
                    if classified.phase_divisible:
                        counts["phase_only_irrational_orders"] += 1
                        if first_phase_only is None:
                            first_phase_only = {
                                "first_factor": first_factor,
                                "second_factor": second_factor,
                                "order": order,
                                "phase_order": classified.phase_order,
                            }
                    continue
                counts["rational_orders"] += 1
                counts[f"{classified.category}_orders"] += 1
                if exact != 0 and not classified.phase_divisible:
                    counts["classification_failures"] += 1
                if exact + 1 <= 0:
                    continue
                inverse = pow(first_factor, -1, order)
                reduced_exponent = (inverse - 1) % order
                reduced_order = order // math.gcd(order, reduced_exponent)
                left = (int(exact + 1)) ** (euler_phi(order) // 2)
                right_numerator = cyclotomic_at_one(reduced_order) ** (
                    euler_phi(order) // euler_phi(reduced_order)
                )
                right_denominator = cyclotomic_at_one(order)
                counts["norm_checks"] += 1
                if left * right_denominator != right_numerator:
                    counts["classification_failures"] += 1

    phase_obstruction = classify_rational_root_orbit(2, 4, 5)
    if (
        not phase_obstruction.phase_divisible
        or exact_cyclotomic_root_ratio(2, 4, 5) is not None
    ):
        raise AssertionError("minimal phase-only obstruction failed")
    witnesses = {
        "phi4_square_free": witness(2, 55, 3, 7, 1, 1, 5),
        "phi4_repeated_prime": witness(2, 75, 3, 7, 1, 1, 25),
        "phi6_square_free": witness(12, 35, 5, 3, 2, 1, 7),
    }
    if counts["classification_failures"]:
        raise AssertionError("M25 rational-root classification failed")
    summary = {
        "schema_version": "1.0.0",
        "parameters": vars(args),
        "counts": counts,
        "first_phase_only_irrational_order": first_phase_only,
        "minimal_phase_only_obstruction": {
            "first_factor": 2,
            "second_factor": 4,
            "order": 5,
            "phase_order": phase_obstruction.phase_order,
        },
        "modular_witnesses": witnesses,
    }
    canonical = json.dumps(summary, sort_keys=True, separators=(",", ":"))
    summary["summary_sha256"] = hashlib.sha256(canonical.encode()).hexdigest()
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
