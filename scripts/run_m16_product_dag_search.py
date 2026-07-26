"""Audit the M16 non-materializing product-DAG model."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import sys
from collections.abc import Iterator
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

from mosef_reference import (  # noqa: E402
    ProductGate,
    evaluate_product_dag,
    prime_factorization,
    repeated_product_program,
)


def canonical_json(value: Any) -> bytes:
    """Serialize one result deterministically for hashing."""
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def product_programs(
    atom_count: int,
    gate_count: int,
) -> Iterator[tuple[ProductGate, ...]]:
    """Enumerate commutative product programs with exactly ``gate_count`` gates."""
    if gate_count == 0:
        yield ()
        return

    def extend(prefix: tuple[ProductGate, ...]) -> Iterator[tuple[ProductGate, ...]]:
        if len(prefix) == gate_count:
            yield prefix
            return
        available = atom_count + len(prefix)
        for left, right in itertools.combinations_with_replacement(
            range(available),
            2,
        ):
            yield from extend((*prefix, ProductGate(left, right)))

    yield from extend(())


def valuation(value: int, prime: int) -> int:
    """Return the exact prime-adic valuation of a nonzero integer."""
    if value == 0:
        return 1 << 60
    result = 0
    while value % prime == 0:
        value //= prime
        result += 1
    return result


def search(
    exponent_bound: int,
    program_step_max: int,
    residue_step_max: int,
    modulus_max: int,
    base_max: int,
) -> dict[str, Any]:
    """Run the registered deterministic product-DAG audit."""
    if not 1 <= exponent_bound <= 8:
        raise ValueError("exponent_bound must lie in [1, 8]")
    if not 0 <= program_step_max <= 6:
        raise ValueError("program_step_max must lie in [0, 6]")
    if not 0 <= residue_step_max <= 3:
        raise ValueError("residue_step_max must lie in [0, 3]")
    if not 4 <= modulus_max <= 512:
        raise ValueError("modulus_max must lie in [4, 512]")
    if not 1 <= base_max <= 64:
        raise ValueError("base_max must lie in [1, 64]")

    syntax_program_checks = 0
    syntax_gate_checks = 0
    maximum_occurrences = [0] * program_step_max
    for atom_count in range(1, 4):
        exponents = tuple(range(1, atom_count + 1))
        for gate_count in range(program_step_max + 1):
            for gates in product_programs(atom_count, gate_count):
                evaluation = evaluate_product_dag(2, 101, exponents, gates)
                syntax_program_checks += 1
                for gate_index, multiplicities in enumerate(
                    evaluation.multiplicities[atom_count:]
                ):
                    occurrence_count = sum(multiplicities)
                    syntax_gate_checks += 1
                    if occurrence_count != evaluation.occurrence_counts[
                        atom_count + gate_index
                    ]:
                        raise AssertionError("formal occurrence sum mismatch")
                    if occurrence_count > 1 << (gate_index + 1):
                        raise AssertionError("unfolded occurrence bound failed")
                    maximum_occurrences[gate_index] = max(
                        maximum_occurrences[gate_index],
                        occurrence_count,
                    )
    expected_maxima = [1 << step for step in range(1, program_step_max + 1)]
    if maximum_occurrences != expected_maxima:
        raise AssertionError("repeated self-product failed to attain every bound")

    circuit_checks = 0
    node_semantics_checks = 0
    valuation_component_checks = 0
    proper_node_implication_checks = 0
    masked_success_nodes = 0
    unit_prechecks = 0
    proper_nonunit_prechecks = 0
    full_nonunit_prechecks = 0

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
            for atom_count in range(1, min(3, exponent_bound) + 1):
                for exponents in itertools.combinations(
                    range(1, exponent_bound + 1),
                    atom_count,
                ):
                    integer_atoms = tuple(
                        pow(base, exponent) - 1 for exponent in exponents
                    )
                    for gate_count in range(residue_step_max + 1):
                        for gates in product_programs(atom_count, gate_count):
                            evaluation = evaluate_product_dag(
                                base,
                                modulus,
                                exponents,
                                gates,
                            )
                            circuit_checks += 1
                            proper_atom_flags = tuple(
                                1 < divisor < modulus
                                for divisor in evaluation.atom_gcds
                            )
                            for node_index, multiplicities in enumerate(
                                evaluation.multiplicities
                            ):
                                has_proper_used_atom = any(
                                    multiplicity > 0 and is_proper
                                    for multiplicity, is_proper in zip(
                                        multiplicities,
                                        proper_atom_flags,
                                        strict=True,
                                    )
                                )
                                direct = math.prod(
                                    pow(atom, multiplicity, modulus)
                                    for atom, multiplicity in zip(
                                        integer_atoms,
                                        multiplicities,
                                        strict=True,
                                    )
                                ) % modulus
                                node_semantics_checks += 1
                                if direct != evaluation.node_residues[node_index]:
                                    raise AssertionError(
                                        "formal product residue semantics failed"
                                    )
                                predicted = 1
                                for prime, exponent in factors:
                                    total = sum(
                                        multiplicity * valuation(atom, prime)
                                        for atom, multiplicity in zip(
                                            integer_atoms,
                                            multiplicities,
                                            strict=True,
                                        )
                                    )
                                    predicted *= prime ** min(exponent, total)
                                    valuation_component_checks += 1
                                actual = evaluation.node_gcds[node_index]
                                if actual != predicted:
                                    raise AssertionError(
                                        "formal product valuation semantics failed"
                                    )
                                if 1 < actual < modulus:
                                    proper_node_implication_checks += 1
                                    if not has_proper_used_atom:
                                        raise AssertionError(
                                            "proper product node had no proper used atom"
                                        )
                                if (
                                    node_index >= atom_count
                                    and has_proper_used_atom
                                    and actual == modulus
                                ):
                                    masked_success_nodes += 1

    union_collision = evaluate_product_dag(
        2,
        21,
        (2, 3),
        (ProductGate(0, 1),),
    )
    if (
        union_collision.atom_gcds != (3, 7)
        or union_collision.node_gcds[-1] != 21
    ):
        raise AssertionError("named union collision failed")
    repeated_collision = evaluate_product_dag(
        4,
        9,
        (1,),
        repeated_product_program(1, 0, 5),
    )
    if (
        repeated_collision.atom_gcds != (3,)
        or repeated_collision.node_gcds[1] != 9
        or repeated_collision.occurrence_counts[-1] != 32
    ):
        raise AssertionError("named repeated prime-power collision failed")

    result: dict[str, Any] = {
        "schema_version": "1.0.0",
        "parameters": {
            "exponent_bound": exponent_bound,
            "program_step_max": program_step_max,
            "residue_step_max": residue_step_max,
            "modulus_max": modulus_max,
            "base_max": base_max,
        },
        "syntax": {
            "program_checks": syntax_program_checks,
            "gate_checks": syntax_gate_checks,
            "maximum_occurrences_by_gate": maximum_occurrences,
        },
        "residue": {
            "circuit_checks": circuit_checks,
            "node_semantics_checks": node_semantics_checks,
            "valuation_component_checks": valuation_component_checks,
            "proper_node_implication_checks": proper_node_implication_checks,
            "masked_success_nodes": masked_success_nodes,
            "unit_prechecks": unit_prechecks,
            "proper_nonunit_prechecks": proper_nonunit_prechecks,
            "full_nonunit_prechecks": full_nonunit_prechecks,
        },
        "named_union_collision": {
            "base": 2,
            "modulus": 21,
            "exponents": [2, 3],
            "atom_gcds": list(union_collision.atom_gcds),
            "root_gcd": union_collision.node_gcds[-1],
        },
        "named_repeated_collision": {
            "base": 4,
            "modulus": 9,
            "exponents": [1],
            "atom_gcd": repeated_collision.atom_gcds[0],
            "first_product_gcd": repeated_collision.node_gcds[1],
            "final_occurrences": repeated_collision.occurrence_counts[-1],
        },
    }
    result["summary_sha256"] = hashlib.sha256(canonical_json(result)).hexdigest()
    return result


def main() -> int:
    """Parse arguments, run the audit, and print deterministic JSON."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--exponent-bound", type=int, default=4)
    parser.add_argument("--program-step-max", type=int, default=5)
    parser.add_argument("--residue-step-max", type=int, default=2)
    parser.add_argument("--modulus-max", type=int, default=128)
    parser.add_argument("--base-max", type=int, default=16)
    args = parser.parse_args()
    result = search(
        args.exponent_bound,
        args.program_step_max,
        args.residue_step_max,
        args.modulus_max,
        args.base_max,
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
