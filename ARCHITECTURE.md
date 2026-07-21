# Architecture — Semi-magic Powers 3×3

```text
racines et puissances → triples indexés par somme → shards de recherche
        → déduction de grille → canonicalisation → CSV / JSON / validation
```

- `src/search_semimagic_3x3_powers.py` est le prototype en mémoire.
- V2 organise la recherche exacte par shards sur disque ;
  `semimagic_disk_backend.py` fournit génération, agrégation et validation.
- V3 ajoute la reprise incrémentale et le bornage d'exécution.
- `work/` est temporaire et reprenable ; `results/` contient les sorties
  contrôlées ; `RUNS.md` porte les commandes et chiffres de campagne.

`STATUS.md` résume les bornes atteintes et les priorités ; ne pas y recopier les
journaux d'exécution.
## Choix du moteur par objectif

| Cible | Moteur de référence | Rôle de l’autre moteur |
|---|---|---|
| Toutes les classes semi-magiques (6 lignes) | V2/V3 sur disque | campagne exhaustive générale |
| Classes ayant une transversale magique (7 lignes) | `lo_shu_search.py` / `scripts/export_lo_shu_catalog.py` | V2 reste l’oracle borné de comparaison |

Le moteur Lo Shu regroupe les progressions de trois carrés par raison commune.
Il est exact pour les classes à transversale magique : une telle transversale se
ramène à une diagonale par permutation de colonnes. La régression R=500 donne
exactement les quatre classes du catalogue, en environ 0,013 s, contre des
milliards d’alignements pour le parcours V2. Toute extension de cette cible doit
employer ce moteur ; une optimisation future doit suivre le protocole
`AGENTS.md`.
