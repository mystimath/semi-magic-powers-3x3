# Prototype à transversale imposée — 21 juillet 2026

## Résultat borné

Le mode `--require-magic-transversal` a été validé par une recherche autonome
sur les shards existants des carrés jusqu'à `R = 127`.

- 333 375 triples de racines ;
- 14 545 896 alignements examinés ;
- 6 troisièmes lignes candidates après la contrainte de transversale ;
- 2 troisièmes triples présents dans l'index ;
- 1 classe canonique obtenue : la classe attendue de racine maximale 127.

Le résultat correspond exactement à la première entrée du catalogue de
référence `reports/lo_shu/catalog_R1000_lo_shu.csv`.

## Filtre précoce

Avant de calculer la troisième ligne, pour deux premières lignes `A`, `B` et
une transversale d'indices `(i, j, k)`, la condition est

`A[i] + B[j] = A[k] + B[k]`.

Elle est nécessaire et suffisante une fois la troisième ligne imposée par les
sommes de colonnes. Le moteur l'applique donc avant les tests de puissances de
la troisième ligne. Les sorties de ce mode vivent dans un espace distinct du
cache exhaustif.

## Limite observée

Le filtre réduit fortement les candidats tardifs, mais pas encore le nombre de
paires et d'alignements. Une reprise brute à `R = 500` conserverait environ
4,1 milliards d'alignements : ce n'est pas une extension rationnelle.

## Pivot retenu

Toute grille semi-magique possédant une transversale magique peut être ramenée,
par permutation de colonnes, à une grille dont la diagonale principale est
magique. Pour les valeurs `a, e, i` de cette diagonale et `b` en position
(1,2), la grille est nécessairement

```text
a        b        e + i - b
2i - b   e        a + b - i
e-i+b    a+i-b    i
```

Le prochain moteur doit générer cette forme directement, en ne conservant que
les choix où les neuf expressions sont des carrés distincts. Cette
paramétrisation est implémentée et testée dans
`src/semimagic_core.py::build_transversal_normalized_grid`.
