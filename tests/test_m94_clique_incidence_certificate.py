"""Regression and mutation tests for the M94 clique-incidence certificates."""

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
CHECKER_PATH = ROOT / "scripts" / "check_m94_clique_incidence_certificate.py"
GENERATOR_PATH = ROOT / "scripts" / "run_m94_clique_incidence_audit.py"
SCHEMA_PATH = ROOT / "schemas" / "m94-clique-incidence-certificates-v1.json"
SOURCE_PATH = ROOT / "schemas" / "m93-early-repair-certificates-v1.json"


def load_module(name: str, path: Path) -> ModuleType:
    """Load a repository script from its exact path."""
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


CHECKER = load_module("check_m94_clique_incidence", CHECKER_PATH)
GENERATOR = load_module("run_m94_clique_incidence", GENERATOR_PATH)


def rehash(schema: dict[str, Any]) -> None:
    """Update the self-hash of a deliberately mutated schema."""
    schema["summary_sha256"] = CHECKER.canonical_hash(schema)


class M94CliqueIncidenceTests(unittest.TestCase):
    """Check exact clique incidence, costs, and mutation rejection."""

    def setUp(self) -> None:
        self.schema = cast(
            dict[str, Any],
            json.loads(SCHEMA_PATH.read_text(encoding="utf-8")),
        )
        self.source = cast(
            dict[str, Any],
            json.loads(SOURCE_PATH.read_text(encoding="utf-8")),
        )

    def test_registered_portfolio_passes(self) -> None:
        totals = CHECKER.validate_all(self.schema)
        self.assertEqual(totals["instance_count"], 2)
        self.assertEqual(totals["tracked_point_count"], 7)
        self.assertEqual(totals["pair_count"], 9)
        self.assertEqual(totals["type_count"], 7)
        self.assertEqual(totals["coverer_incidence_count"], 18)
        self.assertEqual(totals["abstract_certificate_payload_bits"], 130)
        self.assertEqual(totals["payload_bits_saved"], 56)

    def test_generator_reproduces_registered_schema(self) -> None:
        self.assertEqual(GENERATOR.build_summary(), self.schema)

    def test_checker_is_standard_library_only_and_independent(self) -> None:
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
        self.assertLessEqual(len(source.splitlines()), 400)
        self.assertNotIn("check_m93", source)
        self.assertNotIn("run_m94", source)
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

    def test_every_coverer_column_is_one_complete_graph_edge(self) -> None:
        for instance in self.schema["instances"]:
            type_ids = [
                record["type_id"] for record in instance["coverage_types"]
            ]
            observed = [
                tuple(record["coverer_type_ids"])
                for record in instance["coverer_sets"]
            ]
            self.assertTrue(all(len(pair) == 2 for pair in observed))
            self.assertEqual(
                sorted(observed),
                list(itertools.combinations(type_ids, 2)),
            )

    def test_exact_repairs_and_cost_tradeoff_are_frozen(self) -> None:
        self.assertEqual(
            [
                int(instance["exact_repair_number"])
                for instance in self.schema["instances"]
            ],
            [2, 3],
        )
        self.assertEqual(
            [
                int(instance["verification_cost"]["payload_bits_saved"])
                for instance in self.schema["instances"]
            ],
            [8, 48],
        )
        self.assertEqual(
            [
                int(
                    instance["verification_cost"]["verifier_bit_test_delta"]
                )
                for instance in self.schema["instances"]
            ],
            [5, 0],
        )

    def test_rehashed_coverer_trace_mutation_is_rejected(self) -> None:
        schema = copy.deepcopy(self.schema)
        schema["instances"][1]["coverer_sets"][0][
            "coverer_type_ids"
        ] = ["T0", "T2"]
        rehash(schema)
        with self.assertRaisesRegex(AssertionError, "coverer sets"):
            CHECKER.validate_all(schema)

    def test_rehashed_source_anchor_mutation_is_rejected(self) -> None:
        schema = copy.deepcopy(self.schema)
        schema["source"]["file_sha256"] = "0" * 64
        rehash(schema)
        with self.assertRaisesRegex(AssertionError, "source anchor"):
            CHECKER.validate_all(schema)

    def test_rehashed_coverage_mask_mutation_is_rejected(self) -> None:
        schema = copy.deepcopy(self.schema)
        schema["instances"][0]["coverage_types"][0][
            "coverage_mask_hex"
        ] = "0"
        rehash(schema)
        with self.assertRaisesRegex(AssertionError, "coverage masks"):
            CHECKER.validate_all(schema)

    def test_rehashed_cost_mutation_is_rejected(self) -> None:
        schema = copy.deepcopy(self.schema)
        schema["instances"][1]["verification_cost"][
            "payload_bits_saved"
        ] += 1
        rehash(schema)
        with self.assertRaisesRegex(AssertionError, "verification cost"):
            CHECKER.validate_all(schema)

    def test_non_clique_column_is_rejected_after_source_rebinding(self) -> None:
        source_instance = copy.deepcopy(self.source["instances"][0])
        instance = copy.deepcopy(self.schema["instances"][0])
        replacement = {
            "type_id": "T2",
            "pattern": [0, 1, 0],
            "coverage_mask_hex": "5",
        }
        source_instance["coverage_types"][2].update(replacement)
        instance["coverage_types"][2] = replacement
        buckets = tuple(
            tuple(int(prime) for prime in bucket)
            for bucket in instance["collision_buckets"]
        )
        pairs = CHECKER.pair_universe(buckets)
        type_ids = tuple(
            record["type_id"] for record in instance["coverage_types"]
        )
        masks = tuple(
            int(record["coverage_mask_hex"], 16)
            for record in instance["coverage_types"]
        )
        instance["coverer_sets"] = CHECKER.reconstruct_coverers(
            type_ids,
            masks,
            pairs,
        )
        instance["source_instance_sha256"] = CHECKER.canonical_hash(
            source_instance
        )
        with self.assertRaisesRegex(AssertionError, "two coverers"):
            CHECKER.validate_instance(instance, source_instance)

    def test_coverer_trace_differential_matches_direct_masks(self) -> None:
        for instance in self.schema["instances"]:
            type_ids = tuple(
                record["type_id"] for record in instance["coverage_types"]
            )
            masks = tuple(
                int(record["coverage_mask_hex"], 16)
                for record in instance["coverage_types"]
            )
            direct = [
                tuple(
                    type_id
                    for type_id, mask in zip(type_ids, masks, strict=True)
                    if (mask >> pair_index) & 1
                )
                for pair_index in range(int(instance["pair_count"]))
            ]
            registered = [
                tuple(record["coverer_type_ids"])
                for record in instance["coverer_sets"]
            ]
            self.assertEqual(direct, registered)


if __name__ == "__main__":
    unittest.main()
