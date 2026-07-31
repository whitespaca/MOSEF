"""Check M89 narrative/appendix boundaries in all focused manuscripts."""

from __future__ import annotations

import re
from pathlib import Path
from typing import NamedTuple

ROOT = Path(__file__).resolve().parents[1]
FOCUSED = ROOT / "paper" / "focused"

PAPER_CONFIG = {
    ("promise-factorization", "en"): {
        "main_sections": (
            r"\section{Scope and model}",
            r"\section{Fresh-base \texorpdfstring{\(p-1\)}{p-1} factorization}",
            r"\section{Coverage is not separation}",
            r"\section{The conjugate channel is correlated}",
            (
                r"\section{Independent nonsplit "
                r"\texorpdfstring{\(p+1\)}{p+1} factorization}"
            ),
            r"\section{Bounded total wrappers}",
            r"\section{A common-schedule limitation}",
        ),
        "appendix_sections": (
            r"\section{Primary-source positioning audit}",
            r"\section{Reproduction, limitations, and archival map}",
        ),
        "labels": (
            "app:promise-source-positioning",
            "app:promise-reproduction",
        ),
        "limitation": "no claim here solves general classical "
        "polynomial-time factorization",
    },
    ("promise-factorization", "ko"): {
        "main_sections": (
            r"\section{범위와 계산 모형}",
            (
                r"\section{새로운 밑을 이용한 "
                r"\texorpdfstring{\(p-1\)}{p-1} 인수분해}"
            ),
            r"\section{포함은 분리가 아니다}",
            r"\section{켤레 채널의 상관}",
            (
                r"\section{독립적인 비분할 "
                r"\texorpdfstring{\(p+1\)}{p+1} 인수분해}"
            ),
            r"\section{유한 예산 total wrapper}",
            r"\section{공통 schedule의 한계}",
        ),
        "appendix_sections": (
            r"\section{1차 문헌 포지셔닝 감사}",
            r"\section{재현성, 한계 및 아카이브 지도}",
        ),
        "labels": (
            "app:promise-source-positioning",
            "app:promise-reproduction",
        ),
        "limitation": "일반 고전적 다항시간 인수분해 문제는 열린 상태이다",
    },
    ("cyclotomic-extraction", "en"): {
        "main_sections": (
            r"\section{Charged circuit grammar}",
            r"\section{Primitive residues and public overlap}",
            r"\section{Complete rational root-orbit classification}",
            r"\section{Division-free exceptional cofactors}",
            r"\section{Overlap and schedule barriers}",
        ),
        "appendix_sections": (
            r"\section{Primary-source positioning audit}",
            r"\section{Reproduction, limitations, and archival map}",
        ),
        "labels": (
            "app:cyclotomic-source-positioning",
            "app:cyclotomic-reproduction",
        ),
        "limitation": "supplies no universal selector, prime-support density "
        "theorem, or general factoring algorithm",
    },
    ("cyclotomic-extraction", "ko"): {
        "main_sections": (
            r"\section{비용이 명시된 회로 문법}",
            r"\section{Primitive residue와 공개 overlap}",
            r"\section{유리 root-orbit의 완전 분류}",
            r"\section{나눗셈 없는 예외적 cofactor}",
            r"\section{Overlap 및 schedule 장벽}",
        ),
        "appendix_sections": (
            r"\section{1차 문헌 포지셔닝 감사}",
            r"\section{재현성, 한계 및 아카이브 지도}",
        ),
        "labels": (
            "app:cyclotomic-source-positioning",
            "app:cyclotomic-reproduction",
        ),
        "limitation": "universal selector, prime-support density 정리, "
        "일반 인수분해 알고리즘을 제공하지 않는다",
    },
    ("finite-certificates", "en"): {
        "main_sections": (
            r"\section{Population, selector, and trust boundary}",
            r"\section{Signature criterion}",
            r"\section{Initial and widened finite theorems}",
            r"\section{Exact finite threshold synthesis}",
            r"\section{Asymptotic barriers inside the same grammar}",
        ),
        "appendix_sections": (
            r"\section{Primary-source positioning audit}",
            r"\section{Certificate reproduction, limitations, and archival map}",
        ),
        "labels": (
            "app:finite-source-positioning",
            "app:finite-reproduction",
        ),
        "limitation": "General classical polynomial-time factoring remains open",
    },
    ("finite-certificates", "ko"): {
        "main_sections": (
            r"\section{모집단, selector, 신뢰 경계}",
            r"\section{Signature 판정}",
            r"\section{초기 및 확장 유한 정리}",
            r"\section{정확한 유한 threshold 종합}",
            r"\section{같은 문법 내부의 점근 장벽}",
        ),
        "appendix_sections": (
            r"\section{1차 문헌 포지셔닝 감사}",
            r"\section{인증서 재현, 한계 및 아카이브 지도}",
        ),
        "labels": (
            "app:finite-source-positioning",
            "app:finite-reproduction",
        ),
        "limitation": "일반 고전적 다항시간 인수분해는 열린 문제이다",
    },
}

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
        "THM-026",
        "THM-027",
        "THM-028",
        "THM-004",
        "THM-005",
        "THM-014",
        "THM-019",
        "BAR-041",
        "BAR-046",
    ),
}

EXPECTED_COMMANDS = {
    "promise-factorization": (
        "python scripts/run_m3_semismooth_search.py",
        "python scripts/check_m3_semismooth_differential.py",
        "python scripts/run_m7_nonsplit_search.py",
        "python scripts/check_m7_nonsplit_differential.py",
        "python scripts/check_m84_promise_wrappers.py",
        "python -m unittest discover -s tests -p test_promise_wrappers.py",
    ),
    "cyclotomic-extraction": (
        "python scripts/run_m24_rational_residue_audit.py",
        "python scripts/check_m24_rational_residue_audit_differential.py",
        "python scripts/run_m25_rational_root_orbit_audit.py",
        "python scripts/check_m25_rational_root_orbit_differential.py",
        "python scripts/run_m26_exceptional_cyclotomic_audit.py",
        "python scripts/check_m26_exceptional_cyclotomic_differential.py",
    ),
    "finite-certificates": (
        "python scripts/generate_m50_finite_threshold_summary.py --check",
        "python scripts/check_m50_finite_threshold_summary.py",
        "python scripts/check_m85_m41_semantic_certificate.py",
        "python scripts/check_m86_m46_streaming_certificate.py",
        "python scripts/check_m91_all_rows_semantic_certificate.py",
        "python scripts/check_m92_pair_cover_certificate.py",
        "python -m pytest -p no:cacheprovider tests/test_m92_pair_cover_certificate.py -q",
        "python scripts/check_m93_early_repair_certificate.py",
        "pytest -p no:cacheprovider tests/test_m93_early_repair_certificate.py -q",
        "python scripts/check_m94_clique_incidence_certificate.py",
        "pytest -p no:cacheprovider tests/test_m94_clique_incidence_certificate.py -q",
        "python scripts/check_m95_coverer_graph_certificate.py",
        "pytest -p no:cacheprovider tests/test_m95_coverer_graph_certificate.py -q",
        "python scripts/check_m96_matching_certificate.py",
        "pytest -p no:cacheprovider tests/test_m96_matching_certificate.py -q",
        "python scripts/check_m97_bipartite_cover.py",
        "pytest -p no:cacheprovider tests/test_m97_bipartite_cover.py -q",
        "python scripts/check_m98_oct_cover.py",
        "pytest -p no:cacheprovider tests/test_m98_oct_cover.py -q",
        "python scripts/check_m99_oct_discovery.py",
        "pytest -p no:cacheprovider tests/test_m99_oct_discovery.py -q",
    ),
}

EXPECTED_PATHS = {
    "promise-factorization": (
        "research/proofs/THM-001-semismooth-promise.md",
        "research/proofs/THM-002-nonsplit-lucas-promise.md",
        "research/proofs/M84-bounded-total-promise-wrappers.md",
        "python/mosef_reference/promise_wrappers.py",
        "research/experiments/EXP-0003-m3-semismooth-search.md",
        "research/experiments/EXP-0006-m7-nonsplit-lucas.md",
        "research/CLAIMS.md",
        "research/NEGATIVE_RESULTS.md",
        "schemas/m82-paper-portfolio-v1.json",
    ),
    "cyclotomic-extraction": (
        "research/proofs/THM-003-rational-root-orbits.md",
        "research/experiments",
        "research/CLAIMS.md",
        "schemas/m82-paper-portfolio-v1.json",
    ),
    "finite-certificates": (
        "schemas/m50-finite-threshold-summary-v1.json",
        "schemas",
        "scripts",
        "research/experiments",
        "research/CLAIMS.md",
        "schemas/m82-paper-portfolio-v1.json",
    ),
}

EXPECTED_CITATIONS = {
    "promise-factorization": (
        "pollard1974theorems",
        "williams1982pplusone",
        "katona1966separating",
    ),
    "cyclotomic-extraction": (
        "yao1976evaluation",
        "conway1976trigonometric",
    ),
    "finite-certificates": (
        "katona1966separating",
        "bernstein2004smoothparts",
        "lokshtanov2009oct",
    ),
}

EXPECTED_MILESTONES = {
    "promise-factorization": (
        "M83-R01",
        "M83-R02",
        "M83-R03",
        "M83",
        "M84",
    ),
    "cyclotomic-extraction": (
        "M83-R04",
        "M83-R05",
        "M83",
    ),
    "finite-certificates": (
        "M83-R03",
        "M83-R06",
        "M83-R07",
        "M83-R08",
        "M83",
        "M31",
        "M46",
        "M41",
        "M98",
        "M99",
    ),
}

SECTION_PATTERN = re.compile(r"^\\section\{.*\}$", re.MULTILINE)
CLAIM_PATTERN = re.compile(
    r"\\claimstatus\{([A-Z]+-\d{3})\}\{([A-Z]+)\}"
)
COMMAND_PATTERN = re.compile(r"^(?:python|pytest) .+$", re.MULTILINE)
PATH_PATTERN = re.compile(r"\\path\{([^}]+)\}")
CITATION_PATTERN = re.compile(r"\\cite\{([^}]+)\}")
LABEL_PATTERN = re.compile(r"\\label\{([^}]+)\}")
MILESTONE_PATTERN = re.compile(r"(?<![A-Z])M\d{2}(?:-R\d{2})?")


class AppendixReport(NamedTuple):
    """Validated anchor counts for one focused manuscript."""

    paper_id: str
    language: str
    main_sections: int
    appendix_sections: int
    commands: int
    paths: int
    citations: int


def split_appendix(text: str) -> tuple[str, str]:
    """Split one manuscript at its sole explicit appendix boundary."""
    marker = r"\appendix"
    if text.count(marker) != 1:
        raise AssertionError("appendix boundary count changed")
    main, appendix = text.split(marker, 1)
    return main, appendix


def extract_citations(text: str) -> tuple[str, ...]:
    """Extract citation keys while preserving manuscript order."""
    keys: list[str] = []
    for group in CITATION_PATTERN.findall(text):
        keys.extend(key.strip() for key in group.split(","))
    return tuple(keys)


def validate_paper_text(
    paper_id: str,
    language: str,
    text: str,
) -> AppendixReport:
    """Validate one focused manuscript's narrative/audit split."""
    key = (paper_id, language)
    if key not in PAPER_CONFIG:
        raise AssertionError(f"unknown focused manuscript: {key}")
    config = PAPER_CONFIG[key]
    main, appendix = split_appendix(text)

    forbidden_main = {
        "repository path": r"\path{",
        "archive macro": r"\archivepaper",
        "verbatim command block": r"\begin{verbatim}",
        "experiment ID": "EXP-",
        "file hash": "SHA-256",
    }
    for label, marker in forbidden_main.items():
        if marker in main:
            raise AssertionError(f"{paper_id}-{language} {label} remains in main")
    if COMMAND_PATTERN.search(main):
        raise AssertionError(f"{paper_id}-{language} command remains in main")
    if MILESTONE_PATTERN.search(main):
        raise AssertionError(
            f"{paper_id}-{language} milestone ID remains in main"
        )

    main_sections = tuple(SECTION_PATTERN.findall(main))
    appendix_sections = tuple(SECTION_PATTERN.findall(appendix))
    if main_sections != config["main_sections"]:
        raise AssertionError(f"{paper_id}-{language} main section order drifted")
    if appendix_sections != config["appendix_sections"]:
        raise AssertionError(
            f"{paper_id}-{language} appendix section order drifted"
        )

    labels = tuple(LABEL_PATTERN.findall(appendix))
    if labels != config["labels"]:
        raise AssertionError(f"{paper_id}-{language} appendix labels drifted")

    claims_main = tuple(
        claim_id
        for claim_id, status in CLAIM_PATTERN.findall(main)
        if status == "PROVED"
    )
    claims_all = tuple(
        claim_id for claim_id, _status in CLAIM_PATTERN.findall(text)
    )
    if claims_main != EXPECTED_CLAIMS[paper_id] or claims_all != claims_main:
        raise AssertionError(
            f"{paper_id}-{language} claim placement or status drifted"
        )

    commands = tuple(COMMAND_PATTERN.findall(appendix))
    if commands != EXPECTED_COMMANDS[paper_id]:
        raise AssertionError(f"{paper_id}-{language} command anchors drifted")

    paths = tuple(PATH_PATTERN.findall(appendix))
    if paths != EXPECTED_PATHS[paper_id]:
        raise AssertionError(f"{paper_id}-{language} archive paths drifted")
    if appendix.count(r"\archivepaper") != 1:
        raise AssertionError(f"{paper_id}-{language} archive macro drifted")

    citations = extract_citations(appendix)
    if citations != EXPECTED_CITATIONS[paper_id]:
        raise AssertionError(f"{paper_id}-{language} source anchors drifted")
    if extract_citations(main):
        raise AssertionError(f"{paper_id}-{language} source audit remains in main")

    milestones = tuple(dict.fromkeys(MILESTONE_PATTERN.findall(appendix)))
    if milestones != EXPECTED_MILESTONES[paper_id]:
        raise AssertionError(f"{paper_id}-{language} milestone anchors drifted")

    limitation = config["limitation"]
    normalized_appendix = " ".join(appendix.split())
    if not isinstance(limitation, str) or limitation not in normalized_appendix:
        raise AssertionError(f"{paper_id}-{language} limitation anchor missing")

    return AppendixReport(
        paper_id=paper_id,
        language=language,
        main_sections=len(main_sections),
        appendix_sections=len(appendix_sections),
        commands=len(commands),
        paths=len(paths),
        citations=len(citations),
    )


def validate_pair(
    paper_id: str,
    english: str,
    korean: str,
) -> tuple[AppendixReport, AppendixReport]:
    """Validate a bilingual pair and its exact audit-anchor parity."""
    english_report = validate_paper_text(paper_id, "en", english)
    korean_report = validate_paper_text(paper_id, "ko", korean)

    for extractor, label in (
        (COMMAND_PATTERN.findall, "commands"),
        (PATH_PATTERN.findall, "paths"),
        (extract_citations, "citations"),
    ):
        english_appendix = split_appendix(english)[1]
        korean_appendix = split_appendix(korean)[1]
        if tuple(extractor(english_appendix)) != tuple(
            extractor(korean_appendix)
        ):
            raise AssertionError(f"{paper_id} bilingual {label} drifted")
    return english_report, korean_report


def validate_all() -> tuple[AppendixReport, ...]:
    """Validate all three bilingual focused-paper pairs."""
    reports: list[AppendixReport] = []
    for paper_id in EXPECTED_CLAIMS:
        english = (FOCUSED / f"{paper_id}-en.tex").read_text(encoding="utf-8")
        korean = (FOCUSED / f"{paper_id}-ko.tex").read_text(encoding="utf-8")
        reports.extend(validate_pair(paper_id, english, korean))
    return tuple(reports)


def main() -> int:
    """Run the complete M89 appendix-boundary gate."""
    reports = validate_all()
    print(
        "M89 appendix-boundary checker: PASS "
        f"({len(reports)} papers, "
        f"{sum(report.main_sections for report in reports)} main sections, "
        f"{sum(report.appendix_sections for report in reports)} appendices, "
        f"{sum(report.commands for report in reports)} commands, "
        f"{sum(report.paths for report in reports)} paths, "
        f"{sum(report.citations for report in reports)} source anchors)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
