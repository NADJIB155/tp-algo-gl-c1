"""
main.py — Point d'entrée : charge une instance, lance Chvátal puis B&B.

Usage :
    python main.py instances/small_instance.json
    python main.py instances/medium_instance.json

    (sans argument : utilise instances/small_instance.json par défaut)
"""

import sys
import os
import math

# Pour que les "import parser" etc. fonctionnent quel que soit le dossier
# depuis lequel on lance le script.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from parser import charger_instance, afficher_instance
from chvatal import chvatal
from branch_and_bound import branch_and_bound, exporter_graphviz


def main():
    # ── 1. Trouver l'instance à charger ──
    if len(sys.argv) < 2:
        # Par défaut : ../instances/small_instance.json (relativement à src/)
        chemin = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "instances", "small_instance.json")
        )
        print(f"[i] Aucun argument fourni : utilisation de {chemin}")
    else:
        chemin = sys.argv[1]

    inst = charger_instance(chemin)
    afficher_instance(inst)
    print()

    exigences = inst["requirements"]
    tests = inst["tests"]

    # ── 2. Heuristique de Chvátal ──
    print("=" * 60)
    print(" Heuristique de Chvátal")
    print("=" * 60)
    sel_chv, taille_chv, trace = chvatal(exigences, tests)
    for etape in trace:
        print(f"  Étape {etape['etape']} : restant {etape['restant_avant']}")
        print(f"      -> prendre {etape['choix']} "
              f"(gain={etape['gain']}, ratio={etape['ratio']})")
        print(f"      nouveaux : {etape['nouveaux']} -> reste {etape['restant_apres']}")
    print(f"  => Solution Chvátal : {sel_chv} (taille = {taille_chv})")
    print()

    # ── 3. B&B en mode RAPIDE (warm-start avec la solution Chvátal) ──
    print("=" * 60)
    print(" B&B exact — mode RAPIDE (warm-start : UB = taille Chvátal)")
    print("=" * 60)
    sel_bb, taille_bb, metriques, _ = branch_and_bound(
        exigences, tests, ub_init=taille_chv, generer_arbre=False,
        solution_initiale=sel_chv,
    )
    print(f"  => Solution B&B : {sel_bb} (taille = {taille_bb})")
    print(f"  Métriques :")
    for k, v in metriques.items():
        print(f"    {k:<22} : {v}")
    print()

    # ── 4. B&B en mode PÉDAGOGIQUE (UB = ∞) + arbre Graphviz ──
    #    Uniquement si l'instance est petite (≤ 8 exigences).
    if len(exigences) <= 8:
        print("=" * 60)
        print(" B&B — mode PÉDAGOGIQUE (UB = ∞) + export Graphviz")
        print("=" * 60)
        sel_bb2, taille_bb2, metriques2, arbre = branch_and_bound(
            exigences, tests, ub_init=None, generer_arbre=True
        )
        print(f"  => Solution B&B : {sel_bb2} (taille = {taille_bb2})")
        print(f"  Métriques :")
        for k, v in metriques2.items():
            print(f"    {k:<22} : {v}")
        if arbre is not None:
            chemin_dot = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "..", "arbre_bb.dot")
            )
            exporter_graphviz(arbre, chemin_dot)
            print(f"  Pour rendre l'arbre en image (optionnel) :")
            print(f"    dot -Tpng {chemin_dot} -o arbre_bb.png")
        print()

    # ── 5. Résumé comparatif ──
    print("=" * 60)
    print(" Résumé")
    print("=" * 60)
    print(f"  Chvátal : taille = {taille_chv}")
    print(f"  B&B     : taille = {taille_bb}  (OPTIMUM prouvé)")
    if taille_bb > 0:
        ratio = taille_chv / taille_bb
        garantie = math.log(len(exigences)) + 1
        print(f"  Ratio mesuré Chvátal/OPT = {ratio:.2f}")
        print(f"  Garantie théorique ln(|U|)+1 = ln({len(exigences)})+1 ≈ {garantie:.2f}")


if __name__ == "__main__":
    main()
