from __future__ import annotations

from collections import defaultdict
from itertools import combinations, combinations_with_replacement, permutations
from math import comb
from typing import Callable, Iterator, Sequence

RootTriple = tuple[int, int, int]
Grid = tuple[int, int, int, int, int, int, int, int, int]


def make_power_tables(
    max_root: int,
    power: int,
    positive: bool = True,
) -> tuple[dict[int, int], dict[int, int]]:
    """Retourne racine -> puissance et puissance -> racine."""
    if max_root < 1:
        raise ValueError("max_root doit être supérieur ou égal à 1.")
    if power < 2:
        raise ValueError("power doit être supérieur ou égal à 2.")

    start = 1 if positive else 0
    root_to_value = {root: root**power for root in range(start, max_root + 1)}
    value_to_root = {value: root for root, value in root_to_value.items()}
    return root_to_value, value_to_root


def triple_count(max_root: int, distinct_roots: bool, positive: bool = True) -> int:
    """Nombre théorique de triples non ordonnés."""
    root_count = max_root if positive else max_root + 1
    if distinct_roots:
        return comb(root_count, 3) if root_count >= 3 else 0
    return comb(root_count + 2, 3)


def iter_root_triples(
    max_root: int,
    distinct_roots: bool = True,
    positive: bool = True,
) -> Iterator[RootTriple]:
    """Génère les triples de racines dans un ordre canonique."""
    start = 1 if positive else 0
    roots = range(start, max_root + 1)
    if distinct_roots:
        yield from combinations(roots, 3)
    else:
        yield from combinations_with_replacement(roots, 3)


def build_triple_groups(
    max_root: int,
    power: int,
    distinct_roots: bool = True,
    positive: bool = True,
    progress_every: int = 0,
    progress_callback: Callable[[int, int], None] | None = None,
) -> tuple[dict[int, list[RootTriple]], dict[int, int], dict[int, int]]:
    """Regroupe les triples de racines par somme de leurs puissances."""
    root_to_value, value_to_root = make_power_tables(max_root, power, positive)
    groups: dict[int, list[RootTriple]] = defaultdict(list)
    total = triple_count(max_root, distinct_roots, positive)

    for index, triple in enumerate(
        iter_root_triples(max_root, distinct_roots, positive),
        start=1,
    ):
        a, b, c = triple
        total_value = root_to_value[a] + root_to_value[b] + root_to_value[c]
        groups[total_value].append(triple)

        if (
            progress_every > 0
            and progress_callback is not None
            and index % progress_every == 0
        ):
            progress_callback(index, total)

    if progress_callback is not None and total:
        progress_callback(total, total)

    return dict(groups), root_to_value, value_to_root


def unique_permutations(values: Sequence[int]) -> tuple[tuple[int, int, int], ...]:
    """Retourne les permutations distinctes d'un triple."""
    if len(values) != 3:
        raise ValueError("Trois valeurs sont attendues.")
    return tuple(sorted(set(permutations(values, 3))))


def derive_third_row(
    target_sum: int,
    first_row: Sequence[int],
    second_row: Sequence[int],
) -> tuple[int, int, int]:
    """Déduit la troisième ligne imposée par les sommes de colonnes."""
    if len(first_row) != 3 or len(second_row) != 3:
        raise ValueError("Chaque ligne doit contenir exactement trois valeurs.")
    return tuple(
        target_sum - first_row[index] - second_row[index]
        for index in range(3)
    )


def row_sums(grid: Sequence[int]) -> tuple[int, int, int]:
    _validate_grid_length(grid)
    return (sum(grid[0:3]), sum(grid[3:6]), sum(grid[6:9]))


def column_sums(grid: Sequence[int]) -> tuple[int, int, int]:
    _validate_grid_length(grid)
    return (
        grid[0] + grid[3] + grid[6],
        grid[1] + grid[4] + grid[7],
        grid[2] + grid[5] + grid[8],
    )


def is_semimagic(grid: Sequence[int]) -> bool:
    """Vérifie l'égalité des trois lignes et des trois colonnes."""
    rows = row_sums(grid)
    cols = column_sums(grid)
    return len(set(rows + cols)) == 1


def transpose_grid(grid: Sequence[int]) -> Grid:
    _validate_grid_length(grid)
    return (
        grid[0], grid[3], grid[6],
        grid[1], grid[4], grid[7],
        grid[2], grid[5], grid[8],
    )


def permute_grid(
    grid: Sequence[int],
    row_order: Sequence[int],
    column_order: Sequence[int],
) -> Grid:
    """Applique une permutation de lignes et une permutation de colonnes."""
    _validate_grid_length(grid)
    if sorted(row_order) != [0, 1, 2] or sorted(column_order) != [0, 1, 2]:
        raise ValueError("Les ordres doivent être des permutations de (0, 1, 2).")

    matrix = [grid[0:3], grid[3:6], grid[6:9]]
    return tuple(
        matrix[row_index][column_index]
        for row_index in row_order
        for column_index in column_order
    )  # type: ignore[return-value]


def canonical_grid(grid: Sequence[int]) -> Grid:
    """Représentant canonique sous lignes, colonnes et transposition."""
    _validate_grid_length(grid)
    candidates: list[Grid] = []
    orders = tuple(permutations((0, 1, 2)))

    for base in (tuple(grid), transpose_grid(grid)):
        for row_order in orders:
            for column_order in orders:
                candidates.append(permute_grid(base, row_order, column_order))

    return min(candidates)


def format_grid(grid: Sequence[int], width: int | None = None) -> str:
    """Formate une grille 3×3 lisible."""
    _validate_grid_length(grid)
    actual_width = width or max(len(str(value)) for value in grid)
    return "\n".join(
        "  ".join(f"{value:>{actual_width}}" for value in grid[start:start + 3])
        for start in (0, 3, 6)
    )


def _validate_grid_length(grid: Sequence[int]) -> None:
    if len(grid) != 9:
        raise ValueError("Une grille 3×3 doit contenir exactement neuf valeurs.")
