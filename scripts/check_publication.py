"""Check that the current manuscript and claims ledger remain synchronized."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLAIMS = ROOT / "research" / "CLAIMS.md"
PAPER = ROOT / "paper" / "main.tex"
MATRIX = ROOT / "research" / "PUBLICATION_CLAIMS.md"

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
    "Algorithms and bit-complexity synthesis",
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

    matrix = dict(MATRIX_ROW.findall(matrix_text))
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

    forbidden = (
        "we solve general classical factoring",
        "polynomial-time factoring of every integer",
        "the channels fail independently",
    )
    lower_paper = paper_text.lower()
    for phrase in forbidden:
        if phrase in lower_paper:
            fail(f"forbidden overclaim phrase: {phrase!r}")
            errors += 1

    if errors:
        return 1
    print(
        "Publication consistency: PASS "
        f"({len(ledger)} claims, {len(EXPERIMENT_RECORDS)} experiment hashes)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
