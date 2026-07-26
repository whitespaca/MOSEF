"""Differentially check selected M7 root counts and Lucas candidates."""

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
    evaluate_lucas_candidate,
    lucas_root_count,
)


def load_vectors() -> dict[str, list[dict[str, Any]]]:
    """Load the selected M7 cross-language vectors."""
    path = ROOT / "schemas" / "m7-nonsplit-vectors-v1.json"
    with path.open(encoding="utf-8") as handle:
        value = json.load(handle)
    roots = value.get("root_count_vectors")
    candidates = value.get("candidate_vectors")
    if not isinstance(roots, list) or not isinstance(candidates, list):
        raise TypeError("M7 vectors must contain root and candidate arrays")
    return {"roots": roots, "candidates": candidates}


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

    for vector in vectors["roots"]:
        arguments = [str(vector["prime"]), str(vector["exponent"])]
        expected = str(lucas_root_count(vector["prime"], vector["exponent"]))
        if expected != str(vector["root_count"]):
            raise AssertionError(
                f"Python formula disagrees with registered root vector {arguments}"
            )
        for label, command in (
            ("Rust", [rust, "lucas-root-count-direct", *arguments]),
            ("C#", [*csharp, "lucas-root-count-direct", *arguments]),
        ):
            environment = dotnet_environment if label == "C#" else None
            actual = run(command, environment)
            if actual != expected:
                raise AssertionError(
                    f"{label} root count {arguments}: "
                    f"expected {expected!r}, got {actual!r}"
                )
            checks += 1

    for vector in vectors["candidates"]:
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
                f"Python disagrees with registered candidate {arguments}: "
                f"{expected!r} != {registered!r}"
            )
        for label, command in (
            ("Rust", [rust, "lucas-separator", *arguments]),
            ("C#", [*csharp, "lucas-separator", *arguments]),
        ):
            environment = dotnet_environment if label == "C#" else None
            actual = run(command, environment)
            if actual != expected:
                raise AssertionError(
                    f"{label} candidate {arguments}: "
                    f"expected {expected!r}, got {actual!r}"
                )
            checks += 1

    print(f"M7 nonsplit differential validation: PASS ({checks} checks)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
