"""Exact-output support accounting for polynomially capped DEF-032 selectors."""

from __future__ import annotations

from dataclasses import dataclass

from .diversified_compact_signatures import ExceptionalSelectorDescriptor
from .exceptional_cofactor_schedule import exceptional_cofactor_overlap


@dataclass(frozen=True)
class DescriptorOutputBudget:
    """The eight positive exact primitive values and their charged bit budget."""

    descriptor: ExceptionalSelectorDescriptor
    values: tuple[int, ...]
    bit_budget: int
    selector_cap_upper_bound: int


def _geometric_sum(base: int, count: int) -> int:
    """Return ``1 + base + ... + base**(count - 1)`` exactly."""
    return int((pow(base, count) - 1) // (base - 1))


def exact_primitive_exit_integers(
    descriptor: ExceptionalSelectorDescriptor,
) -> tuple[int, ...]:
    """Materialize the eight public integers underlying one DEF-032 mask.

    This function is for proof and bounded audits.  The public factoring path
    retains the compact modular evaluators and does not materialize the large
    stage or cofactor integers.
    """
    if not isinstance(descriptor, ExceptionalSelectorDescriptor):
        raise ValueError("descriptor must be an ExceptionalSelectorDescriptor")

    first = descriptor.first_factor
    second = descriptor.second_factor
    base = descriptor.base
    first_stage = _geometric_sum(base, first)
    nested_base = pow(base, first)
    second_stage = _geometric_sum(nested_base, second)
    first_coefficient = 1 if descriptor.family == "phi4" else 2
    cyclotomic = (
        base * base + 1
        if descriptor.family == "phi4"
        else base * base - base + 1
    )
    aggregate = first_coefficient * first_stage + second_stage
    cofactor, remainder = divmod(aggregate, cyclotomic)
    if remainder or cofactor < 1:
        raise AssertionError("exceptional cofactor was not a positive integer")
    overlap_resultant = exceptional_cofactor_overlap(
        first,
        second,
        descriptor.family,
    ).cyclotomic_cofactor_resultant
    second_public_bound = (
        second if descriptor.family == "phi4" else 2 * second
    )
    values = (
        base,
        first_stage,
        second_stage,
        second,
        second_public_bound,
        cyclotomic,
        overlap_resultant,
        cofactor,
    )
    if any(value < 1 for value in values):
        raise AssertionError("DEF-032 primitive values must be positive")
    return values


def descriptor_bit_budget_upper_bound(selector_cap: int) -> int:
    """Return the uniform M47 bit bound for one valid capped descriptor."""
    if (
        isinstance(selector_cap, bool)
        or not isinstance(selector_cap, int)
        or selector_cap < 2
    ):
        raise ValueError("selector_cap must be an integer at least two")
    width = selector_cap.bit_length()
    return (
        2 * selector_cap * selector_cap * width
        + selector_cap * width
        + 9 * width
        + 5
    )


def selector_descriptor_count_upper_bound(selector_cap: int) -> int:
    """Return the DEF-032 family-agnostic descriptor-count upper bound."""
    if (
        isinstance(selector_cap, bool)
        or not isinstance(selector_cap, int)
        or selector_cap < 2
    ):
        raise ValueError("selector_cap must be an integer at least two")
    return 2 * (selector_cap - 1) ** 3


def selector_output_bit_budget_upper_bound(selector_cap: int) -> int:
    """Bound the total bit length of all eight exact primitive lifts."""
    return selector_descriptor_count_upper_bound(
        selector_cap
    ) * descriptor_bit_budget_upper_bound(selector_cap)


def descriptor_output_budget(
    descriptor: ExceptionalSelectorDescriptor,
    selector_cap: int,
) -> DescriptorOutputBudget:
    """Materialize one bounded audit record and verify the uniform bound."""
    if (
        max(
            descriptor.first_factor,
            descriptor.second_factor,
            descriptor.base,
        )
        > selector_cap
    ):
        raise ValueError("descriptor exceeds selector_cap")
    values = exact_primitive_exit_integers(descriptor)
    bit_budget = sum(value.bit_length() for value in values)
    upper_bound = descriptor_bit_budget_upper_bound(selector_cap)
    if bit_budget > upper_bound:
        raise AssertionError("descriptor exact-output bit bound failed")
    return DescriptorOutputBudget(
        descriptor=descriptor,
        values=values,
        bit_budget=bit_budget,
        selector_cap_upper_bound=upper_bound,
    )
