# Rapport power 2 — R = 750

Recherche exhaustive complète et validée le 15 juillet 2026. Les racines sont
les entiers positifs de 1 à 750, les neuf racines sont distinctes et chaque
entrée est leur carré. Les lignes et colonnes ont une somme commune ; les
diagonales ne sont pas imposées.

## Résultats

- Shards : 256/256
- Triples attendus et observés : 70 031 500
- Records sur disque : 840 378 000 octets
- Sommes distinctes : 1 269 997
- Groupes avec au moins deux triples : 1 211 390
- Groupes avec au moins trois triples : 1 165 348
- Taille maximale d'un groupe : 390
- Paires testées : 3 660 483 077
- Paires disjointes : 3 529 749 523
- Alignements : 21 178 497 138
- Troisièmes lignes entièrement carrées : 67 371
- Troisièmes triples indexés : 21 946
- Solutions canoniques uniques : 10 973
- Solutions primitives : 8 816
- Temps de recherche cumulé des shards : 21 514,0638975 s
- Temps mural entre création du work-dir et résumé final : 6 214,80 s

La validation indépendante confirme le nombre exact de records, les 256 shards
et l'absence d'erreur de format. Les 22 tests unitaires passent après le run.
Une seconde vérification parcourt les 10 973 lignes du catalogue, contrôle les
racines, les carrés, les six sommes semi-magiques, l'unicité des représentants,
les PGCD et les six transversales.

## Analyse des transversales sur les orbites

Six classes seulement possèdent une transversale de somme magique :

| Racine max. | Somme | PGCD | Racines canoniques | Interprétation |
|---:|---:|---:|---|---|
| 127 | 21 609 = 147² | 1 | 2,74,127 / 94,97,58 / 113,82,46 | Sallows |
| 254 | 86 436 = 294² | 2 | 4,148,254 / 188,194,116 / 226,164,92 | Sallows ×2 |
| 381 | 194 481 = 441² | 3 | 6,222,381 / 282,291,174 / 339,246,138 | Sallows ×3 |
| 446 | 257 049 = 507² | 1 | 62,233,446 / 313,334,218 / 394,302,103 | classe primitive distincte |
| 508 | 345 744 = 588² | 4 | 8,296,508 / 376,388,232 / 452,328,184 | Sallows ×4 |
| 635 | 540 225 = 735² | 5 | 10,370,635 / 470,485,290 / 565,410,230 | Sallows ×5 |

Chaque classe possède exactement une transversale magique parmi les six.
Aucune classe ne possède donc un représentant pleinement magique. Les deux
classes ajoutées depuis R500 sont seulement les changements d'échelle ×4 et ×5
de Sallows. La classe de racine maximale 446 reste la seule autre classe
primitive observée avec sept sommes égales.

## Exécution séquentielle puis parallèle

La génération et les 53 premiers shards de recherche ont utilisé le chemin
séquentiel validé. La reprise a ensuite utilisé huit workers, chaque worker
appelant sans modification `search_one_shard` et écrivant un fichier JSON
distinct par remplacement atomique. Les shards déjà terminés ont été conservés.

Avant la reprise, l'équivalence a été testée sur deux copies indépendantes du
work-dir R52 : 22 100 records, 64 shards, statistiques agrégées, solution et CSV
étaient identiques entre exécution séquentielle et parallèle, hors temps mesuré.

## Artefacts

- `work/squares_R750`
- `results/squares/semimagic_3x3_squares_R750.csv`
- `results/squares/semimagic_3x3_squares_R750_catalog.csv`
- `results/squares/semimagic_3x3_squares_R750_primitive.csv`
- `results/squares/semimagic_3x3_squares_R750_magic_diagonal.csv`
- `logs/squares/semimagic_3x3_squares_R750_summary.json`
- `scripts/run_squares_R750.ps1`
- `scripts/resume_squares_R750_parallel.ps1`

## Validation

```powershell
python src/search_semimagic_3x3_powers_v2_disk.py --power 2 --max-root 750 `
  --shards 256 --work-dir work/squares_R750 --phase validate
python -m unittest discover -s tests -v
```
