# État du chantier

## Socle exact

- [x] Génération des puissances et regroupement exact des triples.
- [x] Déduction exacte de la troisième ligne.
- [x] Racines positives et globalement distinctes.
- [x] Canonicalisation sous lignes, colonnes et transposition.
- [x] Backend V2 NumPy sur disque, sharding et reprise.
- [x] Export CSV, résumé JSON et validation du work-dir.
- [x] Tests unitaires du cœur et du backend.

## Runs scientifiques

- [x] Carrés jusqu'à `R = 52` : première classe observée, unique à cette borne.
- [x] Carrés jusqu'à `R = 127` : 48 classes semi-magiques, dont Sallows.
- [x] Carrés jusqu'à `R = 160` : 111 classes semi-magiques.
- [x] Carrés jusqu'à `R = 200` : 220 classes semi-magiques.
- [x] Carrés jusqu'à `R = 250` : 466 classes semi-magiques.
- [x] Carrés jusqu'à `R = 320` : 1 011 classes semi-magiques.
- [x] Carrés jusqu'à `R = 400` : 1 950 classes semi-magiques.
- [x] Carrés jusqu'à `R = 500` : 3 661 classes semi-magiques, dont 3 054 primitives.
- [x] Analyse des orbites `power = 2` à `R = 500` : 4 classes avec une
  transversale de somme magique, aucune classe pleinement magique.
- [x] Carrés jusqu'à `R = 750` : 10 973 classes semi-magiques, dont 8 816 primitives.
- [x] Analyse des orbites `power = 2` à `R = 750` : 6 classes avec une
  transversale magique ; les deux ajouts sont Sallows ×4 et ×5, sans nouvelle
  classe primitive au-delà de la classe 446.
- [x] Carrés jusqu'à `R = 1000` : 23 215 classes semi-magiques, dont 18 248 primitives.
- [x] Analyse des orbites `power = 2` à `R = 1000` : 10 classes avec une
  transversale magique ; nouvelle classe primitive du catalogue à racine
  maximale 878, sans présumer de son antériorité externe.
- [x] Catalogue spécialisé Lo Shu jusqu'à `R = 5000` : 63 classes à
  transversale magique, dont 10 primitives. Les sept nouvelles classes
  primitives du catalogue du projet au-delà de `R = 1000` ont pour racines
  maximales 2434, 2982, 3134, 3191, 3642, 4583 et 4893 ; aucune revendication
  d'antériorité externe. Artefact :
  `reports/lo_shu/direct_catalog_R5000_20260721.json`.
- [x] Catalogue spécialisé Lo Shu jusqu'à `R = 10000` : 137 classes et 17
  primitives ; sept nouvelles classes primitives au-delà de `R = 5000`, dont
  trois distinctes de racine maximale 6271. Artefact :
  `reports/lo_shu/direct_catalog_R10000_20260721.json`.
- [x] Cubes jusqu'à `R = 500` : recherche complète, résultat nul.
- [x] Cubes jusqu'à `R = 750` : recherche complète, résultat nul.
- [x] Cubes jusqu'à `R = 1000` : recherche complète, résultat nul.
- [x] Cubes jusqu'à `R = 1500` : recherche complète, résultat nul.
- [x] Cubes jusqu'à `R = 2000` : recherche complète, résultat nul.
- [x] Cubes jusqu'à `R = 2250` : recherche complète, résultat nul.
- [x] Cubes jusqu'à `R = 2500` : recherche complète, résultat nul.
- [x] Puissances quatrièmes jusqu'à `R = 250` : recherche complète, résultat nul.
- [x] Puissances quatrièmes jusqu'à `R = 500` : recherche complète, résultat nul.
- [x] Puissances quatrièmes jusqu'à `R = 750` : recherche complète, résultat nul.
- [x] Puissances quatrièmes jusqu'à `R = 1000` : recherche complète, résultat nul.
- [x] Puissances quatrièmes jusqu'à `R = 1500` : recherche complète, résultat nul.
- [x] Puissances quatrièmes jusqu'à `R = 1750` : recherche complète, résultat nul.
- [x] Puissances quatrièmes jusqu'à `R = 2000` : recherche complète, résultat nul.

Les chiffres exacts et commandes sont consignés dans `RUNS.md`. Aucun résultat
n'est annoncé avant la fin et l'agrégation de tous les shards.

## Suite

- [x] Étendre le catalogue des carrés à `R = 1000`.
- [ ] Étendre progressivement le catalogue des carrés jusqu'à `R = 1500`.
- [x] Prototyper un moteur à transversale imposée : validation autonome à
  `R = 127`, puis équivalence spécialisée validée à `R = 500`. Le moteur Lo Shu
  est désormais le chemin de référence pour cette cible.
- [ ] Étendre progressivement le catalogue spécialisé Lo Shu au-delà de
  `R = 10000`, avec artefact JSON, test de régression et vérification des
  classes primitives à chaque palier.

- [x] Terminer le catalogue `power = 2` à `R = 500`.
- [x] Après R = 500, vérifier toutes les classes power = 2 sur leur orbite et
  extraire celles ayant au moins une diagonale de somme magique (au moins 7/8 lignes).
- [ ] Définir ensuite le sous-projet bi-semi-magique : grille initiale magique,
  grille des carrés semi-magique.
- Ajouter séparément un mode autorisant les racines répétées pour retrouver Parker.
- [x] Valider le run des puissances quatrièmes `R = 250`.
- [x] Préparer le script `R = 500` sans lancer ce run.
- [x] Vérifier les ressources puis exécuter et valider `R = 500`.
- [x] Terminer les puissances quatrièmes à `R = 2000`.
- [x] Terminer les cubes à `R = 2500`.
- Définir séparément la notion de presque-solution avant toute recherche 8/9,
  7/9 ou 6/9.
