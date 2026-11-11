#  TP Algorithmique Avancée & Complexité — Variante GL-C1

**Université Blida 1 — Génie Logiciel (2026-2027)**  
**Thème GL-C :** Tests de régression (Couverture complète avec un minimum de tests — *Set Cover*)

---

##  1. Description de la Problématique
Avant chaque livraison logicielle, l'équipe exécute une suite de tests de régression. Chaque test couvre un sous-ensemble d'exigences fonctionnelles.  
**Objectif (Variante GL-C1) :** Sélectionner un sous-ensemble de tests de **cardinalité minimale** permettant de couvrir 100 % des exigences.

### Modélisation Mathématique
* **Univers des exigences :** $U = \{e_1, e_2, \dots, e_m\}$
* **Ensemble des tests :** $S = \{S_1, S_2, \dots, S_n\}$ avec $S_i \subseteq U$
* **Variables de décision :** $x_i \in \{0, 1\}$ ($1$ si le test $S_i$ est sélectionné, $0$ sinon)
* **Fonction Objectif :**
  $$\min \sum_{i=1}^{n} x_i \quad \text{sous la contrainte} \quad \bigcup_{x_i = 1} S_i = U$$

---

##  2. Approche Algorithmique
1. **Algorithme Exact :** *Branch and Bound (B&B)* sur arbre binaire de décision (inclusion/exclusion d'un test $S_i$).
2. **Heuristique (non vue en cours) :** *Glouton de Chvátal* (sélection itérative du test maximisant le nombre de nouvelles exigences couvertes, garantie théorique $\ln(|U|) + 1$), utilisé comme **borne supérieure initiale** pour élaguer l'arbre du B&B.
3. **Complexité :** Preuve de NP-complétude par réduction polynomiale depuis *Vertex Cover* ($\text{Vertex Cover} \le_p \text{Set Cover}$).

---

##  3. Structure du Dépôt
* `/src` : Implémentation du Branch & Bound, Glouton de Chvátal et Parseur
* `/instances` : Petite instance de démo ($\le 8$ éléments) + instances OR-Library (Beasley)
* `/docs` : Modélisation formelle, arbre de recherche, preuve NP et slides (1er Décembre)
* `/web` : Application Web interactive de visualisation et comparaison

---

##  4. Équipe & Répartition (3 Binômes)
* **Binôme 1 (Modélisation & Preuve NP) :** Membre 1 & Membre 2
* **Binôme 2 (Algorithme Exact B&B & Heuristique Chvátal) :** Membre 3 & Membre 4
* **Binôme 3 (Git, Benchmarks OR-Library & Application Web) :** Membre 5 & Membre 6
