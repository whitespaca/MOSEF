"""Regression tests for the M50 finite-threshold publication artifact."""

from __future__ import annotations

import copy
import importlib.util
import unittest
from pathlib import Path
from types import ModuleType

ROOT = Path(__file__).resolve().parents[1]


def load_script(name: str) -> ModuleType:
    """Load one repository script without turning scripts into a package."""
    path = ROOT / "scripts" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


GENERATOR = load_script("generate_m50_finite_threshold_summary")
CHECKER = load_script("check_m50_finite_threshold_summary")


class FiniteThresholdSummaryTests(unittest.TestCase):
    """Check coverage, family-relative arithmetic, and scope boundaries."""

    def setUp(self) -> None:
        self.artifact = GENERATOR.build_artifact()

    def test_exact_finite_window(self) -> None:
        rows = self.artifact["rows"]
        self.assertEqual(
            [row["input_length"] for row in rows],
            list(range(9, 35)),
        )
        self.assertEqual(len(rows), 26)

    def test_known_nonmonotone_threshold(self) -> None:
        rows = {row["input_length"]: row for row in self.artifact["rows"]}
        self.assertEqual(rows[28]["family_relative_minimal_cap"], 104)
        self.assertEqual(rows[29]["family_relative_minimal_cap"], 103)

    def test_final_finite_threshold_and_scope(self) -> None:
        final = self.artifact["rows"][-1]
        self.assertEqual(final["population_size"], 3299)
        self.assertEqual(final["family_relative_minimal_cap"], 201)
        self.assertEqual(final["local_offset"], 167)
        self.assertEqual(final["strict_endpoint"]["reduced_numerator"], 100)
        self.assertEqual(final["strict_endpoint"]["reduced_denominator"], 17)
        self.assertEqual(final["predecessor_collision_buckets"], [[97927, 99527]])
        self.assertIn("no asymptotic rate", self.artifact["scope"])

    def test_only_certified_incremental_minima_are_numeric(self) -> None:
        rows = {row["input_length"]: row for row in self.artifact["rows"]}
        expected = {26: 2, 27: 5, 28: 5, 29: 1, 30: 2, 31: 1, 32: 1, 33: 1, 34: 1}
        observed = {
            input_length: row["repair_coordinate_count"]
            for input_length, row in rows.items()
            if row["repair_coordinate_status"] == "CERTIFIED_MINIMUM"
        }
        self.assertEqual(observed, expected)

    def test_canonical_hash_is_stable(self) -> None:
        self.assertEqual(
            self.artifact["summary_sha256"],
            GENERATOR.canonical_hash(self.artifact),
        )

    def test_checker_rejects_forged_repair_minimum(self) -> None:
        row = copy.deepcopy(self.artifact["rows"][-1])
        row["repair_coordinate_count"] = 0
        source = CHECKER.read_json(ROOT / row["source_schema"])
        with self.assertRaisesRegex(AssertionError, "repair-coordinate count"):
            CHECKER.check_source_projection(row, source)

    def test_checker_rejects_unreduced_endpoint_tampering(self) -> None:
        row = copy.deepcopy(self.artifact["rows"][-1])
        row["strict_endpoint"]["reduced_numerator"] = 200
        with self.assertRaisesRegex(AssertionError, "reduced endpoint numerator"):
            CHECKER.check_row_arithmetic(row)


if __name__ == "__main__":
    unittest.main()
