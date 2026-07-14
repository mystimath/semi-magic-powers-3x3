from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path


CELLS = "abcdefghi"


def enrich(row: dict[str, str]) -> dict[str, object]:
    roots = [int(row[f"root_{cell}"]) for cell in CELLS]
    values = [int(row[f"value_{cell}"]) for cell in CELLS]
    expected_values = [root * root for root in roots]
    if values != expected_values:
        raise ValueError("les valeurs ne sont pas les carrés des racines")
    if len(set(roots)) != 9 or min(roots) <= 0:
        raise ValueError("les neuf racines doivent être positives et distinctes")

    line_sums = [
        sum(values[0:3]), sum(values[3:6]), sum(values[6:9]),
        sum(values[0::3]), sum(values[1::3]), sum(values[2::3]),
    ]
    magic_sum = int(row["magic_sum"])
    if any(total != magic_sum for total in line_sums):
        raise ValueError("la grille n'est pas semi-magique")

    diagonal_1 = values[0] + values[4] + values[8]
    diagonal_2 = values[2] + values[4] + values[6]
    root_gcd = math.gcd(*roots)
    value_gcd = math.gcd(*values)
    result: dict[str, object] = dict(row)
    result.update(
        actual_max_root=max(roots),
        root_gcd=root_gcd,
        value_gcd=value_gcd,
        common_square_factor=root_gcd * root_gcd,
        is_primitive=root_gcd == 1,
        is_fully_magic=diagonal_1 == magic_sum and diagonal_2 == magic_sum,
        diagonal_1=diagonal_1,
        diagonal_2=diagonal_2,
    )
    return result


def build_catalog(source: Path) -> list[dict[str, object]]:
    with source.open(newline="", encoding="utf-8") as handle:
        rows = [enrich(row) for row in csv.DictReader(handle)]
    rows.sort(key=lambda row: (int(row["actual_max_root"]), int(row["magic_sum"])))
    return rows


def write_catalog(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError("catalogue vide")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Enrichit un catalogue de carrés semi-magiques.")
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--limit", type=int)
    args = parser.parse_args()
    rows = build_catalog(args.source)
    if args.limit is not None:
        rows = rows[: args.limit]
    write_catalog(args.output, rows)
    print(f"{len(rows)} classes écrites dans {args.output}")


if __name__ == "__main__":
    main()
