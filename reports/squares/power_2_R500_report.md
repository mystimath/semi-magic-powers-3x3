# Rapport power 2 — R = 500

Recherche exhaustive complète et validée le 15 juillet 2026. Les racines sont
les entiers positifs de 1 à 500, les neuf racines sont distinctes et chaque
entrée est leur carré. Les lignes et colonnes ont une somme commune ; les
diagonales ne sont pas imposées.

## Résultats

- Shards : 256/256
- Triples attendus et observés : 20 708 500
- Records sur disque : 248 502 000 octets
- Sommes distinctes : 553 403
- Groupes avec au moins deux triples : 522 126
- Groupes avec au moins trois triples : 498 338
- Taille maximale d'un groupe : 261
- Paires testées : 717 849 658
- Paires disjointes : 682 753 714
- Alignements : 4 096 522 284
- Troisièmes lignes entièrement carrées : 22 744
- Troisièmes triples indexés : 7 322
- Solutions canoniques uniques : 3 661
- Solutions primitives : 3 054
- Temps de recherche : 3 776,288869 s
- Temps total de l'invocation : 3 786,13 s

La validation indépendante confirme le nombre exact de records, les 256 shards
et l'absence d'erreur de format. Les 22 tests unitaires passent après le run.

## Analyse des diagonales sur les orbites

Pour chaque classe, les six transversales (une case de chaque ligne et de chaque
colonne) ont été testées. Une transversale peut être transformée en diagonale
par permutation des lignes et des colonnes.

Quatre classes seulement possèdent une transversale de somme magique :

| Racine max. | Somme | PGCD | Racines canoniques | Racines de la transversale magique |
|---:|---:|---:|---|---|
| 127 | 21 609 | 1 | 2,74,127 / 94,97,58 / 113,82,46 | 74,58,113 |
| 254 | 86 436 | 2 | 4,148,254 / 188,194,116 / 226,164,92 | 148,116,226 |
| 381 | 194 481 | 3 | 6,222,381 / 282,291,174 / 339,246,138 | 222,174,339 |
| 446 | 257 049 | 1 | 62,233,446 / 313,334,218 / 394,302,103 | 233,218,394 |

Les trois premières sont la classe de Sallows et ses changements d'échelle par
2 et 3. La classe de racine maximale 446 est primitive et distincte. Chacune
possède exactement une transversale magique parmi les six ; aucune classe ne
possède donc un représentant pleinement magique.

## Artefacts

- `work/squares_R500`
- `results/squares/semimagic_3x3_squares_R500.csv`
- `results/squares/semimagic_3x3_squares_R500_catalog.csv`
- `results/squares/semimagic_3x3_squares_R500_primitive.csv`
- `results/squares/semimagic_3x3_squares_R500_magic_diagonal.csv`
- `logs/squares/semimagic_3x3_squares_R500_summary.json`
- `scripts/run_squares_R500.ps1`

## Reproduction et validation

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/run_squares_R500.ps1
python src/search_semimagic_3x3_powers_v2_disk.py --power 2 --max-root 500 `
  --shards 256 --work-dir work/squares_R500 --phase validate
```
