"""Differentially check selected M22 symmetric-difference vectors."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
from mosef_reference import evaluate_symmetric_quotient_difference


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


def protocol(value: Any) -> str:
    division = (
        "none"
        if value.division_cofactor is None
        else str(value.division_cofactor)
    )
    return (
        f"exponent:{value.exponent}|"
        f"first_quotient:{value.first_quotient_residue}|"
        f"second_quotient:{value.second_quotient_residue}|"
        f"difference:{value.difference_residue}|"
        f"difference_gcd:{value.difference_gcd}|"
        f"endpoint:{value.endpoint_residue}|"
        f"endpoint_gcd:{value.endpoint_gcd}|"
        f"endpoint_status:{value.endpoint_status}|"
        f"cofactor:{value.cofactor_residue}|"
        f"cofactor_gcd:{value.cofactor_gcd}|"
        f"division_cofactor:{division}|"
        f"cofactor_monomials:{value.cofactor_monomial_count}|"
        f"cofactor_degree:{value.cofactor_degree}|"
        f"matrix_multiplications:{value.matrix_multiplication_count}"
    )


def check_registered_fields(vector: dict[str, Any], value: Any) -> None:
    actual = {
        "first_quotient": value.first_quotient_residue,
        "second_quotient": value.second_quotient_residue,
        "difference": value.difference_residue,
        "difference_gcd": value.difference_gcd,
        "endpoint": value.endpoint_residue,
        "endpoint_gcd": value.endpoint_gcd,
        "endpoint_status": value.endpoint_status,
        "cofactor": value.cofactor_residue,
        "cofactor_gcd": value.cofactor_gcd,
        "division_cofactor": value.division_cofactor,
        "cofactor_monomials": value.cofactor_monomial_count,
        "cofactor_degree": value.cofactor_degree,
        "matrix_multiplications": value.matrix_multiplication_count,
    }
    expected = {field: vector[field] for field in actual}
    if actual != expected:
        raise AssertionError(
            f"registered vector disagrees with Python: expected {expected}, got {actual}"
        )


def main() -> int:
    data = json.loads(
        (
            ROOT / "schemas/m22-symmetric-quotient-difference-vectors-v1.json"
        ).read_text()
    )
    vectors = data["symmetric_quotient_difference_vectors"]
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
        value = evaluate_symmetric_quotient_difference(
            vector["base"],
            vector["modulus"],
            vector["exponent"],
        )
        check_registered_fields(vector, value)
        expected = protocol(value)
        args = [
            str(vector["base"]),
            str(vector["modulus"]),
            str(vector["exponent"]),
        ]
        for command, env_arg in (
            ([str(rust), "symmetric-quotient-difference", *args], None),
            ([*csharp, "symmetric-quotient-difference", *args], env),
        ):
            if run(command, env_arg) != expected:
                raise AssertionError(f"symmetric-difference disagreement: {args}")
            checks += 1
    print(
        f"M22 symmetric quotient-difference differential validation: PASS ({checks} checks)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
