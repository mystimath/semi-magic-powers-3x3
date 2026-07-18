from __future__ import annotations

import argparse
import csv
import json
import platform
import statistics
import sys
import time
import tracemalloc
from datetime import datetime, timezone
from itertools import combinations, permutations
from pathlib import Path
from typing import Callable

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC))

from lo_shu_catalog import canonicalize_semimagic_class  # noqa: E402
from lo_shu_search import SevenLineSearchResult, search_seven_line_square_classes  # noqa: E402
from semimagic_core import (  # noqa: E402
    Grid,
    build_triple_groups,
    canonical_grid,
    derive_third_row,
    unique_permutations,
)

CELLS = "abcdefghi"


def has_magic_transversal(roots: Grid, target: int) -> bool:
    values = tuple(root * root for root in roots)
    return any(
        sum(values[3 * row + column_order[row]] for row in range(3)) == target
        for column_order in permutations(range(3))
    )


def search_general_transversal_classes(max_root: int) -> dict[str, object]:
    """Petit oracle exhaustif reprenant la logique du moteur général en mémoire."""

    groups, root_to_value, value_to_root = build_triple_groups(
        max_root=max_root,
        power=2,
        distinct_roots=True,
        positive=True,
    )
    candidates = {target: triples for target, triples in groups.items() if len(triples) >= 2}
    all_classes: set[Grid] = set()
    transversal_classes: set[Grid] = set()
    stats = {
        "root_triples": sum(len(triples) for triples in groups.values()),
        "distinct_sums": len(groups),
        "candidate_sums": len(candidates),
        "triple_pairs": 0,
        "disjoint_pairs": 0,
        "row_alignments": 0,
        "square_third_rows": 0,
        "semimagic_classes": 0,
        "transversal_classes": 0,
    }
    for target, triples in candidates.items():
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
                key = canonical_grid(roots)
                if key in all_classes:
                    continue
                all_classes.add(key)
                if has_magic_transversal(key, target):
                    transversal_classes.add(key)
    stats["semimagic_classes"] = len(all_classes)
    stats["transversal_classes"] = len(transversal_classes)
    return {"classes": tuple(sorted(transversal_classes)), "stats": stats}


def _measure(name: str, function: Callable[[], object], run: int) -> tuple[dict[str, object], object]:
    tracemalloc.start()
    started_cpu = time.process_time()
    started_wall = time.perf_counter()
    result = function()
    wall_seconds = time.perf_counter() - started_wall
    cpu_seconds = time.process_time() - started_cpu
    _, peak_bytes = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    row = {
        "engine": name,
        "run": run,
        "wall_seconds": wall_seconds,
        "cpu_seconds": cpu_seconds,
        "python_peak_bytes": peak_bytes,
    }
    return row, result


def benchmark(max_root: int, repeats: int) -> dict[str, object]:
    if max_root < 3:
        raise ValueError("La borne du benchmark doit être au moins 3.")
    if repeats < 1:
        raise ValueError("Le nombre de répétitions doit être positif.")
    rows: list[dict[str, object]] = []
    last_general: dict[str, object] | None = None
    last_specialized: SevenLineSearchResult | None = None
    for run in range(1, repeats + 1):
        general_row, general = _measure(
            "general_sum_index",
            lambda: search_general_transversal_classes(max_root),
            run,
        )
        specialized_row, specialized = _measure(
            "lo_shu_difference_index",
            lambda: search_seven_line_square_classes(max_root),
            run,
        )
        last_general = general  # type: ignore[assignment]
        last_specialized = specialized  # type: ignore[assignment]
        general_classes = set(last_general["classes"])
        specialized_classes = {item.semimagic_key for item in last_specialized.classes}
        if general_classes != specialized_classes:
            raise RuntimeError("Les deux moteurs ne produisent pas les mêmes classes.")
        general_row["class_count"] = len(general_classes)
        specialized_row["class_count"] = len(specialized_classes)
        rows.extend((general_row, specialized_row))
    assert last_general is not None and last_specialized is not None
    medians = {
        engine: {
            "wall_seconds": statistics.median(
                float(row["wall_seconds"]) for row in rows if row["engine"] == engine
            ),
            "cpu_seconds": statistics.median(
                float(row["cpu_seconds"]) for row in rows if row["engine"] == engine
            ),
            "python_peak_bytes": statistics.median(
                int(row["python_peak_bytes"]) for row in rows if row["engine"] == engine
            ),
        }
        for engine in ("general_sum_index", "lo_shu_difference_index")
    }
    speedup = (
        medians["general_sum_index"]["wall_seconds"]
        / medians["lo_shu_difference_index"]["wall_seconds"]
    )
    return {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version,
        "platform": platform.platform(),
        "domain": {
            "power": 2,
            "max_root": max_root,
            "positive_roots": True,
            "distinct_roots": True,
            "target": "semimagic classes with at least one magic transversal",
            "equivalence": "S3xS3 and transposition",
        },
        "repeats": repeats,
        "runs": rows,
        "medians": medians,
        "specialized_wall_speedup": speedup,
        "class_sets_equal": True,
        "class_count": len(last_specialized.classes),
        "classes": [list(item.semimagic_key) for item in last_specialized.classes],
        "general_stats": last_general["stats"],
        "specialized_stats": last_specialized.stats,
    }


def write_benchmark(payload: dict[str, object], json_out: Path, csv_out: Path) -> None:
    json_out.parent.mkdir(parents=True, exist_ok=True)
    csv_out.parent.mkdir(parents=True, exist_ok=True)
    json_out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    rows = payload["runs"]
    assert isinstance(rows, list) and rows
    with csv_out.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def convert_catalog(source: Path, output: Path, expected_count: int | None) -> int:
    converted: list[dict[str, object]] = []
    with source.open(newline="", encoding="utf-8-sig") as handle:
        for row in csv.DictReader(handle):
            values = tuple(int(row[f"value_{cell}"]) for cell in CELLS)
            try:
                report = canonicalize_semimagic_class(values)
            except ValueError:
                continue
            actual_max_root = max(int(row[f"root_{cell}"]) for cell in CELLS)
            converted.append(
                {
                    "source": str(source),
                    "class_name": f"max-root-{actual_max_root}-sum-{row['magic_sum']}",
                    "max_root": actual_max_root,
                    "magic_sum": report["magic_sum"],
                    "x": report["x"],
                    "r": report["r"],
                    "u": report["u"],
                    "v": report["v"],
                    "A": report["A"],
                    "B": report["B"],
                    "C": report["C"],
                    "diagonal_defect": report["diagonal_defect"],
                    "is_fully_magic": report["is_fully_magic"],
                    "all_entries_square": report["all_entries_square"],
                    "distinct_entries": len(set(values)) == 9,
                    "canonical_key": " ".join(map(str, report["canonical_key"])),
                }
            )
    converted.sort(key=lambda item: (int(item["max_root"]), int(item["magic_sum"])))
    if expected_count is not None and len(converted) != expected_count:
        raise RuntimeError(f"{len(converted)} classes converties, attendu {expected_count}.")
    output.parent.mkdir(parents=True, exist_ok=True)
    if not converted:
        raise RuntimeError("Aucune classe à transversal magique dans le catalogue.")
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(converted[0]))
        writer.writeheader()
        writer.writerows(converted)
    return len(converted)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compare les paramétrisations semi-magiques.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    bench = subparsers.add_parser("benchmark", help="Compare l'oracle général et Lo Shu.")
    bench.add_argument("--max-root", type=int, default=150)
    bench.add_argument("--repeats", type=int, default=3)
    bench.add_argument("--json-out", type=Path)
    bench.add_argument("--csv-out", type=Path)
    catalog = subparsers.add_parser("catalog", help="Convertit les classes à transversale.")
    catalog.add_argument("source", type=Path)
    catalog.add_argument("output", type=Path)
    catalog.add_argument("--expected-count", type=int)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.command == "catalog":
        count = convert_catalog(args.source, args.output, args.expected_count)
        print(f"{count} classes Lo Shu écrites dans {args.output}")
        return 0
    payload = benchmark(args.max_root, args.repeats)
    json_out = args.json_out or PROJECT_ROOT / "reports" / "lo_shu" / (
        f"benchmark_R{args.max_root}.json"
    )
    csv_out = args.csv_out or PROJECT_ROOT / "reports" / "lo_shu" / (
        f"benchmark_R{args.max_root}.csv"
    )
    write_benchmark(payload, json_out, csv_out)
    print(json.dumps({
        "class_count": payload["class_count"],
        "class_sets_equal": payload["class_sets_equal"],
        "specialized_wall_speedup": payload["specialized_wall_speedup"],
        "json": str(json_out),
        "csv": str(csv_out),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
