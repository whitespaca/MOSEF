"""Differentially check selected M31 primitive exit coordinates."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
from mosef_reference import (
    ExceptionalSelectorDescriptor,
    diversified_exceptional_selector,
    diversified_selector_profile,
    exceptional_cofactor_coefficients,
    primitive_exit_mask,
)


def run(command: list[str], env: dict[str, str] | None = None) -> str:
    return subprocess.run(
        command,
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env,
    ).stdout.strip()


def parse_protocol(record: str) -> dict[str, str]:
    return dict(item.split(":", 1) for item in record.split("|"))


def reconstructed_mask(
    evaluation: dict[str, str],
    overlap: dict[str, str],
    base: int,
    prime: int,
) -> int:
    support = (
        base % prime == 0,
        int(evaluation["first_quotient_gcd"]) == prime,
        int(evaluation["second_quotient_gcd"]) == prime,
        int(evaluation["first_public_bound_gcd"]) == prime,
        int(evaluation["second_public_bound_gcd"]) == prime,
        int(evaluation["cyclotomic_gcd"]) == prime,
        int(overlap["cyclotomic_cofactor_resultant"]) % prime == 0,
        int(evaluation["cofactor_gcd"]) == prime,
    )
    aggregate_hit = int(evaluation["aggregate_gcd"]) == prime
    if aggregate_hit != (support[5] or support[7]):
        raise AssertionError("independent aggregate support is inconsistent")
    return sum(1 << index for index, hit in enumerate(support) if hit)


def dense_polynomial_residue(
    coefficients: tuple[int, ...],
    base: int,
    prime: int,
) -> int:
    result = 0
    for coefficient in reversed(coefficients):
        result = (result * base + coefficient) % prime
    return result


def dense_exit_mask(
    descriptor: ExceptionalSelectorDescriptor,
    prime: int,
) -> int:
    if descriptor.base % prime == 0:
        return 1
    first_stage = sum(
        pow(descriptor.base, exponent, prime)
        for exponent in range(descriptor.first_factor)
    ) % prime
    nested_base = pow(
        descriptor.base,
        descriptor.first_factor,
        prime,
    )
    second_stage = sum(
        pow(nested_base, exponent, prime)
        for exponent in range(descriptor.second_factor)
    ) % prime
    if descriptor.family == "phi4":
        cyclotomic = (descriptor.base * descriptor.base + 1) % prime
        constant = (
            descriptor.first_factor * (descriptor.second_factor + 2) + 1
        ) // 4
        linear = (
            descriptor.first_factor * (descriptor.second_factor - 2) + 1
        ) // 4
        resultant = constant * constant + linear * linear
        first_bound = descriptor.second_factor
        second_bound = descriptor.second_factor
    else:
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
        first_bound = descriptor.second_factor
        second_bound = 2 * descriptor.second_factor
    cofactor = dense_polynomial_residue(
        exceptional_cofactor_coefficients(
            descriptor.first_factor,
            descriptor.second_factor,
            descriptor.family,
        ),
        descriptor.base,
        prime,
    )
    support = (
        False,
        first_stage == 0,
        second_stage == 0,
        first_bound % prime == 0,
        second_bound % prime == 0,
        cyclotomic == 0,
        resultant % prime == 0,
        cofactor == 0,
    )
    return sum(1 << index for index, hit in enumerate(support) if hit)


def dense_source_hit(source: str, prime: int) -> bool:
    family, first, second, base, kind = source.split(":")
    descriptor = ExceptionalSelectorDescriptor(
        family,
        int(first),
        int(second),
        int(base),
    )
    bit_index = (
        "base",
        "first_stage",
        "second_stage",
        "first_public_bound",
        "second_public_bound",
        "cyclotomic",
        "overlap_resultant",
        "cofactor",
    ).index(kind)
    return bool(dense_exit_mask(descriptor, prime) & (1 << bit_index))


def main() -> int:
    data = json.loads(
        (
            ROOT
            / "schemas/m31-diversified-compact-signature-vectors-v1.json"
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

    checks = 0
    for vector in data["primitive_exit_vectors"]:
        descriptor = ExceptionalSelectorDescriptor(
            vector["family"],
            vector["first_factor"],
            vector["second_factor"],
            vector["base"],
        )
        expected_mask = primitive_exit_mask(descriptor, vector["prime"])
        if expected_mask != vector["expected_mask"]:
            raise AssertionError("registered primitive mask disagrees with Python")
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
        for executable, env_arg in (
            ([str(rust)], None),
            (csharp, env),
        ):
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
                    "M31 primitive exit disagreement: "
                    f"{evaluation_arguments} expected={expected_mask} "
                    f"actual={actual_mask}"
                )
            checks += 2

    for expected in data["selector_profiles"]:
        profile = diversified_selector_profile(expected["input_length"])
        actual = {
            "input_length": profile.input_length,
            "population_size": len(profile.population_primes),
            "descriptor_count": profile.descriptor_count,
            "normalized_coordinate_count": len(profile.normalized_columns),
            "distinct_signature_count": profile.distinct_signature_count,
            "collision_pair_count": profile.collision_pair_count,
            "minimum_certificate_size": len(
                profile.minimum_separating_column_indices or ()
            ),
        }
        if actual != expected:
            raise AssertionError(
                f"registered selector profile changed: {actual} != {expected}"
            )

    certificate_pair_checks = 0
    for certificate in data["construction_certificates"]:
        signatures = tuple(
            sum(
                1 << column_index
                for column_index, source in enumerate(
                    certificate["column_sources"]
                )
                if dense_source_hit(source, prime)
            )
            for prime in certificate["primes"]
        )
        if list(signatures) != certificate["restricted_signatures"]:
            raise AssertionError(
                "dense construction certificate changed at length "
                f"{certificate['input_length']}"
            )
        if len(set(signatures)) != len(signatures):
            raise AssertionError("dense construction certificate is not injective")
        certificate_pair_checks += len(signatures) * (len(signatures) - 1) // 2

    collision = data["collision_certificate"]
    collision_primes = collision["primes"]
    for descriptor in diversified_exceptional_selector(
        collision["input_length"]
    ):
        masks = tuple(
            dense_exit_mask(descriptor, prime)
            for prime in collision_primes
        )
        if len(set(masks)) != 1:
            raise AssertionError(
                "registered dense collision certificate no longer collides"
            )

    print(
        "M31 diversified compact-signature differential validation: "
        f"PASS ({checks} cross-language command checks, "
        f"{len(data['selector_profiles'])} profile checks, "
        f"{certificate_pair_checks} dense certificate pair checks)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
