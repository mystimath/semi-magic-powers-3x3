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

- [x] Cubes jusqu'à `R = 500` : recherche complète, résultat nul.
- [x] Puissances quatrièmes jusqu'à `R = 250` : recherche complète, résultat nul.
- [ ] Puissances quatrièmes jusqu'à `R = 500`.

Les chiffres exacts et commandes sont consignés dans `RUNS.md`. Aucun résultat
n'est annoncé avant la fin et l'agrégation de tous les shards.

## Suite

- [x] Valider le run des puissances quatrièmes `R = 250`.
- [x] Préparer le script `R = 500` sans lancer ce run.
- [ ] Vérifier une dernière fois les ressources disponibles avant de lancer `R = 500`.
- Définir séparément la notion de presque-solution avant toute recherche 8/9,
  7/9 ou 6/9.
