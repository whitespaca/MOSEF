"""Exact small-input semantics for M4 divisor and separator covers."""

from __future__ import annotations

from dataclasses import dataclass
from math import isqrt


@dataclass(frozen=True)
class CoverAnalysis:
    """Exact divisibility analysis for one candidate family and order profile."""

    signatures: tuple[tuple[int, ...], ...]
    divisor_cover: bool
    separates_profile: bool
    distinct_signatures: bool


def positive_differences(
    left: tuple[int, ...] | list[int],
    right: tuple[int, ...] | list[int],
) -> tuple[int, ...]:
    """Return the distinct positive directed differences ``s - t``."""
    if not left or not right:
        raise ValueError("left and right must be nonempty")
    if any(value <= 0 for value in (*left, *right)):
        raise ValueError("difference-family entries must be positive")
    return tuple(
        sorted(
            {
                left_value - right_value
                for left_value in left
                for right_value in right
                if left_value > right_value
            }
        )
    )


def divisibility_signature(order: int, candidates: tuple[int, ...]) -> tuple[int, ...]:
    """Return the candidate indices divisible by ``order``."""
    if order <= 0 or not candidates or any(value <= 0 for value in candidates):
        raise ValueError("order and every candidate must be positive")
    return tuple(
        index for index, candidate in enumerate(candidates) if candidate % order == 0
    )


def analyze_cover(
    candidates: tuple[int, ...] | list[int],
    orders: tuple[int, ...] | list[int],
) -> CoverAnalysis:
    """Analyze coverage, direct separation, and signature injectivity."""
    normalized_candidates = tuple(sorted(set(candidates)))
    normalized_orders = tuple(orders)
    if not normalized_candidates or any(value <= 0 for value in normalized_candidates):
        raise ValueError("candidates must contain positive integers")
    if len(normalized_orders) < 2 or any(value <= 0 for value in normalized_orders):
        raise ValueError("orders must contain at least two positive integers")
    signatures = tuple(
        divisibility_signature(order, normalized_candidates)
        for order in normalized_orders
    )
    separates = any(
        0
        < sum(candidate % order == 0 for order in normalized_orders)
        < len(normalized_orders)
        for candidate in normalized_candidates
    )
    return CoverAnalysis(
        signatures=signatures,
        divisor_cover=all(signatures),
        separates_profile=separates,
        distinct_signatures=len(set(signatures)) == len(signatures),
    )


def has_n_divisor_property(candidates: tuple[int, ...], bound: int) -> bool:
    """Return whether every integer in ``[1,bound]`` divides a candidate."""
    if bound < 1:
        raise ValueError("bound must be positive")
    if not candidates or any(value <= 0 for value in candidates):
        raise ValueError("candidates must contain positive integers")
    return all(
        any(candidate % order == 0 for candidate in candidates)
        for order in range(1, bound + 1)
    )


def has_distinct_order_separator_property(
    candidates: tuple[int, ...],
    bound: int,
) -> bool:
    """Return whether signatures are injective on ``[1,bound]``."""
    if bound < 1:
        raise ValueError("bound must be positive")
    signatures = tuple(
        divisibility_signature(order, candidates) for order in range(1, bound + 1)
    )
    return len(set(signatures)) == bound


def square_difference_cover(
    bound: int,
) -> tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...]]:
    """Return the explicit square construction containing ``[1,bound]``."""
    if bound < 1:
        raise ValueError("bound must be positive")
    root = isqrt(bound)
    width = root if root * root == bound else root + 1
    left = tuple(1 + index * width for index in range(1, width + 1))
    right = tuple(1 + index for index in range(width))
    return left, right, positive_differences(left, right)


def signature_count_lower_bound(bound: int) -> int:
    """Return ``ceil(log2(bound + 1))`` without floating-point arithmetic."""
    if bound < 1:
        raise ValueError("bound must be positive")
    return bound.bit_length()
