# Audit du moteur V3

Audit effectué le 11 juillet 2026.

## Moteurs et formats

Le prototype mémoire ne reprend pas une interruption. V2 reprend génération et recherche, mais son encodage et ses intervalles de shards dépendent de `max_root` : ses records `(sum:u64, code:u32|u64)` font 12 ou 16 octets et ne sont pas directement extensibles.

V3 reste séparé afin de préserver V2. Il génère seulement `R_old < c <= R_new`, stocke `(sum:u64,a:u32,b:u32,c:u32)` sur 20 octets et choisit `sum mod shard_count`, placement stable entre bornes. Chaque shard est trié par `(sum,a,b,c)`.

## Reprise et recherche

Le manifeste conserve l'extension en attente, `next_c`, tailles de staging, tailles avant fusion, shards fusionnés, sommes affectées et historique. Une reprise tronque le staging au checkpoint. Les remplacements sont atomiques et leurs tailles permettent de reconnaître un remplacement achevé avant la mise à jour du manifeste.

Pour chaque somme affectée, V3 relit le groupe complet ancien et nouveau, ignore les sommes strictement anciennes, déduplique par forme canonique et fusionne avec les solutions connues.

## Limites

Le format V3 est plus volumineux. La limite de temps est appliquée entre fusions; la génération se reprend par `c`. Aucun artefact V2 massif n'est converti automatiquement.
