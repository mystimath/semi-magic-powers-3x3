from __future__ import annotations

import argparse
import csv
from itertools import permutations
from pathlib import Path


CELLS = "abcdefghi"


def transversal_count(row: dict[str, str]) -> int:
    values = [int(row[f"value_{cell}"]) for cell in CELLS]
    grid = [values[0:3], values[3:6], values[6:9]]
    target = int(row["magic_sum"])
    return sum(
        grid[0][perm[0]] + grid[1][perm[1]] + grid[2][perm[2]] == target
        for perm in permutations(range(3))
    )


def write_rows(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyse les orbites d'un catalogue de carrés.")
    parser.add_argument("catalog", type=Path)
    parser.add_argument("--primitive-out", type=Path, required=True)
    parser.add_argument("--transversal-out", type=Path, required=True)
    args = parser.parse_args()

    with args.catalog.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise ValueError("catalogue vide")

    primitives = [row for row in rows if row["is_primitive"].lower() == "true"]
    hits: list[dict[str, object]] = []
    for row in rows:
        count = transversal_count(row)
        if count:
            hit: dict[str, object] = dict(row)
            hit["magic_transversal_count"] = count
            hits.append(hit)

    write_rows(args.primitive_out, primitives, list(rows[0]))
    write_rows(args.transversal_out, hits, list(rows[0]) + ["magic_transversal_count"])
    print(f"{len(rows)} classes; {len(primitives)} primitives; {len(hits)} classes à transversale magique")


if __name__ == "__main__":
    main()
