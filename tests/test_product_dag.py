"""Exact tests for the M16 non-materializing product-DAG model."""

from __future__ import annotations

import itertools
import math
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

from mosef_reference import (  # noqa: E402
    ProductGate,
    evaluate_product_dag,
    maximum_unfolded_occurrences,
    prime_factorization,
    repeated_product_program,
)
from scripts.run_m16_product_dag_search import search  # noqa: E402


def valuation(value: int, prime: int) -> int:
    """Return a valuation sentinel large enough for every test modulus."""
    if value == 0:
        return 1 << 60
    result = 0
    while value % prime == 0:
        value //= prime
        result += 1
    return result


class ProductDagTests(unittest.TestCase):
    def test_union_collision_uses_only_two_explicit_atoms(self) -> None:
        evaluation = evaluate_product_dag(
            2,
            21,
            (2, 3),
            (ProductGate(0, 1),),
        )
        self.assertEqual(evaluation.atom_residues, (3, 7))
        self.assertEqual(evaluation.atom_gcds, (3, 7))
        self.assertEqual(evaluation.node_residues, (3, 7, 0))
        self.assertEqual(evaluation.node_gcds, (3, 7, 21))
        self.assertEqual(evaluation.multiplicities, ((1, 0), (0, 1), (1, 1)))
        self.assertEqual(evaluation.occurrence_counts, (1, 1, 2))
        self.assertEqual(evaluation.proper_atom_indices, (0, 1))

    def test_compact_repetition_can_turn_prime_power_split_full(self) -> None:
        evaluation = evaluate_product_dag(
            4,
            9,
            (1,),
            repeated_product_program(1, 0, 5),
        )
        self.assertEqual(evaluation.atom_residues, (3,))
        self.assertEqual(evaluation.atom_gcds, (3,))
        self.assertEqual(evaluation.node_gcds[1], 9)
        self.assertEqual(evaluation.multiplicities[-1], (32,))
        self.assertEqual(evaluation.occurrence_counts[-1], 32)

    def test_tight_unfolded_occurrence_bound(self) -> None:
        for gate_count in range(10):
            evaluation = evaluate_product_dag(
                2,
                101,
                (1,),
                repeated_product_program(1, 0, gate_count),
            )
            self.assertEqual(
                evaluation.occurrence_counts[-1],
                maximum_unfolded_occurrences(gate_count),
            )

    def test_exact_formal_and_valuation_semantics(self) -> None:
        programs = (
            (),
            (ProductGate(0, 0),),
            (ProductGate(0, 1),),
            (ProductGate(0, 1), ProductGate(2, 2)),
        )
        for modulus in range(4, 80):
            factors = prime_factorization(modulus)
            for base in range(1, min(modulus, 12)):
                if math.gcd(base, modulus) != 1:
                    continue
                for exponents in ((1,), (1, 2)):
                    atoms = [pow(base, exponent) - 1 for exponent in exponents]
                    for gates in programs:
                        if any(
                            gate.left >= len(exponents) + index
                            or gate.right >= len(exponents) + index
                            for index, gate in enumerate(gates)
                        ):
                            continue
                        evaluation = evaluate_product_dag(
                            base,
                            modulus,
                            exponents,
                            gates,
                        )
                        for node_index, multiplicities in enumerate(
                            evaluation.multiplicities
                        ):
                            direct = math.prod(
                                pow(atom, multiplicity, modulus)
                                for atom, multiplicity in zip(
                                    atoms,
                                    multiplicities,
                                    strict=True,
                                )
                            ) % modulus
                            self.assertEqual(
                                evaluation.node_residues[node_index],
                                direct,
                            )
                            predicted = 1
                            for prime, exponent in factors:
                                total = sum(
                                    multiplicity * valuation(atom, prime)
                                    for atom, multiplicity in zip(
                                        atoms,
                                        multiplicities,
                                        strict=True,
                                    )
                                )
                                predicted *= prime ** min(exponent, total)
                            self.assertEqual(
                                evaluation.node_gcds[node_index],
                                predicted,
                            )
                            if 1 < predicted < modulus:
                                self.assertTrue(
                                    any(
                                        multiplicity > 0
                                        and 1 < atom_gcd < modulus
                                        for multiplicity, atom_gcd in zip(
                                            multiplicities,
                                            evaluation.atom_gcds,
                                            strict=True,
                                        )
                                    )
                                )

    def test_every_small_gate_syntax_obeys_occurrence_bound(self) -> None:
        for atom_count in range(1, 4):
            for first in itertools.combinations_with_replacement(
                range(atom_count),
                2,
            ):
                first_gate = ProductGate(*first)
                for second in itertools.combinations_with_replacement(
                    range(atom_count + 1),
                    2,
                ):
                    evaluation = evaluate_product_dag(
                        2,
                        101,
                        tuple(range(1, atom_count + 1)),
                        (first_gate, ProductGate(*second)),
                    )
                    for step, count in enumerate(
                        evaluation.occurrence_counts[atom_count:],
                        start=1,
                    ):
                        self.assertLessEqual(count, 1 << step)

    def test_invalid_domains_raise(self) -> None:
        invalid_calls = (
            lambda: evaluate_product_dag(2, 1, (1,), ()),
            lambda: evaluate_product_dag(True, 5, (1,), ()),
            lambda: evaluate_product_dag(5, 35, (1,), ()),
            lambda: evaluate_product_dag(2, 5, (), ()),
            lambda: evaluate_product_dag(2, 5, (0,), ()),
            lambda: evaluate_product_dag(2, 5, (True,), ()),
            lambda: evaluate_product_dag(2, 5, (2, 1), ()),
            lambda: evaluate_product_dag(2, 5, (1, 1), ()),
            lambda: evaluate_product_dag(2, 5, (1,), ((0, 0),)),
            lambda: evaluate_product_dag(
                2,
                5,
                (1,),
                (ProductGate(-1, 0),),
            ),
            lambda: evaluate_product_dag(
                2,
                5,
                (1,),
                (ProductGate(0, 1),),
            ),
            lambda: maximum_unfolded_occurrences(-1),
            lambda: maximum_unfolded_occurrences(True),
            lambda: repeated_product_program(0, 0, 1),
            lambda: repeated_product_program(1, -1, 1),
            lambda: repeated_product_program(1, 0, -1),
        )
        for invalid_call in invalid_calls:
            with self.subTest(invalid_call=invalid_call):
                with self.assertRaises(ValueError):
                    invalid_call()

    def test_registered_search_smoke(self) -> None:
        result = search(4, 2, 1, 48, 10)
        self.assertGreater(result["syntax"]["program_checks"], 0)
        self.assertGreater(result["residue"]["circuit_checks"], 0)
        self.assertGreater(result["residue"]["masked_success_nodes"], 0)
        self.assertEqual(len(result["summary_sha256"]), 64)


if __name__ == "__main__":
    unittest.main()
