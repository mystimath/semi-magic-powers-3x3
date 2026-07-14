# Rapport power 2 — R = 400

Recherche exhaustive complète et validée le 14 juillet 2026. Les racines sont
les entiers positifs de 1 à 400, les neuf racines sont distinctes et chaque
entrée est leur carré. Les lignes et colonnes ont une somme commune ; les
diagonales ne sont pas imposées.

## Résultats

- Shards : 256/256
- Triples attendus et observés : 10 586 800
- Records sur disque : 127 041 600 octets
- Sommes distinctes : 349 893
- Groupes avec au moins deux triples : 327 927
- Groupes avec au moins trois triples : 311 267
- Taille maximale d'un groupe : 202
- Paires testées : 292 279 929
- Paires disjointes : 275 339 536
- Alignements : 1 652 037 216
- Troisièmes lignes entièrement carrées : 12 199
- Troisièmes triples indexés : 3 900
- Solutions canoniques uniques : 1 950
- Temps de recherche : 1 465,3741122 s
- Temps total : 1 472,29 s

La validation indépendante confirme le nombre exact de records, les 256 shards
et l'absence d'erreur de format.

## Reproduction et validation

```powershell
python src/search_semimagic_3x3_powers_v2_disk.py --power 2 --max-root 400 `
  --shards 256 --work-dir work/squares_R400 --phase all `
  --out results/squares/semimagic_3x3_squares_R400.csv `
  --summary-json logs/squares/semimagic_3x3_squares_R400_summary.json
python src/search_semimagic_3x3_powers_v2_disk.py --power 2 --max-root 400 `
  --shards 256 --work-dir work/squares_R400 --phase validate
```
