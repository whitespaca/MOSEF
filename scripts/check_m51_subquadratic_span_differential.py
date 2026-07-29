"""Independently validate the M51 variable-order signature records."""

from __future__ import annotations

import hashlib
import json
import math
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "python")]

from mosef_reference import balanced_prime_population

SCHEMA = ROOT / "schemas/m51-subquadratic-span-v1.json"


def _independent_hit(level: int, prime: int) -> bool:
    exponent = 3 * (1 << level) + 5
    return (pow(2, exponent, prime) + 3) % prime == 0


def _balanced_order(candidate_count: int, level_span: int) -> int:
    logarithmic_scale = candidate_count.bit_length()
    quotient = (level_span + logarithmic_scale - 1) // logarithmic_scale
    order = math.isqrt(quotient)
    if order * order < quotient:
        order += 1
    return min(candidate_count, max(1, order))


def main() -> int:
    """Check the hash, variable order, signatures, and exact finite bounds."""
    data = json.loads(SCHEMA.read_text(encoding="utf-8"))
    canonical = dict(data)
    expected_hash = canonical.pop("summary_sha256")
    actual_hash = hashlib.sha256(
        json.dumps(canonical, sort_keys=True, separators=(",", ":")).encode(
            "utf-8"
        )
    ).hexdigest()
    if actual_hash != expected_hash:
        raise AssertionError("M51 canonical summary hash changed")

    profile_checks = 0
    coordinate_checks = 0
    pair_formula_checks = 0
    balance_checks = 0
    for record in data["profiles"]:
        input_length = int(record["input_length"])
        levels = tuple(int(level) for level in record["candidate_levels"])
        candidate_count = len(levels)
        level_span = levels[-1] - levels[0]
        overlap_order = _balanced_order(candidate_count, level_span)
        threshold = overlap_order + 1
        primes = balanced_prime_population(input_length)
        signatures = []
        for prime in primes:
            signature = sum(
                1 << index
                for index, level in enumerate(levels)
                if _independent_hit(level, prime)
            )
            signatures.append(signature)
            coordinate_checks += candidate_count
        counts = Counter(signatures)
        weights = [signature.bit_count() for signature in signatures]
        high_weight_count = sum(weight >= threshold for weight in weights)
        pair_count = math.comb(len(primes), 2)
        collision_count = sum(
            math.comb(count, 2) for count in counts.values()
        )
        maximum_common_gap = level_span // overlap_order
        overlap_bit_bound = 5 * ((1 << maximum_common_gap) - 1) + 1
        population_prime_bits = (input_length - 1) // 2
        high_weight_bound = (
            math.comb(candidate_count, threshold)
            * overlap_bit_bound
            // population_prime_bits
            if threshold <= candidate_count
            else 0
        )
        low_weight_capacity = sum(
            math.comb(candidate_count, weight)
            for weight in range(min(threshold, candidate_count + 1))
        )
        logarithmic_scale = candidate_count.bit_length()
        expected = {
            "candidate_count": candidate_count,
            "level_span": level_span,
            "compact_evaluation_level_sum": sum(levels),
            "overlap_order": overlap_order,
            "high_weight_threshold": threshold,
            "maximum_common_gap": maximum_common_gap,
            "logarithmic_scale": logarithmic_scale,
            "balance_product": overlap_order**2 * logarithmic_scale,
            "span_log_product": level_span * logarithmic_scale,
            "input_length_squared": input_length**2,
            "population_size": len(primes),
            "distinct_signature_count": len(counts),
            "zero_signature_count": counts.get(0, 0),
            "high_weight_prime_count": high_weight_count,
            "maximum_signature_weight": max(weights),
            "high_weight_population_upper_bound": high_weight_bound,
            "high_weight_upper_bound_bit_length": high_weight_bound.bit_length(),
            "low_weight_signature_capacity": low_weight_capacity,
            "low_weight_capacity_bit_length": low_weight_capacity.bit_length(),
            "pair_count": pair_count,
            "separated_pair_count": pair_count - collision_count,
            "collision_pair_count": collision_count,
            "maximum_bucket_size": max(counts.values()),
            "theorem_forces_collision": (
                len(primes) - high_weight_bound > low_weight_capacity
            ),
            "injective": collision_count == 0,
        }
        for field, value in expected.items():
            if record[field] != value:
                raise AssertionError(f"M51 field changed: {field}")
        if high_weight_count > high_weight_bound:
            raise AssertionError("M51 high-weight bound failed")
        if overlap_order**2 * logarithmic_scale < level_span:
            raise AssertionError("M51 balance inequality failed")
        profile_checks += 1
        pair_formula_checks += 1
        balance_checks += 1

    print(
        "M51 subquadratic-span differential validation: PASS "
        f"({profile_checks} profile checks, "
        f"{coordinate_checks} coordinate checks, "
        f"{pair_formula_checks} pair-formula checks, "
        f"{balance_checks} variable-order balance checks)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
