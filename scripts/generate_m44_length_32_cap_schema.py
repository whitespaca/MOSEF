"""Generate registered M44 length-32 cap vectors."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "python"))

from mosef_reference import ExceptionalSelectorDescriptor, primitive_exit_mask

from scripts.run_m44_length_32_cap_audit import build_summary

SCHEMA = ROOT / "schemas/m44-length-32-cap-v1.json"
PRIMITIVE_CASES = (
    ("phi4", 167, 119, 93, 59699),
    ("phi4", 167, 119, 93, 63463),
    ("phi4", 119, 47, 149, 46549),
    ("phi6", 47, 153, 132, 59651),
)


def main() -> int:
    """Write the deterministic M44 schema."""
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
