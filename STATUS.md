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
- [x] Cubes jusqu'à `R = 500` : recherche complète, résultat nul.
- [x] Cubes jusqu'à `R = 750` : recherche complète, résultat nul.
- [x] Cubes jusqu'à `R = 1000` : recherche complète, résultat nul.
- [x] Cubes jusqu'à `R = 1500` : recherche complète, résultat nul.
- [x] Cubes jusqu'à `R = 2000` : recherche complète, résultat nul.
- [x] Puissances quatrièmes jusqu'à `R = 250` : recherche complète, résultat nul.
- [x] Puissances quatrièmes jusqu'à `R = 500` : recherche complète, résultat nul.
- [x] Puissances quatrièmes jusqu'à `R = 750` : recherche complète, résultat nul.
- [x] Puissances quatrièmes jusqu'à `R = 1000` : recherche complète, résultat nul.

Les chiffres exacts et commandes sont consignés dans `RUNS.md`. Aucun résultat
n'est annoncé avant la fin et l'agrégation de tous les shards.

## Suite

- Étudier les 47 autres classes semi-magiques trouvées à `power = 2`, `R = 127`.
- Ajouter séparément un mode autorisant les racines répétées pour retrouver Parker.
- [x] Valider le run des puissances quatrièmes `R = 250`.
- [x] Préparer le script `R = 500` sans lancer ce run.
- [x] Vérifier les ressources puis exécuter et valider `R = 500`.
- [ ] Prochain palier cubes à évaluer : `R = 2000` ou une optimisation ciblée.
- Définir séparément la notion de presque-solution avant toute recherche 8/9,
  7/9 ou 6/9.
