"""Generate the canonical M60--M80 synthesis schema."""

from __future__ import annotations

import json
from pathlib import Path

from run_m60_m80_synthesis_audit import build_summary

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "schemas/m60-m80-synthesis-v1.json"


def main() -> int:
    OUTPUT.write_text(
        json.dumps(build_summary(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
