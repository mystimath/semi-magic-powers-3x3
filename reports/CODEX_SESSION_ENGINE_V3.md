# Session ENGINE V3

Mission reprise et achevée le 11 juillet 2026 après la panne électrique.

V3 a été ajouté séparément de V2. Il génère uniquement les triples dont `R_old < c <= R_new`, utilise un sharding stable, fusionne atomiquement, recherche seulement les sommes affectées et conserve l'historique et le registre canonique des solutions.

Validations : 21 tests passent; équivalence direct/incrémental pour puissances 2, 3 et 4; interruption et reprise; shard incomplet; benchmark R35; contrôle scientifique R52 avec 22 100 triples et la solution connue unique.

Rapports : `ENGINE_V3_AUDIT.md`, `EXISTING_RUNS_VALIDATION.md`, `ENGINE_V3_BENCHMARK.md`. Marqueur : `.codex-state/ENGINE_V3_READY.json`.

Aucune grande recherche n'a été lancée. Limites : records V3 de 20 octets, pas de conversion automatique des grands work-dirs V2, limite temporelle vérifiée entre fusions.