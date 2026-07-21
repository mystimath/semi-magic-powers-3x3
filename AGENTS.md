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
## Amélioration des moteurs

À chaque moteur plus performant découvert ou validé :

1. le comparer à un oracle exact sur une borne commune ;
2. consigner le gain, le domaine exact et les limites dans `ARCHITECTURE.md` et
   `RUNS.md` ;
3. le déclarer chemin recommandé dans `README.md` et `STATUS.md` avant toute
   nouvelle campagne de même cible ;
4. conserver l'ancien moteur comme oracle ou contrôle de régression, sans le
   relancer à grande borne si le moteur spécialisé est exact.
