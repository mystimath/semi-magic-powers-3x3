$ErrorActionPreference = "Stop"

$workDir = "work/squares_R1000"
$rawOut = "results/squares/semimagic_3x3_squares_R1000.csv"
$summary = "logs/squares/semimagic_3x3_squares_R1000_summary.json"
$catalog = "results/squares/semimagic_3x3_squares_R1000_catalog.csv"
$primitive = "results/squares/semimagic_3x3_squares_R1000_primitive.csv"
$transversal = "results/squares/semimagic_3x3_squares_R1000_magic_diagonal.csv"

python src/search_semimagic_3x3_powers_v2_disk.py `
    --power 2 --max-root 1000 --shards 256 `
    --work-dir $workDir --phase generate `
    --progress-a 10 --progress-shards 1
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

python src/search_semimagic_shards_parallel.py `
    --power 2 --max-root 1000 --shards 256 `
    --work-dir $workDir --workers 8
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

python src/search_semimagic_3x3_powers_v2_disk.py `
    --power 2 --max-root 1000 --shards 256 `
    --work-dir $workDir --phase aggregate `
    --out $rawOut --summary-json $summary
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

python src/catalog_square_solutions.py $rawOut $catalog
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

python src/analyze_square_transversals.py $catalog `
    --primitive-out $primitive --transversal-out $transversal
exit $LASTEXITCODE
