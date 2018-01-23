Notes :

def et ref seront utiles pour les derniers critères


Codage du graphe :
Noeuds : étiquette + valeur des variables (état)

Arcs : étiquettes des 2 noeuds du graphe associé + condition + opération

Chemins : liste des noeuds parcourus

Analyse de courverture :
- graphe générique en entrée
- critères de couverture : TA, ...
- jeu de tests : dictionnaire des valeurs des variables définissant des états initaux à tester.

Chaque éxécution du programme génère une succession d'états possbiles parcourus par le programme
Un critère regarde les patterns dans la liste autorisés ("pas plus de x fois la même Node dans le graphe, sinon boucle trop longue ..." )
