from __future__ import annotations

import json
import math
import os
import time
from dataclasses import asdict, dataclass
from itertools import combinations, permutations
from pathlib import Path
from typing import Any

import numpy as np

from semimagic_core import canonical_grid, is_semimagic

FORMAT_VERSION = 3
RECORD_DTYPE = np.dtype([("sum", "<u8"), ("a", "<u4"), ("b", "<u4"), ("c", "<u4")])


@dataclass(frozen=True)
class V3Config:
    power: int
    shard_count: int = 64

    def validate(self) -> None:
        if self.power not in (2, 3, 4):
            raise ValueError("power doit valoir 2, 3 ou 4")
        if self.shard_count < 1:
            raise ValueError("shard_count doit être positif")


def _atomic_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(temp, path)


def _manifest_path(work_dir: Path) -> Path:
    return work_dir / "manifest.json"


def _shard_path(work_dir: Path, shard_id: int) -> Path:
    return work_dir / "shards" / f"shard_{shard_id:04d}.bin"


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def initialize(work_dir: Path, config: V3Config) -> dict[str, Any]:
    config.validate()
    path = _manifest_path(work_dir)
    if path.exists():
        manifest = _load(path)
        if manifest.get("format_version") != FORMAT_VERSION or manifest.get("power") != config.power or manifest.get("shard_count") != config.shard_count:
            raise ValueError("Manifeste V3 incompatible")
        return manifest
    if work_dir.exists() and any(work_dir.iterdir()):
        raise FileExistsError(f"Répertoire non vide sans manifeste V3: {work_dir}")
    (work_dir / "shards").mkdir(parents=True, exist_ok=True)
    manifest = {
        "format_version": FORMAT_VERSION,
        "power": config.power,
        "shard_count": config.shard_count,
        "record_itemsize": RECORD_DTYPE.itemsize,
        "max_root": 2,
        "records": 0,
        "history": [],
        "pending_extension": None,
        "known_solutions": [],
        "created_unix": time.time(),
    }
    _atomic_json(path, manifest)
    return manifest


def _write_extension_records(work_dir: Path, config: V3Config, old: int, new: int, checkpoint_every: int, stop_after_c: int | None) -> tuple[dict[str, Any], bool]:
    path = _manifest_path(work_dir)
    manifest = _load(path)
    pending = manifest.get("pending_extension")
    stage = work_dir / "staging"
    if pending is None:
        stage.mkdir(parents=True, exist_ok=True)
        pending = {"old_root": old, "new_root": new, "next_c": old + 1, "stage_sizes": [0] * config.shard_count, "phase": "generate"}
        manifest["pending_extension"] = pending
        _atomic_json(path, manifest)
    elif (pending["old_root"], pending["new_root"]) != (old, new):
        raise ValueError("Une autre extension est déjà en attente")

    sizes = list(map(int, pending["stage_sizes"]))
    for shard_id, expected in enumerate(sizes):
        target = stage / f"shard_{shard_id:04d}.bin"
        actual = target.stat().st_size if target.exists() else 0
        if actual < expected:
            raise IOError(f"Shard de staging incomplet: {target}")
        if actual > expected:
            with target.open("r+b") as handle:
                handle.truncate(expected)

    for c in range(int(pending["next_c"]), new + 1):
        buckets: dict[int, list[tuple[int, int, int, int]]] = {}
        for a, b in combinations(range(1, c), 2):
            total = a**config.power + b**config.power + c**config.power
            buckets.setdefault(total % config.shard_count, []).append((total, a, b, c))
        for shard_id, rows in buckets.items():
            records = np.asarray(rows, dtype=RECORD_DTYPE)
            target = stage / f"shard_{shard_id:04d}.bin"
            with target.open("ab") as handle:
                handle.write(records.tobytes())
            sizes[shard_id] += records.nbytes
        if (c - old) % max(1, checkpoint_every) == 0 or c == new:
            pending.update({"next_c": c + 1, "stage_sizes": sizes})
            manifest["pending_extension"] = pending
            _atomic_json(path, manifest)
        if stop_after_c is not None and c >= stop_after_c:
            return manifest, False
    pending["phase"] = "merge"
    pending["base_sizes"] = [
        _shard_path(work_dir, shard_id).stat().st_size
        if _shard_path(work_dir, shard_id).exists()
        else 0
        for shard_id in range(config.shard_count)
    ]
    manifest["pending_extension"] = pending
    _atomic_json(path, manifest)
    return manifest, True


def _find_solutions(records: np.ndarray[Any, Any], power: int, only_sums: set[int] | None = None) -> list[dict[str, Any]]:
    if records.size == 0:
        return []
    records.sort(order=["sum", "a", "b", "c"], kind="stable")
    powers = {root: root**power for root in set(records["a"]) | set(records["b"]) | set(records["c"])}
    inverse = {value: root for root, value in powers.items()}
    results: dict[tuple[int, ...], dict[str, Any]] = {}
    sums = records["sum"]
    boundaries = np.flatnonzero(sums[1:] != sums[:-1]) + 1
    for group in np.split(records, boundaries):
        target = int(group[0]["sum"])
        if only_sums is not None and target not in only_sums:
            continue
        triples = [(int(r["a"]), int(r["b"]), int(r["c"])) for r in group]
        if len(triples) < 3:
            continue
        triple_set = set(triples)
        for first, second in combinations(triples, 2):
            if set(first) & set(second):
                continue
            for aligned in permutations(second):
                values = tuple(target - powers[first[i]] - powers[aligned[i]] for i in range(3))
                third = tuple(inverse.get(value, 0) for value in values)
                if 0 in third or len(set(first + aligned + third)) != 9 or tuple(sorted(third)) not in triple_set:
                    continue
                roots = first + aligned + third
                values_grid = tuple(root**power for root in roots)
                if not is_semimagic(values_grid):
                    raise RuntimeError("Candidat V3 non semi-magique")
                canonical = tuple(int(root) for root in canonical_grid(roots))
                results[canonical] = {"magic_sum": target, "roots": list(canonical)}
    return [results[key] for key in sorted(results)]


def extend(work_dir: Path, config: V3Config, new_root: int, *, checkpoint_every: int = 1, max_shards_this_run: int = 0, time_limit_minutes: float = 0, stop_after_c: int | None = None) -> dict[str, Any]:
    manifest = initialize(work_dir, config)
    old = int(manifest["max_root"])
    pending = manifest.get("pending_extension")
    if pending is not None:
        old, expected_new = int(pending["old_root"]), int(pending["new_root"])
        if new_root != expected_new:
            raise ValueError(f"Reprise attendue vers R={expected_new}")
    if new_root <= old:
        raise ValueError("La nouvelle borne doit être supérieure à la borne courante")
    started = time.monotonic()
    manifest, generated = _write_extension_records(work_dir, config, old, new_root, checkpoint_every, stop_after_c)
    if not generated:
        return manifest
    pending = manifest["pending_extension"]
    completed = set(pending.get("merged_shards", []))
    affected_sums: set[int] = set(map(int, pending.get("affected_sums", [])))
    processed = 0
    for shard_id in range(config.shard_count):
        if shard_id in completed:
            continue
        if max_shards_this_run and processed >= max_shards_this_run:
            return _load(_manifest_path(work_dir))
        if time_limit_minutes and time.monotonic() - started >= time_limit_minutes * 60:
            return _load(_manifest_path(work_dir))
        base_path = _shard_path(work_dir, shard_id)
        stage_path = work_dir / "staging" / f"shard_{shard_id:04d}.bin"
        base_size = int(pending["base_sizes"][shard_id])
        stage_size = stage_path.stat().st_size if stage_path.exists() else 0
        actual_size = base_path.stat().st_size if base_path.exists() else 0
        if actual_size == base_size + stage_size and actual_size != base_size:
            completed.add(shard_id)
            pending["merged_shards"] = sorted(completed)
            manifest["pending_extension"] = pending
            _atomic_json(_manifest_path(work_dir), manifest)
            continue
        if actual_size != base_size:
            raise IOError(f"État de fusion incohérent pour le shard {shard_id}")
        old_records = np.fromfile(base_path, dtype=RECORD_DTYPE) if base_path.exists() else np.empty(0, dtype=RECORD_DTYPE)
        new_records = np.fromfile(stage_path, dtype=RECORD_DTYPE) if stage_path.exists() else np.empty(0, dtype=RECORD_DTYPE)
        affected_sums.update(map(int, new_records["sum"]))
        merged = np.concatenate((old_records, new_records))
        merged.sort(order=["sum", "a", "b", "c"], kind="stable")
        temp = base_path.with_suffix(".bin.tmp")
        base_path.parent.mkdir(parents=True, exist_ok=True)
        merged.tofile(temp)
        os.replace(temp, base_path)
        completed.add(shard_id)
        processed += 1
        pending.update({"merged_shards": sorted(completed), "affected_sums": sorted(affected_sums)})
        manifest["pending_extension"] = pending
        _atomic_json(_manifest_path(work_dir), manifest)

    known = {tuple(row["roots"]): row for row in manifest.get("known_solutions", [])}
    for shard_id in range(config.shard_count):
        path = _shard_path(work_dir, shard_id)
        records = np.fromfile(path, dtype=RECORD_DTYPE) if path.exists() else np.empty(0, dtype=RECORD_DTYPE)
        shard_sums = {value for value in affected_sums if value % config.shard_count == shard_id}
        for row in _find_solutions(records, config.power, shard_sums):
            known[tuple(row["roots"])] = row
    added = math.comb(new_root, 3) - math.comb(old, 3)
    manifest.update({
        "max_root": new_root,
        "records": math.comb(new_root, 3),
        "known_solutions": [known[key] for key in sorted(known)],
        "pending_extension": None,
        "history": manifest["history"] + [{"old_root": old, "new_root": new_root, "records_added": added, "affected_sums": len(affected_sums), "completed_unix": time.time()}],
    })
    _atomic_json(_manifest_path(work_dir), manifest)
    return manifest


def validate(work_dir: Path, config: V3Config) -> dict[str, Any]:
    manifest = initialize(work_dir, config)
    errors: list[str] = []
    count = 0
    for shard_id in range(config.shard_count):
        path = _shard_path(work_dir, shard_id)
        size = path.stat().st_size if path.exists() else 0
        if size % RECORD_DTYPE.itemsize:
            errors.append(f"shard {shard_id} incomplet")
        count += size // RECORD_DTYPE.itemsize
    if manifest.get("pending_extension") is None and count != math.comb(int(manifest["max_root"]), 3):
        errors.append(f"records={count}, attendu={math.comb(int(manifest['max_root']), 3)}")
    return {"ok": not errors, "errors": errors, "records": count, "manifest_records": manifest["records"]}
