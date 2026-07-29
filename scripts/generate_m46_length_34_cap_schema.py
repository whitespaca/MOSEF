"""Generate registered M46 length-34 cap vectors."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "python")]

from mosef_reference import ExceptionalSelectorDescriptor, primitive_exit_mask

from scripts.run_m46_length_34_cap_audit import build_summary

SCHEMA = ROOT / "schemas/m46-length-34-cap-v1.json"
PRIMITIVE_CASES = (
    ("phi6", 149, 201, 45, 97927),
    ("phi6", 149, 201, 45, 99527),
    ("phi4", 199, 147, 116, 127877),
    ("phi6", 47, 195, 118, 97927),
)


def main() -> int:
    """Write the deterministic M46 schema."""
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
