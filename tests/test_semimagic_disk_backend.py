from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))

from semimagic_disk_backend import (  # noqa: E402
    RunConfig,
    decode_roots,
    encode_roots_scalar,
    generate_shards,
    search_shards,
    shard_id_for_sum,
    shard_path,
    validate_disk_layout,
    _candidate_from_pair,
)


class DiskBackendTests(unittest.TestCase):
    def test_encode_decode(self) -> None:
        config = RunConfig(power=3, max_root=500, shard_count=256)
        code = encode_roots_scalar(12, 245, 500, config.root_bits)
        self.assertEqual(decode_roots(code, config.root_bits), (12, 245, 500))

    def test_shard_bounds(self) -> None:
        config = RunConfig(power=3, max_root=30, shard_count=8)
        self.assertEqual(shard_id_for_sum(config.min_sum, config), 0)
        self.assertEqual(shard_id_for_sum(config.max_sum, config), 7)


    def test_pair_logic_with_lo_shu_identity_values(self) -> None:
        triples = [(1, 6, 8), (2, 4, 9), (3, 5, 7)]
        power_values = list(range(10))
        value_to_root = {value: value for value in range(1, 10)}

        found = False
        first = triples[0]
        second = triples[1]
        for second_permuted in __import__("itertools").permutations(second):
            third = _candidate_from_pair(
                15, first, second_permuted, power_values, value_to_root
            )
            if third is not None and tuple(sorted(third)) == triples[2]:
                found = True
                break
        self.assertTrue(found)


    def test_generated_records_are_exact(self) -> None:
        import itertools
        import numpy as np

        config = RunConfig(power=3, max_root=8, shard_count=4)
        with tempfile.TemporaryDirectory() as temp_dir:
            work_dir = Path(temp_dir) / "run"
            generate_shards(work_dir, config, progress_every_a=0)

            observed = set()
            for shard_id in range(config.shard_count):
                path = shard_path(work_dir, shard_id)
                if not path.exists():
                    continue
                records = np.fromfile(path, dtype=config.record_dtype)
                for record in records:
                    triple = decode_roots(int(record["code"]), config.root_bits)
                    observed.add((int(record["sum"]), triple))

            expected = {
                (a**3 + b**3 + c**3, (a, b, c))
                for a, b, c in itertools.combinations(range(1, 9), 3)
            }
            self.assertEqual(observed, expected)

    def test_small_generation_and_search(self) -> None:
        config = RunConfig(power=3, max_root=12, shard_count=8)
        with tempfile.TemporaryDirectory() as temp_dir:
            work_dir = Path(temp_dir) / "run"
            generate_shards(work_dir, config, progress_every_a=0)
            validation = validate_disk_layout(work_dir, config)
            self.assertTrue(validation["ok"], validation["errors"])
            self.assertEqual(validation["records"], config.total_triples)

            summary = search_shards(work_dir, config, progress_every_shards=0)
            self.assertTrue(summary["search_complete"])
            self.assertEqual(summary["stats"]["records"], config.total_triples)
            self.assertEqual(summary["results_count"], 0)


if __name__ == "__main__":
    unittest.main()
