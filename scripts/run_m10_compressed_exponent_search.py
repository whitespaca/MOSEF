"""Exhaustively falsify the M10 multiplication straight-line growth barrier."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

from mosef_reference import (
    generic_multiplication_lower_bound,
    tower_descriptor_exponent,
)


def canonical_json(value: Any) -> bytes:
    """Serialize a value deterministically for hashing."""
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def search(step_max: int, descriptor_level_max: int) -> dict[str, Any]:
    """Enumerate every commutative program through ``step_max`` nodes."""
    if step_max < 1 or step_max > 8:
        raise ValueError("step_max must lie in [1, 8]")
    if descriptor_level_max < 1 or descriptor_level_max > 18:
        raise ValueError("descriptor_level_max must lie in [1, 18]")

    base = 7
    modulus = 1009
    exponents = [1]
    residues = [base % modulus]
    program_counts = [0] * (step_max + 1)
    maximum_exponents = [0] * (step_max + 1)
    unique_output_exponents = [set() for _ in range(step_max + 1)]
    node_growth_checks = 0
    residue_checks = 0

    def visit(depth: int) -> None:
        nonlocal node_growth_checks, residue_checks
        program_counts[depth] += 1
        output_exponent = exponents[-1]
        maximum_exponents[depth] = max(maximum_exponents[depth], output_exponent)
        unique_output_exponents[depth].add(output_exponent)
        if depth == step_max:
            return
        node_index = depth + 1
        for left in range(node_index):
            for right in range(left, node_index):
                exponent = exponents[left] + exponents[right]
                residue = residues[left] * residues[right] % modulus
                node_growth_checks += 1
                if exponent > 1 << node_index:
                    raise AssertionError(
                        ("exponent growth", node_index, left, right, exponent)
                    )
                residue_checks += 1
                if residue != pow(base, exponent, modulus):
                    raise AssertionError(
                        ("residue semantics", node_index, left, right, exponent)
                    )
                exponents.append(exponent)
                residues.append(residue)
                visit(depth + 1)
                residues.pop()
                exponents.pop()

    visit(0)
    expected_maxima = [1 << depth for depth in range(step_max + 1)]
    if maximum_exponents != expected_maxima:
        raise AssertionError(("maximum exponent sequence", maximum_exponents))

    descriptor_checks = 0
    descriptor_records: list[dict[str, int]] = []
    for level in range(descriptor_level_max + 1):
        exponent = tower_descriptor_exponent(level)
        required = 1 << level
        descriptor_checks += 1
        if generic_multiplication_lower_bound(exponent) != required:
            raise AssertionError(("descriptor lower bound", level))
        residue = base % modulus
        for _ in range(required):
            residue = residue * residue % modulus
        if residue != pow(base, exponent, modulus):
            raise AssertionError(("descriptor evaluation", level))
        descriptor_records.append(
            {
                "level": level,
                "exponent_bit_length": exponent.bit_length(),
                "required_multiplications": required,
            }
        )

    summary: dict[str, Any] = {
        "bounds": {
            "multiplication_count": [0, step_max],
            "descriptor_level": [0, descriptor_level_max],
        },
        "seed": None,
        "commutative_program_counts": program_counts,
        "maximum_exponents": maximum_exponents,
        "unique_output_exponent_counts": [
            len(values) for values in unique_output_exponents
        ],
        "node_growth_checks": node_growth_checks,
        "residue_checks": residue_checks,
        "descriptor_checks": descriptor_checks,
        "descriptor_records": descriptor_records,
        "checked": {
            "nodewise_exponent_growth": True,
            "direct_modular_residue_semantics": True,
            "repeated_squaring_tightness": True,
            "tower_descriptor_lower_bound": True,
            "tower_descriptor_repeated_squaring": True,
        },
    }
    summary["summary_sha256"] = hashlib.sha256(canonical_json(summary)).hexdigest()
    return summary


def main() -> int:
    """Command-line entry point."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--step-max", type=int, default=7)
    parser.add_argument("--descriptor-level-max", type=int, default=16)
    args = parser.parse_args()
    print(
        json.dumps(
            search(args.step_max, args.descriptor_level_max),
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
