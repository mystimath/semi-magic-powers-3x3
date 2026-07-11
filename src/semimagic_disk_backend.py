from __future__ import annotations

import csv
import json
import math
import os
import shutil
import time
from dataclasses import asdict, dataclass
from itertools import combinations, permutations
from pathlib import Path
from typing import Any, Iterable

import numpy as np

from semimagic_core import canonical_grid, column_sums, is_semimagic, row_sums

FORMAT_VERSION = 2


@dataclass(frozen=True)
class RunConfig:
    power: int
    max_root: int
    shard_count: int
    positive: bool = True
    distinct_roots: bool = True

    def validate(self) -> None:
        if self.power not in (2, 3, 4):
            raise ValueError("La puissance doit valoir 2, 3 ou 4.")
        if self.max_root < 3:
            raise ValueError("max_root doit être supérieur ou égal à 3.")
        if self.shard_count < 1:
            raise ValueError("shard_count doit être supérieur ou égal à 1.")
        if not self.positive:
            raise ValueError("La V2 sur disque traite uniquement les racines positives.")
        if not self.distinct_roots:
            raise ValueError("La V2 sur disque traite uniquement les racines distinctes.")

    @property
    def root_bits(self) -> int:
        return self.max_root.bit_length()

    @property
    def code_dtype(self) -> str:
        return "<u4" if 3 * self.root_bits <= 32 else "<u8"

    @property
    def record_dtype(self) -> np.dtype[Any]:
        return np.dtype([("sum", "<u8"), ("code", self.code_dtype)])

    @property
    def total_triples(self) -> int:
        return math.comb(self.max_root, 3)

    @property
    def min_sum(self) -> int:
        return 1**self.power + 2**self.power + 3**self.power

    @property
    def max_sum(self) -> int:
        r = self.max_root
        return r**self.power + (r - 1) ** self.power + (r - 2) ** self.power

    @property
    def shard_width(self) -> int:
        span = self.max_sum - self.min_sum + 1
        return (span + self.shard_count - 1) // self.shard_count


@dataclass
class SearchStats:
    shard_id: int
    records: int = 0
    sums_total: int = 0
    collision_sums_ge_2: int = 0
    candidate_sums_ge_3: int = 0
    max_group_size: int = 0
    triple_pairs: int = 0
    disjoint_pairs: int = 0
    alignments_tested: int = 0
    third_row_power_hits: int = 0
    third_triple_hits: int = 0
    solutions: int = 0
    elapsed_seconds: float = 0.0


def atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    for attempt in range(5):
        try:
            os.replace(temp, path)
            return
        except PermissionError:
            if attempt == 4:
                raise
            time.sleep(0.05 * (attempt + 1))


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def powers_table(config: RunConfig) -> list[int]:
    return [root**config.power for root in range(config.max_root + 1)]


def value_to_root_table(config: RunConfig) -> dict[int, int]:
    return {root**config.power: root for root in range(1, config.max_root + 1)}


def encode_roots_scalar(a: int, b: int, c: int, bits: int) -> int:
    return a | (b << bits) | (c << (2 * bits))


def encode_roots_vector(
    a: int,
    b: int,
    c: np.ndarray[Any, Any],
    bits: int,
    dtype: str,
) -> np.ndarray[Any, Any]:
    target_dtype = np.dtype(dtype)
    factor_b = np.asarray(1 << bits, dtype=target_dtype)
    factor_c = np.asarray(1 << (2 * bits), dtype=target_dtype)
    return (
        np.asarray(a, dtype=target_dtype)
        | (np.asarray(b, dtype=target_dtype) * factor_b)
        | (c.astype(target_dtype, copy=False) * factor_c)
    )


def decode_roots(code: int, bits: int) -> tuple[int, int, int]:
    mask = (1 << bits) - 1
    return code & mask, (code >> bits) & mask, (code >> (2 * bits)) & mask


def shard_id_for_sum(target_sum: int, config: RunConfig) -> int:
    shard_id = (target_sum - config.min_sum) // config.shard_width
    return min(max(shard_id, 0), config.shard_count - 1)


def shard_path(work_dir: Path, shard_id: int) -> Path:
    return work_dir / "shards" / f"shard_{shard_id:04d}.bin"


def shard_result_path(work_dir: Path, shard_id: int) -> Path:
    return work_dir / "search" / f"shard_{shard_id:04d}.json"


def manifest_path(work_dir: Path) -> Path:
    return work_dir / "manifest.json"


def _config_payload(config: RunConfig) -> dict[str, Any]:
    payload = asdict(config)
    payload.update(
        {
            "format_version": FORMAT_VERSION,
            "root_bits": config.root_bits,
            "code_dtype": config.code_dtype,
            "record_itemsize": config.record_dtype.itemsize,
            "total_triples": config.total_triples,
            "min_sum": config.min_sum,
            "max_sum": config.max_sum,
            "shard_width": config.shard_width,
        }
    )
    return payload


def initialize_work_dir(
    work_dir: Path,
    config: RunConfig,
    overwrite: bool = False,
) -> dict[str, Any]:
    config.validate()
    manifest_file = manifest_path(work_dir)

    if work_dir.exists() and overwrite:
        shutil.rmtree(work_dir)

    if manifest_file.exists():
        manifest = load_json(manifest_file)
        assert_manifest_compatible(manifest, config)
        return manifest

    if work_dir.exists() and any(work_dir.iterdir()):
        raise FileExistsError(
            f"{work_dir} existe déjà sans manifeste compatible. "
            "Utilisez --overwrite pour le recréer."
        )

    (work_dir / "shards").mkdir(parents=True, exist_ok=True)
    (work_dir / "search").mkdir(parents=True, exist_ok=True)

    manifest: dict[str, Any] = {
        **_config_payload(config),
        "generation_complete": False,
        "next_a": 1,
        "generated_records": 0,
        "shard_sizes": [0] * config.shard_count,
        "created_unix": time.time(),
        "updated_unix": time.time(),
    }
    atomic_write_json(manifest_file, manifest)
    return manifest


def assert_manifest_compatible(manifest: dict[str, Any], config: RunConfig) -> None:
    expected = _config_payload(config)
    keys = (
        "format_version",
        "power",
        "max_root",
        "shard_count",
        "positive",
        "distinct_roots",
        "root_bits",
        "code_dtype",
        "record_itemsize",
        "total_triples",
        "min_sum",
        "max_sum",
        "shard_width",
    )
    mismatches = [key for key in keys if manifest.get(key) != expected.get(key)]
    if mismatches:
        details = ", ".join(
            f"{key}: manifeste={manifest.get(key)!r}, attendu={expected.get(key)!r}"
            for key in mismatches
        )
        raise ValueError(f"Manifeste incompatible : {details}")


def rollback_to_manifest(work_dir: Path, manifest: dict[str, Any], config: RunConfig) -> None:
    sizes = manifest["shard_sizes"]
    if len(sizes) != config.shard_count:
        raise ValueError("Le manifeste contient un nombre de tailles de shards invalide.")

    for shard_id, expected_size in enumerate(sizes):
        path = shard_path(work_dir, shard_id)
        if not path.exists():
            if expected_size != 0:
                raise FileNotFoundError(f"Shard manquant : {path}")
            continue
        actual_size = path.stat().st_size
        if actual_size < expected_size:
            raise IOError(
                f"Shard tronqué : {path} ({actual_size} octets au lieu de {expected_size})."
            )
        if actual_size > expected_size:
            with path.open("r+b") as handle:
                handle.truncate(expected_size)


def generate_shards(
    work_dir: Path,
    config: RunConfig,
    overwrite: bool = False,
    progress_every_a: int = 10,
) -> dict[str, Any]:
    manifest = initialize_work_dir(work_dir, config, overwrite=overwrite)
    manifest_file = manifest_path(work_dir)

    if manifest.get("generation_complete"):
        return manifest

    rollback_to_manifest(work_dir, manifest, config)

    dtype = config.record_dtype
    itemsize = dtype.itemsize
    bits = config.root_bits
    shard_width = config.shard_width
    min_sum = config.min_sum
    power_values = np.asarray(powers_table(config), dtype=np.uint64)

    next_a = int(manifest["next_a"])
    generated_records = int(manifest["generated_records"])
    shard_sizes = [int(value) for value in manifest["shard_sizes"]]

    handles: list[Any] = []
    try:
        for shard_id in range(config.shard_count):
            path = shard_path(work_dir, shard_id)
            path.parent.mkdir(parents=True, exist_ok=True)
            handles.append(path.open("ab", buffering=0))

        started = time.perf_counter()
        for a in range(next_a, config.max_root - 1):
            buffers: dict[int, bytearray] = {}
            records_this_a = 0

            for b in range(a + 1, config.max_root):
                c_roots = np.arange(b + 1, config.max_root + 1, dtype=np.uint64)
                if c_roots.size == 0:
                    continue

                sums = power_values[a] + power_values[b] + power_values[c_roots]
                shard_ids = ((sums - min_sum) // shard_width).astype(np.int64)
                np.clip(shard_ids, 0, config.shard_count - 1, out=shard_ids)
                codes = encode_roots_vector(a, b, c_roots, bits, config.code_dtype)

                records = np.empty(c_roots.size, dtype=dtype)
                records["sum"] = sums
                records["code"] = codes

                split_points = np.flatnonzero(shard_ids[1:] != shard_ids[:-1]) + 1
                starts = np.concatenate((np.asarray([0]), split_points))
                ends = np.concatenate((split_points, np.asarray([c_roots.size])))
                raw = records.tobytes(order="C")

                for start, end in zip(starts.tolist(), ends.tolist()):
                    shard_id = int(shard_ids[start])
                    buffer = buffers.setdefault(shard_id, bytearray())
                    buffer.extend(raw[start * itemsize : end * itemsize])

                records_this_a += int(c_roots.size)

            for shard_id, buffer in buffers.items():
                handles[shard_id].write(buffer)
                shard_sizes[shard_id] += len(buffer)

            generated_records += records_this_a
            manifest.update(
                {
                    "next_a": a + 1,
                    "generated_records": generated_records,
                    "shard_sizes": shard_sizes,
                    "updated_unix": time.time(),
                }
            )
            atomic_write_json(manifest_file, manifest)

            if progress_every_a > 0 and (
                a == next_a or a % progress_every_a == 0 or a == config.max_root - 2
            ):
                elapsed = time.perf_counter() - started
                percent = 100.0 * generated_records / config.total_triples
                disk_mb = sum(shard_sizes) / (1024 * 1024)
                print(
                    f"[génération] a={a:>4}/{config.max_root - 2}  "
                    f"triples={generated_records:,}/{config.total_triples:,} "
                    f"({percent:6.2f} %)  disque={disk_mb:,.1f} Mo  "
                    f"temps={elapsed:,.1f}s",
                    flush=True,
                )

        if generated_records != config.total_triples:
            raise RuntimeError(
                f"Comptage final incohérent : {generated_records:,} au lieu de "
                f"{config.total_triples:,}."
            )

        manifest.update(
            {
                "generation_complete": True,
                "next_a": config.max_root - 1,
                "generated_records": generated_records,
                "shard_sizes": shard_sizes,
                "generation_finished_unix": time.time(),
                "updated_unix": time.time(),
            }
        )
        atomic_write_json(manifest_file, manifest)
        return manifest
    finally:
        for handle in handles:
            handle.close()


def _group_boundaries(sorted_sums: np.ndarray[Any, Any]) -> tuple[np.ndarray[Any, Any], np.ndarray[Any, Any]]:
    if sorted_sums.size == 0:
        empty = np.asarray([], dtype=np.int64)
        return empty, empty
    changes = np.flatnonzero(sorted_sums[1:] != sorted_sums[:-1]) + 1
    starts = np.concatenate((np.asarray([0], dtype=np.int64), changes))
    ends = np.concatenate((changes, np.asarray([sorted_sums.size], dtype=np.int64)))
    return starts, ends


def _candidate_from_pair(
    target_sum: int,
    first: tuple[int, int, int],
    second_permuted: tuple[int, int, int],
    power_values: list[int],
    value_to_root: dict[int, int],
) -> tuple[int, int, int] | None:
    derived_values = (
        target_sum - power_values[first[0]] - power_values[second_permuted[0]],
        target_sum - power_values[first[1]] - power_values[second_permuted[1]],
        target_sum - power_values[first[2]] - power_values[second_permuted[2]],
    )
    roots = (
        value_to_root.get(derived_values[0]),
        value_to_root.get(derived_values[1]),
        value_to_root.get(derived_values[2]),
    )
    if any(root is None for root in roots):
        return None
    return roots[0], roots[1], roots[2]  # type: ignore[return-value]


def search_one_shard(
    work_dir: Path,
    config: RunConfig,
    shard_id: int,
    max_results: int = 0,
) -> dict[str, Any]:
    started = time.perf_counter()
    path = shard_path(work_dir, shard_id)
    dtype = config.record_dtype
    stats = SearchStats(shard_id=shard_id)
    results: list[dict[str, Any]] = []

    if not path.exists() or path.stat().st_size == 0:
        stats.elapsed_seconds = time.perf_counter() - started
        return {"stats": asdict(stats), "results": results}

    if path.stat().st_size % dtype.itemsize != 0:
        raise IOError(f"Taille invalide pour {path}.")

    records = np.fromfile(path, dtype=dtype)
    stats.records = int(records.size)
    records.sort(order=["sum", "code"], kind="quicksort")

    sums = records["sum"]
    starts, ends = _group_boundaries(sums)
    stats.sums_total = int(starts.size)

    power_values = powers_table(config)
    value_to_root = value_to_root_table(config)
    seen_canonical: set[tuple[int, ...]] = set()

    stop = False
    for start, end in zip(starts.tolist(), ends.tolist()):
        group_size = end - start
        stats.max_group_size = max(stats.max_group_size, group_size)
        if group_size >= 2:
            stats.collision_sums_ge_2 += 1
        if group_size < 3:
            continue
        stats.candidate_sums_ge_3 += 1

        target_sum = int(sums[start])
        codes = records["code"][start:end]
        triples = [decode_roots(int(code), config.root_bits) for code in codes]
        triple_to_index = {triple: index for index, triple in enumerate(triples)}

        for i, j in combinations(range(group_size), 2):
            stats.triple_pairs += 1
            first = triples[i]
            second = triples[j]
            if set(first) & set(second):
                continue
            stats.disjoint_pairs += 1

            for second_permuted in permutations(second):
                stats.alignments_tested += 1
                third_or_none = _candidate_from_pair(
                    target_sum,
                    first,
                    second_permuted,
                    power_values,
                    value_to_root,
                )
                if third_or_none is None:
                    continue
                stats.third_row_power_hits += 1

                third = third_or_none
                if len(set(first + second + third)) != 9:
                    continue

                third_sorted = tuple(sorted(third))
                third_index = triple_to_index.get(third_sorted)
                if third_index is None or third_index <= j:
                    continue
                stats.third_triple_hits += 1

                root_grid = (*first, *second_permuted, *third)
                value_grid = tuple(power_values[root] for root in root_grid)
                if not is_semimagic(value_grid):
                    raise RuntimeError("Erreur interne : grille non semi-magique.")

                canonical_roots = canonical_grid(root_grid)
                if canonical_roots in seen_canonical:
                    continue
                seen_canonical.add(canonical_roots)
                canonical_values = tuple(power_values[root] for root in canonical_roots)
                diagonals = (
                    canonical_values[0] + canonical_values[4] + canonical_values[8],
                    canonical_values[2] + canonical_values[4] + canonical_values[6],
                )

                result: dict[str, Any] = {
                    "power": config.power,
                    "max_root": config.max_root,
                    "magic_sum": target_sum,
                    "is_fully_magic": diagonals[0] == target_sum and diagonals[1] == target_sum,
                    "diagonal_1": diagonals[0],
                    "diagonal_2": diagonals[1],
                }
                for name, root in zip("abcdefghi", canonical_roots):
                    result[f"root_{name}"] = int(root)
                for name, value in zip("abcdefghi", canonical_values):
                    result[f"value_{name}"] = int(value)
                results.append(result)
                stats.solutions += 1

                if max_results > 0 and stats.solutions >= max_results:
                    stop = True
                    break
            if stop:
                break
        if stop:
            break

    stats.elapsed_seconds = time.perf_counter() - started
    return {"stats": asdict(stats), "results": results}


def search_shards(
    work_dir: Path,
    config: RunConfig,
    max_results: int = 0,
    progress_every_shards: int = 1,
) -> dict[str, Any]:
    manifest_file = manifest_path(work_dir)
    if not manifest_file.exists():
        raise FileNotFoundError(f"Manifeste absent : {manifest_file}")
    manifest = load_json(manifest_file)
    assert_manifest_compatible(manifest, config)
    if not manifest.get("generation_complete"):
        raise RuntimeError("La génération des shards n'est pas terminée.")

    started = time.perf_counter()
    completed = 0
    total_solutions = 0

    for shard_id in range(config.shard_count):
        output_path = shard_result_path(work_dir, shard_id)
        if output_path.exists():
            payload = load_json(output_path)
            total_solutions += len(payload.get("results", []))
            completed += 1
            continue

        payload = search_one_shard(
            work_dir=work_dir,
            config=config,
            shard_id=shard_id,
            max_results=max_results,
        )
        atomic_write_json(output_path, payload)
        total_solutions += len(payload["results"])
        completed += 1

        if progress_every_shards > 0 and (
            completed == 1
            or completed % progress_every_shards == 0
            or completed == config.shard_count
        ):
            stats = payload["stats"]
            elapsed = time.perf_counter() - started
            print(
                f"[recherche] shard={shard_id + 1:>4}/{config.shard_count}  "
                f"records={stats['records']:,}  groupes>=3={stats['candidate_sums_ge_3']:,}  "
                f"alignements={stats['alignments_tested']:,}  "
                f"solutions cumulées={total_solutions:,}  temps={elapsed:,.1f}s",
                flush=True,
            )

        if max_results > 0 and total_solutions >= max_results:
            break

    return aggregate_search(work_dir, config)


def aggregate_search(work_dir: Path, config: RunConfig) -> dict[str, Any]:
    aggregate_stats: dict[str, int | float] = {
        "records": 0,
        "sums_total": 0,
        "collision_sums_ge_2": 0,
        "candidate_sums_ge_3": 0,
        "max_group_size": 0,
        "triple_pairs": 0,
        "disjoint_pairs": 0,
        "alignments_tested": 0,
        "third_row_power_hits": 0,
        "third_triple_hits": 0,
        "solutions": 0,
        "elapsed_seconds": 0.0,
    }
    results: list[dict[str, Any]] = []
    completed_shards = 0

    additive_keys = (
        "records",
        "sums_total",
        "collision_sums_ge_2",
        "candidate_sums_ge_3",
        "triple_pairs",
        "disjoint_pairs",
        "alignments_tested",
        "third_row_power_hits",
        "third_triple_hits",
        "solutions",
        "elapsed_seconds",
    )

    for shard_id in range(config.shard_count):
        path = shard_result_path(work_dir, shard_id)
        if not path.exists():
            continue
        payload = load_json(path)
        completed_shards += 1
        stats = payload["stats"]
        for key in additive_keys:
            aggregate_stats[key] = aggregate_stats[key] + stats[key]  # type: ignore[operator]
        aggregate_stats["max_group_size"] = max(
            int(aggregate_stats["max_group_size"]), int(stats["max_group_size"])
        )
        results.extend(payload.get("results", []))

    summary = {
        **_config_payload(config),
        "completed_shards": completed_shards,
        "search_complete": completed_shards == config.shard_count,
        "stats": aggregate_stats,
        "results_count": len(results),
        "results": results,
    }
    return summary


def write_results_csv(path: Path, results: Iterable[dict[str, Any]]) -> int:
    rows = list(results)
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "power",
        "max_root",
        "magic_sum",
        "is_fully_magic",
        "diagonal_1",
        "diagonal_2",
        *[f"root_{name}" for name in "abcdefghi"],
        *[f"value_{name}" for name in "abcdefghi"],
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return len(rows)


def validate_disk_layout(work_dir: Path, config: RunConfig) -> dict[str, Any]:
    manifest = load_json(manifest_path(work_dir))
    assert_manifest_compatible(manifest, config)
    dtype = config.record_dtype
    actual_sizes: list[int] = []
    records = 0
    errors: list[str] = []

    for shard_id in range(config.shard_count):
        path = shard_path(work_dir, shard_id)
        size = path.stat().st_size if path.exists() else 0
        actual_sizes.append(size)
        if size % dtype.itemsize != 0:
            errors.append(f"shard {shard_id}: taille {size} non multiple de {dtype.itemsize}")
        records += size // dtype.itemsize

    expected_sizes = [int(value) for value in manifest["shard_sizes"]]
    if actual_sizes != expected_sizes:
        errors.append("Les tailles réelles des shards diffèrent du manifeste.")
    if manifest.get("generation_complete") and records != config.total_triples:
        errors.append(
            f"Nombre de records {records:,} différent de l'attendu {config.total_triples:,}."
        )

    return {
        "ok": not errors,
        "errors": errors,
        "records": records,
        "expected_records": config.total_triples,
        "disk_bytes": sum(actual_sizes),
        "record_itemsize": dtype.itemsize,
    }
