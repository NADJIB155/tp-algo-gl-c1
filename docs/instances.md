GL-C1 — Jeux d'essai du problème Set Cover

1. Introduction

Afin d'évaluer les méthodes de résolution du problème Set Cover, nous utilisons plusieurs instances de tailles différentes.

Chaque instance contient :

- Un univers U représentant les exigences fonctionnelles.
- Une famille de sous-ensembles S représentant les tests de régression.
- Chaque test couvre un ensemble d'exigences.

L'objectif est de sélectionner le nombre minimal de tests permettant de couvrir toutes les exigences.

2. Petite instance

Le fichier "small_instance.json" contient :

- Nombre d'exigences : 5.
- Nombre de tests : 4.
- Univers U = {e1, e2, e3, e4, e5}.

Les tests disponibles sont :

- T1 = {e1, e2, e3}
- T2 = {e2, e4}
- T3 = {e3, e4, e5}
- T4 = {e4, e5}

Solution

On peut sélectionner les tests T1 et T3.

Leur union couvre toutes les exigences :

T1 ∪ T3 = {e1, e2, e3, e4, e5} = U

Aucun test seul ne couvre les cinq exigences.

La solution optimale est donc de sélectionner 2 tests.

3. Instance moyenne

Le fichier "medium_instance.json" contient :

- Nombre d'exigences : 10.
- Nombre de tests : 15.
- Univers U = {e1, e2, e3, e4, e5, e6, e7, e8, e9, e10}.

Chaque test couvre un sous-ensemble des exigences disponibles.

Cette instance permet d'étudier le comportement des méthodes de résolution sur un problème plus grand que la petite instance.

4. Intérêt des jeux d'essai

L'utilisation de deux instances de tailles différentes permet :

- De comprendre le fonctionnement du problème sur un petit exemple.
- D'étudier la sélection des tests nécessaires pour couvrir toutes les exigences.
- De comparer les résultats des algorithmes exacts et des heuristiques.
- D'observer l'évolution du temps de calcul lorsque la taille de l'instance augmente.

5. Fichiers associés

Les données des instances sont stockées au format JSON dans le dossier "instances/" :

- "small_instance.json"
- "medium_instance.json"

Ces fichiers sont destinés à être utilisés par les programmes de résolution du projet GL-C1.