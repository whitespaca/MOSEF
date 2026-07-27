"""Differentially check selected M4 profiles in Python, Rust, and C#."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

from mosef_reference import analyze_cover


def load_vectors() -> list[dict[str, Any]]:
    """Load the selected M4 cross-language vectors."""
    path = ROOT / "schemas" / "m4-difference-cover-vectors-v1.json"
    with path.open(encoding="utf-8") as handle:
        value = json.load(handle)
    vectors = value.get("vectors")
    if not isinstance(vectors, list):
        raise TypeError("M4 vectors must contain a vectors array")
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


def protocol(cover: bool, separates: bool, distinct: bool) -> str:
    """Serialize one profile in the shared verifier protocol."""
    return (
        f"cover:{str(cover).lower()}|separates:{str(separates).lower()}|"
        f"distinct:{str(distinct).lower()}"
    )


def main() -> int:
    """Build and run all three implementations on every selected vector."""
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
        candidates = tuple(vector["candidates"])
        orders = tuple(vector["orders"])
        analysis = analyze_cover(candidates, orders)
        expected = protocol(
            analysis.divisor_cover,
            analysis.separates_profile,
            analysis.distinct_signatures,
        )
        registered = protocol(
            vector["cover"], vector["separates"], vector["distinct"]
        )
        if expected != registered:
            raise AssertionError(
                f"Python disagrees with registered vector {(candidates, orders)}"
            )
        arguments = [
            ",".join(map(str, candidates)),
            ",".join(map(str, orders)),
        ]
        for label, command in (
            ("Rust", [rust, "cover-profile", *arguments]),
            ("C#", [*csharp, "cover-profile", *arguments]),
        ):
            environment = dotnet_environment if label == "C#" else None
            actual = run(command, environment)
            if actual != expected:
                raise AssertionError(
                    f"{label} profile {arguments}: expected {expected!r}, got {actual!r}"
                )
            checks += 1

    print(f"M4 difference-cover differential validation: PASS ({checks} checks)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
