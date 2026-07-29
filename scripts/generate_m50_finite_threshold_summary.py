"""Generate the M50 finite family-relative threshold summary and paper tables."""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "schemas" / "m50-finite-threshold-summary-v1.json"
TABLE_EN = ROOT / "paper" / "tables" / "finite-threshold-summary-en.tex"
TABLE_KO = ROOT / "paper" / "tables" / "finite-threshold-summary-ko.tex"
SOURCE_SNAPSHOT_COMMIT = "e286a0042ca2cda57fdc31e143ecc65605ea57fd"

M31_SOURCE = "schemas/m31-diversified-compact-signature-vectors-v1.json"
M32_SOURCE = "schemas/m32-widened-selector-cap-v1.json"
FOLLOWUP_SOURCES = (
    (21, "schemas/m33-linear-cap-recurrence-v1.json"),
    (22, "schemas/m34-next-envelope-v1.json"),
    (23, "schemas/m35-next-envelope-v1.json"),
    (24, "schemas/m36-distinct-cap-v1.json"),
    (25, "schemas/m37-length-25-cap-v1.json"),
    (26, "schemas/m38-length-26-cap-v1.json"),
    (27, "schemas/m39-length-27-cap-v1.json"),
    (28, "schemas/m40-length-28-cap-v1.json"),
    (29, "schemas/m41-length-29-cap-v1.json"),
    (30, "schemas/m42-length-30-cap-v1.json"),
    (31, "schemas/m43-length-31-cap-v1.json"),
    (32, "schemas/m44-length-32-cap-v1.json"),
    (33, "schemas/m45-length-33-cap-v1.json"),
    (34, "schemas/m46-length-34-cap-v1.json"),
)


def load_json(relative_path: str) -> dict[str, Any]:
    """Load one registered JSON artifact."""
    return json.loads((ROOT / relative_path).read_text(encoding="utf-8"))


def file_sha256(relative_path: str) -> str:
    """Return the SHA-256 digest of one registered source artifact."""
    return hashlib.sha256((ROOT / relative_path).read_bytes()).hexdigest()


def canonical_hash(value: dict[str, Any]) -> str:
    """Hash a JSON object with the summary hash field omitted."""
    canonical = dict(value)
    canonical.pop("summary_sha256", None)
    encoded = json.dumps(
        canonical,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def evidence_ids(input_length: int) -> list[str]:
    """Return the theorem, barrier, and experiment anchors for one row."""
    if input_length <= 15:
        return ["THM-004", "EMP-030"]
    if input_length <= 20:
        return ["THM-005", "BAR-026", "EMP-031"]
    theorem_number = input_length - 15
    barrier_number = input_length + 6
    experiment_number = input_length + 11
    return [
        f"THM-{theorem_number:03d}",
        f"BAR-{barrier_number:03d}",
        f"EMP-{experiment_number:03d}",
    ]


def threshold_row(
    *,
    input_length: int,
    population_size: int,
    selector_cap: int,
    predecessor_buckets: list[list[int]] | None,
    repair_coordinate_count: int | None,
    repair_coordinate_status: str,
    source_schema: str,
) -> dict[str, Any]:
    """Build one normalized finite-threshold row."""
    endpoint = Fraction(selector_cap - 1, input_length)
    return {
        "input_length": input_length,
        "population_size": population_size,
        "family_relative_minimal_cap": selector_cap,
        "local_offset": selector_cap - input_length,
        "strict_endpoint": {
            "numerator": selector_cap - 1,
            "denominator": input_length,
            "reduced_numerator": endpoint.numerator,
            "reduced_denominator": endpoint.denominator,
        },
        "predecessor_collision_buckets": predecessor_buckets,
        "repair_coordinate_count": repair_coordinate_count,
        "repair_coordinate_status": repair_coordinate_status,
        "evidence_ids": evidence_ids(input_length),
        "source_schema": source_schema,
    }


def build_rows() -> list[dict[str, Any]]:
    """Extract all 26 registered thresholds from the M31--M46 artifacts."""
    rows: list[dict[str, Any]] = []
    m31 = load_json(M31_SOURCE)
    profiles = {
        int(profile["input_length"]): profile
        for profile in m31["selector_profiles"]
    }
    for input_length in range(9, 16):
        profile = profiles[input_length]
        if int(profile["collision_pair_count"]) != 0:
            raise ValueError(f"M31 profile at m={input_length} is not injective")
        rows.append(
            threshold_row(
                input_length=input_length,
                population_size=int(profile["population_size"]),
                selector_cap=input_length,
                predecessor_buckets=None,
                repair_coordinate_count=None,
                repair_coordinate_status="NOT_APPLICABLE_DOMAIN_FLOOR",
                source_schema=M31_SOURCE,
            )
        )

    m32 = load_json(M32_SOURCE)
    for record in m32["threshold_records"]:
        input_length = int(record["input_length"])
        rows.append(
            threshold_row(
                input_length=input_length,
                population_size=int(record["population_size"]),
                selector_cap=int(record["minimal_selector_cap"]),
                predecessor_buckets=[
                    [int(prime) for prime in bucket]
                    for bucket in record["predecessor_collision_buckets"]
                ],
                repair_coordinate_count=None,
                repair_coordinate_status="NOT_SEPARATELY_CERTIFIED",
                source_schema=M32_SOURCE,
            )
        )

    for input_length, source_schema in FOLLOWUP_SOURCES:
        data = load_json(source_schema)
        if int(data["input_length"]) != input_length:
            raise ValueError(f"{source_schema} has the wrong input length")
        repair = data["repair_profile"]
        predecessor = data.get("predecessor_profile") or data["failed_profile"]
        if int(repair["collision_pair_count"]) != 0:
            raise ValueError(f"{source_schema} repair profile is not injective")
        repair_count = repair.get("new_repair_coordinate_count")
        if repair_count is None:
            repair_count = data.get("construction_certificate", {}).get(
                "minimum_new_coordinate_count"
            )
        rows.append(
            threshold_row(
                input_length=input_length,
                population_size=int(repair["population_size"]),
                selector_cap=int(repair["selector_cap"]),
                predecessor_buckets=[
                    [int(prime) for prime in bucket]
                    for bucket in predecessor["collision_buckets"]
                ],
                repair_coordinate_count=(
                    None if repair_count is None else int(repair_count)
                ),
                repair_coordinate_status=(
                    "NOT_SEPARATELY_CERTIFIED"
                    if repair_count is None
                    else "CERTIFIED_MINIMUM"
                ),
                source_schema=source_schema,
            )
        )

    if [row["input_length"] for row in rows] != list(range(9, 35)):
        raise ValueError("threshold rows do not cover exactly m=9..34")
    return rows


def build_artifact() -> dict[str, Any]:
    """Build the complete consolidated artifact."""
    source_paths = [M31_SOURCE, M32_SOURCE, *(path for _, path in FOLLOWUP_SOURCES)]
    sources = []
    for source_path in source_paths:
        source = load_json(source_path)
        sources.append(
            {
                "path": source_path,
                "file_sha256": file_sha256(source_path),
                "schema_version": source.get("schema_version"),
                "embedded_summary_sha256": source.get("summary_sha256"),
            }
        )
    artifact: dict[str, Any] = {
        "schema_version": "1.0.0",
        "artifact_id": "ART-M50-FINITE-THRESHOLDS",
        "source_snapshot_commit": SOURCE_SNAPSHOT_COMMIT,
        "selector_family": "DEF-032 T_{m,L}",
        "population": "balanced primes P_m",
        "finite_window": {"minimum_input_length": 9, "maximum_input_length": 34},
        "scope": (
            "Complete finite family-relative thresholds only; no asymptotic "
            "rate, promise recognizer, all-selector lower bound, or general "
            "factoring conclusion."
        ),
        "rows": build_rows(),
        "sources": sources,
    }
    artifact["summary_sha256"] = canonical_hash(artifact)
    return artifact


def endpoint_tex(row: dict[str, Any]) -> str:
    """Format one strict endpoint as a reduced TeX fraction."""
    endpoint = row["strict_endpoint"]
    numerator = endpoint["reduced_numerator"]
    denominator = endpoint["reduced_denominator"]
    if denominator == 1:
        return str(numerator)
    return rf"\(\frac{{{numerator}}}{{{denominator}}}\)"


def buckets_tex(row: dict[str, Any], *, korean: bool) -> str:
    """Format predecessor collision buckets for a compact paper cell."""
    buckets = row["predecessor_collision_buckets"]
    if buckets is None:
        return "정의역 하한" if korean else "domain floor"
    return "; ".join(
        r"\(\{" + ",".join(str(prime) for prime in bucket) + r"\}\)"
        for bucket in buckets
    )


def repair_tex(row: dict[str, Any]) -> str:
    """Format the certified incremental-repair count."""
    status = row["repair_coordinate_status"]
    if status == "CERTIFIED_MINIMUM":
        return str(row["repair_coordinate_count"])
    if status == "NOT_APPLICABLE_DOMAIN_FLOOR":
        return "--"
    return "n.c."


def render_table(rows: list[dict[str, Any]], *, korean: bool) -> str:
    """Render one bilingual longtable fragment from the shared rows."""
    predecessor = (
        r"\(L_m^\star-1\) 충돌 bucket"
        if korean
        else r"collision bucket at \(L_m^\star-1\)"
    )
    evidence = "근거" if korean else "evidence"
    lines = [
        r"\begingroup",
        r"\scriptsize",
        r"\setlength{\tabcolsep}{3pt}",
        r"\begin{longtable}{rrrrrL{3.3cm}rL{2.5cm}}",
        r"\toprule",
        (
            rf"\(m\) & \(|\mathcal P_m|\) & \(L_m^\star\) & "
            rf"\(L_m^\star-m\) & \((L_m^\star-1)/m\) & {predecessor} & "
            rf"\(\Delta\) 좌표 & {evidence} \\"
            if korean
            else rf"\(m\) & \(|\mathcal P_m|\) & \(L_m^\star\) & "
            rf"\(L_m^\star-m\) & \((L_m^\star-1)/m\) & {predecessor} & "
            rf"\(\Delta\) coord. & {evidence} \\"
        ),
        r"\midrule",
        r"\endfirsthead",
        r"\toprule",
        (
            rf"\(m\) & \(|\mathcal P_m|\) & \(L_m^\star\) & "
            rf"\(L_m^\star-m\) & \((L_m^\star-1)/m\) & {predecessor} & "
            rf"\(\Delta\) 좌표 & {evidence} \\"
            if korean
            else rf"\(m\) & \(|\mathcal P_m|\) & \(L_m^\star\) & "
            rf"\(L_m^\star-m\) & \((L_m^\star-1)/m\) & {predecessor} & "
            rf"\(\Delta\) coord. & {evidence} \\"
        ),
        r"\midrule",
        r"\endhead",
    ]
    for row in rows:
        ids = ", ".join(rf"\texttt{{{claim_id}}}" for claim_id in row["evidence_ids"])
        lines.append(
            f"{row['input_length']} & {row['population_size']} & "
            f"{row['family_relative_minimal_cap']} & {row['local_offset']} & "
            f"{endpoint_tex(row)} & {buckets_tex(row, korean=korean)} & "
            f"{repair_tex(row)} & {ids} \\\\"
        )
    lines.extend([r"\bottomrule", r"\end{longtable}", r"\endgroup", ""])
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    """Parse generation or no-write verification mode."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="fail if the registered JSON or paper tables are not canonical",
    )
    return parser.parse_args()


def main() -> int:
    """Generate or verify the consolidated artifact and bilingual tables."""
    args = parse_args()
    artifact = build_artifact()
    json_text = json.dumps(artifact, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    table_en = render_table(artifact["rows"], korean=False)
    table_ko = render_table(artifact["rows"], korean=True)
    expected = ((OUTPUT, json_text), (TABLE_EN, table_en), (TABLE_KO, table_ko))
    if args.check:
        stale = [
            str(path.relative_to(ROOT))
            for path, text in expected
            if not path.exists() or path.read_text(encoding="utf-8") != text
        ]
        if stale:
            raise SystemExit(f"stale M50 generated artifacts: {', '.join(stale)}")
        print(
            "M50 finite-threshold generation check: PASS "
            f"({len(artifact['rows'])} rows, {len(artifact['sources'])} sources)"
        )
        return 0
    for path, text in expected:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        print(path.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
