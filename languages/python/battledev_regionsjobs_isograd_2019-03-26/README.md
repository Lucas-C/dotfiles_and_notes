Sujets et solutions persos : https://www.isograd.com/FR/solutionconcours.php

### Challenge 1

#### Énoncé
Le marathon est une épreuve sportive où les participants doivent parcourir 42 kilomètres.
Lors d'une soirée pizza avec vos amis, vous discutez du prochain marathon qui se tiendra dans votre ville.
Vos amis sont convaincus que vous n'êtes pas capable de terminer la course et vous, vous leur jurez que vous êtes sûr(e) de finir dans les 100 premiers.

Les paris sont lancés :

- si vous terminez dans le top 100, vous gagnez 1 000 euros ;
- si vous terminez le marathon, vous gagnez 100 euros ;
- si vous ne terminez pas le marathon, vous aurez juste perdu votre crédibilité.

Vous passez la ligne de départ à une certaine place, et tous les kilomètres, vous faites le point sur le nombre de personnes qui vous ont dépassées et celles que vous avez dépassées pour connaitre votre classement.

Dans ce challenge, on considère que le marathon fait exactement 42km et que si vous terminez après la 10 000ème place, cela veut dire que vous avez abandonné.

#### Objectif
Vous devez déterminer le montant gagné lors de votre pari.

#### Format des données
**Entrée**
- Ligne 1 : un entier compris entre 1 et 20 000 correspondant à votre classement lorsque vous passez la ligne de départ.
- Lignes 2 à 43 : deux entiers séparés par un espace représentant respectivement les personnes vous ayant dépassé(e) et celles que vous avez dépassées pour un kilomètre donné.

**Sortie**

Un entier correspondant au montant gagné lors de votre pari. Si vous ne gagnez rien, renvoyez la chaîne de caractères KO.

### Challenge 2

#### Énoncé

Vous cherchez depuis plusieurs mois un nouveau logement et vous avez enfin trouvé l'appartement de vos rêves. Seul petit problème, il est situé au 8ème étage et il n'y a pas d'ascenseur.
Le déménagement risque d'être compliqué. Vous décidez alors d'utiliser un monte-charge.
C'est super pratique car vous pouvez y déposer plusieurs cartons. Par contre, il ne supporte pas un poids strictement supérieur à 100 Kg.

Vous préférez ne pas vous compliquer la vie à optimiser les montées et vous décidez de poser les cartons sur le monte-charge dès que vous les sortez du camion.
Lorsque l'alarme signalant un poids excessif sonne, vous retirez le dernier carton et vous faites partir la machine.

Dans ce challenge, on considère que le déménagement ne concerne que des cartons et que la surface du monte-charge est suffisamment grande pour accueillir autant de cartons que l'on souhaite.
Par ailleurs, on vous garantit qu'un carton pèse entre 1 et 100 kg.

#### Objectif

Vous devez déterminer le nombre d'allers-retours que devra faire le monte-charge.

#### Format des données

**Entrée**
- Ligne 1 : un entier N compris entre 1 et 1 000 correspondant au nombre de cartons à faire monter.
- Lignes 2 à N+1 : un entier P correspondant au poids en kilogramme de chaque carton.

**Sortie**

Un entier correspondant au nombre d'allers-retours.

### Challenge 3

#### Énoncé

Après avoir surmonté un boss difficile de jeu vidéo, il est temps pour vous de récupérer votre récompense : vous arrivez dans une salle au trésor. Dans ce jeu, votre personnage peut ramasser deux sortes d'objets :

- les pièces d'or, qui augmentent votre richesse d'une unité ;
- les multiplicateurs, qui doublent la fortune dont vous disposez au moment de les ramasser. Donc plus vous êtes riche, plus vous vous enrichissez. (Toute ressemblance avec la réalité est une pure coïncidence.)

#### Objectif

La salle est représentée par une grille carrée de taille NxN, et vous commencez dans le coin en haut à gauche. L'objectif est de déterminer la séquence de mouvements qui vous permettra de maximiser votre butin.

#### Données

**Entrée**
- Ligne 1 : un entier N compris entre 1 et 20, représentant la taille de la grille.
- Lignes 2 à N+1 : les lignes de la carte représentées par des chaînes de N caractères. Les caractères de la ligne sont soit `o` (une pièce), soit `*` (un multiplicateur), soit `.` (vide).

**Sortie**

Une chaîne de caractères, indiquant les mouvements successifs à effectuer par votre personnage. Les caractères possibles sont les suivants :

- `^` : déplacement d'une case vers le haut
- `v` : déplacement d'une case vers le bas
- `<` : déplacement d'une case vers la gauche
- `>` : déplacement d'une case vers la droite
- `x` : ramasser l'objet sur la case actuelle

On demande que cette chaîne indique des mouvements légaux : le personnage ne doit pas sortir des bords de la grille, ni tenter de ramasser un objet sur une case ne contenant pas d'objet.
(Après avoir été ramassé, un objet disparaît de sa case.) Il faut de plus qu'elle atteigne le score le plus grand possible.

**Exemple**
```
4
....
o.*o
....
....
```
Une sortie acceptée est `vx>>>x<x` :

- on descend d'une case (v) sur la pièce la plus à gauche, puis on la ramasse (`x`) ;
- on se déplace de 3 cases vers la droite, pour atteindre la pièce de droite (en passant au-dessus du `*`, qu'on n'active pas encore);
- on ramasse cette seconde pièce, puis on se déplace vers la gauche sur le multiplicateur, qu'on ramasse à son tour.

Ainsi on obtient un total de 4 pièces (soit (1+1)×2), c'est bien le mieux qu'on puisse faire. Par exemple, si on avait utilisé le multiplicateur avant de récupérer la seconde pièce, on aurait obtenu seulement 3 pièces.
Il y a d'autres façons de se déplacer pour finir par avoir 4 pièces, qui sont également des solutions acceptées.

### Challenge 4

#### Énoncé

Récemment, votre clavier s'est mis à souffrir d'un fâcheux défaut : il arrive que des appuis sur des touches ne soient pas enregistrés. Par conséquent, vous qui aviez pris l'habitude de taper à toute vitesse sans vous relire, vous constatez maintenant quelques lettres manquantes dans vos textes.

Heureusement, la plupart du temps, le contexte permet de retrouver quel mot était censé se trouver là. Vous vous demandez donc quelles ambiguïtés sont susceptibles d'apparaître. Étant donnée une liste de mots, vous cherchez à savoir s'il est possible de tous les confondre en supprimant des lettres au milieu.

#### Objectif

L'objectif de ce challenge est donc de trouver une suite de lettres qui se retrouvent, dans le même ordre, dans tous mots de la liste en entrée. On voudrait que cette suite soit la plus longue possible, autrement dit que l'obtenir à partir des mots donnés implique le moins de suppressions de lettres possible.
(Pour simplifier, dans cet exercice, les mots de la liste seront tous de longueur 10.)

**Indication :** vous pouvez procéder par énumération exhaustive (force brute).

#### Données

**Entrée**
- Ligne 1 : un entier N entre 2 et 100, le nombre de mots différents.
- Lignes 2 à N+1 : sur chaque ligne, une chaîne de 10 caractères constituée uniquement des 26 lettres de l'alphabet en minuscule.

**Sortie**

Une suite de caractères de longueur maximale qui pourrait être obtenue à partir des mots en entrée par suppression de caractères.
Si les mots n'ont aucune lettre commune, affichez KO.

**Exemple**

Sur l'entrée suivante :
```
3
artificiel
algorithme
algebrique
```
Tous les 3 mots ci-dessus peuvent donner arie en supprimant 6 caractères. En supprimant 5 caractères ou moins, on ne pourrait pas obtenir une suite de lettres commune aux trois mots. C'est donc arie qu'il faut afficher.

Si l'entrée avait été :
```
2
artificiel
algorithme
```
Alors les réponses arie et arte auraient toutes les deux été acceptées.

Enfin, sur l'entrée suivante :
```
2
algorithme
algebrique
```
La réponse attendue est algrie.

### Challenge 5

#### Énoncé

Ce challenge est une variante de "Salle au trésor". Ici, votre personnage atterrit au milieu d'un couloir rempli de pièces d'or et de multiplicateurs de richesse. Ce couloir est représenté par une chaîne de caractères (en effet, il est unidimensionnel), dont les caractères peuvent être :

- `o` : pièce d'or, augmente votre richesse de 1
- `*` : multiplicateur, double votre richesse
- `X` : position initiale de votre personnage (ce caractère apparaît exactement une fois)
(Il n'y a pas de case vide.)

#### Objectif

Le couloir étant étroit, si une case contient un objet, et que vous souhaitez accéder à la partie du couloir qui se trouve derrière, vous êtes obligé de le ramasser (et donc d'activer son effet) si vous voulez libérer le passage.
L'objectif est toujours de déterminer la séquence de mouvements qui vous permettra de maximiser votre butin.

#### Données

**Entrée**
- Ligne 1 : un entier N compris entre 1 et 100, représentant la taille du couloir (nombre de caractères de la chaîne).
- Ligne 2 : une chaîne de caractères de longueur N, composée de `o`, `*` et `X` comme indiqué plus haut.

**Sortie**

Une chaîne de caractères, indiquant la suite de `o` et `*` que votre personnage ramassera dans l'ordre s'il se déplace de façon à optimiser le butin final.

**Exemple**
```
7
*o*X**o
```

La sortie attendue est `*o**o*`, ce qui correspond à :

- d'abord prendre le multiplicateur immédiatement à gauche de la position initiale ;
- ensuite prendre la pièce d'or à gauche ;
- ensuite partir vers la droite et ramasser les 3 objets successivement rencontrés jusqu'au bout du couloir ;
- enfin revenir à l'extrémité gauche et prendre le dernier multiplicateur.

### Challenge 6

???
