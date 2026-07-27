"""Exact same-base straight-line semantics for compressed exponents."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from math import gcd

MultiplicationStep = tuple[int, int]
SignedStep = tuple[int, int, int]


@dataclass(frozen=True)
class StraightLineEvaluation:
    """Formal exponents and modular residues for every program node."""

    exponents: tuple[int, ...]
    residues: tuple[int, ...]

    @property
    def multiplication_count(self) -> int:
        """Return the number of multiplication nodes."""
        return len(self.exponents) - 1


@dataclass(frozen=True)
class SignedStraightLineEvaluation:
    """Signed formal exponents and unit residues for every program node."""

    exponents: tuple[int, ...]
    residues: tuple[int, ...]
    inversion_count: int

    @property
    def node_count(self) -> int:
        """Return the number of charged addition-subtraction nodes."""
        return len(self.exponents) - 1


def _normalized_steps(
    steps: Iterable[MultiplicationStep],
) -> tuple[MultiplicationStep, ...]:
    """Validate and freeze a multiplication straight-line program."""
    normalized: list[MultiplicationStep] = []
    for node_index, step in enumerate(steps, start=1):
        if not isinstance(step, tuple) or len(step) != 2:
            raise ValueError("each step must be a pair of parent indices")
        left, right = step
        if (
            isinstance(left, bool)
            or isinstance(right, bool)
            or not isinstance(left, int)
            or not isinstance(right, int)
            or left < 0
            or right < 0
            or left >= node_index
            or right >= node_index
        ):
            raise ValueError("each parent must be an earlier node")
        normalized.append((left, right))
    return tuple(normalized)


def evaluate_multiplication_program(
    base: int,
    modulus: int,
    steps: Iterable[MultiplicationStep],
) -> StraightLineEvaluation:
    """Evaluate one factor-oblivious multiplication DAG from the node ``g``."""
    if isinstance(base, bool) or not isinstance(base, int):
        raise ValueError("base must be an integer")
    if isinstance(modulus, bool) or not isinstance(modulus, int) or modulus < 2:
        raise ValueError("modulus must be at least two")
    normalized = _normalized_steps(steps)
    exponents = [1]
    residues = [base % modulus]
    for left, right in normalized:
        exponents.append(exponents[left] + exponents[right])
        residues.append((residues[left] * residues[right]) % modulus)
    return StraightLineEvaluation(tuple(exponents), tuple(residues))


def _normalized_signed_steps(
    steps: Iterable[SignedStep],
) -> tuple[SignedStep, ...]:
    """Validate and freeze an addition-subtraction straight-line program."""
    normalized: list[SignedStep] = []
    for node_index, step in enumerate(steps, start=1):
        if not isinstance(step, tuple) or len(step) != 3:
            raise ValueError(
                "each signed step must contain two parents and a sign"
            )
        left, right, sign = step
        if (
            isinstance(left, bool)
            or isinstance(right, bool)
            or not isinstance(left, int)
            or not isinstance(right, int)
            or left < 0
            or right < 0
            or left >= node_index
            or right >= node_index
        ):
            raise ValueError("each parent must be an earlier node")
        if (
            isinstance(sign, bool)
            or not isinstance(sign, int)
            or sign not in (-1, 1)
        ):
            raise ValueError("each signed step sign must be -1 or 1")
        normalized.append((left, right, sign))
    return tuple(normalized)


def evaluate_addition_subtraction_program(
    base: int,
    modulus: int,
    steps: Iterable[SignedStep],
) -> SignedStraightLineEvaluation:
    """Evaluate a charged same-base addition-subtraction program.

    Sign ``1`` multiplies the two parent residues. Sign ``-1`` multiplies the
    left parent by the inverse of the right parent. The base must be a unit,
    so every requested inverse exists.
    """
    if isinstance(base, bool) or not isinstance(base, int):
        raise ValueError("base must be an integer")
    if isinstance(modulus, bool) or not isinstance(modulus, int) or modulus < 2:
        raise ValueError("modulus must be at least two")
    reduced_base = base % modulus
    if gcd(reduced_base, modulus) != 1:
        raise ValueError("base must be a unit modulo the modulus")
    normalized = _normalized_signed_steps(steps)
    exponents = [1]
    residues = [reduced_base]
    inversion_count = 0
    for left, right, sign in normalized:
        exponents.append(exponents[left] + sign * exponents[right])
        right_residue = residues[right]
        if sign == -1:
            right_residue = pow(right_residue, -1, modulus)
            inversion_count += 1
        residues.append((residues[left] * right_residue) % modulus)
    return SignedStraightLineEvaluation(
        tuple(exponents),
        tuple(residues),
        inversion_count,
    )


def absolute_exponent_support(exponents: Iterable[int]) -> tuple[int, ...]:
    """Return the sorted nonzero absolute exponents exposed by a program."""
    normalized: set[int] = set()
    for exponent in exponents:
        if isinstance(exponent, bool) or not isinstance(exponent, int):
            raise ValueError("exponents must be integers")
        if exponent:
            normalized.add(abs(exponent))
    return tuple(sorted(normalized))


def signed_exponent_lower_bound(exponent: int) -> int:
    """Return the node-growth lower bound for a nonzero signed exponent."""
    if isinstance(exponent, bool) or not isinstance(exponent, int) or exponent == 0:
        raise ValueError("exponent must be a nonzero integer")
    return (abs(exponent) - 1).bit_length()


def repeated_squaring_program(
    multiplication_count: int,
) -> tuple[MultiplicationStep, ...]:
    """Return the program attaining exponent ``2**multiplication_count``."""
    if (
        isinstance(multiplication_count, bool)
        or not isinstance(multiplication_count, int)
        or multiplication_count < 0
    ):
        raise ValueError("multiplication_count must be nonnegative")
    return tuple((index, index) for index in range(multiplication_count))


def generic_multiplication_lower_bound(exponent: int) -> int:
    """Return ``ceil(log2(exponent))``, the generic multiplication lower bound."""
    if isinstance(exponent, bool) or not isinstance(exponent, int) or exponent < 1:
        raise ValueError("exponent must be positive")
    return (exponent - 1).bit_length()


def tower_descriptor_exponent(level: int) -> int:
    """Interpret ``tower(level)`` as the exact exponent ``2**(2**level)``."""
    if isinstance(level, bool) or not isinstance(level, int) or level < 0:
        raise ValueError("level must be nonnegative")
    return 1 << (1 << level)
