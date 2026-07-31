"""Regression and mutation tests for the clean-room M85 checker."""

from __future__ import annotations

import ast
import copy
import importlib.util
import sys
import unittest
from pathlib import Path
from types import ModuleType
from typing import Any, ClassVar

ROOT = Path(__file__).resolve().parents[1]
CHECKER_PATH = ROOT / "scripts" / "check_m85_m41_semantic_certificate.py"


def load_checker() -> ModuleType:
    """Load the checker without making scripts a production package."""
    spec = importlib.util.spec_from_file_location("check_m85_semantic", CHECKER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {CHECKER_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


CHECKER = load_checker()


class M85SemanticCertificateTests(unittest.TestCase):
    """Check the trust boundary, frozen artifact, and semantic mutations."""

    artifact: ClassVar[dict[str, Any]]
    report: ClassVar[Any]

    @classmethod
    def setUpClass(cls) -> None:
        cls.artifact = CHECKER.read_artifact()
        cls.report = CHECKER.validate_semantics(cls.artifact)

    def test_frozen_m41_artifact_passes(self) -> None:
        self.assertEqual(self.report.population_size, 685)
        self.assertEqual(self.report.certificate_coordinate_count, 1528)
        self.assertEqual(self.report.certificate_pair_count, 234270)
        self.assertEqual(self.report.predecessor_descriptor_count, 89789)
        self.assertEqual(self.report.new_raw_coordinate_count, 47912)

    def test_checker_is_small_and_has_no_project_imports(self) -> None:
        source = CHECKER_PATH.read_text(encoding="utf-8")
        self.assertLess(len(source.splitlines()), 1000)
        tree = ast.parse(source)
        imported_roots: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported_roots.update(alias.name.split(".", 1)[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                if node.level:
                    self.fail("clean-room checker contains a relative import")
                if node.module:
                    imported_roots.add(node.module.split(".", 1)[0])
        self.assertLessEqual(
            imported_roots,
            {"__future__", "collections", "hashlib", "json", "math", "pathlib", "typing"},
        )

    def test_rehashed_population_mutation_is_rejected(self) -> None:
        mutated = copy.deepcopy(self.artifact)
        mutated["construction_certificate"]["primes"][-1] = 23161
        mutated["summary_sha256"] = CHECKER.canonical_hash(mutated)
        with self.assertRaisesRegex(AssertionError, "balanced population"):
            CHECKER.validate_semantics(mutated)

    def test_rehashed_descriptor_mutation_is_rejected(self) -> None:
        mutated = copy.deepcopy(self.artifact)
        mutated["construction_certificate"]["column_sources"][0] = (
            "phi4:7:3:104:first_stage"
        )
        mutated["summary_sha256"] = CHECKER.canonical_hash(mutated)
        with self.assertRaisesRegex(AssertionError, "cap-103 grammar"):
            CHECKER.validate_semantics(mutated)

    def test_rehashed_primitive_vector_mutation_is_rejected(self) -> None:
        mutated = copy.deepcopy(self.artifact)
        mutated["primitive_exit_vectors"][0]["expected_mask"] ^= 128
        mutated["summary_sha256"] = CHECKER.canonical_hash(mutated)
        with self.assertRaisesRegex(AssertionError, "primitive exit vector"):
            CHECKER.validate_semantics(mutated)

    def test_signature_mutation_is_rejected_semantically(self) -> None:
        registered = list(
            self.artifact["construction_certificate"]["restricted_signatures"]
        )
        registered[0] ^= 1
        with self.assertRaisesRegex(AssertionError, "restricted signatures"):
            CHECKER.check_registered_signatures(
                tuple(
                    int(value)
                    for value in self.artifact["construction_certificate"][
                        "restricted_signatures"
                    ]
                ),
                registered,
            )

    def test_repair_vector_is_recomputed(self) -> None:
        descriptor = CHECKER.Descriptor("phi4", 87, 95, 103)
        self.assertEqual(CHECKER.primitive_exit_mask(descriptor, 18979), 0)
        self.assertEqual(CHECKER.primitive_exit_mask(descriptor, 21031), 128)

    def test_derivative_branch_matches_an_exact_small_quotient(self) -> None:
        descriptor = CHECKER.Descriptor("phi4", 3, 7, 2)
        first_stage = sum(2**index for index in range(3))
        nested_base = 2**3
        second_stage = sum(nested_base**index for index in range(7))
        exact_cofactor, remainder = divmod(first_stage + second_stage, 2**2 + 1)
        self.assertEqual(remainder, 0)
        self.assertEqual(
            CHECKER.cofactor_residue(descriptor, 5),
            exact_cofactor % 5,
        )


if __name__ == "__main__":
    unittest.main()
