# Rapport power 3 — R = 2500

Recherche exhaustive complète et validée le 15 juillet 2026. Les racines sont
les entiers positifs de 1 à 2500 et les neuf racines doivent être globalement
distinctes. Les entrées sont leurs cubes ; les trois lignes et les trois
colonnes doivent partager une somme commune. Les diagonales ne sont pas
imposées.

## Résultat

Aucun carré semi-magique 3×3 de neuf cubes positifs globalement distincts n'a
été trouvé dans ce domaine.

## Statistiques exactes

- Shards : 256/256
- Triples attendus et observés : 2 601 042 500
- Records binaires : 41 616 680 000 octets
- Taille d'un record : 16 octets
- Sommes distinctes : 2 245 424 704
- Groupes avec au moins deux triples : 291 045 440
- Groupes avec au moins trois triples : 50 417 211
- Taille maximale d'un groupe : 21
- Paires de triples : 198 764 432
- Paires disjointes : 192 263 004
- Alignements testés : 1 153 578 024
- Troisièmes lignes entièrement cubiques : 0
- Troisièmes triples indexés : 0
- Solutions canoniques uniques : 0
- Temps cumulé de recherche des shards : 4 657,6458134 s
- Temps mural entre création du work-dir et résumé final : 1 661,74 s

## Exécution

La génération des 2 601 042 500 triples et les 31 premiers shards de recherche
ont utilisé le moteur V2 séquentiel. Le moteur produit un résultat JSON atomique
par shard, ce qui permet une reprise sans recalcul des shards achevés.

Les 225 shards manquants ont ensuite été traités avec huit workers indépendants
par `src/search_semimagic_shards_parallel.py`. Cet orchestrateur réutilise sans
modification la fonction exacte `search_one_shard`. Après les 256 résultats,
l'agrégation V2 a produit le CSV nul et le résumé JSON final.

## Validation

La validation indépendante du work-dir confirme :

```text
records          = 2 601 042 500
expected_records = 2 601 042 500
disk_bytes       = 41 616 680 000
record_itemsize  = 16
errors           = []
```

Les 22 tests unitaires passent après le run.

## Artefacts

- `work/cubes_R2500`
- `results/cubes/semimagic_3x3_cubes_R2500.csv`
- `logs/semimagic_3x3_cubes_R2500_summary.json`
- `logs/semimagic_3x3_cubes_R2500_run.stdout.log`
- `logs/semimagic_3x3_cubes_R2500_parallel.stdout.log`
- `scripts/run_cubes_R2500.ps1`
- `scripts/resume_cubes_R2500_parallel.ps1`

## Reproduction et validation

```powershell
./scripts/run_cubes_R2500.ps1
python src/search_semimagic_3x3_powers_v2_disk.py --power 3 --max-root 2500 `
  --shards 256 --work-dir work/cubes_R2500 --phase validate
python -m unittest discover -s tests -v
```