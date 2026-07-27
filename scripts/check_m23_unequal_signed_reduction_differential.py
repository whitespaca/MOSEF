"""Differentially check selected M23 unequal signed-reduction vectors."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
from mosef_reference import evaluate_unequal_signed_reduction  # noqa: E402


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


def optional(value: int | None) -> str:
    return "none" if value is None else str(value)


def protocol(value: Any) -> str:
    return (
        f"first_factor:{value.first_factor}|second_factor:{value.second_factor}|"
        f"first_coefficient:{value.first_coefficient}|"
        f"second_coefficient:{value.second_coefficient}|"
        f"first_quotient:{value.first_quotient_residue}|"
        f"second_quotient:{value.second_quotient_residue}|"
        f"first_quotient_gcd:{value.first_quotient_gcd}|"
        f"second_quotient_gcd:{value.second_quotient_gcd}|"
        f"aggregate:{value.aggregate_residue}|aggregate_gcd:{value.aggregate_gcd}|"
        f"prefix_status:{value.first_quotient_status}|"
        f"rational:{optional(value.rational_reduction_residue)}|"
        f"rational_gcd:{optional(value.rational_reduction_gcd)}|"
        f"public_full:{value.public_full_residue}|"
        f"public_full_gcd:{value.public_full_gcd}|"
        f"common_stage_gcd:{value.common_stage_gcd}|"
        f"multiplier_gcd:{value.multiplier_gcd}|"
        f"x_factor:{str(value.has_x_factor).lower()}|"
        f"x_minus_one_factor:{str(value.has_x_minus_one_factor).lower()}|"
        f"formal_degree:{value.formal_degree}|"
        f"collected_monomials:{value.collected_monomial_count}|"
        f"common_step:{value.common_step}|difference:{value.difference_residue}|"
        f"difference_gcd:{value.difference_gcd}|"
        f"common_factor:{value.common_factor_residue}|"
        f"common_factor_gcd:{value.common_factor_gcd}|"
        f"cofactor:{optional(value.difference_cofactor_residue)}|"
        f"cofactor_gcd:{optional(value.difference_cofactor_gcd)}|"
        f"cofactor_degree:{value.difference_cofactor_degree}"
    )


def main() -> int:
    data = json.loads(
        (ROOT / "schemas/m23-unequal-signed-reduction-vectors-v1.json").read_text()
    )
    vectors = data["unequal_signed_reduction_vectors"]
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
            "restore",
            "verification/csharp/MosefVerifier.csproj",
            "--configfile",
            "verification/csharp/NuGet.Config",
            "--verbosity",
            "quiet",
        ],
        env,
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
    for vector in vectors:
        arguments = [
            vector["base"],
            vector["modulus"],
            vector["first_factor"],
            vector["second_factor"],
            vector["first_coefficient"],
            vector["second_coefficient"],
        ]
        value = evaluate_unequal_signed_reduction(*arguments)
        if asdict(value) != vector:
            raise AssertionError("registered vector disagrees with Python")
        expected = protocol(value)
        text_arguments = [str(item) for item in arguments]
        for command, env_arg in (
            ([str(rust), "unequal-signed-reduction", *text_arguments], None),
            ([*csharp, "unequal-signed-reduction", *text_arguments], env),
        ):
            if run(command, env_arg) != expected:
                raise AssertionError(
                    f"unequal signed-reduction disagreement: {text_arguments}"
                )
            checks += 1
    print(f"M23 unequal signed-reduction differential validation: PASS ({checks} checks)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
