"""Exact input-length semantics for the M81 migration audit.

The public research parameter is the standard binary bit length

    bitlength(value) = floor(log2(value)) + 1

for every positive integer ``value``.  The legacy ``ceil(log2(value))``
quantity is retained only to characterize the former documentation defect.
All functions use integer arithmetic.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isqrt


@dataclass(frozen=True)
class LengthComparison:
    """Exact comparison between the standard and legacy length functions."""

    value: int
    standard_bit_length: int
    legacy_ceiling_log_length: int
    is_power_of_two: bool

    @property
    def discrepancy(self) -> int:
        """Return the standard length minus the legacy quantity."""

        return self.standard_bit_length - self.legacy_ceiling_log_length


def _positive_integer(value: int, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise ValueError(f"{name} must be a positive integer")
    return value


def standard_bit_length(value: int) -> int:
    """Return ``floor(log2(value)) + 1`` without floating point."""

    return _positive_integer(value, "value").bit_length()


def legacy_ceiling_log_length(value: int) -> int:
    """Return the former ``ceil(log2(value))`` repository quantity exactly."""

    return (_positive_integer(value, "value") - 1).bit_length()


def is_power_of_two(value: int) -> bool:
    """Return whether a positive integer is an exact power of two."""

    checked = _positive_integer(value, "value")
    return checked & (checked - 1) == 0


def compare_lengths(value: int) -> LengthComparison:
    """Return the exact standard/legacy comparison for one input."""

    return LengthComparison(
        value=value,
        standard_bit_length=standard_bit_length(value),
        legacy_ceiling_log_length=legacy_ceiling_log_length(value),
        is_power_of_two=is_power_of_two(value),
    )


def balanced_prime_interval(input_length: int) -> tuple[int, int]:
    """Return the integer endpoints of the balanced-prime population.

    A prime ``p`` is in the population exactly when
    ``2**(n-1) <= p*p < 2**n``.
    """

    checked = _positive_integer(input_length, "input_length")
    if checked < 4:
        raise ValueError("input_length must be at least four")
    lower = isqrt((1 << (checked - 1)) - 1) + 1
    upper = isqrt((1 << checked) - 1)
    return lower, upper


def is_prime(value: int) -> bool:
    """Exact deterministic trial-division predicate for audit-sized values."""

    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError("value must be an integer")
    if value < 2:
        return False
    if value % 2 == 0:
        return value == 2
    divisor = 3
    while divisor * divisor <= value:
        if value % divisor == 0:
            return False
        divisor += 2
    return True


def balanced_prime_population(input_length: int) -> tuple[int, ...]:
    """Enumerate the complete finite population used by selector certificates."""

    lower, upper = balanced_prime_interval(input_length)
    return tuple(value for value in range(lower, upper + 1) if is_prime(value))
