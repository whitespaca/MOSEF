"""Differentially check selected M28 materialized-support profiles."""

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
from mosef_reference import length_indexed_support_profile


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
    return "|".join(
        (
            f"input_length:{value.input_length}",
            f"population_size:{value.population_size}",
            f"min_prime_log2_floor:{value.min_prime_log2_floor}",
            f"charged_value_count:{value.charged_value_count}",
            f"materialized_bit_budget:{value.materialized_bit_budget}",
            f"hit_primes:{','.join(str(item) for item in value.hit_primes)}",
            f"missed_primes:{','.join(str(item) for item in value.missed_primes)}",
            f"hit_prime_count:{value.hit_prime_count}",
            f"forced_miss_pair_count:{value.forced_miss_pair_count}",
            f"pair_count:{value.pair_count}",
            f"maximum_coverable_pair_count:{value.maximum_coverable_pair_count}",
            f"support_cap:{value.support_cap}",
            (
                "necessary_universal_bit_budget:"
                f"{value.necessary_universal_bit_budget}"
            ),
        )
    )


def main() -> int:
    data = json.loads(
        (
            ROOT / "schemas/m28-length-indexed-support-vectors-v1.json"
        ).read_text(encoding="utf-8")
    )
    vectors = data["length_indexed_support_vectors"]
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
        input_length = vector["input_length"]
        primes = tuple(vector["primes"])
        charged_values = tuple(vector["charged_values"])
        value = length_indexed_support_profile(
            input_length,
            primes,
            charged_values,
        )
        actual_record = asdict(value)
        actual_record["hit_primes"] = list(actual_record["hit_primes"])
        actual_record["missed_primes"] = list(actual_record["missed_primes"])
        if actual_record != vector["expected"]:
            raise AssertionError("registered vector disagrees with Python")
        expected = protocol(value)
        text_arguments = [
            str(input_length),
            ",".join(str(item) for item in primes),
            ",".join(str(item) for item in charged_values),
        ]
        for command, env_arg in (
            ([str(rust), "length-indexed-support-profile", *text_arguments], None),
            ([*csharp, "length-indexed-support-profile", *text_arguments], env),
        ):
            actual = run(command, env_arg)
            if actual != expected:
                raise AssertionError(
                    "length-indexed support disagreement: "
                    f"{text_arguments}\nexpected={expected}\nactual={actual}"
                )
            checks += 1
    print(f"M28 length-indexed differential validation: PASS ({checks} checks)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
