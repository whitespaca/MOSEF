"""Regression and mutation tests for the M97 bipartite constructor."""

from __future__ import annotations

import ast
import copy
import importlib.util
import itertools
import json
import sys
import unittest
from pathlib import Path
from types import ModuleType
from typing import Any, cast

ROOT = Path(__file__).resolve().parents[1]
CHECKER_PATH = ROOT / "scripts" / "check_m97_bipartite_cover.py"
GENERATOR_PATH = ROOT / "scripts" / "run_m97_bipartite_cover_profile.py"
SCHEMA_PATH = ROOT / "schemas" / "m97-bipartite-cover-v1.json"


def load_module(name: str, path: Path) -> ModuleType:
    """Load one repository script from its exact path."""
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


CHECKER = load_module("check_m97_bipartite_cover", CHECKER_PATH)
GENERATOR = load_module("run_m97_bipartite_cover", GENERATOR_PATH)


def rehash(schema: dict[str, Any]) -> None:
    """Rehash one deliberately mutated schema."""
    schema["summary_sha256"] = CHECKER.canonical_hash(schema)


class M97BipartiteCoverTests(unittest.TestCase):
    """Check construction, nonbipartite boundaries, and mutations."""

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
                "case_count": 8,
                "bipartite_case_count": 6,
                "nonbipartite_case_count": 2,
                "constructed_exact_count": 6,
                "nonbipartite_equality_count": 1,
                "matching_gap_count": 1,
                "residual_vertex_cover_number_sum": 15,
                "residual_matching_number_sum": 14,
                "exact_repair_number_sum": 21,
                "constructed_output_payload_bits": 88,
                "constructed_output_verification_tests": 48,
                "augmentations": 10,
                "augmenting_path_searches": 16,
                "nonbipartite_equality_payload_bits": 17,
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
        self.assertLessEqual(len(source.splitlines()), 700)
        self.assertNotIn("run_m97", source)
        self.assertNotIn("check_m96", source)
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

    def test_all_targets_are_complete_non_templates(self) -> None:
        self.assertTrue(
            all(
                record["complete_normal_form"]
                and not record["m95_template"]
                for record in self.schema["cases"]
            )
        )

    def test_all_bipartite_cases_are_constructed_exactly(self) -> None:
        cases = [
            record for record in self.schema["cases"] if record["bipartite"]
        ]
        self.assertEqual(len(cases), 6)
        self.assertTrue(
            all(
                record["constructor"]["status"] == "constructed_exact"
                and len(record["constructor"]["minimum_cover_type_ids"])
                == len(
                    record["constructor"][
                        "maximum_matching_column_indices"
                    ]
                )
                for record in cases
            )
        )

    def test_nonbipartite_equality_is_preserved(self) -> None:
        record = self.schema["cases"][6]
        self.assertEqual(record["case_id"], "N1-triangle-pendant")
        self.assertFalse(record["bipartite"])
        self.assertTrue(record["exact_audit"]["matching_equality"])
        self.assertEqual(
            record["exact_audit"]["equality_certificate_payload_bits"],
            17,
        )

    def test_nonbipartite_gap_is_preserved(self) -> None:
        record = self.schema["cases"][7]
        self.assertEqual(record["case_id"], "N2-C5")
        self.assertEqual(
            (
                record["exact_audit"]["residual_vertex_cover_number"],
                record["exact_audit"]["residual_matching_number"],
            ),
            (3, 2),
        )

    def test_seed_slots_are_the_frozen_looped_k5(self) -> None:
        slots = [
            tuple(record["coverer_type_ids"])
            for record in self.schema["seed"]["slots"]
        ]
        self.assertEqual(len(slots), 15)
        self.assertEqual(sum(len(slot) == 1 for slot in slots), 5)
        self.assertEqual(sum(len(slot) == 2 for slot in slots), 10)

    def test_exhaustive_small_bipartite_graphs_match_exact_oracle(self) -> None:
        checked = 0
        for left_count in range(4):
            for right_count in range(4):
                left = tuple(f"L{index}" for index in range(left_count))
                right = tuple(f"R{index}" for index in range(right_count))
                vertices = left + right
                possible_edges = tuple(itertools.product(left, right))
                for mask in range(1 << len(possible_edges)):
                    edges = tuple(
                        (index, edge)
                        for index, edge in enumerate(possible_edges)
                        if mask & (1 << index)
                    )
                    matching, searches = (
                        GENERATOR.construct_maximum_matching(left, edges)
                    )
                    cover = GENERATOR.construct_minimum_cover(
                        left,
                        right,
                        edges,
                        matching,
                    )
                    exact_cover = CHECKER.minimum_vertex_cover(
                        vertices,
                        edges,
                    )
                    exact_matching = CHECKER.maximum_matching(edges)
                    self.assertEqual(len(matching), len(exact_matching))
                    self.assertEqual(len(cover), len(exact_cover))
                    self.assertEqual(len(cover), len(matching))
                    self.assertEqual(searches, len(matching) + 1)
                    CHECKER.validate_matching(list(matching), edges)
                    CHECKER.validate_cover(list(cover), vertices, edges)
                    checked += 1
        self.assertEqual(checked, 689)

    def test_parallel_edges_and_isolates_are_supported(self) -> None:
        left = ("L0", "L1", "L2")
        right = ("R0", "R1", "R2")
        edges = (
            (10, ("L0", "R0")),
            (11, ("L0", "R0")),
            (12, ("L1", "R1")),
        )
        matching, searches = GENERATOR.construct_maximum_matching(
            left,
            edges,
        )
        cover = GENERATOR.construct_minimum_cover(
            left,
            right,
            edges,
            matching,
        )
        self.assertEqual(len(matching), 2)
        self.assertEqual(len(cover), 2)
        self.assertEqual(searches, 3)
        CHECKER.validate_matching(list(matching), edges)
        CHECKER.validate_cover(list(cover), left + right, edges)

    def test_rehashed_source_anchor_mutation_is_rejected(self) -> None:
        schema = copy.deepcopy(self.schema)
        schema["source"]["file_sha256"] = "0" * 64
        rehash(schema)
        with self.assertRaisesRegex(AssertionError, "source anchor"):
            CHECKER.validate_all(schema)

    def test_rehashed_case_grammar_mutation_is_rejected(self) -> None:
        schema = copy.deepcopy(self.schema)
        schema["case_grammar"]["registered_cases"].pop()
        rehash(schema)
        with self.assertRaisesRegex(AssertionError, "case grammar"):
            CHECKER.validate_all(schema)

    def test_rehashed_deleted_edge_mutation_is_rejected(self) -> None:
        schema = copy.deepcopy(self.schema)
        schema["cases"][0]["deleted_edge_column_indices"].pop()
        rehash(schema)
        with self.assertRaisesRegex(AssertionError, "deleted_edge"):
            CHECKER.validate_all(schema)

    def test_rehashed_bipartition_mutation_is_rejected(self) -> None:
        schema = copy.deepcopy(self.schema)
        schema["cases"][0]["constructor"]["left_type_ids"] = ["T0"]
        rehash(schema)
        with self.assertRaisesRegex(AssertionError, "bipartition"):
            CHECKER.validate_all(schema)

    def test_rehashed_constructor_matching_mutation_is_rejected(self) -> None:
        schema = copy.deepcopy(self.schema)
        schema["cases"][3]["constructor"][
            "maximum_matching_column_indices"
        ] = [0, 1]
        rehash(schema)
        with self.assertRaisesRegex(AssertionError, "constructor matching"):
            CHECKER.validate_all(schema)

    def test_rehashed_constructor_cover_mutation_is_rejected(self) -> None:
        schema = copy.deepcopy(self.schema)
        schema["cases"][2]["constructor"]["minimum_cover_type_ids"] = ["T1"]
        rehash(schema)
        with self.assertRaisesRegex(AssertionError, "constructor cover"):
            CHECKER.validate_all(schema)

    def test_rehashed_cost_mutation_is_rejected(self) -> None:
        schema = copy.deepcopy(self.schema)
        schema["cases"][5]["constructor"]["output_payload_bits"] += 1
        rehash(schema)
        with self.assertRaisesRegex(AssertionError, "output_payload_bits"):
            CHECKER.validate_all(schema)

    def test_rehashed_odd_cycle_mutation_is_rejected(self) -> None:
        schema = copy.deepcopy(self.schema)
        schema["cases"][6]["odd_cycle_type_ids"] = [
            "T0",
            "T1",
            "T3",
            "T0",
        ]
        rehash(schema)
        with self.assertRaisesRegex(AssertionError, "odd_cycle_type_ids"):
            CHECKER.validate_all(schema)

    def test_rehashed_scope_mutation_is_rejected(self) -> None:
        schema = copy.deepcopy(self.schema)
        schema["scope"]["not_claimed"].pop()
        rehash(schema)
        with self.assertRaisesRegex(AssertionError, "scope boundary"):
            CHECKER.validate_all(schema)


if __name__ == "__main__":
    unittest.main()
