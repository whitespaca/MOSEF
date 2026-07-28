"""Independently validate the M35 recurrence and repair certificates."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "python"))
from mosef_reference import (
    ExceptionalSelectorDescriptor,
    diversified_exceptional_selector,
    diversified_selector_profile,
    primitive_exit_mask,
)

from scripts.check_m31_diversified_compact_signature_differential import (
    dense_exit_mask,
    dense_source_hit,
    parse_protocol,
    reconstructed_mask,
)


def run(command: list[str], env: dict[str, str] | None = None) -> str:
    """Run one verifier command and return UTF-8 stdout."""
    return subprocess.run(
        command,
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env,
    ).stdout.strip()


def main() -> int:
    """Check frozen M35 records with compact, dense, Rust, and C# paths."""
    data = json.loads(
        (ROOT / "schemas/m35-next-envelope-v1.json").read_text(
            encoding="utf-8"
        )
    )
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
    for vector in data["primitive_exit_vectors"]:
        descriptor = ExceptionalSelectorDescriptor(
            vector["family"],
            vector["first_factor"],
            vector["second_factor"],
            vector["base"],
        )
        expected_mask = primitive_exit_mask(descriptor, vector["prime"])
        if expected_mask != vector["expected_mask"]:
            raise AssertionError("registered M35 primitive mask changed")
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
            evaluation = parse_protocol(
                run(
                    [
                        *executable,
                        "exceptional-cyclotomic",
                        *evaluation_arguments,
                    ],
                    env_arg,
                )
            )
            overlap = parse_protocol(
                run(
                    [
                        *executable,
                        "exceptional-cofactor-overlap",
                        *overlap_arguments,
                    ],
                    env_arg,
                )
            )
            actual_mask = reconstructed_mask(
                evaluation,
                overlap,
                vector["base"],
                vector["prime"],
            )
            if actual_mask != expected_mask:
                raise AssertionError("M35 primitive exit disagreement")
            cross_language_checks += 2

    repaired_record = data["repair_profile"]
    repaired = diversified_selector_profile(
        data["input_length"],
        repaired_record["selector_cap"],
        compute_minimum_certificate=False,
    )
    if (
        len(repaired.population_primes)
        != repaired_record["population_size"]
        or repaired.descriptor_count != repaired_record["descriptor_count"]
        or len(repaired.normalized_columns)
        != repaired_record["normalized_coordinate_count"]
        or not repaired.injective
    ):
        raise AssertionError("registered M35 repair profile changed")

    certificate = data["construction_certificate"]
    dense_signatures = tuple(
        sum(
            1 << column_index
            for column_index, source in enumerate(
                certificate["column_sources"]
            )
            if dense_source_hit(source, prime)
        )
        for prime in certificate["primes"]
    )
    if list(dense_signatures) != certificate["restricted_signatures"]:
        raise AssertionError("dense M35 construction certificate changed")
    if len(set(dense_signatures)) != len(dense_signatures):
        raise AssertionError("dense M35 construction certificate collides")
    dense_pair_checks = (
        len(dense_signatures) * (len(dense_signatures) - 1) // 2
    )

    failed = data["failed_profile"]
    failed_bucket = failed["collision_buckets"][0]
    dense_failed_descriptor_checks = 0
    for descriptor in diversified_exceptional_selector(
        data["input_length"],
        failed["selector_cap"],
    ):
        masks = tuple(
            dense_exit_mask(descriptor, prime) for prime in failed_bucket
        )
        if len(set(masks)) != 1:
            raise AssertionError(
                "registered M35 failed-schedule bucket separated: "
                f"{descriptor.key}"
            )
        dense_failed_descriptor_checks += 1

    predecessor = data["predecessor_profile"]
    predecessor_bucket = predecessor["collision_buckets"][0]
    dense_predecessor_descriptor_checks = 0
    for descriptor in diversified_exceptional_selector(
        data["input_length"],
        predecessor["selector_cap"],
    ):
        masks = tuple(
            dense_exit_mask(descriptor, prime)
            for prime in predecessor_bucket
        )
        if len(set(masks)) != 1:
            raise AssertionError(
                "registered M35 predecessor collision separated: "
                f"{descriptor.key}"
            )
        dense_predecessor_descriptor_checks += 1

    print(
        "M35 next-envelope differential validation: PASS "
        f"({cross_language_checks} cross-language command checks, "
        f"{dense_pair_checks} dense certificate pair checks, "
        f"{dense_failed_descriptor_checks} dense failed-schedule "
        "collision-descriptor checks, "
        f"{dense_predecessor_descriptor_checks} dense predecessor "
        "collision-descriptor checks)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
