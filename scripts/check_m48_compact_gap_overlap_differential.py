"""Independently validate the M48 overlap and finite signature records."""

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

SCHEMA = ROOT / "schemas/m48-compact-gap-overlap-v1.json"


def _independent_hit(level: int, prime: int) -> bool:
    exponent = 3 * (1 << level) + 5
    return (pow(2, exponent, prime) + 3) % prime == 0


def main() -> int:
    """Check canonical hashing, signatures, collisions, and overlap divisibility."""
    data = json.loads(SCHEMA.read_text(encoding="utf-8"))
    canonical = dict(data)
    expected_hash = canonical.pop("summary_sha256")
    actual_hash = hashlib.sha256(
        json.dumps(canonical, sort_keys=True, separators=(",", ":")).encode(
            "utf-8"
        )
    ).hexdigest()
    if actual_hash != expected_hash:
        raise AssertionError("M48 canonical summary hash changed")

    overlap_checks = 0
    for record in data["overlap_records"]:
        gap = int(record["level_gap"])
        odd_exponent = (1 << gap) - 1
        exact = pow(3, odd_exponent) + pow(32, odd_exponent)
        if odd_exponent != record["odd_exponent"]:
            raise AssertionError("M48 overlap exponent changed")
        if exact.bit_length() != record["exact_bit_length"]:
            raise AssertionError("M48 overlap bit length changed")
        if exact.bit_length() > record["bit_length_upper_bound"]:
            raise AssertionError("M48 overlap upper bound failed")
        overlap_checks += 1

    common_support_checks = 0
    for witness in data["overlap_witnesses"]:
        prime = int(witness["prime"])
        first_level = int(witness["first_level"])
        second_level = int(witness["second_level"])
        if not _independent_hit(first_level, prime):
            raise AssertionError("M48 first overlap witness hit failed")
        if not _independent_hit(second_level, prime):
            raise AssertionError("M48 second overlap witness hit failed")
        gap = second_level - first_level
        odd_exponent = (1 << gap) - 1
        overlap = pow(3, odd_exponent) + pow(32, odd_exponent)
        if overlap % prime:
            raise AssertionError("M48 overlap witness divisibility failed")
        common_support_checks += 1

    profile_checks = 0
    coordinate_checks = 0
    pair_formula_checks = 0
    for record in data["profiles"]:
        input_length = int(record["input_length"])
        levels = tuple(int(level) for level in record["candidate_levels"])
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
            hit_indices = tuple(
                index
                for index in range(len(levels))
                if signature & (1 << index)
            )
            for first_index in range(len(hit_indices)):
                for second_index in range(first_index + 1, len(hit_indices)):
                    gap = (
                        levels[hit_indices[second_index]]
                        - levels[hit_indices[first_index]]
                    )
                    odd_exponent = (1 << gap) - 1
                    overlap = (
                        pow(3, odd_exponent) + pow(32, odd_exponent)
                    )
                    if overlap % prime:
                        raise AssertionError(
                            "M48 common support escaped overlap integer"
                        )
                    common_support_checks += 1

        counts = Counter(signatures)
        pair_count = math.comb(len(primes), 2)
        collision_count = sum(
            math.comb(count, 2) for count in counts.values()
        )
        multi_hit_count = sum(
            signature.bit_count() >= 2 for signature in signatures
        )
        if len(primes) != record["population_size"]:
            raise AssertionError("M48 population size changed")
        if len(counts) != record["distinct_signature_count"]:
            raise AssertionError("M48 distinct signature count changed")
        if counts.get(0, 0) != record["zero_signature_count"]:
            raise AssertionError("M48 zero signature count changed")
        if multi_hit_count != record["multi_hit_prime_count"]:
            raise AssertionError("M48 multi-hit count changed")
        if pair_count != record["pair_count"]:
            raise AssertionError("M48 pair count changed")
        if collision_count != record["collision_pair_count"]:
            raise AssertionError("M48 collision count changed")
        if pair_count - collision_count != record["separated_pair_count"]:
            raise AssertionError("M48 separated pair count changed")
        if max(counts.values()) != record["maximum_bucket_size"]:
            raise AssertionError("M48 maximum bucket changed")
        if (
            multi_hit_count
            > record["overlap_population_upper_bound"]
        ):
            raise AssertionError("M48 overlap population bound failed")
        profile_checks += 1
        pair_formula_checks += 1

    print(
        "M48 compact-gap overlap differential validation: PASS "
        f"({overlap_checks} overlap checks, "
        f"{profile_checks} profile checks, "
        f"{coordinate_checks} coordinate checks, "
        f"{pair_formula_checks} pair-formula checks, "
        f"{common_support_checks} common-support checks)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
