"""Independently validate the M45 length-33 cap certificates."""

from __future__ import annotations

import hashlib
import json
import os
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "python")]

from mosef_reference import ExceptionalSelectorDescriptor, primitive_exit_mask

from scripts import (
    check_m31_diversified_compact_signature_differential as protocol_reference,
)
from scripts.check_m44_length_32_cap_differential import (
    _parse_source,
    _repair_coordinate_checks,
    _transition_checks,
    collision_descriptor_checks,
    independent_exit_mask,
    run,
)

SCHEMA = ROOT / "schemas/m45-length-33-cap-v1.json"
FINAL_COLLISION = [80309, 92671]
REPAIR_SOURCE = "phi4:195:91:20:cofactor"


def main() -> int:
    """Check M45 records with formula, dense, Rust, and C# paths."""
    data = json.loads(SCHEMA.read_text(encoding="utf-8"))
    summary_hash = data["summary_sha256"]
    canonical = dict(data)
    canonical.pop("summary_sha256")
    canonical.pop("primitive_exit_vectors")
    recomputed_hash = hashlib.sha256(
        json.dumps(canonical, sort_keys=True, separators=(",", ":")).encode(
            "utf-8"
        )
    ).hexdigest()
    if recomputed_hash != summary_hash:
        raise AssertionError("M45 canonical summary hash changed")

    env = os.environ.copy()
    env["APPDATA"] = str(ROOT / "verification/csharp/obj/sandbox-appdata")
    run(
        [
            "cargo",
            "build",
            "--quiet",
            "-p",
            "mosef-arithmetic",
            "--bin",
            "mosef-baseline",
        ]
    )
    run(
        [
            "dotnet",
            "build",
            "verification/csharp/MosefVerifier.csproj",
            "--nologo",
            "--no-restore",
            "--verbosity",
            "quiet",
        ],
        env,
    )
    rust = ROOT / "target/debug/mosef-baseline.exe"
    csharp = [
        "dotnet",
        str(ROOT / "verification/csharp/bin/Debug/net8.0/MosefVerifier.dll"),
    ]

    cross_language_checks = 0
    dense_vector_checks = 0
    for vector in data["primitive_exit_vectors"]:
        descriptor = ExceptionalSelectorDescriptor(
            vector["family"],
            vector["first_factor"],
            vector["second_factor"],
            vector["base"],
        )
        expected_mask = primitive_exit_mask(descriptor, vector["prime"])
        if expected_mask != vector["expected_mask"]:
            raise AssertionError("registered M45 primitive mask changed")
        if independent_exit_mask(descriptor, vector["prime"]) != expected_mask:
            raise AssertionError("independent M45 primitive mask changed")
        if (
            protocol_reference.dense_exit_mask(descriptor, vector["prime"])
            != expected_mask
        ):
            raise AssertionError("dense M45 primitive mask changed")
        dense_vector_checks += 1
        evaluation_arguments = [
            str(vector["base"]),
            str(vector["prime"]),
            str(vector["first_factor"]),
            str(vector["second_factor"]),
            vector["family"],
        ]
        overlap_arguments = [
            str(vector["first_factor"]),
            str(vector["second_factor"]),
            vector["family"],
        ]
        for executable, env_arg in (([str(rust)], None), (csharp, env)):
            evaluation = protocol_reference.parse_protocol(
                run(
                    [
                        *executable,
                        "exceptional-cyclotomic",
                        *evaluation_arguments,
                    ],
                    env_arg,
                )
            )
            overlap = protocol_reference.parse_protocol(
                run(
                    [
                        *executable,
                        "exceptional-cofactor-overlap",
                        *overlap_arguments,
                    ],
                    env_arg,
                )
            )
            actual_mask = protocol_reference.reconstructed_mask(
                evaluation,
                overlap,
                vector["base"],
                vector["prime"],
            )
            if actual_mask != expected_mask:
                raise AssertionError("M45 primitive exit disagreement")
            cross_language_checks += 2

    public_descriptor_checks = sum(
        collision_descriptor_checks(data["input_length"], record)
        for record in data["registered_public_profiles"]
    )
    transition_checks = _transition_checks(
        data["input_length"],
        data["transition_profiles"],
    )

    certificate = data["construction_certificate"]
    parsed_sources = tuple(
        _parse_source(source) for source in certificate["column_sources"]
    )
    independent_signatures = tuple(
        sum(
            1 << column_index
            for column_index, (descriptor, kind_index) in enumerate(
                parsed_sources
            )
            if independent_exit_mask(descriptor, int(prime))
            & (1 << kind_index)
        )
        for prime in certificate["primes"]
    )
    if list(independent_signatures) != certificate["restricted_signatures"]:
        raise AssertionError("independent M45 construction changed")
    if len(set(independent_signatures)) != len(independent_signatures):
        raise AssertionError("independent M45 construction collides")
    certificate_pair_checks = (
        len(independent_signatures)
        * (len(independent_signatures) - 1)
        // 2
    )
    predecessor_mask = (
        1 << int(certificate["predecessor_column_count"])
    ) - 1
    predecessor_groups: defaultdict[int, list[int]] = defaultdict(list)
    for prime, signature in zip(
        certificate["primes"],
        independent_signatures,
        strict=True,
    ):
        predecessor_groups[signature & predecessor_mask].append(int(prime))
    predecessor_buckets = [
        bucket
        for bucket in predecessor_groups.values()
        if len(bucket) > 1
    ]
    if predecessor_buckets != [FINAL_COLLISION]:
        raise AssertionError("independent M45 predecessor changed")

    tracked = tuple(int(prime) for prime in certificate["tracked_primes"])
    repair_checks, observed_repairs = _repair_coordinate_checks(
        data["input_length"],
        int(data["predecessor_profile"]["selector_cap"]),
        int(data["repair_profile"]["selector_cap"]),
        tracked,
    )
    if observed_repairs != {(1, 0): [REPAIR_SOURCE]}:
        raise AssertionError(
            f"independent M45 repair coordinates changed: {observed_repairs}"
        )
    if data["exact_length_33_threshold"] != 195:
        raise AssertionError("M45 exact threshold changed")
    if data["repaired_additive_schedule"]["cap"] != "m+162":
        raise AssertionError("M45 additive repair changed")
    if (
        data["repaired_multiplicative_schedule"]["working_witness"]
        != "ceil(147m/25)"
    ):
        raise AssertionError("M45 multiplicative repair changed")

    print(
        "M45 length-33 cap differential validation: PASS "
        f"({cross_language_checks} cross-language command checks, "
        f"{dense_vector_checks} dense vector checks, "
        f"{public_descriptor_checks} public-cap descriptor checks, "
        f"{transition_checks} transition local-exit checks, "
        f"{repair_checks} repair-coordinate checks, "
        f"{certificate_pair_checks} independent certificate pair checks)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
