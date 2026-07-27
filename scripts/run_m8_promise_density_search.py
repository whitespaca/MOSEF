"""Exhaustively falsify the M8 combined-signature density barrier."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

from mosef_reference import (
    analyze_combined_density,
    combined_asymmetry,
    combined_signature,
    direct_combined_asymmetry,
    is_prime,
)


def canonical_json(value: Any) -> bytes:
    """Serialize a value deterministically for hashing."""
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def balanced_primes(n: int, prime_max: int) -> tuple[int, ...]:
    """Return primes in ``(2^n, 2^(n+1/2))`` without floating point."""
    lower = 1 << n
    squared_upper = 1 << (2 * n + 1)
    return tuple(
        value
        for value in range(lower + 1, prime_max + 1, 2)
        if value * value < squared_upper and is_prime(value)
    )


def search(
    prime_max: int,
    candidate_max: int,
    family_size_max: int,
    balanced_n_max: int,
) -> dict[str, Any]:
    """Run the deterministic M8 search and return its exact summary."""
    if prime_max < 7 or candidate_max < 1 or family_size_max < 1:
        raise ValueError("prime_max must be at least 7 and family bounds positive")
    if family_size_max > candidate_max:
        raise ValueError("family_size_max cannot exceed candidate_max")
    if balanced_n_max < 2:
        raise ValueError("balanced_n_max must be at least 2")

    primes = tuple(
        value for value in range(3, prime_max + 1, 2) if is_prime(value)
    )
    families = tuple(
        family
        for size in range(1, family_size_max + 1)
        for family in itertools.combinations(range(1, candidate_max + 1), size)
    )
    pair_count = len(primes) * (len(primes) - 1) // 2
    signature_pair_checks = 0
    density_bound_checks = 0
    divisor_bound_checks = 0
    magnitude_zero_signature_checks = 0
    magnitude_zero_pair_checks = 0
    balanced_zero_family_checks = 0
    maximum_density: tuple[Fraction, tuple[int, ...], int, int] | None = None
    minimum_nonzero_density: (
        tuple[Fraction, tuple[int, ...], int, int] | None
    ) = None
    largest_hit: tuple[int, tuple[int, ...]] | None = None

    for family in families:
        for left, right in itertools.combinations(primes, 2):
            signature_pair_checks += 1
            actual = combined_asymmetry(left, right, family)
            direct = direct_combined_asymmetry(left, right, family)
            if actual != direct:
                raise AssertionError(("signature characterization", family, left, right))

        analysis = analyze_combined_density(primes, family)
        density_bound_checks += 1
        if analysis.promised_pairs > analysis.hit_intersecting_pairs:
            raise AssertionError(("pair bound", family, analysis))
        divisor_bound_checks += 1
        if analysis.hit_count > analysis.divisor_hit_bound:
            raise AssertionError(("divisor hit bound", family, analysis))
        if analysis.hit_count > analysis.square_root_hit_bound:
            raise AssertionError(("square-root hit bound", family, analysis))

        density = Fraction(analysis.promised_pairs, analysis.total_pairs)
        density_record = (
            density,
            family,
            analysis.promised_pairs,
            analysis.total_pairs,
        )
        if maximum_density is None or density_record[0] > maximum_density[0]:
            maximum_density = density_record
        if density > 0 and (
            minimum_nonzero_density is None
            or density < minimum_nonzero_density[0]
        ):
            minimum_nonzero_density = density_record
        hit_record = (analysis.hit_count, family)
        if largest_hit is None or hit_record[0] > largest_hit[0]:
            largest_hit = hit_record

        zero_primes = tuple(prime for prime in primes if prime > max(family) + 1)
        for prime in zero_primes:
            magnitude_zero_signature_checks += 1
            if any(
                bit
                for coordinate in combined_signature(prime, family)
                for bit in coordinate
            ):
                raise AssertionError(("magnitude signature", family, prime))
        for left, right in itertools.combinations(zero_primes, 2):
            magnitude_zero_pair_checks += 1
            if combined_asymmetry(left, right, family):
                raise AssertionError(("magnitude pair", family, left, right))

        for n in range(2, balanced_n_max + 1):
            interval_primes = balanced_primes(n, prime_max)
            if len(interval_primes) < 2 or max(family) + 1 >= 1 << n:
                continue
            balanced_zero_family_checks += 1
            interval_analysis = analyze_combined_density(interval_primes, family)
            if interval_analysis.promised_pairs != 0:
                raise AssertionError(("balanced zero density", n, family))

    if maximum_density is None or minimum_nonzero_density is None:
        raise AssertionError("registered bounds must contain nonzero density cases")
    if largest_hit is None:
        raise AssertionError("registered bounds must contain a hit analysis")

    def density_json(
        record: tuple[Fraction, tuple[int, ...], int, int],
    ) -> dict[str, Any]:
        fraction, family, numerator, denominator = record
        return {
            "exponents": list(family),
            "promised_pairs": numerator,
            "total_pairs": denominator,
            "fraction": f"{fraction.numerator}/{fraction.denominator}",
        }

    summary: dict[str, Any] = {
        "bounds": {
            "odd_prime": [3, prime_max],
            "exponent": [1, candidate_max],
            "family_size": [1, family_size_max],
            "balanced_n": [2, balanced_n_max],
        },
        "seed": None,
        "odd_prime_count": len(primes),
        "exponent_family_count": len(families),
        "prime_pairs_per_family": pair_count,
        "signature_pair_checks": signature_pair_checks,
        "density_bound_checks": density_bound_checks,
        "divisor_bound_checks": divisor_bound_checks,
        "magnitude_zero_signature_checks": magnitude_zero_signature_checks,
        "magnitude_zero_pair_checks": magnitude_zero_pair_checks,
        "balanced_zero_family_checks": balanced_zero_family_checks,
        "smallest_all_zero_failure": {
            "exponents": [1],
            "p": 3,
            "q": 5,
            "n": 15,
        },
        "maximum_promised_density": density_json(maximum_density),
        "minimum_nonzero_promised_density": density_json(
            minimum_nonzero_density
        ),
        "largest_hit_set": {
            "count": largest_hit[0],
            "exponents": list(largest_hit[1]),
        },
        "checked": {
            "signature_characterization": True,
            "pair_intersects_hit_bound": True,
            "divisor_hit_bound": True,
            "square_root_hit_bound": True,
            "magnitude_zero_signature": True,
            "balanced_zero_density": True,
        },
    }
    summary["summary_sha256"] = hashlib.sha256(canonical_json(summary)).hexdigest()
    return summary


def main() -> int:
    """Command-line entry point."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prime-max", type=int, default=101)
    parser.add_argument("--candidate-max", type=int, default=18)
    parser.add_argument("--family-size-max", type=int, default=3)
    parser.add_argument("--balanced-n-max", type=int, default=6)
    args = parser.parse_args()
    print(
        json.dumps(
            search(
                args.prime_max,
                args.candidate_max,
                args.family_size_max,
                args.balanced_n_max,
            ),
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
