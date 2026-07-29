"""Independently validate the M49 wide-span signature records."""

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

SCHEMA = ROOT / "schemas/m49-wide-span-compact-gap-v1.json"


def _independent_hit(level: int, prime: int) -> bool:
    exponent = 3 * (1 << level) + 5
    return (pow(2, exponent, prime) + 3) % prime == 0


def _common_gap(levels: tuple[int, ...]) -> int:
    first = levels[0]
    return math.gcd(*(level - first for level in levels[1:]))


def main() -> int:
    """Check canonical hash, higher overlaps, signatures, and pair counts."""
    data = json.loads(SCHEMA.read_text(encoding="utf-8"))
    canonical = dict(data)
    expected_hash = canonical.pop("summary_sha256")
    actual_hash = hashlib.sha256(
        json.dumps(canonical, sort_keys=True, separators=(",", ":")).encode(
            "utf-8"
        )
    ).hexdigest()
    if actual_hash != expected_hash:
        raise AssertionError("M49 canonical summary hash changed")

    common_support_checks = 0
    for witness in data["common_support_witnesses"]:
        prime = int(witness["prime"])
        levels = tuple(int(level) for level in witness["candidate_levels"])
        if not all(_independent_hit(level, prime) for level in levels):
            raise AssertionError("M49 independent common hit failed")
        common_gap = _common_gap(levels)
        odd_exponent = (1 << common_gap) - 1
        overlap = pow(3, odd_exponent) + pow(32, odd_exponent)
        if common_gap != witness["common_gap"] or overlap % prime:
            raise AssertionError("M49 common overlap divisor failed")
        common_support_checks += 1

    profile_checks = 0
    coordinate_checks = 0
    pair_formula_checks = 0
    for record in data["profiles"]:
        input_length = int(record["input_length"])
        levels = tuple(int(level) for level in record["candidate_levels"])
        threshold = int(record["high_weight_threshold"])
        primes = balanced_prime_population(input_length)
        signatures = []
        for prime in primes:
            signature = sum(
                1 << index
                for index, level in enumerate(levels)
                if _independent_hit(level, prime)
            )
            signatures.append(signature)
            coordinate_checks += len(levels)
        counts = Counter(signatures)
        weights = [signature.bit_count() for signature in signatures]
        high_weight_count = sum(weight >= threshold for weight in weights)
        pair_count = math.comb(len(primes), 2)
        collision_count = sum(
            math.comb(count, 2) for count in counts.values()
        )
        candidate_count = len(levels)
        level_span = levels[-1] - levels[0]
        maximum_common_gap = level_span // (threshold - 1)
        overlap_bit_bound = 5 * ((1 << maximum_common_gap) - 1) + 1
        population_prime_bits = (input_length - 1) // 2
        high_weight_bound = (
            math.comb(candidate_count, threshold)
            * overlap_bit_bound
            // population_prime_bits
        )
        low_weight_capacity = sum(
            math.comb(candidate_count, weight)
            for weight in range(threshold)
        )
        if len(primes) != record["population_size"]:
            raise AssertionError("M49 population size changed")
        if len(counts) != record["distinct_signature_count"]:
            raise AssertionError("M49 distinct signature count changed")
        if counts.get(0, 0) != record["zero_signature_count"]:
            raise AssertionError("M49 zero signature count changed")
        if high_weight_count != record["high_weight_prime_count"]:
            raise AssertionError("M49 high-weight count changed")
        if max(weights) != record["maximum_signature_weight"]:
            raise AssertionError("M49 maximum signature weight changed")
        if pair_count != record["pair_count"]:
            raise AssertionError("M49 pair count changed")
        if collision_count != record["collision_pair_count"]:
            raise AssertionError("M49 collision count changed")
        if pair_count - collision_count != record["separated_pair_count"]:
            raise AssertionError("M49 separated count changed")
        if max(counts.values()) != record["maximum_bucket_size"]:
            raise AssertionError("M49 maximum bucket changed")
        if candidate_count != record["candidate_count"]:
            raise AssertionError("M49 candidate count changed")
        if level_span != record["level_span"]:
            raise AssertionError("M49 level span changed")
        if sum(levels) != record["compact_evaluation_level_sum"]:
            raise AssertionError("M49 compact evaluation ledger changed")
        if high_weight_bound != record["high_weight_population_upper_bound"]:
            raise AssertionError("M49 high-weight bound changed")
        if low_weight_capacity != record["low_weight_signature_capacity"]:
            raise AssertionError("M49 low-weight capacity changed")
        if (
            len(primes) - high_weight_bound > low_weight_capacity
        ) != record["theorem_forces_collision"]:
            raise AssertionError("M49 finite theorem flag changed")
        if (collision_count == 0) != record["injective"]:
            raise AssertionError("M49 injectivity flag changed")
        if high_weight_count > high_weight_bound:
            raise AssertionError("M49 high-weight bound failed")
        profile_checks += 1
        pair_formula_checks += 1

    print(
        "M49 wide-span compact-gap differential validation: PASS "
        f"({common_support_checks} common-support checks, "
        f"{profile_checks} profile checks, "
        f"{coordinate_checks} coordinate checks, "
        f"{pair_formula_checks} pair-formula checks)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
