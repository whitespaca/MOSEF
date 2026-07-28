"""Generate registered M34 next-envelope vectors."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "python"))
from mosef_reference import ExceptionalSelectorDescriptor, primitive_exit_mask

from scripts.run_m34_next_envelope_audit import build_summary

SCHEMA = ROOT / "schemas/m34-next-envelope-v1.json"
PRIMITIVE_CASES = (
    ("phi4", 39, 23, 16, 1481),
    ("phi4", 39, 23, 16, 1571),
    ("phi6", 17, 39, 15, 1481),
    ("phi6", 17, 39, 15, 1571),
)


def main() -> int:
    """Write the deterministic M34 schema."""
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
