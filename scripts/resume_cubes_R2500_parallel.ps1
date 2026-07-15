$ErrorActionPreference = "Stop"

python src/search_semimagic_shards_parallel.py `
  --power 3 `
  --max-root 2500 `
  --shards 256 `
  --work-dir work/cubes_R2500 `
  --workers 8
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

python src/search_semimagic_3x3_powers_v2_disk.py `
  --power 3 `
  --max-root 2500 `
  --shards 256 `
  --work-dir work/cubes_R2500 `
  --phase aggregate `
  --out results/cubes/semimagic_3x3_cubes_R2500.csv `
  --summary-json logs/semimagic_3x3_cubes_R2500_summary.json

exit $LASTEXITCODE
