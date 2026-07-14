from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from catalog_square_solutions import enrich  # noqa: E402


class CatalogSquareSolutionsTests(unittest.TestCase):
    def test_enriches_and_validates_known_minimal_solution(self) -> None:
        roots = [4, 23, 52, 32, 44, 17, 47, 28, 16]
        row = {"power": "2", "max_root": "52", "magic_sum": "3249"}
        for cell, root in zip("abcdefghi", roots):
            row[f"root_{cell}"] = str(root)
            row[f"value_{cell}"] = str(root * root)
        result = enrich(row)
        self.assertEqual(result["actual_max_root"], 52)
        self.assertEqual(result["root_gcd"], 1)
        self.assertTrue(result["is_primitive"])
        self.assertFalse(result["is_fully_magic"])


if __name__ == "__main__":
    unittest.main()
