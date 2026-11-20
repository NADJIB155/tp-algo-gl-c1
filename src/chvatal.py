"""
chvatal.py — Heuristique gourmande de Chvátal pour Set Cover (variante GL-C1).

RÈGLE (en une phrase) :
    À chaque étape, choisir le test qui apporte le PLUS de nouvelles exigences
    (gain = |nouvelles exigences couvertes|). En cas d'égalité, prendre le
    test de moindre coût, puis le nom le plus petit (départage déterministe).

COÛTS :
    Si l'instance n'a pas de champ "costs", tous les tests coûtent 1
    (cas GL-C1). L'extension vers C2 (coûts non unitaires) est gratuite :
    il suffit de passer un dict {nom_test: coût} en argument.

GARANTIE THÉORIQUE :
    taille(solution_Chvátal) ≤ (1 + ln|U|) × OPT
    Pour |U| = 5 : 1 + ln(5) ≈ 2,61
    Pour |U| = 10 : 1 + ln(10) ≈ 3,30
"""

def chvatal(exigences, tests, couts=None):
    """Calcule une solution approchée par l'heuristique de Chvátal.

    Paramètres :
        exigences : liste des exigences (ex. ["e1", "e2", ...])
        tests     : dict {nom_test: liste_exigences_couvertes}
        couts     : dict {nom_test: coût} ou None (coûts unitaires par défaut)

    Renvoie : (selection, taille, trace)
        - selection : liste des noms de tests choisis (dans l'ordre)
        - taille    : nombre de tests sélectionnés
        - trace     : liste de dicts décrivant chaque étape
                      (utile pour debug et pour les slides)
    """
    U = set(exigences)

    # Coûts par défaut : tous à 1 (variante GL-C1)
    if couts is None:
        couts = {t: 1 for t in tests}

    couvert = set()       # exigences déjà couvertes
    selection = []        # tests choisis (dans l'ordre)
    trace = []            # journal des étapes

    # Boucle principale : tant qu'on n'a pas couvert tout U
    while couvert != U:
        restant = U - couvert   # exigences encore à couvrir

        # Évaluer chaque test : gain = nouvelles exigences couvertes
        candidats = []
        for nom in sorted(tests.keys()):   # tri pour départage déterministe
            couverts_par_ce_test = set(tests[nom])
            gain = len(couverts_par_ce_test & restant)   # "nouvelles" exigences
            if gain == 0:
                continue   # ce test n'apporte rien -> on l'ignore
            ratio = gain / couts[nom]
            candidats.append({
                "nom": nom,
                "gain": gain,
                "cout": couts[nom],
                "ratio": ratio,
            })

        # Cas pathologique : aucun test ne peut progresser -> instance infaisable
        if not candidats:
            raise ValueError("Instance infaisable : exigences non couvrables")

        # Départage DÉTERMINISTE :
        #   1) ratio plus grand (gain/coût)
        #   2) gain plus grand
        #   3) coût plus petit
        #   4) nom plus petit (ordre alphabétique)
        candidats.sort(key=lambda c: (-c["ratio"], -c["gain"], c["cout"], c["nom"]))
        meilleur = candidats[0]
        nom_choisi = meilleur["nom"]

        # Appliquer le choix
        selection.append(nom_choisi)
        nouvelement_couverts = set(tests[nom_choisi]) & restant
        couvert |= set(tests[nom_choisi])

        # Enregistrer l'étape pour la trace
        trace.append({
            "etape": len(selection),
            "restant_avant": sorted(restant),
            "choix": nom_choisi,
            "gain": meilleur["gain"],
            "ratio": round(meilleur["ratio"], 3),
            "nouveaux": sorted(nouvelement_couverts),
            "restant_apres": sorted(U - couvert),
        })

    return selection, len(selection), trace
