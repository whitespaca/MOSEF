"""Independently validate the M83 source audit and bilingual positioning."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "schemas" / "m83-related-work-audit-v1.json"
MATRIX_EN = ROOT / "research" / "publication" / "M83-related-work-matrix-en.md"
MATRIX_KO = ROOT / "research" / "publication" / "M83-related-work-matrix-ko.md"
REFERENCES = ROOT / "paper" / "references.bib"
MARKER = re.compile(
    r"<!-- (M83-R\d{2})\|([A-Z_]+)\|([A-Z]+-\d+(?:,[A-Z]+-\d+)*)"
    r"\|(SRC-\d+(?:,SRC-\d+)*)\|(NO_PRIORITY_CLAIM) -->"
)

EXPECTED_SOURCES: tuple[tuple[str, str, str, str], ...] = (
    (
        "SRC-008",
        "pollard1974theorems",
        "FULL_ARTICLE",
        "research/literature/SRC-008-pollard-factorization-primality.md",
    ),
    (
        "SRC-005",
        "williams1982pplusone",
        "FULL_ARTICLE",
        "research/literature/SRC-005-williams-p-plus-one.md",
    ),
    (
        "SRC-009",
        "katona1966separating",
        "PARTIAL_FULL_TEXT",
        "research/literature/SRC-009-katona-separating-systems.md",
    ),
    (
        "SRC-010",
        "conway1976trigonometric",
        "FULL_ARTICLE",
        "research/literature/SRC-010-conway-jones-roots-unity.md",
    ),
    (
        "SRC-011",
        "bernstein2004smoothparts",
        "FULL_ARTICLE",
        "research/literature/SRC-011-bernstein-smooth-parts.md",
    ),
    (
        "SRC-012",
        "yao1976evaluation",
        "ABSTRACT_ONLY",
        "research/literature/SRC-012-yao-evaluation-powers.md",
    ),
)

EXPECTED_ROWS: tuple[tuple[str, str, tuple[str, ...], tuple[str, ...]], ...] = (
    ("M83-R01", "SCOPED_SYNTHESIS", ("THM-001",), ("SRC-008",)),
    ("M83-R02", "SCOPED_SYNTHESIS", ("LEM-003", "THM-002"), ("SRC-005",)),
    ("M83-R03", "SCOPED_SYNTHESIS", ("BAR-001", "BAR-024"), ("SRC-009",)),
    ("M83-R04", "SCOPED_SYNTHESIS", ("BAR-018", "BAR-019"), ("SRC-012",)),
    ("M83-R05", "SCOPED_SYNTHESIS", ("THM-003", "BAR-020"), ("SRC-010",)),
    (
        "M83-R06",
        "SCOPED_SYNTHESIS",
        ("THM-004", "THM-005", "THM-014", "THM-019"),
        ("SRC-009", "SRC-011"),
    ),
    (
        "M83-R07",
        "SCOPED_SYNTHESIS",
        ("BAR-041", "BAR-042", "BAR-043", "BAR-044", "BAR-045", "BAR-046"),
        ("SRC-009", "SRC-011"),
    ),
)

REQUIRED_PAPER_ROWS: dict[str, tuple[str, ...]] = {
    "paper/main.tex": tuple(row[0] for row in EXPECTED_ROWS),
    "paper/main-ko.tex": tuple(row[0] for row in EXPECTED_ROWS),
    "paper/focused/promise-factorization-en.tex": ("M83-R01", "M83-R02", "M83-R03"),
    "paper/focused/promise-factorization-ko.tex": ("M83-R01", "M83-R02", "M83-R03"),
    "paper/focused/cyclotomic-extraction-en.tex": ("M83-R04", "M83-R05"),
    "paper/focused/cyclotomic-extraction-ko.tex": ("M83-R04", "M83-R05"),
    "paper/focused/finite-certificates-en.tex": ("M83-R03", "M83-R06", "M83-R07"),
    "paper/focused/finite-certificates-ko.tex": ("M83-R03", "M83-R06", "M83-R07"),
}

REQUIRED_CITATIONS: dict[str, tuple[str, ...]] = {
    "paper/main.tex": tuple(source[1] for source in EXPECTED_SOURCES),
    "paper/main-ko.tex": tuple(source[1] for source in EXPECTED_SOURCES),
    "paper/focused/promise-factorization-en.tex": (
        "pollard1974theorems",
        "williams1982pplusone",
        "katona1966separating",
    ),
    "paper/focused/promise-factorization-ko.tex": (
        "pollard1974theorems",
        "williams1982pplusone",
        "katona1966separating",
    ),
    "paper/focused/cyclotomic-extraction-en.tex": (
        "yao1976evaluation",
        "conway1976trigonometric",
    ),
    "paper/focused/cyclotomic-extraction-ko.tex": (
        "yao1976evaluation",
        "conway1976trigonometric",
    ),
    "paper/focused/finite-certificates-en.tex": (
        "katona1966separating",
        "bernstein2004smoothparts",
    ),
    "paper/focused/finite-certificates-ko.tex": (
        "katona1966separating",
        "bernstein2004smoothparts",
    ),
}

EXPECTED_HASH_PATHS = {
    *(source[3] for source in EXPECTED_SOURCES),
    "research/literature/M83-primary-source-search.md",
    "research/reviews/2026-07-31-m83-source-scope-review.md",
    "paper/references.bib",
    *REQUIRED_PAPER_ROWS,
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


def parse_markers(text: str) -> list[tuple[str, str, tuple[str, ...], tuple[str, ...]]]:
    """Parse language-independent matrix synchronization markers."""
    return [
        (row_id, classification, tuple(claims.split(",")), tuple(sources.split(",")))
        for row_id, classification, claims, sources, _priority in MARKER.findall(text)
    ]


def expected_marker_rows() -> list[tuple[str, str, tuple[str, ...], tuple[str, ...]]]:
    """Return the independently registered marker sequence."""
    return [tuple(row) for row in EXPECTED_ROWS]  # type: ignore[misc]


def validate_matrix_pair(english: str, korean: str) -> list[str]:
    """Check exact bilingual row synchronization and scope language."""
    errors: list[str] = []
    expected = expected_marker_rows()
    if parse_markers(english) != expected:
        errors.append("English matrix marker sequence mismatch")
    if parse_markers(korean) != expected:
        errors.append("Korean matrix marker sequence mismatch")
    if "not evidence of novelty or priority" not in english:
        errors.append("English negative-search limitation missing")
    if "독창성이나 우선권의 증거가 아니다" not in korean:
        errors.append("Korean negative-search limitation missing")
    if "General classical polynomial-time factoring remains open" not in english:
        errors.append("English general-factoring scope missing")
    if "일반 고전적 다항시간 인수분해는 열린 문제" not in korean:
        errors.append("Korean general-factoring scope missing")
    return errors


def validate_source_record(
    source_id: str, inspection_level: str, text: str
) -> list[str]:
    """Validate one source record's explicit inspection and claim boundary."""
    errors: list[str] = []
    if not text.startswith(f"# {source_id} -"):
        errors.append(f"{source_id} heading mismatch")
    if f"Inspection level: `{inspection_level}`" not in text:
        errors.append(f"{source_id} inspection level mismatch")
    lowered = text.lower()
    if "no novelty" not in lowered and "not evidence of novelty" not in lowered:
        errors.append(f"{source_id} novelty limitation missing")
    if source_id == "SRC-012":
        if "abstract-only" not in lowered and "abstract only" not in lowered:
            errors.append("SRC-012 abstract-only limitation missing")
        if "not used" not in lowered:
            errors.append("SRC-012 technical non-use marker missing")
    return errors


def validate_paper(
    path: str, text: str, required_rows: tuple[str, ...], citations: tuple[str, ...]
) -> list[str]:
    """Validate row markers, citations, and conservative wording in one paper."""
    errors: list[str] = []
    observed = tuple(re.findall(r"\bM83-R\d{2}\b", text))
    filtered = tuple(row for row in observed if row in required_rows)
    if filtered != required_rows:
        errors.append(f"{path} related-work row order mismatch")
    for key in citations:
        if f"\\cite{{{key}}}" not in text:
            errors.append(f"{path} citation missing: {key}")
    prohibited = (
        "we are the first",
        "first proof of",
        "최초로 증명한다",
        "최초의 증명",
    )
    for phrase in prohibited:
        if phrase.lower() in text.lower():
            errors.append(f"{path} unsupported priority phrase: {phrase}")
    return errors


def validate_manifest(manifest: dict[str, Any]) -> list[str]:
    """Validate immutable structure, source hashes, and scope fields."""
    errors: list[str] = []
    if manifest.get("schema_version") != "1.0.0":
        errors.append("unexpected schema version")
    if manifest.get("milestone") != "M83":
        errors.append("unexpected milestone")
    if manifest.get("audit_scope") != "BOUNDED_PRIMARY_SOURCE_AUDIT":
        errors.append("unexpected audit scope")

    expected_sources = [
        {
            "source_id": source_id,
            "citation_key": citation_key,
            "inspection_level": inspection_level,
            "record": record,
        }
        for source_id, citation_key, inspection_level, record in EXPECTED_SOURCES
    ]
    if manifest.get("sources") != expected_sources:
        errors.append("source registry mismatch")

    rows = manifest.get("rows")
    if not isinstance(rows, list) or len(rows) != len(EXPECTED_ROWS):
        errors.append("related-work row count mismatch")
    else:
        for row, expected in zip(rows, EXPECTED_ROWS, strict=True):
            row_id, classification, claim_ids, source_ids = expected
            if row.get("row_id") != row_id:
                errors.append(f"row ID mismatch at {row_id}")
            if row.get("classification") != classification:
                errors.append(f"{row_id} classification mismatch")
            if row.get("claim_ids") != list(claim_ids):
                errors.append(f"{row_id} claim list mismatch")
            if row.get("source_ids") != list(source_ids):
                errors.append(f"{row_id} source list mismatch")
            if row.get("priority_status") != "NO_PRIORITY_CLAIM":
                errors.append(f"{row_id} unsupported priority status")

    counts = manifest.get("classification_counts")
    if counts != {
        "established_background_components": 7,
        "scoped_synthesis_rows": 7,
        "positively_labeled_plausibly_new_rows": 0,
    }:
        errors.append("classification counts mismatch")
    if manifest.get("negative_search_rule") != (
        "failure to locate an exact match is not evidence of novelty or priority"
    ):
        errors.append("negative-search rule mismatch")
    scope = manifest.get("scope")
    if scope != {
        "general_classical_polynomial_time_factoring": "OPEN",
        "novelty_claims_made": False,
        "priority_claims_made": False,
        "finite_certificate_max_input_length": 34,
    }:
        errors.append("scope registry mismatch")

    source_hashes = manifest.get("source_sha256")
    if not isinstance(source_hashes, dict):
        errors.append("source hash map missing")
    elif set(source_hashes) != EXPECTED_HASH_PATHS:
        errors.append("source hash path set mismatch")
    else:
        for path, recorded in source_hashes.items():
            source = ROOT / path
            if not source.is_file() or recorded != sha256_text_file(source):
                errors.append(f"source hash mismatch: {path}")

    recorded_summary = manifest.get("audit_summary_sha256")
    summary_input = dict(manifest)
    summary_input.pop("audit_summary_sha256", None)
    if recorded_summary != canonical_hash(summary_input):
        errors.append("audit summary hash mismatch")
    return errors


def validate() -> list[str]:
    """Run the complete independent M83 validation."""
    if not MANIFEST.is_file():
        return ["M83 manifest missing"]
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    errors = validate_manifest(manifest)

    if not MATRIX_EN.is_file() or not MATRIX_KO.is_file():
        errors.append("bilingual related-work matrix missing")
    else:
        errors.extend(
            validate_matrix_pair(
                MATRIX_EN.read_text(encoding="utf-8"),
                MATRIX_KO.read_text(encoding="utf-8"),
            )
        )

    bibliography = REFERENCES.read_text(encoding="utf-8")
    for _source_id, citation_key, _level, _record in EXPECTED_SOURCES:
        if not re.search(rf"@\w+\{{{re.escape(citation_key)},", bibliography):
            errors.append(f"bibliography key missing: {citation_key}")

    for source_id, _key, inspection_level, record in EXPECTED_SOURCES:
        source_path = ROOT / record
        if not source_path.is_file():
            errors.append(f"source record missing: {source_id}")
            continue
        errors.extend(
            validate_source_record(
                source_id,
                inspection_level,
                source_path.read_text(encoding="utf-8"),
            )
        )

    search_path = ROOT / "research" / "literature" / "M83-primary-source-search.md"
    if not search_path.is_file():
        errors.append("primary-source search record missing")
    else:
        search = search_path.read_text(encoding="utf-8")
        if "not evidence that a project result is novel" not in search:
            errors.append("search record novelty limitation missing")

    review_path = (
        ROOT / "research" / "reviews" / "2026-07-31-m83-source-scope-review.md"
    )
    if not review_path.is_file():
        errors.append("adversarial source-scope review missing")
    else:
        review = review_path.read_text(encoding="utf-8")
        if "PASS for M83's bounded acceptance criterion" not in review:
            errors.append("adversarial source-scope review outcome missing")
        if "not represented as an independent external priority survey" not in review:
            errors.append("adversarial review independence limitation missing")

    for path, rows in REQUIRED_PAPER_ROWS.items():
        paper = ROOT / path
        if not paper.is_file():
            errors.append(f"paper missing: {path}")
            continue
        errors.extend(
            validate_paper(path, paper.read_text(encoding="utf-8"), rows, REQUIRED_CITATIONS[path])
        )
    return errors


def main() -> int:
    """Report validation errors with a nonzero exit code."""
    errors = validate()
    if errors:
        for error in errors:
            print(f"M83 related-work check: FAIL: {error}", file=sys.stderr)
        return 1
    print(
        "M83 related-work check: PASS "
        "(6 inspected sources, 7 synchronized rows, no priority claims)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
