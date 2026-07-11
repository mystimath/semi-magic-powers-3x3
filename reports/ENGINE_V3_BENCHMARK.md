# Benchmark ENGINE V3

Puissance 3, R35, 16 shards; temps incluant le démarrage Python.

| Scénario | Temps | Taille |
|---|---:|---:|
| V2 direct R35 | 0,495 s | 85 652 octets |
| V3 initial R20 | 0,507 s | — |
| V3 extension R20→R35 | 0,575 s | 239 572 octets total |
| V3 direct R35 | 0,572 s | 262 207 octets |

V3 évite de régénérer les anciens triples mais paie son format fixe et son journal détaillé. La mémoire maximale n'a pas été mesurée fiablement sous Windows.
