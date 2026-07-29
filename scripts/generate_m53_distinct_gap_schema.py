"""Generate the registered M53 distinct-gap schema."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "python")]

from scripts.run_m53_distinct_gap_audit import build_summary

SCHEMA = ROOT / "schemas/m53-distinct-gap-v1.json"


def main() -> int:
    SCHEMA.write_text(
        json.dumps(build_summary(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(SCHEMA.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
