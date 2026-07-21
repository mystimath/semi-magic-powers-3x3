from __future__ import annotations

import sys
import unittest
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))

from lo_shu_search import search_seven_line_square_classes  # noqa: E402


class PublishedCatalogRegressionTests(unittest.TestCase):
    def test_direct_catalog_r5000_regression(self) -> None:
        result = search_seven_line_square_classes(5000)
        self.assertEqual(result.stats["accepted_classes"], 63)
        self.assertEqual(sum(item.is_primitive for item in result.classes), 10)
        self.assertEqual(
            sorted(max(item.semimagic_key) for item in result.classes if item.is_primitive),
            [127, 446, 878, 2434, 2982, 3134, 3191, 3642, 4583, 4893],
        )
    def test_specialized_search_reproduces_the_ten_r1000_transversal_classes(self) -> None:
        result = search_seven_line_square_classes(1000)
        self.assertEqual(result.stats["accepted_classes"], 10)
        self.assertEqual(
            sorted(max(item.semimagic_key) for item in result.classes),
            [127, 254, 381, 446, 508, 635, 762, 878, 889, 892],
        )
        self.assertEqual(sum(item.is_primitive for item in result.classes), 3)
        self.assertFalse(any(item.is_fully_magic for item in result.classes))


if __name__ == "__main__":
    unittest.main()
