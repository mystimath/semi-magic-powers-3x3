from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from functools import reduce
from math import gcd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from lo_shu_parametrization import validate_semimagic_grid  # noqa: E402
from lo_shu_search import search_seven_line_square_classes  # noqa: E402
from semimagic_core import magic_transversal_count  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Exporte le catalogue direct des carrés semi-magiques à transversale magique."
    )
    parser.add_argument("--max-root", type=int, required=True)
    parser.add_argument("--json-out", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.max_root < 1:
        raise SystemExit("--max-root doit être strictement positif.")

    started = time.perf_counter()
    result = search_seven_line_square_classes(args.max_root)
    elapsed = time.perf_counter() - started
    classes: list[dict[str, object]] = []
    for item in result.classes:
        values = tuple(root * root for root in item.roots)
        validation = validate_semimagic_grid(values)
        transversal_count = magic_transversal_count(values, item.magic_sum)
        if not validation["accepted"] or not validation["all_entries_square"]:
            raise RuntimeError("Validation Lo Shu échouée.")
        if transversal_count < 1:
            raise RuntimeError("Une classe exportée n'a pas de transversale magique.")
        classes.append(
            {
                "max_root": max(item.semimagic_key),
                "magic_sum": item.magic_sum,
                "roots": list(item.roots),
                "canonical_roots": list(item.semimagic_key),
                "root_gcd": reduce(gcd, item.semimagic_key),
                "is_primitive": item.is_primitive,
                "magic_transversal_count_in_orientation": transversal_count,
            }
        )
    primitive = sorted(
        (row for row in classes if row["is_primitive"]),
        key=lambda row: int(row["max_root"]),
    )
    payload = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "algorithm": "lo_shu_difference_index",
        "max_root": args.max_root,
        "positive_roots": True,
        "distinct_roots": True,
        "elapsed_seconds": elapsed,
        "stats": result.stats,
        "class_count": len(classes),
        "primitive_count": len(primitive),
        "primitive_max_roots": [row["max_root"] for row in primitive],
        "classes": classes,
    }
    output = args.json_out or PROJECT_ROOT / "reports" / "lo_shu" / (
        f"direct_catalog_R{args.max_root}.json"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "artifact": str(output),
                "class_count": payload["class_count"],
                "primitive_count": payload["primitive_count"],
                "primitive_max_roots": payload["primitive_max_roots"],
                "elapsed_seconds": elapsed,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())