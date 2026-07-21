from __future__ import annotations

import argparse
import csv
from pathlib import Path

from semimagic_core import magic_transversal_count


CELLS = "abcdefghi"


def transversal_count(row: dict[str, str]) -> int:
    values = tuple(int(row[f"value_{cell}"]) for cell in CELLS)
    return magic_transversal_count(values, int(row["magic_sum"]))


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
