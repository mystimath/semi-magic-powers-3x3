$ErrorActionPreference = "Stop"

python src/search_semimagic_shards_parallel.py `
  --power 2 `
  --max-root 750 `
  --shards 256 `
  --work-dir work/squares_R750 `
  --workers 8
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

python src/search_semimagic_3x3_powers_v2_disk.py `
  --power 2 `
  --max-root 750 `
  --shards 256 `
  --work-dir work/squares_R750 `
  --phase aggregate `
  --out results/squares/semimagic_3x3_squares_R750.csv `
  --summary-json logs/squares/semimagic_3x3_squares_R750_summary.json
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

python src/catalog_square_solutions.py `
  results/squares/semimagic_3x3_squares_R750.csv `
  results/squares/semimagic_3x3_squares_R750_catalog.csv
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

python src/analyze_square_transversals.py `
  results/squares/semimagic_3x3_squares_R750_catalog.csv `
  --primitive-out results/squares/semimagic_3x3_squares_R750_primitive.csv `
  --transversal-out results/squares/semimagic_3x3_squares_R750_magic_diagonal.csv

exit $LASTEXITCODE
