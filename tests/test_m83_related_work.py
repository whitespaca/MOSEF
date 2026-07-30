"""Regression tests for the M83 related-work audit."""

from __future__ import annotations

import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from types import ModuleType
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def load_checker() -> ModuleType:
    """Load the independent checker without making scripts a package."""
    path = ROOT / "scripts" / "check_m83_related_work.py"
    spec = importlib.util.spec_from_file_location("check_m83_related_work", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load M83 checker")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


CHECKER = load_checker()


class RelatedWorkAuditTests(unittest.TestCase):
    """Check valid audit structure and important mutation paths."""

    def setUp(self) -> None:
        self.manifest: dict[str, Any] = json.loads(
            CHECKER.MANIFEST.read_text(encoding="utf-8")
        )

    def test_registered_audit_passes(self) -> None:
        self.assertEqual(CHECKER.validate(), [])

    def test_positive_priority_status_is_rejected(self) -> None:
        altered = copy.deepcopy(self.manifest)
        altered["rows"][0]["priority_status"] = "PLAUSIBLY_NEW"
        errors = CHECKER.validate_manifest(altered)
        self.assertIn("M83-R01 unsupported priority status", errors)

    def test_classification_drift_is_rejected(self) -> None:
        altered = copy.deepcopy(self.manifest)
        altered["rows"][4]["classification"] = "ESTABLISHED_BACKGROUND"
        errors = CHECKER.validate_manifest(altered)
        self.assertIn("M83-R05 classification mismatch", errors)

    def test_bilingual_marker_drift_is_rejected(self) -> None:
        english = CHECKER.MATRIX_EN.read_text(encoding="utf-8")
        korean = CHECKER.MATRIX_KO.read_text(encoding="utf-8")
        altered = korean.replace("M83-R05|", "M83-R08|", 1)
        errors = CHECKER.validate_matrix_pair(english, altered)
        self.assertIn("Korean matrix marker sequence mismatch", errors)

    def test_abstract_only_promotion_is_rejected(self) -> None:
        source = (
            ROOT / "research" / "literature" / "SRC-012-yao-evaluation-powers.md"
        ).read_text(encoding="utf-8")
        altered = source.replace("`ABSTRACT_ONLY`", "`FULL_ARTICLE`", 1)
        errors = CHECKER.validate_source_record("SRC-012", "ABSTRACT_ONLY", altered)
        self.assertIn("SRC-012 inspection level mismatch", errors)

    def test_missing_source_hash_is_rejected(self) -> None:
        altered = copy.deepcopy(self.manifest)
        altered["source_sha256"].pop("paper/references.bib")
        errors = CHECKER.validate_manifest(altered)
        self.assertIn("source hash path set mismatch", errors)

    def test_missing_paper_citation_is_rejected(self) -> None:
        path = "paper/focused/promise-factorization-en.tex"
        text = (ROOT / path).read_text(encoding="utf-8")
        altered = text.replace(r"\cite{pollard1974theorems}", "", 1)
        errors = CHECKER.validate_paper(
            path,
            altered,
            CHECKER.REQUIRED_PAPER_ROWS[path],
            CHECKER.REQUIRED_CITATIONS[path],
        )
        self.assertIn(f"{path} citation missing: pollard1974theorems", errors)

    def test_summary_hash_tamper_is_rejected(self) -> None:
        altered = copy.deepcopy(self.manifest)
        altered["audit_summary_sha256"] = "0" * 64
        errors = CHECKER.validate_manifest(altered)
        self.assertIn("audit summary hash mismatch", errors)

    def test_source_hash_normalizes_line_endings(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "source.txt"
            path.write_bytes(b"alpha\r\nbeta\r\n")
            crlf_hash = CHECKER.sha256_text_file(path)
            path.write_bytes(b"alpha\nbeta\n")
            self.assertEqual(crlf_hash, CHECKER.sha256_text_file(path))


if __name__ == "__main__":
    unittest.main()
