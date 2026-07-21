# Carrés semi-magiques 3×3 de puissances

Recherche expérimentale exacte de carrés semi-magiques 3×3 dont les neuf
entrées sont des carrés (`k = 2`), des cubes (`k = 3`) ou des puissances
quatrièmes (`k = 4`).

Une grille est semi-magique lorsque ses trois lignes et ses trois colonnes ont
la même somme. Les diagonales ne sont pas imposées. Les recherches V2 utilisent
des racines strictement positives et globalement distinctes.

## Moteurs

- `src/search_semimagic_3x3_powers.py` : prototype en mémoire ;
- `src/search_semimagic_3x3_powers_v2_disk.py` : moteur exact sur disque,
  partitionné en shards et reprenable ;
- `src/semimagic_disk_backend.py` : génération, recherche, agrégation et
  validation du format sur disque.

Le moteur V2 accepte `--power 2`, `--power 3` et `--power 4`. Un répertoire de travail déjà
muni d'un manifeste compatible est repris sans `--overwrite`. Les résultats de
chaque shard sont conservés dans `work/.../search`, ce qui permet de ne retraiter
que les shards manquants.

## Recherche spécialisée : transversale magique

Pour les carrés semi-magiques de carrés ayant une transversale de somme magique
(septième alignement), utiliser le moteur Lo Shu plutôt que V2 : il est exact
sur cette sous-famille et évite le balayage des paires de triples.

```powershell
python scripts/export_lo_shu_catalog.py --max-root 5000 `
  --json-out reports/lo_shu/direct_catalog_R5000_YYYYMMDD.json
```

Le moteur général V2 reste l’oracle de comparaison aux petites bornes ; ne pas
l’employer pour étendre cette sous-famille après validation de l’équivalence.
## Extension incrémentale V3

```powershell
python src/search_semimagic_3x3_powers_v3.py --power 3 --max-root 100 `
  --shards 64 --work-dir work/v3_cubes --checkpoint-every 1
python src/search_semimagic_3x3_powers_v3.py --power 3 --max-root 150 `
  --shards 64 --work-dir work/v3_cubes --resume --max-shards-this-run 16
```

Une reprise conserve la puissance, le nombre de shards, le work-dir et la borne
cible. `--time-limit-minutes` borne les fusions; `--validate` contrôle le layout.

## Installation et tests

Python 3.10 ou supérieur et NumPy sont requis.

```powershell
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
```

## Exemple V2

```powershell
python src/search_semimagic_3x3_powers_v2_disk.py `
  --power 4 `
  --max-root 250 `
  --shards 256 `
  --work-dir work/fourth_R250 `
  --phase all `
  --progress-a 10 `
  --progress-shards 1 `
  --out results/fourth-powers/semimagic_3x3_fourth_R250.csv `
  --summary-json logs/semimagic_3x3_fourth_R250_summary.json
```

Ne jamais supprimer le répertoire de travail d'un run scientifique. En cas
d'interruption, relancer la même commande sans `--overwrite`.

## Validation

```powershell
python src/search_semimagic_3x3_powers_v2_disk.py `
  --power 4 `
  --max-root 250 `
  --shards 256 `
  --work-dir work/fourth_R250 `
  --phase validate
```

La méthodologie est détaillée dans `METHODOLOGY.md`, l'état courant dans
`STATUS.md` et les exécutions scientifiques dans `RUNS.md`.

## Cas de référence : Sallows

Le run `scripts/run_squares_R127.ps1` sert de contrôle positif du moteur. Il
retrouve le carré semi-magique de carrés de Lee Sallows parmi 48 classes
canoniques à `R = 127`. Les six sommes de lignes et colonnes valent `21 609`.

Le run indépendant `scripts/run_squares_R52.ps1` trouve une autre classe,
unique à cette borne et de racine maximale minimale parmi les solutions du run
R127. Sa somme commune vaut `3 249 = 57²`.
