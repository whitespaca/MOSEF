"""Regression and mutation tests for the M96 matching certificates."""

from __future__ import annotations

import ast
import copy
import importlib.util
import json
import sys
import unittest
from pathlib import Path
from types import ModuleType
from typing import Any, cast

ROOT = Path(__file__).resolve().parents[1]
CHECKER_PATH = ROOT / "scripts" / "check_m96_matching_certificate.py"
GENERATOR_PATH = ROOT / "scripts" / "run_m96_matching_certificate_profile.py"
SCHEMA_PATH = ROOT / "schemas" / "m96-matching-certificates-v1.json"


def load_module(name: str, path: Path) -> ModuleType:
    """Load one repository script from its exact path."""
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


CHECKER = load_module("check_m96_matching_certificate", CHECKER_PATH)
GENERATOR = load_module("run_m96_matching_certificate", GENERATOR_PATH)


def rehash(schema: dict[str, Any]) -> None:
    """Rehash one deliberately mutated schema."""
    schema["summary_sha256"] = CHECKER.canonical_hash(schema)


class M96MatchingCertificateTests(unittest.TestCase):
    """Check matching equality, gaps, source binding, and mutations."""

    def setUp(self) -> None:
        self.schema = cast(
            dict[str, Any],
            json.loads(SCHEMA_PATH.read_text(encoding="utf-8")),
        )

    def test_registered_portfolio_passes(self) -> None:
        totals = CHECKER.validate_all(self.schema)
        self.assertEqual(
            totals,
            {
                "perturbation_count": 8,
                "matching_equality_count": 5,
                "matching_gap_count": 3,
                "residual_vertex_cover_number_sum": 12,
                "residual_matching_number_sum": 9,
                "exact_repair_number_sum": 28,
                "matching_certificate_payload_bits": 43,
                "matching_certificate_verification_tests": 21,
                "maximum_matching_gap": 1,
            },
        )

    def test_generator_reproduces_registered_schema(self) -> None:
        self.assertEqual(GENERATOR.build_summary(), self.schema)

    def test_checker_is_independent_and_standard_library_only(self) -> None:
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
        self.assertLessEqual(len(source.splitlines()), 500)
        self.assertNotIn("run_m96", source)
        self.assertNotIn("check_m95", source)
        self.assertTrue(
            imported
            <= {
                "__future__",
                "collections",
                "hashlib",
                "itertools",
                "json",
                "pathlib",
                "typing",
            }
        )

    def test_all_registered_systems_are_non_templates(self) -> None:
        self.assertTrue(
            all(
                record["complete_normal_form"]
                and not record["m95_template"]
                for record in self.schema["perturbations"]
            )
        )

    def test_equality_witnesses_are_exact_without_subset_payload(self) -> None:
        tight = [
            record
            for record in self.schema["perturbations"]
            if record["matching_equality"]
        ]
        self.assertEqual(len(tight), 5)
        for record in tight:
            self.assertEqual(
                len(record["minimum_cover_type_ids"]),
                len(record["maximum_matching_column_indices"]),
            )
            self.assertEqual(
                record["matching_certificate"]["status"],
                "exact",
            )

    def test_matching_gap_counterexamples_are_preserved(self) -> None:
        gaps = [
            (
                record["perturbation_id"],
                record["residual_vertex_cover_number"],
                record["residual_matching_number"],
            )
            for record in self.schema["perturbations"]
            if not record["matching_equality"]
        ]
        self.assertEqual(
            gaps,
            [
                ("U3-keep-edges", 2, 1),
                ("U4-keep-edges", 3, 2),
                ("U5-drop-e01", 3, 2),
            ],
        )

    def test_seed_slots_are_the_frozen_looped_k5(self) -> None:
        slots = [
            tuple(record["coverer_type_ids"])
            for record in self.schema["seed"]["slots"]
        ]
        self.assertEqual(len(slots), 15)
        self.assertEqual(sum(len(slot) == 1 for slot in slots), 5)
        self.assertEqual(sum(len(slot) == 2 for slot in slots), 10)

    def test_rehashed_source_anchor_mutation_is_rejected(self) -> None:
        schema = copy.deepcopy(self.schema)
        schema["source"]["file_sha256"] = "0" * 64
        rehash(schema)
        with self.assertRaisesRegex(AssertionError, "source anchor"):
            CHECKER.validate_all(schema)

    def test_rehashed_grammar_mutation_is_rejected(self) -> None:
        schema = copy.deepcopy(self.schema)
        schema["perturbation_grammar"]["registered_parameters"].pop()
        rehash(schema)
        with self.assertRaisesRegex(AssertionError, "grammar"):
            CHECKER.validate_all(schema)

    def test_rehashed_deleted_loop_mutation_is_rejected(self) -> None:
        schema = copy.deepcopy(self.schema)
        schema["perturbations"][0]["deleted_loop_column_indices"] = []
        rehash(schema)
        with self.assertRaisesRegex(AssertionError, "deleted_loop"):
            CHECKER.validate_all(schema)

    def test_rehashed_cover_witness_mutation_is_rejected(self) -> None:
        schema = copy.deepcopy(self.schema)
        schema["perturbations"][1]["minimum_cover_type_ids"] = ["T1"]
        rehash(schema)
        with self.assertRaisesRegex(AssertionError, "cover witness"):
            CHECKER.validate_all(schema)

    def test_rehashed_matching_witness_mutation_is_rejected(self) -> None:
        schema = copy.deepcopy(self.schema)
        schema["perturbations"][6][
            "maximum_matching_column_indices"
        ] = [2]
        rehash(schema)
        with self.assertRaisesRegex(AssertionError, "matching witness"):
            CHECKER.validate_all(schema)

    def test_rehashed_cost_mutation_is_rejected(self) -> None:
        schema = copy.deepcopy(self.schema)
        schema["perturbations"][6]["matching_certificate"][
            "payload_bits"
        ] += 1
        rehash(schema)
        with self.assertRaisesRegex(AssertionError, "certificate cost"):
            CHECKER.validate_all(schema)

    def test_rehashed_gap_mutation_is_rejected(self) -> None:
        schema = copy.deepcopy(self.schema)
        schema["perturbations"][3]["matching_gap"] = 0
        rehash(schema)
        with self.assertRaisesRegex(AssertionError, "matching_gap"):
            CHECKER.validate_all(schema)

    def test_rehashed_scope_mutation_is_rejected(self) -> None:
        schema = copy.deepcopy(self.schema)
        schema["scope"]["not_claimed"].pop()
        rehash(schema)
        with self.assertRaisesRegex(AssertionError, "scope boundary"):
            CHECKER.validate_all(schema)


if __name__ == "__main__":
    unittest.main()
