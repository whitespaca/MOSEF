"""Differentially check selected M17 dyadic telescope vectors."""

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

from mosef_reference import evaluate_dyadic_telescope  # noqa: E402


def load_vectors() -> list[dict[str, Any]]:
    """Load the selected M17 cross-language vectors."""
    path = ROOT / "schemas" / "m17-dyadic-telescope-vectors-v1.json"
    with path.open(encoding="utf-8") as handle:
        value = json.load(handle)
    vectors = value.get("dyadic_telescope_vectors")
    if not isinstance(vectors, list):
        raise TypeError("M17 vectors must contain dyadic_telescope_vectors")
    return vectors


def run(command: list[str], environment: dict[str, str] | None = None) -> str:
    """Run one verifier command and return normalized stdout."""
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
    """Return a platform-specific Rust debug executable path."""
    suffix = ".exe" if os.name == "nt" else ""
    return str(ROOT / "target" / "debug" / f"{name}{suffix}")


def protocol(vector: dict[str, Any]) -> str:
    """Serialize the shared dyadic telescope result."""
    division_quotient = vector["division_quotient"]
    return (
        f"powers:{','.join(map(str, vector['power_residues']))}|"
        f"factors:{','.join(map(str, vector['factor_residues']))}|"
        f"factor_gcds:{','.join(map(str, vector['factor_gcds']))}|"
        f"denominator:{vector['denominator_residue']}|"
        f"denominator_gcd:{vector['denominator_gcd']}|"
        f"numerator:{vector['numerator_residue']}|"
        f"numerator_gcd:{vector['numerator_gcd']}|"
        f"quotient:{vector['quotient_residue']}|"
        f"quotient_gcd:{vector['quotient_gcd']}|"
        f"division_status:{vector['division_status']}|"
        f"division_quotient:{'none' if division_quotient is None else division_quotient}|"
        f"degree:{vector['formal_degree']}|"
        f"monomials:{vector['formal_monomial_count']}|"
        f"squarings:{vector['squaring_count']}|"
        f"products:{vector['product_multiplication_count']}"
    )


def main() -> int:
    """Build and run all three implementations on every selected vector."""
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
            evaluate_dyadic_telescope(
                vector["base"],
                vector["modulus"],
                vector["levels"],
            )
        )
        expected = protocol(evaluation)
        registered = protocol(vector)
        if expected != registered:
            raise AssertionError(f"Python telescope disagrees with {vector}")
        arguments = [
            str(vector["base"]),
            str(vector["modulus"]),
            str(vector["levels"]),
        ]
        for label, command in (
            ("Rust", [rust, "dyadic-telescope", *arguments]),
            ("C#", [*csharp, "dyadic-telescope", *arguments]),
        ):
            environment = dotnet_environment if label == "C#" else None
            actual = run(command, environment)
            if actual != expected:
                raise AssertionError(
                    f"{label} dyadic telescope {arguments}: "
                    f"expected {expected!r}, got {actual!r}"
                )
            checks += 1
    print(f"M17 dyadic-telescope differential validation: PASS ({checks} checks)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
