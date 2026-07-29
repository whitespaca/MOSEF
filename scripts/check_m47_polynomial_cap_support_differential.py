"""Independently validate the M47 exact-output and source inequalities."""

from __future__ import annotations

import hashlib
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "python")]

from mosef_reference import (
    ExceptionalSelectorDescriptor,
    diversified_exceptional_selector,
    exact_primitive_exit_integers,
    exceptional_cofactor_coefficients,
    primitive_exit_mask,
)

SCHEMA = ROOT / "schemas/m47-polynomial-cap-support-v1.json"


def _independent_values(
    descriptor: ExceptionalSelectorDescriptor,
) -> tuple[int, ...]:
    first = descriptor.first_factor
    second = descriptor.second_factor
    base = descriptor.base
    first_stage = sum(pow(base, index) for index in range(first))
    second_stage = sum(
        pow(base, first * index) for index in range(second)
    )
    cyclotomic = (
        base * base + 1
        if descriptor.family == "phi4"
        else base * base - base + 1
    )
    coefficients = exceptional_cofactor_coefficients(
        first,
        second,
        descriptor.family,
    )
    cofactor = sum(
        coefficient * pow(base, exponent)
        for exponent, coefficient in enumerate(coefficients)
    )
    if descriptor.family == "phi4":
        constant = (first * (second + 2) + 1) // 4
        linear = (first * (second - 2) + 1) // 4
        resultant = constant * constant + linear * linear
        second_public_bound = second
    else:
        residual = first * (second - 2) + 1
        constant = -(2 * residual // 3)
        linear = (first * (second + 4) + 4) // 3
        resultant = (
            constant * constant
            + constant * linear
            + linear * linear
        )
        second_public_bound = 2 * second
    return (
        base,
        first_stage,
        second_stage,
        second,
        second_public_bound,
        cyclotomic,
        resultant,
        cofactor,
    )


def _sieve(limit: int) -> tuple[int, ...]:
    flags = bytearray(b"\x01") * (limit + 1)
    flags[:2] = b"\x00\x00"
    for prime in range(2, math.isqrt(limit) + 1):
        if flags[prime]:
            start = prime * prime
            flags[start : limit + 1 : prime] = b"\x00" * (
                (limit - start) // prime + 1
            )
    return tuple(index for index, flag in enumerate(flags) if flag)


def _population_count(primes: tuple[int, ...], input_length: int) -> int:
    lower_square = 1 << (input_length - 1)
    upper_square = 1 << input_length
    return sum(
        lower_square <= prime * prime < upper_square for prime in primes
    )


def main() -> int:
    """Check exact lifts, branch masks, bounds, and prime-count arithmetic."""
    data = json.loads(SCHEMA.read_text(encoding="utf-8"))
    canonical = dict(data)
    expected_hash = canonical.pop("summary_sha256")
    actual_hash = hashlib.sha256(
        json.dumps(canonical, sort_keys=True, separators=(",", ":")).encode(
            "utf-8"
        )
    ).hexdigest()
    if actual_hash != expected_hash:
        raise AssertionError("M47 canonical summary hash changed")

    descriptor_checks = 0
    exact_value_checks = 0
    for profile in data["cap_profiles"]:
        cap = int(profile["selector_cap"])
        descriptors = diversified_exceptional_selector(9, cap)
        exact_budget = 0
        maximum_budget = 0
        for descriptor in descriptors:
            expected_values = _independent_values(descriptor)
            actual_values = exact_primitive_exit_integers(descriptor)
            if actual_values != expected_values:
                raise AssertionError(
                    f"M47 exact lift disagreement: {descriptor.key}"
                )
            bit_budget = sum(value.bit_length() for value in expected_values)
            exact_budget += bit_budget
            maximum_budget = max(maximum_budget, bit_budget)
            descriptor_checks += 1
            exact_value_checks += len(expected_values)
        if len(descriptors) != profile["descriptor_count"]:
            raise AssertionError("M47 descriptor count changed")
        if exact_budget != profile["exact_output_bit_budget"]:
            raise AssertionError("M47 exact output budget changed")
        if maximum_budget != profile["maximum_descriptor_bit_budget"]:
            raise AssertionError("M47 maximum descriptor budget changed")
        if exact_budget > profile["selector_output_bit_upper_bound"]:
            raise AssertionError("M47 selector bound failed independently")

    support_primes = tuple(prime for prime in _sieve(199) if prime >= 2)
    support_checks = 0
    for descriptor in diversified_exceptional_selector(9, 20):
        values = _independent_values(descriptor)
        for prime in support_primes:
            expected_mask = (
                1
                if values[0] % prime == 0
                else sum(
                    1 << index
                    for index, value in enumerate(values)
                    if index and value % prime == 0
                )
            )
            if primitive_exit_mask(descriptor, prime) != expected_mask:
                raise AssertionError(
                    f"M47 branch-mask disagreement: "
                    f"{descriptor.key}, p={prime}"
                )
            support_checks += 1

    margin = 128 * 50000**2 - 81 * 62753**2
    if margin != data["source_inequality"]["integer_square_margin"]:
        raise AssertionError("M47 source inequality changed")
    primes = _sieve(1 << 20)
    population_checks = 0
    registered = {
        int(record["input_length"]): record
        for record in data["population_checks"]
    }
    for input_length in range(10, 41):
        count = _population_count(primes, input_length)
        upper = 2.0 ** (input_length / 2)
        lower_floor = math.floor(upper / (81 * math.log(upper)))
        if count <= lower_floor:
            raise AssertionError("M47 balanced lower bound failed")
        if input_length in registered:
            if count != registered[input_length]["balanced_prime_count"]:
                raise AssertionError("M47 registered population changed")
            if (
                lower_floor
                != registered[input_length]["strict_lower_bound_floor"]
            ):
                raise AssertionError("M47 registered lower floor changed")
        population_checks += 1

    print(
        "M47 polynomial-cap support differential validation: PASS "
        f"({descriptor_checks} descriptor checks, "
        f"{exact_value_checks} exact-value checks, "
        f"{support_checks} branch-support checks, "
        f"{population_checks} independent population checks)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
