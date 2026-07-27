"""Deterministic M28 audit of length-indexed materialized support."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
from mosef_reference import (
    balanced_prime_population,
    compact_exceptional_cofactor_residue,
    length_indexed_support_profile,
    phi4_compact_gap_profile,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-length-min", type=int, default=9)
    parser.add_argument("--input-length-max", type=int, default=18)
    parser.add_argument("--subset-prime-max", type=int, default=8)
    parser.add_argument("--gap-level-max", type=int, default=14)
    return parser.parse_args()


def exact_phi4_gap_cofactor(level: int) -> int:
    second_factor = (1 << level) + 3
    aggregate = 7 + (8**second_factor - 1) // 7
    if aggregate % 5 != 0:
        raise AssertionError("phi4 aggregate is not divisible by five")
    return aggregate // 5


def main() -> int:
    args = parse_args()
    if (
        args.input_length_min > 9
        or args.input_length_max < 18
        or args.subset_prime_max < 8
        or args.gap_level_max < 14
    ):
        raise SystemExit("bounds do not cover the registered M28 audit")
    counts = {
        "input_lengths": 0,
        "balanced_primes": 0,
        "balanced_pair_length_checks": 0,
        "schedule_profiles": 0,
        "materialized_support_bound_checks": 0,
        "pair_gcd_checks": 0,
        "forced_unit_pair_checks": 0,
        "proper_gcd_upper_bound_checks": 0,
        "phi4_gap_levels": 0,
        "phi4_exact_division_checks": 0,
        "phi4_exact_bit_lower_bound_checks": 0,
        "phi4_compact_residue_checks": 0,
        "failures": 0,
    }
    population_extrema: dict[str, int] = {
        "input_length": 0,
        "population_size": 0,
    }
    schedule_extrema: dict[str, int] = {
        "input_length": 0,
        "population_size": 0,
        "hit_prime_count": 0,
        "forced_miss_pair_count": 0,
        "materialized_bit_budget": 0,
    }
    for input_length in range(
        args.input_length_min,
        args.input_length_max + 1,
    ):
        primes = balanced_prime_population(input_length)
        if len(primes) < 2:
            counts["failures"] += 1
            continue
        counts["input_lengths"] += 1
        counts["balanced_primes"] += len(primes)
        if len(primes) > population_extrema["population_size"]:
            population_extrema = {
                "input_length": input_length,
                "population_size": len(primes),
            }
        for index, first_prime in enumerate(primes):
            for second_prime in primes[index + 1 :]:
                if (first_prime * second_prime).bit_length() != input_length:
                    counts["failures"] += 1
                counts["balanced_pair_length_checks"] += 1

        subset_primes = primes[: args.subset_prime_max]
        for mask in range(1 << len(subset_primes)):
            selected = tuple(
                prime
                for index, prime in enumerate(subset_primes)
                if mask & (1 << index)
            )
            product = math.prod(selected) if selected else 1
            value_lists = [(product,)]
            if selected:
                value_lists.append(tuple(-prime if index % 2 else prime for index, prime in enumerate(selected)))
            for charged_values in value_lists:
                profile = length_indexed_support_profile(
                    input_length,
                    primes,
                    charged_values,
                )
                counts["schedule_profiles"] += 1
                if (
                    profile.hit_prime_count
                    * profile.min_prime_log2_floor
                    > profile.materialized_bit_budget
                    or profile.hit_prime_count > profile.support_cap
                ):
                    counts["failures"] += 1
                counts["materialized_support_bound_checks"] += 1
                proper_pair_count = 0
                forced_unit_pair_count = 0
                missed = set(profile.missed_primes)
                for index, first_prime in enumerate(primes):
                    for second_prime in primes[index + 1 :]:
                        modulus = first_prime * second_prime
                        gcds = tuple(
                            math.gcd(abs(value), modulus)
                            for value in charged_values
                        )
                        if any(1 < divisor < modulus for divisor in gcds):
                            proper_pair_count += 1
                        if first_prime in missed and second_prime in missed:
                            if any(divisor != 1 for divisor in gcds):
                                counts["failures"] += 1
                            forced_unit_pair_count += 1
                        counts["pair_gcd_checks"] += len(charged_values)
                if forced_unit_pair_count != profile.forced_miss_pair_count:
                    counts["failures"] += 1
                counts["forced_unit_pair_checks"] += forced_unit_pair_count
                if proper_pair_count > profile.maximum_coverable_pair_count:
                    counts["failures"] += 1
                counts["proper_gcd_upper_bound_checks"] += 1
                rank = (
                    profile.forced_miss_pair_count,
                    profile.hit_prime_count,
                    profile.materialized_bit_budget,
                )
                current_rank = (
                    schedule_extrema["forced_miss_pair_count"],
                    schedule_extrema["hit_prime_count"],
                    schedule_extrema["materialized_bit_budget"],
                )
                if rank > current_rank:
                    schedule_extrema = {
                        "input_length": input_length,
                        "population_size": profile.population_size,
                        "hit_prime_count": profile.hit_prime_count,
                        "forced_miss_pair_count": profile.forced_miss_pair_count,
                        "materialized_bit_budget": profile.materialized_bit_budget,
                    }

    gap_extrema: dict[str, int] = {}
    for level in range(2, args.gap_level_max + 1):
        profile = phi4_compact_gap_profile(level)
        cofactor = exact_phi4_gap_cofactor(level)
        counts["phi4_gap_levels"] += 1
        if (
            (7 + (8**profile.second_factor - 1) // 7)
            != 5 * cofactor
        ):
            counts["failures"] += 1
        counts["phi4_exact_division_checks"] += 1
        if cofactor.bit_length() < profile.cofactor_bit_length_lower_bound:
            counts["failures"] += 1
        counts["phi4_exact_bit_lower_bound_checks"] += 1
        for modulus in (35, 77, 101, 125):
            compact = compact_exceptional_cofactor_residue(
                profile.base,
                modulus,
                profile.first_factor,
                profile.second_factor,
                profile.family,
            )
            if compact != cofactor % modulus:
                counts["failures"] += 1
            counts["phi4_compact_residue_checks"] += 1
        gap_extrema = {
            "level": level,
            "second_factor": profile.second_factor,
            "public_integer_bit_budget": profile.public_integer_bit_budget,
            "compact_count_bit_budget": profile.compact_count_bit_budget,
            "cofactor_degree": profile.cofactor_degree,
            "cofactor_bit_length": cofactor.bit_length(),
            "cofactor_bit_length_lower_bound": (
                profile.cofactor_bit_length_lower_bound
            ),
        }

    if counts["failures"]:
        raise AssertionError("M28 length-indexed support audit failed")
    summary: dict[str, Any] = {
        "schema_version": "1.0.0",
        "parameters": vars(args),
        "counts": counts,
        "population_extrema": population_extrema,
        "schedule_extrema": schedule_extrema,
        "phi4_gap_extrema": gap_extrema,
    }
    canonical = json.dumps(summary, sort_keys=True, separators=(",", ":"))
    summary["summary_sha256"] = hashlib.sha256(canonical.encode()).hexdigest()
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
