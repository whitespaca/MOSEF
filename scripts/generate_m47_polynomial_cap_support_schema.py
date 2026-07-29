"""Generate the registered M47 polynomial-cap support-budget schema."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "python")]

from scripts.run_m47_polynomial_cap_support_audit import build_summary

SCHEMA = ROOT / "schemas/m47-polynomial-cap-support-v1.json"


def main() -> int:
    """Write the deterministic M47 schema."""
    SCHEMA.write_text(
        json.dumps(build_summary(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(SCHEMA.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
