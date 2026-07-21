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
