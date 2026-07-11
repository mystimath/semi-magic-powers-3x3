from __future__ import annotations

import argparse
from collections import Counter

from semimagic_core import build_triple_groups, triple_count


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Profile les collisions de sommes de triples de puissances."
    )
    parser.add_argument("--power", type=int, choices=(3, 4), required=True)
    parser.add_argument("--max-root", type=int, required=True)
    parser.add_argument(
        "--distinct-roots",
        action=argparse.BooleanOptionalAction,
        default=True,
    )
    parser.add_argument(
        "--positive",
        action=argparse.BooleanOptionalAction,
        default=True,
    )
    parser.add_argument("--top", type=int, default=20)
    parser.add_argument("--progress", type=int, default=100_000)
    return parser.parse_args()


def progress(done: int, total: int) -> None:
    percent = 100.0 * done / total if total else 100.0
    print(
        f"\rTriples générés : {done:,}/{total:,} ({percent:6.2f} %)",
        end="",
        flush=True,
    )
    if done >= total:
        print()


def main() -> int:
    args = parse_args()
    groups, _, _ = build_triple_groups(
        max_root=args.max_root,
        power=args.power,
        distinct_roots=args.distinct_roots,
        positive=args.positive,
        progress_every=args.progress,
        progress_callback=progress if args.progress > 0 else None,
    )

    distribution = Counter(len(triples) for triples in groups.values())
    ranked = sorted(groups.items(), key=lambda item: (-len(item[1]), item[0]))

    print("=" * 72)
    print(f"Puissance               : {args.power}")
    print(f"Racine maximale         : {args.max_root}")
    print(
        f"Triples théoriques      : "
        f"{triple_count(args.max_root, args.distinct_roots, args.positive):,}"
    )
    print(f"Sommes distinctes       : {len(groups):,}")
    print("Distribution des tailles de groupes :")
    for size in sorted(distribution):
        print(f"  {size:>4} triple(s) : {distribution[size]:,} somme(s)")

    print()
    print(f"Top {args.top} des sommes les plus collisionnelles :")
    for target_sum, triples in ranked[: args.top]:
        print(f"  S={target_sum:<24} triples={len(triples):>5}")
        for triple in triples[:10]:
            print(f"      {triple}")
        if len(triples) > 10:
            print(f"      ... {len(triples) - 10} autre(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
