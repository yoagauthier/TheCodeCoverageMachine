Auteurs : Yoann Gauthier et Thibaut Seys

Date : 22/02/2018

# IVF - Projet : exécution symbolique et test structurel

## Structure du projet

Le projet contient deux dossiers `Examples` et `model`. Le premier contient l'ensemble des sources en language WHILE annoté et un ensemble de données d'entrées associées à ces sources. Le dossier `model` contient un ensemble de fichiers Python permettant de répondre à la problématique de couverture des critères. Voici une succinte description de son contenu :
- `model/abstract_syntax_tree.py` : implémente la classe ASTree correspondant à l'arbre de syntax abstraite du programme que l'on étudie.
- `model/control_flow_graph.py` : décrit l'ensemble des classes nécessaire à l'implémentation du graphe de contrôle.
- `model/criteria.py` : décrit la logique de l'ensemble des critères à couvrir.
- `model/error.py` : contient l'ensemble des exceptions personnalisées qui seront levées par notre projet.
- `model/nodes.py` : implémente l'ensemble de la logique des noeud de l'arbre de syntax abstraite.
- `model/parser.py` : contient le parser de programme nous permettant de construire l'arbre de syntax abstraite à partir du code source tokenizé.
- `model/tokenizer.py` : permet de tokenizer des sources en language WHILE annoté.

Notre projet contient également deux autres fichiers python : `main.py` et `coverage.py`. Le premier est un script travaillant sur le programme pgcd et des sets de test pour illustrer les différentes relations entre les critères appliquer à pgcd. Le second est une CLI permettant d'utiliser notre projet sur de nouveaux fichiers. Voici comment utiliser notre CLI :

```sh
coverage.py <source_filepath> <testsets_filepath> [--kTC=<k>] [--iTB=<i>]

Options:
    -h --help      Show this screen.
    -k --kTC=<k>   Length of k-path to check [default: 2].
    -i --iTB=<i>   Length of i-loop to check [default: 1].
```

Ainsi un premier exemple d'utilisation pourrait être :

```sh
python coverage.py Examples/fact.txt Examples/testsets.json -k 5
```

## Construction du graphe de contrôle

Nous allons construire le graphe de contrôle en effectuant les étapes suivantes :
1. Tokenizer le code source
2. Parser le code et construire l'arbre de syntax abstraite
3. Construire le graphe de contrôle à partir de l'arbre

### Tokenization du code source

Pour l'étape de tokenization du code source, nous distinguons deux opérations à réaliser. La première consiste à travailler sur le code source et supprimer toutes les lignes de commentaires commençant par '#'. Au cours de cette opération on va également retirer toutes les tabulations et espaces à chaque début de ligne. La seconde opération est celle de la tokenization qui consiste à transformer le code source en une liste de tokens. Le but de cette opération est d'arriver à isoler les différents types de token définis par notre grammaire :
- Les mots clés du language : 'skip', 'if', 'else', 'then', 'while' et 'do'.
- Les symboles du language : ';', ';' et ':='.
- Les parenthèses : '(', ')', '{' et '}'.
- Les opérateurs arithmétiques : '+', '-', '*' et '/'.
- Les comparateurs arithmétiques : '<', '<=', '>', '>=', et '='.
- Les opérateurs booléens : '!', '&' et '|'.
- Les variables booléennes : 'true' et 'false'.
- Les labels qui sont des nombres entiers. *Dans notre projet nous avons considéré que les labels devaient être en odre croissant (utile quand on explore les chemins pour avoir un graphe  de couvertue unidirectionnel, du point d'entrée du programme vers la sortie)*
- Les noms de variables qui sont composées seulement de lettres.

### Parsing et construction de l'arbre de syntax abstraite

Pour parser correctement la liste de tokens au préalable établie nous allons avoir besoin de definir la grammaire de notre language, qui est assez fortement parenthésée :
```
c ::=  l: skip
     | l: X := ( a )
     | c; c
     | if l: b then { c } else { c }
     | while l: b do { c }

a ::=  ( a + a ) | ( a - a ) | ( a / a ) | ( a * a )
     | variable
     | number

b ::=  !( b )
     | ( b & b )
     | ( b | b )
     | ( a < a ) | ( a <= a ) | ( a > a ) | ( a >= a ) | ( a = a )
     | true | false

l ::=  number
```
Nous construisons ensuite l'arbre de syntax abstraite de manière récursive sur la liste de tokens obtenue après l'étape précédente. Au niveau de l'architecture du code, nous avons un objet par type de noeud, ce qui nous permet d'avoir différentes fonctions d'évaluation et de transformation en string.

### Construction du graphe de contrôle

Pour construire le graph de contrôle, nous sommes partis de sa définition donnée pages 45 et 46 du polycopié de cours. Nous avons donc défini un sommet source, un sommet cible, un ensemble de sommets et un ensemble d'arêtes. Nous construisons ensuite de manière récursive le graphe en partant du noeud sommet de l'arbre de syntax abstraite et en appliquant les règles de construction. Ces règles sont également définies pages 45 et 46 du polycopié. Au niveau de l'architecture du code, pour les opérations et conditions qui étiquettent chaque arête, nous gardons les noeuds de l'arbre auparavant définis. Cela nous permet de garder toute l'information nécessaire sans la redéfinir une nouvelle fois.

## Vérification des critères

De manière générale, les critères suivent toujours la même logique. La première étape et d'établir un ensemble d'éléments à couvrir au sein du graphe de contrôle (un sommet, un chemin, etc...). La seconde est d'établir l'ensemble des éléments parmi les éléments à couvrir qui sont couverts par les chemins d'exécutions issus des données de tests. On compare ensuite ces deux ensembles pour obtenir le pourcentage de couverture du critère.

### TA - Tous les assignements

Les éléments à couvrir ici sont les sommets du graphe de contrôle répresentant une opération d'assignement. Pour obtenir cette liste on parcourt l'ensemble des sommets du graphe.

### TD - Toutes les décisions

Les éléments à couvrir ici sont les sommets du graphe de contrôle issu d'une condition, c'est-à-dire le contenu et la sortie d'un `while ... do ...` et d'un `if ... then ... else ...`. Pour obtenir cet ensemble, on parcourt l'ensemble des arêtes du graphe et on prend les noeuds enfants des arêtes ayant pour noeud parent un noeud portant l'opeartion while ou if.

### kTC - Tous les k-chemins

Les éléments à couvrir ici sont les chemins du graphe de contrôle ayant une longueur supérieure ou égale à k. On compare cette ensemble à l'ensemble des chemins d'exécution obtenus après évaluation des jeux de tests. Ici nous effectuons la comparaison sur l'égalité stricte des chemins et non l'inclusion afin de limiter les possibilités de passer plusieurs fois dans une boucle pour couvrir tous les chemins.

### iTB - Toutes les i-boucles

Les éléments à couvrir ici sont les chemins du graphe de contrôle passant par au plus i fois la même boucle au cours de la même itération, ce qui multiplie les possibilités pour les boucles imbriquées. On compare ensuite ces chemins au chemin d'exécution au sens de l'égalité.

### TDéf - Toutes les définitions

Les éléments à couvrir ici sont les des noeuds du graphe qui définissent des variables lors d'une éxécution. Lorsque les chemins sont exécutés, on vérifie que les variables correspondantes sont utilisée plus loin dans le chemin, et si c'est le cas le noeud de définition de la variable est correctement couvert.

### TU - Toutes les utilisations

Les éléments à courvir ici sont les chemins qui passent par la définition d'une variable et ensuite par son utilisation. On trouve ces chemins en descendant le graphe en retrouvant les noeuds correspondants au variables. Les éléments seront effectivement couverts si ces chemins (potentiellement partiels) sont empruntés par des chemin d'exécution.

### TDU - Tous les DU-chemins

Non implémenté

### TC - Toutes les conditions

Les éléments à couvrir ici sont l'évaluation à true et à false de chaque condition du graphe de contrôle. Au contraire des autres critères, nous avons ici besoin de reconstruire les chemins d'exécutions pour vérifier les évaluations des conditions.

## Relations sur les critères pour l'exemple du PGCD

Nous allons ici discuter des relations sur les critères pour l'exemple du programme pgcd se trouvant dans le fichier `Examples/pgcd.txt`. Nous nous baserons sur les résultats obtenus par l'éxécution du script `main.py`.

### TA et TD

Ici nous remarquons que la couverture de TA est équivalente à celle de TD. Cela vient du fait que nous sommes obligés de couvrir toutes les décisions du noeud if 2 pour couvrir toutes les assignations et toutes les décisions du noeud while 1 pour que le programme se termine et passe par le noeud if 2. Pour un autre programme, ces deux critères pourraient ne pas être équivalents si une décision mène à un ensemble d'instructions skip. Dans ce cas là on peut ne pas couvrir la décision menant à cette suite d'instruction et quand même couvrir l'ensemble des assignations.

### TD et kTC

Ici cela va dépendre de la valeur de k. Dans notre exemple du PGCD, si l'on prend k = 2, alors ce sont des sets de tests complétement différents qui vont jouer sur la couverture des critères. Cela vient du fait que les petits chemins ne passent pas dans les boucles. En revanche, si l'on augente la valeur de k, 5 pour notre exemple, alors le critère kTC sera plus fort que le critère TD. puisqu'en plus de couvrir les chemins de longueur minimum pour couvrir aussi les décisions, on devra couvrir les petits et grands chemins.

### kTC et iTB

Pour l'équivalence entre ces deux critères, cela va surtout dépendre des valeurs de k et i choisies. Dans notre exemple pour k = 5 et i = 1, on a les mêmes chemins à couvrir, donc les critères sont équivalents. Si la valeur de i induit des chemins de longueur plus grande que ceux de induit par k alors le critère kTC sera moins fort que le critère iTB. Sinon ce sera l'inverse.

### TDef et TA

Pour le cas de PGCD, les critères TDef et TA sont équivalents car toutes les définitions de PGCD sont utilisées dans la conditions terminal de la boucle while ayant pour label 1. Dans le cas d'un programme terminant avec une affectation de variables, alors on ne peut même par arriver à une couverture totale de ce critère puisqu'il serait impossible d'utiliser cette dernière définition.

### TU et TA

Dans l'exemple du PGCD, le critère TU implique de couvrir un chemin qui passe par toutes les assignations. Le critère TU est donc plus fort que le critère TA puisque celui-ci peut être satisfait par d'autres jeux de tests.

### TD et TC

Dans notre exemple du PGCD, TD et TC sont équivalents, car il n'y a pas d'opérateurs booléens binaires au sein des décisions. Si cela n'était pas le cas alors le critères TC serait plus dur à couvrir car il induirait plus de chemins à couvrir. 
