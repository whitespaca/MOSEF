"""Regression and mutation tests for the M95 coverer-graph portfolio."""

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
CHECKER_PATH = ROOT / "scripts" / "check_m95_coverer_graph_certificate.py"
GENERATOR_PATH = ROOT / "scripts" / "run_m95_coverer_graph_profile.py"
SCHEMA_PATH = ROOT / "schemas" / "m95-coverer-graph-profile-v1.json"
SOURCE_PATHS = {
    "M92": ROOT / "schemas" / "m92-pair-cover-certificates-v1.json",
    "M93": ROOT / "schemas" / "m93-early-repair-certificates-v1.json",
}


def load_module(name: str, path: Path) -> ModuleType:
    """Load a repository script from its exact path."""
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


CHECKER = load_module("check_m95_coverer_graph", CHECKER_PATH)
GENERATOR = load_module("run_m95_coverer_graph", GENERATOR_PATH)


def rehash(schema: dict[str, Any]) -> None:
    """Update the self-hash of a deliberately mutated schema."""
    schema["summary_sha256"] = CHECKER.canonical_hash(schema)


class M95CovererGraphTests(unittest.TestCase):
    """Check the rank-two profile, graph templates, costs, and boundaries."""

    def setUp(self) -> None:
        self.schema = cast(
            dict[str, Any],
            json.loads(SCHEMA_PATH.read_text(encoding="utf-8")),
        )
        self.sources = {
            source_id: cast(
                dict[str, Any],
                json.loads(path.read_text(encoding="utf-8")),
            )
            for source_id, path in SOURCE_PATHS.items()
        }

    def test_registered_portfolio_passes(self) -> None:
        totals = CHECKER.validate_all(self.schema)
        self.assertEqual(totals["instance_count"], 19)
        self.assertEqual(totals["tracked_point_count"], 55)
        self.assertEqual(totals["pair_count"], 64)
        self.assertEqual(totals["type_count"], 37)
        self.assertEqual(totals["coverer_incidence_count"], 98)
        self.assertEqual(totals["degree_one_column_count"], 30)
        self.assertEqual(totals["degree_two_column_count"], 34)
        self.assertEqual(totals["minimum_coordinate_count"], 35)

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
        self.assertLessEqual(len(source.splitlines()), 575)
        self.assertNotIn("run_m95", source)
        self.assertNotIn("check_m92", source)
        self.assertNotIn("check_m93", source)
        self.assertNotIn("check_m94", source)
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

    def test_all_instances_match_one_exact_graph_template(self) -> None:
        counts = {
            "loop_only": 0,
            "looped_clique": 0,
            "loopless_clique": 0,
        }
        for instance in self.schema["instances"]:
            counts[instance["template_kind"]] += 1
            self.assertTrue(
                all(
                    len(record["coverer_type_ids"]) in (1, 2)
                    for record in instance["coverer_sets"]
                )
            )
        self.assertEqual(
            counts,
            {
                "loop_only": 12,
                "looped_clique": 5,
                "loopless_clique": 2,
            },
        )

    def test_exact_repairs_follow_forced_loops_or_cliques(self) -> None:
        for instance in self.schema["instances"]:
            type_count = int(instance["type_count"])
            if instance["template_kind"] == "loopless_clique":
                self.assertEqual(
                    int(instance["exact_repair_number"]),
                    type_count - 1,
                )
                self.assertEqual(instance["looped_type_ids"], [])
            else:
                self.assertEqual(
                    int(instance["exact_repair_number"]),
                    type_count,
                )
                self.assertEqual(
                    len(instance["looped_type_ids"]),
                    type_count,
                )

    def test_coverer_trace_matches_direct_masks(self) -> None:
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

    def test_cost_comparison_is_frozen(self) -> None:
        totals = self.schema["totals"]
        self.assertEqual(totals["incumbent_payload_bits"], 1228)
        self.assertEqual(totals["abstract_certificate_payload_bits"], 1063)
        self.assertEqual(totals["payload_bits_saved"], 165)
        self.assertEqual(totals["incumbent_verifier_bit_tests"], 542)
        self.assertEqual(totals["certificate_verifier_bit_tests"], 520)
        self.assertEqual(totals["verifier_bit_test_delta"], -22)
        deltas = {
            int(instance["input_length"]): int(
                instance["verification_cost"]["verifier_bit_test_delta"]
            )
            for instance in self.schema["instances"]
            if instance["source_id"] == "M93"
        }
        self.assertEqual(deltas[16], 5)
        self.assertEqual(deltas[24], 0)

    def test_rank_two_profile_does_not_determine_exact_minimum(self) -> None:
        boundary = self.schema["rank_two_boundary_counterexample"]
        CHECKER.validate_boundary(boundary)
        self.assertEqual(
            boundary["star_k1_3"]["exact_cover_number"],
            1,
        )
        self.assertEqual(
            boundary["path_p4"]["exact_cover_number"],
            2,
        )

    def test_k2_component_collapses_incident_edge_types(self) -> None:
        def incident_types(
            vertices: tuple[str, ...],
            edges: tuple[tuple[str, str], ...],
        ) -> tuple[frozenset[int], ...]:
            return tuple(
                frozenset(
                    edge_index
                    for edge_index, edge in enumerate(edges)
                    if vertex in edge
                )
                for vertex in vertices
            )

        k2_types = incident_types(("T0", "T1"), (("T0", "T1"),))
        self.assertEqual(k2_types[0], k2_types[1])
        star_types = incident_types(
            ("T0", "T1", "T2", "T3"),
            (("T0", "T1"), ("T0", "T2"), ("T0", "T3")),
        )
        self.assertEqual(len(star_types), len(set(star_types)))

    def test_rehashed_coverer_trace_mutation_is_rejected(self) -> None:
        schema = copy.deepcopy(self.schema)
        schema["instances"][0]["coverer_sets"][0][
            "coverer_type_ids"
        ] = ["T1"]
        rehash(schema)
        with self.assertRaisesRegex(AssertionError, "coverer sets"):
            CHECKER.validate_all(schema)

    def test_rehashed_source_anchor_mutation_is_rejected(self) -> None:
        schema = copy.deepcopy(self.schema)
        schema["sources"][0]["file_sha256"] = "0" * 64
        rehash(schema)
        with self.assertRaisesRegex(AssertionError, "source anchors"):
            CHECKER.validate_all(schema)

    def test_rehashed_scope_mutation_is_rejected(self) -> None:
        schema = copy.deepcopy(self.schema)
        schema["scope"]["not_claimed"].pop()
        rehash(schema)
        with self.assertRaisesRegex(AssertionError, "scope boundary"):
            CHECKER.validate_all(schema)

    def test_rehashed_coverage_mask_mutation_is_rejected(self) -> None:
        schema = copy.deepcopy(self.schema)
        schema["instances"][0]["coverage_types"][0][
            "coverage_mask_hex"
        ] = "0"
        rehash(schema)
        with self.assertRaisesRegex(AssertionError, "coverage masks"):
            CHECKER.validate_all(schema)

    def test_rehashed_template_kind_mutation_is_rejected(self) -> None:
        schema = copy.deepcopy(self.schema)
        schema["instances"][0]["template_kind"] = "loop_only"
        rehash(schema)
        with self.assertRaisesRegex(AssertionError, "graph template"):
            CHECKER.validate_all(schema)

    def test_rehashed_cost_mutation_is_rejected(self) -> None:
        schema = copy.deepcopy(self.schema)
        schema["instances"][1]["verification_cost"][
            "payload_bits_saved"
        ] += 1
        rehash(schema)
        with self.assertRaisesRegex(AssertionError, "verification cost"):
            CHECKER.validate_all(schema)

    def test_rehashed_boundary_mutation_is_rejected(self) -> None:
        schema = copy.deepcopy(self.schema)
        schema["rank_two_boundary_counterexample"]["path_p4"][
            "exact_cover_number"
        ] = 1
        rehash(schema)
        with self.assertRaisesRegex(AssertionError, "registered minimum"):
            CHECKER.validate_all(schema)

    def test_source_rebound_rank_three_column_is_rejected(self) -> None:
        source = copy.deepcopy(self.sources["M93"]["instances"][0])
        instance = copy.deepcopy(
            next(
                record
                for record in self.schema["instances"]
                if record["source_id"] == "M93"
                and int(record["input_length"]) == 16
            )
        )
        source_replacement = copy.deepcopy(source["coverage_types"][0])
        source_replacement["type_id"] = "T2"
        source["coverage_types"][2] = source_replacement
        instance["coverage_types"][2] = {
            "type_id": "T2",
            "pattern": copy.deepcopy(source_replacement["pattern"]),
            "coverage_mask_hex": source_replacement["coverage_mask_hex"],
        }
        buckets = tuple(
            tuple(int(point) for point in bucket)
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
        instance["source_instance_sha256"] = CHECKER.canonical_hash(source)
        with self.assertRaisesRegex(AssertionError, "rank exceeds two"):
            CHECKER.validate_instance(instance, "M93", source)

    def test_template_slots_are_duplicate_free(self) -> None:
        for instance in self.schema["instances"]:
            type_ids = tuple(
                record["type_id"] for record in instance["coverage_types"]
            )
            slots = CHECKER.template_slots(
                type_ids,
                instance["template_kind"],
            )
            self.assertEqual(len(slots), len(set(slots)))
            self.assertEqual(
                sorted(slots),
                sorted(
                    tuple(record["coverer_type_ids"])
                    for record in instance["coverer_sets"]
                ),
            )


if __name__ == "__main__":
    unittest.main()
