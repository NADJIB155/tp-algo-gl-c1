"""
parser.py — Charge les instances JSON créées par Binôme 1.

Ce module est la SEULE porte d'entrée vers les données du problème.
Il lit le format défini dans /instances du repo GitHub :

  {
    "name": "Petite Instance Démo GL-C1",
    "num_requirements": 5,
    "requirements": ["e1", "e2", "e3", "e4", "e5"],
    "tests": {
      "T1": ["e1", "e2", "e3"],
      "T2": ["e2", "e4"],
      "T3": ["e3", "e4", "e5"],
      "T4": ["e4", "e5"]
    }
  }

Usage :
    from parser import charger_instance
    inst = charger_instance("instances/small_instance.json")
    exigences = inst["requirements"]   # liste d'exigences
    tests = inst["tests"]              # dict {nom_test: liste_exigences}
"""

import json


def charger_instance(chemin):
    """Charge un fichier d'instance JSON et vérifie sa cohérence.

    Vérifications effectuées :
      - toutes les clés obligatoires sont présentes ;
      - num_requirements correspond bien à len(requirements) ;
      - aucun test n'est vide ;
      - tous les éléments couverts par les tests existent dans requirements.

    Renvoie le dictionnaire tel quel (avec clés name, num_requirements,
    requirements, tests).
    """
    with open(chemin, encoding="utf-8") as f:
        data = json.load(f)

    # 1) Toutes les clés obligatoires doivent être présentes
    cles_obligatoires = ("name", "num_requirements", "requirements", "tests")
    for cle in cles_obligatoires:
        if cle not in data:
            raise ValueError(f"Clé manquante dans {chemin} : '{cle}'")

    # 2) Cohérence entre num_requirements et la liste réelle
    if data["num_requirements"] != len(data["requirements"]):
        raise ValueError(
            f"num_requirements ({data['num_requirements']}) ne correspond pas "
            f"à len(requirements) ({len(data['requirements'])}) dans {chemin}"
        )

    # 3) Aucun test vide + tous les éléments couverts existent dans U
    univers = set(data["requirements"])
    for nom_test, couverts in data["tests"].items():
        if len(couverts) == 0:
            raise ValueError(f"Test '{nom_test}' vide (couvre 0 exigence) dans {chemin}")
        for e in couverts:
            if e not in univers:
                raise ValueError(
                    f"Test '{nom_test}' couvre '{e}' qui n'est pas dans l'univers "
                    f"de {chemin}"
                )

    return data


def afficher_instance(inst):
    """Affiche un résumé lisible d'une instance (pour debug / demo)."""
    print(f"Instance : {inst['name']}")
    print(f"  Exigences ({inst['num_requirements']}) : {inst['requirements']}")
    print(f"  Tests ({len(inst['tests'])}) :")
    for nom, couverts in inst["tests"].items():
        print(f"    {nom} = {couverts}")
