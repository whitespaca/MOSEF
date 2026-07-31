"""Generate the deterministic M83 bilingual related-work audit."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "schemas" / "m83-related-work-audit-v1.json"
MATRIX_EN = ROOT / "research" / "publication" / "M83-related-work-matrix-en.md"
MATRIX_KO = ROOT / "research" / "publication" / "M83-related-work-matrix-ko.md"
SEARCH_RECORD = ROOT / "research" / "literature" / "M83-primary-source-search.md"

SOURCES: tuple[dict[str, str], ...] = (
    {
        "source_id": "SRC-008",
        "citation_key": "pollard1974theorems",
        "inspection_level": "FULL_ARTICLE",
        "record": "research/literature/SRC-008-pollard-factorization-primality.md",
    },
    {
        "source_id": "SRC-005",
        "citation_key": "williams1982pplusone",
        "inspection_level": "FULL_ARTICLE",
        "record": "research/literature/SRC-005-williams-p-plus-one.md",
    },
    {
        "source_id": "SRC-009",
        "citation_key": "katona1966separating",
        "inspection_level": "PARTIAL_FULL_TEXT",
        "record": "research/literature/SRC-009-katona-separating-systems.md",
    },
    {
        "source_id": "SRC-010",
        "citation_key": "conway1976trigonometric",
        "inspection_level": "FULL_ARTICLE",
        "record": "research/literature/SRC-010-conway-jones-roots-unity.md",
    },
    {
        "source_id": "SRC-011",
        "citation_key": "bernstein2004smoothparts",
        "inspection_level": "FULL_ARTICLE",
        "record": "research/literature/SRC-011-bernstein-smooth-parts.md",
    },
    {
        "source_id": "SRC-012",
        "citation_key": "yao1976evaluation",
        "inspection_level": "ABSTRACT_ONLY",
        "record": "research/literature/SRC-012-yao-evaluation-powers.md",
    },
    {
        "source_id": "SRC-013",
        "citation_key": "lokshtanov2009oct",
        "inspection_level": "FULL_ARTICLE",
        "record": (
            "research/literature/"
            "M99-odd-cycle-transversal-iterative-compression.md"
        ),
    },
)

ROWS: tuple[dict[str, Any], ...] = (
    {
        "row_id": "M83-R01",
        "paper": "promise-factorization",
        "claim_ids": ["THM-001"],
        "source_ids": ["SRC-008"],
        "classification": "SCOPED_SYNTHESIS",
        "established_en": (
            "Pollard gives the practical smooth-p-1 mechanism, including "
            "unit and full-collision branches."
        ),
        "established_ko": (
            "Pollard는 unit 및 full-collision 분기를 포함한 실용적 "
            "smooth-p-1 메커니즘을 제시한다."
        ),
        "project_en": (
            "The project closes a fresh-sample hereditary-promise recursion "
            "with an explicit 5/12 cycle bound and expected bit cost."
        ),
        "project_ko": (
            "본 연구는 fresh sample을 쓰는 유전적 약속 재귀를 명시적 "
            "5/12 cycle 하한과 기대 비트 비용까지 닫는다."
        ),
    },
    {
        "row_id": "M83-R02",
        "paper": "promise-factorization",
        "claim_ids": ["LEM-003", "THM-002"],
        "source_ids": ["SRC-005"],
        "classification": "SCOPED_SYNTHESIS",
        "established_en": (
            "Williams gives the Lucas p+1 mechanism and its split, nonsplit, "
            "and zero-discriminant hypotheses."
        ),
        "established_ko": (
            "Williams는 Lucas p+1 메커니즘과 split, nonsplit, "
            "zero-discriminant 가정을 제시한다."
        ),
        "project_en": (
            "The project proves its exact parameter-root count, preserves "
            "degenerate branches, and derives the greater-than-1/12 witness bound."
        ),
        "project_ko": (
            "본 연구는 정확한 매개변수 root count를 증명하고 퇴화 분기를 "
            "보존하며 1/12보다 큰 witness 하한을 유도한다."
        ),
    },
    {
        "row_id": "M83-R03",
        "paper": "promise-and-finite",
        "claim_ids": ["BAR-001", "BAR-024"],
        "source_ids": ["SRC-009"],
        "classification": "SCOPED_SYNTHESIS",
        "established_en": (
            "Binary membership signatures and pair-separating set systems are "
            "classical combinatorial objects."
        ),
        "established_ko": (
            "이진 membership signature와 pair-separating set system은 "
            "고전적 조합론 객체이다."
        ),
        "project_en": (
            "The project specializes injectivity to divisor/support observables, "
            "prime-power valuations, and exact proper-GCD semantics."
        ),
        "project_ko": (
            "본 연구는 단사성을 divisibility/support 관측량, 소수거듭제곱 "
            "valuation, 정확한 proper-GCD 의미론에 특수화한다."
        ),
    },
    {
        "row_id": "M83-R04",
        "paper": "cyclotomic-extraction",
        "claim_ids": ["BAR-018", "BAR-019"],
        "source_ids": ["SRC-012"],
        "classification": "SCOPED_SYNTHESIS",
        "established_en": (
            "Shared multiplication schedules for evaluating several powers are "
            "classical addition-chain context."
        ),
        "established_ko": (
            "여러 거듭제곱을 평가하는 공유 곱셈 schedule은 고전적 "
            "addition-chain 문맥이다."
        ),
        "project_en": (
            "The project separately proves its exponent-growth and exact-output "
            "charges; the cited source was inspected only at abstract level."
        ),
        "project_ko": (
            "본 연구의 지수 성장 및 exact-output 과금은 별도 증명이며, "
            "인용 문헌은 초록 수준에서만 확인했다."
        ),
    },
    {
        "row_id": "M83-R05",
        "paper": "cyclotomic-extraction",
        "claim_ids": ["THM-003", "BAR-020"],
        "source_ids": ["SRC-010"],
        "classification": "SCOPED_SYNTHESIS",
        "established_en": (
            "Galois actions, short vanishing sums of roots of unity, and rational "
            "cosine relations are established methods."
        ),
        "established_ko": (
            "Galois 작용, 짧은 root-of-unity 소멸합, 유리 cosine 관계는 "
            "확립된 방법이다."
        ),
        "project_en": (
            "The project reconstructs a restricted signed depth-two "
            "common-step/Phi4/Phi6 classification and evaluator."
        ),
        "project_ko": (
            "본 연구는 제한된 signed depth-two 관측량의 "
            "common-step/Phi4/Phi6 분류와 evaluator를 재구성한다."
        ),
    },
    {
        "row_id": "M83-R06",
        "paper": "finite-certificates",
        "claim_ids": ["THM-004", "THM-005", "THM-014", "THM-019"],
        "source_ids": ["SRC-009", "SRC-011"],
        "classification": "SCOPED_SYNTHESIS",
        "established_en": (
            "Separating signatures and product/remainder-tree batch evaluation "
            "are established background."
        ),
        "established_ko": (
            "분리 signature와 product/remainder-tree batch 평가는 확립된 "
            "배경이다."
        ),
        "project_en": (
            "The project gives complete finite, family-relative certificates "
            "for one explicit selector through bit length 34."
        ),
        "project_ko": (
            "본 연구는 하나의 명시적 selector족에 대해 비트길이 34까지 "
            "완전한 family-relative 유한 인증서를 준다."
        ),
    },
    {
        "row_id": "M83-R07",
        "paper": "finite-certificates",
        "claim_ids": ["BAR-041", "BAR-042", "BAR-043", "BAR-044", "BAR-045", "BAR-046"],
        "source_ids": ["SRC-009", "SRC-011"],
        "classification": "SCOPED_SYNTHESIS",
        "established_en": (
            "Signature counting and charged batch evaluation are general "
            "background tools."
        ),
        "established_ko": (
            "signature counting과 과금된 batch 평가는 일반적 배경 도구이다."
        ),
        "project_en": (
            "The proved noninjectivity bounds are restricted to the repository's "
            "declared numeric-cap and compact-gap grammars and constant ranges."
        ),
        "project_ko": (
            "증명된 비단사 경계는 저장소가 선언한 numeric-cap 및 "
            "compact-gap 문법과 상수 범위에만 적용된다."
        ),
    },
    {
        "row_id": "M83-R08",
        "paper": "finite-certificates",
        "claim_ids": ["THM-028"],
        "source_ids": ["SRC-013"],
        "classification": "ESTABLISHED_BACKGROUND",
        "established_en": (
            "Lokshtanov, Saurabh, and Sikdar give iterative-compression "
            "OCT discovery in O(3^k k |E| |V|) time."
        ),
        "established_ko": (
            "Lokshtanov, Saurabh, Sikdar는 O(3^k k |E| |V|) 시간의 "
            "iterative-compression OCT discovery를 제시한다."
        ),
        "project_en": (
            "The project reconstructs that established method for explicit "
            "coverer graphs, adds local bit accounting, and composes it with "
            "the separately proved exact-repair reduction."
        ),
        "project_ko": (
            "본 연구는 그 확립된 방법을 명시적 coverer graph에 맞게 "
            "재구성하고 local bit 비용을 과금한 뒤 별도 증명된 exact "
            "repair reduction과 합성한다."
        ),
    },
)

SOURCE_HASH_PATHS = (
    *(source["record"] for source in SOURCES),
    "research/literature/M83-primary-source-search.md",
    "research/reviews/2026-07-31-m83-source-scope-review.md",
    "paper/references.bib",
    "paper/main.tex",
    "paper/main-ko.tex",
    "paper/focused/promise-factorization-en.tex",
    "paper/focused/promise-factorization-ko.tex",
    "paper/focused/cyclotomic-extraction-en.tex",
    "paper/focused/cyclotomic-extraction-ko.tex",
    "paper/focused/finite-certificates-en.tex",
    "paper/focused/finite-certificates-ko.tex",
)


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


def build_artifact() -> dict[str, Any]:
    """Build the source and positioning projection."""
    source_hashes = {
        path: sha256_text_file(ROOT / path) for path in SOURCE_HASH_PATHS
    }
    rows = []
    for row in ROWS:
        projected = dict(row)
        projected["priority_status"] = "NO_PRIORITY_CLAIM"
        rows.append(projected)
    artifact: dict[str, Any] = {
        "schema_version": "1.0.0",
        "milestone": "M83",
        "generated_date": "2026-07-31",
        "audit_scope": "BOUNDED_PRIMARY_SOURCE_AUDIT",
        "sources": [dict(source) for source in SOURCES],
        "rows": rows,
        "classification_counts": {
            "established_background_components": len(rows),
            "scoped_synthesis_rows": sum(
                row["classification"] == "SCOPED_SYNTHESIS"
                for row in rows
            ),
            "positively_labeled_plausibly_new_rows": 0,
        },
        "search_record": SEARCH_RECORD.relative_to(ROOT).as_posix(),
        "negative_search_rule": (
            "failure to locate an exact match is not evidence of novelty or priority"
        ),
        "source_sha256": source_hashes,
        "scope": {
            "general_classical_polynomial_time_factoring": "OPEN",
            "novelty_claims_made": False,
            "priority_claims_made": False,
            "finite_certificate_max_input_length": 34,
        },
    }
    artifact["audit_summary_sha256"] = canonical_hash(artifact)
    return artifact


def marker(row: dict[str, Any]) -> str:
    """Render one language-independent synchronization marker."""
    claims = ",".join(row["claim_ids"])
    sources = ",".join(row["source_ids"])
    return (
        f"<!-- {row['row_id']}|{row['classification']}|"
        f"{claims}|{sources}|NO_PRIORITY_CLAIM -->"
    )


def render_matrix(language: str) -> str:
    """Render one human-readable synchronized matrix."""
    if language == "en":
        title = "# M83 related-work and positioning matrix"
        intro = (
            "This bounded primary-source audit distinguishes established mechanisms "
            "from the repository's scoped self-contained results. An unmatched "
            "search phrase is not evidence of novelty or priority."
        )
        header = (
            "| Row | Representative result | Primary basis | Established background | "
            "Scoped project result | Priority status |\n"
            "|---|---|---|---|---|---|"
        )
    else:
        title = "# M83 관련 연구 및 포지셔닝 행렬"
        intro = (
            "이 제한적 1차 문헌 감사는 확립된 메커니즘과 저장소의 제한적 "
            "자기완결 결과를 구분한다. 검색에서 같은 문구를 찾지 못한 사실은 "
            "독창성이나 우선권의 증거가 아니다."
        )
        header = (
            "| 행 | 대표 결과 | 1차 문헌 기반 | 확립된 배경 | 제한적 프로젝트 결과 | "
            "우선권 상태 |\n"
            "|---|---|---|---|---|---|"
        )
    lines = [title, "", intro, "", header]
    for row in ROWS:
        claims = ", ".join(f"`{claim}`" for claim in row["claim_ids"])
        sources = ", ".join(f"`{source}`" for source in row["source_ids"])
        established = row[f"established_{language}"]
        project = row[f"project_{language}"]
        status = "No priority claim" if language == "en" else "우선권 주장 없음"
        table_row = (
            f"| {row['row_id']} | {claims} | {sources} | {established} | "
            + f"{project} | {status} |"
        )
        lines.extend(
            (
                marker(row),
                table_row,
            )
        )
    if language == "en":
        scope = (
            "No row is positively labeled plausibly new by M83. This means the "
            "bounded audit does not discharge priority, not that the exact results "
            "are known duplicates. General classical polynomial-time factoring "
            "remains open."
        )
    else:
        scope = (
            "M83은 어느 행에도 '새 결과로 개연적'이라는 양성 라벨을 붙이지 않는다. "
            "이는 제한 감사가 우선권을 입증하지 못했다는 뜻이지, 정확한 결과가 이미 "
            "중복된다는 뜻이 아니다. 일반 고전적 다항시간 인수분해는 열린 문제이다."
        )
    lines.extend(("", "## Scope", "", scope, ""))
    return "\n".join(lines)


def main() -> int:
    """Write or check the registered artifact and synchronized matrices."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    outputs = {
        OUTPUT: json.dumps(build_artifact(), ensure_ascii=False, indent=2) + "\n",
        MATRIX_EN: render_matrix("en"),
        MATRIX_KO: render_matrix("ko"),
    }
    if args.check:
        stale = [
            path.relative_to(ROOT).as_posix()
            for path, content in outputs.items()
            if not path.is_file() or path.read_text(encoding="utf-8") != content
        ]
        if stale:
            raise SystemExit(f"M83 generated outputs are stale: {', '.join(stale)}")
        print("M83 related-work outputs are current")
        return 0
    for path, content in outputs.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="\n")
        print(f"wrote {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
