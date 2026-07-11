$ErrorActionPreference = "Stop"

python src/search_semimagic_3x3_powers_v2_disk.py `
  --power 2 `
  --max-root 52 `
  --shards 64 `
  --work-dir work/squares_R52 `
  --phase all `
  --progress-a 10 `
  --progress-shards 1 `
  --out results/squares/semimagic_3x3_squares_R52.csv `
  --summary-json logs/semimagic_3x3_squares_R52_summary.json

exit $LASTEXITCODE
