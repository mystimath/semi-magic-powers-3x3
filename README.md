# Carrés semi-magiques 3×3 de puissances

Recherche expérimentale de carrés semi-magiques 3×3 dont les neuf entrées sont
des puissances parfaites :

- cubes (`k = 3`) ;
- puissances quatrièmes (`k = 4`).

Une grille

```text
A B C
D E F
G H I
```

est semi-magique lorsque ses trois lignes et ses trois colonnes ont la même
somme `S`. Les diagonales ne sont pas imposées.

## État du projet

Le socle initial couvre la recherche **exacte**, avec :

- racines positives ;
- racines globalement distinctes par défaut ;
- génération des triples de même somme ;
- construction de la troisième ligne à partir des deux premières ;
- élimination des doublons par symétries de lignes, colonnes et transposition ;
- export CSV ;
- résumé JSON ;
- outils de profilage et d'affichage ;
- tests unitaires.

La recherche des presque-solutions `8/9`, `7/9` et `6/9` est volontairement
réservée à une étape ultérieure, car elle nécessite une définition précise de
la notion de défaut.

## Arborescence

```text
semi-magic-powers-3x3/
├── README.md
├── STATUS.md
├── METHODOLOGY.md
├── pyproject.toml
├── .gitignore
├── src/
│   ├── __init__.py
│   ├── semimagic_core.py
│   ├── search_semimagic_3x3_powers.py
│   ├── profile_triple_sums.py
│   └── show_semimagic_square.py
├── tests/
│   └── test_semimagic_core.py
├── results/
│   ├── cubes/.gitkeep
│   └── fourth-powers/.gitkeep
└── logs/
    └── .gitkeep
```

## Principe de recherche

On génère les puissances :

```text
1^k, 2^k, ..., R^k
```

Puis les triples non ordonnés de racines :

```text
a < b < c
```

regroupés par somme :

```text
a^k + b^k + c^k = S
```

Pour deux lignes de même somme :

```text
A B C
D E F
```

la troisième ligne est forcée par les colonnes :

```text
G = S - A - D
H = S - B - E
I = S - C - F
```

Il suffit alors de vérifier que `G`, `H` et `I` sont eux aussi des puissances
k-ièmes autorisées.

## Installation

Aucune dépendance externe n'est requise.

Sous PowerShell :

```powershell
cd semi-magic-powers-3x3
python --version
python -m unittest discover -s tests -v
```

Python 3.10 ou supérieur est recommandé.

## Première recherche sur les cubes

Commencer avec une borne raisonnable :

```powershell
python src/search_semimagic_3x3_powers.py `
  --power 3 `
  --max-root 100 `
  --distinct-roots `
  --positive `
  --target exact `
  --progress 25000 `
  --out results/cubes/semimagic_3x3_cubes_R100.csv `
  --summary-json logs/semimagic_3x3_cubes_R100_summary.json
```

## Première recherche sur les puissances quatrièmes

```powershell
python src/search_semimagic_3x3_powers.py `
  --power 4 `
  --max-root 80 `
  --distinct-roots `
  --positive `
  --target exact `
  --progress 25000 `
  --out results/fourth-powers/semimagic_3x3_fourth_R80.csv `
  --summary-json logs/semimagic_3x3_fourth_R80_summary.json
```

## Profilage des collisions de sommes

```powershell
python src/profile_triple_sums.py `
  --power 3 `
  --max-root 100 `
  --top 20 `
  --progress 25000
```

## Afficher une solution CSV

```powershell
python src/show_semimagic_square.py `
  results/cubes/semimagic_3x3_cubes_R100.csv `
  --index 0
```

## Limites du prototype

Le nombre de triples distincts vaut `C(R, 3)` :

- `R = 100` : 161 700 triples ;
- `R = 250` : 2 573 000 triples ;
- `R = 500` : 20 708 500 triples.

La version initiale travaille en mémoire. Elle bloque par défaut les recherches
dépassant cinq millions de triples. L'option `--force-large` permet de lever
cette protection, mais une future version SQLite, NumPy ou C++ sera préférable
pour les très grandes bornes.
