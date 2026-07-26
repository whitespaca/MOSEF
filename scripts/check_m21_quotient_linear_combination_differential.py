"""Differentially check selected M21 signed quotient-combination vectors."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
from mosef_reference import evaluate_quotient_linear_combination  # noqa: E402


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
    def join(items: Any) -> str:
        return ",".join(map(str, items))

    quotients = tuple(stage.quotient_residue for stage in value.chain.stages)
    quotient_gcds = tuple(stage.quotient_gcd for stage in value.chain.stages)
    return (
        f"factors:{join(value.factors)}|coefficients:{join(value.coefficients)}|"
        f"coefficient_residues:{join(value.coefficient_residues)}|"
        f"coefficient_gcds:{join(value.coefficient_gcds)}|"
        f"quotients:{join(quotients)}|quotient_gcds:{join(quotient_gcds)}|"
        f"weighted:{join(value.weighted_stage_residues)}|"
        f"weighted_gcds:{join(value.weighted_stage_gcds)}|"
        f"aggregate:{value.aggregate_residue}|aggregate_gcd:{value.aggregate_gcd}"
    )


def check_registered_fields(vector: dict[str, Any], value: Any) -> None:
    actual = {
        "coefficient_residues": list(value.coefficient_residues),
        "quotients": [stage.quotient_residue for stage in value.chain.stages],
        "quotient_gcds": [stage.quotient_gcd for stage in value.chain.stages],
        "weighted": list(value.weighted_stage_residues),
        "weighted_gcds": list(value.weighted_stage_gcds),
        "aggregate": value.aggregate_residue,
        "aggregate_gcd": value.aggregate_gcd,
    }
    expected = {field: vector[field] for field in actual}
    if actual != expected:
        raise AssertionError(
            f"registered vector disagrees with Python: expected {expected}, got {actual}"
        )


def main() -> int:
    data = json.loads(
        (
            ROOT / "schemas/m21-quotient-linear-combination-vectors-v1.json"
        ).read_text()
    )
    vectors = data["quotient_linear_combination_vectors"]
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
        value = evaluate_quotient_linear_combination(
            vector["base"],
            vector["modulus"],
            vector["factors"],
            vector["coefficients"],
        )
        check_registered_fields(vector, value)
        expected = protocol(value)
        factors = ",".join(map(str, vector["factors"]))
        coefficients = ",".join(map(str, vector["coefficients"]))
        args = [
            str(vector["base"]),
            str(vector["modulus"]),
            factors,
            coefficients,
        ]
        for command, env_arg in (
            ([str(rust), "quotient-linear-combination", *args], None),
            ([*csharp, "quotient-linear-combination", *args], env),
        ):
            if run(command, env_arg) != expected:
                raise AssertionError(f"quotient linear-combination disagreement: {args}")
            checks += 1
    print(
        f"M21 quotient linear-combination differential validation: PASS ({checks} checks)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
