# Rapport power 3 — R = 2250

Recherche exhaustive complète et validée le 14 juillet 2026. Les racines sont
les entiers positifs de 1 à 2250, les neuf racines sont distinctes et chaque
entrée est leur cube. Les lignes et colonnes ont une somme commune ; les
diagonales ne sont pas imposées.

## Résultats

- Shards : 256/256
- Triples attendus et observés : 1 895 907 000
- Records sur disque : 30 334 512 000 octets
- Sommes distinctes : 1 636 956 745
- Groupes avec au moins deux triples : 212 018 959
- Groupes avec au moins trois triples : 36 679 400
- Taille maximale d'un groupe : 20
- Paires testées : 144 415 564
- Paires disjointes : 139 400 318
- Alignements : 836 401 908
- Troisièmes lignes entièrement cubiques : 0
- Solutions canoniques uniques : 0
- Temps de recherche : 2 445,4517467 s
- Temps total : 2 641,13 s

Le moteur exact V2 sur disque a exécuté un run intégral, le stockage V2 R=2000
n'étant pas importé automatiquement par V3. La validation indépendante confirme
le nombre exact de records, les 256 shards et l'absence d'erreur de format. Le
CSV final ne contient que son en-tête, conformément au résultat nul.

## Reproduction et validation

```powershell
./scripts/run_cubes_R2250.ps1
python src/search_semimagic_3x3_powers_v2_disk.py --power 3 --max-root 2250 `
  --shards 256 --work-dir work/cubes_R2250 --phase validate
```
