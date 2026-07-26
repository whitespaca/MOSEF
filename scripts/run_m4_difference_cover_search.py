"""Exhaustively falsify M4 divisor-cover and signature claims on a finite box."""

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

from mosef_reference import (  # noqa: E402
    CandidateKind,
    analyze_cover,
    evaluate_separator_candidate,
    has_distinct_order_separator_property,
    has_n_divisor_property,
    multiplicative_order_mod_prime,
    signature_count_lower_bound,
    square_difference_cover,
)


def canonical_json(value: Any) -> bytes:
    """Serialize a value deterministically for hashing."""
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def first_actual_collision(modulus_max: int, odd_only: bool) -> dict[str, int] | None:
    """Return the lexicographically first two-prime collision for candidate d=2."""
    for modulus in range(4, modulus_max + 1):
        if odd_only and modulus % 2 == 0:
            continue
        prime_divisors = [
            value
            for value in range(2, modulus + 1)
            if modulus % value == 0
            and all(value % divisor for divisor in range(2, math.isqrt(value) + 1))
        ]
        if len(prime_divisors) < 2:
            continue
        for base in range(2, modulus):
            if math.gcd(base, modulus) != 1:
                continue
            orders = tuple(
                multiplicative_order_mod_prime(base, prime)
                for prime in prime_divisors
            )
            if set(orders) == {1, 2} and evaluate_separator_candidate(
                modulus, base, 2
            ).kind == CandidateKind.SIMULTANEOUS_COLLISION:
                return {"n": modulus, "g": base, "d": 2}
    return None


def search(
    order_bound: int,
    candidate_max: int,
    modulus_max: int,
    construction_bound: int,
) -> dict[str, Any]:
    """Run the deterministic M4 search and return its exact summary."""
    if min(order_bound, candidate_max) < 2 or modulus_max < 6:
        raise ValueError("order_bound and candidate_max must be at least 2")
    if construction_bound < 1:
        raise ValueError("construction_bound must be positive")

    family_count = 0
    profile_checks = 0
    divisor_cover_count = 0
    noninjective_cover_count = 0
    injective_cover_count = 0
    smallest_cover_failure: dict[str, Any] | None = None

    universe = tuple(range(1, candidate_max + 1))
    for size in range(1, candidate_max + 1):
        for candidates in itertools.combinations(universe, size):
            family_count += 1
            signatures = []
            for order in range(1, order_bound + 1):
                signatures.append(
                    tuple(
                        index
                        for index, candidate in enumerate(candidates)
                        if candidate % order == 0
                    )
                )
            for left in range(1, order_bound + 1):
                for right in range(left + 1, order_bound + 1):
                    profile_checks += 1
                    analysis = analyze_cover(candidates, (left, right))
                    if analysis.separates_profile != (
                        signatures[left - 1] != signatures[right - 1]
                    ):
                        raise AssertionError((candidates, left, right))

            is_cover = all(signatures)
            is_injective = len(set(signatures)) == order_bound
            if is_cover:
                divisor_cover_count += 1
                if is_injective:
                    injective_cover_count += 1
                    if len(candidates) < signature_count_lower_bound(order_bound):
                        raise AssertionError(("counting bound", candidates))
                else:
                    noninjective_cover_count += 1
                    case = {
                        "candidates": list(candidates),
                        "equal_order_pair": next(
                            [left, right]
                            for left in range(1, order_bound + 1)
                            for right in range(left + 1, order_bound + 1)
                            if signatures[left - 1] == signatures[right - 1]
                        ),
                    }
                    if smallest_cover_failure is None:
                        smallest_cover_failure = case

    for bound in range(1, construction_bound + 1):
        _, _, candidates = square_difference_cover(bound)
        if not has_n_divisor_property(candidates, bound):
            raise AssertionError(("square cover", bound))
        if not has_distinct_order_separator_property(candidates, bound):
            raise AssertionError(("square separator", bound))

    summary: dict[str, Any] = {
        "bounds": {
            "order": [1, order_bound],
            "candidate": [1, candidate_max],
            "modulus": [4, modulus_max],
            "square_construction": [1, construction_bound],
        },
        "seed": None,
        "candidate_family_count": family_count,
        "two_order_profile_checks": profile_checks,
        "divisor_cover_count": divisor_cover_count,
        "noninjective_divisor_cover_count": noninjective_cover_count,
        "injective_divisor_cover_count": injective_cover_count,
        "smallest_divisor_cover_failure": smallest_cover_failure,
        "minimal_registered_difference_cover_failure": {
            "bound": 2,
            "left": [3],
            "right": [1],
            "candidates": [2],
            "equal_order_pair": [1, 2],
        },
        "smallest_actual_collision": first_actual_collision(modulus_max, False),
        "smallest_odd_actual_collision": first_actual_collision(modulus_max, True),
        "checked": {
            "signature_characterization": True,
            "signature_count_lower_bound": True,
            "square_difference_construction": True,
        },
    }
    summary["summary_sha256"] = hashlib.sha256(canonical_json(summary)).hexdigest()
    return summary


def main() -> int:
    """Command-line entry point."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--order-bound", type=int, default=8)
    parser.add_argument("--candidate-max", type=int, default=12)
    parser.add_argument("--modulus-max", type=int, default=200)
    parser.add_argument("--construction-bound", type=int, default=200)
    args = parser.parse_args()
    print(
        json.dumps(
            search(
                args.order_bound,
                args.candidate_max,
                args.modulus_max,
                args.construction_bound,
            ),
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
