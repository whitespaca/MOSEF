"""Differentially check selected M16 non-materializing product-DAG vectors."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

from mosef_reference import ProductGate, evaluate_product_dag  # noqa: E402


def load_vectors() -> list[dict[str, Any]]:
    """Load the selected M16 cross-language vectors."""
    path = ROOT / "schemas" / "m16-product-dag-vectors-v1.json"
    with path.open(encoding="utf-8") as handle:
        value = json.load(handle)
    vectors = value.get("product_dag_vectors")
    if not isinstance(vectors, list):
        raise TypeError("M16 vectors must contain product_dag_vectors")
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


def protocol(
    nodes: list[int],
    gcds: list[int],
    multiplicities: list[list[int]],
    occurrences: list[int],
) -> str:
    """Serialize the shared product-DAG result."""
    profiles = ";".join(",".join(map(str, profile)) for profile in multiplicities)
    return (
        f"nodes:{','.join(map(str, nodes))}|gcds:{','.join(map(str, gcds))}|"
        f"multiplicities:{profiles}|occurrences:{','.join(map(str, occurrences))}"
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
        gates = tuple(ProductGate(*gate) for gate in vector["gates"])
        evaluation = evaluate_product_dag(
            vector["base"],
            vector["modulus"],
            vector["exponents"],
            gates,
        )
        expected = protocol(
            list(evaluation.node_residues),
            list(evaluation.node_gcds),
            [list(profile) for profile in evaluation.multiplicities],
            list(evaluation.occurrence_counts),
        )
        registered = protocol(
            vector["node_residues"],
            vector["node_gcds"],
            vector["multiplicities"],
            vector["occurrence_counts"],
        )
        if expected != registered:
            raise AssertionError(f"Python product DAG disagrees with {vector}")
        arguments = [
            str(vector["base"]),
            str(vector["modulus"]),
            ",".join(map(str, vector["exponents"])),
            ",".join(f"{left}:{right}" for left, right in vector["gates"]),
        ]
        for label, command in (
            ("Rust", [rust, "product-dag", *arguments]),
            ("C#", [*csharp, "product-dag", *arguments]),
        ):
            environment = dotnet_environment if label == "C#" else None
            actual = run(command, environment)
            if actual != expected:
                raise AssertionError(
                    f"{label} product DAG {arguments}: "
                    f"expected {expected!r}, got {actual!r}"
                )
            checks += 1
    print(f"M16 product-DAG differential validation: PASS ({checks} checks)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
