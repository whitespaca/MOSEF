"""Check that the current manuscript and claims ledger remain synchronized."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLAIMS = ROOT / "research" / "CLAIMS.md"
PAPER = ROOT / "paper" / "main.tex"
KOREAN_PAPER = ROOT / "paper" / "main-ko.tex"
KOREAN_CLAIMS = ROOT / "paper" / "claim-status-ko.tex"
MATRIX = ROOT / "research" / "PUBLICATION_CLAIMS.md"
M50_ARTIFACT = ROOT / "schemas" / "m50-finite-threshold-summary-v1.json"
M50_TABLE_EN = ROOT / "paper" / "tables" / "finite-threshold-summary-en.tex"
M50_TABLE_KO = ROOT / "paper" / "tables" / "finite-threshold-summary-ko.tex"

CLAIM_ROW = re.compile(r"^\| ([A-Z]+-\d+) \| ([A-Z]+) \|", re.MULTILINE)
PAPER_CLAIM = re.compile(r"\\claimstatus\{([A-Z]+-\d+)\}\{([^}]+)\}")
MATRIX_ROW = re.compile(r"^\| ([A-Z]+-\d+) \| ([A-Z]+) \|", re.MULTILINE)
SHA256 = re.compile(r"\b[0-9a-f]{64}\b")
CORE_COMMIT = re.compile(
    r"The M6 manuscript core\s+commit is "
    r"\\texttt\{\\seqsplit\{([0-9a-f]{40})\}\}"
)

REQUIRED_SECTIONS = (
    "Introduction and contributions",
    "Related work and complexity landscape",
    "Model and definitions",
    "Order separators and algorithmic framework",
    "A restricted semismooth-order theorem",
    "Difference coverage versus order separation",
    "A two-channel correlation barrier",
    "A restricted nonsplit Lucas theorem",
    "A combined-promise density barrier",
    "An exponent-encoding divisor barrier",
    "A multiplication straight-line compression barrier",
    "A constant-sensitive boundary barrier",
    "A factor-scale primorial barrier",
    "A general factor-scale boundary barrier",
    "An addition-subtraction compression barrier",
    "A leaf-materialized implicit-batch barrier",
    "A non-materializing explicit-atom product-DAG barrier",
    "A dyadic exact-division and composition barrier",
    "An arbitrary-exponent geometric-sum barrier",
    "A nested geometric-quotient barrier",
    "An iterated geometric-quotient-chain barrier",
    "Signed aggregation separates from product-only iteration",
    "A symmetric signed-difference reduction",
    "An unequal signed-form reduction",
    "Primitive rational residues and exceptional cyclotomic factors",
    "A complete rational root-orbit classification",
    "Compact extraction from the exceptional cofactors",
    "A fixed exceptional-cofactor schedule barrier",
    "A length-indexed materialized-support barrier",
    "Compact cofactor support and the single-coordinate limit",
    "Support signatures: separation, collisions, and candidate lower bounds",
    "Public selector family and support normalization",
    "Selector evaluation and the first finite thresholds",
    "Finite promise theorem and family-relative threshold synthesis",
    "Supplementary finite threshold audit trail",
    "Linearly wide encoded compact-gap barrier",
    "Subquadratic encoded compact-gap barrier",
    "Packing-aware compact-gap boundary constants",
    "Distinct-GCD-gap high-weight charging",
    "Sharpness of realizable GCD gaps",
    "Exact overlap GCDs and prefix LCM scale",
    "Compact-step and bit-operation complexity",
    "Reproducible experimental methodology",
    "Results",
    "Limitations and open problems",
    "Conclusion",
)

REQUIRED_PROOFS = (
    r"\label{proof:LEM-001}",
    r"\label{proof:LEM-002}",
    r"\label{proof:THM-001}",
    r"\label{proof:BAR-001}",
    r"\label{proof:BAR-002}",
    r"\label{proof:LEM-003}",
    r"\label{proof:THM-002}",
    r"\label{proof:BAR-003}",
    r"\label{proof:BAR-004}",
    r"\label{proof:BAR-005}",
    r"\label{proof:BAR-006}",
    r"\label{proof:BAR-007}",
    r"\label{proof:BAR-008}",
    r"\label{proof:BAR-009}",
    r"\label{proof:BAR-010}",
    r"\label{proof:BAR-011}",
    r"\label{proof:BAR-012}",
    r"\label{proof:BAR-013}",
    r"\label{proof:BAR-014}",
    r"\label{proof:BAR-015}",
    r"\label{proof:BAR-016}",
    r"\label{proof:BAR-017}",
    r"\label{proof:BAR-018}",
    r"\label{proof:BAR-019}",
    r"\label{proof:THM-003}",
    r"\label{proof:BAR-020}",
    r"\label{proof:BAR-021}",
    r"\label{proof:BAR-022}",
    r"\label{proof:BAR-023}",
    r"\label{proof:BAR-024}",
    r"\label{proof:THM-004-BAR-025}",
    r"\label{proof:THM-005-BAR-026}",
    r"\label{proof:THM-006-BAR-027}",
    r"\label{proof:THM-007-BAR-028}",
    r"\label{proof:THM-008-BAR-029}",
    r"\label{proof:THM-009-BAR-030}",
    r"\label{proof:THM-010-BAR-031}",
    r"\label{proof:THM-011-BAR-032}",
    r"\label{proof:THM-012-BAR-033}",
    r"\label{proof:THM-013-BAR-034}",
    r"\label{proof:THM-014-BAR-035}",
    r"\label{proof:THM-015-BAR-036}",
    r"\label{proof:THM-016-BAR-037}",
    r"\label{proof:THM-017-BAR-038}",
    r"\label{proof:THM-018-BAR-039}",
    r"\label{proof:THM-019-BAR-040}",
    r"\label{proof:BAR-041}",
    r"\label{proof:BAR-042}",
    r"\label{proof:BAR-043}",
    r"\label{proof:BAR-044}",
    r"\label{proof:BAR-045}",
    r"\label{proof:BAR-046}",
    r"\label{proof:BAR-047}",
    r"\label{proof:BAR-048}",
)

EXPERIMENT_RECORDS = (
    ROOT / "research" / "experiments" / "EXP-0002-m2-separator-search.md",
    ROOT / "research" / "experiments" / "EXP-0003-m3-semismooth-search.md",
    ROOT / "research" / "experiments" / "EXP-0004-m4-difference-cover-search.md",
    ROOT / "research" / "experiments" / "EXP-0005-m5-multigroup-correlation.md",
    ROOT / "research" / "experiments" / "EXP-0006-m7-nonsplit-lucas.md",
    ROOT / "research" / "experiments" / "EXP-0007-m8-promise-density.md",
    ROOT / "research" / "experiments" / "EXP-0008-m9-divisor-budget.md",
    ROOT / "research" / "experiments" / "EXP-0009-m10-compressed-exponents.md",
    ROOT / "research" / "experiments" / "EXP-0010-m11-boundary-schedule.md",
    ROOT / "research" / "experiments" / "EXP-0011-m12-primorial-scale.md",
    ROOT / "research" / "experiments" / "EXP-0012-m13-general-factor-scale.md",
    ROOT / "research" / "experiments" / "EXP-0013-m14-addition-subtraction.md",
    ROOT / "research" / "experiments" / "EXP-0014-m15-implicit-batch.md",
    ROOT / "research" / "experiments" / "EXP-0015-m16-product-dag.md",
    ROOT / "research" / "experiments" / "EXP-0016-m17-dyadic-telescope.md",
    ROOT / "research" / "experiments" / "EXP-0017-m18-geometric-sum.md",
    ROOT / "research" / "experiments" / "EXP-0018-m19-nested-quotient.md",
    ROOT / "research" / "experiments" / "EXP-0019-m20-iterated-quotient.md",
    ROOT
    / "research"
    / "experiments"
    / "EXP-0020-m21-quotient-linear-combination.md",
    ROOT
    / "research"
    / "experiments"
    / "EXP-0021-m22-symmetric-quotient-difference.md",
    ROOT
    / "research"
    / "experiments"
    / "EXP-0022-m23-unequal-signed-reduction.md",
    ROOT
    / "research"
    / "experiments"
    / "EXP-0023-m24-rational-residue-audit.md",
    ROOT
    / "research"
    / "experiments"
    / "EXP-0024-m25-rational-root-orbits.md",
    ROOT
    / "research"
    / "experiments"
    / "EXP-0025-m26-exceptional-cyclotomic.md",
    ROOT
    / "research"
    / "experiments"
    / "EXP-0026-m27-exceptional-cofactor-schedule.md",
    ROOT
    / "research"
    / "experiments"
    / "EXP-0027-m28-length-indexed-support.md",
    ROOT
    / "research"
    / "experiments"
    / "EXP-0028-m29-compact-cofactor-prime-support.md",
    ROOT
    / "research"
    / "experiments"
    / "EXP-0029-m30-compact-support-signatures.md",
    ROOT
    / "research"
    / "experiments"
    / "EXP-0030-m31-diversified-compact-signatures.md",
    ROOT
    / "research"
    / "experiments"
    / "EXP-0031-m32-widened-selector-cap.md",
    ROOT
    / "research"
    / "experiments"
    / "EXP-0032-m33-linear-cap-recurrence.md",
    ROOT
    / "research"
    / "experiments"
    / "EXP-0033-m34-next-envelope.md",
    ROOT
    / "research"
    / "experiments"
    / "EXP-0034-m35-next-envelope.md",
    ROOT
    / "research"
    / "experiments"
    / "EXP-0035-m36-distinct-cap.md",
    ROOT
    / "research"
    / "experiments"
    / "EXP-0036-m37-length-25-cap.md",
    ROOT
    / "research"
    / "experiments"
    / "EXP-0037-m38-length-26-cap.md",
    ROOT
    / "research"
    / "experiments"
    / "EXP-0038-m39-length-27-cap.md",
    ROOT
    / "research"
    / "experiments"
    / "EXP-0039-m40-length-28-cap.md",
    ROOT
    / "research"
    / "experiments"
    / "EXP-0040-m41-length-29-cap.md",
    ROOT
    / "research"
    / "experiments"
    / "EXP-0041-m42-length-30-cap.md",
    ROOT
    / "research"
    / "experiments"
    / "EXP-0042-m43-length-31-cap.md",
    ROOT
    / "research"
    / "experiments"
    / "EXP-0043-m44-length-32-cap.md",
    ROOT
    / "research"
    / "experiments"
    / "EXP-0044-m45-length-33-cap.md",
    ROOT
    / "research"
    / "experiments"
    / "EXP-0045-m46-length-34-cap.md",
    ROOT
    / "research"
    / "experiments"
    / "EXP-0046-m47-polynomial-cap-support.md",
    ROOT
    / "research"
    / "experiments"
    / "EXP-0047-m48-compact-gap-overlap.md",
    ROOT
    / "research"
    / "experiments"
    / "EXP-0048-m49-wide-span-compact-gap.md",
    ROOT
    / "research"
    / "experiments"
    / "EXP-0049-m51-subquadratic-span.md",
    ROOT
    / "research"
    / "experiments"
    / "EXP-0050-m52-boundary-constant.md",
    ROOT
    / "research"
    / "experiments"
    / "EXP-0051-m53-distinct-gap.md",
    ROOT
    / "research"
    / "experiments"
    / "EXP-0052-m54-realizable-gap.md",
    ROOT
    / "research"
    / "experiments"
    / "EXP-0053-m55-overlap-gcd.md",
)


def fail(message: str) -> None:
    """Report one publication-integrity failure."""
    print(f"publication check: FAIL: {message}", file=sys.stderr)


def normalized_status(raw: str) -> str:
    """Return the ledger status represented by a manuscript status label."""
    return raw.split(",", maxsplit=1)[0].strip()


def parse_args() -> argparse.Namespace:
    """Parse the bootstrap exception used before the M6 core commit exists."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--allow-placeholder",
        action="store_true",
        help="permit M6_CORE_COMMIT only while creating the manuscript core commit",
    )
    return parser.parse_args()


def main() -> int:
    """Validate claim IDs, statuses, sections, proofs, and experiment hashes."""
    args = parse_args()
    claims_text = CLAIMS.read_text(encoding="utf-8")
    paper_text = PAPER.read_text(encoding="utf-8")
    korean_paper_text = KOREAN_PAPER.read_text(encoding="utf-8")
    korean_claims_text = KOREAN_CLAIMS.read_text(encoding="utf-8")
    matrix_text = MATRIX.read_text(encoding="utf-8")
    errors = 0

    ledger = dict(CLAIM_ROW.findall(claims_text))
    if not ledger:
        fail("no claim rows found in research/CLAIMS.md")
        return 1

    paper_matches = PAPER_CLAIM.findall(paper_text)
    paper_ids = [claim_id for claim_id, _ in paper_matches]
    duplicates = sorted(
        claim_id for claim_id in set(paper_ids) if paper_ids.count(claim_id) != 1
    )
    if duplicates:
        fail(f"manuscript claim IDs must occur exactly once: {duplicates}")
        errors += 1

    paper = {
        claim_id: normalized_status(status)
        for claim_id, status in paper_matches
    }
    missing_from_paper = sorted(set(ledger) - set(paper))
    unknown_in_paper = sorted(set(paper) - set(ledger))
    if missing_from_paper:
        fail(f"ledger claims absent from manuscript: {missing_from_paper}")
        errors += 1
    if unknown_in_paper:
        fail(f"manuscript claims absent from ledger: {unknown_in_paper}")
        errors += 1
    for claim_id in sorted(set(ledger) & set(paper)):
        if ledger[claim_id] != paper[claim_id]:
            fail(
                f"{claim_id} status mismatch: "
                f"ledger={ledger[claim_id]}, manuscript={paper[claim_id]}"
            )
            errors += 1

    matrix_matches = MATRIX_ROW.findall(matrix_text)
    matrix = dict(matrix_matches)
    if set(matrix) != set(ledger):
        fail("publication claim matrix must contain every ledger claim exactly once")
        errors += 1
    for claim_id in sorted(set(ledger) & set(matrix)):
        if ledger[claim_id] != matrix[claim_id]:
            fail(
                f"{claim_id} matrix status mismatch: "
                f"ledger={ledger[claim_id]}, matrix={matrix[claim_id]}"
            )
            errors += 1

    korean_matches = PAPER_CLAIM.findall(korean_claims_text)
    korean_ids = [claim_id for claim_id, _ in korean_matches]
    korean_duplicates = sorted(
        claim_id
        for claim_id in set(korean_ids)
        if korean_ids.count(claim_id) != 1
    )
    if korean_duplicates:
        fail(
            "Korean claim appendix IDs must occur exactly once: "
            f"{korean_duplicates}"
        )
        errors += 1
    korean_claims = {
        claim_id: normalized_status(status)
        for claim_id, status in korean_matches
    }
    if korean_claims != ledger:
        fail("Korean claim appendix must match every ledger claim and status")
        errors += 1
    if korean_matches != matrix_matches:
        fail("Korean claim appendix must preserve publication-matrix order")
        errors += 1
    if r"\input{paper/claim-status-ko.tex}" not in korean_paper_text:
        fail("Korean manuscript does not include its generated claim appendix")
        errors += 1
    if r"\input{paper/tables/finite-threshold-summary-en.tex}" not in paper_text:
        fail("English manuscript does not include the generated M50 table")
        errors += 1
    if (
        r"\input{paper/tables/finite-threshold-summary-ko.tex}"
        not in korean_paper_text
    ):
        fail("Korean manuscript does not include the generated M50 table")
        errors += 1
    for generated in (M50_ARTIFACT, M50_TABLE_EN, M50_TABLE_KO):
        if not generated.exists():
            fail(f"missing M50 generated artifact: {generated.relative_to(ROOT)}")
            errors += 1

    for section in REQUIRED_SECTIONS:
        if rf"\section{{{section}}}" not in paper_text:
            fail(f"missing required section: {section}")
            errors += 1
    if r"\appendix" not in paper_text:
        fail("missing appendix")
        errors += 1
    for marker in REQUIRED_PROOFS:
        if marker not in paper_text:
            fail(f"missing full-proof marker: {marker}")
            errors += 1

    core_commits = CORE_COMMIT.findall(paper_text)
    placeholder_present = "M6\\_CORE\\_COMMIT" in paper_text
    if args.allow_placeholder and placeholder_present:
        pass
    elif placeholder_present:
        fail("unresolved M6_CORE_COMMIT placeholder")
        errors += 1
    elif len(core_commits) != 1:
        fail("reproduction appendix must contain exactly one 40-hex M6 core commit")
        errors += 1

    for record in EXPERIMENT_RECORDS:
        hashes = SHA256.findall(record.read_text(encoding="utf-8").lower())
        if not hashes:
            fail(f"no SHA-256 found in {record.relative_to(ROOT)}")
            errors += 1
            continue
        summary_hash = hashes[-1]
        if summary_hash not in paper_text.lower():
            fail(
                "manuscript reproduction appendix omits hash "
                f"{summary_hash} from {record.relative_to(ROOT)}"
            )
            errors += 1
        if record.name.startswith(
            (
                "EXP-0028",
                "EXP-0029",
                "EXP-0030",
                "EXP-0031",
                "EXP-0032",
                "EXP-0033",
                "EXP-0034",
                "EXP-0035",
                "EXP-0036",
                "EXP-0037",
                "EXP-0038",
                "EXP-0039",
                "EXP-0040",
                "EXP-0041",
                "EXP-0042",
                "EXP-0043",
                "EXP-0044",
                "EXP-0045",
                "EXP-0046",
                "EXP-0047",
                "EXP-0048",
            )
        ) and (
            summary_hash not in korean_paper_text.lower()
        ):
            fail(
                "Korean manuscript reproduction appendix omits current hash "
                f"{summary_hash}"
            )
            errors += 1

    forbidden = (
        "we solve general classical factoring",
        "polynomial-time factoring of every integer",
        "the channels fail independently",
    )
    lower_paper = paper_text.lower()
    normalized_paper = " ".join(lower_paper.split())
    for phrase in forbidden:
        if phrase in lower_paper:
            fail(f"forbidden overclaim phrase: {phrase!r}")
            errors += 1
    required_scope_phrases = (
        "mosef names the research program",
        "computer-assisted finite promise theorem",
        "family-relative thresholds",
        "not an asymptotic rate",
        "compact modular steps, not to standard bit operations",
    )
    for phrase in required_scope_phrases:
        if phrase not in normalized_paper:
            fail(f"English manuscript omits required scope phrase: {phrase!r}")
            errors += 1
    forbidden_title_counts = (
        "eighteen restricted theorems",
        "thirty-six structural barriers",
    )
    for phrase in forbidden_title_counts:
        if phrase in lower_paper:
            fail(f"English title-count wording remains: {phrase!r}")
            errors += 1

    required_korean = (
        "고전적 정수분해",
        "M29: compact cofactor support와 단일 좌표 한계",
        "일반 정수분해",
        "M30",
        "signature 사상이 단사",
        "M31: 공개 selector family와 support 정규화",
        "191,227,233",
        "M32: selector 계산과 첫 family-relative threshold",
        "THM-005",
        "809,827",
        "M33: 길이 21 재발과 복구",
        "THM-006",
        "1031,1231,1319,1433",
        "M34: 길이 22 유한 envelope의 도약",
        "THM-007",
        "1481,1511,1571,1663,1721,1747,1867,1931,2029",
        "M35: 길이 23의 유한 envelope",
        "THM-008",
        "2411,2477,2741,2777,2837",
        "M36: 길이 24의 서로 다른 cap",
        "THM-009",
        "3049,3643,3769,3863,4057",
        "M37: 길이 25의 유한 envelope",
        "THM-010",
        "4133,4297,4337,4423,4663,5011,5179,5233,5297",
        "M38: 길이 26의 유한 envelope",
        "THM-011",
        "6229,6703,6793,6947,7187,7229,7649",
        "M39: 길이 27의 유한 envelope",
        "THM-012",
        "9463,9791,10607,10939,11087,11213",
        "M40: 길이 28의 유한 envelope",
        "THM-013",
        "11867,12791,13633,13967,14051,15559",
        "M41: 길이 29의 유한 envelope",
        "THM-014",
        "18979,21031",
        "M42: 길이 30의 유한 envelope",
        "THM-015",
        "28591,29209,29387",
        "M43: 길이 31의 유한 envelope",
        "THM-016",
        "37483,44963",
        "M44: 길이 32의 유한 envelope",
        "THM-017",
        "59699,63463",
        "M45: 길이 33의 유한 envelope",
        "THM-018",
        "80309,92671",
        "M46: 길이 34의 유한 envelope",
        "THM-019",
        "97927,99527,127877",
        "M47: polynomial numeric-cap support 장벽",
        "BAR-041",
        "1.25506",
        "M48: short-span encoded compact-gap 장벽",
        "BAR-042",
        "1,636,992",
        "M49: 선형 폭 encoded compact-gap 장벽",
        "BAR-043",
        "M51: subquadratic encoded compact-gap 장벽",
        "BAR-044",
        "Delta_m",
        "o(m^2)",
        "3,645,232",
        "M52: packing-aware compact-gap 경계 상수",
        "BAR-045",
        "c=1/8",
        "89e5465e4f1bf4d577d77d3c7624682405ecf7b8aa208432916cab2e90a8d3aa",
        "M53: distinct-GCD-gap high-weight charge",
        "BAR-046",
        "c=1/2",
        "7b066fc90a8925934886c5e6ee9b819a4dda95bb00c32732430eda3b5d58376b",
        "M54: realizable GCD gap의 sharpness",
        "BAR-047",
        "fc09459c7cc6b93a2be7b8255e28fc64f3637e3b9a015ef45757f4b91a7da96c",
        "M55: exact overlap GCD",
        "BAR-048",
        "b82926a482dd133d94a3e89f041d23ec225ea2d9d30061d25f6e75c017b01534",
    )
    for phrase in required_korean:
        if phrase not in korean_paper_text:
            fail(f"Korean manuscript omits required text: {phrase!r}")
            errors += 1
    forbidden_korean = (
        "일반 고전적 정수분해를 해결했다",
        "모든 정수를 다항 시간에 인수분해한다",
    )
    for phrase in forbidden_korean:
        if phrase in korean_paper_text:
            fail(f"Korean manuscript contains overclaim phrase: {phrase!r}")
            errors += 1
    required_korean_scope = (
        "computer-assisted finite promise theorem",
        "family-relative threshold",
        "표준 bit-operation",
        "offline certificate",
    )
    for phrase in required_korean_scope:
        if phrase not in korean_paper_text:
            fail(f"Korean manuscript omits scope phrase: {phrase!r}")
            errors += 1
    for phrase in ("열여덟 개의 제한 정리", "서른여섯 개의 구조적 장벽"):
        if phrase in korean_paper_text:
            fail(f"Korean title-count wording remains: {phrase!r}")
            errors += 1

    if errors:
        return 1
    print(
        "Bilingual publication consistency: PASS "
        f"({len(ledger)} claims, {len(EXPERIMENT_RECORDS)} experiment hashes)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
