"""Deterministic M29 audit of compact Phi4 cofactor prime support."""

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
    is_prime,
    phi4_balanced_support_profile,
    phi4_pair_outcome,
    phi4_prime_divisibility_profile,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--level-min", type=int, default=2)
    parser.add_argument("--level-max", type=int, default=24)
    parser.add_argument("--prime-max", type=int, default=20_000)
    parser.add_argument("--input-length-min", type=int, default=9)
    parser.add_argument("--input-length-max", type=int, default=40)
    parser.add_argument("--pair-check-max", type=int, default=20)
    parser.add_argument("--exact-level-max", type=int, default=14)
    return parser.parse_args()


def exact_phi4_cofactor(level: int) -> int:
    second_factor = (1 << level) + 3
    return (8**second_factor + 48) // 35


def main() -> int:
    args = parse_args()
    if (
        args.level_min > 2
        or args.level_max < 24
        or args.prime_max < 20_000
        or args.input_length_min > 9
        or args.input_length_max < 40
        or args.pair_check_max < 20
        or args.exact_level_max < 14
    ):
        raise SystemExit("bounds do not cover the registered M29 audit")

    counts = {
        "levels": 0,
        "prime_candidates": 0,
        "generic_congruence_checks": 0,
        "small_prime_quotient_checks": 0,
        "consecutive_support_checks": 0,
        "exact_closed_form_checks": 0,
        "exact_consecutive_gcd_checks": 0,
        "balanced_input_lengths": 0,
        "balanced_primes": 0,
        "balanced_support_hits": 0,
        "balanced_cut_formula_checks": 0,
        "balanced_pair_outcome_checks": 0,
        "balanced_proper_outcomes": 0,
        "balanced_full_collisions": 0,
        "balanced_unit_outcomes": 0,
        "registered_outcome_witnesses": 0,
        "failures": 0,
    }
    primes = tuple(prime for prime in range(2, args.prime_max + 1) if is_prime(prime))
    previous_hits: set[int] | None = None
    prime_support_extrema: dict[str, Any] = {}

    for level in range(args.level_min, args.level_max + 1):
        counts["levels"] += 1
        hits: list[int] = []
        for prime in primes:
            profile = phi4_prime_divisibility_profile(level, prime)
            counts["prime_candidates"] += 1
            compact = compact_exceptional_cofactor_residue(
                2,
                prime,
                3,
                (1 << level) + 3,
                "phi4",
            )
            if (compact == 0) != profile.divides:
                counts["failures"] += 1
            if prime in (2, 3, 5, 7):
                counts["small_prime_quotient_checks"] += 1
            else:
                expected = pow(2, 3 * (1 << level) + 5, prime) == prime - 3
                if profile.divides != expected:
                    counts["failures"] += 1
                counts["generic_congruence_checks"] += 1
            if profile.divides:
                hits.append(prime)
        hit_set = set(hits)
        if previous_hits is not None:
            shared_odd = (previous_hits & hit_set) - {2}
            if shared_odd:
                counts["failures"] += 1
            counts["consecutive_support_checks"] += len(primes) - 1
        previous_hits = hit_set
        if len(hits) > int(prime_support_extrema.get("hit_count", -1)):
            prime_support_extrema = {
                "level": level,
                "hit_count": len(hits),
                "hit_primes": hits,
            }

    for level in range(args.level_min, args.exact_level_max + 1):
        cofactor = exact_phi4_cofactor(level)
        exponent = 3 * (1 << level) + 5
        if cofactor != 16 * ((1 << exponent) + 3) // 35:
            counts["failures"] += 1
        counts["exact_closed_form_checks"] += 1
        if math.gcd(cofactor, exact_phi4_cofactor(level + 1)) != 16:
            counts["failures"] += 1
        counts["exact_consecutive_gcd_checks"] += 1

    balanced_extrema: dict[str, Any] = {}
    for input_length in range(
        args.input_length_min,
        args.input_length_max + 1,
    ):
        profile = phi4_balanced_support_profile(input_length)
        counts["balanced_input_lengths"] += 1
        counts["balanced_primes"] += profile.population_size
        counts["balanced_support_hits"] += profile.hit_prime_count
        if (
            profile.pair_count
            != profile.proper_pair_count
            + profile.full_collision_pair_count
            + profile.unit_pair_count
            or profile.proper_pair_count
            != profile.hit_prime_count
            * (profile.population_size - profile.hit_prime_count)
            or profile.proper_pair_count > profile.maximum_proper_pair_count
            or (
                profile.population_size >= 3
                and profile.universal_pair_coverage_possible
            )
        ):
            counts["failures"] += 1
        counts["balanced_cut_formula_checks"] += 1

        primes_at_length = balanced_prime_population(input_length)
        if input_length <= args.pair_check_max:
            observed = {
                "proper_factor": 0,
                "full_collision": 0,
                "unit": 0,
            }
            for index, first_prime in enumerate(primes_at_length):
                for second_prime in primes_at_length[index + 1 :]:
                    outcome = phi4_pair_outcome(
                        input_length,
                        first_prime,
                        second_prime,
                    )
                    observed[outcome.status] += 1
                    counts["balanced_pair_outcome_checks"] += 1
            if (
                observed["proper_factor"] != profile.proper_pair_count
                or observed["full_collision"]
                != profile.full_collision_pair_count
                or observed["unit"] != profile.unit_pair_count
            ):
                counts["failures"] += 1
            counts["balanced_proper_outcomes"] += observed["proper_factor"]
            counts["balanced_full_collisions"] += observed["full_collision"]
            counts["balanced_unit_outcomes"] += observed["unit"]
        if profile.population_size > int(
            balanced_extrema.get("population_size", -1)
        ):
            balanced_extrema = {
                "input_length": input_length,
                "population_size": profile.population_size,
                "hit_prime_count": profile.hit_prime_count,
                "proper_pair_count": profile.proper_pair_count,
                "pair_count": profile.pair_count,
            }

    witnesses = (
        (2, 107, 109, "proper_factor", 107),
        (2, 5, 107, "full_collision", None),
        (2, 109, 113, "unit", None),
    )
    for level, first_prime, second_prime, status, factor in witnesses:
        outcome = phi4_pair_outcome(level, first_prime, second_prime)
        if outcome.status != status or outcome.factor != factor:
            counts["failures"] += 1
        counts["registered_outcome_witnesses"] += 1

    if counts["failures"]:
        raise AssertionError("M29 compact cofactor prime-support audit failed")
    summary: dict[str, Any] = {
        "schema_version": "1.0.0",
        "parameters": vars(args),
        "counts": counts,
        "prime_support_extrema": prime_support_extrema,
        "balanced_extrema": balanced_extrema,
    }
    canonical = json.dumps(summary, sort_keys=True, separators=(",", ":"))
    summary["summary_sha256"] = hashlib.sha256(canonical.encode()).hexdigest()
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
