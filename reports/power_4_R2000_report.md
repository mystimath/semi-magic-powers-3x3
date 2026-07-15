# Rapport power 4 — R = 2000

Recherche exhaustive complète et validée le 15 juillet 2026. Les racines sont
les entiers positifs de 1 à 2000 et les neuf racines doivent être globalement
distinctes. Les entrées sont leurs puissances quatrièmes ; les trois lignes et
les trois colonnes doivent partager une somme commune. Les diagonales ne sont
pas imposées.

## Résultat

Aucun carré semi-magique 3×3 de neuf puissances quatrièmes positives et
globalement distinctes n'a été trouvé dans ce domaine.

## Statistiques exactes

- Shards : 256/256
- Triples attendus et observés : 1 331 334 000
- Records binaires : 21 301 344 000 octets
- Taille d'un record : 16 octets
- Sommes distinctes : 1 329 459 288
- Groupes avec au moins deux triples : 1 736 045
- Groupes avec au moins trois triples : 69 930
- Taille maximale d'un groupe : 16
- Paires de triples : 457 852
- Paires disjointes : 457 323
- Alignements testés : 2 743 938
- Troisièmes lignes entièrement constituées de puissances quatrièmes : 0
- Troisièmes triples indexés : 0
- Solutions canoniques uniques : 0
- Temps cumulé de recherche des shards : 990,3160145 s
- Temps mural entre création du work-dir et résumé final : 1 140,57 s

## Exécution

Le moteur V2 séquentiel a généré les 1 331 334 000 triples, traité les 256
shards et produit l'agrégation finale sans interruption. Un script de reprise
parallèle avec huit workers a également été préparé, mais n'a pas été nécessaire
pour ce run.

## Validation

La validation indépendante du work-dir confirme :

```text
records          = 1 331 334 000
expected_records = 1 331 334 000
disk_bytes       = 21 301 344 000
record_itemsize  = 16
errors           = []
```

Les 22 tests unitaires passent après le run.

## Artefacts

- `work/fourth_R2000`
- `results/fourth-powers/semimagic_3x3_fourth_R2000.csv`
- `logs/semimagic_3x3_fourth_R2000_summary.json`
- `logs/semimagic_3x3_fourth_R2000_run.stdout.log`
- `scripts/run_fourth_R2000.ps1`
- `scripts/resume_fourth_R2000_parallel.ps1`

## Reproduction et validation

```powershell
./scripts/run_fourth_R2000.ps1
python src/search_semimagic_3x3_powers_v2_disk.py --power 4 --max-root 2000 `
  --shards 256 --work-dir work/fourth_R2000 --phase validate
python -m unittest discover -s tests -v
```