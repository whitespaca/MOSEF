"""Regression and mutation tests for the M98 OCT constructor."""

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
CHECKER_PATH = ROOT / "scripts" / "check_m98_oct_cover.py"
GENERATOR_PATH = ROOT / "scripts" / "run_m98_oct_cover_profile.py"
SCHEMA_PATH = ROOT / "schemas" / "m98-oct-cover-v1.json"


def load_module(name: str, path: Path) -> ModuleType:
    """Load one repository script from its exact path."""
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


CHECKER = load_module("check_m98_oct_cover", CHECKER_PATH)
GENERATOR = load_module("run_m98_oct_cover", GENERATOR_PATH)


def rehash(schema: dict[str, Any]) -> None:
    """Rehash one deliberately mutated schema."""
    schema["summary_sha256"] = CHECKER.canonical_hash(schema)


class M98OctCoverTests(unittest.TestCase):
    """Check branch exactness, exponential scope, and mutations."""

    def setUp(self) -> None:
        self.schema = cast(
            dict[str, Any],
            json.loads(SCHEMA_PATH.read_text(encoding="utf-8")),
        )

    def test_registered_portfolio_passes(self) -> None:
        self.assertEqual(
            CHECKER.validate_all(self.schema),
            {
                "case_count": 8,
                "valid_transversal_count": 7,
                "rejected_transversal_count": 1,
                "transversal_size_sum": 13,
                "branch_count": 24,
                "feasible_branch_count": 18,
                "residual_vertex_cover_number_sum": 25,
                "residual_matching_number_sum": 16,
                "exact_repair_number_sum": 27,
                "transversal_payload_bits": 63,
                "valid_output_cover_payload_bits": 84,
                "maximum_matching_gap": 2,
                "maximum_transversal_size": 3,
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
        self.assertLessEqual(len(source.splitlines()), 850)
        self.assertNotIn("run_m98", source)
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

    def test_valid_and_rejected_case_counts(self) -> None:
        statuses = [
            record["constructor"]["status"]
            for record in self.schema["cases"]
        ]
        self.assertEqual(statuses.count("constructed_exact"), 7)
        self.assertEqual(statuses.count("rejected_invalid_transversal"), 1)

    def test_branch_and_feasibility_ledgers(self) -> None:
        self.assertEqual(
            [
                (
                    record["constructor"]["branch_count"],
                    record["constructor"]["feasible_branch_count"],
                )
                for record in self.schema["cases"]
            ],
            [(2, 2), (2, 2), (2, 2), (2, 2), (4, 3), (4, 3), (8, 4), (0, 0)],
        )

    def test_k5_valid_and_invalid_transversals_are_distinct(self) -> None:
        valid = self.schema["cases"][6]
        rejected = self.schema["cases"][7]
        self.assertEqual(valid["target_edge_pairs"], rejected["target_edge_pairs"])
        self.assertEqual(valid["transversal_size"], 3)
        self.assertEqual(rejected["transversal_size"], 2)
        self.assertEqual(
            rejected["rejection_odd_cycle_type_ids"],
            ["T2", "T3", "T4", "T2"],
        )

    def test_all_valid_outputs_match_exact_audit(self) -> None:
        for record in self.schema["cases"][:7]:
            self.assertEqual(
                record["constructor"]["minimum_cover_number"],
                record["exact_audit"]["residual_vertex_cover_number"],
            )

    def test_exhaustive_four_vertex_graph_transversals(self) -> None:
        vertices = ("V0", "V1", "V2", "V3")
        possible_edges = tuple(itertools.combinations(vertices, 2))
        valid_inputs = 0
        rejected_inputs = 0
        for edge_mask in range(1 << len(possible_edges)):
            edges = tuple(
                (index, edge)
                for index, edge in enumerate(possible_edges)
                if edge_mask & (1 << index)
            )
            exact_cover = GENERATOR.minimum_vertex_cover(vertices, edges)
            for transversal_mask in range(1 << len(vertices)):
                transversal = tuple(
                    vertex
                    for index, vertex in enumerate(vertices)
                    if transversal_mask & (1 << index)
                )
                report = GENERATOR.solve_with_transversal(
                    vertices,
                    edges,
                    transversal,
                )
                if report["status"] == "constructed_exact":
                    self.assertEqual(
                        report["minimum_cover_number"],
                        len(exact_cover),
                    )
                    self.assertEqual(
                        report["branch_count"],
                        1 << len(transversal),
                    )
                    valid_inputs += 1
                else:
                    base = tuple(
                        vertex
                        for vertex in vertices
                        if vertex not in set(transversal)
                    )
                    base_edges = tuple(
                        (index, edge)
                        for index, edge in edges
                        if edge[0] in base and edge[1] in base
                    )
                    self.assertIsNone(
                        GENERATOR.bipartition(base, base_edges)
                    )
                    rejected_inputs += 1
        self.assertEqual(valid_inputs + rejected_inputs, 1024)
        self.assertGreater(valid_inputs, rejected_inputs)

    def test_rehashed_source_anchor_mutation_is_rejected(self) -> None:
        schema = copy.deepcopy(self.schema)
        schema["source"]["file_sha256"] = "0" * 64
        rehash(schema)
        with self.assertRaisesRegex(AssertionError, "source anchor"):
            CHECKER.validate_all(schema)

    def test_rehashed_m97_anchor_mutation_is_rejected(self) -> None:
        schema = copy.deepcopy(self.schema)
        schema["source"]["m97_constructor_sha256"] = "0" * 64
        rehash(schema)
        with self.assertRaisesRegex(AssertionError, "source anchor"):
            CHECKER.validate_all(schema)

    def test_rehashed_case_grammar_mutation_is_rejected(self) -> None:
        schema = copy.deepcopy(self.schema)
        schema["case_grammar"]["registered_cases"].pop()
        rehash(schema)
        with self.assertRaisesRegex(AssertionError, "case grammar"):
            CHECKER.validate_all(schema)

    def test_rehashed_transversal_mutation_is_rejected(self) -> None:
        schema = copy.deepcopy(self.schema)
        schema["cases"][0]["transversal_type_ids"] = ["T1"]
        rehash(schema)
        with self.assertRaisesRegex(AssertionError, "transversal_type_ids"):
            CHECKER.validate_all(schema)

    def test_rehashed_branch_status_mutation_is_rejected(self) -> None:
        schema = copy.deepcopy(self.schema)
        schema["cases"][4]["constructor"]["branches"][0][
            "status"
        ] = "feasible_exact"
        rehash(schema)
        with self.assertRaisesRegex(AssertionError, "infeasible branch"):
            CHECKER.validate_all(schema)

    def test_rehashed_forced_set_mutation_is_rejected(self) -> None:
        schema = copy.deepcopy(self.schema)
        schema["cases"][1]["constructor"]["branches"][0][
            "forced_base_type_ids"
        ].pop()
        rehash(schema)
        with self.assertRaisesRegex(AssertionError, "forced_base_type_ids"):
            CHECKER.validate_all(schema)

    def test_rehashed_candidate_mutation_is_rejected(self) -> None:
        schema = copy.deepcopy(self.schema)
        schema["cases"][2]["constructor"]["branches"][1][
            "candidate_cover_type_ids"
        ] = ["T0"]
        rehash(schema)
        with self.assertRaisesRegex(AssertionError, "candidate_cover_type_ids"):
            CHECKER.validate_all(schema)

    def test_rehashed_minimum_mutation_is_rejected(self) -> None:
        schema = copy.deepcopy(self.schema)
        schema["cases"][5]["constructor"]["minimum_cover_number"] += 1
        rehash(schema)
        with self.assertRaisesRegex(AssertionError, "minimum number"):
            CHECKER.validate_all(schema)

    def test_rehashed_rejection_cycle_mutation_is_rejected(self) -> None:
        schema = copy.deepcopy(self.schema)
        schema["cases"][7]["rejection_odd_cycle_type_ids"] = [
            "T0",
            "T1",
            "T2",
            "T0",
        ]
        rehash(schema)
        with self.assertRaisesRegex(AssertionError, "rejection_odd_cycle"):
            CHECKER.validate_all(schema)

    def test_rehashed_payload_mutation_is_rejected(self) -> None:
        schema = copy.deepcopy(self.schema)
        schema["cases"][6]["transversal_payload_bits"] += 1
        rehash(schema)
        with self.assertRaisesRegex(AssertionError, "transversal_payload_bits"):
            CHECKER.validate_all(schema)

    def test_rehashed_scope_mutation_is_rejected(self) -> None:
        schema = copy.deepcopy(self.schema)
        schema["scope"]["not_claimed"].pop()
        rehash(schema)
        with self.assertRaisesRegex(AssertionError, "scope boundary"):
            CHECKER.validate_all(schema)


if __name__ == "__main__":
    unittest.main()
