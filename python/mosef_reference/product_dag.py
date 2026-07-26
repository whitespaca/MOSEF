"""Exact non-materializing product-DAG semantics for M16."""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd
from typing import Iterable


@dataclass(frozen=True)
class ProductGate:
    """One product gate whose parents are earlier atom or product nodes."""

    left: int
    right: int


@dataclass(frozen=True)
class ProductDagEvaluation:
    """Residues and formal atom multiplicities without unfolded leaves."""

    exponents: tuple[int, ...]
    modulus: int
    atom_residues: tuple[int, ...]
    atom_gcds: tuple[int, ...]
    gates: tuple[ProductGate, ...]
    node_residues: tuple[int, ...]
    node_gcds: tuple[int, ...]
    multiplicities: tuple[tuple[int, ...], ...]
    occurrence_counts: tuple[int, ...]

    @property
    def atom_count(self) -> int:
        """Return the number of explicitly evaluated exponent atoms."""
        return len(self.exponents)

    @property
    def gate_count(self) -> int:
        """Return the number of charged modular product gates."""
        return len(self.gates)

    @property
    def proper_atom_indices(self) -> tuple[int, ...]:
        """Return the atom indices whose individual GCDs are proper."""
        return tuple(
            index
            for index, divisor in enumerate(self.atom_gcds)
            if 1 < divisor < self.modulus
        )


def _normalized_exponents(exponents: Iterable[int]) -> tuple[int, ...]:
    """Validate and freeze the explicit atom exponent list."""
    normalized = tuple(exponents)
    if not normalized:
        raise ValueError("the atom exponent list must be nonempty")
    if any(
        isinstance(exponent, bool)
        or not isinstance(exponent, int)
        or exponent <= 0
        for exponent in normalized
    ):
        raise ValueError("atom exponents must be positive integers")
    if tuple(sorted(set(normalized))) != normalized:
        raise ValueError("atom exponents must be strictly increasing")
    return normalized


def _normalized_gates(gates: Iterable[ProductGate]) -> tuple[ProductGate, ...]:
    """Validate and freeze product-gate syntax."""
    normalized = tuple(gates)
    for gate in normalized:
        if not isinstance(gate, ProductGate):
            raise ValueError("every gate must be a ProductGate")
        if (
            isinstance(gate.left, bool)
            or not isinstance(gate.left, int)
            or isinstance(gate.right, bool)
            or not isinstance(gate.right, int)
        ):
            raise ValueError("gate parents must be integer node indices")
    return normalized


def evaluate_product_dag(
    base: int,
    modulus: int,
    exponents: Iterable[int],
    gates: Iterable[ProductGate],
) -> ProductDagEvaluation:
    """Evaluate explicit atoms and shared product gates modulo ``modulus``."""
    if isinstance(base, bool) or not isinstance(base, int):
        raise ValueError("base must be an integer")
    if isinstance(modulus, bool) or not isinstance(modulus, int) or modulus < 2:
        raise ValueError("modulus must be at least two")
    reduced_base = base % modulus
    if gcd(reduced_base, modulus) != 1:
        raise ValueError("base must be a unit modulo the modulus")
    normalized_exponents = _normalized_exponents(exponents)
    normalized_gates = _normalized_gates(gates)

    atom_residues = tuple(
        (pow(reduced_base, exponent, modulus) - 1) % modulus
        for exponent in normalized_exponents
    )
    atom_count = len(atom_residues)
    node_residues = list(atom_residues)
    multiplicities = [
        tuple(1 if atom == index else 0 for atom in range(atom_count))
        for index in range(atom_count)
    ]
    occurrence_counts = [1] * atom_count

    for gate_index, gate in enumerate(normalized_gates):
        available = atom_count + gate_index
        if (
            gate.left < 0
            or gate.right < 0
            or gate.left >= available
            or gate.right >= available
        ):
            raise ValueError("gate parents must be earlier nodes")
        node_residues.append(
            node_residues[gate.left] * node_residues[gate.right] % modulus
        )
        multiplicities.append(
            tuple(
                left + right
                for left, right in zip(
                    multiplicities[gate.left],
                    multiplicities[gate.right],
                    strict=True,
                )
            )
        )
        occurrence_counts.append(
            occurrence_counts[gate.left] + occurrence_counts[gate.right]
        )

    frozen_residues = tuple(node_residues)
    return ProductDagEvaluation(
        exponents=normalized_exponents,
        modulus=modulus,
        atom_residues=atom_residues,
        atom_gcds=tuple(gcd(residue, modulus) for residue in atom_residues),
        gates=normalized_gates,
        node_residues=frozen_residues,
        node_gcds=tuple(gcd(residue, modulus) for residue in frozen_residues),
        multiplicities=tuple(multiplicities),
        occurrence_counts=tuple(occurrence_counts),
    )


def maximum_unfolded_occurrences(gate_count: int) -> int:
    """Return the tight maximum unfolded occurrences after ``gate_count`` gates."""
    if (
        isinstance(gate_count, bool)
        or not isinstance(gate_count, int)
        or gate_count < 0
    ):
        raise ValueError("gate_count must be nonnegative")
    return 1 << gate_count


def repeated_product_program(
    atom_count: int,
    atom_index: int,
    gate_count: int,
) -> tuple[ProductGate, ...]:
    """Return repeated self-products attaining ``2**gate_count`` occurrences."""
    if (
        isinstance(atom_count, bool)
        or not isinstance(atom_count, int)
        or atom_count < 1
    ):
        raise ValueError("atom_count must be positive")
    if (
        isinstance(atom_index, bool)
        or not isinstance(atom_index, int)
        or not 0 <= atom_index < atom_count
    ):
        raise ValueError("atom_index must identify an atom")
    if (
        isinstance(gate_count, bool)
        or not isinstance(gate_count, int)
        or gate_count < 0
    ):
        raise ValueError("gate_count must be nonnegative")
    gates: list[ProductGate] = []
    previous = atom_index
    for step in range(gate_count):
        gates.append(ProductGate(previous, previous))
        previous = atom_count + step
    return tuple(gates)
