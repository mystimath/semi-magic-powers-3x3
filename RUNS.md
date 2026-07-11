# Exécutions scientifiques

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

Le script `scripts/run_fourth_R500.ps1` est préparé. Ce run n'a pas été lancé.
