"""Generate registered M36 distinct-cap vectors."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "python"))
from mosef_reference import ExceptionalSelectorDescriptor, primitive_exit_mask

from scripts.run_m36_distinct_cap_audit import build_summary

SCHEMA = ROOT / "schemas/m36-distinct-cap-v1.json"
PRIMITIVE_CASES = (
    ("phi4", 43, 51, 23, 3049),
    ("phi4", 43, 51, 23, 4057),
    ("phi6", 23, 39, 51, 3049),
    ("phi6", 23, 39, 51, 4057),
)


def main() -> int:
    """Write the deterministic M36 schema."""
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
