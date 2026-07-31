"""Independently validate the M82 bilingual focused-paper portfolio."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "schemas" / "m82-paper-portfolio-v1.json"
CLAIM_ROW = re.compile(r"^\| ([A-Z]+-\d+) \| ([A-Z]+) \|", re.MULTILINE)
PAPER_CLAIM = re.compile(r"\\claimstatus\{([A-Z]+-\d+)\}\{([A-Z]+)\}")
EXPECTED_ARCHIVE = {
    "english": "paper/main.tex",
    "korean": "paper/main-ko.tex",
    "claim_ledger": "research/CLAIMS.md",
}
EXPECTED_PAPERS: tuple[dict[str, Any], ...] = (
    {
        "id": "promise-factorization",
        "english": "paper/focused/promise-factorization-en.tex",
        "korean": "paper/focused/promise-factorization-ko.tex",
        "representative_claims": [
            "THM-001",
            "BAR-001",
            "BAR-002",
            "LEM-003",
            "THM-002",
            "BAR-003",
            "BAR-004",
        ],
        "reproduction_anchors": [
            "research/experiments/EXP-0003-m3-semismooth-search.md",
            "research/experiments/EXP-0006-m7-nonsplit-lucas.md",
        ],
    },
    {
        "id": "cyclotomic-extraction",
        "english": "paper/focused/cyclotomic-extraction-en.tex",
        "korean": "paper/focused/cyclotomic-extraction-ko.tex",
        "representative_claims": [
            "BAR-018",
            "BAR-019",
            "THM-003",
            "BAR-020",
            "BAR-021",
            "BAR-022",
            "BAR-023",
        ],
        "reproduction_anchors": [
            "research/experiments/EXP-0023-m24-rational-residue-audit.md",
            "research/experiments/EXP-0024-m25-rational-root-orbits.md",
            "research/experiments/EXP-0025-m26-exceptional-cyclotomic.md",
        ],
    },
    {
        "id": "finite-certificates",
        "english": "paper/focused/finite-certificates-en.tex",
        "korean": "paper/focused/finite-certificates-ko.tex",
        "representative_claims": [
            "BAR-024",
            "THM-021",
            "THM-022",
            "THM-023",
            "THM-024",
            "THM-004",
            "THM-005",
            "THM-014",
            "THM-019",
            "BAR-041",
            "BAR-046",
        ],
        "reproduction_anchors": [
            "schemas/m50-finite-threshold-summary-v1.json",
            "paper/tables/finite-threshold-summary-en.tex",
            "paper/tables/finite-threshold-summary-ko.tex",
        ],
    },
)
EXPECTED_SOURCE_PATHS = {
    EXPECTED_ARCHIVE["claim_ledger"],
    EXPECTED_ARCHIVE["english"],
    EXPECTED_ARCHIVE["korean"],
    "paper/focused/preamble-en.tex",
    "paper/focused/preamble-ko.tex",
    *(
        path
        for paper in EXPECTED_PAPERS
        for path in (paper["english"], paper["korean"])
    ),
}


def sha256_bytes(data: bytes) -> str:
    """Return a lowercase SHA-256 digest."""
    return hashlib.sha256(data).hexdigest()


def sha256_text_file(path: Path) -> str:
    """Hash UTF-8 text after universal-newline normalization."""
    return sha256_bytes(path.read_text(encoding="utf-8").encode("utf-8"))


def canonical_hash(value: Any) -> str:
    """Hash canonical compact JSON."""
    encoded = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return sha256_bytes(encoded)


def parse_unique_claims(text: str, pattern: re.Pattern[str]) -> tuple[list[tuple[str, str]], list[str]]:
    """Return ordered pairs and duplicate-ID errors."""
    pairs = pattern.findall(text)
    seen: set[str] = set()
    errors: list[str] = []
    for claim_id, _status in pairs:
        if claim_id in seen:
            errors.append(f"duplicate claim ID: {claim_id}")
        seen.add(claim_id)
    return pairs, errors


def validate_paper_pair(
    english_text: str,
    korean_text: str,
    expected_pairs: list[tuple[str, str]],
    paper_id: str,
) -> list[str]:
    """Validate one bilingual claim projection without file-system access."""
    errors: list[str] = []
    english_pairs, english_errors = parse_unique_claims(english_text, PAPER_CLAIM)
    korean_pairs, korean_errors = parse_unique_claims(korean_text, PAPER_CLAIM)
    errors.extend(f"{paper_id} English {error}" for error in english_errors)
    errors.extend(f"{paper_id} Korean {error}" for error in korean_errors)
    if english_pairs != expected_pairs:
        errors.append(f"{paper_id} English claim order/status mismatch")
    if korean_pairs != expected_pairs:
        errors.append(f"{paper_id} Korean claim order/status mismatch")
    if not 5 <= len(expected_pairs) <= 11:
        errors.append(f"{paper_id} must project 5--11 representative claims")
    if "general" not in english_text.lower() or "factoring" not in english_text.lower():
        errors.append(f"{paper_id} English general-factoring scope marker missing")
    if "일반" not in korean_text or "인수분해" not in korean_text:
        errors.append(f"{paper_id} Korean general-factoring scope marker missing")
    if paper_id == "promise-factorization":
        if "unrecognized" not in english_text.lower():
            errors.append("promise English unrecognized-membership marker missing")
        if "인식되지 않는" not in korean_text:
            errors.append("promise Korean unrecognized-membership marker missing")
    return errors


def validate_manifest(manifest: dict[str, Any]) -> list[str]:
    """Validate schema, hashes, coverage, bilingual claims, and scope."""
    errors: list[str] = []
    if manifest.get("schema_version") != "1.0.0":
        errors.append("unexpected schema version")
    if manifest.get("milestone") != "M82":
        errors.append("unexpected milestone")

    archive = manifest.get("archive")
    if archive != EXPECTED_ARCHIVE:
        errors.append("authoritative archive path mismatch")
    ledger_path = ROOT / EXPECTED_ARCHIVE["claim_ledger"]
    if not ledger_path.is_file():
        return errors + ["claim ledger missing"]
    ledger_pairs, ledger_errors = parse_unique_claims(
        ledger_path.read_text(encoding="utf-8"), CLAIM_ROW
    )
    errors.extend(f"ledger {error}" for error in ledger_errors)
    ledger = dict(ledger_pairs)
    if manifest.get("ledger_claim_count") != len(ledger):
        errors.append("ledger claim count mismatch")
    if manifest.get("claim_status_sha256") != canonical_hash(ledger_pairs):
        errors.append("claim status hash mismatch")

    projected: set[str] = set()
    papers = manifest.get("papers")
    if not isinstance(papers, list) or len(papers) != 3:
        return errors + ["portfolio must contain exactly three papers"]
    for paper, expected_paper in zip(papers, EXPECTED_PAPERS, strict=True):
        paper_id = paper.get("id", "<missing>")
        if paper_id != expected_paper["id"]:
            errors.append(f"unexpected paper ID/order: {paper_id}")
        for key in ("english", "korean", "representative_claims"):
            if paper.get(key) != expected_paper[key]:
                errors.append(f"{paper_id} registered {key} mismatch")
        if paper.get("reproduction_anchors") != expected_paper["reproduction_anchors"]:
            errors.append(f"{paper_id} reproduction-anchor list mismatch")
        claim_rows = paper.get("claim_statuses", [])
        expected_pairs = [
            (row.get("claim_id", ""), row.get("status", "")) for row in claim_rows
        ]
        ids = [claim_id for claim_id, _status in expected_pairs]
        if ids != paper.get("representative_claims"):
            errors.append(f"{paper_id} representative list mismatch")
        for claim_id, status in expected_pairs:
            if claim_id not in ledger:
                errors.append(f"{paper_id} unknown claim: {claim_id}")
            elif ledger[claim_id] != status:
                errors.append(f"{paper_id} status mismatch: {claim_id}")
            if claim_id in projected:
                errors.append(f"claim projected into multiple papers: {claim_id}")
            projected.add(claim_id)

        english_path = ROOT / expected_paper["english"]
        korean_path = ROOT / expected_paper["korean"]
        if not english_path.is_file() or not korean_path.is_file():
            errors.append(f"{paper_id} source file missing")
            continue
        errors.extend(
            validate_paper_pair(
                english_path.read_text(encoding="utf-8"),
                korean_path.read_text(encoding="utf-8"),
                expected_pairs,
                paper_id,
            )
        )
        for anchor in expected_paper["reproduction_anchors"]:
            if not (ROOT / anchor).is_file():
                errors.append(f"{paper_id} reproduction anchor missing: {anchor}")

    archive_rows = manifest.get("archive_only_claims", [])
    archive_pairs = [
        (row.get("claim_id", ""), row.get("status", "")) for row in archive_rows
    ]
    expected_archive = [
        (claim_id, status)
        for claim_id, status in ledger_pairs
        if claim_id not in projected
    ]
    if archive_pairs != expected_archive:
        errors.append("archive-only claim projection mismatch")
    if manifest.get("focused_claim_count") != len(projected):
        errors.append("focused claim count mismatch")
    if manifest.get("archive_only_claim_count") != len(expected_archive):
        errors.append("archive-only claim count mismatch")
    if len(projected) + len(expected_archive) != len(ledger):
        errors.append("claim coverage is not exhaustive")

    source_hashes = manifest.get("source_sha256")
    if not isinstance(source_hashes, dict):
        source_hashes = {}
        errors.append("source hash registry must be an object")
    if set(source_hashes) != EXPECTED_SOURCE_PATHS:
        errors.append("source hash path set mismatch")
    for relative, expected_hash in source_hashes.items():
        path = ROOT / relative
        if not path.is_file():
            errors.append(f"hashed source missing: {relative}")
        elif sha256_text_file(path) != expected_hash:
            errors.append(f"source hash mismatch: {relative}")

    scope = manifest.get("scope", {})
    if scope.get("general_classical_polynomial_time_factoring") != "OPEN":
        errors.append("general factoring scope must remain OPEN")
    if scope.get("focused_papers_are_claim_projections") is not True:
        errors.append("projection scope marker missing")
    if scope.get("archival_monograph_retained") is not True:
        errors.append("archive retention marker missing")
    if scope.get("finite_certificates_extend_through_input_length") != 34:
        errors.append("finite certificate endpoint mismatch")

    registered_summary = manifest.get("portfolio_summary_sha256")
    summary_input = dict(manifest)
    summary_input.pop("portfolio_summary_sha256", None)
    if registered_summary != canonical_hash(summary_input):
        errors.append("portfolio summary hash mismatch")
    return errors


def validate() -> list[str]:
    """Load and validate the registered repository artifact."""
    if not MANIFEST.is_file():
        return [f"missing manifest: {MANIFEST}"]
    try:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"invalid manifest JSON: {exc}"]
    if not isinstance(manifest, dict):
        return ["manifest root must be an object"]
    return validate_manifest(manifest)


def main() -> int:
    """Run the independent portfolio validation."""
    errors = validate()
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    print(
        "M82 portfolio validation passed: "
        f"{manifest['ledger_claim_count']} ledger claims, "
        f"{manifest['focused_claim_count']} focused claims, "
        f"{manifest['archive_only_claim_count']} archive-only claims"
    )
    print(f"summary SHA-256: {manifest['portfolio_summary_sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
