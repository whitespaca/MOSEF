"""Independently validate the M41 length-29 cap certificates."""

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
    exceptional_cofactor_coefficients,
    primitive_exit_mask,
)
from mosef_reference.diversified_compact_signatures import (
    PRIMITIVE_EXIT_KINDS,
)

from scripts import (
    check_m31_diversified_compact_signature_differential as protocol_reference,
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


def _naive_power_sum(base: int, prime: int, exponent: int) -> tuple[int, int]:
    """Evaluate a power and geometric sum by literal repeated multiplication."""
    term = 1
    total = 0
    for _ in range(exponent):
        total = (total + term) % prime
        term = term * base % prime
    return term, total


def _dense_polynomial_residue(
    coefficients: tuple[int, ...],
    base: int,
    prime: int,
) -> int:
    """Evaluate a materialized polynomial by Horner's rule."""
    result = 0
    for coefficient in reversed(coefficients):
        result = (result * base + coefficient) % prime
    return result


@cache
def independent_exit_mask(
    descriptor: ExceptionalSelectorDescriptor,
    prime: int,
) -> int:
    """Reconstruct all primitive bits without the production binary evaluator."""
    if descriptor.base % prime == 0:
        return 1
    first_power, first_sum = _naive_power_sum(
        descriptor.base,
        prime,
        descriptor.first_factor,
    )
    _, second_sum = _naive_power_sum(
        first_power,
        prime,
        descriptor.second_factor,
    )
    if descriptor.family == "phi4":
        first_coefficient = 1
        cyclotomic = (
            descriptor.base * descriptor.base + 1
        ) % prime
        constant = (
            descriptor.first_factor * (descriptor.second_factor + 2) + 1
        ) // 4
        linear = (
            descriptor.first_factor * (descriptor.second_factor - 2) + 1
        ) // 4
        resultant = constant * constant + linear * linear
    else:
        first_coefficient = 2
        cyclotomic = (
            descriptor.base * descriptor.base - descriptor.base + 1
        ) % prime
        residual = (
            descriptor.first_factor * (descriptor.second_factor - 2) + 1
        )
        constant = -(2 * residual // 3)
        linear = (
            descriptor.first_factor * (descriptor.second_factor + 4) + 4
        ) // 3
        resultant = (
            constant * constant + constant * linear + linear * linear
        )
    aggregate = (
        first_coefficient * first_sum + second_sum
    ) % prime
    cofactor = (
        aggregate == 0
        if cyclotomic != 0
        else _dense_polynomial_residue(
            exceptional_cofactor_coefficients(
                descriptor.first_factor,
                descriptor.second_factor,
                descriptor.family,
            ),
            descriptor.base,
            prime,
        )
        == 0
    )
    support = (
        False,
        first_sum == 0,
        second_sum == 0,
        descriptor.second_factor % prime == 0,
        first_coefficient * descriptor.second_factor % prime == 0,
        cyclotomic == 0,
        resultant % prime == 0,
        cofactor,
    )
    if (aggregate == 0) != (support[5] or support[7]):
        raise AssertionError("independent aggregate support is inconsistent")
    return sum(1 << index for index, hit in enumerate(support) if hit)


def collision_descriptor_checks(
    input_length: int,
    record: dict[str, object],
) -> int:
    """Check that every predecessor descriptor preserves its collision."""
    selector_cap = int(record["selector_cap"])
    collision_buckets = record["collision_buckets"]
    if not isinstance(collision_buckets, list) or len(collision_buckets) != 1:
        raise AssertionError("M41 predecessor must have one collision bucket")
    bucket = collision_buckets[0]
    if not isinstance(bucket, list) or len(bucket) != 2:
        raise AssertionError("M41 predecessor collision must be one pair")

    checks = 0
    for descriptor in diversified_exceptional_selector(
        input_length,
        selector_cap,
    ):
        masks = tuple(
            independent_exit_mask(descriptor, int(prime))
            for prime in bucket
        )
        if len(set(masks)) != 1:
            raise AssertionError(
                "registered M41 predecessor separated: "
                f"descriptor={descriptor.key}"
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


def _repair_coordinate_checks(
    input_length: int,
    predecessor_cap: int,
    repair_cap: int,
    pair: tuple[int, int],
    expected_source: str,
) -> int:
    """Independently recover every new coordinate that splits the pair."""
    old_keys = {
        descriptor.key
        for descriptor in diversified_exceptional_selector(
            input_length,
            predecessor_cap,
        )
    }
    observed: list[str] = []
    checks = 0
    for descriptor in diversified_exceptional_selector(
        input_length,
        repair_cap,
    ):
        if descriptor.key in old_keys:
            continue
        masks = tuple(
            independent_exit_mask(descriptor, prime) for prime in pair
        )
        for kind_index, kind in enumerate(PRIMITIVE_EXIT_KINDS):
            pattern = tuple(
                int(bool(mask & (1 << kind_index))) for mask in masks
            )
            if pattern[0] != pattern[1]:
                observed.append(f"{descriptor.key}:{kind}")
            checks += 1
    if observed != [expected_source]:
        raise AssertionError(
            f"independent M41 repair coordinates changed: {observed}"
        )
    return checks


def main() -> int:
    """Check frozen M41 records with naive, dense, Rust, and C# paths."""
    data = json.loads(
        (ROOT / "schemas/m41-length-29-cap-v1.json").read_text(
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
            raise AssertionError("registered M41 primitive mask changed")
        if independent_exit_mask(descriptor, vector["prime"]) != expected_mask:
            raise AssertionError("independent M41 primitive mask changed")
        if (
            protocol_reference.dense_exit_mask(descriptor, vector["prime"])
            != expected_mask
        ):
            raise AssertionError("dense M41 primitive mask changed")
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
                raise AssertionError("M41 primitive exit disagreement")
            cross_language_checks += 2

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
        raise AssertionError("independent M41 construction changed")
    if len(set(independent_signatures)) != len(independent_signatures):
        raise AssertionError("independent M41 construction collides")
    certificate_pair_checks = (
        len(independent_signatures)
        * (len(independent_signatures) - 1)
        // 2
    )

    predecessor_checks = collision_descriptor_checks(
        data["input_length"],
        data["predecessor_profile"],
    )
    tracked = tuple(int(prime) for prime in certificate["tracked_primes"])
    if len(tracked) != 2:
        raise AssertionError("M41 tracked predecessor shape changed")
    repair_coordinate_checks = _repair_coordinate_checks(
        data["input_length"],
        int(data["predecessor_profile"]["selector_cap"]),
        int(data["repair_profile"]["selector_cap"]),
        tracked,
        certificate["unique_new_pair_source"],
    )

    repair_keys = {
        descriptor.key
        for descriptor in diversified_exceptional_selector(
            data["input_length"],
            data["repair_profile"]["selector_cap"],
        )
    }
    schedule_inclusion_checks = 0
    for profile_name in (
        "additive_success_profile",
        "multiplicative_success_profile",
    ):
        schedule_keys = {
            descriptor.key
            for descriptor in diversified_exceptional_selector(
                data["input_length"],
                data[profile_name]["selector_cap"],
            )
        }
        if not repair_keys <= schedule_keys:
            raise AssertionError("M41 successful schedule lost repair selector")
        if len(schedule_keys) != data[profile_name]["descriptor_count"]:
            raise AssertionError("M41 successful schedule count changed")
        schedule_inclusion_checks += len(repair_keys)

    print(
        "M41 length-29 cap differential validation: PASS "
        f"({cross_language_checks} cross-language command checks, "
        f"{dense_vector_checks} dense vector checks, "
        f"{certificate_pair_checks} independent certificate pair checks, "
        f"{predecessor_checks} independent predecessor descriptor checks, "
        f"{repair_coordinate_checks} independent repair-coordinate checks, "
        f"{schedule_inclusion_checks} independent schedule-inclusion checks)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
