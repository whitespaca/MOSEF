"""Regression tests for the M82 bilingual paper portfolio."""

from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path
from types import ModuleType
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def load_checker() -> ModuleType:
    """Load the independent checker without making scripts a package."""
    path = ROOT / "scripts" / "check_m82_paper_portfolio.py"
    spec = importlib.util.spec_from_file_location("check_m82_portfolio", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load M82 checker")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


CHECKER = load_checker()


class PaperPortfolioTests(unittest.TestCase):
    """Check valid projection and important mutation paths."""

    def setUp(self) -> None:
        self.manifest: dict[str, Any] = json.loads(
            CHECKER.MANIFEST.read_text(encoding="utf-8")
        )

    def test_registered_portfolio_passes(self) -> None:
        self.assertEqual(CHECKER.validate(), [])

    def test_duplicate_claim_is_rejected(self) -> None:
        paper = self.manifest["papers"][0]
        english = (ROOT / paper["english"]).read_text(encoding="utf-8")
        korean = (ROOT / paper["korean"]).read_text(encoding="utf-8")
        first = paper["claim_statuses"][0]
        duplicate = (
            f"\\claimstatus{{{first['claim_id']}}}{{{first['status']}}}."
        )
        expected = [
            (row["claim_id"], row["status"]) for row in paper["claim_statuses"]
        ]
        errors = CHECKER.validate_paper_pair(
            english + duplicate, korean, expected, paper["id"]
        )
        self.assertTrue(any("duplicate claim ID" in error for error in errors))

    def test_status_mismatch_is_rejected(self) -> None:
        paper = self.manifest["papers"][1]
        english = (ROOT / paper["english"]).read_text(encoding="utf-8")
        korean = (ROOT / paper["korean"]).read_text(encoding="utf-8")
        expected = [
            (row["claim_id"], row["status"]) for row in paper["claim_statuses"]
        ]
        altered = english.replace("{BAR-018}{PROVED}", "{BAR-018}{OPEN}", 1)
        errors = CHECKER.validate_paper_pair(
            altered, korean, expected, paper["id"]
        )
        self.assertTrue(any("claim order/status mismatch" in error for error in errors))

    def test_missing_korean_scope_marker_is_rejected(self) -> None:
        paper = self.manifest["papers"][2]
        english = (ROOT / paper["english"]).read_text(encoding="utf-8")
        korean = (ROOT / paper["korean"]).read_text(encoding="utf-8")
        expected = [
            (row["claim_id"], row["status"]) for row in paper["claim_statuses"]
        ]
        altered = korean.replace("일반", "범용")
        errors = CHECKER.validate_paper_pair(
            english, altered, expected, paper["id"]
        )
        self.assertTrue(any("scope marker missing" in error for error in errors))

    def test_summary_hash_tamper_is_rejected(self) -> None:
        altered = json.loads(json.dumps(self.manifest))
        altered["portfolio_summary_sha256"] = "0" * 64
        errors = CHECKER.validate_manifest(altered)
        self.assertIn("portfolio summary hash mismatch", errors)

    def test_authoritative_ledger_substitution_is_rejected(self) -> None:
        altered = json.loads(json.dumps(self.manifest))
        altered["archive"]["claim_ledger"] = "paper/main.tex"
        summary_input = dict(altered)
        summary_input.pop("portfolio_summary_sha256")
        altered["portfolio_summary_sha256"] = CHECKER.canonical_hash(summary_input)
        errors = CHECKER.validate_manifest(altered)
        self.assertIn("authoritative archive path mismatch", errors)

    def test_source_hash_omission_is_rejected(self) -> None:
        altered = json.loads(json.dumps(self.manifest))
        altered["source_sha256"].pop("paper/focused/preamble-ko.tex")
        summary_input = dict(altered)
        summary_input.pop("portfolio_summary_sha256")
        altered["portfolio_summary_sha256"] = CHECKER.canonical_hash(summary_input)
        errors = CHECKER.validate_manifest(altered)
        self.assertIn("source hash path set mismatch", errors)


if __name__ == "__main__":
    unittest.main()
