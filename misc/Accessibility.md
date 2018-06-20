# Accessibility

RGAA: http://references.modernisation.gouv.fr/rgaa-accessibilite
http://disic.github.io/guide-contribuer_accessible/ & https://github.com/access42/guide-auditeur

http://references.modernisation.gouv.fr/kit-daudit-modeles-pour-faire-des-audits-rgaa-3
http://disic.github.io/rgaa_methodologie/

## HTML
Exactly 1 <h1> per page

<html lang="en-US">

tabindex: 0 or -1 only, indicate if the element can take input focus and participate to keyboard navigation

ATTENTION <div> != <p> !!
-> les <div> sont non-navigables

FAITES des liens d'accès rapide.
Ils doivent etre VISIBLE (à minima au focus) : ils ne sont pas destinés aux aveugles

https://www.powermapper.com/tests/screen-readers/elements/

### ARIA

[Kit de survie du développeur aria](http://access42.net/Kit-de-survie-du-developpeur-ARIA-1-3)

[No ARIA is better than Bad ARIA](https://www.w3.org/TR/wai-aria-practices-1.1/#no_aria_better_bad_aria)


## Interfaces / GUI design

[DosAndDontsOnDesigningForAccessibility.gov.uk](https://accessibility.blog.gov.uk/2016/09/02/dos-and-donts-on-designing-for-accessibility/)

[Les écueils du contrôle de saisie dynamique](http://access42.net/Les-ecueils-du-controle-de-saisie-dynamique)


## Typographie
[Typographie et accessibilité - Marie Guillaumet, Access42](http://mixit.access42.net/):
- pas de `<meta name="viewport" content="maximum-scale=1.0,user-scalable=no" />`
- pour limiter la longueur des lignes à 80 caractères max : `max-width:80ch` -> adapte la taille du texte au caractère typographique choisis
- polices adaptées à la dyslexie, comme [Open Dyslexic](https://www.opendyslexic.org)
- "l’interlignage et l’espace entre les paragraphes devraient être équivalent à au moins 1,5 fois la taille du texte."
- "Si les textes ne sont pas justifiés, c’est l’idéal !"


## Libs

https://github.com/access42/AccessTooltip : JS function to make the title attribute accessible for keyboard users


## Outils
Quick check WEBAIM based [Wave](http://wave.webaim.org)

[asqatasun](https://doc.asqatasun.org/en/index.html)

Contrast checkers:
- [Colour Contrast Analyser](https://www.paciellogroup.com/resources/contrastanalyser/) (The Paciello Group) : top !
- [Chrome plugin Accessibility Developer Tools](https://chrome.google.com/webstore/detail/accessibility-developer-t/fpkknkljclfencbdbgkenhalefipecmb)
- [Color Oracle](http://colororacle.cartography.ch/) (Windows / Linux small tool - no snapshot)

Other tools:
- [HTML_CodeSniffer](http://squizlabs.github.io/HTML_CodeSniffer/)
- [Extension navigateur Assistant RGAA](https://github.com/DISIC/assistant-rgaa) : permet d'auditer des pages web en suivant le référentiel RGAA
- [PDF Accessibility Checker](http://www.access-for-all.ch/en/pdf-lab/pdf-accessibility-checker-pac/downloading-pac.html) (from Swiss foundation "Access for all")
- [Web Accessibility Toolbar for IE](https://github.com/ThePacielloGroup/WebAccessibilityToolbar/releases) (The Paciello Group)
- [Firefox WebDevelopper](https://addons.mozilla.org/fr/firefox/addon/web-developer/)
- [Accessibility Viewer](https://github.com/ThePacielloGroup/aviewer/releases) (The Paciello Group)
- [WCAG-Zoo](https://wcag-zoo.readthedocs.io/en/latest/commands.html) : Python command line tools that help provide basic validation of HTML against the accessibility guidelines laid out by the W3C Web Content Accessibility Guidelines 2.0

More: https://chezsoi.org/shaarli/?searchtags=Accessibility

### NVDA
https://www.nvda-fr.org/voix/ : installer la voix Hortense et augmenter le débit



## Présentation par Nicolas Chardon
Cas concrets:
- daltonien / malvoyants / aveugles
- navigation sans souris
- épileptiques (! fréquence de clignotement)

4 principes:
- perceptible
- utilisable
- compréhensible
- robuste

3 niveaux RGAA : A (non négociable), AA (atteignable mais difficile à maintenir), AAA

Automatiser tests: axe-core

Couples navigateur + lecteurs d'écrans:
- IE avec JAWS
- VoiceOver avec Safari
- Firefox avec NVDA: https://dequeuniversity.com/screenreaders/nvda-keyboard-shortcuts


## Formation Access42 par Jean-Pierre Villain

loi 1975 sur le handicap : ratio de personnes handicapées par boîte OU contribution à un fond d'aide
=> les boîtes préfèrent payer
2005 : cette contribution passe au-dessus du coût d'embauche
=> recrutement massif

En France:
- 800 000 sourds-muets
- 250 000 braillistes

Exemples d'outils:
- Windows: loupe (magnify.exe) : en général utilisé à 300%
- Windows: clavier visuel (osk.exe)

Beautiful Code : "When a Button Is All That Connects You to the World" (Dr. Arun Mehta on Stephen Hawking's eLocutor tool)
http://www.bapsi.org/Home/elocutor/beautiful-code

500 euros la voix de lecteur d'écran

HTML outline algorithm: pas implémenté pour le moment par les lecteurs d'écran (Google s'est prononcé comme quoi il ne le prendrait pas en compte)

Selon des études de psychologie cognitive,
les utilisateurs se contruisent leur propre carte mentale d'un site
basé sur leur objectif lorsqu'ils le visitent
et totalement décorélée de l'arobrescence "physique" du site

Règle des 3 clics : au-delà, chute exponentielle des réussites en navigation vers un objectif

<!-- la zone de contenu principale est structurée via un élément main, affectée du rôle main. C'est cet élément qui est la cible du lien d'évitement. Un tabindex=-1 permet de synchroniser la reprise du focus avec la tabulation pour certains navigateur.
L'élément main n'étant pas sectionnant, il est contenu dans un élément section afin de produire un plan du document cohérent. Cette section prends comme nom le premier titre h(x) de ses enfants, ici il n'y en a pas, pour améliorer la restitution une propriété aria-label permet de lui donner un nom plus pertinent.
Chaque sous-partie indépendante est structurée via un élément article pour construire le plan du document suivant :
-section machine de turing
 -article commandez une machine
 -article définition
 -article introduction
 -article exemple
-->
<section aria-label="Machine de turing">
  <main id="main" role="main" tabindex="-1">
    <article id="command">

Image décorative / informative : est-elle NECESSAIRE à la compréhension du contenu ?
+ descriptions aussi COURTES que possible, car elles perturbent la lecture et on ne sait quand exactement elles seront lues
On ne DECRIT pas les images aux aveugles

Les outils d'automatisation ne couvrent actuellement que 18% des critères d'accessibilité.

2012 : page d'accueil des JO de Londres provoque des crises d'épilepsie (2 cas au prognostic vital engagé)

Pause animated GIF (example I found: https://github.com/ctrl-freaks/freezeframe.js/)

Seuls Firefox & Safari sont capable d'augmenter UNIQUEMENT la taille de police.

La méthode "mobile-first" est idéale pour s'assurer que les polices de charactères utilisées sont linéarisables.

imgOverlappingTextWhenZooming {
    top: 6em; /* estimate 1st: position of the logo with font size 200% */
    margin-top: -60px; /* 2nd estimate: fix logo positionning with font size 100% */
}

350 combinaisons de couleurs non authorisées

:focus { /* Pour navigation clavier */
    outline: red 2px solid;
}

Les aveugles n'utilisent JAMAIS la touche tabulation.

Ne pas utiliser l'attribut placeholder:
- la valeur disparaît au focus
- contraste identique à disabled => invisible aux malvoyants

Ne pas utiliser de <hX> dans des <form>, mais plutôt des <legend> de <fieldset>

<input> : très important de donner un intitulé explicite et pertinent
-> si impossible visuellement à cause de la maquette, utiliser un title= ou un label

Changer le titre de la page en cas d'erreur de validation de formulaire

Messages d'erreur (exemple: en-tête en cas d'erreur de contrôle de formulaire) : role="alert"
