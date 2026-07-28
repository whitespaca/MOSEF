"""Deterministic M44 audit of the length-32 finite envelope."""

from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "python"))

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

INPUT_LENGTH = 32
ADDITIVE_CAP = 145
MULTIPLICATIVE_CAP = 148
PREDECESSOR_CAP = 166
REPAIR_CAP = 167
ADDITIVE_COLLISION = (
    46549,
    51599,
    53887,
    54049,
    57859,
    58031,
    59651,
    59699,
    61673,
    61861,
    62201,
    62743,
    63463,
    64037,
)
MULTIPLICATIVE_COLLISION = (
    46549,
    53887,
    59651,
    59699,
    61673,
    63463,
)
FINAL_COLLISION = (59699, 63463)
REPAIR_SOURCE = "phi4:167:119:93:cofactor"

# descriptor count, distinct signatures, pairs, bucket, selected sources,
# cumulative optimized local-exit evaluations
EXPECTED_PUBLIC_PROFILES = {
    ADDITIVE_CAP: (
        264384,
        1737,
        91,
        (ADDITIVE_COLLISION,),
        1736,
        81933566,
    ),
    MULTIPLICATIVE_CAP: (
        284004,
        1745,
        15,
        (MULTIPLICATIVE_COLLISION,),
        1744,
        82130579,
    ),
}

# descriptor count, new descriptors, distinct signatures, pairs, bucket,
# selected sources, optimized local-exit evaluations after cap 148
EXPECTED_TRANSITIONS = {
    149: (
        289636,
        5632,
        1746,
        10,
        ((53887, 59651, 59699, 61673, 63463),),
        1745,
        29216,
    ),
    150: (
        291593,
        1957,
        1746,
        10,
        ((53887, 59651, 59699, 61673, 63463),),
        1745,
        39001,
    ),
    151: (
        304650,
        13057,
        1746,
        10,
        ((53887, 59651, 59699, 61673, 63463),),
        1745,
        104286,
    ),
    152: (
        306681,
        2031,
        1746,
        10,
        ((53887, 59651, 59699, 61673, 63463),),
        1745,
        114441,
    ),
    153: (
        312512,
        5831,
        1747,
        6,
        ((53887, 59699, 61673, 63463),),
        1746,
        140566,
    ),
    154: (
        314568,
        2056,
        1747,
        6,
        ((53887, 59699, 61673, 63463),),
        1746,
        148790,
    ),
    155: (
        332332,
        17764,
        1747,
        6,
        ((53887, 59699, 61673, 63463),),
        1746,
        219846,
    ),
    156: (
        334490,
        2158,
        1748,
        3,
        ((59699, 61673, 63463),),
        1747,
        227439,
    ),
    157: (
        336648,
        2158,
        1748,
        3,
        ((59699, 61673, 63463),),
        1747,
        233913,
    ),
    158: (
        338806,
        2158,
        1748,
        3,
        ((59699, 61673, 63463),),
        1747,
        240387,
    ),
    159: (
        357396,
        18590,
        1749,
        1,
        (FINAL_COLLISION,),
        1748,
        285482,
    ),
    160: (
        359658,
        2262,
        1749,
        1,
        (FINAL_COLLISION,),
        1748,
        290006,
    ),
    161: (
        366240,
        6582,
        1749,
        1,
        (FINAL_COLLISION,),
        1748,
        303170,
    ),
    162: (
        368529,
        2289,
        1749,
        1,
        (FINAL_COLLISION,),
        1748,
        307748,
    ),
    163: (
        383778,
        15249,
        1749,
        1,
        (FINAL_COLLISION,),
        1748,
        338246,
    ),
    164: (
        386147,
        2369,
        1749,
        1,
        (FINAL_COLLISION,),
        1748,
        342984,
    ),
    165: (
        392944,
        6797,
        1749,
        1,
        (FINAL_COLLISION,),
        1748,
        356578,
    ),
    166: (
        395340,
        2396,
        1749,
        1,
        (FINAL_COLLISION,),
        1748,
        361370,
    ),
    167: (
        415996,
        20656,
        1750,
        0,
        (),
        1749,
        388074,
    ),
}


def _descriptor_first_cap(descriptor: ExceptionalSelectorDescriptor) -> int:
    """Return the first public cap containing one descriptor."""
    return max(
        INPUT_LENGTH,
        descriptor.first_factor,
        descriptor.second_factor,
        descriptor.base,
    )


def _refine_partition(
    buckets: tuple[tuple[int, ...], ...],
    descriptor: ExceptionalSelectorDescriptor,
) -> tuple[tuple[tuple[int, ...], ...], tuple[str, ...], int]:
    """Split every live equality class and return exact primitive witnesses."""
    resultant = exceptional_cofactor_overlap(
        descriptor.first_factor,
        descriptor.second_factor,
        descriptor.family,
    ).cyclotomic_cofactor_resultant
    refined: list[tuple[int, ...]] = []
    variable_kinds: set[int] = set()
    local_exit_checks = 0
    for bucket in buckets:
        grouped: defaultdict[int, list[int]] = defaultdict(list)
        observed_masks: list[int] = []
        for prime in bucket:
            mask = _primitive_exit_mask_from_resultant(
                descriptor,
                prime,
                resultant,
            )
            observed_masks.append(mask)
            grouped[mask].append(prime)
            local_exit_checks += 1
        if len(grouped) > 1:
            variable_kinds.update(
                kind_index
                for kind_index in range(len(PRIMITIVE_EXIT_KINDS))
                if len(
                    {
                        bool(mask & (1 << kind_index))
                        for mask in observed_masks
                    }
                )
                > 1
            )
        refined.extend(
            tuple(group) for group in grouped.values() if len(group) > 1
        )
    sources = tuple(
        f"{descriptor.key}:{PRIMITIVE_EXIT_KINDS[kind_index]}"
        for kind_index in range(len(PRIMITIVE_EXIT_KINDS))
        if kind_index in variable_kinds
    )
    return tuple(refined), sources, local_exit_checks


def _profile_record(
    cap: int,
    descriptor_count: int,
    new_descriptor_count: int,
    population_size: int,
    buckets: tuple[tuple[int, ...], ...],
    selected_source_count: int,
    local_exit_checks: int,
) -> dict[str, object]:
    """Build one exact equality-partition profile."""
    collision_pairs = sum(
        len(bucket) * (len(bucket) - 1) // 2 for bucket in buckets
    )
    distinct = population_size - sum(len(bucket) - 1 for bucket in buckets)
    return {
        "selector_cap": cap,
        "population_size": population_size,
        "descriptor_count": descriptor_count,
        "new_descriptor_count": new_descriptor_count,
        "raw_coordinate_count": (
            descriptor_count * len(PRIMITIVE_EXIT_KINDS)
        ),
        "distinct_signature_count": distinct,
        "collision_pair_count": collision_pairs,
        "maximum_bucket_size": max(
            (len(bucket) for bucket in buckets),
            default=1,
        ),
        "collision_buckets": buckets,
        "selected_coordinate_count": selected_source_count,
        "optimized_local_exit_checks": local_exit_checks,
    }


def _complete_partition_audit(
    primes: tuple[int, ...],
) -> tuple[
    tuple[dict[str, object], ...],
    tuple[dict[str, object], ...],
    tuple[str, ...],
    tuple[str, ...],
]:
    """Refine exact descriptor equivalence classes through cap 167."""
    descriptors = diversified_exceptional_selector(
        INPUT_LENGTH,
        REPAIR_CAP,
    )
    by_first_cap: defaultdict[
        int,
        list[ExceptionalSelectorDescriptor],
    ] = defaultdict(list)
    for descriptor in descriptors:
        by_first_cap[_descriptor_first_cap(descriptor)].append(descriptor)

    buckets: tuple[tuple[int, ...], ...] = (primes,)
    selected_sources: list[str] = []
    public_records: list[dict[str, object]] = []
    transition_records: list[dict[str, object]] = []
    descriptor_count = 0
    local_exit_checks = 0
    public_check_baseline = 0
    predecessor_sources: tuple[str, ...] = ()
    selected_caps = set(EXPECTED_PUBLIC_PROFILES) | set(
        EXPECTED_TRANSITIONS
    )
    for cap in range(INPUT_LENGTH, REPAIR_CAP + 1):
        added = by_first_cap[cap]
        for descriptor in added:
            buckets, sources, checks = _refine_partition(
                buckets,
                descriptor,
            )
            selected_sources.extend(sources)
            local_exit_checks += checks
        descriptor_count += len(added)
        if cap not in selected_caps:
            continue

        record = _profile_record(
            cap,
            descriptor_count,
            len(added),
            len(primes),
            buckets,
            len(selected_sources),
            local_exit_checks,
        )
        observed = (
            descriptor_count,
            int(record["distinct_signature_count"]),
            int(record["collision_pair_count"]),
            buckets,
            len(selected_sources),
            local_exit_checks,
        )
        if cap in EXPECTED_PUBLIC_PROFILES:
            if observed != EXPECTED_PUBLIC_PROFILES[cap]:
                raise AssertionError(
                    f"registered M44 public profile changed: {cap}, "
                    f"{observed}"
                )
            public_records.append(record)
            if cap == MULTIPLICATIVE_CAP:
                public_check_baseline = local_exit_checks
                transition_records.append(
                    {
                        **record,
                        "new_descriptor_count": 0,
                        "tracked_population_size": len(
                            MULTIPLICATIVE_COLLISION
                        ),
                        "optimized_transition_local_exit_checks": 0,
                    }
                )
            continue

        expected = EXPECTED_TRANSITIONS[cap]
        transition_observed = (
            descriptor_count,
            len(added),
            int(record["distinct_signature_count"]),
            int(record["collision_pair_count"]),
            buckets,
            len(selected_sources),
            local_exit_checks - public_check_baseline,
        )
        if transition_observed != expected:
            raise AssertionError(
                f"registered M44 transition changed: {cap}, "
                f"{transition_observed}"
            )
        transition_records.append(
            {
                **record,
                "tracked_population_size": len(
                    MULTIPLICATIVE_COLLISION
                ),
                "optimized_transition_local_exit_checks": (
                    local_exit_checks - public_check_baseline
                ),
            }
        )
        if cap == PREDECESSOR_CAP:
            predecessor_sources = tuple(selected_sources)

    if descriptor_count != len(descriptors):
        raise AssertionError("M44 descriptor inclusion accounting changed")
    if len(predecessor_sources) != 1748:
        raise AssertionError("M44 predecessor source count changed")
    if tuple(selected_sources[len(predecessor_sources) :]) != (
        REPAIR_SOURCE,
    ):
        raise AssertionError("M44 final repair source changed")
    return (
        tuple(public_records),
        tuple(transition_records),
        predecessor_sources,
        tuple(selected_sources),
    )


def _parse_source(
    source: str,
) -> tuple[ExceptionalSelectorDescriptor, int]:
    """Parse one canonical primitive-coordinate source."""
    family, first, second, base, kind = source.split(":")
    return (
        ExceptionalSelectorDescriptor(
            family,
            int(first),
            int(second),
            int(base),
        ),
        PRIMITIVE_EXIT_KINDS.index(kind),
    )


def _certificate_signatures(
    sources: tuple[str, ...],
    primes: tuple[int, ...],
) -> tuple[int, ...]:
    """Evaluate a compact explicit coordinate certificate on all primes."""
    signatures = [0] * len(primes)
    for column_index, source in enumerate(sources):
        descriptor, kind_index = _parse_source(source)
        resultant = exceptional_cofactor_overlap(
            descriptor.first_factor,
            descriptor.second_factor,
            descriptor.family,
        ).cyclotomic_cofactor_resultant
        signature_bit = 1 << column_index
        exit_bit = 1 << kind_index
        for prime_index, prime in enumerate(primes):
            if (
                _primitive_exit_mask_from_resultant(
                    descriptor,
                    prime,
                    resultant,
                )
                & exit_bit
            ):
                signatures[prime_index] |= signature_bit
    return tuple(signatures)


def _repair_patterns() -> tuple[
    dict[tuple[int, ...], tuple[str, ...]],
    int,
]:
    """Audit every cap-167 primitive coordinate on the last failed pair."""
    old_keys = {
        descriptor.key
        for descriptor in diversified_exceptional_selector(
            INPUT_LENGTH,
            PREDECESSOR_CAP,
        )
    }
    patterns: defaultdict[tuple[int, ...], list[str]] = defaultdict(list)
    raw_checks = 0
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
            _primitive_exit_mask_from_resultant(
                descriptor,
                prime,
                resultant,
            )
            for prime in FINAL_COLLISION
        )
        for kind_index, kind in enumerate(PRIMITIVE_EXIT_KINDS):
            pattern = tuple(
                int(bool(mask & (1 << kind_index))) for mask in masks
            )
            if len(set(pattern)) > 1:
                patterns[pattern].append(f"{descriptor.key}:{kind}")
            raw_checks += 1
    return (
        {
            pattern: tuple(sources)
            for pattern, sources in patterns.items()
        },
        raw_checks,
    )


def build_summary() -> dict[str, object]:
    """Run the exact partition, construction, and repair audit."""
    if ADDITIVE_CAP != INPUT_LENGTH + 113:
        raise AssertionError("registered M44 additive schedule changed")
    if MULTIPLICATIVE_CAP != (60 * INPUT_LENGTH + 12) // 13:
        raise AssertionError("registered M44 multiplicative schedule changed")

    primes = balanced_prime_population(INPUT_LENGTH)
    if len(primes) != 1750:
        raise AssertionError("registered M44 balanced population changed")
    pair_count = len(primes) * (len(primes) - 1) // 2
    (
        public_profiles,
        transitions,
        predecessor_sources,
        construction_sources,
    ) = _complete_partition_audit(primes)

    signatures = _certificate_signatures(construction_sources, primes)
    predecessor_mask = (1 << len(predecessor_sources)) - 1
    predecessor_signatures = tuple(
        signature & predecessor_mask for signature in signatures
    )
    predecessor_counts = Counter(predecessor_signatures)
    predecessor_buckets = tuple(
        tuple(
            prime
            for prime, signature in zip(primes, predecessor_signatures, strict=True)
            if signature == repeated
        )
        for repeated, count in predecessor_counts.items()
        if count > 1
    )
    if predecessor_buckets != (FINAL_COLLISION,):
        raise AssertionError(
            f"M44 predecessor construction changed: {predecessor_buckets}"
        )
    if len(set(signatures)) != len(primes):
        raise AssertionError("M44 construction certificate is not injective")

    patterns, repair_raw_checks = _repair_patterns()
    expected_patterns = {(1, 0): (REPAIR_SOURCE,)}
    if patterns != expected_patterns:
        raise AssertionError(
            f"registered M44 repair patterns changed: {patterns}"
        )
    if repair_raw_checks != 165248:
        raise AssertionError("M44 repair raw-coordinate count changed")
    tracked_indices = tuple(primes.index(prime) for prime in FINAL_COLLISION)
    tracked_predecessor = tuple(
        predecessor_signatures[index] for index in tracked_indices
    )
    if len(set(tracked_predecessor)) != 1:
        raise AssertionError("M44 predecessor pair no longer collides")
    tracked_repair = expected_patterns.popitem()[0]
    if tracked_repair != (1, 0):
        raise AssertionError("M44 repair signatures changed")

    public_by_cap = {
        int(record["selector_cap"]): record for record in public_profiles
    }
    counts = {
        "input_lengths": 1,
        "public_cap_profiles": len(public_profiles),
        "transition_cap_profiles": len(transitions),
        "balanced_primes": len(primes),
        "balanced_prime_pairs": pair_count,
        "public_cap_maximum_descriptors": int(
            public_by_cap[MULTIPLICATIVE_CAP]["descriptor_count"]
        ),
        "public_partition_local_exit_checks": int(
            public_by_cap[MULTIPLICATIVE_CAP][
                "optimized_local_exit_checks"
            ]
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
        "repair_cap_descriptors": int(
            transitions[-1]["descriptor_count"]
        ),
        "repair_cap_raw_coordinates": (
            int(transitions[-1]["descriptor_count"])
            * len(PRIMITIVE_EXIT_KINDS)
        ),
        "predecessor_coordinate_count": len(predecessor_sources),
        "minimum_new_coordinate_count": 1,
        "construction_coordinates": len(construction_sources),
        "construction_local_exit_profiles": (
            len(construction_sources) * len(primes)
        ),
        "certificate_pair_checks": pair_count,
        "repair_raw_coordinate_checks": repair_raw_checks,
    }
    summary: dict[str, object] = {
        "schema_version": "1.0.0",
        "experiment_id": "EXP-0043",
        "input_length": INPUT_LENGTH,
        "registered_public_profiles": public_profiles,
        "additive_failed_profile": public_by_cap[ADDITIVE_CAP],
        "multiplicative_failed_profile": public_by_cap[
            MULTIPLICATIVE_CAP
        ],
        "transition_profiles": transitions,
        "predecessor_profile": transitions[-2],
        "repair_profile": transitions[-1],
        "exact_length_32_threshold": REPAIR_CAP,
        "partition_refinement_invariant": (
            "After each descriptor, the retained buckets are exactly the "
            "non-singleton raw-signature equivalence classes; discarded "
            "singletons cannot merge under coordinate appending."
        ),
        "construction_certificate": {
            "input_length": INPUT_LENGTH,
            "selector_cap": REPAIR_CAP,
            "primes": primes,
            "column_sources": construction_sources,
            "restricted_signatures": signatures,
            "predecessor_column_count": len(predecessor_sources),
            "tracked_primes": FINAL_COLLISION,
            "tracked_predecessor_signatures": tracked_predecessor,
            "new_source_patterns": ((1, 0),),
            "tracked_repair_signatures": tracked_repair,
            "minimum_new_coordinate_count": 1,
            "repair_sources": (REPAIR_SOURCE,),
        },
        "repaired_additive_schedule": {
            "cap": "m+135",
            "minimal_integer_offset_through_32": 135,
            "length_32_slack": 0,
        },
        "repaired_multiplicative_schedule": {
            "admissible_coefficients_through_32": "c>83/16",
            "infimum": "83/16",
            "length_32_local_endpoint": "83/16",
            "working_witness": "ceil(26m/5)",
            "witness_gap": "1/80",
            "length_32_slack": 0,
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
    """Print the registered M44 summary."""
    print(json.dumps(build_summary(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
