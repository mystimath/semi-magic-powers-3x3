# Rapport power 2 — R = 1000

Recherche exhaustive complète et validée le 16 juillet 2026. Les racines sont les entiers positifs de 1 à 1000, les neuf racines sont distinctes et chaque entrée est leur carré. Les lignes et colonnes ont une somme commune ; les diagonales ne sont pas imposées.

## Résultats

- Shards : 256/256
- Triples attendus et observés : 166 167 000
- Records sur disque : 1 994 004 000 octets
- Sommes distinctes : 2 285 787
- Groupes avec au moins deux triples : 2 193 675
- Groupes avec au moins trois triples : 2 120 161
- Taille maximale d'un groupe : 520
- Paires testées : 11 615 079 060
- Paires disjointes : 11 284 537 468
- Alignements : 67 707 224 808
- Troisièmes lignes entièrement carrées : 141 800
- Troisièmes triples indexés : 46 430
- Solutions canoniques uniques : 23 215
- Solutions primitives : 18 248
- Temps de recherche cumulé des shards : 70 086,5976858 s
- Temps mural entre création du work-dir et résumé final : 8 793,16 s

La validation indépendante du work-dir confirme le nombre exact de records, leur taille, les 256 shards et l'absence d'erreur de format. Les 22 tests du moteur passent après le run.

## Analyse des transversales sur les orbites

Dix classes possèdent exactement une transversale de somme magique :

| Racine max. | Somme | PGCD | Racines canoniques | Interprétation |
|---:|---:|---:|---|---|
| 127 | 21 609 = 147² | 1 | 2,74,127 / 94,97,58 / 113,82,46 | classe de Sallows |
| 254 | 86 436 = 294² | 2 | 4,148,254 / 188,194,116 / 226,164,92 | Sallows ×2 |
| 381 | 194 481 = 441² | 3 | 6,222,381 / 282,291,174 / 339,246,138 | Sallows ×3 |
| 446 | 257 049 = 507² | 1 | 62,233,446 / 313,334,218 / 394,302,103 | classe primitive distincte |
| 508 | 345 744 = 588² | 4 | 8,296,508 / 376,388,232 / 452,328,184 | Sallows ×4 |
| 635 | 540 225 = 735² | 5 | 10,370,635 / 470,485,290 / 565,410,230 | Sallows ×5 |
| 762 | 777 924 = 882² | 6 | 12,444,762 / 564,582,348 / 678,492,276 | Sallows ×6 |
| 878 | 1 172 889 = 1083² | 1 | 146,617,878 / 713,718,386 / 802,526,503 | nouvelle classe primitive du catalogue |
| 889 | 1 058 841 = 1029² | 7 | 14,518,889 / 658,679,406 / 791,574,322 | Sallows ×7 |
| 892 | 1 028 196 = 1014² | 2 | 124,466,892 / 626,668,436 / 788,604,206 | classe 446 ×2 |

La borne R750 contenait les six premières classes du tableau. Le palier R1000 ajoute Sallows ×6 et ×7, la classe 446 ×2 et une classe primitive de racine maximale 878. Aucune classe ne possède plus d'une transversale magique ; aucune n'est donc pleinement magique. « Nouvelle » signifie ici nouvelle dans le catalogue exhaustif du projet, sans présumer de l'absence d'une antériorité.

## Exécution

Les triplets ont été générés au format V2 sur disque, puis les 256 shards ont été recherchés par huit workers indépendants utilisant `search_one_shard` et des écritures JSON atomiques. L'agrégation, le catalogage canonique et l'analyse des six transversales ont été exécutés automatiquement après la recherche.

## Artefacts

- `work/squares_R1000`
- `results/squares/semimagic_3x3_squares_R1000.csv`
- `results/squares/semimagic_3x3_squares_R1000_catalog.csv`
- `results/squares/semimagic_3x3_squares_R1000_primitive.csv`
- `results/squares/semimagic_3x3_squares_R1000_magic_diagonal.csv`
- `logs/squares/semimagic_3x3_squares_R1000_summary.json`
- `scripts/run_squares_R1000_parallel.ps1`

## Validation

```powershell
python src/search_semimagic_3x3_powers_v2_disk.py --power 2 --max-root 1000 `
  --shards 256 --work-dir work/squares_R1000 --phase validate
python -m pytest -q
```