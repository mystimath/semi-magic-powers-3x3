from __future__ import annotations

import argparse
import csv
from pathlib import Path

from semimagic_core import column_sums, format_grid, is_semimagic, row_sums


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Affiche et valide une solution exportée en CSV."
    )
    parser.add_argument("csv_file", type=Path)
    parser.add_argument("--index", type=int, default=0)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.index < 0:
        raise SystemExit("--index ne peut pas être négatif.")

    with args.csv_file.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    if not rows:
        raise SystemExit("Le fichier CSV ne contient aucune solution.")
    if args.index >= len(rows):
        raise SystemExit(
            f"Index {args.index} hors limites : le fichier contient {len(rows)} solution(s)."
        )

    record = rows[args.index]
    roots = tuple(int(record[f"root_{name}"]) for name in "abcdefghi")
    values = tuple(int(record[f"value_{name}"]) for name in "abcdefghi")

    print("=" * 72)
    print(f"Solution {args.index + 1}/{len(rows)}")
    print(f"Puissance : {record['power']}")
    print(f"Somme     : {record['magic_sum']}")
    print()
    print("Racines :")
    print(format_grid(roots))
    print()
    print("Puissances :")
    print(format_grid(values))
    print()
    print(f"Sommes des lignes   : {row_sums(values)}")
    print(f"Sommes des colonnes : {column_sums(values)}")
    print(f"Validation           : {'OK' if is_semimagic(values) else 'ÉCHEC'}")
    print("=" * 72)
    return 0 if is_semimagic(values) else 1


if __name__ == "__main__":
    raise SystemExit(main())
