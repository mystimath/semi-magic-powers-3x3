from __future__ import annotations

import sys
import unittest
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))

from semimagic_core import (  # noqa: E402
    canonical_grid,
    column_sums,
    derive_third_row,
    is_semimagic,
    make_power_tables,
    permute_grid,
    row_sums,
    triple_count,
)


class SemimagicCoreTests(unittest.TestCase):
    def test_power_tables(self) -> None:
        root_to_value, value_to_root = make_power_tables(5, 3, positive=True)
        self.assertEqual(root_to_value[4], 64)
        self.assertEqual(value_to_root[125], 5)
        self.assertNotIn(0, root_to_value)

    def test_triple_count_distinct(self) -> None:
        self.assertEqual(triple_count(5, True, True), 10)

    def test_derive_third_row(self) -> None:
        first = (8, 1, 6)
        second = (3, 5, 7)
        self.assertEqual(derive_third_row(15, first, second), (4, 9, 2))

    def test_lo_shu_is_semimagic(self) -> None:
        grid = (8, 1, 6, 3, 5, 7, 4, 9, 2)
        self.assertTrue(is_semimagic(grid))
        self.assertEqual(row_sums(grid), (15, 15, 15))
        self.assertEqual(column_sums(grid), (15, 15, 15))

    def test_non_semimagic_grid(self) -> None:
        self.assertFalse(is_semimagic((1, 2, 3, 4, 5, 6, 7, 8, 9)))

    def test_smallest_observed_distinct_square_semimagic(self) -> None:
        roots = (4, 23, 52, 32, 44, 17, 47, 28, 16)
        values = tuple(root * root for root in roots)
        self.assertEqual(len(set(roots)), 9)
        self.assertTrue(is_semimagic(values))
        self.assertEqual(row_sums(values), (3249, 3249, 3249))
        self.assertEqual(column_sums(values), (3249, 3249, 3249))
        self.assertNotEqual(values[0] + values[4] + values[8], 3249)
        self.assertNotEqual(values[2] + values[4] + values[6], 3249)

    def test_canonicalization_is_invariant(self) -> None:
        grid = (8, 1, 6, 3, 5, 7, 4, 9, 2)
        transformed = permute_grid(grid, (2, 0, 1), (1, 2, 0))
        self.assertEqual(canonical_grid(grid), canonical_grid(transformed))


if __name__ == "__main__":
    unittest.main()
