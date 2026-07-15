from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

from semimagic_disk_backend import (
    RunConfig,
    assert_manifest_compatible,
    atomic_write_json,
    load_json,
    manifest_path,
    search_one_shard,
    shard_result_path,
)


def search_and_write(work_dir: Path, config: RunConfig, shard_id: int) -> tuple[int, int]:
    payload = search_one_shard(work_dir, config, shard_id)
    atomic_write_json(shard_result_path(work_dir, shard_id), payload)
    return shard_id, len(payload["results"])


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Recherche parallèle reprenable, avec un fichier atomique distinct par shard."
    )
    parser.add_argument("--power", type=int, choices=(2, 3, 4), required=True)
    parser.add_argument("--max-root", type=int, required=True)
    parser.add_argument("--shards", type=int, default=256)
    parser.add_argument("--work-dir", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()

    config = RunConfig(args.power, args.max_root, args.shards)
    manifest = load_json(manifest_path(args.work_dir))
    assert_manifest_compatible(manifest, config)
    if not manifest.get("generation_complete"):
        raise RuntimeError("La génération des shards n'est pas terminée.")

    pending = [
        shard_id
        for shard_id in range(config.shard_count)
        if not shard_result_path(args.work_dir, shard_id).exists()
    ]
    print(
        f"{config.shard_count - len(pending)}/{config.shard_count} shards déjà terminés; "
        f"{len(pending)} à traiter avec {args.workers} workers",
        flush=True,
    )
    if not pending:
        return

    completed = config.shard_count - len(pending)
    with ProcessPoolExecutor(max_workers=args.workers) as executor:
        futures = {
            executor.submit(search_and_write, args.work_dir, config, shard_id): shard_id
            for shard_id in pending
        }
        for future in as_completed(futures):
            shard_id, solutions = future.result()
            completed += 1
            print(
                f"[parallèle] shard={shard_id + 1:>4}/{config.shard_count} "
                f"terminé; solutions={solutions:,}; total terminé={completed}/{config.shard_count}",
                flush=True,
            )


if __name__ == "__main__":
    main()
