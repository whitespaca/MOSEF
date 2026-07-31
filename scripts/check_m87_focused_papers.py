"""Check M87 abstract length, opening cost boxes, and bilingual claim parity."""

from __future__ import annotations

import re
from pathlib import Path
from typing import NamedTuple

ROOT = Path(__file__).resolve().parents[1]
FOCUSED = ROOT / "paper" / "focused"

ABSTRACT_MIN_WORDS = 200
ABSTRACT_MAX_WORDS = 300

PAPER_IDS = (
    "promise-factorization",
    "cyclotomic-extraction",
    "finite-certificates",
)

EXPECTED_CLAIMS = {
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

EXPECTED_COST_LABELS = {
    ("promise-factorization", "en"): (
        "Online charged",
        "Not supplied",
        "Offline proof",
        "Guarantee",
    ),
    ("promise-factorization", "ko"): (
        "온라인 과금",
        "주어지지 않음",
        "오프라인 증명",
        "보장 범위",
    ),
    ("cyclotomic-extraction", "en"): (
        "Online charged",
        "Offline proof",
        "Output rule",
        "Guarantee",
    ),
    ("cyclotomic-extraction", "ko"): (
        "온라인 과금",
        "오프라인 증명",
        "출력 규칙",
        "보장 범위",
    ),
    ("finite-certificates", "en"): (
        "Online charged",
        "Offline proof",
        "Not supplied",
        "Guarantee",
    ),
    ("finite-certificates", "ko"): (
        "온라인 과금",
        "오프라인 증명",
        "주어지지 않음",
        "보장 범위",
    ),
}

EXPECTED_COST_TITLES = {
    "en": "Cost model at a glance",
    "ko": "비용 모델 요약",
}

CLAIM_PATTERN = re.compile(
    r"\\claimstatus\{([A-Z]+-\d{3})\}\{([A-Z]+)\}"
)
LEXICAL_TOKEN_PATTERN = re.compile(
    r"[^\W_]+(?:[-'][^\W_]+)*",
    re.UNICODE,
)


class PaperReport(NamedTuple):
    """One focused-paper editorial validation result."""

    paper_id: str
    language: str
    abstract_words: int
    cost_rows: int
    claim_count: int


def strip_latex_comments(text: str) -> str:
    """Remove unescaped LaTeX comments."""
    return re.sub(r"(?m)(?<!\\)%.*$", " ", text)


def extract_environment(text: str, name: str) -> tuple[str, int, int]:
    """Extract one uniquely occurring environment body and its source span."""
    begin = f"\\begin{{{name}}}"
    end = f"\\end{{{name}}}"
    if text.count(begin) != 1 or text.count(end) != 1:
        raise AssertionError(f"expected exactly one {name} environment")
    begin_index = text.index(begin)
    body_start = begin_index + len(begin)
    end_index = text.index(end, body_start)
    return text[body_start:end_index], begin_index, end_index + len(end)


def abstract_tokens(abstract: str) -> tuple[str, ...]:
    """Count prose tokens while treating each displayed formula as one word."""
    text = strip_latex_comments(abstract)
    text = re.sub(
        r"\\\((?:.|\n)*?\\\)|\\\[(?:.|\n)*?\\\]|\$(?:.|\n)*?\$",
        " MATH ",
        text,
    )
    for _iteration in range(4):
        text = re.sub(
            r"\\(?:texttt|textbf|emph)\{([^{}]*)\}",
            r"\1",
            text,
        )
    text = re.sub(r"\\[A-Za-z@]+\*?(?:\[[^\]]*\])?", " ", text)
    text = text.replace("{", " ").replace("}", " ").replace("\\", " ")
    return tuple(LEXICAL_TOKEN_PATTERN.findall(text))


def parse_braced_argument(text: str, start: int) -> tuple[str, int]:
    """Parse one possibly nested braced argument."""
    cursor = start
    while cursor < len(text) and text[cursor].isspace():
        cursor += 1
    if cursor >= len(text) or text[cursor] != "{":
        raise AssertionError("expected a braced cost-model argument")
    depth = 1
    cursor += 1
    content_start = cursor
    while cursor < len(text):
        character = text[cursor]
        if character == "{" and (cursor == 0 or text[cursor - 1] != "\\"):
            depth += 1
        elif character == "}" and (cursor == 0 or text[cursor - 1] != "\\"):
            depth -= 1
            if depth == 0:
                return text[content_start:cursor], cursor + 1
        cursor += 1
    raise AssertionError("unterminated cost-model argument")


def parse_cost_model(text: str) -> tuple[str, tuple[tuple[str, str], ...], int]:
    """Parse the one opening cost-model table."""
    _body, begin_index, end_index = extract_environment(text, "costmodel")
    marker = "\\begin{costmodel}"
    title, title_end = parse_braced_argument(text, begin_index + len(marker))
    closing = text.index("\\end{costmodel}", title_end)
    body = text[title_end:closing]

    rows: list[tuple[str, str]] = []
    cursor = 0
    while True:
        row_index = body.find("\\costrow", cursor)
        if row_index < 0:
            break
        label, after_label = parse_braced_argument(
            body,
            row_index + len("\\costrow"),
        )
        value, cursor = parse_braced_argument(body, after_label)
        rows.append((label.strip(), value.strip()))
    return title.strip(), tuple(rows), end_index


def validate_paper_text(
    paper_id: str,
    language: str,
    text: str,
) -> PaperReport:
    """Validate one focused paper without reading another artifact."""
    if paper_id not in PAPER_IDS:
        raise AssertionError(f"unknown focused paper: {paper_id}")
    if language not in {"en", "ko"}:
        raise AssertionError(f"unsupported focused-paper language: {language}")

    abstract, _abstract_start, abstract_end = extract_environment(
        text,
        "abstract",
    )
    word_count = len(abstract_tokens(abstract))
    if not ABSTRACT_MIN_WORDS <= word_count <= ABSTRACT_MAX_WORDS:
        raise AssertionError(
            f"{paper_id}-{language} abstract has {word_count} words; "
            f"expected {ABSTRACT_MIN_WORDS}--{ABSTRACT_MAX_WORDS}"
        )

    title, rows, cost_end = parse_cost_model(text)
    if title != EXPECTED_COST_TITLES[language]:
        raise AssertionError(f"{paper_id}-{language} cost-model title changed")
    labels = tuple(label for label, _value in rows)
    if labels != EXPECTED_COST_LABELS[(paper_id, language)]:
        raise AssertionError(f"{paper_id}-{language} cost-model rows changed")
    if any(not abstract_tokens(value) for _label, value in rows):
        raise AssertionError(f"{paper_id}-{language} has an empty cost row")

    first_section = text.find("\\section{")
    if first_section < 0:
        raise AssertionError(f"{paper_id}-{language} has no section")
    if not abstract_end < text.index("\\begin{costmodel}") < cost_end < first_section:
        raise AssertionError(
            f"{paper_id}-{language} cost model is not between abstract "
            "and first section"
        )

    claims = tuple(CLAIM_PATTERN.findall(text))
    expected_claims = EXPECTED_CLAIMS[paper_id]
    if tuple(claim_id for claim_id, _status in claims) != expected_claims:
        raise AssertionError(f"{paper_id}-{language} front-facing claims drifted")
    if any(status != "PROVED" for _claim_id, status in claims):
        raise AssertionError(f"{paper_id}-{language} claim status drifted")

    return PaperReport(
        paper_id=paper_id,
        language=language,
        abstract_words=word_count,
        cost_rows=len(rows),
        claim_count=len(claims),
    )


def validate_pair(
    paper_id: str,
    english: str,
    korean: str,
) -> tuple[PaperReport, PaperReport]:
    """Validate one bilingual pair and its exact claim/status parity."""
    english_report = validate_paper_text(paper_id, "en", english)
    korean_report = validate_paper_text(paper_id, "ko", korean)
    english_claims = CLAIM_PATTERN.findall(english)
    korean_claims = CLAIM_PATTERN.findall(korean)
    if english_claims != korean_claims:
        raise AssertionError(f"{paper_id} bilingual claim/status parity changed")
    return english_report, korean_report


def validate_all() -> tuple[PaperReport, ...]:
    """Validate the three bilingual focused-paper pairs."""
    reports: list[PaperReport] = []
    for paper_id in PAPER_IDS:
        english = (FOCUSED / f"{paper_id}-en.tex").read_text(encoding="utf-8")
        korean = (FOCUSED / f"{paper_id}-ko.tex").read_text(encoding="utf-8")
        reports.extend(validate_pair(paper_id, english, korean))
    return tuple(reports)


def main() -> int:
    """Run the complete M87 editorial gate."""
    reports = validate_all()
    counts = ", ".join(
        f"{report.paper_id}-{report.language}={report.abstract_words}"
        for report in reports
    )
    print(
        "M87 focused-paper editorial checker: PASS "
        f"({len(reports)} papers, 24 cost rows, "
        f"{sum(report.claim_count for report in reports) // 2} "
        "bilingual claim IDs; "
        f"abstract words: {counts})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
