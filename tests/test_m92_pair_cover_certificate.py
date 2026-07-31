"""Regression tests for the M92 pair-cover certificate theorem."""

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
CHECKER_PATH = ROOT / "scripts" / "check_m92_pair_cover_certificate.py"
GENERATOR_PATH = ROOT / "scripts" / "run_m92_pair_cover_audit.py"
M91_PATH = ROOT / "scripts" / "check_m91_all_rows_semantic_certificate.py"
SCHEMA_PATH = ROOT / "schemas" / "m92-pair-cover-certificates-v1.json"


def load_module(name: str, path: Path) -> ModuleType:
    """Load one repository script by path."""
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


CHECKER = load_module("check_m92_pair_cover", CHECKER_PATH)
GENERATOR = load_module("run_m92_pair_cover", GENERATOR_PATH)


def rehash(schema: dict[str, Any]) -> None:
    """Update a deliberately mutated schema's canonical hash."""
    schema["summary_sha256"] = CHECKER.canonical_hash(schema)


class M92PairCoverCertificateTests(unittest.TestCase):
    """Check the theorem application and adversarial mutations."""

    def setUp(self) -> None:
        self.schema = cast(
            dict[str, Any],
            json.loads(SCHEMA_PATH.read_text(encoding="utf-8")),
        )

    def test_registered_portfolio_passes(self) -> None:
        totals = CHECKER.validate_all(self.schema)
        self.assertEqual(totals["instance_count"], 9)
        self.assertEqual(totals["pair_count"], 41)
        self.assertEqual(totals["coverage_type_count"], 19)
        self.assertEqual(totals["minimum_coordinate_count"], 19)

    def test_generator_reproduces_registered_schema(self) -> None:
        self.assertEqual(GENERATOR.build_summary(), self.schema)

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
        self.assertLessEqual(len(source.splitlines()), 450)
        self.assertTrue(
            imported
            <= {
                "__future__",
                "collections",
                "hashlib",
                "itertools",
                "json",
                "math",
                "pathlib",
                "typing",
            }
        )

    def test_private_pairs_force_every_selected_type(self) -> None:
        for instance in self.schema["instances"]:
            type_count = len(instance["coverage_types"])
            self.assertEqual(
                len(instance["private_pair_lower_witness"]),
                type_count,
            )
            self.assertEqual(
                instance["upper_witness"],
                [f"T{index}" for index in range(type_count)],
            )

    def test_rehashed_coverage_mask_mutation_is_rejected(self) -> None:
        schema = copy.deepcopy(self.schema)
        schema["instances"][0]["coverage_types"][0]["coverage_mask_hex"] = "0"
        rehash(schema)
        with self.assertRaisesRegex(AssertionError, "coverage mask"):
            CHECKER.validate_all(schema)

    def test_rehashed_private_pair_mutation_is_rejected(self) -> None:
        schema = copy.deepcopy(self.schema)
        witness = schema["instances"][1]["private_pair_lower_witness"][0]
        witness["pair_index"] = 0
        witness["pair"] = schema["instances"][1]["collision_buckets"][0][:2]
        rehash(schema)
        with self.assertRaisesRegex(AssertionError, "not private"):
            CHECKER.validate_all(schema)

    def test_rehashed_upper_witness_mutation_is_rejected(self) -> None:
        schema = copy.deepcopy(self.schema)
        schema["instances"][4]["upper_witness"] = ["T0"]
        rehash(schema)
        with self.assertRaisesRegex(AssertionError, "uncovered pair"):
            CHECKER.validate_all(schema)

    def test_rehashed_source_path_mutation_is_rejected(self) -> None:
        schema = copy.deepcopy(self.schema)
        schema["instances"][0]["source_path"] = "schemas/other.json"
        rehash(schema)
        with self.assertRaisesRegex(AssertionError, "source path"):
            CHECKER.validate_all(schema)

    def test_rehashed_bucket_mutation_is_rejected(self) -> None:
        schema = copy.deepcopy(self.schema)
        schema["instances"][0]["collision_buckets"][0][0] = 7189
        rehash(schema)
        with self.assertRaisesRegex(AssertionError, "collision buckets"):
            CHECKER.validate_all(schema)

    def test_rehashed_cost_mutation_is_rejected(self) -> None:
        schema = copy.deepcopy(self.schema)
        schema["instances"][2]["verification_cost"][
            "private_type_tests"
        ] += 1
        rehash(schema)
        with self.assertRaisesRegex(AssertionError, "cost ledger"):
            CHECKER.validate_all(schema)

    def test_raw_coverage_types_differentially_match_m91(self) -> None:
        m91 = load_module("check_m91_for_m92", M91_PATH)
        for instance in self.schema["instances"]:
            buckets = tuple(
                tuple(int(prime) for prime in bucket)
                for bucket in instance["collision_buckets"]
            )
            tracked_primes = tuple(
                prime for bucket in buckets for prime in bucket
            )
            pairs = m91.pair_universe(buckets)
            raw_coverages, _evaluations = m91.all_new_coverages(
                int(instance["base_cap"]),
                int(instance["repair_cap"]),
                tracked_primes,
                pairs,
            )
            registered = {
                int(record["coverage_mask_hex"], 16)
                for record in instance["coverage_types"]
            }
            self.assertEqual(raw_coverages, registered)


if __name__ == "__main__":
    unittest.main()
