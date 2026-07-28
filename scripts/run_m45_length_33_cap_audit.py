"""Deterministic M45 audit of the length-33 finite envelope."""

from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "python")]

from mosef_reference import (
    ExceptionalSelectorDescriptor,
    balanced_prime_population,
    diversified_exceptional_selector,
)
from mosef_reference.diversified_compact_signatures import (
    PRIMITIVE_EXIT_KINDS,
    _primitive_exit_mask_from_resultant,
)
from mosef_reference.exceptional_cofactor_schedule import (
    exceptional_cofactor_overlap,
)

INPUT_LENGTH = 33
ADDITIVE_CAP = 168
MULTIPLICATIVE_CAP = 172
PREDECESSOR_CAP = 194
REPAIR_CAP = 195
ADDITIVE_COLLISION = (
    66089,
    71039,
    75161,
    75629,
    78791,
    80309,
    81043,
    91387,
    91411,
    92173,
    92641,
    92671,
)
MULTIPLICATIVE_COLLISION = (
    71039,
    75161,
    75629,
    80309,
    91387,
    91411,
    92173,
    92671,
)
FINAL_COLLISION = (80309, 92671)
REPAIR_SOURCE = "phi4:195:91:20:cofactor"

# descriptor count, distinct signatures, pairs, bucket, selected sources,
# cumulative optimized local-exit evaluations
EXPECTED_PUBLIC_PROFILES = {
    168: (
        418502,
        2399,
        66,
        (ADDITIVE_COLLISION,),
        2399,
        157886016,
    ),
    172: (
        447678,
        2403,
        28,
        (MULTIPLICATIVE_COLLISION,),
        2403,
        158193605,
    ),
}

# descriptor count, new descriptors, distinct signatures, pairs, bucket,
# selected sources, optimized local-exit evaluations after cap 172
EXPECTED_TRANSITIONS = {
    173: (455284, 7606, 2403, 28, (MULTIPLICATIVE_COLLISION,), 2403, 60848),
    174: (457931, 2647, 2403, 28, (MULTIPLICATIVE_COLLISION,), 2403, 82024),
    175: (
        475542,
        17611,
        2405,
        15,
        ((71039, 80309, 91387, 91411, 92173, 92671),),
        2405,
        209314,
    ),
    176: (
        478275,
        2733,
        2405,
        15,
        ((71039, 80309, 91387, 91411, 92173, 92671),),
        2405,
        225712,
    ),
    177: (
        486112,
        7837,
        2406,
        10,
        ((80309, 91387, 91411, 92173, 92671),),
        2406,
        266238,
    ),
    178: (
        488874,
        2762,
        2406,
        10,
        ((80309, 91387, 91411, 92173, 92671),),
        2406,
        280048,
    ),
    179: (
        512640,
        23766,
        2407,
        6,
        ((80309, 91387, 91411, 92671),),
        2407,
        376214,
    ),
    180: (
        515520,
        2880,
        2407,
        6,
        ((80309, 91387, 91411, 92671),),
        2407,
        387734,
    ),
    181: (
        518400,
        2880,
        2407,
        6,
        ((80309, 91387, 91411, 92671),),
        2407,
        399254,
    ),
    182: (
        521280,
        2880,
        2407,
        6,
        ((80309, 91387, 91411, 92671),),
        2407,
        410774,
    ),
    183: (
        546000,
        24720,
        2407,
        6,
        ((80309, 91387, 91411, 92671),),
        2407,
        509654,
    ),
    184: (
        549000,
        3000,
        2408,
        3,
        ((80309, 91411, 92671),),
        2408,
        518723,
    ),
    185: (
        557704,
        8704,
        2408,
        3,
        ((80309, 91411, 92671),),
        2408,
        544835,
    ),
    186: (
        560735,
        3031,
        2408,
        3,
        ((80309, 91411, 92671),),
        2408,
        553928,
    ),
    187: (
        580878,
        20143,
        2408,
        3,
        ((80309, 91411, 92671),),
        2408,
        614357,
    ),
    188: (584001, 3123, 2409, 1, (FINAL_COLLISION,), 2409, 621813),
    189: (592952, 8951, 2409, 1, (FINAL_COLLISION,), 2409, 639715),
    190: (596106, 3154, 2409, 1, (FINAL_COLLISION,), 2409, 646023),
    191: (623200, 27094, 2409, 1, (FINAL_COLLISION,), 2409, 700211),
    192: (626480, 3280, 2409, 1, (FINAL_COLLISION,), 2409, 706771),
    193: (629760, 3280, 2409, 1, (FINAL_COLLISION,), 2409, 713331),
    194: (633040, 3280, 2409, 1, (FINAL_COLLISION,), 2409, 719891),
    195: (661152, 28112, 2410, 0, (), 2410, 751601),
}


def _first_cap(descriptor: ExceptionalSelectorDescriptor) -> int:
    return int(
        max(
        INPUT_LENGTH,
        descriptor.first_factor,
        descriptor.second_factor,
        descriptor.base,
        )
    )


def _refine(
    buckets: tuple[tuple[int, ...], ...],
    descriptor: ExceptionalSelectorDescriptor,
) -> tuple[tuple[tuple[int, ...], ...], tuple[str, ...], int]:
    resultant = exceptional_cofactor_overlap(
        descriptor.first_factor,
        descriptor.second_factor,
        descriptor.family,
    ).cyclotomic_cofactor_resultant
    refined: list[tuple[int, ...]] = []
    variable_kinds: set[int] = set()
    checks = 0
    for bucket in buckets:
        grouped: defaultdict[int, list[int]] = defaultdict(list)
        masks: list[int] = []
        for prime in bucket:
            mask = _primitive_exit_mask_from_resultant(
                descriptor,
                prime,
                resultant,
            )
            grouped[mask].append(prime)
            masks.append(mask)
            checks += 1
        if len(grouped) > 1:
            variable_kinds.update(
                kind_index
                for kind_index in range(len(PRIMITIVE_EXIT_KINDS))
                if len(
                    {
                        bool(mask & (1 << kind_index))
                        for mask in masks
                    }
                )
                > 1
            )
        refined.extend(
            tuple(group) for group in grouped.values() if len(group) > 1
        )
    sources = tuple(
        f"{descriptor.key}:{PRIMITIVE_EXIT_KINDS[kind_index]}"
        for kind_index in sorted(variable_kinds)
    )
    return tuple(refined), sources, checks


def _profile(
    cap: int,
    descriptor_count: int,
    new_descriptor_count: int,
    population_size: int,
    buckets: tuple[tuple[int, ...], ...],
    selected_count: int,
    checks: int,
) -> dict[str, object]:
    pairs = sum(len(bucket) * (len(bucket) - 1) // 2 for bucket in buckets)
    return {
        "selector_cap": cap,
        "population_size": population_size,
        "descriptor_count": descriptor_count,
        "new_descriptor_count": new_descriptor_count,
        "raw_coordinate_count": descriptor_count * len(PRIMITIVE_EXIT_KINDS),
        "distinct_signature_count": population_size
        - sum(len(bucket) - 1 for bucket in buckets),
        "collision_pair_count": pairs,
        "maximum_bucket_size": max(
            (len(bucket) for bucket in buckets),
            default=1,
        ),
        "collision_buckets": buckets,
        "selected_coordinate_count": selected_count,
        "optimized_local_exit_checks": checks,
    }


def _partition_audit(
    primes: tuple[int, ...],
) -> tuple[
    tuple[dict[str, object], ...],
    tuple[dict[str, object], ...],
    tuple[str, ...],
    tuple[str, ...],
]:
    descriptors = diversified_exceptional_selector(INPUT_LENGTH, REPAIR_CAP)
    by_cap: defaultdict[int, list[ExceptionalSelectorDescriptor]] = defaultdict(
        list
    )
    for descriptor in descriptors:
        by_cap[_first_cap(descriptor)].append(descriptor)

    buckets: tuple[tuple[int, ...], ...] = (primes,)
    selected: list[str] = []
    public: list[dict[str, object]] = []
    transitions: list[dict[str, object]] = []
    descriptor_count = 0
    checks = 0
    baseline = 0
    predecessor_sources: tuple[str, ...] = ()
    selected_caps = set(EXPECTED_PUBLIC_PROFILES) | set(EXPECTED_TRANSITIONS)
    for cap in range(INPUT_LENGTH, REPAIR_CAP + 1):
        added = by_cap[cap]
        for descriptor in added:
            buckets, sources, local_checks = _refine(buckets, descriptor)
            selected.extend(sources)
            checks += local_checks
        descriptor_count += len(added)
        if cap not in selected_caps:
            continue
        record = _profile(
            cap,
            descriptor_count,
            len(added),
            len(primes),
            buckets,
            len(selected),
            checks,
        )
        if cap in EXPECTED_PUBLIC_PROFILES:
            observed = (
                descriptor_count,
                record["distinct_signature_count"],
                record["collision_pair_count"],
                buckets,
                len(selected),
                checks,
            )
            if observed != EXPECTED_PUBLIC_PROFILES[cap]:
                raise AssertionError(f"M45 public profile changed: {cap}, {observed}")
            public.append(record)
            if cap == MULTIPLICATIVE_CAP:
                baseline = checks
                transitions.append(
                    {
                        **record,
                        "new_descriptor_count": 0,
                        "tracked_population_size": len(MULTIPLICATIVE_COLLISION),
                        "optimized_transition_local_exit_checks": 0,
                    }
                )
            continue

        observed_transition = (
            descriptor_count,
            len(added),
            record["distinct_signature_count"],
            record["collision_pair_count"],
            buckets,
            len(selected),
            checks - baseline,
        )
        if observed_transition != EXPECTED_TRANSITIONS[cap]:
            raise AssertionError(
                f"M45 transition changed: {cap}, {observed_transition}"
            )
        transitions.append(
            {
                **record,
                "tracked_population_size": len(MULTIPLICATIVE_COLLISION),
                "optimized_transition_local_exit_checks": checks - baseline,
            }
        )
        if cap == PREDECESSOR_CAP:
            predecessor_sources = tuple(selected)

    if descriptor_count != len(descriptors):
        raise AssertionError("M45 descriptor accounting changed")
    if len(predecessor_sources) != 2409:
        raise AssertionError("M45 predecessor source count changed")
    if tuple(selected[len(predecessor_sources) :]) != (REPAIR_SOURCE,):
        raise AssertionError("M45 final repair source changed")
    return (
        tuple(public),
        tuple(transitions),
        predecessor_sources,
        tuple(selected),
    )


def _parse_source(
    source: str,
) -> tuple[ExceptionalSelectorDescriptor, int]:
    family, first, second, base, kind = source.split(":")
    return (
        ExceptionalSelectorDescriptor(family, int(first), int(second), int(base)),
        PRIMITIVE_EXIT_KINDS.index(kind),
    )


def _signatures(
    sources: tuple[str, ...],
    primes: tuple[int, ...],
) -> tuple[int, ...]:
    signatures = [0] * len(primes)
    for column_index, source in enumerate(sources):
        descriptor, kind_index = _parse_source(source)
        resultant = exceptional_cofactor_overlap(
            descriptor.first_factor,
            descriptor.second_factor,
            descriptor.family,
        ).cyclotomic_cofactor_resultant
        exit_bit = 1 << kind_index
        signature_bit = 1 << column_index
        for index, prime in enumerate(primes):
            if (
                _primitive_exit_mask_from_resultant(
                    descriptor,
                    prime,
                    resultant,
                )
                & exit_bit
            ):
                signatures[index] |= signature_bit
    return tuple(signatures)


def _repair_patterns() -> tuple[dict[tuple[int, ...], tuple[str, ...]], int]:
    old_keys = {
        descriptor.key
        for descriptor in diversified_exceptional_selector(
            INPUT_LENGTH,
            PREDECESSOR_CAP,
        )
    }
    patterns: defaultdict[tuple[int, ...], list[str]] = defaultdict(list)
    checks = 0
    for descriptor in diversified_exceptional_selector(
        INPUT_LENGTH,
        REPAIR_CAP,
    ):
        if descriptor.key in old_keys:
            continue
        resultant = exceptional_cofactor_overlap(
            descriptor.first_factor,
            descriptor.second_factor,
            descriptor.family,
        ).cyclotomic_cofactor_resultant
        masks = tuple(
            _primitive_exit_mask_from_resultant(descriptor, prime, resultant)
            for prime in FINAL_COLLISION
        )
        for kind_index, kind in enumerate(PRIMITIVE_EXIT_KINDS):
            pattern = tuple(
                int(bool(mask & (1 << kind_index))) for mask in masks
            )
            if len(set(pattern)) > 1:
                patterns[pattern].append(f"{descriptor.key}:{kind}")
            checks += 1
    return (
        {pattern: tuple(sources) for pattern, sources in patterns.items()},
        checks,
    )


def build_summary() -> dict[str, object]:
    """Run the exact partition, construction, and repair audit."""
    if ADDITIVE_CAP != INPUT_LENGTH + 135:
        raise AssertionError("M45 additive schedule changed")
    if MULTIPLICATIVE_CAP != (26 * INPUT_LENGTH + 4) // 5:
        raise AssertionError("M45 multiplicative schedule changed")

    primes = balanced_prime_population(INPUT_LENGTH)
    if len(primes) != 2410:
        raise AssertionError("M45 balanced population changed")
    pair_count = len(primes) * (len(primes) - 1) // 2
    public, transitions, predecessor_sources, sources = _partition_audit(primes)
    signatures = _signatures(sources, primes)
    predecessor_mask = (1 << len(predecessor_sources)) - 1
    predecessor_signatures = tuple(
        signature & predecessor_mask for signature in signatures
    )
    counts_by_signature = Counter(predecessor_signatures)
    predecessor_buckets = tuple(
        tuple(
            prime
            for prime, signature in zip(
                primes,
                predecessor_signatures,
                strict=True,
            )
            if signature == repeated
        )
        for repeated, count in counts_by_signature.items()
        if count > 1
    )
    if predecessor_buckets != (FINAL_COLLISION,):
        raise AssertionError(f"M45 predecessor changed: {predecessor_buckets}")
    if len(set(signatures)) != len(primes):
        raise AssertionError("M45 construction certificate collides")

    patterns, repair_checks = _repair_patterns()
    if patterns != {(1, 0): (REPAIR_SOURCE,)}:
        raise AssertionError(f"M45 repair patterns changed: {patterns}")
    if repair_checks != 224896:
        raise AssertionError("M45 repair-coordinate count changed")
    tracked_indices = tuple(primes.index(prime) for prime in FINAL_COLLISION)
    tracked_predecessor = tuple(
        predecessor_signatures[index] for index in tracked_indices
    )
    if len(set(tracked_predecessor)) != 1:
        raise AssertionError("M45 predecessor pair no longer collides")

    public_by_cap = {int(record["selector_cap"]): record for record in public}
    counts = {
        "input_lengths": 1,
        "public_cap_profiles": len(public),
        "transition_cap_profiles": len(transitions),
        "balanced_primes": len(primes),
        "balanced_prime_pairs": pair_count,
        "public_cap_maximum_descriptors": int(
            public_by_cap[MULTIPLICATIVE_CAP]["descriptor_count"]
        ),
        "public_partition_local_exit_checks": int(
            public_by_cap[MULTIPLICATIVE_CAP]["optimized_local_exit_checks"]
        ),
        "repair_partition_local_exit_checks": int(
            transitions[-1]["optimized_local_exit_checks"]
        ),
        "transition_new_descriptors": (
            int(transitions[-1]["descriptor_count"])
            - int(transitions[0]["descriptor_count"])
        ),
        "transition_full_local_exit_profiles": (
            (
                int(transitions[-1]["descriptor_count"])
                - int(transitions[0]["descriptor_count"])
            )
            * len(MULTIPLICATIVE_COLLISION)
        ),
        "repair_cap_descriptors": int(transitions[-1]["descriptor_count"]),
        "repair_cap_raw_coordinates": int(
            transitions[-1]["raw_coordinate_count"]
        ),
        "predecessor_coordinate_count": len(predecessor_sources),
        "minimum_new_coordinate_count": 1,
        "construction_coordinates": len(sources),
        "construction_local_exit_profiles": len(sources) * len(primes),
        "certificate_pair_checks": pair_count,
        "repair_raw_coordinate_checks": repair_checks,
    }
    summary: dict[str, object] = {
        "schema_version": "1.0.0",
        "experiment_id": "EXP-0044",
        "input_length": INPUT_LENGTH,
        "registered_public_profiles": public,
        "additive_failed_profile": public_by_cap[ADDITIVE_CAP],
        "multiplicative_failed_profile": public_by_cap[MULTIPLICATIVE_CAP],
        "transition_profiles": transitions,
        "predecessor_profile": transitions[-2],
        "repair_profile": transitions[-1],
        "exact_length_33_threshold": REPAIR_CAP,
        "partition_refinement_invariant": (
            "After each descriptor, the retained buckets are exactly the "
            "non-singleton raw-signature equivalence classes; discarded "
            "singletons cannot merge under coordinate appending."
        ),
        "construction_certificate": {
            "input_length": INPUT_LENGTH,
            "selector_cap": REPAIR_CAP,
            "primes": primes,
            "column_sources": sources,
            "restricted_signatures": signatures,
            "predecessor_column_count": len(predecessor_sources),
            "tracked_primes": FINAL_COLLISION,
            "tracked_predecessor_signatures": tracked_predecessor,
            "new_source_patterns": ((1, 0),),
            "tracked_repair_signatures": (1, 0),
            "minimum_new_coordinate_count": 1,
            "repair_sources": (REPAIR_SOURCE,),
        },
        "repaired_additive_schedule": {
            "cap": "m+162",
            "minimal_integer_offset_through_33": 162,
            "length_33_slack": 0,
        },
        "repaired_multiplicative_schedule": {
            "admissible_coefficients_through_33": "c>194/33",
            "infimum": "194/33",
            "length_33_local_endpoint": "194/33",
            "working_witness": "ceil(147m/25)",
            "witness_gap": "1/825",
            "length_33_slack": 0,
        },
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
    counts = summary["counts"]
    if not isinstance(counts, dict):
        raise AssertionError("M45 counts have the wrong shape")
    print(
        "M45 length-33 cap audit: PASS "
        f"(threshold={summary['exact_length_33_threshold']}, "
        f"summary_sha256={summary['summary_sha256']}, "
        f"construction_coordinates={counts['construction_coordinates']})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
