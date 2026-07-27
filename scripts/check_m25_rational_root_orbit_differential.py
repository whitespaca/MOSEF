"""Differentially check selected M25 rational-root orbit vectors."""

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
from mosef_reference import classify_rational_root_orbit  # noqa: E402


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
    boolean = lambda item: str(item).lower()
    return (
        f"first_factor:{value.first_factor}|second_factor:{value.second_factor}|"
        f"order:{value.order}|category:{value.category}|"
        f"outside_stage_zeros:{boolean(value.outside_stage_zeros)}|"
        f"phase_order:{value.phase_order}|"
        f"phase_divisible:{boolean(value.phase_divisible)}|"
        f"rational_ratio:{optional(value.rational_ratio)}|"
        f"primitive_first_coefficient:"
        f"{optional(value.primitive_first_coefficient)}|"
        f"primitive_second_coefficient:"
        f"{optional(value.primitive_second_coefficient)}|"
        f"common_step:{value.common_step}|"
        f"phi4_enabled:{boolean(value.phi4_enabled)}|"
        f"phi6_enabled:{boolean(value.phi6_enabled)}"
    )


def main() -> int:
    data = json.loads(
        (ROOT / "schemas/m25-rational-root-orbit-vectors-v1.json").read_text()
    )
    vectors = data["rational_root_orbit_vectors"]
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
        arguments = [
            vector["first_factor"],
            vector["second_factor"],
            vector["order"],
        ]
        value = classify_rational_root_orbit(*arguments)
        if asdict(value) != vector:
            raise AssertionError("registered vector disagrees with Python")
        expected = protocol(value)
        text_arguments = [str(item) for item in arguments]
        for command, env_arg in (
            ([str(rust), "rational-root-orbit", *text_arguments], None),
            ([*csharp, "rational-root-orbit", *text_arguments], env),
        ):
            actual = run(command, env_arg)
            if actual != expected:
                raise AssertionError(
                    "rational-root orbit disagreement: "
                    f"{text_arguments}\nexpected={expected}\nactual={actual}"
                )
            checks += 1
    print(f"M25 rational-root differential validation: PASS ({checks} checks)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
