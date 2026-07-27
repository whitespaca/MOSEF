"""Differentially check selected M30 compact Phi4 signatures."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
from mosef_reference import phi4_compact_signature


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


def protocol(levels: tuple[int, ...], prime: int, signature: int) -> str:
    return "|".join(
        (
            f"candidate_levels:{','.join(map(str, levels))}",
            f"prime:{prime}",
            f"signature:{signature}",
            f"hit_count:{signature.bit_count()}",
        )
    )


def main() -> int:
    data = json.loads(
        (
            ROOT / "schemas/m30-compact-support-signature-vectors-v1.json"
        ).read_text(encoding="utf-8")
    )
    vectors = data["compact_phi4_signatures"]
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
        levels = tuple(vector["candidate_levels"])
        prime = vector["prime"]
        signature = phi4_compact_signature(levels, prime)
        if signature != vector["expected_signature"]:
            raise AssertionError("registered vector disagrees with Python")
        expected = protocol(levels, prime, signature)
        text_arguments = [",".join(map(str, levels)), str(prime)]
        for command, env_arg in (
            ([str(rust), "compact-phi4-signature", *text_arguments], None),
            ([*csharp, "compact-phi4-signature", *text_arguments], env),
        ):
            actual = run(command, env_arg)
            if actual != expected:
                raise AssertionError(
                    "compact Phi4 signature disagreement: "
                    f"{text_arguments}\nexpected={expected}\nactual={actual}"
                )
            checks += 1
    print(
        "M30 compact support-signature differential validation: "
        f"PASS ({checks} checks)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
