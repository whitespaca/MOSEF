"""Regression tests for the M89 focused-paper appendix boundary."""

from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path
from types import ModuleType

ROOT = Path(__file__).resolve().parents[1]
CHECKER_PATH = ROOT / "scripts" / "check_m89_appendix_boundaries.py"


def load_checker() -> ModuleType:
    """Load the standalone M89 checker."""
    spec = importlib.util.spec_from_file_location(
        "check_m89_appendices",
        CHECKER_PATH,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {CHECKER_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


CHECKER = load_checker()


class M89AppendixBoundaryTests(unittest.TestCase):
    """Keep mathematical narrative separate from audit machinery."""

    def setUp(self) -> None:
        self.promise_en = (
            ROOT / "paper" / "focused" / "promise-factorization-en.tex"
        ).read_text(encoding="utf-8")
        self.promise_ko = (
            ROOT / "paper" / "focused" / "promise-factorization-ko.tex"
        ).read_text(encoding="utf-8")

    def test_current_appendix_boundaries_pass(self) -> None:
        reports = CHECKER.validate_all()
        self.assertEqual(len(reports), 6)
        self.assertEqual(sum(report.main_sections for report in reports), 34)
        self.assertEqual(
            sum(report.appendix_sections for report in reports),
            12,
        )
        self.assertEqual(sum(report.commands for report in reports), 54)
        self.assertEqual(sum(report.paths for report in reports), 38)
        self.assertEqual(sum(report.citations for report in reports), 14)

    def test_missing_appendix_boundary_is_rejected(self) -> None:
        mutated = self.promise_en.replace(r"\appendix", "", 1)
        with self.assertRaisesRegex(AssertionError, "boundary count changed"):
            CHECKER.validate_paper_text(
                "promise-factorization",
                "en",
                mutated,
            )

    def test_command_in_main_is_rejected(self) -> None:
        mutated = self.promise_en.replace(
            r"\appendix",
            "python scripts/unreviewed.py\n\\appendix",
            1,
        )
        with self.assertRaisesRegex(AssertionError, "verbatim|main|command"):
            CHECKER.validate_paper_text(
                "promise-factorization",
                "en",
                mutated,
            )

    def test_archive_path_in_main_is_rejected(self) -> None:
        mutated = self.promise_en.replace(
            r"\appendix",
            "\\path{research/leaked.md}\n\\appendix",
            1,
        )
        with self.assertRaisesRegex(AssertionError, "repository path"):
            CHECKER.validate_paper_text(
                "promise-factorization",
                "en",
                mutated,
            )

    def test_milestone_id_in_main_is_rejected(self) -> None:
        mutated = self.promise_en.replace(
            r"\appendix",
            "M89 internal chronology\n\\appendix",
            1,
        )
        with self.assertRaisesRegex(AssertionError, "milestone ID"):
            CHECKER.validate_paper_text(
                "promise-factorization",
                "en",
                mutated,
            )

    def test_main_section_reordering_is_rejected(self) -> None:
        mutated = self.promise_en.replace(
            r"\section{Scope and model}",
            r"\section{TMP}",
            1,
        ).replace(
            r"\section{Coverage is not separation}",
            r"\section{Scope and model}",
            1,
        ).replace(
            r"\section{TMP}",
            r"\section{Coverage is not separation}",
            1,
        )
        with self.assertRaisesRegex(AssertionError, "main section order"):
            CHECKER.validate_paper_text(
                "promise-factorization",
                "en",
                mutated,
            )

    def test_claim_moved_to_appendix_is_rejected(self) -> None:
        claim = r"\claimstatus{THM-001}{PROVED}"
        mutated = self.promise_en.replace(claim, "", 1).replace(
            r"\appendix",
            "\\appendix\n" + claim,
            1,
        )
        with self.assertRaisesRegex(AssertionError, "claim placement"):
            CHECKER.validate_paper_text(
                "promise-factorization",
                "en",
                mutated,
            )

    def test_command_anchor_loss_is_rejected(self) -> None:
        mutated = self.promise_en.replace(
            "python scripts/run_m3_semismooth_search.py\n",
            "",
            1,
        )
        with self.assertRaisesRegex(AssertionError, "command anchors"):
            CHECKER.validate_paper_text(
                "promise-factorization",
                "en",
                mutated,
            )

    def test_path_anchor_loss_is_rejected(self) -> None:
        mutated = self.promise_en.replace(
            r"\path{research/NEGATIVE_RESULTS.md}",
            r"\path{research/REMOVED.md}",
            1,
        )
        with self.assertRaisesRegex(AssertionError, "archive paths"):
            CHECKER.validate_paper_text(
                "promise-factorization",
                "en",
                mutated,
            )

    def test_source_anchor_loss_is_rejected(self) -> None:
        mutated = self.promise_en.replace(
            r"\cite{pollard1974theorems}",
            r"\cite{uninspected-source}",
            1,
        )
        with self.assertRaisesRegex(AssertionError, "source anchors"):
            CHECKER.validate_paper_text(
                "promise-factorization",
                "en",
                mutated,
            )

    def test_limitation_anchor_loss_is_rejected(self) -> None:
        mutated = self.promise_en.replace(
            "general classical polynomial-time factorization",
            "the general problem is solved",
            1,
        )
        with self.assertRaisesRegex(AssertionError, "limitation anchor"):
            CHECKER.validate_paper_text(
                "promise-factorization",
                "en",
                mutated,
            )

    def test_bilingual_path_drift_is_rejected(self) -> None:
        mutated = self.promise_ko.replace(
            r"\path{research/NEGATIVE_RESULTS.md}",
            r"\path{research/OTHER.md}",
            1,
        )
        with self.assertRaisesRegex(AssertionError, "archive paths|bilingual"):
            CHECKER.validate_pair(
                "promise-factorization",
                self.promise_en,
                mutated,
            )


if __name__ == "__main__":
    unittest.main()
