# État du chantier

## Phase 0 — Socle initial

- [x] Définition de la structure semi-magique 3×3.
- [x] Génération des puissances.
- [x] Regroupement des triples par somme.
- [x] Déduction de la troisième ligne.
- [x] Vérification exacte des puissances.
- [x] Racines positives.
- [x] Racines globalement distinctes.
- [x] Canonicalisation sous permutations de lignes, permutations de colonnes
      et transposition.
- [x] Export CSV.
- [x] Résumé JSON.
- [x] Profilage des collisions de sommes.
- [x] Affichage et validation d'une solution.
- [x] Tests unitaires.

## Phase 1 — Premiers runs

- [ ] Cubes jusqu'à `R = 100`.
- [ ] Cubes jusqu'à `R = 150`.
- [ ] Puissances quatrièmes jusqu'à `R = 80`.
- [ ] Puissances quatrièmes jusqu'à `R = 120`.
- [ ] Mesurer mémoire, temps et distribution des groupes.

## Phase 2 — Montée en charge

- [ ] Backend SQLite ou tri externe.
- [ ] Génération par blocs.
- [ ] Parallélisation des sommes candidates.
- [ ] Reprise après interruption.
- [ ] Journalisation détaillée.
- [ ] Comparaison Python / NumPy / C++.

## Phase 3 — Presque-solutions

Avant de coder, fixer précisément la définition :

1. les six sommes de lignes et colonnes restent-elles exactes ?
2. combien d'entrées doivent être des puissances ?
3. une entrée libre peut-elle être négative ou nulle ?
4. les racines doivent-elles rester distinctes ?
5. comment classer la qualité des objets trouvés ?

- [ ] Recherche 8/9.
- [ ] Recherche 7/9.
- [ ] Recherche 6/9.

## Résultats

Aucun run scientifique n'est encore enregistré dans ce dépôt initial.
