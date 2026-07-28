"""Independently validate M32 widened-cap certificates."""

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
    """Run one repository verifier command and return UTF-8 stdout."""
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
    """Check frozen profiles with compact, dense, Rust, and C# evaluators."""
    data = json.loads(
        (
            ROOT / "schemas/m32-widened-selector-cap-v1.json"
        ).read_text(encoding="utf-8")
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
    base_branch_checks = 0
    for vector in data["primitive_exit_vectors"]:
        descriptor = ExceptionalSelectorDescriptor(
            vector["family"],
            vector["first_factor"],
            vector["second_factor"],
            vector["base"],
        )
        expected_mask = primitive_exit_mask(descriptor, vector["prime"])
        if expected_mask != vector["expected_mask"]:
            raise AssertionError("registered M32 primitive mask changed")
        if vector["base"] % vector["prime"] == 0:
            if expected_mask != 1 or dense_exit_mask(
                descriptor,
                vector["prime"],
            ) != 1:
                raise AssertionError("nonunit base branch is not total")
            base_branch_checks += 1
            continue
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
                raise AssertionError(
                    "M32 primitive exit disagreement: "
                    f"{evaluation_arguments} expected={expected_mask} "
                    f"actual={actual_mask}"
                )
            cross_language_checks += 2

    profile_checks = 0
    dense_certificate_pair_checks = 0
    dense_collision_descriptor_checks = 0
    certificates = {
        certificate["input_length"]: certificate
        for certificate in data["construction_certificates"]
    }
    for record in data["threshold_records"]:
        input_length = record["input_length"]
        selector_cap = record["minimal_selector_cap"]
        profile = diversified_selector_profile(
            input_length,
            selector_cap,
            compute_minimum_certificate=False,
        )
        actual = {
            "population_size": len(profile.population_primes),
            "threshold_descriptor_count": profile.descriptor_count,
            "threshold_raw_coordinate_count": profile.raw_coordinate_count,
            "threshold_normalized_coordinate_count": len(
                profile.normalized_columns
            ),
        }
        expected = {
            key: record[key]
            for key in (
                "population_size",
                "threshold_descriptor_count",
                "threshold_raw_coordinate_count",
                "threshold_normalized_coordinate_count",
            )
        }
        if actual != expected or not profile.injective:
            raise AssertionError(
                f"registered threshold profile changed: {actual} != {expected}"
            )
        profile_checks += 1

        certificate = certificates[input_length]
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
            raise AssertionError(
                f"dense M32 certificate changed at m={input_length}"
            )
        if len(set(dense_signatures)) != len(dense_signatures):
            raise AssertionError("dense M32 certificate is not injective")
        dense_certificate_pair_checks += (
            len(dense_signatures) * (len(dense_signatures) - 1) // 2
        )

        predecessor_cap = selector_cap - 1
        collision_buckets = record["predecessor_collision_buckets"]
        for descriptor in diversified_exceptional_selector(
            input_length,
            predecessor_cap,
        ):
            for bucket in collision_buckets:
                masks = tuple(
                    dense_exit_mask(descriptor, prime) for prime in bucket
                )
                if len(set(masks)) != 1:
                    raise AssertionError(
                        "registered predecessor collision no longer collides: "
                        f"m={input_length}, cap={predecessor_cap}, "
                        f"descriptor={descriptor.key}, bucket={bucket}"
                    )
                dense_collision_descriptor_checks += 1

    print(
        "M32 widened-selector differential validation: PASS "
        f"({cross_language_checks} cross-language command checks, "
        f"{base_branch_checks} nonunit-base branch checks, "
        f"{profile_checks} threshold profile checks, "
        f"{dense_certificate_pair_checks} dense certificate pair checks, "
        f"{dense_collision_descriptor_checks} dense collision-descriptor "
        "checks)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
