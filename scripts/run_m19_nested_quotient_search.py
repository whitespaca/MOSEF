"""Audit the M19 cancellation-obscured nested geometric quotient."""

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

from mosef_reference import evaluate_nested_quotient


def canonical_json(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def search(
    exponent_max: int,
    modulus_max: int,
    base_max: int,
) -> dict[str, Any]:
    if not 1 <= exponent_max <= 32:
        raise ValueError("exponent_max must lie in [1, 32]")
    if not 4 <= modulus_max <= 256:
        raise ValueError("modulus_max must lie in [4, 256]")
    if not 1 <= base_max <= 32:
        raise ValueError("base_max must lie in [1, 32]")

    symbolic_identities = 0
    coefficient_checks = 0
    for inner_exponent in range(1, exponent_max + 1):
        for multiplier in range(1, exponent_max + 1):
            product = [0] * (inner_exponent * multiplier)
            for outer_index in range(multiplier):
                for inner_index in range(inner_exponent):
                    product[outer_index * inner_exponent + inner_index] += 1
            if product != [1] * (inner_exponent * multiplier):
                raise AssertionError("nested formal identity failed")
            symbolic_identities += 1
            coefficient_checks += len(product)

    circuits = 0
    residue_identities = 0
    rational_unit = 0
    rational_proper = 0
    rational_full = 0
    composed_unit = 0
    composed_proper = 0
    composed_full = 0
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
            for inner_exponent in range(1, exponent_max + 1):
                for multiplier in range(1, exponent_max + 1):
                    value = evaluate_nested_quotient(
                        base,
                        modulus,
                        inner_exponent,
                        multiplier,
                    )
                    circuits += 1
                    residue_identities += 2
                    if value.rational_division_status == "unit":
                        rational_unit += 1
                        if (
                            value.rational_division_quotient
                            != value.quotient_residue
                            or value.rational_numerator_gcd != value.quotient_gcd
                        ):
                            unexplained += 1
                    elif value.rational_division_status == "proper_factor":
                        rational_proper += 1
                        if not 1 < value.intermediate_gcd < modulus:
                            unexplained += 1
                        if (
                            1 < value.quotient_gcd < modulus
                            and value.quotient_gcd != value.intermediate_gcd
                        ):
                            different_proper_values += 1
                    else:
                        rational_full += 1
                        if (
                            value.quotient_residue != multiplier % modulus
                            or value.quotient_gcd != value.multiplier_gcd
                        ):
                            unexplained += 1

                    if value.composed_division_status == "unit":
                        composed_unit += 1
                        if (
                            value.composed_division_quotient
                            != value.quotient_residue
                            or value.endpoint_gcd != value.quotient_gcd
                        ):
                            unexplained += 1
                    elif value.composed_division_status == "proper_factor":
                        composed_proper += 1
                        if not 1 < value.composed_denominator_gcd < modulus:
                            unexplained += 1
                    else:
                        composed_full += 1
                        if value.quotient_gcd != value.multiplier_gcd:
                            unexplained += 1
    if unexplained:
        raise AssertionError("nested quotient reduction failed")

    named = evaluate_nested_quotient(2, 15, 2, 2)
    full = evaluate_nested_quotient(2, 15, 4, 5)
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
        },
        "modular": {
            "circuits": circuits,
            "residue_identities": residue_identities,
            "rational_unit": rational_unit,
            "rational_proper": rational_proper,
            "rational_full": rational_full,
            "composed_unit": composed_unit,
            "composed_proper": composed_proper,
            "composed_full": composed_full,
            "different_proper_values": different_proper_values,
            "unexplained": unexplained,
            "base_units": base_units,
            "base_nonunits": base_nonunits,
        },
        "named_different_factor": {
            "intermediate_gcd": named.intermediate_gcd,
            "quotient_gcd": named.quotient_gcd,
            "numerator_gcd": named.rational_numerator_gcd,
        },
        "named_full_intermediate": {
            "intermediate_gcd": full.intermediate_gcd,
            "inner_power": full.inner_power_residue,
            "quotient_gcd": full.quotient_gcd,
            "multiplier_gcd": full.multiplier_gcd,
        },
    }
    result["summary_sha256"] = hashlib.sha256(canonical_json(result)).hexdigest()
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--exponent-max", type=int, default=12)
    parser.add_argument("--modulus-max", type=int, default=128)
    parser.add_argument("--base-max", type=int, default=16)
    args = parser.parse_args()
    print(
        json.dumps(
            search(args.exponent_max, args.modulus_max, args.base_max),
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
