$ErrorActionPreference = "Stop"

python src/search_semimagic_3x3_powers_v2_disk.py `
  --power 3 `
  --max-root 2250 `
  --shards 256 `
  --work-dir work/cubes_R2250 `
  --phase all `
  --progress-a 10 `
  --progress-shards 1 `
  --out results/cubes/semimagic_3x3_cubes_R2250.csv `
  --summary-json logs/semimagic_3x3_cubes_R2250_summary.json

exit $LASTEXITCODE
