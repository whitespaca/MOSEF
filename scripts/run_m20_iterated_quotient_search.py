"""Audit the M20 iterated geometric-quotient chain."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import sys
from pathlib import Path
from typing import Any, Iterator

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

from mosef_reference import evaluate_iterated_quotient  # noqa: E402


def canonical_json(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def factor_chains(factor_max: int, depth_max: int) -> Iterator[tuple[int, ...]]:
    for depth in range(1, depth_max + 1):
        yield from itertools.product(range(1, factor_max + 1), repeat=depth)


def search(
    factor_max: int,
    depth_max: int,
    modulus_max: int,
    base_max: int,
) -> dict[str, Any]:
    if not 1 <= factor_max <= 8:
        raise ValueError("factor_max must lie in [1, 8]")
    if not 1 <= depth_max <= 5:
        raise ValueError("depth_max must lie in [1, 5]")
    if not 4 <= modulus_max <= 256:
        raise ValueError("modulus_max must lie in [4, 256]")
    if not 1 <= base_max <= 32:
        raise ValueError("base_max must lie in [1, 32]")

    chains = tuple(factor_chains(factor_max, depth_max))
    chain_identities = 0
    stage_identities = 0
    coefficient_checks = 0
    maximum_prefix = 1
    for factors in chains:
        prefix = 1
        product = [1]
        for factor in factors:
            quotient = [0] * (prefix * (factor - 1) + 1)
            for index in range(factor):
                quotient[index * prefix] = 1
            expanded = [0] * (prefix * factor)
            for left_index, left_value in enumerate(product):
                for right_index, right_value in enumerate(quotient):
                    expanded[left_index + right_index] += left_value * right_value
            if expanded != [1] * (prefix * factor):
                raise AssertionError("iterated formal identity failed")
            product = expanded
            prefix *= factor
            maximum_prefix = max(maximum_prefix, prefix)
            stage_identities += 1
            coefficient_checks += len(expanded)
        if product != [1] * prefix:
            raise AssertionError("iterated chain certificate failed")
        chain_identities += 1

    circuits = 0
    stages = 0
    prefix_linkages = 0
    residue_identities = 0
    rational_unit = 0
    rational_proper = 0
    rational_full = 0
    composed_unit = 0
    composed_proper = 0
    composed_full = 0
    proper_final_products = 0
    masked_stage_successes = 0
    different_proper_values = 0
    unexplained = 0
    base_units = 0
    base_nonunits = 0
    for modulus in range(4, modulus_max + 1):
        for base in range(base_max + 1):
            if math.gcd(base, modulus) != 1:
                base_nonunits += 1
                continue
            base_units += 1
            for factors in chains:
                value = evaluate_iterated_quotient(base, modulus, factors)
                circuits += 1
                stages += len(value.stages)
                prefix_linkages += max(0, len(value.stages) - 1)
                residue_identities += 2 * len(value.stages) + 1
                if value.final_prefix_residue != value.final_quotient_product_residue:
                    unexplained += 1
                proper_stages = [
                    stage for stage in value.stages
                    if 1 < stage.quotient_gcd < modulus
                ]
                if 1 < value.final_prefix_gcd < modulus:
                    proper_final_products += 1
                    if not proper_stages:
                        unexplained += 1
                elif value.final_prefix_gcd == modulus and proper_stages:
                    masked_stage_successes += 1

                for stage in value.stages:
                    if stage.rational_division_status == "unit":
                        rational_unit += 1
                        if (
                            stage.rational_division_quotient
                            != stage.quotient_residue
                            or stage.rational_numerator_gcd != stage.quotient_gcd
                        ):
                            unexplained += 1
                    elif stage.rational_division_status == "proper_factor":
                        rational_proper += 1
                        if not 1 < stage.intermediate_gcd < modulus:
                            unexplained += 1
                        if (
                            1 < stage.quotient_gcd < modulus
                            and stage.quotient_gcd != stage.intermediate_gcd
                        ):
                            different_proper_values += 1
                    else:
                        rational_full += 1
                        if (
                            stage.quotient_residue != stage.multiplier % modulus
                            or stage.quotient_gcd != stage.multiplier_gcd
                        ):
                            unexplained += 1

                    if stage.composed_division_status == "unit":
                        composed_unit += 1
                        if (
                            stage.composed_division_quotient
                            != stage.quotient_residue
                            or stage.endpoint_gcd != stage.quotient_gcd
                        ):
                            unexplained += 1
                    elif stage.composed_division_status == "proper_factor":
                        composed_proper += 1
                        if not 1 < stage.composed_denominator_gcd < modulus:
                            unexplained += 1
                    else:
                        composed_full += 1
                        if stage.quotient_gcd != stage.multiplier_gcd:
                            unexplained += 1
    if unexplained:
        raise AssertionError("iterated quotient reduction failed")

    different = evaluate_iterated_quotient(2, 15, (2, 2, 3))
    full = evaluate_iterated_quotient(2, 15, (4, 5, 2))
    result: dict[str, Any] = {
        "schema_version": "1.0.0",
        "parameters": {
            "factor_max": factor_max,
            "depth_max": depth_max,
            "modulus_max": modulus_max,
            "base_max": base_max,
        },
        "symbolic": {
            "chains": len(chains),
            "chain_identities": chain_identities,
            "stage_identities": stage_identities,
            "coefficient_checks": coefficient_checks,
            "maximum_prefix_exponent": maximum_prefix,
        },
        "modular": {
            "circuits": circuits,
            "stages": stages,
            "prefix_linkages": prefix_linkages,
            "residue_identities": residue_identities,
            "rational_unit": rational_unit,
            "rational_proper": rational_proper,
            "rational_full": rational_full,
            "composed_unit": composed_unit,
            "composed_proper": composed_proper,
            "composed_full": composed_full,
            "proper_final_products": proper_final_products,
            "masked_stage_successes": masked_stage_successes,
            "different_proper_values": different_proper_values,
            "unexplained": unexplained,
            "base_units": base_units,
            "base_nonunits": base_nonunits,
        },
        "named_different_factor": {
            "stage": 2,
            "intermediate_gcd": different.stages[1].intermediate_gcd,
            "quotient_gcd": different.stages[1].quotient_gcd,
            "numerator_gcd": different.stages[1].rational_numerator_gcd,
        },
        "named_full_intermediate": {
            "stage": 2,
            "intermediate_gcd": full.stages[1].intermediate_gcd,
            "inner_power": full.stages[1].inner_power_residue,
            "quotient_gcd": full.stages[1].quotient_gcd,
            "multiplier_gcd": full.stages[1].multiplier_gcd,
        },
    }
    result["summary_sha256"] = hashlib.sha256(canonical_json(result)).hexdigest()
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--factor-max", type=int, default=5)
    parser.add_argument("--depth-max", type=int, default=3)
    parser.add_argument("--modulus-max", type=int, default=128)
    parser.add_argument("--base-max", type=int, default=16)
    args = parser.parse_args()
    print(
        json.dumps(
            search(
                args.factor_max,
                args.depth_max,
                args.modulus_max,
                args.base_max,
            ),
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
