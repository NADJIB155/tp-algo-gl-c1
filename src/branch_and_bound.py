"""
branch_and_bound.py — Algorithme exact Branch & Bound pour Set Cover (GL-C1).

IDÉE EN UNE PHRASE :
    On dessine l'arbre de toutes les décisions "quel test choisir pour couvrir
    l'exigence la plus rare" et on l'explore, en coupant les branches dont on
    peut prouver qu'elles ne battront jamais le record courant.

DEUX GARDE-FOUS :

  UB (Upper Bound, le "record à battre") :
      taille de la meilleure solution connue.
      - Si ub_init est un entier (ex. taille Chvátal) : WARM-START.
        Le B&B démarre avec un bon record et élague tout de suite.
      - Si ub_init = None ou float('inf') : MODE PÉDAGOGIQUE.
        On développe l'arbre entièrement (utile pour dessiner l'arbre).

  LB (Lower Bound, la "promesse minimale" d'un nœud) :
      Pour un nœud avec |reste| exigences à couvrir et max_gain = gain
      maximum parmi les tests disponibles, il faut AU MOINS
            LB = ⌈|reste| / max_gain⌉
      tests supplémentaires. Si une exigence n'est couverte par aucun test
      disponible, LB = +∞ (branche infaisable).

TROIS RAISONS DE COUPER UNE BRANCHE :
   1. LB infaisable : une exigence n'est couverte par aucun test dispo.
   2. LB ≥ UB       : la branche ne peut pas strictement battre le record.
   3. UB            : solution complète trouvée mais pas meilleure que le
                      record courant (elle est ignorée).

BRANCHEMENT :
   À chaque nœud, on choisit l'exigence non couverte la PLUS RARE
   (couverte par le moins de tests disponibles). Analogie Sudoku : si une
   case ne peut contenir qu'un seul chiffre, on le joue d'abord.
   Un enfant par test qui couvre cette exigence rare.
"""

import time



#  Fonctions auxiliaires (hors de la récursion principale)

def _rarete(restant, tests_disponibles, tests):
    """Compte, pour chaque exigence restante, combien de tests disponibles
    la couvrent. Renvoie (exigence_la_plus_rare, nombre_de_tests).

    Si une exigence n'est couverte par AUCUN test disponible -> (e, 0),
    c'est le signal d'infaisabilité.
    """
    meilleure = None
    min_compte = None
    for e in restant:
        compte = sum(1 for t in tests_disponibles if e in tests[t])
        if compte == 0:
            return e, 0        # infaisabilité détectée
        if min_compte is None or compte < min_compte:
            min_compte = compte
            meilleure = e
    return meilleure, min_compte


def _borne_inferieure(restant, tests_disponibles, tests):
    """Calcule LB = ⌈|reste| / max_gain⌉.
    Renvoie float('inf') si l'exigence est infaisable."""
    if not restant:
        return 0
    rare, compte = _rarete(restant, tests_disponibles, tests)
    if compte == 0:
        return float('inf')
    # Gain maximum parmi les tests disponibles
    restant_set = set(restant)
    max_gain = max(len(tests[t] & restant_set) for t in tests_disponibles)
    if max_gain == 0:
        return float('inf')
    # ⌈a/b⌉ = (a + b - 1) // b  en arithmétique entière
    return (len(restant) + max_gain - 1) // max_gain


#  Algorithme principal


def branch_and_bound(exigences, tests, ub_init=None, generer_arbre=False,
                     solution_initiale=None):
    """Résout Set Cover exactement par Branch & Bound.

    Paramètres :
        exigences          : liste d'exigences
        tests              : dict {nom_test: liste_exigences}
        ub_init            : borne supérieure initiale.
                            - None ou float('inf') : mode pédagogique.
                            - un entier (ex. taille Chvátal) : warm-start.
        generer_arbre      : si True, enregistre l'arbre pour export Graphviz
                            (uniquement si ≤ 8 exigences et ≤ 60 nœuds).
        solution_initiale  : liste de tests à utiliser comme solution de
                            départ (typiquement la solution Chvátal en
                            warm-start). Si le B&B ne trouve rien de mieux,
                            il renvoie cette solution.

    Renvoie :
        (selection, taille, metriques, arbre)
        - selection : liste des tests de la solution optimale
        - taille    : nombre de tests
        - metriques : dict avec noeuds, elagages_lb, elagages_ub,
                      elagages_infaisable, profondeur_max, temps
        - arbre     : liste de dicts (id, parent, decision, label, type)
                      ou None si generer_arbre=False
    """
    U = set(exigences)
    # Conversion des listes en sets (recherche plus rapide)
    tests = {t: set(tests[t]) for t in tests}

    if ub_init is None:
        ub_init = float('inf')

    # Solution de départ (en warm-start, c'est la solution Chvátal).
    # Si le B&B ne trouve rien de mieux, il renvoie cette solution.
    if solution_initiale is None:
        solution_initiale = []

    # État global partagé pendant la récursion (mutable pour éviter "nonlocal")
    etat = {
        "meilleure_selection": list(solution_initiale),
        "meilleure_taille": ub_init,
        "noeuds": 0,
        "elagages_lb": 0,
        "elagages_ub": 0,
        "elagages_infaisable": 0,
        "profondeur_max": 0,
    }

    # Limite de sécurité pour l'arbre Graphviz (règle de votre code V3)
    arbre = [] if generer_arbre else None
    compteur_noeud = [0]
    limite_atteinte = [False]
    MAX_NOEUDS_ARBRE = 60

    if generer_arbre and len(U) > 8:
        print(f"[!] Arbre désactivé : {len(U)} exigences (> 8).")
        generer_arbre = False
        arbre = None

    
    #  Fonction récursive : explore un nœud de l'arbre
    
    def explorer(selection, couvert, profondeur, id_parent=None, decision=""):
        etat["noeuds"] += 1
        etat["profondeur_max"] = max(etat["profondeur_max"], profondeur)

        restant = U - couvert
        type_noeud = "explore"

        # ── Cas 1 : solution complète (tout est couvert) ──
        if not restant:
            if len(selection) < etat["meilleure_taille"]:
                # Nouveau record ! On garde cette solution
                etat["meilleure_selection"] = list(selection)
                etat["meilleure_taille"] = len(selection)
            else:
                # Solution trouvée mais pas meilleure que le record
                etat["elagages_ub"] += 1
            type_noeud = "solution"

        else:
            # ── Calcul des tests disponibles (encore utiles) ──
            disponibles = [t for t in tests
                           if t not in selection and (tests[t] & restant)]
            if not disponibles:
                # Aucun test ne peut couvrir les exigences restantes
                etat["elagages_infaisable"] += 1
                type_noeud = "prune"
            else:
                # ── Borne inférieure LB ──
                lb = _borne_inferieure(restant, disponibles, tests)
                if lb == float('inf'):
                    etat["elagages_infaisable"] += 1
                    type_noeud = "prune"
                elif len(selection) + lb >= etat["meilleure_taille"]:
                    # La branche ne peut pas strictement battre le record
                    etat["elagages_lb"] += 1
                    type_noeud = "prune"

        # ── Enregistrement du nœud dans l'arbre 
        id_noeud = None
        if generer_arbre and not limite_atteinte[0]:
            compteur_noeud[0] += 1
            id_noeud = f"n{compteur_noeud[0]}"
            if compteur_noeud[0] >= MAX_NOEUDS_ARBRE:
                limite_atteinte[0] = True
                print(f"[!] Limite de {MAX_NOEUDS_ARBRE} nœuds atteinte, "
                      f"arrêt de l'enregistrement de l'arbre.")

            # Construction du label affiché dans Graphviz
            if not restant:
                lbl = (f"Choisi: {{{', '.join(selection)}}}\\n"
                       f"Taille={len(selection)}\\nSOLUTION")
            else:
                lbl = (f"Choisi: {{{', '.join(selection) or '∅'}}}\\n"
                       f"Reste: {{{', '.join(sorted(restant))}}}")
                if type_noeud == "prune":
                    lbl += "\\n[COUPE]"

            arbre.append({
                "id": id_noeud,
                "parent": id_parent,
                "decision": decision,
                "label": lbl,
                "type": type_noeud,
            })

        # ── Si le nœud est exploré (non coupé), on descend ──
        if type_noeud == "explore":
            # Branchement sur l'exigence la plus rare
            rare, _ = _rarete(restant, disponibles, tests)
            tests_pour_rare = sorted(t for t in disponibles if rare in tests[t])
            for t in tests_pour_rare:
                explorer(selection + [t],
                         couvert | tests[t],
                         profondeur + 1,
                         id_parent=id_noeud,
                         decision=f"e={rare}\\nprendre {t}")

    # ── Lancement de la recherche ──
    debut = time.time()
    explorer([], set(), 0)
    duree = time.time() - debut

    metriques = {
        "noeuds": etat["noeuds"],
        "elagages_lb": etat["elagages_lb"],
        "elagages_ub": etat["elagages_ub"],
        "elagages_infaisable": etat["elagages_infaisable"],
        "profondeur_max": etat["profondeur_max"],
        "temps_s": round(duree, 4),
    }

    return (list(etat["meilleure_selection"]),
            etat["meilleure_taille"],
            metriques,
            arbre)



#  Export Graphviz (.dot)

def exporter_graphviz(arbre, chemin):
    """Exporte l'arbre de recherche au format DOT (Graphviz).

    Pour générer une image PNG à partir du .dot :
        dot -Tpng arbre_bb.dot -o arbre_bb.png

    (Graphviz doit être installé : sudo apt install graphviz)
    """
    if arbre is None or len(arbre) == 0:
        print("[!] Arbre vide, rien à exporter.")
        return

    # Couleurs par type de nœud (faible saturation, liseré coloré)
    couleurs = {
        "explore":   ("#DBEAFE", "#4C6EF5"),   # bleu clair / bord bleu
        "solution":  ("#D1FAE5", "#10B981"),   # vert clair  / bord vert
        "prune":     ("#FEF3C7", "#EF4444"),   # ambre clair / bord rouge
    }

    lignes = [
        "digraph BB {",
        "  rankdir=TB;",                       # top -> bottom
        '  node [shape=box, style="filled,rounded", fontname="Helvetica"];',
        '  edge [fontname="Helvetica", fontsize=10];',
    ]

    # Nœuds
    for n in arbre:
        fond, bord = couleurs.get(n["type"], couleurs["explore"])
        label = n["label"].replace('"', '\\"')
        lignes.append(
            f'  "{n["id"]}" [label="{label}", fillcolor="{fond}", color="{bord}"];'
        )

    # Arêtes
    for n in arbre:
        if n["parent"] is not None:
            decision = n["decision"].replace('"', '\\"')
            lignes.append(
                f'  "{n["parent"]}" -> "{n["id"]}" [label="{decision}"];'
            )

    lignes.append("}")

    with open(chemin, "w", encoding="utf-8") as f:
        f.write("\n".join(lignes))
    print(f"[+] Arbre exporté : {chemin} ({len(arbre)} nœuds)")
