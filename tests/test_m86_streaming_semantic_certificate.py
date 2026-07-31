"""Regression and mutation tests for the streaming clean-room M86 checker."""

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
CHECKER_PATH = ROOT / "scripts" / "check_m86_m46_streaming_certificate.py"


def load_checker() -> ModuleType:
    """Load the standalone checker without packaging scripts."""
    spec = importlib.util.spec_from_file_location("check_m86_streaming", CHECKER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {CHECKER_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


CHECKER = load_checker()


class M86StreamingSemanticCertificateTests(unittest.TestCase):
    """Check frozen semantics, streaming assembly, and mutation rejection."""

    artifact: ClassVar[dict[str, Any]]
    report: ClassVar[Any]

    @classmethod
    def setUpClass(cls) -> None:
        cls.artifact = CHECKER.read_artifact()
        cls.report = CHECKER.validate_semantics(cls.artifact)

    def test_frozen_m46_artifact_passes(self) -> None:
        self.assertEqual(self.report.population_size, 3299)
        self.assertEqual(self.report.certificate_coordinate_count, 3298)
        self.assertEqual(self.report.certificate_pair_count, 5440051)
        self.assertEqual(self.report.certificate_evaluation_count, 10880102)
        self.assertEqual(self.report.predecessor_descriptor_count, 704261)
        self.assertEqual(self.report.new_descriptor_count, 10139)
        self.assertEqual(self.report.new_raw_coordinate_count, 81112)
        self.assertEqual(self.report.peak_signature_slots, 3299)

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
            {
                "__future__",
                "collections",
                "hashlib",
                "json",
                "math",
                "pathlib",
                "time",
                "typing",
            },
        )

    def test_streaming_assembly_matches_a_small_materialized_oracle(self) -> None:
        primes = (11, 13, 17)
        sources = (
            (CHECKER.Descriptor("phi4", 3, 7, 2), "first_stage"),
            (CHECKER.Descriptor("phi4", 3, 7, 3), "cofactor"),
            (CHECKER.Descriptor("phi6", 5, 3, 4), "second_stage"),
        )
        observed, evaluations = CHECKER.stream_certificate_signatures(
            primes,
            sources,
        )
        expected = tuple(
            sum(
                1 << index
                for index, (descriptor, kind) in enumerate(sources)
                if CHECKER.primitive_exit_hit(descriptor, kind, prime)
            )
            for prime in primes
        )
        self.assertEqual(observed, expected)
        self.assertEqual(evaluations, len(primes) * len(sources))

    def test_streamed_descriptor_counts_are_exact(self) -> None:
        self.assertEqual(CHECKER.descriptor_count(200), 704261)
        self.assertEqual(CHECKER.descriptor_count(201), 714400)

    def test_rehashed_population_mutation_is_rejected(self) -> None:
        mutated = copy.deepcopy(self.artifact)
        mutated["construction_certificate"]["primes"][-1] = 131069
        mutated["summary_sha256"] = CHECKER.canonical_hash(mutated)
        with self.assertRaisesRegex(AssertionError, "balanced population"):
            CHECKER.validate_semantics(mutated)

    def test_rehashed_descriptor_mutation_is_rejected(self) -> None:
        mutated = copy.deepcopy(self.artifact)
        mutated["construction_certificate"]["column_sources"][0] = (
            "phi4:7:3:202:first_stage"
        )
        mutated["summary_sha256"] = CHECKER.canonical_hash(mutated)
        with self.assertRaisesRegex(AssertionError, "cap-201 grammar"):
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

    def test_unique_repair_vector_is_recomputed(self) -> None:
        descriptor = CHECKER.Descriptor("phi6", 149, 201, 45)
        self.assertEqual(CHECKER.primitive_exit_mask(descriptor, 97927), 128)
        self.assertEqual(CHECKER.primitive_exit_mask(descriptor, 99527), 0)


if __name__ == "__main__":
    unittest.main()
