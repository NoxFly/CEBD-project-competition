# CEBD Project - Competition

Projet Python & SQLite réalisé par Leer0r (Lilian Russo) et NoxFly (Dorian Thivolle).

Toute partie graphique a été gérée par Qt Designer.

Nous avons testé avant d'envoyer, toutes les fenêtres s'ouvrent et aucune erreur ne survient (windows 10, python 3.7.8 64-bit).

Chaque branche git correspond à une partie donnée dans l'ennoncé.

## Partie 1

Compléter les fonctionnalités proposées :

1. [x] **Réaliser les extensions** du code fourni
	- [x] changer l'ui (`gui/fct_comp_1_changed.ui`)
	- [x] rajouter dateNaisSp (1.1)
	- [x] Améliorer l'interface pour rajouter des inputs (1.5)
	- [x] Changer l'input de la liste des épreuves v2 (1.6)
	- [x] Rajouter des restrictions sur les menus déroulants (1.7)
1. [x] **Créer les vues** comprenant les attributs calculés et mettre à jour l'interface
	- [x] Créer la vue LesSportifs et modifier l'affichage (1.2)
	- [x] Créer la vue LesEquipes et modifier l'affichage (1.4)
1. [x] **Créer une table LesDisciplines**, insérer les données fournies, effacer les données de LesEpreuves, insérer les données incluant les disciplines des épreuves et modifier l'affichage (1.3)

## Partie 2

- [x] **Créer des nouvelles fenêtres** dans l'interface
	- [x] Afficher l'**âge moyen des équipes qui ont gagné une médaille d'or** (2.1)
	- [x] Afficher le **classement des pays** selon leur nombre de médailles (pays, nbOr, nbArgent, nbBronze) (2.2)
- [x] Gérer les évènements et les associer à des nouvelles actions (2.1 + 2.2)


## Partie 3

Partie libre (2 exemples donnés).

- [ ] Imaginer des **nouvells fonctionnalités** de l'application (**insert**, **delete**, **update**, ...)
	- [ ] Gérer des **inscriptions** à des épreuves
	- [ ] Gérer des **résultats** aux épreuves
- [ ] Implémenter un **trigger**
- [ ] 3.1 : Imaginer des **nouvelles fonctionnalités** de l'application (**insert**, **delete**, **update**, ...)
	- [x] 3.1.1 : Gérer des **inscriptions** à des épreuves
        - [x] Faire l'interface graphique
        - [x] Link l'interface avec le code
        - [x] Faire les évents de chaque comboBox
        - [x] Sélectionner les équipes en fonction de la catégorie de l'épreuve
        - [x] Ajouter la sélection à la table LesInscription
	- [ ] 3.1.2 : Gérer des **résultats** aux épreuves
- [ ] 3.2 : Implémenter un **trigger**


Nous n'avons pas fini la partie 3 (3.1.2 et 3.2).
Nous avons seulement fait la partie `insert` de la 3.1.1.
Les fichiers de la partie 3 dans le dossier action sont `action_add_comp_*.py`.