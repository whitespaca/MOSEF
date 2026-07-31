"""Generate the registered M93 early repair certificate schema."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.run_m93_early_repair_audit import build_summary

SCHEMA = ROOT / "schemas" / "m93-early-repair-certificates-v1.json"


def main() -> int:
    """Write the deterministic registered schema."""
    SCHEMA.write_text(
        json.dumps(build_summary(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(SCHEMA.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
