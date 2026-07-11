$ErrorActionPreference = "Stop"

python src/search_semimagic_3x3_powers_v2_disk.py `
  --power 2 `
  --max-root 127 `
  --shards 256 `
  --work-dir work/squares_R127 `
  --phase all `
  --progress-a 10 `
  --progress-shards 1 `
  --out results/squares/semimagic_3x3_squares_R127.csv `
  --summary-json logs/semimagic_3x3_squares_R127_summary.json

exit $LASTEXITCODE
