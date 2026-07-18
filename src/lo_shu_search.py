from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from math import gcd, isqrt
from typing import Iterable

from lo_shu_parametrization import (
    build_grid_from_abcr,
    canonicalize_semimagic_grid,
    validate_semimagic_grid,
)
from semimagic_core import Grid, canonical_grid


@dataclass(frozen=True, order=True)
class SquareProgression:
    low_root: int
    center_root: int
    high_root: int
    difference: int

    @property
    def first(self) -> int:
        return self.low_root * self.low_root

    @property
    def middle(self) -> int:
        return self.center_root * self.center_root

    @property
    def last(self) -> int:
        return self.high_root * self.high_root

    @property
    def roots(self) -> tuple[int, int, int]:
        return self.low_root, self.center_root, self.high_root


@dataclass(frozen=True)
class SevenLineClass:
    semimagic_key: Grid
    lo_shu_key: tuple[int, ...]
    canonical_grid: Grid
    roots: Grid
    magic_sum: int
    x: int
    r: int
    u: int
    v: int
    A: int
    B: int
    C: int
    is_fully_magic: bool
    is_primitive: bool


@dataclass(frozen=True)
class SevenLineSearchResult:
    max_root: int
    classes: tuple[SevenLineClass, ...]
    stats: dict[str, int]


def generate_square_progressions(max_root: int) -> tuple[SquareProgression, ...]:
    """Énumère une fois chaque progression croissante de trois carrés positifs."""

    if isinstance(max_root, bool) or not isinstance(max_root, int) or max_root < 1:
        raise ValueError("max_root doit être un entier strictement positif.")
    square_to_root = {root * root: root for root in range(1, max_root + 1)}
    progressions: list[SquareProgression] = []
    for low_root in range(1, max_root + 1):
        low = low_root * low_root
        for center_root in range(low_root + 1, max_root + 1):
            center = center_root * center_root
            high = 2 * center - low
            high_root = square_to_root.get(high)
            if high_root is None or high_root <= center_root:
                continue
            progressions.append(
                SquareProgression(
                    low_root=low_root,
                    center_root=center_root,
                    high_root=high_root,
                    difference=center - low,
                )
            )
    return tuple(progressions)


def _flat(nested: Iterable[Iterable[int]]) -> Grid:
    values = tuple(value for row in nested for value in row)
    if len(values) != 9:
        raise ValueError("Une grille 3×3 doit contenir neuf valeurs.")
    return values  # type: ignore[return-value]


def search_seven_line_square_classes(
    max_root: int,
    *,
    primitive_only: bool = False,
    fully_magic_only: bool = False,
) -> SevenLineSearchResult:
    """Cherche les classes à neuf carrés possédant un septième alignement.

    Les progressions sont regroupées par raison ``r``. Trois progressions de
    même raison construisent automatiquement une grille à sept alignements ;
    l'index S3×S3/transposition du moteur général sert à comparer les sorties au
    catalogue exhaustif, tandis que ``lo_shu_key`` conserve la géométrie D4.
    """

    progressions = generate_square_progressions(max_root)
    by_difference: dict[int, list[SquareProgression]] = {}
    for progression in progressions:
        by_difference.setdefault(progression.difference, []).append(progression)

    stats = {
        "progressions": len(progressions),
        "difference_groups": len(by_difference),
        "groups_with_at_least_three": 0,
        "progression_triplets": 0,
        "disjoint_progression_triplets": 0,
        "fully_magic_triplets": 0,
        "duplicate_semimagic_classes": 0,
        "accepted_classes": 0,
    }
    classes: dict[Grid, SevenLineClass] = {}
    for difference, group in sorted(by_difference.items()):
        if len(group) < 3:
            continue
        stats["groups_with_at_least_three"] += 1
        ordered = sorted(group, key=lambda progression: progression.first)
        for low, middle, high in combinations(ordered, 3):
            stats["progression_triplets"] += 1
            roots = low.roots + middle.roots + high.roots
            if len(set(roots)) != 9:
                continue
            stats["disjoint_progression_triplets"] += 1
            A, B, C = low.first, middle.first, high.first
            is_fully_magic = A + C == 2 * B
            if is_fully_magic:
                stats["fully_magic_triplets"] += 1
            if fully_magic_only and not is_fully_magic:
                continue
            grid = _flat(build_grid_from_abcr(A, B, C, difference))
            validation = validate_semimagic_grid(grid)
            if not validation["accepted"] or not validation["all_entries_square"]:
                raise ArithmeticError("Le générateur Lo Shu a produit une grille invalide.")
            report = canonicalize_semimagic_grid(grid)
            canonical_values = _flat(report["canonical_grid"])  # type: ignore[arg-type]
            canonical_roots = tuple(isqrt(value) for value in canonical_values)
            semimagic_key = canonical_grid(canonical_roots)
            root_gcd = gcd(*semimagic_key)
            if primitive_only and root_gcd != 1:
                continue
            candidate = SevenLineClass(
                semimagic_key=semimagic_key,
                lo_shu_key=report["canonical_key"],  # type: ignore[arg-type]
                canonical_grid=canonical_values,
                roots=canonical_roots,  # type: ignore[arg-type]
                magic_sum=int(report["magic_sum"]),
                x=int(report["x"]),
                r=int(report["r"]),
                u=int(report["u"]),
                v=int(report["v"]),
                A=int(report["A"]),
                B=int(report["B"]),
                C=int(report["C"]),
                is_fully_magic=bool(report["is_fully_magic"]),
                is_primitive=root_gcd == 1,
            )
            if semimagic_key in classes:
                stats["duplicate_semimagic_classes"] += 1
                if candidate.lo_shu_key < classes[semimagic_key].lo_shu_key:
                    classes[semimagic_key] = candidate
            else:
                classes[semimagic_key] = candidate

    frozen = tuple(classes[key] for key in sorted(classes))
    stats["accepted_classes"] = len(frozen)
    return SevenLineSearchResult(max_root=max_root, classes=frozen, stats=stats)
