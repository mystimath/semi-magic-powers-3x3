# Méthodologie

## 1. Définition

On cherche neuf racines entières `r1, ..., r9` telles que les valeurs
`r1^k, ..., r9^k` forment une grille 3×3 dont les trois lignes et les trois
colonnes ont une même somme `S`.

Les diagonales sont libres.

## 2. Réduction du problème

On choisit deux lignes de même somme :

```text
A B C
D E F
```

La troisième ligne est déterminée :

```text
G = S - A - D
H = S - B - E
I = S - C - F
```

Les colonnes valent alors `S`, et la troisième ligne vaut automatiquement `S`.

## 3. Symétries

La propriété est préservée par :

- les 6 permutations de lignes ;
- les 6 permutations de colonnes ;
- la transposition.

Le programme calcule donc une forme canonique parmi au plus 72 représentations.

## 4. Réduction des permutations

Pour chaque paire de triples :

- la première ligne est conservée dans l'ordre croissant ;
- seules les permutations distinctes de la deuxième ligne sont testées.

Toute solution peut être ramenée à cette forme par permutation des colonnes.

## 5. Racines distinctes

Avec `--distinct-roots`, les neuf racines doivent être toutes différentes.

## 6. Validation

Chaque résultat est revérifié : puissances autorisées, positivité, distinction
des racines, égalité des trois lignes et des trois colonnes.
