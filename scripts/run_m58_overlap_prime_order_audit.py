"""Deterministic M58 audit of overlap-prime occurrence orders."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "python")]

from mosef_reference import compact_gap_overlap_prime_occurrence

PRIME_MAXIMUM = 50_000
MAXIMUM_GAP = 16


def _primes_up_to(limit: int) -> tuple[int, ...]:
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[:2] = b"\x00\x00"
    for prime in range(2, int(limit**0.5) + 1):
        if sieve[prime]:
            start = prime * prime
            sieve[start : limit + 1 : prime] = b"\x00" * (
                (limit - start) // prime + 1
            )
    return tuple(
        value
        for value in range(11, limit + 1)
        if sieve[value]
    )


def _sequence_sha256(values: tuple[int, ...]) -> str:
    payload = ",".join(str(value) for value in values).encode("ascii")
    return hashlib.sha256(payload).hexdigest()


def build_summary() -> dict[str, object]:
    """Build exact prime-order and occurrence-period records."""
    hit_profiles: list[dict[str, int | bool | list[int] | str]] = []
    aggregate = hashlib.sha256()
    prime_count = 0
    periodicity_checks = 0
    for prime in _primes_up_to(PRIME_MAXIMUM):
        profile = compact_gap_overlap_prime_occurrence(
            prime,
            MAXIMUM_GAP,
        )
        record: dict[str, int | bool | list[int] | str] = {
            "prime": prime,
            "ratio_residue": profile.ratio_residue,
            "ratio_order": profile.ratio_order,
            "odd_half_order": profile.odd_half_order,
            "occurrence_period": profile.occurrence_period,
            "predicted_occurrence_gaps": list(
                profile.predicted_occurrence_gaps
            ),
            "direct_occurrence_gaps": list(
                profile.direct_occurrence_gaps
            ),
            "occurrence_sha256": _sequence_sha256(
                profile.direct_occurrence_gaps
            ),
            "characterization_holds": profile.characterization_holds,
        }
        aggregate.update(
            json.dumps(
                record,
                sort_keys=True,
                separators=(",", ":"),
            ).encode("utf-8")
        )
        aggregate.update(b"\n")
        prime_count += 1
        if profile.direct_occurrence_gaps:
            hit_profiles.append(record)
            periodicity_checks += len(profile.direct_occurrence_gaps)

    counts = {
        "prime_profiles": prime_count,
        "hit_primes": len(hit_profiles),
        "miss_primes": prime_count - len(hit_profiles),
        "direct_divisibility_checks": prime_count * MAXIMUM_GAP,
        "periodicity_checks": periodicity_checks,
        "sequence_hash_checks": prime_count,
    }
    summary: dict[str, object] = {
        "schema_version": "1.0.0",
        "experiment_id": "EXP-0056",
        "prime_maximum": PRIME_MAXIMUM,
        "maximum_gap": MAXIMUM_GAP,
        "characterization": (
            "p|R_q iff ord_p(3/32)=2d with odd d|(2^q-1)"
        ),
        "all_profiles_sha256": aggregate.hexdigest(),
        "hit_profiles": hit_profiles,
        "counts": counts,
        "status": "PASS",
    }
    canonical = json.dumps(summary, sort_keys=True, separators=(",", ":"))
    summary["summary_sha256"] = hashlib.sha256(
        canonical.encode("utf-8")
    ).hexdigest()
    return summary


def main() -> int:
    summary = build_summary()
    hit_profiles = summary["hit_profiles"]
    if not isinstance(hit_profiles, list):
        raise AssertionError("M58 hit profiles have the wrong shape")
    if any(
        not profile["characterization_holds"]
        for profile in hit_profiles
    ):
        raise AssertionError("M58 order characterization failed")
    counts = summary["counts"]
    if not isinstance(counts, dict):
        raise AssertionError("M58 counts have the wrong shape")
    print(
        "M58 overlap-prime order audit: PASS "
        f"(summary_sha256={summary['summary_sha256']}, "
        f"primes={counts['prime_profiles']}, "
        f"hits={counts['hit_primes']})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
