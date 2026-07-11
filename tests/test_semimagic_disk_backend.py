from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))

from semimagic_core import canonical_grid  # noqa: E402
from semimagic_disk_backend import (  # noqa: E402
    RunConfig,
    atomic_write_json,
    decode_roots,
    encode_roots_scalar,
    generate_shards,
    search_shards,
    search_one_shard,
    shard_id_for_sum,
    shard_path,
    validate_disk_layout,
    _candidate_from_pair,
)


class DiskBackendTests(unittest.TestCase):
    def test_atomic_json_retries_transient_windows_lock(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "state.json"
            from semimagic_disk_backend import os as backend_os

            real_replace = backend_os.replace
            calls = 0

            def transient_replace(source: Path, destination: Path) -> None:
                nonlocal calls
                calls += 1
                if calls < 3:
                    raise PermissionError("verrou Windows transitoire")
                real_replace(source, destination)

            with (
                patch("semimagic_disk_backend.os.replace", side_effect=transient_replace),
                patch("semimagic_disk_backend.time.sleep"),
            ):
                atomic_write_json(path, {"ok": True})

            self.assertEqual(calls, 3)
            self.assertEqual(path.read_text(encoding="utf-8").strip(), '{\n  "ok": true\n}')

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

    def test_sallows_square_is_found(self) -> None:
        import numpy as np

        config = RunConfig(power=2, max_root=127, shard_count=256)
        target_sum = 21609
        triples = ((46, 58, 127), (2, 94, 113), (74, 82, 97))
        expected_roots = canonical_grid(
            (127, 46, 58, 2, 113, 94, 74, 82, 97)
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            work_dir = Path(temp_dir) / "run"
            shard_id = shard_id_for_sum(target_sum, config)
            path = shard_path(work_dir, shard_id)
            path.parent.mkdir(parents=True)
            records = np.empty(len(triples), dtype=config.record_dtype)
            records["sum"] = target_sum
            records["code"] = [
                encode_roots_scalar(*triple, config.root_bits)
                for triple in triples
            ]
            records.tofile(path)

            payload = search_one_shard(work_dir, config, shard_id)

        self.assertEqual(payload["stats"]["solutions"], 1)
        result = payload["results"][0]
        observed_roots = tuple(result[f"root_{name}"] for name in "abcdefghi")
        self.assertEqual(observed_roots, expected_roots)
        self.assertEqual(result["magic_sum"], 21609)
        self.assertFalse(result["is_fully_magic"])


if __name__ == "__main__":
    unittest.main()
