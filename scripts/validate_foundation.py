"""Validate the dependency-free M0 research foundation."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "experiment-result-v1.schema.json"
EXAMPLE_PATH = ROOT / "schemas" / "examples" / "experiment-result-v1.example.json"

REQUIRED_FILES = (
    "research/ROADMAP.md",
    "research/STATUS.md",
    "research/CLAIMS.md",
    "research/DECISIONS.md",
    "research/BLOCKERS.md",
    "research/NEGATIVE_RESULTS.md",
    "research/literature/SOURCE_POLICY.md",
    "research/literature/BASELINE.md",
    "paper/main.tex",
    "paper/references.bib",
    "schemas/experiment-result-v1.schema.json",
    "schemas/examples/experiment-result-v1.example.json",
)

CLAIM_STATUSES = {
    "DEFINITION",
    "PROVED",
    "CONDITIONAL",
    "CONJECTURE",
    "HEURISTIC",
    "EMPIRICAL",
    "OPEN",
    "REFUTED",
}
RESULT_STATUSES = {"PASS", "FAIL", "ERROR", "SKIPPED"}
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
EXPERIMENT_RE = re.compile(r"^EXP-[0-9]{4,}$")

TOP_LEVEL_REQUIRED = {
    "schema_version",
    "experiment_id",
    "git_commit",
    "timestamp_utc",
    "host",
    "toolchains",
    "algorithm",
    "parameters",
    "seed",
    "input_manifest_sha256",
    "result",
    "timing",
    "peak_memory_bytes",
    "stdout_sha256",
    "status",
}
HOST_REQUIRED = {"os", "arch", "cpu", "logical_cores", "memory_bytes"}
TIMING_REQUIRED = {"wall_seconds", "cpu_seconds"}


def load_json(path: Path) -> dict[str, Any]:
    """Load a JSON object or raise a descriptive error."""
    with path.open(encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def validate_record(record: dict[str, Any]) -> list[str]:
    """Validate the executable subset of the experiment-result v1 contract."""
    errors: list[str] = []
    keys = set(record)
    missing = TOP_LEVEL_REQUIRED - keys
    extra = keys - TOP_LEVEL_REQUIRED
    if missing:
        errors.append(f"missing top-level fields: {sorted(missing)}")
    if extra:
        errors.append(f"unexpected top-level fields: {sorted(extra)}")

    if record.get("schema_version") != "1.0.0":
        errors.append("schema_version must be 1.0.0")
    if not isinstance(record.get("experiment_id"), str) or not EXPERIMENT_RE.fullmatch(
        record["experiment_id"]
    ):
        errors.append("experiment_id must match EXP-NNNN")
    if not isinstance(record.get("git_commit"), str) or not COMMIT_RE.fullmatch(
        record["git_commit"]
    ):
        errors.append("git_commit must be 40 lowercase hexadecimal characters")

    timestamp = record.get("timestamp_utc")
    if not isinstance(timestamp, str) or not timestamp.endswith("Z"):
        errors.append("timestamp_utc must be an RFC3339 UTC string ending in Z")
    else:
        try:
            datetime.fromisoformat(timestamp.removesuffix("Z") + "+00:00")
        except ValueError:
            errors.append("timestamp_utc is not a valid RFC3339 date-time")

    host = record.get("host")
    if not isinstance(host, dict):
        errors.append("host must be an object")
    else:
        host_missing = HOST_REQUIRED - set(host)
        host_extra = set(host) - HOST_REQUIRED
        if host_missing:
            errors.append(f"missing host fields: {sorted(host_missing)}")
        if host_extra:
            errors.append(f"unexpected host fields: {sorted(host_extra)}")
        for field in ("os", "arch", "cpu"):
            if not isinstance(host.get(field), str) or not host[field]:
                errors.append(f"host.{field} must be a nonempty string")
        for field in ("logical_cores", "memory_bytes"):
            if (
                not isinstance(host.get(field), int)
                or isinstance(host.get(field), bool)
                or host[field] < 1
            ):
                errors.append(f"host.{field} must be a positive integer")

    for field in ("toolchains", "parameters", "result"):
        if not isinstance(record.get(field), dict):
            errors.append(f"{field} must be an object")
    for field in ("algorithm", "seed"):
        if not isinstance(record.get(field), str) or not record[field]:
            errors.append(f"{field} must be a nonempty string")
    for field in ("input_manifest_sha256", "stdout_sha256"):
        if not isinstance(record.get(field), str) or not SHA256_RE.fullmatch(record[field]):
            errors.append(f"{field} must be 64 lowercase hexadecimal characters")

    timing = record.get("timing")
    if not isinstance(timing, dict):
        errors.append("timing must be an object")
    else:
        timing_missing = TIMING_REQUIRED - set(timing)
        timing_extra = set(timing) - TIMING_REQUIRED
        if timing_missing:
            errors.append(f"missing timing fields: {sorted(timing_missing)}")
        if timing_extra:
            errors.append(f"unexpected timing fields: {sorted(timing_extra)}")
        for field in TIMING_REQUIRED:
            value = timing.get(field)
            if (
                not isinstance(value, (int, float))
                or isinstance(value, bool)
                or value < 0
            ):
                errors.append(f"timing.{field} must be a nonnegative number")

    peak = record.get("peak_memory_bytes")
    if peak is not None and (
        not isinstance(peak, int) or isinstance(peak, bool) or peak < 0
    ):
        errors.append("peak_memory_bytes must be null or a nonnegative integer")
    if record.get("status") not in RESULT_STATUSES:
        errors.append(f"status must be one of {sorted(RESULT_STATUSES)}")
    return errors


def validate_schema_contract(schema: dict[str, Any]) -> list[str]:
    """Check that the published schema matches the executable contract."""
    errors: list[str] = []
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        errors.append("schema must declare JSON Schema draft 2020-12")
    if schema.get("additionalProperties") is not False:
        errors.append("schema must reject additional top-level properties")
    if set(schema.get("required", [])) != TOP_LEVEL_REQUIRED:
        errors.append("schema required fields do not match the executable contract")
    properties = schema.get("properties")
    if not isinstance(properties, dict) or set(properties) != TOP_LEVEL_REQUIRED:
        errors.append("schema properties do not match the executable contract")
    return errors


def validate_claim_statuses() -> list[str]:
    """Ensure every claims-ledger row uses an allowed status."""
    errors: list[str] = []
    claims_path = ROOT / "research" / "CLAIMS.md"
    row_re = re.compile(r"^\|\s*([A-Z]+-[A-Z0-9-]+|\w+-\d+)\s*\|\s*([A-Z]+)\s*\|")
    claim_rows = 0
    for line_number, line in enumerate(claims_path.read_text(encoding="utf-8").splitlines(), 1):
        match = row_re.match(line)
        if not match:
            continue
        claim_rows += 1
        claim_id, status = match.groups()
        if status not in CLAIM_STATUSES:
            errors.append(f"CLAIMS.md:{line_number}: {claim_id} has invalid status {status}")
    if claim_rows == 0:
        errors.append("CLAIMS.md contains no claim rows")
    return errors


def validate_citations() -> list[str]:
    """Check that all manuscript citation keys exist in the BibTeX file."""
    paper = (ROOT / "paper" / "main.tex").read_text(encoding="utf-8")
    bibliography = (ROOT / "paper" / "references.bib").read_text(encoding="utf-8")
    cited: set[str] = set()
    for group in re.findall(r"\\cite\{([^}]+)\}", paper):
        cited.update(key.strip() for key in group.split(","))
    defined = set(re.findall(r"@\w+\{([^,]+),", bibliography))
    return [f"paper citation key has no bibliography entry: {key}" for key in sorted(cited - defined)]


def validate_foundation() -> list[str]:
    """Run all M0 validation checks."""
    errors = [
        f"required file is missing: {relative}"
        for relative in REQUIRED_FILES
        if not (ROOT / relative).is_file()
    ]
    if errors:
        return errors
    schema = load_json(SCHEMA_PATH)
    example = load_json(EXAMPLE_PATH)
    errors.extend(validate_schema_contract(schema))
    errors.extend(validate_record(example))
    errors.extend(validate_claim_statuses())
    errors.extend(validate_citations())
    return errors


def main() -> int:
    """Command-line entry point."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--record",
        type=Path,
        help="also validate an experiment-result JSON record",
    )
    args = parser.parse_args()

    errors = validate_foundation()
    if args.record is not None:
        errors.extend(validate_record(load_json(args.record)))
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("M0 foundation validation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
