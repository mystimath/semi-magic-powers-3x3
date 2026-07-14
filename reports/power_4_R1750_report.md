# Rapport power 4 — R = 1750

Recherche exhaustive complète et validée le 14 juillet 2026. Les racines sont
les entiers positifs de 1 à 1750, les neuf racines sont distinctes et chaque
entrée est leur puissance quatrième. Les lignes et colonnes ont une somme
commune ; les diagonales ne sont pas imposées.

## Résultats

- Shards : 256/256
- Triples attendus et observés : 891 698 500
- Records sur disque : 14 267 176 000 octets
- Sommes distinctes : 890 290 058
- Groupes avec au moins deux triples : 1 305 665
- Groupes avec au moins trois triples : 52 643
- Taille maximale d'un groupe : 16
- Paires testées : 337 369
- Paires disjointes : 336 942
- Alignements : 2 021 652
- Troisièmes lignes entièrement puissances quatrièmes : 0
- Solutions canoniques uniques : 0
- Temps total : 788,38 s

Le moteur exact V2 sur disque a exécuté un run intégral, le stockage V2 R=1500
n'étant pas importé automatiquement par V3. La validation indépendante confirme
le nombre exact de records et l'absence d'erreur de format.

## Reproduction et validation

```powershell
./scripts/run_fourth_R1750.ps1
python src/search_semimagic_3x3_powers_v2_disk.py --power 4 --max-root 1750 `
  --shards 256 --work-dir work/fourth_R1750 --phase validate
```
