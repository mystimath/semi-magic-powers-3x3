from __future__ import annotations

import math
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np

SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))

from semimagic_v3_backend import (  # noqa: E402
    RECORD_DTYPE,
    V3Config,
    _find_solutions,
    extend,
    validate,
)


class V3BackendTests(unittest.TestCase):
    def test_record_encoding_round_trip_and_itemsize(self) -> None:
        records = np.asarray([(36, 1, 2, 3)], dtype=RECORD_DTYPE)
        restored = np.frombuffer(records.tobytes(), dtype=RECORD_DTYPE)
        self.assertEqual(RECORD_DTYPE.itemsize, 20)
        self.assertEqual(tuple(int(restored[0][name]) for name in ("sum", "a", "b", "c")), (36, 1, 2, 3))

    def test_full_generation_for_all_powers(self) -> None:
        for power in (2, 3, 4):
            with self.subTest(power=power), tempfile.TemporaryDirectory() as temp:
                config = V3Config(power, 5)
                manifest = extend(Path(temp) / "run", config, 9)
                self.assertEqual(manifest["records"], math.comb(9, 3))
                self.assertTrue(validate(Path(temp) / "run", config)["ok"])

    def test_direct_equals_two_and_three_step_extension(self) -> None:
        for power in (2, 3, 4):
            with self.subTest(power=power), tempfile.TemporaryDirectory() as temp:
                config = V3Config(power, 7)
                direct = extend(Path(temp) / "direct", config, 16)
                two = extend(Path(temp) / "two", config, 9)
                two = extend(Path(temp) / "two", config, 16)
                three = extend(Path(temp) / "three", config, 7)
                three = extend(Path(temp) / "three", config, 11)
                three = extend(Path(temp) / "three", config, 16)
                self.assertEqual(direct["records"], two["records"])
                self.assertEqual(direct["known_solutions"], two["known_solutions"])
                self.assertEqual(direct["known_solutions"], three["known_solutions"])
                for shard in range(config.shard_count):
                    name = f"shards/shard_{shard:04d}.bin"
                    self.assertEqual((Path(temp) / "direct" / name).read_bytes(), (Path(temp) / "two" / name).read_bytes())

    def test_interruption_and_resume_does_not_duplicate(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            work = Path(temp) / "run"
            config = V3Config(3, 5)
            interrupted = extend(work, config, 13, stop_after_c=7)
            self.assertIsNotNone(interrupted["pending_extension"])
            resumed = extend(work, config, 13)
            self.assertIsNone(resumed["pending_extension"])
            self.assertEqual(validate(work, config)["records"], math.comb(13, 3))

    def test_bounded_shard_merge_and_resume(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            work = Path(temp) / "run"
            config = V3Config(4, 6)
            partial = extend(work, config, 10, max_shards_this_run=2)
            self.assertIsNotNone(partial["pending_extension"])
            complete = extend(work, config, 10)
            self.assertIsNone(complete["pending_extension"])
            self.assertTrue(validate(work, config)["ok"])

    def test_incomplete_shard_is_detected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            work = Path(temp) / "run"
            config = V3Config(2, 4)
            extend(work, config, 8)
            shard = next((work / "shards").glob("*.bin"))
            with shard.open("ab") as handle:
                handle.write(b"x")
            report = validate(work, config)
            self.assertFalse(report["ok"])
            self.assertIn("incomplet", " ".join(report["errors"]))

    def test_canonical_deduplication(self) -> None:
        triples = [(15, 1, 6, 8), (15, 2, 4, 9), (15, 3, 5, 7)]
        results = _find_solutions(np.asarray(triples, dtype=RECORD_DTYPE), 1)
        self.assertEqual(len(results), 1)


if __name__ == "__main__":
    unittest.main()
