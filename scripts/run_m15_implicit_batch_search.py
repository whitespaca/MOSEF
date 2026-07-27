"""Audit the M15 leaf-materialized standard product-tree model."""

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
    batch_tree_multiplication_count,
    evaluate_batch_product,
    prime_factorization,
)


def canonical_json(value: Any) -> bytes:
    """Serialize a value deterministically for hashing."""
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def valuation(value: int, prime: int) -> int:
    """Return the exact prime-adic valuation of a nonzero integer."""
    if value == 0:
        return 1 << 60
    exponent = 0
    while value % prime == 0:
        value //= prime
        exponent += 1
    return exponent


def search(
    exponent_bound: int,
    modulus_max: int,
    base_max: int,
    tree_leaf_max: int,
) -> dict[str, Any]:
    """Run the registered deterministic finite batch audit."""
    if not 1 <= exponent_bound <= 14:
        raise ValueError("exponent_bound must lie in [1, 14]")
    if not 4 <= modulus_max <= 1024:
        raise ValueError("modulus_max must lie in [4, 1024]")
    if not 1 <= base_max <= 128:
        raise ValueError("base_max must lie in [1, 128]")
    if not 1 <= tree_leaf_max <= 1_000_000:
        raise ValueError("tree_leaf_max must lie in [1, 1000000]")

    subset_checks = 0
    valuation_component_checks = 0
    proper_root_batches = 0
    unit_root_batches = 0
    full_root_batches = 0
    batches_with_leaf_separator = 0
    masked_separator_batches = 0
    proper_root_implication_checks = 0
    unit_prechecks = 0
    proper_nonunit_prechecks = 0
    full_nonunit_prechecks = 0
    subset_count = 1 << exponent_bound

    for modulus in range(4, modulus_max + 1):
        factors = prime_factorization(modulus)
        for base in range(base_max + 1):
            base_gcd = math.gcd(base, modulus)
            if base_gcd != 1:
                if base_gcd == modulus:
                    full_nonunit_prechecks += 1
                else:
                    proper_nonunit_prechecks += 1
                continue
            unit_prechecks += 1
            leaves = [
                (pow(base, exponent, modulus) - 1) % modulus
                for exponent in range(1, exponent_bound + 1)
            ]
            leaf_gcds = [math.gcd(leaf, modulus) for leaf in leaves]
            leaf_valuations = [
                tuple(
                    min(multiplicity, valuation(pow(base, exponent) - 1, prime))
                    for prime, multiplicity in factors
                )
                for exponent in range(1, exponent_bound + 1)
            ]
            products = [1] * subset_count
            separator_flags = [False] * subset_count
            valuation_sums = [tuple(0 for _ in factors)] * subset_count
            for mask in range(1, subset_count):
                previous = mask & (mask - 1)
                bit = (mask ^ previous).bit_length() - 1
                products[mask] = products[previous] * leaves[bit] % modulus
                separator_flags[mask] = separator_flags[previous] or (
                    1 < leaf_gcds[bit] < modulus
                )
                valuation_sums[mask] = tuple(
                    min(
                        multiplicity,
                        valuation_sums[previous][index]
                        + leaf_valuations[bit][index],
                    )
                    for index, (_, multiplicity) in enumerate(factors)
                )
                predicted = math.prod(
                    prime**valuation_sums[mask][index]
                    for index, (prime, _) in enumerate(factors)
                )
                actual = math.gcd(products[mask], modulus)
                subset_checks += 1
                valuation_component_checks += len(factors)
                if actual != predicted:
                    raise AssertionError("capped valuation formula failed")
                if actual == 1:
                    unit_root_batches += 1
                elif actual == modulus:
                    full_root_batches += 1
                else:
                    proper_root_batches += 1
                    proper_root_implication_checks += 1
                    if not separator_flags[mask]:
                        raise AssertionError(
                            "proper root GCD had no proper leaf GCD"
                        )
                if separator_flags[mask]:
                    batches_with_leaf_separator += 1
                    if actual == modulus:
                        masked_separator_batches += 1

    tree_count_checks = 0
    for leaf_count in range(1, tree_leaf_max + 1):
        tree_count_checks += 1
        if batch_tree_multiplication_count(leaf_count) != leaf_count - 1:
            raise AssertionError("binary tree multiplication count failed")

    named = evaluate_batch_product(2, 21, (2, 3))
    if (
        named.leaf_residues != (3, 7)
        or named.leaf_gcds != (3, 7)
        or named.root_gcd != 21
    ):
        raise AssertionError("named aggregate-collision witness failed")

    result: dict[str, Any] = {
        "schema_version": "1.0.0",
        "parameters": {
            "exponent_bound": exponent_bound,
            "modulus_max": modulus_max,
            "base_max": base_max,
            "tree_leaf_max": tree_leaf_max,
        },
        "counts": {
            "subset_checks": subset_checks,
            "valuation_component_checks": valuation_component_checks,
            "proper_root_batches": proper_root_batches,
            "unit_root_batches": unit_root_batches,
            "full_root_batches": full_root_batches,
            "batches_with_leaf_separator": batches_with_leaf_separator,
            "masked_separator_batches": masked_separator_batches,
            "proper_root_implication_checks": proper_root_implication_checks,
            "unit_prechecks": unit_prechecks,
            "proper_nonunit_prechecks": proper_nonunit_prechecks,
            "full_nonunit_prechecks": full_nonunit_prechecks,
        },
        "tree": {
            "maximum_leaf_count": tree_leaf_max,
            "multiplication_count_checks": tree_count_checks,
            "maximum_multiplication_count": tree_leaf_max - 1,
        },
        "named_union_collision": {
            "base": 2,
            "modulus": 21,
            "exponents": [2, 3],
            "leaf_residues": list(named.leaf_residues),
            "leaf_gcds": list(named.leaf_gcds),
            "root_residue": named.root_residue,
            "root_gcd": named.root_gcd,
        },
    }
    result["summary_sha256"] = hashlib.sha256(canonical_json(result)).hexdigest()
    return result


def main() -> int:
    """Parse arguments, run the audit, and print deterministic JSON."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--exponent-bound", type=int, default=10)
    parser.add_argument("--modulus-max", type=int, default=256)
    parser.add_argument("--base-max", type=int, default=24)
    parser.add_argument("--tree-leaf-max", type=int, default=4096)
    args = parser.parse_args()
    result = search(
        args.exponent_bound,
        args.modulus_max,
        args.base_max,
        args.tree_leaf_max,
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
