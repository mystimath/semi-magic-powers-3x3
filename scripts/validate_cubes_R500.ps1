$ErrorActionPreference = "Stop"

python src/search_semimagic_3x3_powers_v2_disk.py `
  --power 3 `
  --max-root 500 `
  --shards 256 `
  --work-dir work/cubes_R500 `
  --phase validate

exit $LASTEXITCODE
