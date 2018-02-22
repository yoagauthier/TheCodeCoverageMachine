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

Notre projet contient également deux autres fichiers python : `main.py` et `coverage.py`. Le premier est un script travaillant sur quelques sources et sets de test pour illustrer le fonctionnement de notre logique. Le second est une CLI permettant d'utiliser notre projet sur de nouveaux fichiers.

## Construction du graphe de contrôle



## Vérification des critères 
