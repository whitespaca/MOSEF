"""Differentially check selected M19 nested quotient vectors."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
from mosef_reference import evaluate_nested_quotient


def run(command: list[str], env: dict[str, str] | None = None) -> str:
    return subprocess.run(
        command, cwd=ROOT, check=True, capture_output=True, text=True,
        encoding="utf-8", env=env
    ).stdout.strip()


def protocol(v: dict[str, Any]) -> str:
    none = lambda x: "none" if x is None else str(x)
    return (
        f"inner_power:{v['inner_power_residue']}|intermediate:{v['intermediate_residue']}|"
        f"intermediate_gcd:{v['intermediate_gcd']}|quotient:{v['quotient_residue']}|"
        f"quotient_gcd:{v['quotient_gcd']}|rational_numerator:{v['rational_numerator_residue']}|"
        f"rational_numerator_gcd:{v['rational_numerator_gcd']}|"
        f"composed_denominator:{v['composed_denominator_residue']}|"
        f"composed_denominator_gcd:{v['composed_denominator_gcd']}|"
        f"endpoint:{v['endpoint_residue']}|endpoint_gcd:{v['endpoint_gcd']}|"
        f"multiplier_gcd:{v['multiplier_gcd']}|"
        f"rational_status:{v['rational_division_status']}|"
        f"rational_quotient:{none(v['rational_division_quotient'])}|"
        f"composed_status:{v['composed_division_status']}|"
        f"composed_quotient:{none(v['composed_division_quotient'])}"
    )


def main() -> int:
    data = json.loads(
        (ROOT / "schemas/m19-nested-quotient-vectors-v1.json").read_text()
    )
    vectors = data["nested_quotient_vectors"]
    env = os.environ.copy()
    env["APPDATA"] = str(ROOT / "verification/csharp/obj/sandbox-appdata")
    run(["cargo", "build", "--quiet", "-p", "mosef-arithmetic", "--bin", "mosef-baseline"])
    run(["dotnet", "restore", "verification/csharp/MosefVerifier.csproj",
         "--configfile", "verification/csharp/NuGet.Config", "--verbosity", "quiet"], env)
    run(["dotnet", "build", "verification/csharp/MosefVerifier.csproj",
         "--nologo", "--no-restore", "--verbosity", "quiet"], env)
    rust = ROOT / "target/debug/mosef-baseline.exe"
    csharp = ["dotnet", str(ROOT / "verification/csharp/bin/Debug/net8.0/MosefVerifier.dll")]
    checks = 0
    for vector in vectors:
        expected = protocol(asdict(evaluate_nested_quotient(
            vector["base"], vector["modulus"], vector["inner_exponent"], vector["multiplier"]
        )))
        if expected != protocol(vector):
            raise AssertionError("registered vector disagrees with Python")
        args = list(map(str, (vector["base"], vector["modulus"],
                             vector["inner_exponent"], vector["multiplier"])))
        for command, env_arg in (([str(rust), "nested-quotient", *args], None),
                                 ([*csharp, "nested-quotient", *args], env)):
            if run(command, env_arg) != expected:
                raise AssertionError(f"nested quotient disagreement: {args}")
            checks += 1
    print(f"M19 nested-quotient differential validation: PASS ({checks} checks)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
