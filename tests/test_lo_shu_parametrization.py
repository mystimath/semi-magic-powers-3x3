from __future__ import annotations

import sys
import unittest
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))

from lo_shu_parametrization import (  # noqa: E402
    build_grid_from_abcr,
    build_grid_from_xruv,
    canonicalize_semimagic_grid,
    d4_orbit_with_ids,
    extract_xruv_from_canonical_grid,
    is_square,
    validate_semimagic_grid,
)
from lo_shu_search import search_seven_line_square_classes  # noqa: E402


EXAMPLES = {
    "bremner": {
        "grid": (
            139129, 360721, 42025,
            83521, 180625, 277729,
            319225, 529, 222121,
        ),
        "xruv": (529, 41496, 55608, 55608),
        "magic_sum": 541875,
        "main_diagonal": 541875,
        "square_count": 7,
    },
    "sallows": {
        "grid": (
            9409, 8836, 3364,
            6724, 12769, 2116,
            5476, 4, 16129,
        ),
        "xruv": (4, 3360, 2685, -14013),
        "magic_sum": 21609,
        "main_diagonal": 38307,
        "square_count": 9,
    },
    "root_446": {
        "grid": (
            3844, 97969, 155236,
            198916, 47524, 10609,
            54289, 111556, 91204,
        ),
        "xruv": (111556, 43680, -195072, -80595),
        "magic_sum": 257049,
        "main_diagonal": 142572,
        "square_count": 9,
    },
    "root_878": {
        "grid": (
            21316, 770884, 380689,
            508369, 148996, 515524,
            643204, 253009, 276676,
        ),
        "xruv": (253009, 127680, -487053, 238848),
        "magic_sum": 1172889,
        "main_diagonal": 446988,
        "square_count": 9,
    },
}


def flat(grid: list[list[int]]) -> tuple[int, ...]:
    return tuple(value for row in grid for value in row)


class ConstructionTests(unittest.TestCase):
    def test_control_examples_extract_and_reconstruct_exactly(self) -> None:
        for name, example in EXAMPLES.items():
            with self.subTest(name=name):
                grid = example["grid"]
                x, r, u, v = extract_xruv_from_canonical_grid(grid)
                self.assertEqual((x, r, u, v), example["xruv"])
                self.assertEqual(flat(build_grid_from_xruv(x, r, u, v)), grid)
                A, B, C = x, x + 2 * r + u, x + 4 * r + u + v
                self.assertEqual(flat(build_grid_from_abcr(A, B, C, r)), grid)

    def test_sum_and_defect_identities(self) -> None:
        for name, example in EXAMPLES.items():
            with self.subTest(name=name):
                x, r, u, v = example["xruv"]
                expected_sum = 3 * x + 9 * r + 2 * u + v
                expected_main = 3 * x + 9 * r + 3 * u
                self.assertEqual(expected_sum, example["magic_sum"])
                self.assertEqual(expected_main, example["main_diagonal"])
                self.assertEqual(expected_main - expected_sum, u - v)

    def test_square_counts_are_exact(self) -> None:
        for name, example in EXAMPLES.items():
            with self.subTest(name=name):
                report = validate_semimagic_grid(example["grid"])
                self.assertTrue(report["accepted"])
                self.assertEqual(report["square_count"], example["square_count"])
                self.assertEqual(report["all_entries_square"], name != "bremner")
        bremner = EXAMPLES["bremner"]["grid"]
        nonsquare_positions = tuple(
            index for index, value in enumerate(bremner) if not is_square(value)
        )
        self.assertEqual(nonsquare_positions, (1, 8))

    def test_magic_condition_is_exact(self) -> None:
        for name, example in EXAMPLES.items():
            with self.subTest(name=name):
                _, _, u, v = example["xruv"]
                report = validate_semimagic_grid(example["grid"])
                self.assertEqual(report["is_fully_magic"], u == v)


class CanonicalizationTests(unittest.TestCase):
    def test_all_d4_images_have_one_stable_key(self) -> None:
        for name, example in EXAMPLES.items():
            with self.subTest(name=name):
                expected = canonicalize_semimagic_grid(example["grid"])["canonical_key"]
                keys = {
                    canonicalize_semimagic_grid(transformed)["canonical_key"]
                    for _, transformed in d4_orbit_with_ids(example["grid"])
                }
                self.assertEqual(keys, {expected})

    def test_canonical_report_preserves_defect_formula(self) -> None:
        for name, example in EXAMPLES.items():
            with self.subTest(name=name):
                report = canonicalize_semimagic_grid(example["grid"])
                self.assertEqual(report["diagonal_defect"], report["u"] - report["v"])
                self.assertEqual(report["secondary_diagonal_sum"], report["magic_sum"])


class SpecializedSearchTests(unittest.TestCase):
    def test_first_published_transversal_class_appears_at_root_127(self) -> None:
        result = search_seven_line_square_classes(127)
        self.assertEqual(result.stats["accepted_classes"], 1)
        self.assertEqual(
            result.classes[0].semimagic_key,
            (2, 74, 127, 94, 97, 58, 113, 82, 46),
        )
        self.assertEqual(result.classes[0].magic_sum, 21609)
        self.assertFalse(result.classes[0].is_fully_magic)


if __name__ == "__main__":
    unittest.main()
