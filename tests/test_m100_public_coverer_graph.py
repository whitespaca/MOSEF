"""Regression and mutation tests for the M100 public graph audit."""

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
CHECKER_PATH = ROOT / "scripts" / "check_m100_public_coverer_graph.py"
GENERATOR_PATH = ROOT / "scripts" / "run_m100_public_coverer_graph_audit.py"
SCHEMA_PATH = ROOT / "schemas" / "m100-public-coverer-graph-v1.json"


def load_module(name: str, path: Path) -> ModuleType:
    """Load one repository script from its exact path."""
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


CHECKER = load_module("check_m100_public_coverer_graph", CHECKER_PATH)
GENERATOR = load_module("run_m100_public_coverer_graph_audit", GENERATOR_PATH)


def rehash(schema: dict[str, Any]) -> None:
    """Rehash one deliberately mutated schema."""
    schema["summary_sha256"] = CHECKER.canonical_hash(schema)


class M100PublicCovererGraphTests(unittest.TestCase):
    """Check public construction, cost boundaries, and mutations."""

    def setUp(self) -> None:
        self.schema = cast(
            dict[str, Any],
            json.loads(SCHEMA_PATH.read_text(encoding="utf-8")),
        )

    def test_registered_portfolio_passes(self) -> None:
        self.assertEqual(
            CHECKER.validate_all(self.schema),
            {
                "instance_count": 19,
                "population_size": 12209,
                "population_label_bits": 193753,
                "selected_coordinate_count": 421541,
                "selected_certificate_evaluations": 39426052,
                "baseline_persistence_descriptor_evaluations": 5253406,
                "baseline_persistence_primitive_tests": 42027248,
                "tracked_point_count": 55,
                "pair_count": 64,
                "new_descriptor_count": 152879,
                "new_descriptor_prime_evaluations": 581361,
                "primitive_coordinate_tests": 4650888,
                "complete_type_count": 37,
                "forced_type_count": 30,
                "residual_vertex_count": 7,
                "residual_edge_count": 9,
                "public_oct_cap": 96,
                "exact_oct_number": 3,
                "graph_payload_bits": 1063,
                "maximum_exact_oct_number": 2,
                "all_public_caps_accepted": True,
            },
        )

    def test_generator_reproduces_schema(self) -> None:
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
        self.assertLessEqual(len(source.splitlines()), 1100)
        self.assertNotIn("run_m100", source)
        self.assertTrue(
            imported
            <= {
                "__future__",
                "collections",
                "functools",
                "hashlib",
                "itertools",
                "json",
                "math",
                "pathlib",
                "typing",
            }
        )

    def test_public_oct_schedule_is_not_row_advice(self) -> None:
        for record in self.schema["instances"]:
            input_length = record["input_length"]
            self.assertEqual(
                record["public_oct_cap"],
                (input_length - 1).bit_length(),
            )
            self.assertLessEqual(
                record["exact_oct_number"],
                record["public_oct_cap"],
            )

    def test_early_public_type_enumeration_matches_m93(self) -> None:
        early = [
            record
            for record in self.schema["instances"]
            if record["source_id"] == "M93"
        ]
        self.assertEqual(sum(row["new_descriptor_count"] for row in early), 7398)
        self.assertEqual(
            sum(row["new_descriptor_prime_evaluations"] for row in early),
            19365,
        )
        self.assertEqual(
            sum(row["primitive_coordinate_tests"] for row in early),
            154920,
        )
        self.assertEqual(sum(row["complete_type_count"] for row in early), 18)

    def test_late_public_type_enumeration_matches_m92(self) -> None:
        late = [
            record
            for record in self.schema["instances"]
            if record["source_id"] == "M92"
        ]
        self.assertEqual(
            sum(row["new_descriptor_count"] for row in late),
            145481,
        )
        self.assertEqual(
            sum(row["primitive_coordinate_tests"] for row in late),
            4495968,
        )
        self.assertEqual(sum(row["complete_type_count"] for row in late), 19)

    def test_only_two_residual_graphs_need_nonzero_oct(self) -> None:
        nonzero = [
            (
                record["input_length"],
                record["residual_vertex_count"],
                record["residual_edge_count"],
                record["exact_oct_number"],
            )
            for record in self.schema["instances"]
            if record["exact_oct_number"]
        ]
        self.assertEqual(nonzero, [(16, 3, 3, 1), (24, 4, 6, 2)])

    def test_baseline_blocks_and_graph_are_materialized(self) -> None:
        modes = {
            record["baseline_partition_mode"]
            for record in self.schema["instances"]
        }
        self.assertEqual(
            modes,
            {
                "selected-subfamily-plus-raw-persistence",
                "full-raw-family-refinement",
            },
        )
        for record in self.schema["instances"]:
            self.assertTrue(record["baseline_collision_buckets"])
            self.assertEqual(
                len(record["coverage_types"]),
                record["complete_type_count"],
            )
            self.assertEqual(
                len(record["coverer_sets"]),
                record["pair_count"],
            )
            self.assertEqual(
                len(record["forced_type_ids"]),
                record["forced_type_count"],
            )
            self.assertEqual(
                len(record["residual_edges"]),
                record["residual_edge_count"],
            )

    def test_hash_only_counterexample_changes_the_minimum(self) -> None:
        counterexample = self.schema["hash_only_counterexample"]
        CHECKER.validate_counterexample(counterexample)
        self.assertEqual(
            counterexample["claimed_payload"]["claimed_exact_cover_number"],
            2,
        )
        self.assertEqual(counterexample["actual_exact_cover_number"], 1)

    def test_rehashed_source_mutation_is_rejected(self) -> None:
        schema = copy.deepcopy(self.schema)
        schema["sources"][1]["file_sha256"] = "0" * 64
        rehash(schema)
        with self.assertRaisesRegex(AssertionError, "source registry"):
            CHECKER.validate_all(schema)

    def test_rehashed_contract_mutation_is_rejected(self) -> None:
        schema = copy.deepcopy(self.schema)
        schema["constructor_contract"]["forbidden_advice"].pop()
        rehash(schema)
        with self.assertRaisesRegex(AssertionError, "constructor contract"):
            CHECKER.validate_all(schema)

    def test_rehashed_cap_mutation_is_rejected(self) -> None:
        schema = copy.deepcopy(self.schema)
        schema["instances"][0]["base_cap"] += 1
        rehash(schema)
        with self.assertRaisesRegex(AssertionError, "cap interval"):
            CHECKER.validate_all(schema)

    def test_rehashed_type_mutation_is_rejected(self) -> None:
        schema = copy.deepcopy(self.schema)
        schema["instances"][0]["complete_coverage_masks_hex"][0] = "0"
        rehash(schema)
        with self.assertRaisesRegex(AssertionError, "instance ledger"):
            CHECKER.validate_all(schema)

    def test_rehashed_baseline_block_mutation_is_rejected(self) -> None:
        schema = copy.deepcopy(self.schema)
        schema["instances"][0]["baseline_collision_buckets"][0][0] += 2
        rehash(schema)
        with self.assertRaisesRegex(AssertionError, "instance ledger"):
            CHECKER.validate_all(schema)

    def test_rehashed_coverer_column_mutation_is_rejected(self) -> None:
        schema = copy.deepcopy(self.schema)
        schema["instances"][0]["coverer_sets"][0][
            "coverer_type_ids"
        ].append("T1")
        rehash(schema)
        with self.assertRaisesRegex(AssertionError, "instance ledger"):
            CHECKER.validate_all(schema)

    def test_rehashed_oct_mutation_is_rejected(self) -> None:
        schema = copy.deepcopy(self.schema)
        schema["instances"][0]["exact_oct_number"] += 1
        rehash(schema)
        with self.assertRaisesRegex(AssertionError, "instance ledger"):
            CHECKER.validate_all(schema)

    def test_rehashed_hash_counterexample_mutation_is_rejected(self) -> None:
        schema = copy.deepcopy(self.schema)
        schema["hash_only_counterexample"]["actual_exact_cover_number"] = 2
        rehash(schema)
        with self.assertRaisesRegex(AssertionError, "minimum"):
            CHECKER.validate_all(schema)

    def test_rehashed_boundary_mutation_is_rejected(self) -> None:
        schema = copy.deepcopy(self.schema)
        schema["boundary"]["registered_path_is_polynomial_in_m"] = True
        rehash(schema)
        with self.assertRaisesRegex(AssertionError, "boundary"):
            CHECKER.validate_all(schema)

    def test_rehashed_scope_mutation_is_rejected(self) -> None:
        schema = copy.deepcopy(self.schema)
        schema["scope"]["not_claimed"].pop()
        rehash(schema)
        with self.assertRaisesRegex(AssertionError, "scope"):
            CHECKER.validate_all(schema)


if __name__ == "__main__":
    unittest.main()
