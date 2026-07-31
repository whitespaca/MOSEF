"""Check M88 reader-facing labels and stable focused-paper claim metadata."""

from __future__ import annotations

import re
from pathlib import Path
from typing import NamedTuple

ROOT = Path(__file__).resolve().parents[1]
FOCUSED = ROOT / "paper" / "focused"

PAPER_CLAIMS = {
    "promise-factorization": (
        "THM-001",
        "BAR-001",
        "BAR-002",
        "LEM-003",
        "THM-002",
        "BAR-003",
        "BAR-004",
    ),
    "cyclotomic-extraction": (
        "BAR-018",
        "BAR-019",
        "THM-003",
        "BAR-020",
        "BAR-021",
        "BAR-022",
        "BAR-023",
    ),
    "finite-certificates": (
        "BAR-024",
        "THM-021",
        "THM-022",
        "THM-023",
        "THM-024",
        "THM-025",
        "THM-004",
        "THM-005",
        "THM-014",
        "THM-019",
        "BAR-041",
        "BAR-046",
    ),
}

READER_LABELS = {
    "THM-001": {
        "en": ("Theorem", r"Hereditary \(p-1\) complete factorization"),
        "ko": ("정리", r"유전적 \(p-1\) 완전 인수분해"),
    },
    "BAR-001": {
        "en": (
            "Counterexample and criterion",
            "Coverage is not separation",
        ),
        "ko": ("반례와 판정", "약수 포함은 차수 분리가 아니다"),
    },
    "THM-021": {
        "en": ("Theorem", "Private-pair repair certificate"),
        "ko": ("정리", "Private-pair repair 인증서"),
    },
    "THM-022": {
        "en": ("Theorem", "Subset-obstruction repair certificate"),
        "ko": ("정리", "Subset-obstruction repair 인증서"),
    },
    "THM-023": {
        "en": ("Theorem", "Complete-graph repair certificate"),
        "ko": ("정리", "Complete-graph repair 인증서"),
    },
    "THM-024": {
        "en": ("Theorem", "Looped graph repair certificate"),
        "ko": ("정리", "Looped graph repair 인증서"),
    },
    "THM-025": {
        "en": ("Theorem", "Matching-equality repair certificate"),
        "ko": ("정리", "Matching-equality repair 인증서"),
    },
    "BAR-002": {
        "en": (
            "Proposition",
            "Conjugate channels have identical support",
        ),
        "ko": ("명제", "켤레 채널의 support는 동일하다"),
    },
    "LEM-003": {
        "en": ("Proposition", "Exact Lucas root count"),
        "ko": ("명제", "정확한 Lucas root 개수"),
    },
    "THM-002": {
        "en": (
            "Theorem",
            r"Hereditary nonsplit \(p+1\) complete factorization",
        ),
        "ko": ("정리", r"유전적 비분할 \(p+1\) 완전 인수분해"),
    },
    "BAR-003": {
        "en": ("Barrier", "Common-schedule density ceiling"),
        "ko": ("장벽", "공통 schedule의 분포 상한"),
    },
    "BAR-004": {
        "en": (
            "Barrier",
            "Subcritical exponent-list sparsity",
        ),
        "ko": ("장벽", "임계 미만 지수 목록의 희소성"),
    },
    "BAR-018": {
        "en": (
            "Proposition",
            "Stage coprimality and exact resultant",
        ),
        "ko": ("명제", "stage 서로소성과 정확한 resultant"),
    },
    "BAR-019": {
        "en": (
            "Proposition",
            "Total content and resultant reduction",
        ),
        "ko": ("명제", "total content 및 resultant 축약"),
    },
    "THM-003": {
        "en": (
            "Theorem",
            "Rational root-of-unity ratios",
        ),
        "ko": ("정리", "유리 root-of-unity 비율"),
    },
    "BAR-020": {
        "en": (
            "Proposition",
            "Division-free exceptional cofactors",
        ),
        "ko": ("명제", "나눗셈 없는 예외 cofactor"),
    },
    "BAR-021": {
        "en": (
            "Proposition",
            "Branch-total cofactor extraction",
        ),
        "ko": ("명제", "branch-total cofactor 추출"),
    },
    "BAR-022": {
        "en": (
            "Barrier",
            "Exponentially costly exact lifts",
        ),
        "ko": ("장벽", "지수적으로 비싼 exact lift"),
    },
    "BAR-023": {
        "en": ("Barrier", "One-bit cofactor support"),
        "ko": ("장벽", "cofactor support 한 비트"),
    },
    "BAR-024": {
        "en": ("Proposition", "Signature separation"),
        "ko": ("명제", "signature 분리"),
    },
    "THM-004": {
        "en": (
            "Finite certificate",
            "Base cap through length 15",
        ),
        "ko": ("유한 인증서", "길이 15까지의 base cap"),
    },
    "THM-005": {
        "en": (
            "Finite certificate",
            "Offset 11 through length 20",
        ),
        "ko": ("유한 인증서", "길이 20까지의 offset 11"),
    },
    "THM-014": {
        "en": ("Finite certificate", "Length-29 nonmonotonicity"),
        "ko": ("유한 인증서", "길이 29 비단조성"),
    },
    "THM-019": {
        "en": ("Finite certificate", "Length-34 endpoint"),
        "ko": ("유한 인증서", "길이 34 endpoint"),
    },
    "BAR-041": {
        "en": ("Barrier", "Polynomial numeric-cap failure"),
        "ko": ("장벽", "다항 numeric-cap 실패"),
    },
    "BAR-046": {
        "en": (
            "Barrier",
            r"Compact-gap failure below \(1/2\)",
        ),
        "ko": (
            "장벽",
            r"\(1/2\) 미만 compact-gap 실패",
        ),
    },
}

READER_PATTERN = re.compile(
    r"\\readerclaim\{([^{}\n]+)\}\{([^{}\n]+)\}\s*"
    r"\{\\claimstatus\{([A-Z]+-\d{3})\}\{([A-Z]+)\}\}"
)
CLAIM_PATTERN = re.compile(
    r"\\claimstatus\{([A-Z]+-\d{3})\}\{([A-Z]+)\}"
)


class ReaderRecord(NamedTuple):
    """One parsed reader-facing claim header."""

    kind: str
    title: str
    claim_id: str
    status: str


class PaperReport(NamedTuple):
    """One focused-paper label validation result."""

    paper_id: str
    language: str
    claim_ids: tuple[str, ...]
    kinds: tuple[str, ...]


def parse_records(text: str) -> tuple[ReaderRecord, ...]:
    """Parse all reader labels with their embedded stable metadata."""
    return tuple(ReaderRecord(*match) for match in READER_PATTERN.findall(text))


def validate_preamble(language: str, text: str) -> None:
    """Require one reusable three-argument reader-label macro."""
    if language not in {"en", "ko"}:
        raise AssertionError(f"unsupported language: {language}")
    marker = r"\newcommand{\readerclaim}[3]"
    if text.count(marker) != 1:
        raise AssertionError(f"{language} readerclaim macro count changed")
    if r"\newcommand{\claimstatus}[2]" not in text:
        raise AssertionError(f"{language} stable claimstatus macro missing")


def validate_paper_text(
    paper_id: str,
    language: str,
    text: str,
) -> PaperReport:
    """Validate one paper's reader labels, IDs, statuses, and order."""
    if paper_id not in PAPER_CLAIMS:
        raise AssertionError(f"unknown focused paper: {paper_id}")
    if language not in {"en", "ko"}:
        raise AssertionError(f"unsupported language: {language}")

    records = parse_records(text)
    raw_claims = tuple(CLAIM_PATTERN.findall(text))
    wrapped_claims = tuple(
        (record.claim_id, record.status) for record in records
    )
    if raw_claims != wrapped_claims:
        raise AssertionError(
            f"{paper_id}-{language} has an unwrapped or malformed claim"
        )

    expected_ids = PAPER_CLAIMS[paper_id]
    actual_ids = tuple(record.claim_id for record in records)
    if actual_ids != expected_ids:
        raise AssertionError(f"{paper_id}-{language} claim order drifted")

    for record in records:
        if record.status != "PROVED":
            raise AssertionError(
                f"{paper_id}-{language} status drifted for {record.claim_id}"
            )
        expected_kind, expected_title = READER_LABELS[record.claim_id][language]
        if (record.kind, record.title) != (expected_kind, expected_title):
            raise AssertionError(
                f"{paper_id}-{language} reader label drifted for "
                f"{record.claim_id}"
            )
        if record.claim_id in record.kind or record.claim_id in record.title:
            raise AssertionError(
                f"{paper_id}-{language} exposes an ID as a reader label"
            )

    return PaperReport(
        paper_id=paper_id,
        language=language,
        claim_ids=actual_ids,
        kinds=tuple(record.kind for record in records),
    )


def validate_pair(
    paper_id: str,
    english: str,
    korean: str,
) -> tuple[PaperReport, PaperReport]:
    """Validate one bilingual paper pair and stable ID order."""
    english_report = validate_paper_text(paper_id, "en", english)
    korean_report = validate_paper_text(paper_id, "ko", korean)
    if english_report.claim_ids != korean_report.claim_ids:
        raise AssertionError(f"{paper_id} bilingual claim IDs drifted")
    return english_report, korean_report


def validate_all() -> tuple[PaperReport, ...]:
    """Validate both preambles and all three focused-paper pairs."""
    for language in ("en", "ko"):
        preamble = (FOCUSED / f"preamble-{language}.tex").read_text(
            encoding="utf-8"
        )
        validate_preamble(language, preamble)

    reports: list[PaperReport] = []
    for paper_id in PAPER_CLAIMS:
        english = (FOCUSED / f"{paper_id}-en.tex").read_text(encoding="utf-8")
        korean = (FOCUSED / f"{paper_id}-ko.tex").read_text(encoding="utf-8")
        reports.extend(validate_pair(paper_id, english, korean))
    return tuple(reports)


def main() -> int:
    """Run the complete M88 reader-label gate."""
    reports = validate_all()
    headings = sum(len(report.claim_ids) for report in reports)
    kinds = {kind for report in reports for kind in report.kinds}
    print(
        "M88 reader-label checker: PASS "
        f"({len(reports)} papers, {headings} rendered headings, "
        f"{headings // 2} bilingual claim IDs, "
        f"{len(kinds)} localized reader kinds)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
