"""Regression tests for the M88 reader-facing claim-label gate."""

from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path
from types import ModuleType

ROOT = Path(__file__).resolve().parents[1]
CHECKER_PATH = ROOT / "scripts" / "check_m88_reader_labels.py"


def load_checker() -> ModuleType:
    """Load the standalone M88 checker."""
    spec = importlib.util.spec_from_file_location("check_m88_labels", CHECKER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {CHECKER_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


CHECKER = load_checker()


class M88ReaderLabelTests(unittest.TestCase):
    """Check readable labels without weakening stable metadata."""

    def setUp(self) -> None:
        self.promise_en = (
            ROOT / "paper" / "focused" / "promise-factorization-en.tex"
        ).read_text(encoding="utf-8")
        self.promise_ko = (
            ROOT / "paper" / "focused" / "promise-factorization-ko.tex"
        ).read_text(encoding="utf-8")
        self.preamble_en = (
            ROOT / "paper" / "focused" / "preamble-en.tex"
        ).read_text(encoding="utf-8")

    def test_current_reader_labels_pass(self) -> None:
        reports = CHECKER.validate_all()
        self.assertEqual(len(reports), 6)
        self.assertEqual(sum(len(report.claim_ids) for report in reports), 42)
        self.assertEqual(
            {kind for report in reports for kind in report.kinds},
            {
                "Theorem",
                "Counterexample and criterion",
                "Proposition",
                "Barrier",
                "Finite certificate",
                "정리",
                "반례와 판정",
                "명제",
                "장벽",
                "유한 인증서",
            },
        )

    def test_missing_reader_macro_is_rejected(self) -> None:
        mutated = self.preamble_en.replace(
            r"\newcommand{\readerclaim}[3]",
            r"\newcommand{\readerclaiX}[3]",
            1,
        )
        with self.assertRaisesRegex(AssertionError, "macro count changed"):
            CHECKER.validate_preamble("en", mutated)

    def test_unwrapped_claim_is_rejected(self) -> None:
        mutated = self.promise_en.replace(
            r"\readerclaim{Theorem}{Hereditary \(p-1\) complete factorization}"
            "\n",
            "",
            1,
        )
        with self.assertRaisesRegex(AssertionError, "unwrapped or malformed"):
            CHECKER.validate_paper_text(
                "promise-factorization",
                "en",
                mutated,
            )

    def test_reader_kind_drift_is_rejected(self) -> None:
        mutated = self.promise_en.replace(
            r"\readerclaim{Theorem}",
            r"\readerclaim{Conjecture}",
            1,
        )
        with self.assertRaisesRegex(AssertionError, "reader label drifted"):
            CHECKER.validate_paper_text(
                "promise-factorization",
                "en",
                mutated,
            )

    def test_reader_title_drift_is_rejected(self) -> None:
        mutated = self.promise_en.replace(
            r"{Hereditary \(p-1\) complete factorization}",
            r"{General integer factorization}",
            1,
        )
        with self.assertRaisesRegex(AssertionError, "reader label drifted"):
            CHECKER.validate_paper_text(
                "promise-factorization",
                "en",
                mutated,
            )

    def test_claim_id_drift_is_rejected(self) -> None:
        mutated = self.promise_en.replace(
            r"\claimstatus{THM-001}{PROVED}",
            r"\claimstatus{THM-099}{PROVED}",
            1,
        )
        with self.assertRaisesRegex(AssertionError, "claim order drifted"):
            CHECKER.validate_paper_text(
                "promise-factorization",
                "en",
                mutated,
            )

    def test_status_drift_is_rejected(self) -> None:
        mutated = self.promise_en.replace(
            r"\claimstatus{THM-001}{PROVED}",
            r"\claimstatus{THM-001}{CONJECTURE}",
            1,
        )
        with self.assertRaisesRegex(AssertionError, "status drifted"):
            CHECKER.validate_paper_text(
                "promise-factorization",
                "en",
                mutated,
            )

    def test_claim_reordering_is_rejected(self) -> None:
        mutated = self.promise_en.replace(
            r"\claimstatus{THM-001}{PROVED}",
            r"\claimstatus{TMP-999}{PROVED}",
            1,
        ).replace(
            r"\claimstatus{BAR-001}{PROVED}",
            r"\claimstatus{THM-001}{PROVED}",
            1,
        ).replace(
            r"\claimstatus{TMP-999}{PROVED}",
            r"\claimstatus{BAR-001}{PROVED}",
            1,
        )
        with self.assertRaisesRegex(AssertionError, "claim order drifted"):
            CHECKER.validate_paper_text(
                "promise-factorization",
                "en",
                mutated,
            )

    def test_korean_label_drift_is_rejected(self) -> None:
        mutated = self.promise_ko.replace(
            r"\readerclaim{정리}{유전적 \(p-1\) 완전 인수분해}",
            r"\readerclaim{추측}{유전적 \(p-1\) 완전 인수분해}",
            1,
        )
        with self.assertRaisesRegex(AssertionError, "reader label drifted"):
            CHECKER.validate_pair(
                "promise-factorization",
                self.promise_en,
                mutated,
            )


if __name__ == "__main__":
    unittest.main()
