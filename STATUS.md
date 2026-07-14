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
- [x] Cubes jusqu'à `R = 500` : recherche complète, résultat nul.
- [x] Cubes jusqu'à `R = 750` : recherche complète, résultat nul.
- [x] Cubes jusqu'à `R = 1000` : recherche complète, résultat nul.
- [x] Cubes jusqu'à `R = 1500` : recherche complète, résultat nul.
- [x] Cubes jusqu'à `R = 2000` : recherche complète, résultat nul.
- [x] Cubes jusqu'à `R = 2250` : recherche complète, résultat nul.
- [x] Puissances quatrièmes jusqu'à `R = 250` : recherche complète, résultat nul.
- [x] Puissances quatrièmes jusqu'à `R = 500` : recherche complète, résultat nul.
- [x] Puissances quatrièmes jusqu'à `R = 750` : recherche complète, résultat nul.
- [x] Puissances quatrièmes jusqu'à `R = 1000` : recherche complète, résultat nul.
- [x] Puissances quatrièmes jusqu'à `R = 1500` : recherche complète, résultat nul.
- [x] Puissances quatrièmes jusqu'à `R = 1750` : recherche complète, résultat nul.

Les chiffres exacts et commandes sont consignés dans `RUNS.md`. Aucun résultat
n'est annoncé avant la fin et l'agrégation de tous les shards.

## Suite

- [ ] Terminer le catalogue `power = 2` à `R = 500`.
- [ ] Après R = 500, vérifier toutes les classes power = 2 sur leur orbite et
  extraire celles ayant au moins une diagonale de somme magique (au moins 7/8 lignes).
- [ ] Définir ensuite le sous-projet bi-semi-magique : grille initiale magique,
  grille des carrés semi-magique.
- Ajouter séparément un mode autorisant les racines répétées pour retrouver Parker.
- [x] Valider le run des puissances quatrièmes `R = 250`.
- [x] Préparer le script `R = 500` sans lancer ce run.
- [x] Vérifier les ressources puis exécuter et valider `R = 500`.
- [ ] Terminer les puissances quatrièmes à `R = 2000` et les cubes à `R = 2500`.
- Définir séparément la notion de presque-solution avant toute recherche 8/9,
  7/9 ou 6/9.
