"""Differentially check selected M20 iterated quotient-chain vectors."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
from mosef_reference import evaluate_iterated_quotient  # noqa: E402


def run(command: list[str], env: dict[str, str] | None = None) -> str:
    return subprocess.run(
        command,
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env,
    ).stdout.strip()


def protocol(value: Any) -> str:
    prefixes = ",".join(map(str, value.prefix_exponents))
    stages = ";".join(
        ",".join(
            map(
                str,
                (
                    stage.inner_power_residue,
                    stage.intermediate_residue,
                    stage.intermediate_gcd,
                    stage.quotient_residue,
                    stage.quotient_gcd,
                    stage.rational_numerator_residue,
                    stage.rational_numerator_gcd,
                    stage.composed_denominator_gcd,
                    stage.endpoint_gcd,
                    stage.multiplier_gcd,
                    stage.rational_division_status,
                    stage.composed_division_status,
                ),
            )
        )
        for stage in value.stages
    )
    return (
        f"prefixes:{prefixes}|final_product:{value.final_quotient_product_residue}|"
        f"final_prefix:{value.final_prefix_residue}|final_gcd:{value.final_prefix_gcd}|"
        f"stages:{stages}"
    )


def check_registered_fields(vector: dict[str, Any], value: Any) -> None:
    actual = {
        "prefix_exponents": list(value.prefix_exponents),
        "final_product": value.final_quotient_product_residue,
        "final_prefix": value.final_prefix_residue,
        "final_gcd": value.final_prefix_gcd,
    }
    expected = {field: vector[field] for field in actual}
    if actual != expected:
        raise AssertionError(
            f"registered vector disagrees with Python: expected {expected}, got {actual}"
        )


def main() -> int:
    data = json.loads(
        (ROOT / "schemas/m20-iterated-quotient-vectors-v1.json").read_text()
    )
    vectors = data["iterated_quotient_vectors"]
    env = os.environ.copy()
    env["APPDATA"] = str(ROOT / "verification/csharp/obj/sandbox-appdata")
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
        env,
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
        env,
    )
    rust = ROOT / "target/debug/mosef-baseline.exe"
    csharp = [
        "dotnet",
        str(ROOT / "verification/csharp/bin/Debug/net8.0/MosefVerifier.dll"),
    ]
    checks = 0
    for vector in vectors:
        value = evaluate_iterated_quotient(
            vector["base"], vector["modulus"], vector["factors"]
        )
        check_registered_fields(vector, value)
        expected = protocol(value)
        factors = ",".join(map(str, vector["factors"]))
        args = [str(vector["base"]), str(vector["modulus"]), factors]
        for command, env_arg in (
            ([str(rust), "iterated-quotient", *args], None),
            ([*csharp, "iterated-quotient", *args], env),
        ):
            if run(command, env_arg) != expected:
                raise AssertionError(f"iterated quotient disagreement: {args}")
            checks += 1
    print(f"M20 iterated-quotient differential validation: PASS ({checks} checks)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
