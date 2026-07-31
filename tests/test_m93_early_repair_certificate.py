"""Regression and mutation tests for the M93 early repair certificates."""

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
CHECKER_PATH = ROOT / "scripts" / "check_m93_early_repair_certificate.py"
GENERATOR_PATH = ROOT / "scripts" / "run_m93_early_repair_audit.py"
M91_PATH = ROOT / "scripts" / "check_m91_all_rows_semantic_certificate.py"
SCHEMA_PATH = ROOT / "schemas" / "m93-early-repair-certificates-v1.json"


def load_module(name: str, path: Path) -> ModuleType:
    """Load one repository script from its exact path."""
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


CHECKER = load_module("check_m93_early_repair", CHECKER_PATH)
GENERATOR = load_module("run_m93_early_repair", GENERATOR_PATH)


def rehash(schema: dict[str, Any]) -> None:
    """Update the canonical hash of a deliberately mutated schema."""
    schema["summary_sha256"] = CHECKER.canonical_hash(schema)


class M93EarlyRepairCertificateTests(unittest.TestCase):
    """Check exact minima, independent reconstruction, and mutations."""

    def setUp(self) -> None:
        self.schema = cast(
            dict[str, Any],
            json.loads(SCHEMA_PATH.read_text(encoding="utf-8")),
        )

    def test_registered_portfolio_passes(self) -> None:
        totals = CHECKER.validate_all(self.schema)
        self.assertEqual(totals["instance_count"], 10)
        self.assertEqual(totals["tracked_prime_count"], 27)
        self.assertEqual(totals["pair_count"], 23)
        self.assertEqual(totals["coverage_type_count"], 18)
        self.assertEqual(totals["minimum_coordinate_count"], 16)
        self.assertEqual(totals["raw_coordinate_tests"], 154_920)
        self.assertEqual(totals["abstract_certificate_payload_bits"], 483)

    def test_generator_reproduces_registered_schema(self) -> None:
        self.assertEqual(GENERATOR.build_summary(), self.schema)

    def test_checker_is_standard_library_only_and_clean_room(self) -> None:
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
        self.assertNotIn("check_m91", source)
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

    def test_exact_minima_and_lower_witness_kinds_are_frozen(self) -> None:
        minima = [
            int(instance["minimum_coordinate_count"])
            for instance in self.schema["instances"]
        ]
        kinds = [
            str(instance["lower_witness"]["kind"])
            for instance in self.schema["instances"]
        ]
        self.assertEqual(minima, [2, 2, 1, 1, 1, 3, 1, 1, 3, 1])
        self.assertEqual(kinds[0], "cardinality")
        self.assertEqual(kinds[8], "subset_obstructions")
        self.assertEqual(
            [kind for index, kind in enumerate(kinds) if index not in (0, 8)],
            ["private_pairs"] * 8,
        )

    def test_private_pair_criterion_fails_exactly_at_16_and_24(self) -> None:
        for instance in (self.schema["instances"][0], self.schema["instances"][8]):
            masks = {
                record["type_id"]: int(record["coverage_mask_hex"], 16)
                for record in instance["coverage_types"]
            }
            for type_id in instance["upper_witness"]:
                has_private_pair = any(
                    (masks[type_id] >> pair_index) & 1
                    and sum(
                        (mask >> pair_index) & 1 for mask in masks.values()
                    )
                    == 1
                    for pair_index in range(int(instance["pair_count"]))
                )
                self.assertFalse(has_private_pair)

    def test_m24_subset_obstruction_lists_every_two_type_subset(self) -> None:
        instance = self.schema["instances"][8]
        lower = instance["lower_witness"]
        self.assertEqual(lower["subset_size"], 2)
        expected = {
            tuple(subset)
            for subset in __import__("itertools").combinations(
                [record["type_id"] for record in instance["coverage_types"]],
                2,
            )
        }
        self.assertEqual(
            {tuple(entry["type_ids"]) for entry in lower["entries"]},
            expected,
        )
        self.assertEqual(len(lower["entries"]), 6)

    def test_rehashed_coverage_type_mutation_is_rejected(self) -> None:
        schema = copy.deepcopy(self.schema)
        schema["instances"][0]["coverage_types"][0]["coverage_mask_hex"] = "0"
        rehash(schema)
        with self.assertRaisesRegex(AssertionError, "raw coverage types"):
            CHECKER.validate_all(schema)

    def test_rehashed_source_path_mutation_is_rejected(self) -> None:
        schema = copy.deepcopy(self.schema)
        schema["instances"][0]["source_path"] = "schemas/other.json"
        rehash(schema)
        with self.assertRaisesRegex(AssertionError, "source path"):
            CHECKER.validate_all(schema)

    def test_rehashed_upper_witness_mutation_is_rejected(self) -> None:
        schema = copy.deepcopy(self.schema)
        schema["instances"][5]["upper_witness"] = ["T0", "T1"]
        rehash(schema)
        with self.assertRaisesRegex(AssertionError, "upper witness"):
            CHECKER.validate_all(schema)

    def test_rehashed_cardinality_mutation_is_rejected(self) -> None:
        schema = copy.deepcopy(self.schema)
        schema["instances"][0]["lower_witness"]["maximum_bucket_size"] = 2
        rehash(schema)
        with self.assertRaisesRegex(AssertionError, "lower witness"):
            CHECKER.validate_all(schema)

    def test_rehashed_private_pair_mutation_is_rejected(self) -> None:
        schema = copy.deepcopy(self.schema)
        schema["instances"][1]["lower_witness"]["entries"][0][
            "pair_index"
        ] = 1
        rehash(schema)
        with self.assertRaisesRegex(AssertionError, "lower witness"):
            CHECKER.validate_all(schema)

    def test_rehashed_subset_obstruction_mutation_is_rejected(self) -> None:
        schema = copy.deepcopy(self.schema)
        schema["instances"][8]["lower_witness"]["entries"].pop()
        rehash(schema)
        with self.assertRaisesRegex(AssertionError, "lower witness"):
            CHECKER.validate_all(schema)

    def test_rehashed_cost_mutation_is_rejected(self) -> None:
        schema = copy.deepcopy(self.schema)
        schema["instances"][8]["verification_cost"][
            "lower_witness_bit_tests"
        ] += 1
        rehash(schema)
        with self.assertRaisesRegex(AssertionError, "cost ledger"):
            CHECKER.validate_all(schema)

    def test_raw_coverage_types_differentially_match_m91(self) -> None:
        m91 = load_module("check_m91_for_m93", M91_PATH)
        for instance in self.schema["instances"]:
            buckets = tuple(
                tuple(int(prime) for prime in bucket)
                for bucket in instance["collision_buckets"]
            )
            primes = tuple(prime for bucket in buckets for prime in bucket)
            pairs = m91.pair_universe(buckets)
            coverages, evaluations = m91.all_new_coverages(
                int(instance["base_cap"]),
                int(instance["repair_cap"]),
                primes,
                pairs,
            )
            registered = {
                int(record["coverage_mask_hex"], 16)
                for record in instance["coverage_types"]
            }
            self.assertEqual(coverages, registered)
            self.assertEqual(
                evaluations,
                int(
                    instance["verification_cost"][
                        "descriptor_prime_evaluations"
                    ]
                ),
            )


if __name__ == "__main__":
    unittest.main()
