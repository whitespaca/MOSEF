"""Differentially check selected M18 arbitrary geometric-sum vectors."""

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

from mosef_reference import evaluate_geometric_sum


def load_vectors() -> list[dict[str, Any]]:
    path = ROOT / "schemas" / "m18-geometric-sum-vectors-v1.json"
    with path.open(encoding="utf-8") as handle:
        value = json.load(handle)
    vectors = value.get("geometric_sum_vectors")
    if not isinstance(vectors, list):
        raise TypeError("M18 vectors must contain geometric_sum_vectors")
    return vectors


def run(command: list[str], environment: dict[str, str] | None = None) -> str:
    completed = subprocess.run(
        command,
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=environment,
    )
    return completed.stdout.strip()


def executable(name: str) -> str:
    suffix = ".exe" if os.name == "nt" else ""
    return str(ROOT / "target" / "debug" / f"{name}{suffix}")


def protocol(vector: dict[str, Any]) -> str:
    division_quotient = vector["division_quotient"]
    return (
        f"power:{vector['power_residue']}|sum:{vector['sum_residue']}|"
        f"denominator:{vector['denominator_residue']}|"
        f"denominator_gcd:{vector['denominator_gcd']}|"
        f"numerator:{vector['numerator_residue']}|"
        f"numerator_gcd:{vector['numerator_gcd']}|"
        f"sum_gcd:{vector['sum_gcd']}|exponent_gcd:{vector['exponent_gcd']}|"
        f"division_status:{vector['division_status']}|"
        f"division_quotient:{'none' if division_quotient is None else division_quotient}|"
        f"bit_length:{vector['exponent_bit_length']}|"
        f"degree:{vector['formal_degree']}|"
        f"monomials:{vector['formal_monomial_count']}|"
        f"multiplications:{vector['multiplication_count']}|"
        f"additions:{vector['addition_count']}"
    )


def main() -> int:
    vectors = load_vectors()
    dotnet_environment = os.environ.copy()
    dotnet_appdata = ROOT / "verification" / "csharp" / "obj" / "sandbox-appdata"
    dotnet_appdata.mkdir(parents=True, exist_ok=True)
    dotnet_environment["APPDATA"] = str(dotnet_appdata)
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
        dotnet_environment,
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
        dotnet_environment,
    )
    rust = executable("mosef-baseline")
    csharp = [
        "dotnet",
        str(
            ROOT
            / "verification"
            / "csharp"
            / "bin"
            / "Debug"
            / "net8.0"
            / "MosefVerifier.dll"
        ),
    ]
    checks = 0
    for vector in vectors:
        evaluation = asdict(
            evaluate_geometric_sum(
                vector["base"],
                vector["modulus"],
                vector["exponent"],
            )
        )
        expected = protocol(evaluation)
        registered = protocol(vector)
        if expected != registered:
            raise AssertionError(f"Python geometric sum disagrees with {vector}")
        arguments = [
            str(vector["base"]),
            str(vector["modulus"]),
            str(vector["exponent"]),
        ]
        for label, command in (
            ("Rust", [rust, "geometric-sum", *arguments]),
            ("C#", [*csharp, "geometric-sum", *arguments]),
        ):
            environment = dotnet_environment if label == "C#" else None
            actual = run(command, environment)
            if actual != expected:
                raise AssertionError(
                    f"{label} geometric sum {arguments}: "
                    f"expected {expected!r}, got {actual!r}"
                )
            checks += 1
    print(f"M18 geometric-sum differential validation: PASS ({checks} checks)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
