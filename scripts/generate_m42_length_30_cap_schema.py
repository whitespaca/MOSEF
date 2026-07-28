"""Generate registered M42 length-30 cap vectors."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "python"))

from mosef_reference import ExceptionalSelectorDescriptor, primitive_exit_mask

from scripts.run_m42_length_30_cap_audit import build_summary

SCHEMA = ROOT / "schemas/m42-length-30-cap-v1.json"
PRIMITIVE_CASES = (
    ("phi4", 123, 59, 87, 28591),
    ("phi4", 123, 59, 87, 29387),
    ("phi4", 79, 123, 54, 28591),
    ("phi4", 79, 123, 54, 29387),
)


def main() -> int:
    """Write the deterministic M42 schema."""
    schema = build_summary()
    schema["primitive_exit_vectors"] = tuple(
        {
            "family": family,
            "first_factor": first,
            "second_factor": second,
            "base": base,
            "prime": prime,
            "expected_mask": primitive_exit_mask(
                ExceptionalSelectorDescriptor(family, first, second, base),
                prime,
            ),
        }
        for family, first, second, base, prime in PRIMITIVE_CASES
    )
    SCHEMA.write_text(
        json.dumps(schema, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(SCHEMA.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
