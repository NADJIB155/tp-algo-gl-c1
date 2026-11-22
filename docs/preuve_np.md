GL-C1 — Preuve d'appartenance de Set Cover à NP

1. Introduction

Le problème Set Cover consiste à sélectionner un nombre minimal de sous-ensembles parmi une famille donnée, de manière à couvrir tous les éléments de l'univers.

Pour étudier sa complexité, nous considérons la version décisionnelle du problème.

2. Version décisionnelle de Set Cover

La version décisionnelle transforme le problème d'optimisation en une question à réponse OUI ou NON.

2.1. Entrée

Une instance de Set Cover contient :

- Un univers U = {e1, e2, ..., em}.
- Une famille de sous-ensembles S = {S1, S2, ..., Sn}, avec chaque Si inclus dans U.
- Un entier positif k.

2.2. Question

Existe-t-il au plus k sous-ensembles dont l'union couvre tout l'univers U ?

Autrement dit, existe-t-il une sélection de sous-ensembles telle que :

- Le nombre de sous-ensembles sélectionnés est inférieur ou égal à k.
- Tous les éléments de U sont couverts.

La réponse est OUI si une telle sélection existe, et NON dans le cas contraire.

3. Appartenance de Set Cover à NP

Pour montrer que Set Cover appartient à NP, nous devons démontrer qu'une solution proposée peut être vérifiée en temps polynomial.

3.1. Certificat

Un certificat est une solution proposée sous la forme d'une liste des indices des sous-ensembles sélectionnés.

Par exemple, si la solution proposée est composée des sous-ensembles S1 et S3, le certificat contient les indices 1 et 3.

3.2. Vérification du certificat

Pour vérifier le certificat, nous contrôlons deux conditions :

Condition 1 : Respect de la borne k

Le nombre de sous-ensembles sélectionnés doit être inférieur ou égal à k.

Condition 2 : Couverture complète

L'union des sous-ensembles sélectionnés doit être égale à l'univers U.

Cela signifie que chaque élément de U doit apparaître dans au moins un des sous-ensembles sélectionnés.

3.3. Complexité de la vérification

La vérification consiste à :

1. Compter le nombre de sous-ensembles sélectionnés et vérifier qu'il ne dépasse pas k.
2. Parcourir les sous-ensembles sélectionnés.
3. Vérifier que chaque élément de l'univers U est couvert.

Ces opérations peuvent être effectuées en temps polynomial par rapport à la taille de l'instance.

Il est donc possible de vérifier efficacement une solution proposée, sans devoir rechercher toutes les solutions possibles.

Pour analyser le temps nécessaire à la vérification du certificat, on définit :

- m : le nombre total d'exigences dans l'univers U.
- n : le nombre total de tests disponibles.
- c : le nombre de tests sélectionnés dans le certificat.
- L : le nombre total d'exigences parcourues dans les tests sélectionnés.

La vérification s'effectue en trois étapes :

1. Vérification de la taille : on vérifie que le nombre de tests sélectionnés est inférieur ou égal à k. Cette opération prend un temps O(c).

2. Vérification de la couverture : on crée un tableau booléen de taille m, initialisé à Faux. Pour chaque test sélectionné, on parcourt les exigences qu'il couvre et on marque les exigences correspondantes dans le tableau. Cette opération prend un temps O(L).

3. Vérification finale : on parcourt le tableau pour vérifier que toutes les exigences sont couvertes. Cette étape prend un temps O(m).

Le temps total de vérification est donc :

O(c + L + m).

Or, c ≤ n et chaque test peut couvrir au maximum m exigences. Ainsi :

L ≤ c × m ≤ n × m.

Par conséquent, le temps de vérification est borné par O(n × m), ce qui est polynomial par rapport à la taille de l'instance.

3.4. Conclusion

Nous avons montré qu'un certificat de Set Cover peut être vérifié en temps polynomial.

Par conséquent :
Set Cover appartient à NP.

Notation :
Set Cover ∈ NP