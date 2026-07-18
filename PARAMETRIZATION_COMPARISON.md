# Comparaison de la paramétrisation Lo Shu des carrés semi-magiques 3×3

_Audit local et expérience du 18 juillet 2026._

## Conclusion exécutive

La représentation `(x,r,u,v)` est une forme linéaire exacte de tout carré
semi-magique 3×3 auquel on a ajouté une diagonale de somme commune, après
orientation convenable. Elle a quatre degrés de liberté, exactement comme cet
espace linéaire. Elle ne réduit donc pas à elle seule l'espace mathématique.

Pour neuf entrées carrées, sa lecture utile est `(A,B,C,r)` : les neuf valeurs
sont trois progressions arithmétiques de trois carrés partageant la raison
`r`. L'index naturel est d'abord la raison, puis le premier terme. Dans le cas
pleinement magique, `A+C=2B`; cette spécialisation est exactement la
formulation B2 déjà publiée dans le dépôt voisin.

L'implémentation spécialisée ajoutée ici reproduit objet par objet les dix
classes à transversale magique du catalogue exhaustif `R=1000`. À la borne
témoin `R=127`, elle retrouve le même singleton de Sallows que l'oracle général
et réduit le travail de 333 375 triples de racines et 14 557 824 alignements à
51 progressions de carrés et une combinaison. Le rapport de temps observé est
environ 29 460 sur un seul run exploratoire ; ce nombre n'est pas présenté
comme un benchmark confirmatoire multi-machine.

La revue d'antériorité interdit toute revendication de nouveauté pour la
structure algébrique : Robertson formule explicitement le cas pleinement
magique par trois progressions de carrés de même raison, et Bremner étudie déjà
les carrés de neuf carrés ayant sept sommes égales. La contribution locale est
un noyau exact, une canonicalisation documentée, un index spécialisé et leur
validation contre le catalogue Mystimath.

## 1. Périmètre et conventions

On écrit la grille

```text
a b c
d e f
g h i
```

et on choisit l'antidiagonale `c,e,g` comme septième alignement. La convention
Lo Shu est

```text
M1 H3 L2
L3 M2 H1
H2 L1 M3
```

avec

```text
L = (x,             x+r,           x+2r)
M = (x+2r+u,        x+3r+u,        x+4r+u)
H = (x+4r+u+v,      x+5r+u+v,      x+6r+u+v).
```

Les lettres `L`, `M`, `H` sont structurelles. Elles n'imposent ni `L<M<H`, ni
un ordre des racines. `u` et `v` peuvent être négatifs. La raison est rendue
positive par orientation, `r>0`.

## 2. Identités et complétude linéaire

La grille construite est

```text
x+2r+u       x+6r+u+v       x+r
x+2r         x+3r+u         x+4r+u+v
x+5r+u+v     x              x+4r+u
```

Une addition directe donne, pour les trois lignes, les trois colonnes et
l'antidiagonale,

```text
S = 3x + 9r + 2u + v.
```

La diagonale principale est le triplet `M` :

```text
D = 3x + 9r + 3u,
D - S = u - v.
```

La grille est donc pleinement magique si et seulement si `u=v`.

Réciproquement, l'espace des grilles semi-magiques 3×3 a cinq degrés de
liberté. Imposer `c+e+g=S` ajoute une équation indépendante, donc laisse quatre
degrés de liberté. En posant

```text
x = h,
r = c-h,
u = a-d,
v = f-i,
```

et en résolvant les six égalités semi-magiques plus l'antidiagonale, on
retrouve exactement les neuf expressions ci-dessus. La transformation est
donc bijective pour une orientation fixée, hors choix de symétrie et inversion
simultanée des trois progressions.

## 3. Représentation `(A,B,C,r)`

Posons les premiers termes

```text
A = x,
B = x+2r+u,
C = x+4r+u+v.
```

Les trois progressions deviennent

```text
(A, A+r, A+2r)
(B, B+r, B+2r)
(C, C+r, C+2r).
```

La transformation inverse est

```text
x = A,
u = B-A-2r,
v = C-B-2r.
```

Les deux invariants les plus simples sont

```text
S = A+B+C+3r,
D-S = 2B-A-C.
```

Ainsi, le carré est pleinement magique si et seulement si les premiers termes
`A,B,C` forment eux-mêmes une progression :

```text
A+C = 2B.
```

Pour la génération, `(A,B,C,r)` est préférable à `(x,r,u,v)` : ses quatre
variables sont directement les clés d'un catalogue de progressions de carrés.
Pour présenter une grille orientée et son défaut diagonal, `(x,r,u,v)` reste
plus lisible.

## 4. Correspondance avec les moteurs existants

### 4.1 Moteur semi-magique général

Dans ce dépôt :

- `src/semimagic_core.py:51`, `build_triple_groups`, énumère les triples de
  racines et les groupe par somme de puissances ;
- `src/semimagic_core.py:92`, `derive_third_row`, force la troisième ligne à
  partir des deux premières et de la somme ;
- `src/semimagic_core.py:154`, `canonical_grid`, quotient par permutations de
  lignes, permutations de colonnes et transposition ;
- `src/semimagic_disk_backend.py:260`, `generate_shards`, matérialise le même
  index par somme sur disque ;
- `src/semimagic_disk_backend.py:407`, `search_one_shard`, recherche toutes les
  classes semi-magiques d'une boîte ;
- `src/semimagic_v3_backend.py:130`, `_find_solutions`, reprend cette logique
  dans le moteur incrémental ;
- `src/catalog_square_solutions.py:12`, `enrich`, ne génère rien : il valide et
  enrichit les résultats.

Ce moteur est exhaustif pour toutes les classes semi-magiques, avec ou sans
transversale. Ses paramètres effectifs sont deux triples de racines appartenant
au même groupe de somme et une permutation du second ; la troisième ligne est
forcée. Positivité, puissance parfaite, distinction et borne sont intégrées
par les tables et validées après reconstruction. La contrepartie est un espace
énorme lorsque seule la sous-famille à transversale intéresse la recherche.

### 4.2 Formulations A/B du carré pleinement magique

Dans le dépôt voisin `magic-square-of-squares-3x3` :

- `experiments/formulations_comparison/prototypes/model.py:45`,
  `build_centered_grid(center,p,q)`, construit

  ```text
  e-p       e+p+q     e-q
  e+p-q     e         e-p+q
  e+q       e-p-q     e+p ;
  ```

- `model.py:59` et `model.py:84` génèrent les progressions de trois carrés,
  respectivement par oracle quadratique et paramétrisation primitive ;
- `formulation_b1.py:18`, `search_formulation_b1`, indexe les raisons par
  centre carré ;
- `formulation_b2.py:16`, `search_formulation_b2`, indexe les centres par
  raison commune.

Dans l'orientation choisie, la correspondance exacte est

```text
x = e-p-q
r = p
u = q-2p
v = q-2p.
```

Inversement, lorsque `u=v`,

```text
e = x+3r+u
p = r
q = u+2r.
```

Les premiers termes sont `A=e-p-q`, `B=e-p`, `C=e-p+q`. Ils forment une
progression. B2 est donc exactement la branche `A+C=2B` de Lo Shu, avec le
même index principal par `r`. Il ne s'agit pas d'une nouvelle méthode pour le
cas pleinement magique.

La formulation A parcourt trois paramètres libres du carré magique puis teste
les neuf carrés. B1 et B2 intègrent les progressions de carrés avant la
combinaison. Les contraintes de borne, positivité, distinction et primitivité
sont appliquées dans `model.py:131`, `accept_grid`.

### 4.3 Formulations C et D

`formulation_c.py:64`, `progression_to_triangle`, transforme une progression
de trois carrés en triangle rectangle rationnel de même aire. Cette couche ne
change ni `A,B,C,r`, ni le nombre de degrés de liberté ; elle apporte une
interprétation géométrique.

`formulation_d.py:97`, `point_from_progression`, et
`formulation_d.py:135`, `progression_from_point`, expriment chaque progression
sur la courbe congruente `y²=x(x²-r²)`. La sonde D publiée part du même
catalogue entier ; une recherche elliptique autonome serait un autre projet.

### 4.4 Branches partielles à centre non carré

Les scripts `src/search_non_square_center_v2_*.py` du dépôt voisin conservent
les relations du carré pleinement magique centré, mais relâchent les
contraintes de carré sur certaines cases. Ils traitent les motifs 6/9 à 8/9,
pas l'espace de neuf carrés à sept alignements. Ils ne sont donc pas
bijectifs avec la famille étudiée ici.

## 5. Les quatre cas de contrôle

L'extraction est effectuée sur l'orientation fournie par le brief, avant toute
canonicalisation élargie du catalogue.

| Cas | `(x,r,u,v)` | `S` | `D` | `u-v` | Carrés |
|---|---|---:|---:|---:|---:|
| Bremner | `(529,41496,55608,55608)` | 541875 | 541875 | 0 | 7/9 |
| Sallows | `(4,3360,2685,-14013)` | 21609 | 38307 | 16698 | 9/9 |
| max-root 446 | `(111556,43680,-195072,-80595)` | 257049 | 142572 | -114477 | 9/9 |
| max-root 878 | `(253009,127680,-487053,238848)` | 1172889 | 446988 | -725901 | 9/9 |

Pour Bremner, les seules entrées non carrées sont `b=360721` et `i=222121` :
le masque exact est `acdefgh`. Les sept autres entrées sont des carrés
parfaits positifs et les neuf valeurs sont distinctes.

Les paramètres du fichier `reports/lo_shu/catalog_R1000_lo_shu.csv` peuvent
différer de ce tableau. Le tableau conserve la géométrie D4 de l'exemple ; le
CSV choisit en plus un témoin minimal dans l'orbite semi-magique de 72 éléments
afin de rejoindre les clés du catalogue publié. Ces deux quotients ne doivent
pas être confondus.

## 6. Symétries et clés

Deux notions sont nécessaires.

1. **Géométrie D4.** Les huit rotations/réflexions conservent lignes,
   colonnes et diagonales. `canonicalize_semimagic_grid` place la diagonale
   supplémentaire sur l'antidiagonale, impose `r>0`, puis minimise le tuple
   structurel complet
   `(L1,L2,L3,M1,M2,M3,H1,H2,H3)`.
2. **Classe semi-magique S3×S3/transposition.** Les 72 opérations conservent
   les six sommes, mais pas une diagonale géométrique. C'est l'équivalence du
   catalogue R=1000. `canonicalize_semimagic_class` cherche un témoin Lo Shu
   dans cette orbite, sans substituer cette opération à D4.

La clé structurelle complète est recommandée pour D4. Elle est sans perte et
rend les conventions auditables. `(x,r,u,v)` et `(A,B,C,r)` sont bijectifs dans
une orientation valide, mais leur sens est moins immédiat en présence de
plusieurs orientations admissibles, notamment pour un carré pleinement
magique. Pour comparer au catalogue général, la clé de référence reste celle
de `semimagic_core.canonical_grid`.

## 7. Stratégies de recherche

### 7.1 Parcours direct de `(x,r,u,v)`

Sans paramétrer les contraintes de carré, quatre boucles entières doivent
tester neuf expressions. Les bornes naturelles de `u` et `v` dépendent de
`x,r` et de la positivité. Cette forme est bonne pour prouver et classifier,
mais mauvaise comme moteur brut.

### 7.2 Triplets de carrés groupés par raison

On génère chaque progression de carrés

```text
(q0²,q1²,q2²), q1²-q0²=q2²-q1²=r,
```

puis on l'indexe par `(r,premier_terme)`. Si `n_r` progressions partagent la
raison `r`, la branche à sept alignements examine au plus

```text
sum_r C(n_r,3)
```

triplets de progressions, avec un filtre immédiat sur les neuf racines
distinctes. Chaque combinaison valide construit automatiquement les sept
sommes ; il n'est pas nécessaire de retester les six lignes.

Pour le carré pleinement magique, on ne parcourt pas les combinaisons
cubiques : on cherche `A+C=2B` par appartenance dans un ensemble. C'est B2.

### 7.3 Paramétrisation diophantienne des progressions

Le générateur quadratique local est suffisant à `R=1000`, mais pas pour une
grande montée de borne. Le générateur paramétrique déjà validé dans le dépôt
voisin produit les racines

```text
|m²+2mn-n²|, m²+n², |-m²+2mn+n²|
```

puis leurs dilatations, avec déduplication. Il doit être réutilisé ou porté
dans un noyau compilé avant toute expérience à grande borne. Les courbes
elliptiques peuvent générer des progressions rationnelles, mais ne suppriment
pas à elles seules le problème de faire coïncider trois raisons entières.

### 7.4 Index secondaires

- **Raison `r` :** meilleur index primaire ; c'est la contrainte partagée avant
  combinaison.
- **Premier terme :** meilleur index secondaire ; il permet le test
  `A+C=2B` et une reprise par tranches.
- **Somme `S` :** calculée seulement après choix de `A,B,C`; peu sélective en
  amont.
- **Racine centrale :** utile dans B1, mais non commune aux trois progressions
  de la famille à sept alignements.
- **Paramètres diophantiens primitifs et facteur d'échelle :** utiles pour
  produire le catalogue de progressions sans doublons.

L'index `(r,A)` se partitionne naturellement par intervalles de `r`, se
parallélise sans communication pendant la génération et accepte des
checkpoints par groupes de raison.

## 8. Expériences réalisées

### 8.1 Benchmark commun à `R=127`

Domaine : racines entières `1..127`, neuf racines distinctes, entrées carrées,
classes semi-magiques possédant au moins une transversale magique, quotient
S3×S3/transposition.

| Moteur | Temps mur | Temps CPU | Classes |
|---|---:|---:|---:|
| Oracle général par somme | 31,648492 s | 31,546875 s | 1 |
| Index Lo Shu par raison | 0,001074 s | résolution affichée 0 s | 1 |

Les deux ensembles contiennent exactement la clé de Sallows
`2,74,127 / 94,97,58 / 113,82,46`.

Compteurs généraux :

- 333 375 triples de racines ;
- 32 305 sommes distinctes ;
- 2 797 149 paires de triples ;
- 14 557 824 alignements ;
- 339 troisièmes lignes carrées ;
- 288 candidats distincts avant quotient ;
- 6 témoins à transversale, une classe.

Compteurs Lo Shu :

- 51 progressions de carrés ;
- 48 raisons ;
- une raison contenant au moins trois progressions ;
- une combinaison, une classe.

Le rapport de temps est `29459,64`. Limites : un seul run, CPython 3.11.15,
même machine mais pas de mesure de pointe mémoire. Il démontre un gain
structurel dans ce domaine ciblé, pas un facteur universel.

Artefacts : `reports/lo_shu/benchmark_R127.json` et `.csv`.

### 8.2 Contrôle exact du catalogue `R=1000`

La recherche spécialisée produit :

- 647 progressions ;
- 593 raisons ;
- exactement dix raisons avec au moins trois progressions ;
- dix combinaisons disjointes ;
- dix classes, dont trois primitives ;
- aucune classe pleinement magique.

L'ensemble des dix clés est exactement égal au fichier publié
`semimagic-square-878/data/magic_transversal_classes_R1000.csv` : zéro classe
manquante, zéro classe supplémentaire. Les racines maximales sont
`127,254,381,446,508,635,762,878,889,892`.

Artefacts : `reports/lo_shu/catalog_verification_R1000.json` et
`reports/lo_shu/catalog_R1000_lo_shu.csv`.

## 9. Revue d'antériorité

La forme générale du carré magique 3×3 est classique et associée à Lucas ; le
fac-similé du tome IV de ses _Récréations mathématiques_ (1894) est disponible
[ici](https://commons.wikimedia.org/wiki/File:Lucas_-_R%C3%A9cr%C3%A9ations_math%C3%A9matiques,_tome_4,_1894.pdf).

Robertson énonce explicitement en 1996 l'équivalence entre le problème du
carré magique de neuf carrés et trois progressions arithmétiques de trois
carrés de même raison, dont les termes centraux sont eux-mêmes en progression.
Cela correspond exactement à la branche `A+C=2B` décrite ici :
[John P. Robertson, “Magic Squares of Squares”, _Mathematics Magazine_ 69(4),
289–293](https://doi.org/10.1080/0025570X.1996.11996457).

Bremner présente l'exemple de Sallows à sept sommes, construit des familles de
neuf carrés ayant toutes les sommes égales sauf une diagonale et écrit le carré
magique comme trois triplets `{a,a±c}`, `{a+b,a+b±c}`,
`{a-b,a-b±c}`. La famille linéaire à sept alignements et sa lecture en trois
progressions ne peuvent donc pas être revendiquées comme nouvelles :
[Andrew Bremner, “On squares of squares”, _Acta Arithmetica_ 88(3),
289–297](https://doi.org/10.4064/aa-88-3-289-297).

Bremner II distingue ensuite le problème dual — un carré pleinement magique
avec le plus grand nombre possible d'entrées carrées — et étudie
systématiquement les configurations de six entrées carrées ; c'est le bon
contexte pour l'exemple à sept carrés utilisé comme contrôle, mais pas pour le
catalogue de neuf carrés à sept sommes :
[Andrew Bremner, “On squares of squares II”, _Acta Arithmetica_ 99(3),
289–308](https://doi.org/10.4064/aa99-3-6).

Conclusion d'antériorité : aucune revendication de nouvelle paramétrisation
mathématique. L'indexation exhaustive par raison commune, son adaptation au
catalogue Mystimath, la canonicalisation à deux niveaux et les contrôles
R=127/R=1000 constituent une contribution logicielle et expérimentale locale.
Une revendication de nouveauté algorithmique dans la littérature demanderait
une recherche bibliographique beaucoup plus large et une relecture externe.

## 10. Réponses explicites aux dix questions

1. **Équivalence à une forme existante ?** Oui pour la branche pleinement
   magique : elle est B2. Pour sept alignements, c'est l'extension à quatre
   degrés de liberté du carré magique centré à trois degrés.
2. **Transformation exacte ?** `x=e-p-q`, `r=p`, `u=v=q-2p`; inverse
   `e=x+3r+u`, `p=r`, `q=u+2r`. La forme `(A,B,C,r)` est reliée par
   `A=x`, `B=x+2r+u`, `C=x+4r+u+v`.
3. **Familles en plus ou en moins ?** Avec `u` et `v` indépendants, toutes les
   grilles semi-magiques ayant une diagonale supplémentaire ; `u=v` redonne
   exactement les grilles pleinement magiques de cette orientation.
4. **`(A,B,C,r)` préférable ?** Oui pour générer et indexer ; `(x,r,u,v)` est
   préférable pour exposer le défaut `u-v`.
5. **Équivalence avec trois progressions ?** Oui, exactement, pour une grille
   semi-magique avec septième alignement après orientation. Ce n'est pas vrai
   pour une grille semi-magique arbitraire sans transversale.
6. **Condition magique complète ?** Oui : `u=v`, équivalemment `A+C=2B`, est
   nécessaire et suffisante dans cette convention.
7. **Clé minimisant les doublons D4 ?** Le tuple structurel complet après
   filtre sur la diagonale et `r>0`. Pour le catalogue général, conserver la
   clé S3×S3/transposition séparée.
8. **Meilleur index ?** `(r,premier_terme)`, enrichi des racines et d'un facteur
   d'échelle primitif. La somme et le centre sont secondaires.
9. **Accélération ?** Oui, fortement et mesurablement pour la sous-famille à
   transversale ; non comme remplacement du moteur exhaustif de toutes les
   classes semi-magiques. Pour le cas pleinement magique, le gain était déjà
   celui de B2.
10. **Expérience objective suivante ?** Porter le générateur paramétrique de
    progressions dans un noyau secondaire compilé, comparer à bornes
    `R=1000,1250,1500` sur sorties exactes, temps, mémoire et disque, avec au
    moins cinq répétitions pour les phases rapides. Ne lancer cette expérience
    qu'après estimation thermique et de stockage.

## 11. Fichiers ajoutés et commandes de contrôle

Fichiers principaux :

- `src/lo_shu_parametrization.py` : construction, extraction, validation D4 ;
- `src/lo_shu_catalog.py` : pont explicite vers l'orbite semi-magique de 72 ;
- `src/lo_shu_search.py` : catalogue de progressions et recherche spécialisée ;
- `scripts/compare_parametrizations.py` : conversion de catalogues et
  benchmark de référence ;
- `scripts/benchmark_lo_shu.py` : micro-benchmark filtré ;
- `scripts/verify_lo_shu_catalog.py` : comparaison exacte des ensembles ;
- `tests/test_lo_shu_parametrization.py` et `tests/test_lo_shu_r1000.py`.

Commandes exécutées :

```powershell
python -m pytest -q tests\test_lo_shu_parametrization.py
python scripts\benchmark_lo_shu.py --max-root 127
python -m pytest -q tests\test_lo_shu_r1000.py
python scripts\compare_parametrizations.py catalog `
  C:\dev\mystimath\semimagic-square-878\data\magic_transversal_classes_R1000.csv `
  reports\lo_shu\catalog_R1000_lo_shu.csv --expected-count 10
python scripts\verify_lo_shu_catalog.py `
  C:\dev\mystimath\semimagic-square-878\data\magic_transversal_classes_R1000.csv `
  --max-root 1000
python -m pytest -q
git diff --check
```

Deux tentatives préliminaires du benchmark de référence avec suivi mémoire ont
été arrêtées automatiquement à 120 secondes (`R=150`, trois répétitions, puis
`R=127`, une répétition). Aucun résultat incomplet n'a été conservé. Le script
filtré a ensuite produit le benchmark borné rapporté ci-dessus.
