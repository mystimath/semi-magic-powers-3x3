$ErrorActionPreference = "Stop"

python src/search_semimagic_3x3_powers_v2_disk.py `
  --power 3 `
  --max-root 500 `
  --shards 256 `
  --work-dir work/cubes_R500 `
  --phase all `
  --progress-a 10 `
  --progress-shards 1 `
  --out results/cubes/semimagic_3x3_cubes_R500.csv `
  --summary-json logs/semimagic_3x3_cubes_R500_summary.json

exit $LASTEXITCODE
