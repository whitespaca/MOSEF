"""Generate or check the canonical M99 OCT-discovery schema."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.run_m99_oct_discovery_profile import build_summary

OUTPUT = ROOT / "schemas" / "m99-oct-discovery-v1.json"


def main() -> int:
    """Generate the deterministic schema or check its current bytes."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    rendered = json.dumps(build_summary(), indent=2, ensure_ascii=False) + "\n"
    if args.check:
        if not OUTPUT.exists() or OUTPUT.read_text(encoding="utf-8") != rendered:
            raise SystemExit("M99 schema is stale; regenerate it")
        print("M99 OCT-discovery schema: PASS")
        return 0
    OUTPUT.write_text(rendered, encoding="utf-8", newline="\n")
    print(f"wrote {OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
