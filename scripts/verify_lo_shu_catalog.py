from __future__ import annotations

import argparse
import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from lo_shu_search import search_seven_line_square_classes  # noqa: E402

CELLS = "abcdefghi"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Compare exactement la recherche Lo Shu au catalogue de transversales."
    )
    parser.add_argument("catalog", type=Path)
    parser.add_argument("--max-root", type=int, required=True)
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args()

    with args.catalog.open(newline="", encoding="utf-8-sig") as handle:
        published = {
            tuple(int(row[f"root_{cell}"]) for cell in CELLS)
            for row in csv.DictReader(handle)
        }
    result = search_seven_line_square_classes(args.max_root)
    generated = {item.semimagic_key for item in result.classes}
    missing = sorted(published - generated)
    unexpected = sorted(generated - published)
    payload = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "catalog": str(args.catalog.resolve()),
        "max_root": args.max_root,
        "published_classes": len(published),
        "generated_classes": len(generated),
        "exact_set_equality": not missing and not unexpected,
        "missing": [list(item) for item in missing],
        "unexpected": [list(item) for item in unexpected],
        "generated_stats": result.stats,
    }
    output = args.json_out or PROJECT_ROOT / "reports" / "lo_shu" / (
        f"catalog_verification_R{args.max_root}.json"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if payload["exact_set_equality"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
