"""Differentially check selected M24 rational-residue audit vectors."""

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
from mosef_reference import evaluate_rational_residue_audit


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


def optional(value: int | None) -> str:
    return "none" if value is None else str(value)


def protocol(value: Any) -> str:
    return (
        f"first_factor:{value.first_factor}|second_factor:{value.second_factor}|"
        f"first_coefficient:{value.first_coefficient}|"
        f"second_coefficient:{value.second_coefficient}|content:{value.content}|"
        f"primitive_first_coefficient:{value.primitive_first_coefficient}|"
        f"primitive_second_coefficient:{value.primitive_second_coefficient}|"
        f"content_gcd:{value.content_gcd}|content_status:{value.content_status}|"
        f"first_quotient:{value.first_quotient_residue}|"
        f"second_quotient:{value.second_quotient_residue}|"
        f"first_quotient_gcd:{value.first_quotient_gcd}|"
        f"second_quotient_gcd:{value.second_quotient_gcd}|"
        f"aggregate:{value.aggregate_residue}|aggregate_gcd:{value.aggregate_gcd}|"
        f"primitive_aggregate:{value.primitive_aggregate_residue}|"
        f"primitive_aggregate_gcd:{value.primitive_aggregate_gcd}|"
        f"prefix_status:{value.prefix_status}|rational:{optional(value.rational_residue)}|"
        f"rational_gcd:{optional(value.rational_gcd)}|"
        f"primitive_rational:{optional(value.primitive_rational_residue)}|"
        f"primitive_rational_gcd:{optional(value.primitive_rational_gcd)}|"
        f"first_overlap_gcd:{value.first_overlap_gcd}|"
        f"first_public_bound_gcd:{value.first_public_bound_gcd}|"
        f"second_overlap_gcd:{value.second_overlap_gcd}|"
        f"second_public_bound_gcd:{value.second_public_bound_gcd}|"
        f"first_resultant_base:{value.first_resultant_base}|"
        f"first_resultant_exponent:{value.first_resultant_exponent}|"
        f"second_resultant_coefficient_base:"
        f"{value.second_resultant_coefficient_base}|"
        f"second_resultant_coefficient_exponent:"
        f"{value.second_resultant_coefficient_exponent}|"
        f"second_resultant_stage_base:{value.second_resultant_stage_base}|"
        f"second_resultant_stage_exponent:{value.second_resultant_stage_exponent}"
    )


def main() -> int:
    data = json.loads(
        (
            ROOT / "schemas/m24-rational-residue-audit-vectors-v1.json"
        ).read_text()
    )
    vectors = data["rational_residue_audit_vectors"]
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
        arguments = [
            vector["base"],
            vector["modulus"],
            vector["first_factor"],
            vector["second_factor"],
            vector["first_coefficient"],
            vector["second_coefficient"],
        ]
        value = evaluate_rational_residue_audit(*arguments)
        if asdict(value) != vector:
            raise AssertionError("registered vector disagrees with Python")
        expected = protocol(value)
        text_arguments = [str(item) for item in arguments]
        for command, env_arg in (
            ([str(rust), "rational-residue-audit", *text_arguments], None),
            ([*csharp, "rational-residue-audit", *text_arguments], env),
        ):
            actual = run(command, env_arg)
            if actual != expected:
                raise AssertionError(
                    "rational-residue audit disagreement: "
                    f"{text_arguments}\nexpected={expected}\nactual={actual}"
                )
            checks += 1
    print(f"M24 rational-residue differential validation: PASS ({checks} checks)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
