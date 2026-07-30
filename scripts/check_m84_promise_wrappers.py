"""Independently check the M84 bounded-wrapper contract and publication."""

from __future__ import annotations

import ast
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IMPLEMENTATION = ROOT / "python" / "mosef_reference" / "promise_wrappers.py"
PROOF = ROOT / "research" / "proofs" / "M84-bounded-total-promise-wrappers.md"
REVIEW = ROOT / "research" / "reviews" / "2026-07-31-m84-total-wrapper-review.md"
CLAIMS = ROOT / "research" / "CLAIMS.md"
PAPERS = (
    ROOT / "paper" / "main.tex",
    ROOT / "paper" / "main-ko.tex",
    ROOT / "paper" / "focused" / "promise-factorization-en.tex",
    ROOT / "paper" / "focused" / "promise-factorization-ko.tex",
)


def validate_implementation(text: str) -> list[str]:
    """Check the public result states, wrappers, and factor-oblivious scope."""
    errors: list[str] = []
    try:
        tree = ast.parse(text)
    except SyntaxError as error:
        return [f"implementation syntax error: {error}"]
    names = {
        node.name
        for node in ast.walk(tree)
        if isinstance(node, (ast.ClassDef, ast.FunctionDef))
    }
    required_names = {
        "BoundedFactorizationStatus",
        "BoundedFactorizationResult",
        "local_unresolved_probability_bound",
        "complete_unresolved_probability_bound",
        "factor_semismooth_bounded",
        "factor_nonsplit_lucas_bounded",
    }
    missing = sorted(required_names - names)
    if missing:
        errors.append(f"implementation public definitions missing: {missing}")
    for token in (
        'FACTORED = "factored"',
        'UNRESOLVED = "unresolved"',
        "Fraction(7, 12)",
        "Fraction(11, 12)",
        'raise AssertionError("splitter returned an invalid factor")',
    ):
        if token not in text:
            errors.append(f"implementation contract token missing: {token}")
    for banned in (
        "prime_factorization",
        "find_semismooth_witness",
        "find_semismooth_asymmetry_witness",
        "is_hereditarily_semismooth",
    ):
        if banned in text:
            errors.append(f"factor-aware oracle leaked into wrapper: {banned}")
    return errors


def validate_probability_arithmetic() -> list[str]:
    """Reconstruct the two exact geometric tails without project imports."""
    errors: list[str] = []
    prior_minus = Fraction(1)
    prior_plus = Fraction(1)
    for cycles in range(1, 65):
        minus = Fraction(7, 12) ** cycles
        plus = Fraction(11, 12) ** cycles
        if not 0 < minus < prior_minus:
            errors.append(f"semismooth tail is not decreasing at {cycles}")
        if not 0 < plus < prior_plus:
            errors.append(f"Lucas tail is not decreasing at {cycles}")
        prior_minus = minus
        prior_plus = plus
    if Fraction(1) - Fraction(5, 12) != Fraction(7, 12):
        errors.append("semismooth success complement mismatch")
    if Fraction(1) - Fraction(1, 12) != Fraction(11, 12):
        errors.append("Lucas success complement mismatch")
    return errors


def validate_proof(text: str) -> list[str]:
    """Check the totality, recursion, and scope statements."""
    errors: list[str] = []
    flat = " ".join(text.split())
    for token in (
        "Totality and no-wrong-factor theorem",
        "fewer than \\(4m\\) total invocations",
        "\\left(\\frac7{12}\\right)^s",
        "\\left(\\frac{11}{12}\\right)^s",
        "does not assume that different recursive nodes are mutually independent",
        "Neither wrapper recognizes its hereditary promise",
        "no general classical polynomial-time factoring theorem",
    ):
        if token not in flat:
            errors.append(f"proof contract token missing: {token}")
    return errors


def validate_claims(text: str) -> list[str]:
    """Check both existing theorem rows received the bounded corollary."""
    errors: list[str] = []
    for claim_id, tail in (("THM-001", "(7/12)^s"), ("THM-002", "(11/12)^s")):
        rows = [
            line
            for line in text.splitlines()
            if line.startswith(f"| {claim_id} | PROVED |")
        ]
        if len(rows) != 1:
            errors.append(f"{claim_id} ledger row missing or duplicated")
            continue
        row = rows[0]
        for token in ("UNRESOLVED", tail, "4m", "never returns a wrong"):
            if token not in row:
                errors.append(f"{claim_id} bounded token missing: {token}")
    return errors


def validate_paper(path: Path, text: str) -> list[str]:
    """Check synchronized M84 bounds and interpretation in one manuscript."""
    errors: list[str] = []
    for token in (
        "M84",
        "UNRESOLVED",
        "\\frac7{12}",
        "\\frac{11}{12}",
        "4m",
    ):
        if token not in text:
            errors.append(f"{path.relative_to(ROOT).as_posix()} missing {token}")
    return errors


def validate() -> list[str]:
    """Run the complete no-import M84 consistency check."""
    errors = validate_probability_arithmetic()
    required = (IMPLEMENTATION, PROOF, REVIEW, CLAIMS, *PAPERS)
    for path in required:
        if not path.is_file():
            errors.append(f"required file missing: {path.relative_to(ROOT)}")
    if errors:
        return errors
    errors.extend(validate_implementation(IMPLEMENTATION.read_text(encoding="utf-8")))
    errors.extend(validate_proof(PROOF.read_text(encoding="utf-8")))
    errors.extend(validate_claims(CLAIMS.read_text(encoding="utf-8")))
    review = " ".join(REVIEW.read_text(encoding="utf-8").split())
    if "PASS for the M84 bounded theorem" not in review:
        errors.append("M84 adversarial review outcome missing")
    if "not an external peer review" not in review:
        errors.append("M84 review independence limitation missing")
    for paper in PAPERS:
        errors.extend(validate_paper(paper, paper.read_text(encoding="utf-8")))
    return errors


def main() -> int:
    """Report every contract failure with a nonzero exit status."""
    errors = validate()
    if errors:
        for error in errors:
            print(f"M84 total-wrapper check: FAIL: {error}", file=sys.stderr)
        return 1
    print(
        "M84 total-wrapper check: PASS "
        "(2 total wrappers, exact local tails, capped complete bounds)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
