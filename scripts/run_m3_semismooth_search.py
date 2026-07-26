"""Falsify the M3 Las Vegas theorem and minimize a fixed-base collision."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

from mosef_reference import (  # noqa: E402
    factor_semismooth_oracle,
    factor_semismooth_promised,
    is_hereditarily_semismooth_asymmetric,
    is_hereditarily_semismooth_separable,
    is_prime,
    multiplicative_order_mod_prime,
    prime_factorization,
    semismooth_asymmetry_witnesses,
    stage_one_exponent,
    successful_residue_count,
)


def canonical_json(value: Any) -> bytes:
    """Serialize a value deterministically for hashing."""
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def find_naive_collision(n_max: int, smooth_bound_max: int) -> dict[str, int] | None:
    """Find the smallest fixed-base collision defeating ``q-1`` nondivisibility."""
    collisions: list[dict[str, int]] = []
    primes = [value for value in range(3, n_max + 1, 2) if is_prime(value)]
    for smooth_bound in range(1, smooth_bound_max + 1):
        exponent = stage_one_exponent(smooth_bound)
        for p in primes:
            if exponent % (p - 1) != 0:
                continue
            for q in primes:
                if q == p or p * q > n_max:
                    continue
                if exponent % (q - 1) == 0:
                    continue
                if pow(2, exponent, q) != 1:
                    continue
                n = p * q
                if math.gcd(pow(2, exponent, n) - 1, n) != n:
                    raise AssertionError("registered collision did not return n")
                collisions.append(
                    {
                        "n": n,
                        "p": min(p, q),
                        "q": max(p, q),
                        "smooth_bound": smooth_bound,
                        "exponent": exponent,
                        "order_mod_q": multiplicative_order_mod_prime(2, q),
                    }
                )
    return min(
        collisions,
        key=lambda item: (item["n"], item["smooth_bound"], item["p"], item["q"]),
        default=None,
    )


def search(
    n_max: int,
    base_bound: int,
    smooth_bound: int,
    cofactor_bound: int,
    collision_bound_max: int,
) -> dict[str, Any]:
    """Check both the theorem promise and the fixed-base boundary."""
    asymmetric_promised_inputs = 0
    asymmetric_completely_factored = 0
    smallest_asymmetric_promised: dict[str, Any] | None = None
    minimum_success: dict[str, Any] | None = None
    witness_nodes = 0
    for n in range(6, n_max + 1):
        witnesses = semismooth_asymmetry_witnesses(
            n,
            smooth_bound,
            cofactor_bound,
        )
        for witness in witnesses:
            witness_nodes += 1
            successful = successful_residue_count(n, witness.exponent)
            fraction = Fraction(successful, n)
            candidate = {
                "n": n,
                "p": witness.p,
                "q": witness.q,
                "multiplier": witness.multiplier,
                "exponent": witness.exponent,
                "successful_residues": successful,
                "total_residues": n,
                "success_fraction": (
                    f"{fraction.numerator}/{fraction.denominator}"
                ),
            }
            if minimum_success is None or Fraction(
                candidate["successful_residues"],
                candidate["total_residues"],
            ) < Fraction(
                minimum_success["successful_residues"],
                minimum_success["total_residues"],
            ):
                minimum_success = candidate
            if 12 * successful < 5 * n:
                raise AssertionError(
                    f"five-twelfths success bound failed for n={n}"
                )

    for n in range(4, n_max + 1):
        if is_prime(n):
            continue
        if not is_hereditarily_semismooth_asymmetric(
            n,
            smooth_bound,
            cofactor_bound,
        ):
            continue
        asymmetric_promised_inputs += 1
        factors = factor_semismooth_oracle(
            n,
            smooth_bound,
            cofactor_bound,
        )
        if factors is None or math.prod(factors) != n:
            raise AssertionError(f"asymmetric promised factorization failed for n={n}")
        asymmetric_completely_factored += 1
        if smallest_asymmetric_promised is None:
            smallest_asymmetric_promised = {
                "n": n,
                "factorization": [list(item) for item in prime_factorization(n)],
                "output": list(factors),
            }

    fixed_base_promised_inputs = 0
    fixed_base_completely_factored = 0
    smallest_fixed_base_promised: dict[str, Any] | None = None
    for n in range(4, n_max + 1):
        if is_prime(n):
            continue
        if not is_hereditarily_semismooth_separable(
            n,
            base_bound,
            smooth_bound,
            cofactor_bound,
        ):
            continue
        fixed_base_promised_inputs += 1
        factors = factor_semismooth_promised(
            n,
            base_bound,
            smooth_bound,
            cofactor_bound,
        )
        if factors is None or math.prod(factors) != n:
            raise AssertionError(f"promised factorization failed for n={n}")
        fixed_base_completely_factored += 1
        if smallest_fixed_base_promised is None:
            smallest_fixed_base_promised = {
                "n": n,
                "factorization": [list(item) for item in prime_factorization(n)],
                "output": list(factors),
            }

    collision = find_naive_collision(n_max, collision_bound_max)
    summary: dict[str, Any] = {
        "bounds": {
            "n": [4, n_max],
            "base_bound": base_bound,
            "smooth_bound": smooth_bound,
            "cofactor_bound": cofactor_bound,
            "naive_collision_smooth_bound_max": collision_bound_max,
        },
        "seed": None,
        "asymmetric_promise": {
            "promised_inputs": asymmetric_promised_inputs,
            "completely_factored_by_exhaustive_oracle": (
                asymmetric_completely_factored
            ),
            "smallest_promised_input": smallest_asymmetric_promised,
            "witness_nodes_checked": witness_nodes,
            "minimum_exact_success_probability": minimum_success,
        },
        "fixed_base_diagnostic": {
            "promised_inputs": fixed_base_promised_inputs,
            "completely_factored_promised_inputs": fixed_base_completely_factored,
            "smallest_promised_input": smallest_fixed_base_promised,
        },
        "smallest_naive_q_minus_one_collision": collision,
        "checked": {
            "all_asymmetric_promised_inputs_factored_in_search_box": (
                asymmetric_promised_inputs == asymmetric_completely_factored
            ),
            "five_twelfths_success_bound_holds_in_search_box": True,
            "all_fixed_base_promised_inputs_factored_in_search_box": (
                fixed_base_promised_inputs == fixed_base_completely_factored
            ),
            "naive_q_minus_one_condition_refuted_in_search_box": (
                collision is not None
            ),
        },
    }
    summary["summary_sha256"] = hashlib.sha256(canonical_json(summary)).hexdigest()
    return summary


def main() -> int:
    """Command-line entry point."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n-max", type=int, default=500)
    parser.add_argument("--base-bound", type=int, default=5)
    parser.add_argument("--smooth-bound", type=int, default=8)
    parser.add_argument("--cofactor-bound", type=int, default=3)
    parser.add_argument("--collision-bound-max", type=int, default=20)
    args = parser.parse_args()
    print(
        json.dumps(
            search(
                args.n_max,
                args.base_bound,
                args.smooth_bound,
                args.cofactor_bound,
                args.collision_bound_max,
            ),
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
