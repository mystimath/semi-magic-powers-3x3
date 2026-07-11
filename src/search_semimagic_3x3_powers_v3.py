from __future__ import annotations

import argparse
import json
from pathlib import Path

from semimagic_v3_backend import V3Config, extend, validate


def main() -> int:
    parser = argparse.ArgumentParser(description="Moteur incrémental et reprenable V3")
    parser.add_argument("--power", type=int, choices=(2, 3, 4), required=True)
    parser.add_argument("--max-root", type=int, required=True)
    parser.add_argument("--work-dir", type=Path, required=True)
    parser.add_argument("--shards", type=int, default=64)
    parser.add_argument("--resume", action="store_true", help="Documente explicitement une reprise; la reprise est automatique")
    parser.add_argument("--time-limit-minutes", type=float, default=0)
    parser.add_argument("--max-shards-this-run", type=int, default=0)
    parser.add_argument("--checkpoint-every", type=int, default=1)
    parser.add_argument("--validate", action="store_true")
    args = parser.parse_args()
    config = V3Config(args.power, args.shards)
    if args.validate:
        report = validate(args.work_dir, config)
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0 if report["ok"] else 1
    manifest = extend(args.work_dir, config, args.max_root, checkpoint_every=args.checkpoint_every, max_shards_this_run=args.max_shards_this_run, time_limit_minutes=args.time_limit_minutes)
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
