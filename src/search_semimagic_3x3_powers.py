from __future__ import annotations

import argparse
import csv
import json
import sys
import time
from itertools import combinations, combinations_with_replacement
from pathlib import Path
from typing import Any

from semimagic_core import (
    build_triple_groups,
    canonical_grid,
    derive_third_row,
    format_grid,
    is_semimagic,
    triple_count,
    unique_permutations,
)

MAX_SAFE_TRIPLES = 5_000_000


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Recherche exacte de carrés semi-magiques 3×3 de puissances."
    )
    parser.add_argument("--power", type=int, choices=(2, 3, 4), required=True)
    parser.add_argument("--max-root", type=int, required=True)
    parser.add_argument(
        "--distinct-roots",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Impose neuf racines globalement distinctes.",
    )
    parser.add_argument(
        "--positive",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Utilise uniquement des racines strictement positives.",
    )
    parser.add_argument("--target", choices=("exact",), default="exact")
    parser.add_argument("--progress", type=int, default=100_000)
    parser.add_argument("--max-results", type=int, default=0)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--summary-json", type=Path)
    parser.add_argument(
        "--force-large",
        action="store_true",
        help="Lève la limite de sécurité de la version en mémoire.",
    )
    return parser.parse_args()


def print_progress(done: int, total: int) -> None:
    if total <= 0:
        return
    percent = 100.0 * done / total
    print(
        f"\rTriples générés : {done:,}/{total:,} ({percent:6.2f} %)",
        end="",
        flush=True,
    )
    if done >= total:
        print()


def roots_are_globally_distinct(*rows: tuple[int, int, int]) -> bool:
    roots = [root for row in rows for root in row]
    return len(roots) == len(set(roots))


def write_results(path: Path, results: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "power",
        "max_root",
        "magic_sum",
        *[f"root_{name}" for name in "abcdefghi"],
        *[f"value_{name}" for name in "abcdefghi"],
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)


def write_summary(path: Path, summary: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def main() -> int:
    args = parse_args()

    if args.max_root < 1:
        raise SystemExit("--max-root doit être supérieur ou égal à 1.")
    if args.max_results < 0:
        raise SystemExit("--max-results ne peut pas être négatif.")

    total_triples = triple_count(
        args.max_root,
        args.distinct_roots,
        args.positive,
    )
    if total_triples > MAX_SAFE_TRIPLES and not args.force_large:
        raise SystemExit(
            f"La recherche générerait {total_triples:,} triples, au-delà de la "
            f"limite de sécurité ({MAX_SAFE_TRIPLES:,}). "
            "Réduisez --max-root ou utilisez --force-large."
        )

    started = time.perf_counter()
    print("=" * 72)
    print("Recherche de carrés semi-magiques 3×3 de puissances")
    print("=" * 72)
    print(f"Puissance              : {args.power}")
    print(f"Racine maximale        : {args.max_root}")
    print(f"Racines distinctes     : {args.distinct_roots}")
    print(f"Racines positives      : {args.positive}")
    print(f"Triples théoriques     : {total_triples:,}")
    print()

    groups, root_to_value, value_to_root = build_triple_groups(
        max_root=args.max_root,
        power=args.power,
        distinct_roots=args.distinct_roots,
        positive=args.positive,
        progress_every=args.progress,
        progress_callback=print_progress if args.progress > 0 else None,
    )

    minimum_group_size = 2 if args.distinct_roots else 1
    candidate_groups = {
        target_sum: triples
        for target_sum, triples in groups.items()
        if len(triples) >= minimum_group_size
    }

    print(f"Sommes distinctes      : {len(groups):,}")
    print(
        f"Sommes avec ≥{minimum_group_size} triple(s) : "
        f"{len(candidate_groups):,}"
    )
    print()

    results: list[dict[str, Any]] = []
    seen_canonical: set[tuple[int, ...]] = set()
    triple_pairs_tested = 0
    row_alignments_tested = 0

    stop = False
    for target_sum, triples in sorted(candidate_groups.items()):
        pair_iterator = (
            combinations(triples, 2)
            if args.distinct_roots
            else combinations_with_replacement(triples, 2)
        )
        for roots_row_1, roots_row_2 in pair_iterator:
            triple_pairs_tested += 1

            if args.distinct_roots and set(roots_row_1) & set(roots_row_2):
                continue

            values_row_1 = tuple(root_to_value[root] for root in roots_row_1)

            for permuted_roots_row_2 in unique_permutations(roots_row_2):
                row_alignments_tested += 1
                values_row_2 = tuple(
                    root_to_value[root] for root in permuted_roots_row_2
                )
                values_row_3 = derive_third_row(
                    target_sum,
                    values_row_1,
                    values_row_2,
                )

                if any(value not in value_to_root for value in values_row_3):
                    continue

                roots_row_3 = tuple(value_to_root[value] for value in values_row_3)

                if args.positive and any(root <= 0 for root in roots_row_3):
                    continue

                if args.distinct_roots and not roots_are_globally_distinct(
                    roots_row_1,
                    permuted_roots_row_2,
                    roots_row_3,
                ):
                    continue

                values_grid = (
                    *values_row_1,
                    *values_row_2,
                    *values_row_3,
                )
                if not is_semimagic(values_grid):
                    raise RuntimeError("Erreur interne : grille candidate non semi-magique.")

                canonical = canonical_grid(values_grid)
                if canonical in seen_canonical:
                    continue
                seen_canonical.add(canonical)

                canonical_roots = tuple(value_to_root[value] for value in canonical)
                record: dict[str, Any] = {
                    "power": args.power,
                    "max_root": args.max_root,
                    "magic_sum": target_sum,
                }
                for name, root in zip("abcdefghi", canonical_roots):
                    record[f"root_{name}"] = root
                for name, value in zip("abcdefghi", canonical):
                    record[f"value_{name}"] = value
                results.append(record)

                print(f"Solution #{len(results)} — somme {target_sum}")
                print("Racines :")
                print(format_grid(canonical_roots))
                print("Puissances :")
                print(format_grid(canonical))
                print("-" * 72)

                if args.max_results and len(results) >= args.max_results:
                    stop = True
                    break
            if stop:
                break
        if stop:
            break

    elapsed = time.perf_counter() - started
    summary = {
        "power": args.power,
        "max_root": args.max_root,
        "distinct_roots": args.distinct_roots,
        "positive": args.positive,
        "target": args.target,
        "total_triples": total_triples,
        "distinct_sums": len(groups),
        "minimum_triples_per_candidate_sum": minimum_group_size,
        "candidate_sums": len(candidate_groups),
        "triple_pairs_tested": triple_pairs_tested,
        "row_alignments_tested": row_alignments_tested,
        "unique_solutions": len(results),
        "elapsed_seconds": round(elapsed, 6),
        "stopped_by_max_results": stop,
    }

    if args.out:
        write_results(args.out, results)
        print(f"CSV                     : {args.out}")
    if args.summary_json:
        write_summary(args.summary_json, summary)
        print(f"Résumé JSON             : {args.summary_json}")

    print()
    print("=" * 72)
    print(f"Solutions uniques       : {len(results):,}")
    print(f"Paires de triples       : {triple_pairs_tested:,}")
    print(f"Alignements testés      : {row_alignments_tested:,}")
    print(f"Temps total             : {elapsed:.3f} s")
    print("=" * 72)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("\nRecherche interrompue par l'utilisateur.", file=sys.stderr)
        raise SystemExit(130)
