"""Generate registered M45 length-33 cap vectors."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "python")]

from mosef_reference import ExceptionalSelectorDescriptor, primitive_exit_mask

from scripts.run_m45_length_33_cap_audit import build_summary

SCHEMA = ROOT / "schemas/m45-length-33-cap-v1.json"
PRIMITIVE_CASES = (
    ("phi4", 195, 91, 20, 80309),
    ("phi4", 195, 91, 20, 92671),
    ("phi4", 155, 71, 175, 71039),
    ("phi6", 107, 171, 87, 91387),
)


def main() -> int:
    """Write the deterministic M45 schema."""
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
