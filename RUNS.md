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

## Puissances quatrièmes — R = 750

- Date : 11 juillet 2026
- Puissance : 4
- Racines : 1 à 750, positives et globalement distinctes
- Shards : 256
- Triples : 70 031 500
- Shards terminés : 256/256
- Recherche complète : oui
- Validation du format disque : OK
- Taille des records sur disque : 840 378 000 octets
- Sommes distinctes : 69 812 223
- Sommes avec au moins 2 triples : 204 472
- Sommes avec au moins 3 triples : 8 458
- Taille maximale d'un groupe : 12
- Paires de triples : 46 884
- Paires disjointes : 46 775
- Alignements testés : 280 650
- Troisièmes lignes puissances : 0
- Troisièmes triples indexés : 0
- Solutions uniques : 0
- Temps de recherche cumulé des shards : 60,7759078000672 s

Artefacts : `work/fourth_R750`, le CSV et le résumé JSON R750, et
`scripts/run_fourth_R750.ps1`.

## Puissances quatrièmes — R = 1000

- Date : 11 juillet 2026
- Puissance : 4
- Racines : 1 à 1000, positives et globalement distinctes
- Shards : 256
- Triples : 166 167 000
- Shards terminés : 256/256
- Recherche complète : oui
- Validation du format disque : OK
- Taille des records sur disque : 1 994 004 000 octets
- Sommes distinctes : 165 753 013
- Sommes avec au moins 2 triples : 385 177
- Sommes avec au moins 3 triples : 15 801
- Taille maximale d'un groupe : 12
- Paires de triples : 92 301
- Paires disjointes : 92 127
- Alignements testés : 552 762
- Troisièmes lignes puissances : 0
- Troisièmes triples indexés : 0
- Solutions uniques : 0
- Temps de recherche cumulé des shards : 150,452065200094 s

Artefacts : `work/fourth_R1000`, le CSV et le résumé JSON R1000, et
`scripts/run_fourth_R1000.ps1`.

## Puissances quatrièmes — R = 1500

- Date : 11 juillet 2026
- Puissance : 4
- Racines : 1 à 1500, positives et globalement distinctes
- Shards : 256
- Triples : 561 375 500
- Shards terminés : 256/256
- Recherche complète : oui
- Validation du format disque : OK
- Taille des records sur disque : 8 982 008 000 octets
- Sommes distinctes : 560 366 519
- Sommes avec au moins 2 triples : 936 372
- Sommes avec au moins 3 triples : 37 858
- Taille maximale d'un groupe : 12
- Paires de triples : 236 697
- Paires disjointes : 236 359
- Alignements testés : 1 418 154
- Troisièmes lignes puissances : 0
- Troisièmes triples indexés : 0
- Solutions uniques : 0
- Temps de recherche cumulé des shards : 421,635932199992 s

Artefacts : `work/fourth_R1500`, le CSV et le résumé JSON R1500, et
`scripts/run_fourth_R1500.ps1`.

## Puissances quatrièmes — R = 1750

- Date : 14 juillet 2026
- Triples : 891 698 500 ; shards : 256/256 ; validation : OK
- Records : 14 267 176 000 octets ; sommes distinctes : 890 290 058
- Groupes >=2 : 1 305 665 ; groupes >=3 : 52 643 ; groupe maximal : 16
- Paires : 337 369 ; disjointes : 336 942 ; alignements : 2 021 652
- Troisièmes lignes puissances : 0 ; solutions uniques : 0
- Temps de recherche : 675,4966938 s ; temps total : 788,38 s
- Artefacts : `work/fourth_R1750`, CSV, résumé JSON, rapport et `scripts/run_fourth_R1750.ps1`.

## Puissances quatrièmes — R = 2000

- Date : 15 juillet 2026
- Triples : 1 331 334 000 ; shards : 256/256 ; validation : OK
- Records : 21 301 344 000 octets ; sommes distinctes : 1 329 459 288
- Groupes >=2 : 1 736 045 ; groupes >=3 : 69 930 ; groupe maximal : 16
- Paires : 457 852 ; disjointes : 457 323
- Alignements : 2 743 938
- Troisièmes lignes puissances : 0 ; troisièmes triples indexés : 0
- Solutions uniques : 0
- Temps de recherche : 990,3160145 s ; temps mural : 1 140,57 s

Le moteur V2 séquentiel a terminé la génération, les 256 shards et l'agrégation
sans interruption. La validation indépendante des records et les 22 tests
unitaires sont réussis. Le script de reprise parallèle à huit workers a été
préparé comme voie de secours mais n'a pas été nécessaire pour ce run.

Artefacts : `work/fourth_R2000`, CSV nul, résumé JSON, rapport,
`scripts/run_fourth_R2000.ps1` et `scripts/resume_fourth_R2000_parallel.ps1`.
## Cubes — R = 2250

- Date : 14 juillet 2026
- Triples : 1 895 907 000 ; shards : 256/256 ; validation : OK
- Records : 30 334 512 000 octets ; sommes distinctes : 1 636 956 745
- Groupes >=2 : 212 018 959 ; groupes >=3 : 36 679 400 ; groupe maximal : 20
- Paires : 144 415 564 ; disjointes : 139 400 318 ; alignements : 836 401 908
- Troisièmes lignes puissances : 0 ; solutions uniques : 0
- Temps de recherche : 2 445,4517467 s ; temps total : 2 641,13 s
- Artefacts : `work/cubes_R2250`, CSV, résumé JSON, rapport et `scripts/run_cubes_R2250.ps1`.

## Cubes — R = 2500

- Date : 15 juillet 2026
- Triples : 2 601 042 500 ; shards : 256/256 ; validation : OK
- Records : 41 616 680 000 octets ; sommes distinctes : 2 245 424 704
- Groupes >=2 : 291 045 440 ; groupes >=3 : 50 417 211 ; groupe maximal : 21
- Paires : 198 764 432 ; disjointes : 192 263 004
- Alignements : 1 153 578 024
- Troisièmes lignes puissances : 0 ; troisièmes triples indexés : 0
- Solutions uniques : 0
- Temps cumulé des shards : 4 657,6458134 s ; temps mural : 1 661,74 s

La génération complète et les 31 premiers shards ont utilisé le moteur V2
séquentiel. Les 225 shards restants ont été repris avec huit workers via
`search_semimagic_shards_parallel.py`, sans recalculer les shards achevés.
L'agrégation finale, la validation des 2 601 042 500 records et les 22 tests
unitaires sont toutes réussies.

Artefacts : `work/cubes_R2500`, CSV nul, résumé JSON, rapport,
`scripts/run_cubes_R2500.ps1` et `scripts/resume_cubes_R2500_parallel.ps1`.
## Carrés — catalogue R = 160 à R = 320

Tous les runs utilisent des racines positives globalement distinctes, 256 shards, le moteur V2 exact et ont été validés avant le palier suivant.

| R | Triples | Sommes | Groupes >=3 | Groupe max. | Alignements | Solutions |
|---:|---:|---:|---:|---:|---:|---:|
| 160 | 669 920 | 52 455 | 43 444 | 76 | 38 142 474 | 111 |
| 200 | 1 313 400 | 83 426 | 70 655 | 94 | 96 287 790 | 220 |
| 250 | 2 573 000 | 132 529 | 114 391 | 119 | 241 468 878 | 466 |
| 320 | 5 410 240 | 220 806 | 193 783 | 154 | 664 656 990 | 1 011 |

Artefacts : `work/squares_R<R>`, `results/squares/semimagic_3x3_squares_R<R>.csv` et `logs/squares/semimagic_3x3_squares_R<R>_summary.json`.

## Carrés — R = 400

- Date : 14 juillet 2026
- Racines : 1 à 400, positives et globalement distinctes
- Triples : 10 586 800 ; shards : 256/256 ; validation : OK
- Records : 127 041 600 octets ; sommes distinctes : 349 893
- Groupes >=2 : 327 927 ; groupes >=3 : 311 267 ; groupe maximal : 202
- Paires : 292 279 929 ; disjointes : 275 339 536
- Alignements : 1 652 037 216
- Troisièmes lignes carrées : 12 199 ; troisièmes triples indexés : 3 900
- Solutions canoniques uniques : 1 950
- Temps de recherche : 1 465,3741122 s ; temps total : 1 472,29 s
- Artefacts : `work/squares_R400`, CSV, résumé JSON et rapport R400.

## Carrés — R = 500

- Date : 15 juillet 2026
- Racines : 1 à 500, positives et globalement distinctes
- Triples : 20 708 500 ; shards : 256/256 ; validation : OK
- Records : 248 502 000 octets ; sommes distinctes : 553 403
- Groupes >=2 : 522 126 ; groupes >=3 : 498 338 ; groupe maximal : 261
- Paires : 717 849 658 ; disjointes : 682 753 714
- Alignements : 4 096 522 284
- Troisièmes lignes carrées : 22 744 ; troisièmes triples indexés : 7 322
- Solutions canoniques uniques : 3 661 ; solutions primitives : 3 054
- Temps de recherche : 3 776,288869 s ; temps total : 3 786,13 s

L'analyse des six transversales de chaque orbite trouve quatre classes avec
une transversale de somme magique, de racines maximales 127, 254, 381 et 446.
Les trois premières sont la classe de Sallows et ses changements d'échelle par
2 et 3 ; la classe de racine maximale 446 est primitive et distincte. Chacune
possède exactement une telle transversale, donc aucune classe n'est pleinement
magique.

Artefacts : `work/squares_R500`, CSV principal, catalogues complet, primitif et
à diagonale magique, résumé JSON, rapport R500 et `scripts/run_squares_R500.ps1`.
## Carrés — R = 750

- Date : 15 juillet 2026
- Racines : 1 à 750, positives et globalement distinctes
- Triples : 70 031 500 ; shards : 256/256 ; validation : OK
- Records : 840 378 000 octets ; sommes distinctes : 1 269 997
- Groupes >=2 : 1 211 390 ; groupes >=3 : 1 165 348 ; groupe maximal : 390
- Paires : 3 660 483 077 ; disjointes : 3 529 749 523
- Alignements : 21 178 497 138
- Troisièmes lignes carrées : 67 371 ; troisièmes triples indexés : 21 946
- Solutions canoniques uniques : 10 973 ; solutions primitives : 8 816
- Temps cumulé des shards : 21 514,0638975 s ; temps mural : 6 214,80 s

L'analyse indépendante des six transversales de chaque classe trouve six
classes de racines maximales 127, 254, 381, 446, 508 et 635. Les classes 127,
254, 381, 508 et 635 sont Sallows et ses changements d'échelle par 2, 3, 4 et
5. La classe 446 reste la seule autre classe primitive. Chacune possède une
seule transversale magique et aucune classe n'est pleinement magique.

Le run a commencé avec le moteur séquentiel validé, puis a repris après 53
shards avec huit workers indépendants. L'orchestration parallèle réutilise
exactement `search_one_shard` et ses écritures JSON atomiques ; son équivalence
avec la voie séquentielle a été vérifiée sur les 22 100 records du run R52,
avec statistiques et CSV scientifiques identiques.

Artefacts : `work/squares_R750`, CSV principal, catalogues complet, primitif et
à diagonale magique, résumé JSON, rapport R750, `scripts/run_squares_R750.ps1`
et `scripts/resume_squares_R750_parallel.ps1`.

## Ordre de reprise convenu

1. Carrés : poursuivre vers le palier R = 1500 par incréments prudents.
2. Sous-projet semi-bimagic : grille initiale magique et grille des carrés semi-magique.

Ne pas lancer de recherche power 4 à R = 5000.

## Carrés — R = 1000

- Date : 16 juillet 2026
- Racines : 1 à 1000, positives et globalement distinctes
- Triples : 166 167 000 ; shards : 256/256 ; validation : OK
- Records : 1 994 004 000 octets ; sommes distinctes : 2 285 787
- Groupes >=2 : 2 193 675 ; groupes >=3 : 2 120 161 ; groupe maximal : 520
- Paires : 11 615 079 060 ; disjointes : 11 284 537 468
- Alignements : 67 707 224 808
- Troisièmes lignes carrées : 141 800 ; troisièmes triples indexés : 46 430
- Solutions canoniques uniques : 23 215 ; solutions primitives : 18 248
- Temps cumulé des shards : 70 086,5976858 s ; temps mural : 8 793,16 s

L'analyse des orbites trouve dix classes à transversale magique. Sept sont les changements d'échelle ×1 à ×7 de Sallows, deux sont la classe 446 et son changement d'échelle ×2, et une classe primitive supplémentaire a pour racine maximale 878. Chacune possède exactement une transversale magique ; aucune classe n'est pleinement magique. La classe R878 est nouvelle dans le catalogue du projet, sans préjuger d'une éventuelle antériorité externe.

La validation des 166 167 000 records et les 22 tests du moteur réussissent. Artefacts : `work/squares_R1000`, CSV principal, catalogues complet, primitif et à diagonale magique, résumé JSON, rapport R1000 et `scripts/run_squares_R1000_parallel.ps1`.
