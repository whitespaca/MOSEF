"""Independently validate the M44 length-32 cap certificates."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from collections import defaultdict
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


def _geometric_sum(base: int, exponent: int, prime: int) -> tuple[int, int]:
    """Evaluate a power and sum via an independent closed formula."""
    normalized = base % prime
    power = pow(normalized, exponent, prime)
    if normalized == 1:
        return power, exponent % prime
    total = (power - 1) * pow(normalized - 1, -1, prime) % prime
    return power, total


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


def independent_exit_mask(
    descriptor: ExceptionalSelectorDescriptor,
    prime: int,
) -> int:
    """Reconstruct all primitive bits without the binary production path."""
    if descriptor.base % prime == 0:
        return 1
    first_power, first_sum = _geometric_sum(
        descriptor.base,
        descriptor.first_factor,
        prime,
    )
    _, second_sum = _geometric_sum(
        first_power,
        descriptor.second_factor,
        prime,
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
    """Check every public descriptor on each registered failed bucket."""
    selector_cap = int(record["selector_cap"])  # type: ignore[arg-type]
    collision_buckets = record["collision_buckets"]
    if not isinstance(collision_buckets, list):
        raise AssertionError("M44 collision buckets have the wrong shape")
    descriptors = diversified_exceptional_selector(
        input_length,
        selector_cap,
    )
    for descriptor in descriptors:
        for bucket in collision_buckets:
            if not isinstance(bucket, list) or len(bucket) < 2:
                raise AssertionError("M44 collision bucket is malformed")
            masks = tuple(
                independent_exit_mask(descriptor, int(prime))
                for prime in bucket
            )
            if len(set(masks)) != 1:
                raise AssertionError(
                    "registered M44 collision separated: "
                    f"cap={selector_cap}, descriptor={descriptor.key}"
                )
    return len(descriptors)


def _descriptor_first_cap(
    input_length: int,
    descriptor: ExceptionalSelectorDescriptor,
) -> int:
    """Return the first selector cap containing a descriptor."""
    return max(
        input_length,
        descriptor.first_factor,
        descriptor.second_factor,
        descriptor.base,
    )


def _transition_checks(
    input_length: int,
    records: list[dict[str, object]],
) -> int:
    """Reconstruct each post-cap-148 class with independent arithmetic."""
    first = records[0]
    root_buckets = first["collision_buckets"]
    if not isinstance(root_buckets, list) or len(root_buckets) != 1:
        raise AssertionError("M44 transition root bucket changed")
    tracked = tuple(int(prime) for prime in root_buckets[0])
    repair_cap = int(
        records[-1]["selector_cap"]  # type: ignore[arg-type]
    )
    descriptors = diversified_exceptional_selector(
        input_length,
        repair_cap,
    )
    by_first_cap: defaultdict[
        int,
        list[ExceptionalSelectorDescriptor],
    ] = defaultdict(list)
    for descriptor in descriptors:
        by_first_cap[
            _descriptor_first_cap(input_length, descriptor)
        ].append(descriptor)

    signatures = {prime: bytearray() for prime in tracked}
    checks = 0
    descriptor_count = int(
        first["descriptor_count"]  # type: ignore[arg-type]
    )
    for record in records[1:]:
        cap = int(record["selector_cap"])  # type: ignore[arg-type]
        added = by_first_cap[cap]
        if len(added) != int(
            record["new_descriptor_count"]  # type: ignore[arg-type]
        ):
            raise AssertionError("independent M44 transition count changed")
        descriptor_count += len(added)
        if descriptor_count != int(
            record["descriptor_count"]  # type: ignore[arg-type]
        ):
            raise AssertionError("independent M44 cumulative count changed")
        for prime in tracked:
            signatures[prime].extend(
                independent_exit_mask(descriptor, prime)
                for descriptor in added
            )
            checks += len(added)
        grouped: defaultdict[bytes, list[int]] = defaultdict(list)
        for prime in tracked:
            grouped[bytes(signatures[prime])].append(prime)
        observed_buckets = [
            bucket for bucket in grouped.values() if len(bucket) > 1
        ]
        observed_pairs = sum(
            len(bucket) * (len(bucket) - 1) // 2
            for bucket in observed_buckets
        )
        if observed_buckets != record["collision_buckets"]:
            raise AssertionError("independent M44 transition bucket changed")
        if observed_pairs != int(
            record["collision_pair_count"]  # type: ignore[arg-type]
        ):
            raise AssertionError("independent M44 transition pairs changed")
    return checks


def _parse_source(
    source: str,
) -> tuple[ExceptionalSelectorDescriptor, int]:
    """Parse one registered primitive-coordinate source."""
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
    tracked: tuple[int, ...],
) -> tuple[int, dict[tuple[int, ...], list[str]]]:
    """Independently recover all new nonconstant final-pair coordinates."""
    old_keys = {
        descriptor.key
        for descriptor in diversified_exceptional_selector(
            input_length,
            predecessor_cap,
        )
    }
    observed: defaultdict[tuple[int, ...], list[str]] = defaultdict(list)
    checks = 0
    for descriptor in diversified_exceptional_selector(
        input_length,
        repair_cap,
    ):
        if descriptor.key in old_keys:
            continue
        masks = tuple(
            independent_exit_mask(descriptor, prime) for prime in tracked
        )
        for kind_index, kind in enumerate(PRIMITIVE_EXIT_KINDS):
            pattern = tuple(
                int(bool(mask & (1 << kind_index))) for mask in masks
            )
            if len(set(pattern)) > 1:
                observed[pattern].append(f"{descriptor.key}:{kind}")
            checks += 1
    return checks, dict(observed)


def main() -> int:
    """Check M44 records with formula, dense, Rust, and C# paths."""
    data = json.loads(
        (ROOT / "schemas/m44-length-32-cap-v1.json").read_text(
            encoding="utf-8"
        )
    )
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
        raise AssertionError("M44 canonical summary hash changed")

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
            raise AssertionError("registered M44 primitive mask changed")
        if independent_exit_mask(descriptor, vector["prime"]) != expected_mask:
            raise AssertionError("independent M44 primitive mask changed")
        if (
            protocol_reference.dense_exit_mask(descriptor, vector["prime"])
            != expected_mask
        ):
            raise AssertionError("dense M44 primitive mask changed")
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
                raise AssertionError("M44 primitive exit disagreement")
            cross_language_checks += 2

    public_collision_checks = sum(
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
        raise AssertionError("independent M44 construction changed")
    if len(set(independent_signatures)) != len(independent_signatures):
        raise AssertionError("independent M44 construction collides")
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
    if predecessor_buckets != [[59699, 63463]]:
        raise AssertionError("independent M44 predecessor changed")

    tracked = tuple(int(prime) for prime in certificate["tracked_primes"])
    repair_checks, observed_repairs = _repair_coordinate_checks(
        data["input_length"],
        int(data["predecessor_profile"]["selector_cap"]),
        int(data["repair_profile"]["selector_cap"]),
        tracked,
    )
    expected_repairs = {
        (1, 0): ["phi4:167:119:93:cofactor"],
    }
    if observed_repairs != expected_repairs:
        raise AssertionError(
            f"independent M44 repair coordinates changed: {observed_repairs}"
        )
    if data["exact_length_32_threshold"] != 167:
        raise AssertionError("M44 exact threshold changed")
    if data["repaired_additive_schedule"]["cap"] != "m+135":
        raise AssertionError("M44 additive repair changed")
    if (
        data["repaired_multiplicative_schedule"]["working_witness"]
        != "ceil(26m/5)"
    ):
        raise AssertionError("M44 multiplicative repair changed")

    print(
        "M44 length-32 cap differential validation: PASS "
        f"({cross_language_checks} cross-language command checks, "
        f"{dense_vector_checks} dense vector checks, "
        f"{public_collision_checks} public-cap descriptor checks, "
        f"{transition_checks} transition local-exit checks, "
        f"{repair_checks} repair-coordinate checks, "
        f"{certificate_pair_checks} independent certificate pair checks)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
