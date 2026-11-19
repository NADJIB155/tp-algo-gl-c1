GL-C1 — Réduction polynomiale de Vertex Cover vers Set Cover

1. Introduction

Pour montrer que le problème Set Cover est NP-difficile, nous allons effectuer une réduction polynomiale depuis le problème Vertex Cover.

Vertex Cover est un problème connu comme étant NP-complet. L'idée est de transformer toute instance de Vertex Cover en une instance de Set Cover, tout en conservant la réponse au problème.

La réduction utilisée est :

Vertex Cover ≤p Set Cover

2. Rappel du problème Vertex Cover

Une instance de Vertex Cover est composée de :

- Un graphe non orienté G = (V, E), où V représente l'ensemble des sommets et E l'ensemble des arêtes.
- Un entier positif k.

La question est :

Existe-t-il au plus k sommets permettant de toucher toutes les arêtes du graphe ?

Un ensemble de sommets qui touche chaque arête au moins une fois est appelé une couverture de sommets (Vertex Cover).

3. Construction de la réduction

À partir d'une instance de Vertex Cover (G = (V, E), k), nous construisons une instance de Set Cover comme suit :

3.1. Construction de l'univers

L'univers de Set Cover correspond à l'ensemble des arêtes du graphe :

U = E

Chaque arête du graphe devient donc un élément de l'univers.

3.2. Construction des sous-ensembles

Pour chaque sommet v appartenant à V, nous créons un sous-ensemble S_v.

Ce sous-ensemble contient toutes les arêtes incidentes au sommet v, c'est-à-dire toutes les arêtes qui touchent ce sommet.

S_v = { e appartenant à E | e est incidente au sommet v }

Ainsi, chaque sommet du graphe correspond à un sous-ensemble de Set Cover.

3.3. Conservation de la borne

Nous conservons le même entier k dans la nouvelle instance.

On obtient donc l'instance de Set Cover :

(U, {S_v | v appartient à V}, k)

4. Exemple illustratif

Considérons un graphe triangulaire composé de trois sommets :

V = {A, B, C}

Et de trois arêtes :

E = {e1 = (A, B), e2 = (B, C), e3 = (A, C)}

4.1. Transformation en Set Cover

L'univers devient :

U = {e1, e2, e3}

Pour chaque sommet, on construit le sous-ensemble des arêtes qui lui sont incidentes :

- S_A = {e1, e3}
- S_B = {e1, e2}
- S_C = {e2, e3}

On obtient donc trois sous-ensembles.

4.2. Recherche d'une solution

Supposons que k = 2.

Dans Vertex Cover, choisissons les sommets A et B.

Ces deux sommets touchent toutes les arêtes du graphe.

Dans Set Cover, cela revient à sélectionner les sous-ensembles S_A et S_B.

Leur union est :

S_A ∪ S_B = {e1, e3} ∪ {e1, e2}

S_A ∪ S_B = {e1, e2, e3} = U

Toutes les arêtes sont donc couvertes avec deux sous-ensembles.

5. Preuve de l'équivalence

Nous devons démontrer que la réponse reste la même après la transformation.

Autrement dit :

(G, k) appartient à Vertex Cover si et seulement si (U, {S_v | v appartient à V}, k) appartient à Set Cover.

Cette équivalence se démontre dans les deux sens.

5.1. Sens direct : Vertex Cover vers Set Cover

Supposons qu'il existe une couverture de sommets C incluse dans V telle que :
C est l'ensemble des sommets sélectionnés dans Vertex Cover
|C| ≤ k

Puisque C est une couverture de sommets, chaque arête du graphe est incidente à au moins un sommet appartenant à C.

Or, chaque sommet v appartenant à C correspond à un sous-ensemble S_v contenant toutes les arêtes incidentes à ce sommet.

Par conséquent, les sous-ensembles correspondant aux sommets de C couvrent toutes les arêtes :

Union de tous les ensembles S_v, pour v appartenant à C = E = U

Le nombre de sous-ensembles sélectionnés est égal au nombre de sommets sélectionnés. Il est donc inférieur ou égal à k.

Ainsi, l'instance de Set Cover admet une couverture de taille au plus k.

5.2. Sens inverse : Set Cover vers Vertex Cover

Supposons maintenant qu'il existe une famille de sous-ensembles sélectionnés de taille au plus k qui couvre tout l'univers U = E.

Chaque sous-ensemble sélectionné S_v correspond à un sommet v du graphe.

Puisque tous les éléments de E sont couverts, chaque arête appartient à au moins un sous-ensemble sélectionné.

Cela signifie que chaque arête est incidente à au moins un des sommets correspondants.
Ces sommets forment donc une couverture de sommets de taille au plus k.

Ainsi, l'instance de Vertex Cover admet également une solution.

5.3. Conclusion de l'équivalence

Nous avons démontré les deux implications :

- Si Vertex Cover possède une solution de taille au plus k, alors Set Cover possède une solution de taille au plus k.
- Si Set Cover possède une solution de taille au plus k, alors Vertex Cover possède une solution de taille au plus k.

Par conséquent :

(G, k) appartient à Vertex Cover si et seulement si (U, {S_v | v appartient à V}, k) appartient à Set Cover.

6. Caractère polynomial de la réduction

La transformation peut être effectuée en temps polynomial.

En effet :

- On parcourt les sommets du graphe.
- Pour chaque sommet, on construit le sous-ensemble contenant ses arêtes incidentes.
- On conserve la même valeur de k.

La construction nécessite donc un nombre d'opérations polynomial par rapport à la taille du graphe.

La réduction est ainsi polynomiale :

Vertex Cover ≤p Set Cover

7. Conclusion

Vertex Cover est un problème NP-complet connu.

Comme Vertex Cover se réduit polynomialement à Set Cover, nous concluons que Set Cover est NP-difficile.

De plus, nous avons montré dans le fichier "preuve_np.md" que Set Cover appartient à NP.

Par conséquent, la version décisionnelle de Set Cover est NP-complète.

La version d'optimisation, qui consiste à trouver une couverture de cardinalité minimale, est NP-difficile.