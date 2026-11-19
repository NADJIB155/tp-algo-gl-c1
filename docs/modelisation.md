GL-C1 — Modélisation mathématique du problème Set Cover

1. Contexte et problématique

Avant chaque livraison d'un logiciel, l'équipe de développement exécute une suite de tests de régression afin de vérifier que les fonctionnalités déjà développées fonctionnent toujours correctement après les modifications du logiciel.

Chaque test permet de vérifier un sous-ensemble d'exigences fonctionnelles.

Exécuter tous les tests peut demander beaucoup de temps. Il est donc intéressant de sélectionner le plus petit nombre possible de tests tout en garantissant que toutes les exigences sont vérifiées.

Cette problématique peut être modélisée à l'aide du problème classique de couverture d'ensemble (Set Cover).

2. Modélisation mathématique

2.1. Données du problème

On considère :

- U = {e1, e2, ..., em} : l'ensemble des exigences fonctionnelles à couvrir.
- T = {t1, t2, ..., tn} : l'ensemble des tests disponibles.
- Si ⊆ U : l'ensemble des exigences couvertes par le test ti, pour i = 1, ..., n.

L'objectif est de sélectionner certains tests de manière à couvrir toutes les exigences.

2.2. Variables de décision

Pour chaque test ti, on définit une variable binaire :

xi ∈ {0, 1}

avec :

- xi = 1 si le test ti est sélectionné.
- xi = 0 si le test ti n'est pas sélectionné.

2.3. Fonction objectif

On cherche à minimiser le nombre total de tests sélectionnés.

La fonction objectif est :

Minimiser Z = x1 + x2 + ... + xn

2.4. Contraintes de couverture

Chaque exigence doit être couverte par au moins un test sélectionné.

Pour chaque exigence e appartenant à U, on impose :

Somme des xi pour tous les tests ti qui couvrent e ≥ 1.

Autrement dit, on additionne les variables des tests qui couvrent une exigence donnée. Le résultat doit être supérieur ou égal à 1.

Cette contrainte garantit que toutes les exigences sont couvertes.

2.5. Représentation matricielle des données

On peut également représenter les données du problème à l'aide d'une matrice de couverture A.

Cette matrice comporte :

- Une ligne pour chaque exigence.
- Une colonne pour chaque test.

On définit :

a(j,i) = 1 si le test ti couvre l'exigence ej.

a(j,i) = 0 sinon.

Ainsi, la valeur 1 indique qu'un test couvre une exigence, tandis que la valeur 0 indique qu'il ne la couvre pas.

Pour chaque exigence ej, la contrainte de couverture s'écrit :

a(j,1)x1 + a(j,2)x2 + ... + a(j,n)xn ≥ 1

Cette représentation permet de traduire le problème mathématique sous une forme exploitable par un programme informatique.