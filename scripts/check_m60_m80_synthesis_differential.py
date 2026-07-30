"""Independently reconstruct the registered M60--M80 arithmetic audit."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas/m60-m80-synthesis-v1.json"


def _divisors(value: int) -> tuple[int, ...]:
    result: list[int] = []
    for divisor in range(1, math.isqrt(value) + 1):
        if value % divisor == 0:
            result.append(divisor)
            if divisor * divisor != value:
                result.append(value // divisor)
    return tuple(sorted(result))


def _minimal(values: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(
        value
        for value in values
        if not any(
            value % smaller == 0
            for smaller in values
            if smaller < value
        )
    )


def _is_prime(value: int) -> bool:
    if value < 2:
        return False
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            return False
        divisor += 1 if divisor == 2 else 2
    return True


def _balanced_primes(input_length: int) -> tuple[int, ...]:
    lower = math.isqrt((1 << (input_length - 1)) - 1) + 1
    upper = math.isqrt((1 << input_length) - 1)
    return tuple(
        value for value in range(lower, upper + 1) if _is_prime(value)
    )


def _residue_row(input_length: int) -> dict[str, int | str]:
    gap = input_length // 2
    lower = math.isqrt((1 << (input_length - 1)) - 1) + 1
    upper = math.isqrt((1 << input_length) - 1)
    threshold = 3
    while 33**threshold <= lower:
        threshold += 2
    admissible = tuple(
        divisor
        for divisor in _divisors((1 << gap) - 1)
        if divisor >= threshold
    )
    minimal = _minimal(admissible)
    residues: set[int] = set()
    for value in range(lower, upper + 1):
        if any((value - 1) % (2 * divisor) == 0 for divisor in minimal):
            residues.add(value)
    interval_size = upper - lower + 1
    row: dict[str, int | str] = {
        "input_length": input_length,
        "gap": gap,
        "size_threshold": threshold,
        "admissible_divisor_count": len(admissible),
        "minimal_divisor_count": len(minimal),
        "residue_union_size": len(residues),
        "interval_size": interval_size,
        "elementary_union_bound": sum(
            interval_size // (2 * divisor) + 1 for divisor in minimal
        ),
    }
    row["row_sha256"] = hashlib.sha256(
        json.dumps(row, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    return row


def _separator_row(input_length: int) -> dict[str, int | str]:
    levels = tuple(range(2, input_length + 13))
    signatures: dict[int, int] = {}
    for prime in _balanced_primes(input_length):
        signature = 0
        for index, level in enumerate(levels):
            exponent = 3 * (1 << level) + 5
            if (pow(2, exponent, prime) + 3) % prime == 0:
                signature |= 1 << index
        signatures[prime] = signature
    primes = tuple(signatures)
    separated = 0
    verified = 0
    for index, first in enumerate(primes):
        for second in primes[index + 1 :]:
            if signatures[first] == signatures[second]:
                continue
            separated += 1
            differing = signatures[first] ^ signatures[second]
            coordinate = (differing & -differing).bit_length() - 1
            first_hit = bool(signatures[first] & (1 << coordinate))
            factor = first if first_hit else second
            verified += int(factor in (first, second))
    row: dict[str, int | str] = {
        "input_length": input_length,
        "candidate_count": len(levels),
        "separated_pairs": separated,
        "verified_proper_factors": verified,
    }
    row["row_sha256"] = hashlib.sha256(
        json.dumps(row, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    return row


def main() -> int:
    data = json.loads(SCHEMA.read_text(encoding="utf-8"))
    canonical = dict(data)
    expected = canonical.pop("summary_sha256")
    actual = hashlib.sha256(
        json.dumps(canonical, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    if actual != expected:
        raise AssertionError("synthesis canonical hash changed")

    residue_rows = [_residue_row(length) for length in range(9, 41)]
    separator_rows = [_separator_row(length) for length in range(9, 19)]
    if residue_rows != data["residue_rows"]:
        raise AssertionError("registered residue rows changed")
    if separator_rows != data["separator_rows"]:
        raise AssertionError("registered separator rows changed")
    counts = {
        "residue_profiles": len(residue_rows),
        "admissible_divisor_profiles": sum(
            int(row["admissible_divisor_count"]) for row in residue_rows
        ),
        "exact_residue_candidates": sum(
            int(row["residue_union_size"]) for row in residue_rows
        ),
        "separator_profiles": len(separator_rows),
        "separated_pair_checks": sum(
            int(row["separated_pairs"]) for row in separator_rows
        ),
        "verified_proper_factors": sum(
            int(row["verified_proper_factors"]) for row in separator_rows
        ),
        "row_hashes": len(residue_rows) + len(separator_rows),
    }
    if counts != data["counts"]:
        raise AssertionError("registered synthesis counts changed")
    print(
        "M60-M80 synthesis differential validation: PASS "
        f"({len(residue_rows)} residue profiles, "
        f"{len(separator_rows)} separator profiles)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
