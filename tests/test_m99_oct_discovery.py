"""Regression and mutation tests for M99 iterative-compression discovery."""

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
CHECKER_PATH = ROOT / "scripts" / "check_m99_oct_discovery.py"
GENERATOR_PATH = ROOT / "scripts" / "run_m99_oct_discovery_profile.py"
SCHEMA_PATH = ROOT / "schemas" / "m99-oct-discovery-v1.json"


def load_module(name: str, path: Path) -> ModuleType:
    """Load one repository script from its exact path."""
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


CHECKER = load_module("check_m99_oct_discovery", CHECKER_PATH)
GENERATOR = load_module("run_m99_oct_discovery", GENERATOR_PATH)


def rehash(schema: dict[str, Any]) -> None:
    """Rehash one deliberately mutated schema."""
    schema["summary_sha256"] = CHECKER.canonical_hash(schema)


class M99OctDiscoveryTests(unittest.TestCase):
    """Check iterative compression, exact composition, and mutations."""

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
                "accepted_count": 7,
                "rejected_count": 1,
                "cap_sum": 13,
                "discovered_oct_size_sum": 11,
                "compression_calls": 38,
                "partition_count": 204,
                "flow_call_count": 160,
                "flow_augmentations": 102,
                "flow_searches": 158,
                "discovered_oct_payload_bits": 51,
                "composed_cover_number_sum": 21,
                "composed_cover_payload_bits": 79,
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
        self.assertLessEqual(len(source.splitlines()), 550)
        self.assertNotIn("run_m99", source)
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

    def test_discovered_oct_registry_is_exact(self) -> None:
        self.assertEqual(
            [
                record["discovery"]["oct_type_ids"]
                for record in self.schema["cases"]
            ],
            [
                ["T0"],
                ["T0"],
                ["T0"],
                ["T1"],
                ["T0", "T1"],
                ["T2", "T3"],
                ["T0", "T1", "T2"],
                None,
            ],
        )

    def test_k5_cap_boundary_is_preserved(self) -> None:
        accepted = self.schema["cases"][6]
        rejected = self.schema["cases"][7]
        self.assertEqual(accepted["residual_edges"], rejected["residual_edges"])
        self.assertEqual(accepted["cap"], 3)
        self.assertEqual(rejected["cap"], 2)
        self.assertEqual(
            rejected["discovery"]["status"],
            "rejected_above_cap",
        )
        self.assertEqual(rejected["discovery"]["rejected_prefix_size"], 5)

    def test_exhaustive_five_vertex_graph_caps(self) -> None:
        vertices = ("V0", "V1", "V2", "V3", "V4")
        possible_edges = tuple(itertools.combinations(vertices, 2))
        comparisons = 0
        for edge_mask in range(1 << len(possible_edges)):
            edges = tuple(
                (index, edge)
                for index, edge in enumerate(possible_edges)
                if edge_mask & (1 << index)
            )
            exact = CHECKER.minimum_oct(vertices, edges)
            for cap in range(4):
                report = GENERATOR.discover_oct(vertices, edges, cap)
                if len(exact) <= cap:
                    self.assertEqual(report["status"], "discovered_exact")
                    discovered = tuple(report["oct_type_ids"])
                    self.assertEqual(len(discovered), len(exact))
                    self.assertTrue(
                        GENERATOR.is_oct(vertices, edges, discovered)
                    )
                else:
                    self.assertEqual(report["status"], "rejected_above_cap")
                comparisons += 1
        self.assertEqual(comparisons, 4096)

    def test_parallel_edge_and_isolate_regression(self) -> None:
        vertices = ("A", "B", "C", "D")
        edges = (
            (0, ("A", "B")),
            (1, ("A", "B")),
            (2, ("B", "C")),
            (3, ("A", "C")),
        )
        report = GENERATOR.discover_oct(vertices, edges, 1)
        self.assertEqual(report["status"], "discovered_exact")
        self.assertEqual(report["oct_type_ids"], ["A"])
        self.assertTrue(GENERATOR.is_oct(vertices, edges, ("A",)))

    def test_separator_can_delete_shared_terminal(self) -> None:
        vertices = ("A",)
        separator, metrics = GENERATOR.minimum_vertex_separator(
            vertices,
            (),
            ("A",),
            ("A",),
            1,
        )
        self.assertEqual(separator, ("A",))
        self.assertEqual(metrics["flow_augmentations"], 1)

    def test_separator_rejects_budget_zero_path(self) -> None:
        vertices = ("A", "B")
        separator, _ = GENERATOR.minimum_vertex_separator(
            vertices,
            ((0, ("A", "B")),),
            ("A",),
            ("B",),
            0,
        )
        self.assertIsNone(separator)

    def test_rehashed_source_mutation_is_rejected(self) -> None:
        schema = copy.deepcopy(self.schema)
        schema["source"]["file_sha256"] = "0" * 64
        rehash(schema)
        with self.assertRaisesRegex(AssertionError, "source anchor"):
            CHECKER.validate_all(schema)

    def test_rehashed_literature_mutation_is_rejected(self) -> None:
        schema = copy.deepcopy(self.schema)
        schema["literature_basis"]["inspected_pages"] = 4
        rehash(schema)
        with self.assertRaisesRegex(AssertionError, "literature basis"):
            CHECKER.validate_all(schema)

    def test_rehashed_graph_mutation_is_rejected(self) -> None:
        schema = copy.deepcopy(self.schema)
        schema["cases"][0]["residual_edges"].pop()
        rehash(schema)
        with self.assertRaisesRegex(AssertionError, "residual edges"):
            CHECKER.validate_all(schema)

    def test_rehashed_cap_mutation_is_rejected(self) -> None:
        schema = copy.deepcopy(self.schema)
        schema["cases"][1]["cap"] = 2
        rehash(schema)
        with self.assertRaisesRegex(AssertionError, "cap changed"):
            CHECKER.validate_all(schema)

    def test_rehashed_status_mutation_is_rejected(self) -> None:
        schema = copy.deepcopy(self.schema)
        schema["cases"][2]["discovery"]["status"] = "rejected_above_cap"
        rehash(schema)
        with self.assertRaisesRegex(AssertionError, "accepted status"):
            CHECKER.validate_all(schema)

    def test_rehashed_oct_mutation_is_rejected(self) -> None:
        schema = copy.deepcopy(self.schema)
        schema["cases"][3]["discovery"]["oct_type_ids"] = ["T4"]
        rehash(schema)
        with self.assertRaisesRegex(AssertionError, "discovered OCT"):
            CHECKER.validate_all(schema)

    def test_rehashed_metric_mutation_is_rejected(self) -> None:
        schema = copy.deepcopy(self.schema)
        schema["cases"][4]["discovery"]["partition_count"] += 1
        rehash(schema)
        with self.assertRaisesRegex(AssertionError, "metrics"):
            CHECKER.validate_all(schema)

    def test_rehashed_payload_mutation_is_rejected(self) -> None:
        schema = copy.deepcopy(self.schema)
        schema["cases"][5]["discovered_oct_payload_bits"] += 1
        rehash(schema)
        with self.assertRaisesRegex(AssertionError, "OCT payload"):
            CHECKER.validate_all(schema)

    def test_rehashed_cover_mutation_is_rejected(self) -> None:
        schema = copy.deepcopy(self.schema)
        schema["cases"][6]["composed_minimum_cover_type_ids"].pop()
        rehash(schema)
        with self.assertRaisesRegex(AssertionError, "composed cover"):
            CHECKER.validate_all(schema)

    def test_rehashed_rejection_mutation_is_rejected(self) -> None:
        schema = copy.deepcopy(self.schema)
        schema["cases"][7]["discovery"]["rejected_prefix_size"] = 4
        rehash(schema)
        with self.assertRaisesRegex(AssertionError, "rejection prefix"):
            CHECKER.validate_all(schema)

    def test_rehashed_scope_mutation_is_rejected(self) -> None:
        schema = copy.deepcopy(self.schema)
        schema["scope"]["not_claimed"].pop()
        rehash(schema)
        with self.assertRaisesRegex(AssertionError, "scope boundary"):
            CHECKER.validate_all(schema)


if __name__ == "__main__":
    unittest.main()
