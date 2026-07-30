"""Generate the canonical M81 bit-length migration schema."""

from __future__ import annotations

import json
from pathlib import Path

from run_m81_bitlength_audit import build_summary

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "schemas/m81-bitlength-audit-v1.json"


def main() -> int:
    OUTPUT.write_text(
        json.dumps(build_summary(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
