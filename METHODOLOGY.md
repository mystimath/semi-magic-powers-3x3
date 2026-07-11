# Méthodologie

## 1. Définition

On cherche neuf racines entières positives et distinctes `r1, ..., r9` telles
que les valeurs `r1^k, ..., r9^k`, avec `k` égal à 3 ou 4, forment une grille
3×3 dont les trois lignes et les trois colonnes ont une même somme `S`. Les
diagonales sont libres.

## 2. Réduction exacte

Les triples non ordonnés `a < b < c` sont regroupés par somme
`a^k + b^k + c^k = S`. Pour deux lignes de même somme,

```text
A B C
D E F
```

la troisième ligne est imposée par les colonnes :

```text
G = S - A - D
H = S - B - E
I = S - C - F
```

Si `G`, `H` et `I` sont des puissances k-ièmes autorisées, leur somme vaut
automatiquement `S`. Le moteur contrôle ensuite la distinction globale des neuf
racines et l'égalité exacte des six sommes.

## 3. Symétries

La propriété est préservée par les 6 permutations de lignes, les 6 permutations
de colonnes et la transposition. Une forme canonique parmi au plus 72
représentations élimine les doublons. Pour chaque paire de triples, la première
ligne reste croissante et les 6 permutations de la seconde sont testées.

## 4. Backend V2 sur disque

Les `C(R, 3)` triples sont encodés dans des records NumPy `(sum, code)` et
répartis dans des shards selon leur somme. Le manifeste enregistre après chaque
valeur de la première racine le nombre de records et la taille validée de chaque
shard. Au redémarrage, tout octet au-delà des tailles du manifeste est tronqué,
ce qui rend la génération reprenable sans duplication.

Chaque shard est trié par somme puis par code. Seuls les groupes comptant au
moins trois triples peuvent fournir les trois lignes. Pour chaque paire de
triples disjoints et chaque alignement, la troisième ligne est calculée puis
recherchée dans la table exacte des puissances et dans le groupe indexé.

La recherche écrit un JSON atomique par shard. Une reprise ignore les shards
déjà terminés. L'agrégation n'est considérée complète que si les 256 fichiers de
résultat sont présents. Le CSV et le résumé global ne constituent un résultat
scientifique publiable que lorsque `search_complete` vaut `true` et
`completed_shards` vaut le nombre total de shards.

## 5. Validation

La phase `validate` vérifie la compatibilité du manifeste, la taille de chaque
shard, l'alignement sur la taille d'un record et le nombre total de records.
Après un run, on contrôle aussi le JSON agrégé, le CSV et la cohérence des
statistiques (`records`, `solutions`, `results_count`).
