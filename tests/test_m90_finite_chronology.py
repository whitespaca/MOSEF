"""Regression tests for the M90 finite chronology boundary."""

from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path
from types import ModuleType

ROOT = Path(__file__).resolve().parents[1]
CHECKER_PATH = ROOT / "scripts" / "check_m90_finite_chronology.py"


def load_checker() -> ModuleType:
    """Load the standalone M90 checker."""
    spec = importlib.util.spec_from_file_location(
        "check_m90_chronology",
        CHECKER_PATH,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {CHECKER_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


CHECKER = load_checker()


class M90FiniteChronologyTests(unittest.TestCase):
    """Keep five representative cases in main and 26 rows in the appendix."""

    def setUp(self) -> None:
        self.paper_en = (
            ROOT / "paper" / "focused" / "finite-certificates-en.tex"
        ).read_text(encoding="utf-8")
        self.table_en = (
            ROOT / "paper" / "tables" / "finite-threshold-summary-en.tex"
        ).read_text(encoding="utf-8")
        self.table_ko = (
            ROOT / "paper" / "tables" / "finite-threshold-summary-ko.tex"
        ).read_text(encoding="utf-8")
        self.artifact = (
            ROOT / "schemas" / "m50-finite-threshold-summary-v1.json"
        ).read_text(encoding="utf-8")

    def test_current_chronology_boundary_passes(self) -> None:
        cases, rows = CHECKER.validate_all()
        self.assertEqual(cases, 5)
        self.assertEqual(rows, 26)

    def test_full_table_input_in_main_is_rejected(self) -> None:
        table_input = (
            r"\input{paper/tables/finite-threshold-summary-en.tex}"
        )
        mutated = self.paper_en.replace(table_input, "", 1).replace(
            r"\appendix",
            table_input + "\n\\appendix",
            1,
        )
        with self.assertRaisesRegex(AssertionError, "chronology remains in main"):
            CHECKER.validate_paper_text("en", mutated)

    def test_missing_appendix_table_input_is_rejected(self) -> None:
        mutated = self.paper_en.replace(
            r"\input{paper/tables/finite-threshold-summary-en.tex}",
            "",
            1,
        )
        with self.assertRaisesRegex(AssertionError, "chronology input drifted"):
            CHECKER.validate_paper_text("en", mutated)

    def test_chronology_subsection_reordering_is_rejected(self) -> None:
        first = r"\subsection{Complete 26-row threshold chronology}"
        second = r"\subsection{Artifact and semantic reproduction}"
        mutated = self.paper_en.replace(first, r"\subsection{TEMP}", 1)
        mutated = mutated.replace(second, first, 1)
        mutated = mutated.replace(r"\subsection{TEMP}", second, 1)
        with self.assertRaisesRegex(AssertionError, "subsection order"):
            CHECKER.validate_paper_text("en", mutated)

    def test_length_28_threshold_drift_is_rejected(self) -> None:
        mutated = self.paper_en.replace(
            r"\(L_{28}^\star=104\)",
            r"\(L_{28}^\star=105\)",
            1,
        )
        with self.assertRaisesRegex(AssertionError, "representative case"):
            CHECKER.validate_paper_text("en", mutated)

    def test_length_28_repair_count_drift_is_rejected(self) -> None:
        mutated = self.paper_en.replace(
            "five-coordinate subcertificate",
            "four-coordinate subcertificate",
            1,
        )
        with self.assertRaisesRegex(AssertionError, "representative case"):
            CHECKER.validate_paper_text("en", mutated)

    def test_claim_moved_to_appendix_is_rejected(self) -> None:
        claim = r"\claimstatus{THM-014}{PROVED}"
        mutated = self.paper_en.replace(claim, "", 1).replace(
            r"\appendix",
            "\\appendix\n" + claim,
            1,
        )
        with self.assertRaisesRegex(AssertionError, "claim placement"):
            CHECKER.validate_paper_text("en", mutated)

    def test_english_table_cap_drift_is_rejected(self) -> None:
        mutated = self.table_en.replace(
            "28 & 507 & 104 &",
            "28 & 507 & 105 &",
            1,
        )
        with self.assertRaisesRegex(
            AssertionError,
            "strict endpoint|table rows drifted",
        ):
            CHECKER.validate_table_text("en", mutated)

    def test_korean_table_collision_drift_is_rejected(self) -> None:
        mutated = self.table_ko.replace(
            r"\{97927,99527\}",
            r"\{97927,99529\}",
            1,
        )
        with self.assertRaisesRegex(AssertionError, "table rows drifted"):
            CHECKER.validate_table_text("ko", mutated)

    def test_table_endpoint_fraction_drift_is_rejected(self) -> None:
        mutated = self.table_en.replace(
            r"\(\frac{103}{28}\)",
            r"\(\frac{102}{28}\)",
            1,
        )
        with self.assertRaisesRegex(AssertionError, "strict endpoint"):
            CHECKER.validate_table_text("en", mutated)

    def test_table_repair_status_drift_is_rejected(self) -> None:
        mutated = self.table_en.replace(
            r"\{5011,5179\}\) & n.c.",
            r"\{5011,5179\}\) & --",
            1,
        )
        with self.assertRaisesRegex(AssertionError, "repair status"):
            CHECKER.validate_table_text("en", mutated)

    def test_frozen_artifact_cap_drift_is_rejected(self) -> None:
        mutated = self.artifact.replace(
            '"family_relative_minimal_cap": 201',
            '"family_relative_minimal_cap": 202',
            1,
        )
        with self.assertRaisesRegex(
            AssertionError,
            "strict endpoint|frozen M50",
        ):
            CHECKER.validate_artifact_text(mutated)

    def test_missing_table_row_is_rejected(self) -> None:
        row = next(
            line
            for line in self.table_en.splitlines(keepends=True)
            if line.startswith("21 & 57 & 33 &")
        )
        mutated = self.table_en.replace(row, "", 1)
        with self.assertRaisesRegex(AssertionError, "table rows drifted"):
            CHECKER.validate_table_text("en", mutated)


if __name__ == "__main__":
    unittest.main()
