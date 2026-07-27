"""Exact Galois-orbit classification for the M25 rational root ratio."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import gcd

from .rational_residue_audit import (
    cyclotomic_coefficients,
    monic_polynomial_divide,
)


@dataclass(frozen=True)
class RationalRootOrbitClassification:
    """Classify one cyclotomic order in the unequal depth-two model."""

    first_factor: int
    second_factor: int
    order: int
    category: str
    outside_stage_zeros: bool
    phase_order: int
    phase_divisible: bool
    rational_ratio: int | None
    primitive_first_coefficient: int | None
    primitive_second_coefficient: int | None
    common_step: int
    phi4_enabled: bool
    phi6_enabled: bool


@dataclass(frozen=True)
class RationalRootOrderDescriptor:
    """Compactly describe every rational order for fixed ``A`` and ``B``."""

    first_factor: int
    second_factor: int
    common_step: int
    phi4_enabled: bool
    phi6_enabled: bool


def _validate_inputs(first_factor: int, second_factor: int, order: int) -> None:
    for value, name, minimum in (
        (first_factor, "first_factor", 2),
        (second_factor, "second_factor", 2),
        (order, "order", 2),
    ):
        if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
            raise ValueError(f"{name} must be an integer at least {minimum}")
    if first_factor == second_factor:
        raise ValueError("factors must be unequal")


def rational_root_order_descriptor(
    first_factor: int, second_factor: int
) -> RationalRootOrderDescriptor:
    """Return a compact descriptor for every nonboundary rational order."""
    _validate_inputs(first_factor, second_factor, 2)
    return RationalRootOrderDescriptor(
        first_factor=first_factor,
        second_factor=second_factor,
        common_step=gcd(first_factor - 1, second_factor - 1),
        phi4_enabled=first_factor % 4 == 3 and second_factor % 4 == 3,
        phi6_enabled=first_factor % 6 == 5 and second_factor % 6 == 3,
    )


def classify_rational_root_orbit(
    first_factor: int, second_factor: int, order: int
) -> RationalRootOrbitClassification:
    """Apply the complete M25 rational-ratio classification theorem."""
    _validate_inputs(first_factor, second_factor, order)
    first_zero = first_factor % order == 0
    second_zero = (
        first_factor * second_factor % order == 0 and not first_zero
    )
    outside = not first_zero and not second_zero
    phase_order = first_factor * (second_factor - 2) + 1
    descriptor = rational_root_order_descriptor(first_factor, second_factor)

    category = "irrational"
    ratio: int | None = None
    coefficients: tuple[int, int] | None = None
    if not outside:
        category = "stage_zero"
    elif (
        (first_factor - 1) % order == 0
        and (second_factor - 1) % order == 0
    ):
        category = "common_step"
        ratio = -1
        coefficients = (-1, 1)
    elif order == 4 and descriptor.phi4_enabled:
        category = "phi4"
        ratio = 1
        coefficients = (1, 1)
    elif order == 6 and descriptor.phi6_enabled:
        category = "phi6"
        ratio = 2
        coefficients = (2, 1)

    return RationalRootOrbitClassification(
        first_factor=first_factor,
        second_factor=second_factor,
        order=order,
        category=category,
        outside_stage_zeros=outside,
        phase_order=phase_order,
        phase_divisible=phase_order % order == 0,
        rational_ratio=ratio,
        primitive_first_coefficient=(
            None if coefficients is None else coefficients[0]
        ),
        primitive_second_coefficient=(
            None if coefficients is None else coefficients[1]
        ),
        common_step=descriptor.common_step,
        phi4_enabled=descriptor.phi4_enabled,
        phi6_enabled=descriptor.phi6_enabled,
    )


def _geometric_coefficients(count: int, step: int = 1) -> tuple[int, ...]:
    result = [0] * (step * (count - 1) + 1)
    for index in range(count):
        result[step * index] = 1
    return tuple(result)


def _remainder(values: tuple[int, ...], order: int) -> tuple[int, ...]:
    return monic_polynomial_divide(
        values,
        cyclotomic_coefficients(order),
    )[1]


def exact_cyclotomic_root_ratio(
    first_factor: int, second_factor: int, order: int
) -> Fraction | None:
    """Return the exact rational ratio, or ``None`` if it is not rational.

    Stage-zero orders also return ``None`` because the M25 ratio is outside
    its domain there.
    """
    _validate_inputs(first_factor, second_factor, order)
    classification = classify_rational_root_orbit(
        first_factor,
        second_factor,
        order,
    )
    if not classification.outside_stage_zeros:
        return None
    first = _remainder(_geometric_coefficients(first_factor), order)
    second = _remainder(
        _geometric_coefficients(second_factor, first_factor),
        order,
    )
    width = max(len(first), len(second))
    first += (0,) * (width - len(first))
    second += (0,) * (width - len(second))
    candidate: Fraction | None = None
    for left, right in zip(first, second, strict=True):
        if left == 0:
            if right != 0:
                return None
            continue
        current = Fraction(-right, left)
        if candidate is None:
            candidate = current
        elif candidate != current:
            return None
    return candidate
