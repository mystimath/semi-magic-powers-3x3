from __future__ import annotations

from itertools import permutations
from typing import Sequence

from lo_shu_parametrization import canonicalize_semimagic_grid
from semimagic_core import Grid, is_semimagic, permute_grid, transpose_grid


def canonicalize_semimagic_class(grid: Sequence[int]) -> dict[str, object]:
    """Trouve un témoin Lo Shu dans l'orbite S3×S3/transposition du catalogue.

    Cette opération est distincte de la canonicalisation D4. Les permutations
    de lignes et de colonnes servent ici uniquement à comparer une classe du
    catalogue général avec la sous-famille possédant une transversale magique.
    """

    flat = tuple(grid)
    if len(flat) != 9:
        raise ValueError("Une grille 3×3 doit contenir exactement neuf valeurs.")
    if not is_semimagic(flat):
        raise ValueError("La grille n'est pas semi-magique.")
    orders = tuple(permutations((0, 1, 2)))
    candidates: list[tuple[tuple[int, ...], str, dict[str, object]]] = []
    bases: tuple[tuple[bool, Grid], ...] = (
        (False, flat),  # type: ignore[arg-type]
        (True, transpose_grid(flat)),
    )
    for transposed, base in bases:
        for row_order in orders:
            for column_order in orders:
                transformed = permute_grid(base, row_order, column_order)
                try:
                    report = canonicalize_semimagic_grid(transformed)
                except ValueError:
                    continue
                symmetry_id = (
                    f"transpose={int(transposed)};rows={row_order};cols={column_order}"
                )
                candidates.append(
                    (report["canonical_key"], symmetry_id, report)  # type: ignore[arg-type]
                )
    if not candidates:
        raise ValueError("La classe semi-magique ne possède aucune transversale magique.")
    _, semimagic_symmetry_id, selected = min(candidates, key=lambda item: item[0])
    result = dict(selected)
    result["semimagic_symmetry_id"] = semimagic_symmetry_id
    return result
