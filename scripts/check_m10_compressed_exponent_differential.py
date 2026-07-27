"""Differentially check selected M10 straight-line exponent vectors."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

from mosef_reference import (
    evaluate_multiplication_program,
    generic_multiplication_lower_bound,
)


def load_vectors() -> dict[str, list[dict[str, Any]]]:
    """Load the selected M10 cross-language vectors."""
    path = ROOT / "schemas" / "m10-compressed-exponent-vectors-v1.json"
    with path.open(encoding="utf-8") as handle:
        value = json.load(handle)
    keys = ("program_vectors", "lower_bound_vectors")
    if any(not isinstance(value.get(key), list) for key in keys):
        raise TypeError("M10 vectors must contain both vector arrays")
    return {key: value[key] for key in keys}


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


def step_protocol(steps: list[list[int]]) -> str:
    """Serialize parent pairs for the shared verifier protocol."""
    return ",".join(f"{left}:{right}" for left, right in steps)


def evaluation_protocol(exponents: list[int], residues: list[int]) -> str:
    """Serialize a complete straight-line evaluation."""
    return (
        f"exponents:{','.join(map(str, exponents))}|"
        f"residues:{','.join(map(str, residues))}"
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

    for vector in vectors["program_vectors"]:
        evaluation = evaluate_multiplication_program(
            vector["base"],
            vector["modulus"],
            tuple(tuple(step) for step in vector["steps"]),
        )
        expected = evaluation_protocol(
            list(evaluation.exponents),
            list(evaluation.residues),
        )
        registered = evaluation_protocol(vector["exponents"], vector["residues"])
        if expected != registered:
            raise AssertionError(f"Python program disagrees with {vector}")
        arguments = [
            str(vector["base"]),
            str(vector["modulus"]),
            step_protocol(vector["steps"]),
        ]
        for label, command in (
            ("Rust", [rust, "multiplication-program", *arguments]),
            ("C#", [*csharp, "multiplication-program", *arguments]),
        ):
            environment = dotnet_environment if label == "C#" else None
            actual = run(command, environment)
            if actual != expected:
                raise AssertionError(
                    f"{label} program {arguments}: "
                    f"expected {expected!r}, got {actual!r}"
                )
            checks += 1

    for vector in vectors["lower_bound_vectors"]:
        expected = str(generic_multiplication_lower_bound(vector["exponent"]))
        if expected != str(vector["minimum_multiplications"]):
            raise AssertionError(f"Python lower bound disagrees with {vector}")
        arguments = [str(vector["exponent"])]
        for label, command in (
            ("Rust", [rust, "multiplication-lower-bound", *arguments]),
            ("C#", [*csharp, "multiplication-lower-bound", *arguments]),
        ):
            environment = dotnet_environment if label == "C#" else None
            actual = run(command, environment)
            if actual != expected:
                raise AssertionError(
                    f"{label} lower bound {arguments}: "
                    f"expected {expected!r}, got {actual!r}"
                )
            checks += 1

    print(
        "M10 compressed-exponent differential validation: "
        f"PASS ({checks} checks)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
