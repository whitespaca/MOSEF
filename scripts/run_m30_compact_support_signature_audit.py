"""Deterministic M30 audit of multi-candidate compact support signatures."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from itertools import combinations, product
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
from mosef_reference import (
    balanced_prime_population,
    materialized_support_signature,
    minimum_candidate_count,
    minimum_signature_collision_count,
    phi4_compact_signature,
    phi4_prefix_signature_profile,
    signature_pair_accounting,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--assignment-candidate-max", type=int, default=3)
    parser.add_argument("--assignment-population-max", type=int, default=5)
    parser.add_argument("--input-length-min", type=int, default=9)
    parser.add_argument("--input-length-max", type=int, default=40)
    parser.add_argument("--pair-check-max", type=int, default=20)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if (
        args.assignment_candidate_max < 3
        or args.assignment_population_max < 5
        or args.input_length_min > 9
        or args.input_length_max < 40
        or args.pair_check_max < 20
    ):
        raise SystemExit("bounds do not cover the registered M30 audit")

    counts = {
        "signature_assignments": 0,
        "assignment_pair_checks": 0,
        "injectivity_equivalence_checks": 0,
        "collision_lower_bound_checks": 0,
        "coverage_lower_bound_checks": 0,
        "tight_collision_instances": 0,
        "materialized_witness_checks": 0,
        "prefix_input_lengths": 0,
        "prefix_prime_signatures": 0,
        "prefix_coordinate_checks": 0,
        "prefix_pair_formula_checks": 0,
        "prefix_explicit_pair_checks": 0,
        "prefix_pairs": 0,
        "prefix_separated_pairs": 0,
        "prefix_collision_pairs": 0,
        "failures": 0,
    }
    collision_extrema: list[dict[str, int]] = []

    for candidate_count in range(1, args.assignment_candidate_max + 1):
        signature_limit = 1 << candidate_count
        for population_size in range(2, args.assignment_population_max + 1):
            observed_minimum: int | None = None
            for signatures in product(
                range(signature_limit),
                repeat=population_size,
            ):
                profile = signature_pair_accounting(
                    signatures,
                    candidate_count,
                )
                direct_collision_count = sum(
                    first == second
                    for first, second in combinations(signatures, 2)
                )
                direct_separated_count = (
                    profile.pair_count - direct_collision_count
                )
                counts["signature_assignments"] += 1
                counts["assignment_pair_checks"] += profile.pair_count
                if (
                    profile.collision_pair_count != direct_collision_count
                    or profile.separated_pair_count != direct_separated_count
                    or profile.injective
                    != (direct_separated_count == profile.pair_count)
                ):
                    counts["failures"] += 1
                counts["injectivity_equivalence_checks"] += 1
                if (
                    profile.collision_pair_count
                    < profile.minimum_collision_pair_count
                ):
                    counts["failures"] += 1
                counts["collision_lower_bound_checks"] += 1
                if (
                    profile.covers_every_population_member
                    and candidate_count
                    < profile.coverage_candidate_lower_bound
                    and profile.injective
                ):
                    counts["failures"] += 1
                counts["coverage_lower_bound_checks"] += 1
                if (
                    observed_minimum is None
                    or profile.collision_pair_count < observed_minimum
                ):
                    observed_minimum = profile.collision_pair_count
            expected_minimum = minimum_signature_collision_count(
                population_size,
                candidate_count,
            )
            if observed_minimum != expected_minimum:
                counts["failures"] += 1
            counts["tight_collision_instances"] += 1
            collision_extrema.append(
                {
                    "candidate_count": candidate_count,
                    "population_size": population_size,
                    "minimum_collision_pair_count": expected_minimum,
                }
            )

    witness_candidates = (15, 7)
    witness_primes = (3, 5, 7)
    witness_signatures = tuple(
        materialized_support_signature(witness_candidates, prime)
        for prime in witness_primes
    )
    witness_profile = signature_pair_accounting(witness_signatures, 2)
    witness_modulus = witness_primes[0] * witness_primes[1]
    witness_gcds = tuple(
        math.gcd(candidate, witness_modulus)
        for candidate in witness_candidates
    )
    if (
        witness_signatures != (1, 1, 2)
        or witness_gcds != (15, 1)
        or not witness_profile.covers_every_population_member
        or witness_profile.injective
        or witness_profile.candidate_count
        != minimum_candidate_count(3, require_nonzero=True)
    ):
        counts["failures"] += 1
    counts["materialized_witness_checks"] += 5

    zero_signature_lengths: list[int] = []
    injective_lengths: list[int] = []
    prefix_selected: dict[str, Any] = {}
    largest_population: dict[str, Any] = {}
    best_separation: dict[str, Any] = {}
    for input_length in range(
        args.input_length_min,
        args.input_length_max + 1,
    ):
        profile = phi4_prefix_signature_profile(input_length)
        counts["prefix_input_lengths"] += 1
        counts["prefix_prime_signatures"] += profile.population_size
        counts["prefix_coordinate_checks"] += (
            profile.population_size * len(profile.candidate_levels)
        )
        counts["prefix_pairs"] += profile.pair_count
        counts["prefix_separated_pairs"] += profile.separated_pair_count
        counts["prefix_collision_pairs"] += profile.collision_pair_count
        if (
            profile.pair_count
            != profile.separated_pair_count + profile.collision_pair_count
            or profile.injective
            != (profile.collision_pair_count == 0)
            or profile.information_candidate_lower_bound
            > len(profile.candidate_levels)
        ):
            counts["failures"] += 1
        counts["prefix_pair_formula_checks"] += 1
        if profile.zero_signature_count == profile.population_size:
            zero_signature_lengths.append(input_length)
        if profile.injective:
            injective_lengths.append(input_length)

        if input_length <= args.pair_check_max:
            primes = balanced_prime_population(input_length)
            signatures = tuple(
                phi4_compact_signature(profile.candidate_levels, prime)
                for prime in primes
            )
            direct_separated = sum(
                first != second
                for first, second in combinations(signatures, 2)
            )
            if direct_separated != profile.separated_pair_count:
                counts["failures"] += 1
            counts["prefix_explicit_pair_checks"] += profile.pair_count

        if input_length in (9, 14, 40):
            prefix_selected[str(input_length)] = {
                "population_size": profile.population_size,
                "candidate_count": len(profile.candidate_levels),
                "distinct_signature_count": profile.distinct_signature_count,
                "zero_signature_count": profile.zero_signature_count,
                "covered_prime_count": profile.covered_prime_count,
                "separated_pair_count": profile.separated_pair_count,
                "collision_pair_count": profile.collision_pair_count,
            }
        if profile.population_size > int(
            largest_population.get("population_size", -1)
        ):
            largest_population = {
                "input_length": input_length,
                "population_size": profile.population_size,
                "candidate_count": len(profile.candidate_levels),
                "distinct_signature_count": profile.distinct_signature_count,
                "zero_signature_count": profile.zero_signature_count,
                "separated_pair_count": profile.separated_pair_count,
                "collision_pair_count": profile.collision_pair_count,
            }
        if (
            not best_separation
            or profile.separated_pair_count
            * int(best_separation["pair_count"])
            > int(best_separation["separated_pair_count"])
            * profile.pair_count
        ):
            best_separation = {
                "input_length": input_length,
                "pair_count": profile.pair_count,
                "separated_pair_count": profile.separated_pair_count,
                "collision_pair_count": profile.collision_pair_count,
            }

    expected_selected = {
        "9": {
            "population_size": 2,
            "candidate_count": 8,
            "distinct_signature_count": 1,
            "zero_signature_count": 2,
            "covered_prime_count": 0,
            "separated_pair_count": 0,
            "collision_pair_count": 1,
        },
        "14": {
            "population_size": 7,
            "candidate_count": 13,
            "distinct_signature_count": 2,
            "zero_signature_count": 6,
            "covered_prime_count": 1,
            "separated_pair_count": 6,
            "collision_pair_count": 15,
        },
        "40": {
            "population_size": 22_394,
            "candidate_count": 39,
            "distinct_signature_count": 1,
            "zero_signature_count": 22_394,
            "covered_prime_count": 0,
            "separated_pair_count": 0,
            "collision_pair_count": 250_734_421,
        },
    }
    expected_zero_lengths = [
        9,
        10,
        11,
        12,
        13,
        16,
        17,
        19,
        23,
        25,
        31,
        32,
        33,
        34,
        38,
        40,
    ]
    if (
        prefix_selected != expected_selected
        or zero_signature_lengths != expected_zero_lengths
        or injective_lengths
    ):
        counts["failures"] += 1

    if counts["failures"]:
        raise AssertionError("M30 compact support-signature audit failed")
    summary: dict[str, Any] = {
        "schema_version": "1.0.0",
        "parameters": vars(args),
        "counts": counts,
        "collision_extrema": collision_extrema,
        "materialized_coverage_counterexample": {
            "candidates": witness_candidates,
            "primes": witness_primes,
            "signatures": witness_signatures,
            "failed_pair": witness_modulus,
            "candidate_gcds": witness_gcds,
        },
        "prefix_zero_signature_lengths": zero_signature_lengths,
        "prefix_injective_lengths": injective_lengths,
        "prefix_selected": prefix_selected,
        "largest_population": largest_population,
        "best_separation": best_separation,
    }
    canonical = json.dumps(summary, sort_keys=True, separators=(",", ":"))
    summary["summary_sha256"] = hashlib.sha256(canonical.encode()).hexdigest()
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
