"""Differentially check selected M26 exceptional-cyclotomic vectors."""

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
from mosef_reference import evaluate_exceptional_cyclotomic  # noqa: E402


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


def optional(value: Any) -> str:
    return "none" if value is None else str(value)


def protocol(value: Any) -> str:
    return "|".join(
        (
            f"base:{value.base}",
            f"modulus:{value.modulus}",
            f"family:{value.family}",
            f"order:{value.order}",
            f"first_factor:{value.first_factor}",
            f"second_factor:{value.second_factor}",
            f"first_coefficient:{value.first_coefficient}",
            f"second_coefficient:{value.second_coefficient}",
            f"cyclotomic_residue:{value.cyclotomic_residue}",
            f"cyclotomic_gcd:{value.cyclotomic_gcd}",
            f"cyclotomic_status:{value.cyclotomic_status}",
            f"aggregate_residue:{value.aggregate_residue}",
            f"aggregate_gcd:{value.aggregate_gcd}",
            f"aggregate_status:{value.aggregate_status}",
            f"cofactor_residue:{optional(value.cofactor_residue)}",
            f"cofactor_gcd:{optional(value.cofactor_gcd)}",
            f"cofactor_status:{optional(value.cofactor_status)}",
            f"extraction_source:{value.extraction_source}",
            f"extraction_gcd:{optional(value.extraction_gcd)}",
            f"first_quotient_gcd:{value.first_quotient_gcd}",
            f"second_quotient_gcd:{value.second_quotient_gcd}",
            f"first_public_bound_gcd:{value.first_public_bound_gcd}",
            f"second_public_bound_gcd:{value.second_public_bound_gcd}",
            f"dense_cofactor_degree:{value.dense_cofactor_degree}",
            "dense_cofactor_coefficient_count:"
            f"{value.dense_cofactor_coefficient_count}",
        )
    )


def main() -> int:
    data = json.loads(
        (
            ROOT / "schemas/m26-exceptional-cyclotomic-vectors-v1.json"
        ).read_text()
    )
    vectors = data["exceptional_cyclotomic_vectors"]
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
        arguments = (
            vector["base"],
            vector["modulus"],
            vector["first_factor"],
            vector["second_factor"],
            vector["family"],
        )
        value = evaluate_exceptional_cyclotomic(*arguments)
        if asdict(value) != vector:
            raise AssertionError("registered vector disagrees with Python")
        expected = protocol(value)
        text_arguments = [str(item) for item in arguments]
        for command, env_arg in (
            ([str(rust), "exceptional-cyclotomic", *text_arguments], None),
            ([*csharp, "exceptional-cyclotomic", *text_arguments], env),
        ):
            actual = run(command, env_arg)
            if actual != expected:
                raise AssertionError(
                    "exceptional-cyclotomic disagreement: "
                    f"{text_arguments}\nexpected={expected}\nactual={actual}"
                )
            checks += 1
    print(
        f"M26 exceptional-cyclotomic differential validation: "
        f"PASS ({checks} checks)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
