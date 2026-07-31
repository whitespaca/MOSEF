"""Generate or check the canonical M96 matching-certificate schema."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.run_m96_matching_certificate_profile import build_summary

SCHEMA = ROOT / "schemas" / "m96-matching-certificates-v1.json"


def main() -> int:
    """Write the schema, or verify it under --check."""
    rendered = json.dumps(build_summary(), indent=2, ensure_ascii=False) + "\n"
    if "--check" in sys.argv:
        if not SCHEMA.exists() or SCHEMA.read_text(encoding="utf-8") != rendered:
            raise SystemExit("M96 schema is stale; regenerate it")
        print("M96 matching-certificate schema: PASS")
        return 0
    SCHEMA.write_text(rendered, encoding="utf-8")
    print(f"Wrote {SCHEMA.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
