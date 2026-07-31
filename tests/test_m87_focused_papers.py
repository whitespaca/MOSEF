"""Regression tests for the M87 focused-paper editorial gate."""

from __future__ import annotations

import importlib.util
import re
import sys
import unittest
from pathlib import Path
from types import ModuleType

ROOT = Path(__file__).resolve().parents[1]
CHECKER_PATH = ROOT / "scripts" / "check_m87_focused_papers.py"


def load_checker() -> ModuleType:
    """Load the standalone editorial checker."""
    spec = importlib.util.spec_from_file_location("check_m87_focused", CHECKER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {CHECKER_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


CHECKER = load_checker()


class M87FocusedPaperTests(unittest.TestCase):
    """Check word counts, cost boundaries, and claim parity."""

    def setUp(self) -> None:
        self.promise_en = (
            ROOT / "paper" / "focused" / "promise-factorization-en.tex"
        ).read_text(encoding="utf-8")
        self.promise_ko = (
            ROOT / "paper" / "focused" / "promise-factorization-ko.tex"
        ).read_text(encoding="utf-8")

    def test_current_focused_papers_pass(self) -> None:
        reports = CHECKER.validate_all()
        self.assertEqual(len(reports), 6)
        self.assertEqual(sum(report.cost_rows for report in reports), 24)
        self.assertEqual(
            {f"{report.paper_id}-{report.language}": report.abstract_words
             for report in reports},
            {
                "promise-factorization-en": 226,
                "promise-factorization-ko": 204,
                "cyclotomic-extraction-en": 231,
                "cyclotomic-extraction-ko": 200,
                "finite-certificates-en": 235,
                "finite-certificates-ko": 200,
            },
        )

    def test_math_expression_counts_as_one_token(self) -> None:
        self.assertEqual(
            CHECKER.abstract_tokens(r"alpha \(\min\{x,y\}\) beta"),
            ("alpha", "MATH", "beta"),
        )

    def test_short_abstract_is_rejected(self) -> None:
        mutated = re.sub(
            r"\\begin\{abstract\}.*?\\end\{abstract\}",
            "\\\\begin{abstract}\ntoo short\n\\\\end{abstract}",
            self.promise_en,
            count=1,
            flags=re.DOTALL,
        )
        with self.assertRaisesRegex(AssertionError, "abstract has 2 words"):
            CHECKER.validate_paper_text(
                "promise-factorization",
                "en",
                mutated,
            )

    def test_long_abstract_is_rejected(self) -> None:
        long_body = " ".join(["word"] * 301)
        mutated = re.sub(
            r"\\begin\{abstract\}.*?\\end\{abstract\}",
            f"\\\\begin{{abstract}}\n{long_body}\n\\\\end{{abstract}}",
            self.promise_en,
            count=1,
            flags=re.DOTALL,
        )
        with self.assertRaisesRegex(AssertionError, "abstract has 301 words"):
            CHECKER.validate_paper_text(
                "promise-factorization",
                "en",
                mutated,
            )

    def test_cost_label_drift_is_rejected(self) -> None:
        mutated = self.promise_en.replace(
            r"\costrow{Online charged}",
            r"\costrow{Online omitted}",
            1,
        )
        with self.assertRaisesRegex(AssertionError, "cost-model rows changed"):
            CHECKER.validate_paper_text(
                "promise-factorization",
                "en",
                mutated,
            )

    def test_empty_cost_row_is_rejected(self) -> None:
        mutated = self.promise_en.replace(
            r"\costrow{Not supplied}{Witness prime factors, a promise-membership bit, and"
            "\nfactor-dependent schedules are not inputs and are not inferred.}",
            r"\costrow{Not supplied}{}",
            1,
        )
        with self.assertRaisesRegex(AssertionError, "empty cost row"):
            CHECKER.validate_paper_text(
                "promise-factorization",
                "en",
                mutated,
            )

    def test_late_cost_model_is_rejected(self) -> None:
        start = self.promise_en.index(r"\begin{costmodel}")
        end = self.promise_en.index(r"\end{costmodel}", start) + len(
            r"\end{costmodel}"
        )
        cost_block = self.promise_en[start:end]
        without = self.promise_en[:start] + self.promise_en[end:]
        section_end = without.index("\n", without.index(r"\section{"))
        mutated = without[:section_end] + "\n" + cost_block + without[section_end:]
        with self.assertRaisesRegex(AssertionError, "not between abstract"):
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
        with self.assertRaisesRegex(AssertionError, "front-facing claims drifted"):
            CHECKER.validate_paper_text(
                "promise-factorization",
                "en",
                mutated,
            )

    def test_bilingual_status_drift_is_rejected(self) -> None:
        mutated_ko = self.promise_ko.replace(
            r"\claimstatus{THM-001}{PROVED}",
            r"\claimstatus{THM-001}{CONDITIONAL}",
            1,
        )
        with self.assertRaisesRegex(AssertionError, "claim status drifted"):
            CHECKER.validate_pair(
                "promise-factorization",
                self.promise_en,
                mutated_ko,
            )


if __name__ == "__main__":
    unittest.main()
