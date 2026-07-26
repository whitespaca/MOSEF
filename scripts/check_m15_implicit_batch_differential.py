"""Differentially check selected M15 leaf-materialized batch vectors."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

from mosef_reference import evaluate_batch_product  # noqa: E402


def load_vectors() -> list[dict[str, Any]]:
    """Load the selected M15 cross-language vectors."""
    path = ROOT / "schemas" / "m15-implicit-batch-vectors-v1.json"
    with path.open(encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value.get("batch_vectors"), list):
        raise TypeError("M15 vectors must contain batch_vectors")
    return value["batch_vectors"]


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


def protocol(
    leaves: list[int],
    root: int,
    leaf_gcds: list[int],
    root_gcd: int,
    multiplication_count: int,
) -> str:
    """Serialize the shared leaf-materialized batch result."""
    return (
        f"leaves:{','.join(map(str, leaves))}|root:{root}|"
        f"leaf_gcds:{','.join(map(str, leaf_gcds))}|root_gcd:{root_gcd}|"
        f"multiplications:{multiplication_count}"
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
        evaluation = evaluate_batch_product(
            vector["base"],
            vector["modulus"],
            vector["exponents"],
        )
        expected = protocol(
            list(evaluation.leaf_residues),
            evaluation.root_residue,
            list(evaluation.leaf_gcds),
            evaluation.root_gcd,
            evaluation.multiplication_count,
        )
        registered = protocol(
            vector["leaf_residues"],
            vector["root_residue"],
            vector["leaf_gcds"],
            vector["root_gcd"],
            vector["multiplication_count"],
        )
        if expected != registered:
            raise AssertionError(f"Python batch disagrees with {vector}")
        arguments = [
            str(vector["base"]),
            str(vector["modulus"]),
            ",".join(map(str, vector["exponents"])),
        ]
        for label, command in (
            ("Rust", [rust, "batch-product", *arguments]),
            ("C#", [*csharp, "batch-product", *arguments]),
        ):
            environment = dotnet_environment if label == "C#" else None
            actual = run(command, environment)
            if actual != expected:
                raise AssertionError(
                    f"{label} batch {arguments}: "
                    f"expected {expected!r}, got {actual!r}"
                )
            checks += 1
    print(f"M15 implicit-batch differential validation: PASS ({checks} checks)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
