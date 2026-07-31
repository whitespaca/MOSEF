"""Generate the deterministic M82 focused-paper claim projection."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CLAIMS = ROOT / "research" / "CLAIMS.md"
ARCHIVE_EN = ROOT / "paper" / "main.tex"
ARCHIVE_KO = ROOT / "paper" / "main-ko.tex"
PREAMBLE_EN = ROOT / "paper" / "focused" / "preamble-en.tex"
PREAMBLE_KO = ROOT / "paper" / "focused" / "preamble-ko.tex"
OUTPUT = ROOT / "schemas" / "m82-paper-portfolio-v1.json"

CLAIM_ROW = re.compile(r"^\| ([A-Z]+-\d+) \| ([A-Z]+) \|", re.MULTILINE)
PAPER_CLAIM = re.compile(r"\\claimstatus\{([A-Z]+-\d+)\}\{([A-Z]+)\}")

PAPERS: tuple[dict[str, Any], ...] = (
    {
        "id": "promise-factorization",
        "title_en": "Las Vegas Complete Factorization under Unrecognized Hereditary Order Promises",
        "title_ko": "인식되지 않는 유전적 차수 약속 아래의 Las Vegas 완전 인수분해",
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
        "title_en": "Cyclotomic Exceptional Extraction in Signed Geometric-Sum Circuits",
        "title_ko": "부호 있는 기하급수 회로의 예외적 Cyclotomic 추출",
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
        "title_en": "Computer-Assisted Selector Certificates for Finite Balanced Semiprime Populations",
        "title_ko": "유한 Balanced Semiprime 모집단을 위한 Computer-Assisted Selector 인증서",
        "english": "paper/focused/finite-certificates-en.tex",
        "korean": "paper/focused/finite-certificates-ko.tex",
        "representative_claims": [
            "BAR-024",
            "THM-021",
            "THM-022",
            "THM-023",
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


def sha256_bytes(data: bytes) -> str:
    """Return a lowercase SHA-256 digest."""
    return hashlib.sha256(data).hexdigest()


def sha256_text_file(path: Path) -> str:
    """Hash UTF-8 text after universal-newline normalization."""
    return sha256_bytes(path.read_text(encoding="utf-8").encode("utf-8"))


def canonical_hash(value: Any) -> str:
    """Hash canonical compact JSON."""
    data = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return sha256_bytes(data)


def read_claim_ledger() -> dict[str, str]:
    """Parse all claim IDs and statuses from the authoritative ledger."""
    text = CLAIMS.read_text(encoding="utf-8")
    claims: dict[str, str] = {}
    for claim_id, status in CLAIM_ROW.findall(text):
        if claim_id in claims:
            raise ValueError(f"duplicate ledger claim: {claim_id}")
        claims[claim_id] = status
    if not claims:
        raise ValueError("empty claim ledger")
    return claims


def read_paper_claims(path: Path) -> list[tuple[str, str]]:
    """Parse the ordered claim projection from one focused paper."""
    return PAPER_CLAIM.findall(path.read_text(encoding="utf-8"))


def build_portfolio() -> dict[str, Any]:
    """Build the complete deterministic projection artifact."""
    ledger = read_claim_ledger()
    projected: set[str] = set()
    paper_rows: list[dict[str, Any]] = []
    source_paths = [CLAIMS, ARCHIVE_EN, ARCHIVE_KO, PREAMBLE_EN, PREAMBLE_KO]

    for specification in PAPERS:
        row = dict(specification)
        expected = specification["representative_claims"]
        expected_pairs = [(claim_id, ledger[claim_id]) for claim_id in expected]
        english_path = ROOT / specification["english"]
        korean_path = ROOT / specification["korean"]
        english_pairs = read_paper_claims(english_path)
        korean_pairs = read_paper_claims(korean_path)
        if english_pairs != expected_pairs:
            raise ValueError(
                f"{specification['english']} claim projection differs from specification"
            )
        if korean_pairs != expected_pairs:
            raise ValueError(
                f"{specification['korean']} claim projection differs from specification"
            )
        if projected.intersection(expected):
            raise ValueError(f"cross-paper duplicate claim in {specification['id']}")
        projected.update(expected)
        row["claim_statuses"] = [
            {"claim_id": claim_id, "status": ledger[claim_id]}
            for claim_id in expected
        ]
        paper_rows.append(row)
        source_paths.extend((english_path, korean_path))

    archive_only = [
        {"claim_id": claim_id, "status": status}
        for claim_id, status in ledger.items()
        if claim_id not in projected
    ]
    source_hashes = {
        path.relative_to(ROOT).as_posix(): sha256_text_file(path)
        for path in source_paths
    }
    artifact: dict[str, Any] = {
        "schema_version": "1.0.0",
        "milestone": "M82",
        "generated_date": "2026-07-31",
        "archive": {
            "english": ARCHIVE_EN.relative_to(ROOT).as_posix(),
            "korean": ARCHIVE_KO.relative_to(ROOT).as_posix(),
            "claim_ledger": CLAIMS.relative_to(ROOT).as_posix(),
        },
        "papers": paper_rows,
        "ledger_claim_count": len(ledger),
        "focused_claim_count": len(projected),
        "archive_only_claim_count": len(archive_only),
        "archive_only_claims": archive_only,
        "claim_status_sha256": canonical_hash(list(ledger.items())),
        "source_sha256": source_hashes,
        "scope": {
            "general_classical_polynomial_time_factoring": "OPEN",
            "focused_papers_are_claim_projections": True,
            "archival_monograph_retained": True,
            "finite_certificates_extend_through_input_length": 34,
        },
    }
    artifact["portfolio_summary_sha256"] = canonical_hash(artifact)
    return artifact


def main() -> int:
    """Write or check the registered portfolio artifact."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    rendered = json.dumps(build_portfolio(), ensure_ascii=False, indent=2) + "\n"
    if args.check:
        if not OUTPUT.exists():
            raise SystemExit(f"missing generated artifact: {OUTPUT}")
        if OUTPUT.read_text(encoding="utf-8") != rendered:
            raise SystemExit("M82 portfolio artifact is stale")
        print("M82 portfolio artifact is current")
        return 0
    OUTPUT.write_text(rendered, encoding="utf-8", newline="\n")
    print(f"wrote {OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
