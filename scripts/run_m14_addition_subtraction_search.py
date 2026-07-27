"""Audit the M14 same-base addition-subtraction representation."""

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

from mosef_reference import evaluate_addition_subtraction_program

SignedStep = tuple[int, int, int]


def canonical_json(value: Any) -> bytes:
    """Serialize a value deterministically for hashing."""
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def step_options(available: int) -> tuple[SignedStep, ...]:
    """Return every canonical product and oriented ratio from earlier nodes."""
    additions = tuple(
        (left, right, 1)
        for left, right in itertools.combinations_with_replacement(
            range(available),
            2,
        )
    )
    subtractions = tuple(
        (left, right, -1)
        for left in range(available)
        for right in range(available)
        if left != right
    )
    return additions + subtractions


def search(
    step_max: int,
    residue_step_max: int,
    modulus_max: int,
    base_max: int,
    exponent_max: int,
) -> dict[str, Any]:
    """Run the registered deterministic finite audit."""
    if not 1 <= step_max <= 6:
        raise ValueError("step_max must lie in [1, 6]")
    if not 0 <= residue_step_max <= step_max:
        raise ValueError("residue_step_max must lie in [0, step_max]")
    if not 4 <= modulus_max <= 2048:
        raise ValueError("modulus_max must lie in [4, 2048]")
    if not 1 <= base_max <= 128:
        raise ValueError("base_max must lie in [1, 128]")
    if not 1 <= exponent_max <= 256:
        raise ValueError("exponent_max must lie in [1, 256]")

    residue_cases = ((5, 77), (2, 105), (10, 143), (7, 561))
    options = {
        available: step_options(available)
        for available in range(1, step_max + 1)
    }
    programs_by_depth = [0] * (step_max + 1)
    programs_by_depth[0] = 1
    maximum_absolute_exponent = [1] + [0] * step_max
    node_growth_checks = 0
    residue_checks = 0
    negative_outputs = 0
    zero_outputs = 0
    zero_residue_checks = 0

    initial_residues = tuple((base % modulus,) for base, modulus in residue_cases)

    def visit(
        exponents: tuple[int, ...],
        residues_by_case: tuple[tuple[int, ...], ...] | None,
    ) -> None:
        nonlocal node_growth_checks
        nonlocal residue_checks
        nonlocal negative_outputs
        nonlocal zero_outputs
        nonlocal zero_residue_checks

        depth = len(exponents) - 1
        if depth == step_max:
            return
        available = depth + 1
        next_depth = depth + 1
        for left, right, sign in options[available]:
            exponent = exponents[left] + sign * exponents[right]
            node_growth_checks += 1
            programs_by_depth[next_depth] += 1
            maximum_absolute_exponent[next_depth] = max(
                maximum_absolute_exponent[next_depth],
                abs(exponent),
            )
            if abs(exponent) > 1 << next_depth:
                raise AssertionError("signed exponent growth bound failed")
            if exponent < 0:
                negative_outputs += 1
            elif exponent == 0:
                zero_outputs += 1

            next_residues: tuple[tuple[int, ...], ...] | None = None
            if next_depth <= residue_step_max:
                assert residues_by_case is not None
                built: list[tuple[int, ...]] = []
                for case_index, (base, modulus) in enumerate(residue_cases):
                    residues = residues_by_case[case_index]
                    right_residue = residues[right]
                    if sign == -1:
                        right_residue = pow(right_residue, -1, modulus)
                    residue = residues[left] * right_residue % modulus
                    expected = pow(base, exponent, modulus)
                    residue_checks += 1
                    if residue != expected:
                        raise AssertionError("signed modular semantics failed")
                    if exponent == 0:
                        zero_residue_checks += 1
                        if residue != 1:
                            raise AssertionError("zero exponent was not inert")
                    built.append((*residues, residue))
                next_residues = tuple(built)
            visit((*exponents, exponent), next_residues)

    visit((1,), initial_residues if residue_step_max else None)

    expected_programs = [1]
    product = 1
    for available in range(1, step_max + 1):
        product *= len(options[available])
        expected_programs.append(product)
    if programs_by_depth != expected_programs:
        raise AssertionError("program-prefix enumeration was incomplete")
    expected_maxima = [1 << depth for depth in range(step_max + 1)]
    if maximum_absolute_exponent != expected_maxima:
        raise AssertionError("repeated squaring did not attain every maximum")

    sign_symmetry_checks = 0
    unit_prechecks = 0
    proper_nonunit_prechecks = 0
    full_nonunit_prechecks = 0
    for modulus in range(4, modulus_max + 1):
        for base in range(base_max + 1):
            divisor = math.gcd(base, modulus)
            if divisor == 1:
                unit_prechecks += 1
                for exponent in range(1, exponent_max + 1):
                    positive = math.gcd(pow(base, exponent, modulus) - 1, modulus)
                    negative = math.gcd(pow(base, -exponent, modulus) - 1, modulus)
                    sign_symmetry_checks += 1
                    if positive != negative:
                        raise AssertionError("positive/negative GCD support differed")
            elif divisor == modulus:
                full_nonunit_prechecks += 1
            else:
                proper_nonunit_prechecks += 1

    named_program = (
        (0, 0, 1),
        (1, 0, -1),
        (0, 1, -1),
        (3, 3, 1),
        (2, 2, -1),
    )
    named_evaluation = evaluate_addition_subtraction_program(
        5,
        77,
        named_program,
    )
    result: dict[str, Any] = {
        "schema_version": "1.0.0",
        "parameters": {
            "step_max": step_max,
            "residue_step_max": residue_step_max,
            "modulus_max": modulus_max,
            "base_max": base_max,
            "exponent_max": exponent_max,
            "residue_cases": [list(case) for case in residue_cases],
        },
        "counts": {
            "node_growth_checks": node_growth_checks,
            "residue_checks": residue_checks,
            "sign_symmetry_checks": sign_symmetry_checks,
            "unit_prechecks": unit_prechecks,
            "proper_nonunit_prechecks": proper_nonunit_prechecks,
            "full_nonunit_prechecks": full_nonunit_prechecks,
            "negative_outputs": negative_outputs,
            "zero_outputs": zero_outputs,
            "zero_residue_checks": zero_residue_checks,
        },
        "programs_by_depth": programs_by_depth,
        "maximum_absolute_exponent": maximum_absolute_exponent,
        "named_cancellation_program": {
            "exponents": list(named_evaluation.exponents),
            "residues": list(named_evaluation.residues),
            "inversion_count": named_evaluation.inversion_count,
        },
    }
    result["summary_sha256"] = hashlib.sha256(canonical_json(result)).hexdigest()
    return result


def main() -> int:
    """Parse arguments, run the audit, and print deterministic JSON."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--step-max", type=int, default=6)
    parser.add_argument("--residue-step-max", type=int, default=5)
    parser.add_argument("--modulus-max", type=int, default=512)
    parser.add_argument("--base-max", type=int, default=32)
    parser.add_argument("--exponent-max", type=int, default=64)
    args = parser.parse_args()
    result = search(
        args.step_max,
        args.residue_step_max,
        args.modulus_max,
        args.base_max,
        args.exponent_max,
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
