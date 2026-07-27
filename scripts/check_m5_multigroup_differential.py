"""Differentially check selected M5 Lucas candidates in Python, Rust, and C#."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

from mosef_reference import evaluate_lucas_candidate


def load_vectors() -> list[dict[str, Any]]:
    """Load the selected M5 cross-language vectors."""
    path = ROOT / "schemas" / "m5-multigroup-vectors-v1.json"
    with path.open(encoding="utf-8") as handle:
        value = json.load(handle)
    vectors = value.get("vectors")
    if not isinstance(vectors, list):
        raise TypeError("M5 vectors must contain a vectors array")
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


def protocol(kind: str, factor: int | None, residue: int | None) -> str:
    """Serialize one Lucas outcome in the shared verifier protocol."""
    factor_field = "none" if factor is None else str(factor)
    residue_field = "none" if residue is None else str(residue)
    return f"{kind}|{factor_field}|{residue_field}"


def main() -> int:
    """Build and run all three implementations on every selected vector."""
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

    for vector in load_vectors():
        arguments = [
            str(vector["n"]),
            str(vector["parameter"]),
            str(vector["exponent"]),
        ]
        outcome = evaluate_lucas_candidate(
            vector["n"],
            vector["parameter"],
            vector["exponent"],
        )
        expected = protocol(outcome.kind.value, outcome.factor, outcome.residue)
        registered = protocol(
            vector["kind"],
            vector["factor"],
            vector["residue"],
        )
        if expected != registered:
            raise AssertionError(
                f"Python disagrees with registered vector {arguments}: "
                f"{expected!r} != {registered!r}"
            )
        for label, command in (
            (("Rust"), [rust, "lucas-separator", *arguments]),
            (("C#"), [*csharp, "lucas-separator", *arguments]),
        ):
            environment = dotnet_environment if label == "C#" else None
            actual = run(command, environment)
            if actual != expected:
                raise AssertionError(
                    f"{label} candidate {arguments}: "
                    f"expected {expected!r}, got {actual!r}"
                )
            checks += 1

    print(f"M5 multigroup differential validation: PASS ({checks} checks)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
