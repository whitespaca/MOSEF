"""Differentially check selected M9 divisor-budget vectors."""

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
    combined_asymmetry,
    combined_signature,
    divisor_count,
    hit_primes,
)


def load_vectors() -> dict[str, list[dict[str, Any]]]:
    """Load the selected M9 cross-language vectors."""
    path = ROOT / "schemas" / "m9-divisor-budget-vectors-v1.json"
    with path.open(encoding="utf-8") as handle:
        value = json.load(handle)
    keys = (
        "divisor_count_vectors",
        "signature_vectors",
        "asymmetry_vectors",
        "hit_count_vectors",
    )
    if any(not isinstance(value.get(key), list) for key in keys):
        raise TypeError("M9 vectors must contain all four vector arrays")
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


def signature_protocol(signature: tuple[tuple[bool, bool], ...]) -> str:
    """Serialize signature bits in the shared verifier protocol."""
    return ",".join(
        f"{int(minus)}{int(plus)}" for minus, plus in signature
    )


def csv(values: list[int]) -> str:
    """Serialize a positive-integer list for verifier CLIs."""
    return ",".join(str(value) for value in values)


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

    for vector in vectors["divisor_count_vectors"]:
        arguments = [str(vector["value"])]
        expected = str(divisor_count(vector["value"]))
        if expected != str(vector["divisor_count"]):
            raise AssertionError(f"Python divisor count disagrees with {arguments}")
        for label, command in (
            ("Rust", [rust, "divisor-count", *arguments]),
            ("C#", [*csharp, "divisor-count", *arguments]),
        ):
            environment = dotnet_environment if label == "C#" else None
            actual = run(command, environment)
            if actual != expected:
                raise AssertionError(
                    f"{label} divisor count {arguments}: "
                    f"expected {expected!r}, got {actual!r}"
                )
            checks += 1

    for vector in vectors["signature_vectors"]:
        arguments = [str(vector["prime"]), csv(vector["exponents"])]
        expected = signature_protocol(
            combined_signature(vector["prime"], vector["exponents"])
        )
        if expected != vector["signature"]:
            raise AssertionError(f"Python signature disagrees with {arguments}")
        for label, command in (
            ("Rust", [rust, "combined-signature", *arguments]),
            ("C#", [*csharp, "combined-signature", *arguments]),
        ):
            environment = dotnet_environment if label == "C#" else None
            actual = run(command, environment)
            if actual != expected:
                raise AssertionError(
                    f"{label} signature {arguments}: "
                    f"expected {expected!r}, got {actual!r}"
                )
            checks += 1

    for vector in vectors["asymmetry_vectors"]:
        arguments = [
            str(vector["left_prime"]),
            str(vector["right_prime"]),
            csv(vector["exponents"]),
        ]
        expected = str(
            combined_asymmetry(
                vector["left_prime"],
                vector["right_prime"],
                vector["exponents"],
            )
        ).lower()
        if expected != str(vector["asymmetry"]).lower():
            raise AssertionError(f"Python asymmetry disagrees with {arguments}")
        for label, command in (
            ("Rust", [rust, "combined-asymmetry", *arguments]),
            ("C#", [*csharp, "combined-asymmetry", *arguments]),
        ):
            environment = dotnet_environment if label == "C#" else None
            actual = run(command, environment)
            if actual != expected:
                raise AssertionError(
                    f"{label} asymmetry {arguments}: "
                    f"expected {expected!r}, got {actual!r}"
                )
            checks += 1

    for vector in vectors["hit_count_vectors"]:
        arguments = [csv(vector["primes"]), csv(vector["exponents"])]
        expected = str(len(hit_primes(vector["primes"], vector["exponents"])))
        if expected != str(vector["hit_count"]):
            raise AssertionError(f"Python hit count disagrees with {arguments}")
        for label, command in (
            ("Rust", [rust, "combined-hit-count", *arguments]),
            ("C#", [*csharp, "combined-hit-count", *arguments]),
        ):
            environment = dotnet_environment if label == "C#" else None
            actual = run(command, environment)
            if actual != expected:
                raise AssertionError(
                    f"{label} hit count {arguments}: "
                    f"expected {expected!r}, got {actual!r}"
                )
            checks += 1

    print(f"M9 divisor-budget differential validation: PASS ({checks} checks)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
