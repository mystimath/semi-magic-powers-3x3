from __future__ import annotations

from math import isqrt
from typing import Sequence

from semimagic_core import column_sums, is_semimagic, row_sums

FlatGrid = tuple[int, int, int, int, int, int, int, int, int]
NestedGrid = list[list[int]]
GridInput = Sequence[int] | Sequence[Sequence[int]]
StructuralKey = tuple[int, int, int, int, int, int, int, int, int]


def _flatten_grid(grid: GridInput) -> FlatGrid:
    if len(grid) == 3 and all(
        isinstance(row, Sequence) and not isinstance(row, (str, bytes))
        for row in grid
    ):
        rows = grid  # type: ignore[assignment]
        if any(len(row) != 3 for row in rows):
            raise ValueError("Chaque ligne doit contenir exactement trois valeurs.")
        values = tuple(value for row in rows for value in row)
    else:
        values = tuple(grid)  # type: ignore[arg-type]
    if len(values) != 9:
        raise ValueError("Une grille 3×3 doit contenir exactement neuf valeurs.")
    if any(isinstance(value, bool) or not isinstance(value, int) for value in values):
        raise TypeError("Les neuf valeurs doivent être des entiers, hors booléens.")
    return values  # type: ignore[return-value]


def _nested(grid: Sequence[int]) -> NestedGrid:
    flat = _flatten_grid(grid)
    return [list(flat[0:3]), list(flat[3:6]), list(flat[6:9])]


def is_square(n: int) -> bool:
    """Retourne si ``n`` est un carré parfait entier, zéro compris."""

    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError("Le test de carré attend un entier, hors booléen.")
    if n < 0:
        return False
    root = isqrt(n)
    return root * root == n


def build_grid_from_xruv(x: int, r: int, u: int, v: int) -> NestedGrid:
    """Construit la forme Lo Shu à sept alignements depuis ``(x,r,u,v)``."""

    if any(isinstance(value, bool) or not isinstance(value, int) for value in (x, r, u, v)):
        raise TypeError("x, r, u et v doivent être des entiers, hors booléens.")
    return [
        [x + 2 * r + u, x + 6 * r + u + v, x + r],
        [x + 2 * r, x + 3 * r + u, x + 4 * r + u + v],
        [x + 5 * r + u + v, x, x + 4 * r + u],
    ]


def build_grid_from_abcr(A: int, B: int, C: int, r: int) -> NestedGrid:
    """Construit la même forme depuis les premiers termes ``(A,B,C,r)``."""

    if any(isinstance(value, bool) or not isinstance(value, int) for value in (A, B, C, r)):
        raise TypeError("A, B, C et r doivent être des entiers, hors booléens.")
    return [
        [B, C + 2 * r, A + r],
        [A + 2 * r, B + r, C],
        [C + r, A, B + 2 * r],
    ]


def _structural_terms(grid: GridInput) -> StructuralKey:
    """Extrait ``(L1,L2,L3,M1,M2,M3,H1,H2,H3)`` de l'orientation donnée."""

    a, b, c, d, e, f, g, h, i = _flatten_grid(grid)
    return (h, c, d, a, e, i, f, g, b)


def extract_xruv_from_canonical_grid(grid: GridInput) -> tuple[int, int, int, int]:
    """Extrait les paramètres d'une grille déjà placée dans la convention Lo Shu.

    Les trois triplets structurels doivent être des progressions de même raison
    strictement positive. La fonction ne réoriente pas la grille ; cette tâche
    appartient à :func:`canonicalize_semimagic_grid`.
    """

    L1, L2, L3, M1, M2, M3, H1, H2, H3 = _structural_terms(grid)
    differences = (
        L2 - L1,
        L3 - L2,
        M2 - M1,
        M3 - M2,
        H2 - H1,
        H3 - H2,
    )
    if len(set(differences)) != 1:
        raise ValueError("Les trois triplets ne partagent pas une même raison.")
    r = differences[0]
    if r <= 0:
        raise ValueError("La convention canonique impose une raison r strictement positive.")
    x = L1
    u = M1 - L3
    v = H1 - M3
    if _flatten_grid(build_grid_from_xruv(x, r, u, v)) != _flatten_grid(grid):
        raise ArithmeticError("L'extraction Lo Shu n'a pas reconstruit la grille.")
    return x, r, u, v


def _rotate(grid: FlatGrid) -> FlatGrid:
    return (
        grid[6], grid[3], grid[0],
        grid[7], grid[4], grid[1],
        grid[8], grid[5], grid[2],
    )


def _reflect(grid: FlatGrid) -> FlatGrid:
    return (
        grid[2], grid[1], grid[0],
        grid[5], grid[4], grid[3],
        grid[8], grid[7], grid[6],
    )


def d4_orbit_with_ids(grid: GridInput) -> tuple[tuple[str, FlatGrid], ...]:
    """Retourne les huit images diédriques, avec des identifiants déterministes."""

    base = _flatten_grid(grid)
    transforms: list[tuple[str, FlatGrid]] = []
    current = base
    for turns in range(4):
        transforms.append((f"r{90 * turns}", current))
        transforms.append((f"r{90 * turns}_mirror", _reflect(current)))
        current = _rotate(current)
    unique: dict[FlatGrid, str] = {}
    for symmetry_id, transformed in transforms:
        unique.setdefault(transformed, symmetry_id)
    return tuple((symmetry_id, transformed) for transformed, symmetry_id in unique.items())


def _diagonal_sums(grid: FlatGrid) -> tuple[int, int]:
    return grid[0] + grid[4] + grid[8], grid[2] + grid[4] + grid[6]


def canonicalize_semimagic_grid(grid: GridInput) -> dict[str, object]:
    """Canonicalise sous D4 une grille à sept alignements ou pleinement magique.

    La clé stable est le tuple structurel complet. Contrairement à ``(x,r,u,v)``,
    elle rend la convention et l'absence de perte d'information immédiatement
    visibles. La canonicalisation générale des carrés semi-magiques du dépôt est
    plus large (S3×S3 et transposition) et répond à un autre besoin.
    """

    flat = _flatten_grid(grid)
    if not is_semimagic(flat):
        raise ValueError("La grille n'est pas semi-magique.")
    target = row_sums(flat)[0]
    candidates: list[tuple[StructuralKey, str, FlatGrid, tuple[int, int, int, int]]] = []
    for symmetry_id, transformed in d4_orbit_with_ids(flat):
        _, secondary = _diagonal_sums(transformed)
        if secondary != target:
            continue
        try:
            parameters = extract_xruv_from_canonical_grid(transformed)
        except ValueError:
            continue
        candidates.append((_structural_terms(transformed), symmetry_id, transformed, parameters))
    if not candidates:
        raise ValueError(
            "Aucune orientation D4 ne place un septième alignement sur la diagonale "
            "secondaire avec une raison positive."
        )

    key, symmetry_id, canonical, (x, r, u, v) = min(candidates, key=lambda item: item[0])
    A = x
    B = x + 2 * r + u
    C = x + 4 * r + u + v
    main_diagonal, secondary_diagonal = _diagonal_sums(canonical)
    roots = tuple(isqrt(value) if value >= 0 and is_square(value) else None for value in canonical)
    return {
        "canonical_grid": _nested(canonical),
        "x": x,
        "r": r,
        "u": u,
        "v": v,
        "A": A,
        "B": B,
        "C": C,
        "magic_sum": target,
        "other_diagonal_sum": main_diagonal,
        "secondary_diagonal_sum": secondary_diagonal,
        "diagonal_defect": main_diagonal - target,
        "is_fully_magic": main_diagonal == target,
        "all_entries_square": all(root is not None for root in roots),
        "square_count": sum(root is not None for root in roots),
        "square_roots": roots,
        "canonical_key": key,
        "symmetry_id": symmetry_id,
    }


def validate_semimagic_grid(
    grid: GridInput,
    require_distinct: bool = True,
    require_positive: bool = True,
) -> dict[str, object]:
    """Valide exactement les sommes et les contraintes élémentaires de la grille."""

    flat = _flatten_grid(grid)
    rows = row_sums(flat)
    columns = column_sums(flat)
    main_diagonal, secondary_diagonal = _diagonal_sums(flat)
    semimagic = len(set(rows + columns)) == 1
    target = rows[0] if semimagic else None
    has_extra_alignment = target is not None and target in (main_diagonal, secondary_diagonal)
    positive = all(value > 0 for value in flat)
    distinct = len(set(flat)) == 9
    roots = tuple(isqrt(value) if value >= 0 and is_square(value) else None for value in flat)
    failures: list[str] = []
    if not semimagic:
        failures.append("not_semimagic")
    if not has_extra_alignment:
        failures.append("no_magic_diagonal")
    if require_positive and not positive:
        failures.append("not_strictly_positive")
    if require_distinct and not distinct:
        failures.append("not_pairwise_distinct")
    canonical: dict[str, object] | None = None
    if not failures or (failures == ["not_strictly_positive"] and not require_positive) or (
        failures == ["not_pairwise_distinct"] and not require_distinct
    ):
        try:
            canonical = canonicalize_semimagic_grid(flat)
        except ValueError:
            failures.append("not_lo_shu_representable_under_d4")
    return {
        "grid": _nested(flat),
        "row_sums": rows,
        "column_sums": columns,
        "main_diagonal_sum": main_diagonal,
        "secondary_diagonal_sum": secondary_diagonal,
        "magic_sum": target,
        "is_semimagic": semimagic,
        "has_extra_alignment": has_extra_alignment,
        "is_fully_magic": target is not None
        and main_diagonal == target
        and secondary_diagonal == target,
        "all_positive": positive,
        "all_distinct": distinct,
        "all_entries_square": all(root is not None for root in roots),
        "square_count": sum(root is not None for root in roots),
        "square_roots": roots,
        "canonical": canonical,
        "accepted": not failures,
        "failures": tuple(failures),
    }
