# Exécutions scientifiques

## Carrés — R = 52

- Date : 11 juillet 2026
- Puissance : 2
- Racines : 1 à 52, positives et globalement distinctes
- Shards : 64
- Triples : 22 100
- Shards terminés : 64/64
- Recherche complète : oui
- Validation du format disque : OK
- Taille des records sur disque : 265 200 octets
- Sommes distinctes : 4 871
- Sommes avec au moins 2 triples : 3 864
- Sommes avec au moins 3 triples : 3 120
- Taille maximale d'un groupe : 20
- Paires de triples : 67 987
- Paires disjointes : 52 059
- Alignements testés : 312 354
- Troisièmes lignes puissances : 12
- Troisièmes triples indexés : 2
- Solutions uniques : 1
- Temps de recherche cumulé des shards : 0,729366800016578 s

La solution unique, différente de Sallows, est :

```text
racines              carrés
 4  23  52             16   529  2704
32  44  17           1024  1936   289
47  28  16           2209   784   256
```

Les six sommes de lignes et colonnes valent `3 249 = 57²`. Les diagonales
valent `2 208` et `6 849`; la solution n'est pas pleinement magique. Le
classement exhaustif des 48 solutions du run R127 ne contient aucune solution
de racine maximale inférieure à 52 : cette borne est donc minimale dans le
cadre positif à neuf racines distinctes.

Artefacts :

- `work/squares_R52` (à conserver pour la reprise)
- `results/squares/semimagic_3x3_squares_R52.csv`
- `logs/semimagic_3x3_squares_R52_summary.json`
- `scripts/run_squares_R52.ps1`

## Carrés — R = 127

- Date : 11 juillet 2026
- Puissance : 2
- Racines : 1 à 127, positives et globalement distinctes
- Shards : 256
- Triples : 333 375
- Shards terminés : 256/256
- Recherche complète : oui
- Validation du format disque : OK
- Taille des records sur disque : 4 000 500 octets
- Sommes distinctes : 32 305
- Sommes avec au moins 2 triples : 28 717
- Sommes avec au moins 3 triples : 26 013
- Taille maximale d'un groupe : 58
- Paires de triples : 2 794 445
- Paires disjointes : 2 424 316
- Alignements testés : 14 545 896
- Troisièmes lignes puissances : 339
- Troisièmes triples indexés : 96
- Solutions uniques : 48
- Solutions pleinement magiques : 0
- Temps de recherche cumulé des shards : 14,8846363999837 s

Analyse des diagonales sur toute l'orbite de chaque classe (et non seulement
sur la représentation canonique du CSV) : une seule classe possède au moins une
diagonale de somme `S`, celle de Sallows (index CSV 46). Aucune classe n'a ses
deux diagonales à `S`.

Le carré de Sallows est retrouvé exactement une fois, à l'index CSV 46 en base
zéro, sous la forme canonique suivante :

```text
racines                 carrés
  2   74  127              4   5476  16129
 94   97   58           8836   9409   3364
113   82   46          12769   6724   2116
```

Les six sommes de lignes et de colonnes valent `21 609 = 147²`. Les diagonales
valent `11 529` et `38 307`; la solution est donc semi-magique mais non
pleinement magique.

Artefacts :

- `work/squares_R127` (à conserver pour la reprise)
- `results/squares/semimagic_3x3_squares_R127.csv`
- `logs/semimagic_3x3_squares_R127_summary.json`
- `scripts/run_squares_R127.ps1`

## Cubes — R = 500

- Puissance : 3
- Racines : 1 à 500, positives et globalement distinctes
- Shards : 256
- Triples : 20 708 500
- Shards terminés : 256/256
- Recherche complète : oui
- Sommes distinctes : 17 979 739
- Sommes avec au moins 2 triples : 2 268 345
- Sommes avec au moins 3 triples : 371 670
- Taille maximale d'un groupe : 13
- Paires de triples : 1 405 054
- Paires disjointes : 1 296 954
- Alignements testés : 7 781 724
- Troisièmes lignes puissances : 0
- Solutions uniques : 0
- Temps de recherche cumulé des shards : 32,590556269 s

Artefacts :

- `results/cubes/semimagic_3x3_cubes_R500.csv`
- `logs/semimagic_3x3_cubes_R500_summary.json`
- `scripts/run_cubes_R500.ps1`
- `scripts/validate_cubes_R500.ps1`

## Cubes — R = 750

- Date : 11 juillet 2026
- Puissance : 3
- Racines : 1 à 750, positives et globalement distinctes
- Shards : 256
- Triples : 70 031 500
- Shards terminés : 256/256
- Recherche complète : oui
- Validation du format disque : OK
- Taille des records sur disque : 840 378 000 octets
- Sommes distinctes : 60 663 560
- Sommes avec au moins 2 triples : 7 738 250
- Sommes avec au moins 3 triples : 1 298 431
- Taille maximale d'un groupe : 13
- Paires de triples : 4 987 954
- Paires disjointes : 4 675 701
- Alignements testés : 28 054 206
- Troisièmes lignes puissances : 0
- Solutions uniques : 0
- Temps de recherche cumulé des shards : 92,23130170001241 s

Artefacts : `work/cubes_R750`, le CSV et le résumé JSON R750, et
`scripts/run_cubes_R750.ps1`.

## Cubes — R = 1000

- Date : 11 juillet 2026
- Puissance : 3
- Racines : 1 à 1000, positives et globalement distinctes
- Shards : 256
- Triples : 166 167 000
- Shards terminés : 256/256
- Recherche complète : oui
- Validation du format disque : OK
- Taille des records sur disque : 1 994 004 000 octets
- Sommes distinctes : 143 758 544
- Sommes avec au moins 2 triples : 18 454 166
- Sommes avec au moins 3 triples : 3 130 468
- Taille maximale d'un groupe : 15
- Paires de triples : 12 123 833
- Paires disjointes : 11 469 063
- Alignements testés : 68 814 378
- Troisièmes lignes puissances : 0
- Solutions uniques : 0
- Temps de recherche cumulé des shards : 232,79438730000402 s

Le premier lancement a rencontré un verrou Windows transitoire lors du
remplacement atomique du manifeste à 92,6 % de la génération. La même commande,
sans `--overwrite`, a repris à `next_a = 589`. Le backend réessaie désormais
brièvement les remplacements atomiques refusés par Windows.

Artefacts : `work/cubes_R1000`, le CSV et le résumé JSON R1000, et
`scripts/run_cubes_R1000.ps1`.

## Cubes — R = 1500

- Date : 11 juillet 2026
- Puissance : 3
- Racines : 1 à 1500, positives et globalement distinctes
- Shards : 256
- Triples : 561 375 500
- Shards terminés : 256/256
- Recherche complète : oui
- Validation du format disque : OK
- Taille des records sur disque : 8 982 008 000 octets
- Taille d'un record : 16 octets (`<u8` pour le code des triples)
- Sommes distinctes : 485 098 793
- Sommes avec au moins 2 triples : 62 597 192
- Sommes avec au moins 3 triples : 10 749 912
- Taille maximale d'un groupe : 20
- Paires de triples : 42 023 395
- Paires disjointes : 40 199 220
- Alignements testés : 241 195 320
- Troisièmes lignes puissances : 0
- Solutions uniques : 0
- Temps de recherche cumulé des shards : 691,313986499983 s

Le premier démarrage a révélé un défaut NumPy dans le décalage des codes lorsque
`R=1500` exige un encodage 64 bits. Le backend a été corrigé en conservant le
même encodage binaire, puis les tests de round-trip et les 14 tests unitaires
ont passé. Le run complet a ensuite été repris et validé sans perte de records.

Artefacts : `work/cubes_R1500`, le CSV et le résumé JSON R1500, et
`scripts/run_cubes_R1500.ps1`.

## Cubes — R = 2000

- Date : 11 juillet 2026
- Puissance : 3
- Racines : 1 à 2000, positives et globalement distinctes
- Shards : 256
- Triples : 1 331 334 000
- Shards terminés : 256/256
- Recherche complète : oui
- Validation du format disque : OK
- Taille des records sur disque : 21 301 344 000 octets
- Taille d'un record : 16 octets (`<u8` pour le code des triples)
- Sommes distinctes : 1 149 694 966
- Sommes avec au moins 2 triples : 148 809 304
- Sommes avec au moins 3 triples : 25 695 521
- Taille maximale d'un groupe : 20
- Paires de triples : 100 977 719
- Paires disjointes : 97 236 063
- Alignements testés : 583 416 378
- Troisièmes lignes puissances : 0
- Solutions uniques : 0
- Temps de recherche cumulé des shards : 1 630,96063080004 s

Artefacts : `work/cubes_R2000`, le CSV et le résumé JSON R2000, et
`scripts/run_cubes_R2000.ps1`.

## Puissances quatrièmes — R = 250

- Date : 11 juillet 2026
- Puissance : 4
- Racines : 1 à 250, positives et globalement distinctes
- Shards : 256
- Triples : 2 573 000
- Shards terminés : 256/256
- Recherche complète : oui
- Validation du format disque : OK
- Taille des records sur disque : 30 876 000 octets
- Sommes distinctes : 2 555 828
- Sommes avec au moins 2 triples : 16 165
- Sommes avec au moins 3 triples : 674
- Taille maximale d'un groupe : 7
- Paires de triples : 3 073
- Paires disjointes : 3 069
- Alignements testés : 18 414
- Troisièmes lignes puissances : 0
- Troisièmes triples indexés : 0
- Solutions uniques : 0
- Temps de recherche cumulé des shards : 3,4501069999641913 s

Commande : `scripts/run_fourth_R250.ps1`. Le premier lancement a achevé la
génération puis rencontré une erreur d'encodage de console CP1252 sur le symbole
`≥`. Après remplacement de ce libellé par `>=`, la même commande, sans
`--overwrite`, a repris au deuxième shard et terminé l'agrégation.

Artefacts :

- `work/fourth_R250` (à conserver pour la reprise)
- `results/fourth-powers/semimagic_3x3_fourth_R250.csv`
- `logs/semimagic_3x3_fourth_R250_summary.json`
- `scripts/run_fourth_R250.ps1`

## Puissances quatrièmes — R = 500

- Date : 11 juillet 2026
- Puissance : 4
- Racines : 1 à 500, positives et globalement distinctes
- Shards : 256
- Triples : 20 708 500
- Shards terminés : 256/256
- Recherche complète : oui
- Validation du format disque : OK
- Taille des records sur disque : 248 502 000 octets
- Sommes distinctes : 20 621 339
- Sommes avec au moins 2 triples : 81 514
- Sommes avec au moins 3 triples : 3 401
- Taille maximale d'un groupe : 10
- Paires de triples : 17 607
- Paires disjointes : 17 567
- Alignements testés : 105 402
- Troisièmes lignes puissances : 0
- Troisièmes triples indexés : 0
- Solutions uniques : 0
- Temps de recherche cumulé des shards : 18,310254199994233 s

Commande : `scripts/run_fourth_R500.ps1`. Le premier lancement a été interrompu
pendant la génération par un refus Windows transitoire lors du remplacement
atomique du manifeste. Le manifeste validé indiquait `next_a = 198` et
16 117 949 records. La même commande, relancée sans `--overwrite`, a repris la
génération, terminé les 256 shards et produit l'agrégation complète.

Artefacts :

- `work/fourth_R500` (à conserver pour la reprise)
- `results/fourth-powers/semimagic_3x3_fourth_R500.csv`
- `logs/semimagic_3x3_fourth_R500_summary.json`
- `scripts/run_fourth_R500.ps1`
