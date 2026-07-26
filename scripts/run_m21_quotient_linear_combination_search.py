"""Deterministic falsification search for M21 quotient-stage combinations."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
from mosef_reference import (  # noqa: E402
    evaluate_quotient_linear_combination,
    expand_quotient_linear_combination,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--factor-max", type=int, default=5)
    parser.add_argument("--coefficient-max", type=int, default=1)
    parser.add_argument("--depth-max", type=int, default=3)
    parser.add_argument("--modulus-max", type=int, default=128)
    parser.add_argument("--base-max", type=int, default=16)
    return parser.parse_args()


def is_proper(value: int, modulus: int) -> bool:
    return 1 < value < modulus


def stage_gcds(value: Any) -> tuple[int, ...]:
    return tuple(
        item
        for stage in value.chain.stages
        for item in (
            stage.intermediate_gcd,
            stage.quotient_gcd,
            stage.rational_numerator_gcd,
            stage.composed_denominator_gcd,
            stage.endpoint_gcd,
            stage.multiplier_gcd,
        )
    )


def main() -> int:
    args = parse_args()
    if (
        args.factor_max < 1
        or args.coefficient_max < 1
        or args.depth_max < 2
        or args.modulus_max < 4
        or args.base_max < 0
    ):
        raise SystemExit("invalid positive search bounds")

    coefficients = tuple(
        value
        for value in range(-args.coefficient_max, args.coefficient_max + 1)
        if value != 0
    )
    symbolic = {
        "descriptors": 0,
        "uncollected_terms": 0,
        "collected_terms": 0,
        "evaluation_checks": 0,
    }
    modular = {
        "chains": 0,
        "combinations": 0,
        "proper_aggregates": 0,
        "component_proper_aggregates": 0,
        "new_proper_aggregates": 0,
        "strict_all_unit_successes": 0,
        "full_aggregate_collisions": 0,
        "zero_aggregate_residues": 0,
        "nonunit_bases": 0,
        "unit_bases": 0,
        "unexplained_semantic_failures": 0,
    }
    first_new: dict[str, Any] | None = None
    first_strict: dict[str, Any] | None = None

    factor_tuples = tuple(
        factors
        for depth in range(2, args.depth_max + 1)
        for factors in itertools.product(range(1, args.factor_max + 1), repeat=depth)
    )
    coefficient_tuples = {
        depth: tuple(itertools.product(coefficients, repeat=depth))
        for depth in range(2, args.depth_max + 1)
    }

    for factors in factor_tuples:
        for coefficient_tuple in coefficient_tuples[len(factors)]:
            expanded = expand_quotient_linear_combination(factors, coefficient_tuple)
            symbolic["descriptors"] += 1
            symbolic["uncollected_terms"] += sum(factors)
            symbolic["collected_terms"] += len(expanded)

    for modulus in range(4, args.modulus_max + 1):
        for base in range(min(modulus - 1, args.base_max) + 1):
            if math.gcd(base, modulus) != 1:
                modular["nonunit_bases"] += 1
                continue
            modular["unit_bases"] += 1
            for factors in factor_tuples:
                modular["chains"] += 1
                for coefficient_tuple in coefficient_tuples[len(factors)]:
                    value = evaluate_quotient_linear_combination(
                        base, modulus, factors, coefficient_tuple
                    )
                    modular["combinations"] += 1
                    expanded = expand_quotient_linear_combination(
                        factors, coefficient_tuple
                    )
                    direct = sum(
                        coefficient * pow(base, exponent, modulus)
                        for exponent, coefficient in expanded
                    ) % modulus
                    symbolic["evaluation_checks"] += 1
                    if direct != value.aggregate_residue:
                        modular["unexplained_semantic_failures"] += 1

                    if value.aggregate_residue == 0:
                        modular["zero_aggregate_residues"] += 1
                    if value.aggregate_gcd == modulus:
                        modular["full_aggregate_collisions"] += 1
                    if not is_proper(value.aggregate_gcd, modulus):
                        continue
                    modular["proper_aggregates"] += 1
                    charged = (
                        stage_gcds(value)
                        + value.coefficient_gcds
                        + value.weighted_stage_gcds
                    )
                    if any(is_proper(item, modulus) for item in charged):
                        modular["component_proper_aggregates"] += 1
                        continue
                    modular["new_proper_aggregates"] += 1
                    record = {
                        "modulus": modulus,
                        "base": base,
                        "factors": list(factors),
                        "coefficients": list(coefficient_tuple),
                        "quotients": [
                            stage.quotient_residue for stage in value.chain.stages
                        ],
                        "aggregate": value.aggregate_residue,
                        "aggregate_gcd": value.aggregate_gcd,
                    }
                    if first_new is None:
                        first_new = record
                    if all(item == 1 for item in charged):
                        modular["strict_all_unit_successes"] += 1
                        if first_strict is None:
                            first_strict = record

    if modular["unexplained_semantic_failures"]:
        raise AssertionError("compact and expanded evaluations disagreed")
    named = evaluate_quotient_linear_combination(2, 9, (5, 5), (-1, 1))
    if (
        named.aggregate_residue != 3
        or named.aggregate_gcd != 3
        or any(item != 1 for item in stage_gcds(named))
        or named.coefficient_gcds != (1, 1)
        or named.weighted_stage_gcds != (1, 1)
    ):
        raise AssertionError("registered BAR-016 witness failed")

    summary = {
        "schema_version": "1.0.0",
        "parameters": vars(args),
        "symbolic": symbolic,
        "modular": modular,
        "first_new_proper_aggregate": first_new,
        "first_strict_all_unit_success": first_strict,
        "named_bar_016_witness": {
            "modulus": 9,
            "base": 2,
            "factors": [5, 5],
            "coefficients": [-1, 1],
            "quotients": [4, 7],
            "aggregate": 3,
            "aggregate_gcd": 3,
        },
    }
    canonical = json.dumps(summary, sort_keys=True, separators=(",", ":"))
    summary["summary_sha256"] = hashlib.sha256(canonical.encode()).hexdigest()
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
