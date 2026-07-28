"""Generate registered M33 recurrence and repair vectors."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "python"))
from mosef_reference import ExceptionalSelectorDescriptor, primitive_exit_mask

from scripts.run_m33_linear_cap_recurrence_audit import build_summary

SCHEMA = ROOT / "schemas/m33-linear-cap-recurrence-v1.json"
PRIMITIVE_CASES = (
    ("phi6", 17, 33, 15, 1031),
    ("phi6", 17, 33, 15, 1231),
    ("phi6", 17, 33, 15, 1433),
    ("phi6", 5, 33, 27, 1031),
    ("phi6", 5, 33, 27, 1319),
    ("phi6", 23, 33, 14, 1231),
    ("phi6", 23, 33, 14, 1433),
)


def main() -> int:
    """Write the deterministic M33 schema."""
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
