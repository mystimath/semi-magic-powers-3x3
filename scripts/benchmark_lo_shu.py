from __future__ import annotations

import argparse
import csv
import json
import platform
import sys
import time
from datetime import datetime, timezone
from itertools import combinations, permutations
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from lo_shu_search import search_seven_line_square_classes  # noqa: E402
from semimagic_core import (  # noqa: E402
    Grid,
    build_triple_groups,
    canonical_grid,
    derive_third_row,
    unique_permutations,
)


def has_magic_transversal(roots: tuple[int, ...], target: int) -> bool:
    values = tuple(root * root for root in roots)
    return any(
        sum(values[3 * row + order[row]] for row in range(3)) == target
        for order in permutations(range(3))
    )


def general_oracle(max_root: int) -> tuple[set[Grid], dict[str, int]]:
    """Oracle général, avec filtre transversal avant la canonicalisation S3×S3."""

    groups, root_to_value, value_to_root = build_triple_groups(max_root, 2)
    classes: set[Grid] = set()
    stats = {
        "root_triples": sum(map(len, groups.values())),
        "distinct_sums": len(groups),
        "candidate_sums": 0,
        "triple_pairs": 0,
        "disjoint_pairs": 0,
        "row_alignments": 0,
        "square_third_rows": 0,
        "distinct_semimagic_candidates": 0,
        "transversal_candidates": 0,
        "transversal_classes": 0,
    }
    for target, triples in groups.items():
        if len(triples) < 2:
            continue
        stats["candidate_sums"] += 1
        for first, second in combinations(triples, 2):
            stats["triple_pairs"] += 1
            if set(first) & set(second):
                continue
            stats["disjoint_pairs"] += 1
            first_values = tuple(root_to_value[root] for root in first)
            for aligned_second in unique_permutations(second):
                stats["row_alignments"] += 1
                second_values = tuple(root_to_value[root] for root in aligned_second)
                third_values = derive_third_row(target, first_values, second_values)
                if any(value not in value_to_root for value in third_values):
                    continue
                stats["square_third_rows"] += 1
                third = tuple(value_to_root[value] for value in third_values)
                roots = first + aligned_second + third
                if len(set(roots)) != 9:
                    continue
                stats["distinct_semimagic_candidates"] += 1
                if not has_magic_transversal(roots, target):
                    continue
                stats["transversal_candidates"] += 1
                classes.add(canonical_grid(roots))
    stats["transversal_classes"] = len(classes)
    return classes, stats


def measured(name: str, max_root: int) -> tuple[dict[str, object], set[Grid], dict[str, int]]:
    started_cpu = time.process_time()
    started_wall = time.perf_counter()
    if name == "general_sum_index":
        classes, stats = general_oracle(max_root)
    else:
        result = search_seven_line_square_classes(max_root)
        classes = {item.semimagic_key for item in result.classes}
        stats = result.stats
    return (
        {
            "engine": name,
            "wall_seconds": time.perf_counter() - started_wall,
            "cpu_seconds": time.process_time() - started_cpu,
            "class_count": len(classes),
        },
        classes,
        stats,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Benchmark borné de la spécialisation Lo Shu.")
    parser.add_argument("--max-root", type=int, default=127)
    parser.add_argument("--json-out", type=Path)
    parser.add_argument("--csv-out", type=Path)
    args = parser.parse_args()
    if args.max_root < 3:
        raise SystemExit("--max-root doit être au moins 3")

    general_row, general_classes, general_stats = measured("general_sum_index", args.max_root)
    specialized_row, specialized_classes, specialized_stats = measured(
        "lo_shu_difference_index", args.max_root
    )
    if general_classes != specialized_classes:
        raise RuntimeError("Les ensembles de classes diffèrent.")
    speedup = float(general_row["wall_seconds"]) / float(specialized_row["wall_seconds"])
    payload = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version,
        "platform": platform.platform(),
        "domain": {
            "power": 2,
            "max_root": args.max_root,
            "positive_roots": True,
            "distinct_roots": True,
            "target": "semimagic classes with at least one magic transversal",
            "equivalence": "S3xS3 and transposition",
        },
        "runs": [general_row, specialized_row],
        "specialized_wall_speedup": speedup,
        "memory_note": "Mémoire de pointe non mesurée dans ce micro-benchmark.",
        "class_sets_equal": True,
        "classes": [list(key) for key in sorted(general_classes)],
        "general_stats": general_stats,
        "specialized_stats": specialized_stats,
    }
    json_out = args.json_out or PROJECT_ROOT / "reports" / "lo_shu" / (
        f"benchmark_R{args.max_root}.json"
    )
    csv_out = args.csv_out or PROJECT_ROOT / "reports" / "lo_shu" / (
        f"benchmark_R{args.max_root}.csv"
    )
    json_out.parent.mkdir(parents=True, exist_ok=True)
    csv_out.parent.mkdir(parents=True, exist_ok=True)
    json_out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    with csv_out.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(general_row))
        writer.writeheader()
        writer.writerows((general_row, specialized_row))
    print(json.dumps({
        "class_count": len(general_classes),
        "class_sets_equal": True,
        "specialized_wall_speedup": speedup,
        "json": str(json_out),
        "csv": str(csv_out),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
