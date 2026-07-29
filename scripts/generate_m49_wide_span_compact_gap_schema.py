"""Generate the registered M49 wide-span compact-gap schema."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "python")]

from scripts.run_m49_wide_span_compact_gap_audit import build_summary

SCHEMA = ROOT / "schemas/m49-wide-span-compact-gap-v1.json"


def main() -> int:
    """Write the deterministic M49 schema."""
    SCHEMA.write_text(
        json.dumps(build_summary(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(SCHEMA.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
