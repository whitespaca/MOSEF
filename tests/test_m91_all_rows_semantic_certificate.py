"""Regression tests for the M91 table-wide clean-room checker."""

from __future__ import annotations

import ast
import copy
import importlib.util
import json
import sys
import unittest
from pathlib import Path
from types import ModuleType
from typing import Any, ClassVar, cast

ROOT = Path(__file__).resolve().parents[1]
CHECKER_PATH = (
    ROOT / "scripts" / "check_m91_all_rows_semantic_certificate.py"
)


def load_checker() -> ModuleType:
    """Load the standalone checker without importing project packages."""
    spec = importlib.util.spec_from_file_location("check_m91_all_rows", CHECKER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {CHECKER_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


CHECKER = load_checker()


class M91AllRowsSemanticTests(unittest.TestCase):
    """Exercise the complete reconstruction and focused mutation paths."""

    summary: ClassVar[dict[str, Any]]
    report: ClassVar[Any]

    @classmethod
    def setUpClass(cls) -> None:
        cls.summary = json.loads(
            (
                ROOT / "schemas" / "m50-finite-threshold-summary-v1.json"
            ).read_text(encoding="utf-8")
        )
        cls.report = CHECKER.validate_all(cls.summary)

    def source_data(self, input_length: int) -> dict[str, Any]:
        """Load the source artifact selected by one M50 row."""
        row = self.summary["rows"][input_length - 9]
        return cast(
            dict[str, Any],
            json.loads(
                (ROOT / row["source_schema"]).read_text(encoding="utf-8")
            ),
        )

    def test_complete_reconstruction_passes(self) -> None:
        self.assertEqual(len(self.report.rows), 26)
        self.assertEqual(self.report.source_count, 16)
        self.assertEqual(
            [row.input_length for row in self.report.rows],
            list(range(9, 35)),
        )
        self.assertEqual(self.report.rows[-1].descriptor_count, 714400)

    def test_checker_is_standard_library_only_and_bounded(self) -> None:
        source = CHECKER_PATH.read_text(encoding="utf-8")
        tree = ast.parse(source)
        imported = {
            alias.name.split(".", 1)[0]
            for node in ast.walk(tree)
            if isinstance(node, ast.Import)
            for alias in node.names
        }
        imported.update(
            node.module.split(".", 1)[0]
            for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom) and node.module is not None
        )
        self.assertLessEqual(len(source.splitlines()), 1000)
        self.assertTrue(
            imported
            <= {
                "__future__",
                "collections",
                "hashlib",
                "json",
                "math",
                "pathlib",
                "time",
                "typing",
            }
        )

    def test_descriptor_count_formula_matches_endpoint_counts(self) -> None:
        self.assertEqual(CHECKER.selector_descriptor_count(9), 32)
        self.assertEqual(CHECKER.selector_descriptor_count(102), 89789)
        self.assertEqual(CHECKER.selector_descriptor_count(201), 714400)
        self.assertEqual(
            CHECKER.selector_descriptor_count(40),
            sum(1 for _descriptor in CHECKER.iter_selector_descriptors(40)),
        )

    def test_balanced_population_endpoints_are_reconstructed(self) -> None:
        self.assertEqual(CHECKER.balanced_prime_population(9), (17, 19))
        population = CHECKER.balanced_prime_population(34)
        self.assertEqual(len(population), 3299)
        self.assertEqual(population[0], 92683)
        self.assertEqual(population[-1], 131071)

    def test_simple_root_derivative_branch_matches_exact_quotient(self) -> None:
        descriptor = CHECKER.Descriptor("phi4", 3, 7, 2)
        self.assertEqual(CHECKER.cyclotomic_residue(descriptor, 5), 0)
        first_stage = sum(2**index for index in range(3))
        nested_base = 2**3
        second_stage = sum(nested_base**index for index in range(7))
        exact, remainder = divmod(first_stage + second_stage, 2**2 + 1)
        self.assertEqual(remainder, 0)
        self.assertEqual(CHECKER.cofactor_residue(descriptor, 5), exact % 5)

    def test_noncanonical_source_is_rejected(self) -> None:
        with self.assertRaisesRegex(AssertionError, "noncanonical"):
            CHECKER.parse_source("phi4:3:7:2", 9)
        with self.assertRaisesRegex(AssertionError, "outside"):
            CHECKER.parse_source("phi4:3:7:10:cofactor", 9)

    def test_rehashed_packed_signature_mutation_is_rejected(self) -> None:
        row = copy.deepcopy(self.summary["rows"][0])
        data = self.source_data(9)
        data["construction_certificates"][0]["restricted_signatures"][0] ^= 1
        with self.assertRaisesRegex(AssertionError, "packed signatures"):
            CHECKER.validate_one_row(row, data)

    def test_consistent_but_false_predecessor_mutation_is_rejected(self) -> None:
        row = copy.deepcopy(self.summary["rows"][7])
        data = self.source_data(16)
        false_buckets = [[191, 227]]
        row["predecessor_collision_buckets"] = false_buckets
        data["threshold_records"][0]["predecessor_collision_buckets"] = (
            false_buckets
        )
        with self.assertRaisesRegex(AssertionError, "raw predecessor"):
            CHECKER.validate_one_row(row, data)

    def test_rehashed_exhaustive_repair_pattern_mutation_is_rejected(self) -> None:
        row = copy.deepcopy(self.summary["rows"][17])
        data = self.source_data(26)
        patterns = data["construction_certificate"][
            "new_source_patterns_on_final_collision"
        ]
        patterns[0] = [1, 1, 1]
        with self.assertRaisesRegex(AssertionError, "repair patterns"):
            CHECKER.validate_one_row(row, data)

    def test_rehashed_source_path_mutation_is_rejected(self) -> None:
        summary = copy.deepcopy(self.summary)
        summary["sources"][0]["path"] = "schemas/not-a-source.json"
        summary["summary_sha256"] = CHECKER.canonical_hash(summary)
        with self.assertRaisesRegex(AssertionError, "source order or path"):
            CHECKER.validate_all(summary)

    def test_m50_cap_projection_mutation_is_rejected(self) -> None:
        row = copy.deepcopy(self.summary["rows"][20])
        row["family_relative_minimal_cap"] = 104
        with self.assertRaisesRegex(AssertionError, "M50 cap"):
            CHECKER.validate_one_row(row, self.source_data(29))


if __name__ == "__main__":
    unittest.main()
