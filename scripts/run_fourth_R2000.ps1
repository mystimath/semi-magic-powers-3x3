$ErrorActionPreference = "Stop"

python src/search_semimagic_3x3_powers_v2_disk.py `
  --power 4 `
  --max-root 2000 `
  --shards 256 `
  --work-dir work/fourth_R2000 `
  --phase all `
  --progress-a 10 `
  --progress-shards 1 `
  --out results/fourth-powers/semimagic_3x3_fourth_R2000.csv `
  --summary-json logs/semimagic_3x3_fourth_R2000_summary.json

exit $LASTEXITCODE
