"""Independently validate the M39 length-27 cap certificates."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from functools import cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "python"))
from mosef_reference import (
    ExceptionalSelectorDescriptor,
    diversified_exceptional_selector,
    primitive_exit_mask,
)
from mosef_reference.diversified_compact_signatures import (
    PRIMITIVE_EXIT_KINDS,
)

from scripts import (
    check_m31_diversified_compact_signature_differential as dense_reference,
)

dense_reference.exceptional_cofactor_coefficients = cache(
    dense_reference.exceptional_cofactor_coefficients
)
cached_dense_exit_mask = cache(dense_reference.dense_exit_mask)


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


def dense_collision_descriptor_checks(
    input_length: int,
    record: dict[str, object],
) -> int:
    """Check that every descriptor preserves one registered collision bucket."""
    selector_cap = int(record["selector_cap"])
    collision_buckets = record["collision_buckets"]
    if not isinstance(collision_buckets, list) or len(collision_buckets) != 1:
        raise AssertionError("M39 failed profile must have one collision bucket")
    bucket = collision_buckets[0]
    if not isinstance(bucket, list):
        raise AssertionError("M39 collision bucket has invalid shape")

    checks = 0
    for descriptor in diversified_exceptional_selector(
        input_length,
        selector_cap,
    ):
        masks = tuple(
            cached_dense_exit_mask(descriptor, int(prime)) for prime in bucket
        )
        if len(set(masks)) != 1:
            raise AssertionError(
                "registered M39 collision separated: "
                f"cap={selector_cap}, descriptor={descriptor.key}"
            )
        checks += 1
    return checks


def _parse_source(
    source: str,
) -> tuple[ExceptionalSelectorDescriptor, int]:
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


def main() -> int:
    """Check frozen M39 records with dense, Rust, and C# paths."""
    data = json.loads(
        (ROOT / "schemas/m39-length-27-cap-v1.json").read_text(
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
            raise AssertionError("registered M39 primitive mask changed")
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
            evaluation = dense_reference.parse_protocol(
                run(
                    [
                        *executable,
                        "exceptional-cyclotomic",
                        *evaluation_arguments,
                    ],
                    env_arg,
                )
            )
            overlap = dense_reference.parse_protocol(
                run(
                    [
                        *executable,
                        "exceptional-cofactor-overlap",
                        *overlap_arguments,
                    ],
                    env_arg,
                )
            )
            actual_mask = dense_reference.reconstructed_mask(
                evaluation,
                overlap,
                vector["base"],
                vector["prime"],
            )
            if actual_mask != expected_mask:
                raise AssertionError("M39 primitive exit disagreement")
            cross_language_checks += 2

    certificate = data["construction_certificate"]
    parsed_sources = tuple(
        _parse_source(source) for source in certificate["column_sources"]
    )
    dense_signatures = tuple(
        sum(
            1 << column_index
            for column_index, (descriptor, kind_index) in enumerate(
                parsed_sources
            )
            if cached_dense_exit_mask(descriptor, int(prime))
            & (1 << kind_index)
        )
        for prime in certificate["primes"]
    )
    if list(dense_signatures) != certificate["restricted_signatures"]:
        raise AssertionError("dense M39 construction certificate changed")
    if len(set(dense_signatures)) != len(dense_signatures):
        raise AssertionError("dense M39 construction certificate collides")
    dense_pair_checks = (
        len(dense_signatures) * (len(dense_signatures) - 1) // 2
    )

    dense_additive_checks = dense_collision_descriptor_checks(
        data["input_length"],
        data["additive_failed_profile"],
    )
    dense_multiplicative_checks = dense_collision_descriptor_checks(
        data["input_length"],
        data["multiplicative_failed_profile"],
    )
    dense_predecessor_checks = dense_collision_descriptor_checks(
        data["input_length"],
        data["predecessor_profile"],
    )

    print(
        "M39 length-27 cap differential validation: PASS "
        f"({cross_language_checks} cross-language command checks, "
        f"{dense_pair_checks} dense certificate pair checks, "
        f"{dense_additive_checks} dense additive-cap checks, "
        f"{dense_multiplicative_checks} dense multiplicative-cap checks, "
        f"{dense_predecessor_checks} dense predecessor checks)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
