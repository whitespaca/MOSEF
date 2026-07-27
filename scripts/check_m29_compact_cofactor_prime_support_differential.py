"""Differentially check selected M29 compact Phi4 prime profiles."""

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
from mosef_reference import phi4_prime_divisibility_profile


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


def boolean(value: bool) -> str:
    return str(value).lower()


def protocol(value: Any) -> str:
    return "|".join(
        (
            f"level:{value.level}",
            f"prime:{value.prime}",
            f"second_factor:{value.second_factor}",
            f"exponent:{value.exponent}",
            f"cofactor_residue:{value.cofactor_residue}",
            f"criterion_residue:{value.criterion_residue}",
            f"divides:{boolean(value.divides)}",
            f"rule:{value.rule}",
        )
    )


def main() -> int:
    data = json.loads(
        (
            ROOT
            / "schemas/m29-compact-cofactor-prime-support-vectors-v1.json"
        ).read_text(encoding="utf-8")
    )
    vectors = data["compact_phi4_prime_profiles"]
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
        level = vector["level"]
        prime = vector["prime"]
        value = phi4_prime_divisibility_profile(level, prime)
        if asdict(value) != vector["expected"]:
            raise AssertionError("registered vector disagrees with Python")
        expected = protocol(value)
        text_arguments = [str(level), str(prime)]
        for command, env_arg in (
            ([str(rust), "compact-phi4-prime-profile", *text_arguments], None),
            ([*csharp, "compact-phi4-prime-profile", *text_arguments], env),
        ):
            actual = run(command, env_arg)
            if actual != expected:
                raise AssertionError(
                    "compact Phi4 prime-profile disagreement: "
                    f"{text_arguments}\nexpected={expected}\nactual={actual}"
                )
            checks += 1
    print(
        "M29 compact cofactor prime-support differential validation: "
        f"PASS ({checks} checks)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
