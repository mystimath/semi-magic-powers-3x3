# Consignes locales — Semi-magic Powers 3×3

Lire `README.md`, `STATUS.md` et `RUNS.md` avant d'agir. Ce dépôt exécute des
recherches exactes potentiellement lourdes et reprenables.

- Les moteurs actifs sont `src/search_semimagic_3x3_powers_v2_disk.py` et V3 ;
  le prototype mémoire ne sert pas de référence de campagne.
- Ne lancer un grand run qu'avec une borne, un `work-dir`, une stratégie de
  reprise et un contrôle de capacité explicites.
- Préserver les workdirs et résultats existants ; ne pas utiliser `--overwrite`
  sans autorisation explicite.
- Valider tout changement avec les tests ciblés et le validateur du work-dir.
- Les logs de session et l'état d'outil sont locaux : ils ne doivent pas devenir
  des artefacts scientifiques suivis par Git.
