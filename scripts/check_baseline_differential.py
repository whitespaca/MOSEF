"""Build and differentially check Python, Rust, and C# baseline operations."""

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
    batch_gcd,
    is_prime,
    mod_pow,
    perfect_power,
    pollard_p_minus_one,
    pollard_p_plus_one,
    pollard_rho,
    trial_division,
)


def load_vectors() -> dict[str, Any]:
    with (ROOT / "schemas" / "baseline-vectors-v1.json").open(encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise TypeError("baseline vectors must be a JSON object")
    return value


def run(command: list[str]) -> str:
    completed = subprocess.run(
        command,
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return completed.stdout.strip()


def executable(name: str) -> str:
    suffix = ".exe" if os.name == "nt" else ""
    return str(ROOT / "target" / "debug" / f"{name}{suffix}")


def optional_text(value: int | None) -> str:
    return "none" if value is None else str(value)


def check_equal(label: str, expected: str, actual: str) -> None:
    if actual != expected:
        raise AssertionError(f"{label}: expected {expected!r}, got {actual!r}")


def main() -> int:
    vectors = load_vectors()
    run(["cargo", "build", "--quiet", "-p", "mosef-arithmetic", "--bin", "mosef-baseline"])
    run(["dotnet", "build", "verification/csharp/MosefVerifier.csproj", "--nologo", "--verbosity", "quiet"])

    rust = executable("mosef-baseline")
    csharp = [
        "dotnet",
        str(ROOT / "verification" / "csharp" / "bin" / "Debug" / "net8.0" / "MosefVerifier.dll"),
    ]
    checks = 0

    for vector in vectors["mod_pow"]:
        arguments = [vector["base"], vector["exponent"], vector["modulus"]]
        expected = str(mod_pow(*(int(value) for value in arguments)))
        check_equal("Rust mod-pow", expected, run([rust, "mod-pow", *arguments]))
        check_equal("C# mod-pow", expected, run([*csharp, "mod-pow", *arguments]))
        checks += 2

    for vector in vectors["primality"]:
        n = vector["n"]
        expected = str(is_prime(int(n))).lower()
        check_equal("Rust is-prime", expected, run([rust, "is-prime", n]))
        check_equal("C# is-prime", expected, run([*csharp, "is-prime", n]))
        checks += 2

    for vector in vectors["trial_division"]:
        n = vector["n"]
        expected = optional_text(trial_division(int(n)))
        check_equal("Rust trial-factor", expected, run([rust, "trial-factor", n]))
        check_equal("C# trial-factor", expected, run([*csharp, "trial-factor", n]))
        checks += 2

    for vector in vectors["perfect_power"]:
        n = vector["n"]
        result = perfect_power(int(n))
        expected = "none" if result is None else f"{result[0]}^{result[1]}"
        check_equal("Rust perfect-power", expected, run([rust, "perfect-power", n]))
        checks += 1

    for vector in vectors["pollard_rho"]:
        arguments = [vector["n"], vector["seed"], vector["max_steps"]]
        expected = optional_text(pollard_rho(*(int(value) for value in arguments)))
        check_equal("Rust rho", expected, run([rust, "rho", *arguments]))
        checks += 1

    for vector in vectors["pollard_p_minus_one"]:
        arguments = [vector["n"], vector["bound"], vector["base"]]
        expected = optional_text(pollard_p_minus_one(*(int(value) for value in arguments)))
        check_equal("Rust p-minus-one", expected, run([rust, "p-minus-one", *arguments]))
        checks += 1

    for vector in vectors["pollard_p_plus_one"]:
        arguments = [vector["n"], vector["bound"], vector["parameter"]]
        expected = optional_text(pollard_p_plus_one(*(int(value) for value in arguments)))
        check_equal("Rust p-plus-one", expected, run([rust, "p-plus-one", *arguments]))
        checks += 1

    for vector in vectors["batch_gcd"]:
        modulus = vector["modulus"]
        values = ",".join(vector["values"])
        expected = ",".join(str(value) for value in batch_gcd(
            [int(value) for value in vector["values"]],
            int(modulus),
        ))
        check_equal("Rust batch-gcd", expected, run([rust, "batch-gcd", modulus, values]))
        check_equal("C# batch-gcd", expected, run([*csharp, "batch-gcd", modulus, values]))
        checks += 2

    print(f"Baseline differential validation: PASS ({checks} cross-language checks)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
