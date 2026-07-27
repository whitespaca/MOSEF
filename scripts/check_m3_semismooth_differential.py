"""Differentially check selected M3 family outcomes in Python, Rust, and C#."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

from mosef_reference import successful_residue_count, try_semismooth_factor


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


def load_vectors() -> dict[str, list[dict[str, Any]]]:
    """Load the selected M3 family vectors."""
    path = ROOT / "schemas" / "m3-semismooth-vectors-v1.json"
    with path.open(encoding="utf-8") as handle:
        value = json.load(handle)
    vectors = value.get("vectors")
    probability_vectors = value.get("probability_vectors")
    if not isinstance(vectors, list) or not isinstance(probability_vectors, list):
        raise TypeError("M3 vectors must contain both registered arrays")
    return {"vectors": vectors, "probability_vectors": probability_vectors}


def executable(name: str) -> str:
    """Return a platform-specific Rust debug executable path."""
    suffix = ".exe" if os.name == "nt" else ""
    return str(ROOT / "target" / "debug" / f"{name}{suffix}")


def main() -> int:
    """Build and compare all three implementations."""
    dotnet_environment = os.environ.copy()
    dotnet_appdata = ROOT / "verification" / "csharp" / "obj" / "sandbox-appdata"
    dotnet_appdata.mkdir(parents=True, exist_ok=True)
    dotnet_environment["APPDATA"] = str(dotnet_appdata)
    run(["cargo", "build", "--quiet", "-p", "mosef-arithmetic", "--bin", "mosef-baseline"])
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
        str(ROOT / "verification" / "csharp" / "bin" / "Debug" / "net8.0" / "MosefVerifier.dll"),
    ]
    checks = 0
    vectors = load_vectors()
    for vector in vectors["vectors"]:
        arguments = [
            vector["n"],
            vector["base_bound"],
            vector["smooth_bound"],
            vector["cofactor_bound"],
        ]
        python_result = try_semismooth_factor(*(int(value) for value in arguments))
        expected = "unresolved" if python_result is None else f"factor:{python_result.factor}"
        if expected != vector["result"]:
            raise AssertionError(
                f"Python disagrees with registered vector {arguments}: "
                f"{expected!r} != {vector['result']!r}"
            )
        for label, command, environment in (
            ("Rust", [rust, "semismooth", *arguments], None),
            ("C#", [*csharp, "semismooth", *arguments], dotnet_environment),
        ):
            actual = run(command, environment)
            if actual != expected:
                raise AssertionError(
                    f"{label} semismooth {arguments}: expected {expected!r}, got {actual!r}"
                )
            checks += 1
    for vector in vectors["probability_vectors"]:
        arguments = [vector["n"], vector["exponent"]]
        expected = str(successful_residue_count(*(int(value) for value in arguments)))
        if expected != vector["successful_residues"]:
            raise AssertionError(
                f"Python success count disagrees with {arguments}: "
                f"{expected!r} != {vector['successful_residues']!r}"
            )
        for label, command, environment in (
            (
                "Rust",
                [rust, "semismooth-success-count", *arguments],
                None,
            ),
            (
                "C#",
                [*csharp, "semismooth-success-count", *arguments],
                dotnet_environment,
            ),
        ):
            actual = run(command, environment)
            if actual != expected:
                raise AssertionError(
                    f"{label} success count {arguments}: "
                    f"expected {expected!r}, got {actual!r}"
                )
            checks += 1
    print(f"M3 semismooth differential validation: PASS ({checks} checks)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
