"""Minimal stdlib checker for the consolidated M50 threshold artifact."""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "m50-finite-threshold-summary-v1.json"
TABLE_EN = ROOT / "paper" / "tables" / "finite-threshold-summary-en.tex"
TABLE_KO = ROOT / "paper" / "tables" / "finite-threshold-summary-ko.tex"


def read_json(path: Path) -> dict[str, Any]:
    """Read one JSON object using only the Python standard library."""
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise AssertionError(f"{path.relative_to(ROOT)} is not a JSON object")
    return value


def canonical_hash(value: dict[str, Any]) -> str:
    """Recompute the artifact's canonical SHA-256."""
    canonical = dict(value)
    canonical.pop("summary_sha256", None)
    encoded = json.dumps(
        canonical,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def source_sha256(relative_path: str) -> str:
    """Hash one frozen source schema."""
    return hashlib.sha256((ROOT / relative_path).read_bytes()).hexdigest()


def check_row_arithmetic(row: dict[str, Any]) -> None:
    """Check the family-relative threshold arithmetic in one row."""
    input_length = int(row["input_length"])
    cap = int(row["family_relative_minimal_cap"])
    if int(row["local_offset"]) != cap - input_length:
        raise AssertionError(f"wrong local offset at m={input_length}")
    endpoint = row["strict_endpoint"]
    if int(endpoint["numerator"]) != cap - 1:
        raise AssertionError(f"wrong endpoint numerator at m={input_length}")
    if int(endpoint["denominator"]) != input_length:
        raise AssertionError(f"wrong endpoint denominator at m={input_length}")
    reduced = Fraction(cap - 1, input_length)
    if int(endpoint["reduced_numerator"]) != reduced.numerator:
        raise AssertionError(f"wrong reduced endpoint numerator at m={input_length}")
    if int(endpoint["reduced_denominator"]) != reduced.denominator:
        raise AssertionError(f"wrong reduced endpoint denominator at m={input_length}")


def check_source_projection(row: dict[str, Any], source: dict[str, Any]) -> None:
    """Check a row against the authoritative fields in its registered source."""
    input_length = int(row["input_length"])
    if input_length <= 15:
        profiles = {
            int(profile["input_length"]): profile
            for profile in source["selector_profiles"]
        }
        profile = profiles[input_length]
        expected_cap = input_length
        expected_population = int(profile["population_size"])
        expected_buckets = None
        expected_repair_count = None
        expected_repair_status = "NOT_APPLICABLE_DOMAIN_FLOOR"
        if int(profile["collision_pair_count"]) != 0:
            raise AssertionError(f"noninjective M31 source at m={input_length}")
    elif input_length <= 20:
        records = {
            int(record["input_length"]): record
            for record in source["threshold_records"]
        }
        record = records[input_length]
        expected_cap = int(record["minimal_selector_cap"])
        expected_population = int(record["population_size"])
        expected_buckets = record["predecessor_collision_buckets"]
        expected_repair_count = None
        expected_repair_status = "NOT_SEPARATELY_CERTIFIED"
    else:
        repair = source["repair_profile"]
        predecessor = source.get("predecessor_profile") or source["failed_profile"]
        expected_cap = int(repair["selector_cap"])
        expected_population = int(repair["population_size"])
        expected_buckets = predecessor["collision_buckets"]
        if int(source["input_length"]) != input_length:
            raise AssertionError(f"wrong source input length at m={input_length}")
        if int(repair["collision_pair_count"]) != 0:
            raise AssertionError(f"noninjective repair source at m={input_length}")
        expected_repair_count = repair.get("new_repair_coordinate_count")
        if expected_repair_count is None:
            expected_repair_count = source.get("construction_certificate", {}).get(
                "minimum_new_coordinate_count"
            )
        if expected_repair_count is None:
            expected_repair_status = "NOT_SEPARATELY_CERTIFIED"
        else:
            expected_repair_count = int(expected_repair_count)
            expected_repair_status = "CERTIFIED_MINIMUM"
    if int(row["family_relative_minimal_cap"]) != expected_cap:
        raise AssertionError(f"wrong cap projection at m={input_length}")
    if int(row["population_size"]) != expected_population:
        raise AssertionError(f"wrong population projection at m={input_length}")
    if row["predecessor_collision_buckets"] != expected_buckets:
        raise AssertionError(f"wrong predecessor projection at m={input_length}")
    if row["repair_coordinate_count"] != expected_repair_count:
        raise AssertionError(f"wrong repair-coordinate count at m={input_length}")
    if row["repair_coordinate_status"] != expected_repair_status:
        raise AssertionError(f"wrong repair-coordinate status at m={input_length}")


def check_table_markers(rows: list[dict[str, Any]]) -> None:
    """Check that both paper fragments expose every shared row and scope column."""
    english = TABLE_EN.read_text(encoding="utf-8")
    korean = TABLE_KO.read_text(encoding="utf-8")
    for row in rows:
        marker = (
            f"{row['input_length']} & {row['population_size']} & "
            f"{row['family_relative_minimal_cap']} & {row['local_offset']} &"
        )
        if english.count(marker) != 1 or korean.count(marker) != 1:
            raise AssertionError(f"bilingual table row mismatch at m={row['input_length']}")
        for claim_id in row["evidence_ids"]:
            token = rf"\texttt{{{claim_id}}}"
            if token not in english or token not in korean:
                raise AssertionError(f"missing bilingual evidence anchor {claim_id}")


def main() -> int:
    """Verify hashes, source projections, arithmetic, and bilingual table rows."""
    artifact = read_json(ARTIFACT)
    if artifact["schema_version"] != "1.0.0":
        raise AssertionError("unsupported M50 artifact schema version")
    if artifact["source_snapshot_commit"] != "e286a0042ca2cda57fdc31e143ecc65605ea57fd":
        raise AssertionError("M50 source snapshot commit changed")
    if artifact["summary_sha256"] != canonical_hash(artifact):
        raise AssertionError("M50 canonical summary hash changed")
    if artifact["finite_window"] != {
        "minimum_input_length": 9,
        "maximum_input_length": 34,
    }:
        raise AssertionError("M50 finite window changed")
    required_scope = ("no asymptotic rate", "all-selector lower bound", "general factoring")
    scope = str(artifact["scope"]).lower()
    if any(phrase not in scope for phrase in required_scope):
        raise AssertionError("M50 scope warning is incomplete")

    source_records = {
        str(record["path"]): record for record in artifact["sources"]
    }
    if len(source_records) != 16 or len(artifact["sources"]) != 16:
        raise AssertionError("M50 must freeze exactly 16 distinct source schemas")
    sources: dict[str, dict[str, Any]] = {}
    for relative_path, record in source_records.items():
        if source_sha256(relative_path) != record["file_sha256"]:
            raise AssertionError(f"source hash changed: {relative_path}")
        source = read_json(ROOT / relative_path)
        if source.get("summary_sha256") != record["embedded_summary_sha256"]:
            raise AssertionError(f"embedded source hash changed: {relative_path}")
        sources[relative_path] = source

    rows = artifact["rows"]
    if [int(row["input_length"]) for row in rows] != list(range(9, 35)):
        raise AssertionError("M50 rows do not cover exactly m=9..34")
    if {str(row["source_schema"]) for row in rows} != set(source_records):
        raise AssertionError("M50 row sources do not match the frozen source set")
    for row in rows:
        check_row_arithmetic(row)
        check_source_projection(row, sources[str(row["source_schema"])])
    check_table_markers(rows)
    print(
        "M50 minimal certificate checker: PASS "
        f"({len(rows)} rows, {len(sources)} frozen source schemas, "
        "2 synchronized paper tables)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
