"""Differentially check selected M27 overlap descriptors."""

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
from mosef_reference import exceptional_cofactor_overlap


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
    support = ",".join(str(item) for item in value.stage_overlap_support)
    return "|".join(
        (
            f"family:{value.family}",
            f"order:{value.order}",
            f"first_factor:{value.first_factor}",
            f"second_factor:{value.second_factor}",
            f"cofactor_degree:{value.cofactor_degree}",
            f"remainder_constant:{value.remainder_constant}",
            f"remainder_linear:{value.remainder_linear}",
            (
                "cyclotomic_cofactor_resultant:"
                f"{value.cyclotomic_cofactor_resultant}"
            ),
            f"first_stage_resultant_base:{value.first_stage_resultant_base}",
            (
                "first_stage_resultant_exponent:"
                f"{value.first_stage_resultant_exponent}"
            ),
            (
                "second_stage_power_of_two_exponent:"
                f"{value.second_stage_power_of_two_exponent}"
            ),
            f"second_stage_resultant_base:{value.second_stage_resultant_base}",
            (
                "second_stage_resultant_exponent:"
                f"{value.second_stage_resultant_exponent}"
            ),
            f"stage_overlap_support:{support}",
        )
    )


def main() -> int:
    data = json.loads(
        (
            ROOT / "schemas/m27-exceptional-cofactor-overlap-vectors-v1.json"
        ).read_text()
    )
    vectors = data["exceptional_cofactor_overlap_vectors"]
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
            vector["first_factor"],
            vector["second_factor"],
            vector["family"],
        )
        value = exceptional_cofactor_overlap(*arguments)
        expected_record = dict(vector)
        expected_record["stage_overlap_support"] = tuple(
            expected_record["stage_overlap_support"]
        )
        if asdict(value) != expected_record:
            raise AssertionError("registered vector disagrees with Python")
        expected = protocol(value)
        text_arguments = [str(item) for item in arguments]
        for command, env_arg in (
            ([str(rust), "exceptional-cofactor-overlap", *text_arguments], None),
            ([*csharp, "exceptional-cofactor-overlap", *text_arguments], env),
        ):
            actual = run(command, env_arg)
            if actual != expected:
                raise AssertionError(
                    "exceptional-cofactor overlap disagreement: "
                    f"{text_arguments}\nexpected={expected}\nactual={actual}"
                )
            checks += 1
    print(
        f"M27 exceptional-cofactor differential validation: "
        f"PASS ({checks} checks)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
