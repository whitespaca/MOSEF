"""Generate the registered M32 threshold and certificate vectors."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "python"))
from mosef_reference import ExceptionalSelectorDescriptor, primitive_exit_mask

from scripts.run_m32_widened_selector_cap_audit import build_summary

SCHEMA = ROOT / "schemas/m32-widened-selector-cap-v1.json"
PRIMITIVE_CASES = (
    ("phi4", 19, 3, 5, 191),
    ("phi4", 19, 3, 5, 227),
    ("phi4", 11, 19, 2, 227),
    ("phi4", 11, 19, 2, 233),
    ("phi4", 19, 11, 3, 277),
    ("phi4", 19, 11, 3, 317),
    ("phi4", 7, 15, 19, 263),
    ("phi4", 7, 15, 19, 349),
    ("phi4", 27, 19, 27, 503),
    ("phi4", 27, 19, 27, 509),
    ("phi4", 11, 15, 27, 569),
    ("phi4", 11, 15, 27, 719),
    ("phi4", 23, 31, 21, 809),
    ("phi4", 23, 31, 21, 827),
    ("phi4", 3, 7, 19, 19),
    ("phi4", 3, 19, 2, 19),
    ("phi6", 5, 21, 2, 7),
)


def main() -> int:
    """Write the deterministic schema after rerunning the registered audit."""
    schema = build_summary()
    schema["primitive_exit_bit_order"] = (
        "base",
        "first_stage",
        "second_stage",
        "first_public_bound",
        "second_public_bound",
        "cyclotomic",
        "overlap_resultant",
        "cofactor",
    )
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
