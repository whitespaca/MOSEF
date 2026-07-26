"""Differentially check selected M14 addition-subtraction vectors."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

from mosef_reference import (  # noqa: E402
    evaluate_addition_subtraction_program,
    signed_exponent_lower_bound,
)


def load_vectors() -> dict[str, list[dict[str, Any]]]:
    """Load the selected M14 cross-language vectors."""
    path = ROOT / "schemas" / "m14-addition-subtraction-vectors-v1.json"
    with path.open(encoding="utf-8") as handle:
        value = json.load(handle)
    keys = ("program_vectors", "lower_bound_vectors")
    if any(not isinstance(value.get(key), list) for key in keys):
        raise TypeError("M14 vectors must contain both vector arrays")
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
    """Serialize signed parent pairs for the shared verifier protocol."""
    return ",".join(
        f"{left}:{right}:{'+' if sign == 1 else '-'}"
        for left, right, sign in steps
    )


def evaluation_protocol(
    exponents: list[int],
    residues: list[int],
    inversion_count: int,
) -> str:
    """Serialize a complete signed straight-line evaluation."""
    return (
        f"exponents:{','.join(map(str, exponents))}|"
        f"residues:{','.join(map(str, residues))}|"
        f"inversions:{inversion_count}"
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
        evaluation = evaluate_addition_subtraction_program(
            vector["base"],
            vector["modulus"],
            tuple(tuple(step) for step in vector["steps"]),
        )
        expected = evaluation_protocol(
            list(evaluation.exponents),
            list(evaluation.residues),
            evaluation.inversion_count,
        )
        registered = evaluation_protocol(
            vector["exponents"],
            vector["residues"],
            vector["inversion_count"],
        )
        if expected != registered:
            raise AssertionError(f"Python program disagrees with {vector}")
        arguments = [
            str(vector["base"]),
            str(vector["modulus"]),
            step_protocol(vector["steps"]),
        ]
        for label, command in (
            ("Rust", [rust, "addition-subtraction-program", *arguments]),
            ("C#", [*csharp, "addition-subtraction-program", *arguments]),
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
        expected = str(signed_exponent_lower_bound(vector["exponent"]))
        if expected != str(vector["minimum_nodes"]):
            raise AssertionError(f"Python lower bound disagrees with {vector}")
        arguments = [str(abs(vector["exponent"]))]
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
        "M14 addition-subtraction differential validation: "
        f"PASS ({checks} checks)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
