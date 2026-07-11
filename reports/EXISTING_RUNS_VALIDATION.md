# Validation des recherches existantes

Validation en lecture seule du 11 juillet 2026, sans grand calcul.

Les manifests, `C(R,3)`, tailles, shards, résultats de recherche, résumés et CSV concordent pour : carrés R52/R127; cubes R750/R1000/R1500/R2000; puissances quatrièmes R250/R500/R750/R1000/R1500. Tous ont leurs shards terminés; les carrés ont respectivement 1 et 48 solutions, les autres zéro.

Le résumé et le CSV cubes R500 annoncent 20 708 500 records, 256/256 shards et zéro solution, mais `work/cubes_R500` est absent : validation documentaire seulement.

Les essais prototype cubes R100/R150/R200 et quatrième puissance R80 n'ont pas les marqueurs V2 et ne sont pas comptés comme validations V2. `STATUS.md` mentionne encore R2000 comme palier possible alors qu'il est achevé.
