"""Generate the canonical M59 half-order constraint schema."""

from __future__ import annotations

import json
from pathlib import Path

from run_m59_half_order_size_audit import build_summary

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "schemas/m59-half-order-size-v1.json"


def main() -> int:
    OUTPUT.write_text(
        json.dumps(build_summary(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
