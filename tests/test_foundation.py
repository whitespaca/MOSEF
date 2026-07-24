"""Regression tests for the M0 foundation contract."""

from __future__ import annotations

import copy
import importlib.util
import unittest
from pathlib import Path
from types import ModuleType
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def load_validator() -> ModuleType:
    """Load the foundation validator without making scripts a package."""
    path = ROOT / "scripts" / "validate_foundation.py"
    spec = importlib.util.spec_from_file_location("validate_foundation", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load foundation validator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


VALIDATOR = load_validator()


class FoundationTests(unittest.TestCase):
    """Check the valid example and important rejection paths."""

    def setUp(self) -> None:
        self.example: dict[str, Any] = VALIDATOR.load_json(VALIDATOR.EXAMPLE_PATH)

    def test_complete_foundation_passes(self) -> None:
        self.assertEqual(VALIDATOR.validate_foundation(), [])

    def test_example_record_passes(self) -> None:
        self.assertEqual(VALIDATOR.validate_record(self.example), [])

    def test_missing_required_field_fails(self) -> None:
        record = copy.deepcopy(self.example)
        del record["seed"]
        self.assertTrue(
            any("missing top-level fields" in error for error in VALIDATOR.validate_record(record))
        )

    def test_invalid_hash_and_status_fail(self) -> None:
        record = copy.deepcopy(self.example)
        record["stdout_sha256"] = "not-a-hash"
        record["status"] = "SUCCESS"
        errors = VALIDATOR.validate_record(record)
        self.assertTrue(any("stdout_sha256" in error for error in errors))
        self.assertTrue(any("status must be one of" in error for error in errors))

    def test_boolean_is_not_accepted_as_integer(self) -> None:
        record = copy.deepcopy(self.example)
        record["host"]["logical_cores"] = True
        errors = VALIDATOR.validate_record(record)
        self.assertTrue(any("logical_cores" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
